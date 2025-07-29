# Copyright 2022 DeepMind Technologies Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""""K-FAC loss functions objects, tags and registration functions."""
import abc
from typing import Sequence, Any

import distrax
import jax
import jax.numpy as jnp

from kfac_jax._src import layers_and_loss_tags as tags
from kfac_jax._src import utils
from typing_extensions import Self


Array = utils.Array
Numeric = utils.Numeric
PRNGKey = utils.PRNGKey
Shape = utils.Shape
DType = utils.DType
LossFunctionInputs = tuple[Array, ...]


def filter_none(
    **kwargs: Numeric | None,
) -> tuple[tuple[Numeric, ...], tuple[str, ...]]:
  args, args_names = zip(
      *[(value, name) for name, value in kwargs.items() if value is not None]
  )
  return args, args_names


# pylint: disable=g-one-element-tuple


class LossFunction(utils.Finalizable):
  """Abstract base class for loss functions.

  Note that unlike typical loss functions used in neural networks these are
  neither summed nor averaged over the batch and the output of evaluate() will
  not be a scalar. It is up to the user to then to correctly manipulate them as
  needed.

  Note that all of the GGN and Fisher (factor) multiplication methods defined in
  this class refer to the GGN and Fisher of just the loss function itself, which
  does *not* include the parameterized function (e.g. neural network) that
  generates the inputs (e.g. predictions or logits) feeding into the loss
  function.
  """

  def __init__(self, weight: Numeric):
    """Initializes the loss instance.

    Args:
      weight: The weight attributed to the loss.
    """
    if not isinstance(weight, (int, float)) and type(weight) is not object:  # pylint: disable=unidiomatic-typecheck
      if not isinstance(weight, Array) or weight.size > 1:
        raise ValueError("`weight` must be a scalar value.")
    super().__init__()
    self._weight = weight
    self.finalize()

  @property
  def dtype(self) -> DType:
    return self.parameter_dependants[0].dtype

  @property
  def weight(self) -> Numeric:
    """The weight of the loss."""
    return self._weight

  @property
  @abc.abstractmethod
  def targets(self) -> Array | None:
    """The targets (if present) used for evaluating the loss."""

  @property
  @abc.abstractmethod
  def parameter_dependants(self) -> tuple[Array, ...]:
    """All the parameter dependent arrays of the loss."""

  @property
  def num_parameter_dependants(self) -> int:
    """Number of parameter dependent arrays of the loss."""
    return len(self.parameter_dependants)

  @property
  @abc.abstractmethod
  def parameter_independants(self) -> tuple[Numeric | None, ...]:
    """All the parameter independent arrays of the loss."""

  @property
  def num_parameter_independants(self) -> int:
    """Number of parameter independent arrays of the loss."""
    return len(self.parameter_independants)

  def copy_with_different_inputs(
      self,
      parameter_dependants: Sequence[Array],
  ) -> Self:
    """Creates a copy of the loss function object, but with different inputs."""

    array_args, aux = self.tree_flatten()

    assert len(array_args) == (
        self.num_parameter_dependants + self.num_parameter_independants
    )

    array_args = (tuple(parameter_dependants) +
                  tuple(array_args[self.num_parameter_dependants:]))

    return self.tree_unflatten(aux, array_args)

  def tree_flatten(
      self,
  ) -> tuple[tuple[Numeric | None, ...], dict[str, Any] | None]:
    return self.parameter_dependants + self.parameter_independants, None

  @classmethod
  def tree_unflatten(
      cls,
      aux: dict[str, Any] | None,
      children: tuple[Numeric | None, ...],
  ) -> Self:
    return cls(*children, **(aux or {}))  # pytype: disable=not-instantiable

  def evaluate(
      self,
      targets: Array | None = None,
      coefficient_mode: str = "regular",
  ) -> Array:
    """Evaluates the loss function on the targets.

    Args:
      targets: The targets, on which to evaluate the loss. If this is set to
        ``None`` will use ``self.targets`` instead.
      coefficient_mode: Specifies how to use the weight of the loss in
        the returned value. There are three options:

        1. 'regular' - returns ``self.weight * loss(targets)``

        2. 'sqrt' - returns ``sqrt(self.weight) * loss(targets)``

        3. 'off' - returns ``loss(targets)``

    Returns:
      The value of the loss scaled appropriately by ``self.weight`` according to
      the coefficient mode.
    Raises:
      ValueError if both ``targets`` and ``self.targets`` are ``None``.
    """
    if targets is None and self.targets is None:
      raise ValueError("Cannot evaluate losses with unspecified targets.")
    elif targets is None:
      targets = self.targets
    if coefficient_mode == "regular":
      multiplier = self.weight
    elif coefficient_mode == "sqrt":
      multiplier = jnp.sqrt(self.weight)
    elif coefficient_mode == "off":
      multiplier = 1.0
    else:
      raise ValueError(f"Unrecognized coefficient_mode={coefficient_mode}.")
    return self._evaluate(targets) * multiplier

  @abc.abstractmethod
  def _evaluate(self, targets: Array) -> Array:
    """Evaluates the value of the loss, disregarding the weight."""

  def grad_of_evaluate(
      self,
      targets: Array | None,
      coefficient_mode: str,
  ) -> tuple[Array, ...]:
    """Evaluates the gradient of the loss function w.r.t. its inputs.

    Args:
      targets: The targets at which to evaluate the loss. If this is ``None``
        will use ``self.targets`` instead.
      coefficient_mode: The coefficient mode to use for evaluation. See
        ``self.evaluate`` for more details.

    Returns:
      The gradient of the loss function w.r.t. its inputs, at the provided
      targets.
    """
    def evaluate_sum(inputs: Sequence[Array]) -> Array:
      """Evaluates the loss summed over all axis, including batch etc."""
      instance = self.copy_with_different_inputs(inputs)
      return jnp.sum(instance.evaluate(targets, coefficient_mode))

    return jax.grad(evaluate_sum)(self.parameter_dependants)

  def multiply_ggn(
      self,
      vector: Sequence[Array],
  ) -> tuple[Array, ...]:
    """Right-multiplies a vector by the GGN of the loss function.

    Args:
      vector: The vector to multiply. Must have the same shape(s) as
        ``self.inputs``.

    Returns:
      The vector right-multiplied by the GGN. Will have the same shape(s) as
      ``self.inputs``.
    """
    return utils.scalar_mul(self.multiply_ggn_unweighted(vector), self.weight)

  @abc.abstractmethod
  def multiply_ggn_unweighted(
      self,
      vector: Sequence[Array],
  ) -> tuple[Array, ...]:
    """Unweighted version of :func:`~LossFunction.multiply_ggn`."""

  def multiply_ggn_factor(
      self,
      vector: Array,
  ) -> tuple[Array, ...]:
    """Right-multiplies a vector by a factor B of the GGN.

    Note that B can be any matrix satisfying ``B * B^T = G`` where ``G`` is the
    GGN, but will agree with the one used in the other methods of this class.

    Args:
      vector: The vector to multiply. Must be of the shape(s) given by
        'self.ggn_factor_inner_shape'.

    Returns:
      The vector right-multiplied by B. Will be of the same shape(s) as
      ``self.inputs``.
    """
    return utils.scalar_mul(
        self.multiply_ggn_factor_unweighted(vector), jnp.sqrt(self.weight))

  @abc.abstractmethod
  def multiply_ggn_factor_unweighted(
      self, vector: Array
  ) -> tuple[Array, ...]:
    """Unweighted version of :func:`~LossFunction.multiply_ggn_factor`."""

  def multiply_ggn_factor_transpose(
      self,
      vector: Sequence[Array],
  ) -> Array:
    """Right-multiplies a vector by the transpose of a factor B of the GGN.

    Note that B can be any matrix satisfying ``B * B^T = G`` where G is the GGN,
    but will agree with the one used in the other methods of this class.

    Args:
      vector: The vector to multiply. Must have the same shape(s) as
        ``self.inputs``.

    Returns:
      The vector right-multiplied by B^T. Will be of the shape(s) given by
      ``self.ggn_factor_inner_shape``.
    """
    return utils.scalar_mul(
        self.multiply_ggn_factor_transpose_unweighted(vector),
        jnp.sqrt(self.weight))

  @abc.abstractmethod
  def multiply_ggn_factor_transpose_unweighted(
      self,
      vector: Sequence[Array],
  ) -> Array:
    """Unweighted version of :func:`~LossFunction.multiply_ggn_factor_transpose`."""

  def multiply_ggn_factor_replicated_one_hot(
      self,
      index: tuple[int, ...],
  ) -> tuple[Array, ...]:
    """Right-multiplies a replicated-one-hot vector by a factor B of the GGN.

    A replicated-one-hot vector means a tensor which, for each slice along the
    batch dimension (assumed to be dimension 0), is 1.0 in the entry
    corresponding to the given index and 0 elsewhere.

    Note that B can be any matrix satisfying ``B * B^T = G`` where G is the GGN,
    but will agree with the one used in the other methods of this class.

    The reason that we have this special method and don't just use
    multiply_ggn_factor is that we can be more efficient by using knowledge of
    the zero-entries in the replicated-one-hot vector.

    Args:
      index: A tuple representing in the index of the entry in each slice that
        is 1.0 (excluding the batch dimension). Note that len(index) must be
        equal to the number of elements of the ``ggn_factor_inner_shape`` tensor
        minus one.

    Returns:
      The vector right-multiplied by B^T. Will be of the same shape(s) as the
      ``inputs`` property.
    """
    return utils.scalar_mul(
        self.multiply_ggn_factor_replicated_one_hot_unweighted(index),
        jnp.sqrt(self.weight))

  @abc.abstractmethod
  def multiply_ggn_factor_replicated_one_hot_unweighted(
      self,
      index: tuple[int, ...],
  ) -> tuple[Array, ...]:
    """Unweighted version of :func:`~LossFunction.multiply_ggn_factor_replicated_one_hot`."""

  @property
  @abc.abstractmethod
  def ggn_factor_inner_shape(self) -> Shape:
    """The shape of the array returned by `self.multiply_ggn_factor`."""


class NegativeLogProbLoss(LossFunction):
  """Base class for loss functions that represent negative log-probability."""

  @property
  def parameter_dependants(self) -> tuple[Array, ...]:
    return self.params

  @property
  @abc.abstractmethod
  def params(self) -> tuple[Array, ...]:
    """Parameters to the underlying distribution."""

  def multiply_fisher(
      self,
      vector: Sequence[Array],
  ) -> tuple[Array, ...]:
    """Right-multiplies a vector by the Fisher.

    Args:
      vector: The vector to multiply. Must have the same shape(s) as
        ``self.inputs``.

    Returns:
      The vector right-multiplied by the Fisher. Will have of the same shape(s)
      as ``self.inputs``.
    """
    return utils.scalar_mul(
        self.multiply_fisher_unweighted(vector), self.weight)

  @abc.abstractmethod
  def multiply_fisher_unweighted(
      self,
      vector: Sequence[Array],
  ) -> tuple[Array, ...]:
    """Unweighted version of :func:`~LossFunction.multiply_fisher`."""

  def multiply_fisher_factor(
      self,
      vector: Array,
  ) -> tuple[Array, ...]:
    """Right-multiplies a vector by a factor B of the Fisher.

    Note that B can be any matrix satisfying ``B * B^T = F`` where F is the
    Fisher, but will agree with the one used in the other methods of this class.

    Args:
      vector: The vector to multiply. Must have the same shape(s) as
        ``self.fisher_factor_inner_shape``.

    Returns:
      The vector right-multiplied by B. Will have the same shape(s) as
      ``self.inputs``.
    """
    return utils.scalar_mul(
        self.multiply_fisher_factor_unweighted(vector), jnp.sqrt(self.weight))

  @abc.abstractmethod
  def multiply_fisher_factor_unweighted(
      self,
      vector: Array,
  ) -> tuple[Array, ...]:
    """Unweighted version of  :func:`~LossFunction.multiply_fisher_factor`."""

  def multiply_fisher_factor_transpose(
      self,
      vector: Sequence[Array],
  ) -> Array:
    """Right-multiplies a vector by the transpose of a factor B of the Fisher.

    Note that B can be any matrix satisfying ``B * B^T = F`` where F is the
    Fisher, but will agree with the one used in the other methods of this class.

    Args:
      vector: The vector to multiply. Must have the same shape(s) as
        ``self.inputs``.

    Returns:
      The vector right-multiplied by B^T.  Will have the shape given by
      ``self.fisher_factor_inner_shape``.
    """
    return utils.scalar_mul(
        self.multiply_fisher_factor_transpose_unweighted(vector),
        jnp.sqrt(self.weight))

  @abc.abstractmethod
  def multiply_fisher_factor_transpose_unweighted(
      self,
      vector: Sequence[Array],
  ) -> Array:
    """Unweighted version of :func:`~LossFunction.multiply_fisher_factor_transpose`."""

  def multiply_fisher_factor_replicated_one_hot(
      self,
      index: tuple[int, ...],
  ) -> tuple[Array, ...]:
    """Right-multiplies a replicated-one-hot vector by a factor B of the Fisher.

    A replicated-one-hot vector means a tensor which, for each slice along the
    batch dimension (assumed to be dimension 0), is 1.0 in the entry
    corresponding to the given index and 0 elsewhere.

    Note that B can be any matrix satisfying ``B * B^T = F`` where F is the
    Fisher, but will agree with the one used in the other methods of this class.

    The reason that we have this special method and don't just use
    multiply_fisher_factor is that we can be more efficient by using knowledge
    of the zero-entries in the replicated-one-hot vector.

    Args:
      index: A tuple representing in the index of the entry in each slice that
        is 1.0 (excluding the batch dimension). Note that len(index) must be
        equal to the number of elements of the ``fisher_factor_inner_shape``
        tensor minus one.

    Returns:
      The vector right-multiplied by B. Will have the same shape(s) as
      ``self.inputs``.
    """
    return utils.scalar_mul(
        self.multiply_fisher_factor_replicated_one_hot_unweighted(index),
        jnp.sqrt(self.weight))

  @abc.abstractmethod
  def multiply_fisher_factor_replicated_one_hot_unweighted(
      self,
      index: tuple[int, ...],
  ) -> tuple[Array, ...]:
    """Unweighted version of :func:`~LossFunction.multiply_fisher_factor_replicated_one_hot`."""

  @property
  @abc.abstractmethod
  def fisher_factor_inner_shape(self) -> Shape:
    """The shape of the array returned by :func:`~LossFunction.multiply_fisher_factor`."""

  @abc.abstractmethod
  def sample(self, rng: PRNGKey) -> Array:
    """Sample ``targets`` from the underlying distribution."""

  def grad_of_evaluate_on_sample(
      self,
      rng: Array,
      coefficient_mode: str,
  ) -> tuple[Array, ...]:
    """Evaluates the gradient of the log probability on a random sample.

    Args:
      rng: Jax PRNG key for sampling.
      coefficient_mode: The coefficient mode to use for evaluation.

    Returns:
      The gradient of the log probability of targets sampled from the
      distribution.
    """
    return self.grad_of_evaluate(self.sample(rng), coefficient_mode)


class NaturalParamsNegativeLogProbLoss(NegativeLogProbLoss, abc.ABC):
  """Negative log-probability loss, whose inputs are natural parameters.

  We will take the GGN of the loss to be the Fisher associated with the
  distribution, which also happens to be equal to the Hessian for this class
  of loss functions. See https://arxiv.org/abs/1412.1193 for details.

  Natural parameters are defined for exponential-family models. See for
  example `wikipedia <https://en.wikipedia.org/wiki/Exponential_family>`__.
  """

  def multiply_ggn_unweighted(
      self,
      vector: Sequence[Array],
  ) -> tuple[Array, ...]:
    return self.multiply_fisher_unweighted(vector)

  def multiply_ggn_factor_unweighted(
      self,
      vector: Array,
  ) -> tuple[Array, ...]:
    return self.multiply_fisher_factor_unweighted(vector)

  def multiply_ggn_factor_transpose_unweighted(
      self,
      vector: Sequence[Array],
  ) -> Array:
    return self.multiply_fisher_factor_transpose_unweighted(vector)

  def multiply_ggn_factor_replicated_one_hot_unweighted(
      self,
      index: tuple[int, ...],
  ) -> tuple[Array, ...]:
    return self.multiply_fisher_factor_replicated_one_hot_unweighted(index)

  @property
  def ggn_factor_inner_shape(self) -> Shape:
    return self.fisher_factor_inner_shape


class DistributionNegativeLogProbLoss(NegativeLogProbLoss):
  """Negative log-probability loss that uses a Distrax distribution."""

  @property
  @abc.abstractmethod
  def dist(self) -> distrax.Distribution:
    """The underlying Distrax distribution."""

  def _evaluate(self, targets: Array) -> Array:
    # keeps leading dims intact
    return -self.dist.log_prob(targets)  # pytype: disable=bad-return-type

  def sample(self, rng: PRNGKey) -> Array:
    return self.dist.sample(seed=rng)  # pytype: disable=bad-return-type


@jax.tree_util.register_pytree_node_class
class NormalMeanNegativeLogProbLoss(DistributionNegativeLogProbLoss,
                                    NaturalParamsNegativeLogProbLoss):
  """Loss log prob loss for a normal distribution parameterized by a mean vector.

  Note that the covariance is treated as the identity divided by 2.
  Also note that the Fisher for such a normal distribution with respect the mean
  parameter is given by:

     F = (1 / variance) * I
  """

  def __init__(
      self,
      mean: Array,
      targets: Array | None = None,
      variance: Numeric = 0.5,
      weight: Numeric = 1.0,
      normalize_log_prob: bool = True,
  ):
    """Initializes the loss instance.

    Args:
      mean: The mean of the normal distribution.
      targets: Optional targets to use for evaluation.
      variance: The scalar variance of the normal distribution.
      weight: The weight of the loss.
      normalize_log_prob: Whether the log prob should include the standard
        normalization constant for Gaussians (which is additive and depends
        on the variance).
    """

    if not isinstance(variance, (int, float)) and type(variance) is not object:  # pylint: disable=unidiomatic-typecheck
      if not isinstance(variance, Array) or variance.size > 1:
        raise ValueError("`variance` must be either a python scalar or a "
                         "scalar array.")
    self._mean = mean
    self._targets = targets
    self._variance = variance
    self._normalize_log_prob = normalize_log_prob

    super().__init__(weight=weight)

  @property
  def mean(self) -> Array:
    return self._mean

  @property
  def variance(self) -> Numeric:
    return self._variance

  @property
  def targets(self) -> Array | None:
    return self._targets

  @property
  def normalize_log_prob(self) -> bool:
    return self._normalize_log_prob

  @property
  def parameter_independants(self) -> tuple[Numeric | None, ...]:
    return self._targets, self._variance, self._weight

  @property
  def dist(self) -> distrax.MultivariateNormalDiag:
    scale_diag = jnp.full_like(self.mean, jnp.sqrt(self.variance))
    return distrax.MultivariateNormalDiag(loc=self.mean, scale_diag=scale_diag)

  @property
  def params(self) -> tuple[Array]:
    return (self.mean,)

  @property
  def fisher_factor_inner_shape(self) -> Shape:
    return self._mean.shape

  def _evaluate(self, targets: Array) -> Array:

    if self.normalize_log_prob:
      return super()._evaluate(targets)
    else:
      # keeps leading dims intact
      return 0.5 * jnp.sum(jnp.square(
          self.mean - targets), axis=range(1, targets.ndim)) / self.variance

  def multiply_fisher_unweighted(
      self,
      vector: Sequence[Array]
  ) -> tuple[Array]:
    return (vector[0] / self.variance,)

  def multiply_fisher_factor_unweighted(
      self,
      vector: Array,
  ) -> tuple[Array]:
    return (vector / jnp.sqrt(self.variance),)

  def multiply_fisher_factor_transpose_unweighted(
      self,
      vector: Sequence[Array],
  )  -> Array:
    # it's symmetric
    return self.multiply_fisher_factor_unweighted(vector[0])[0]

  def multiply_fisher_factor_replicated_one_hot_unweighted(
      self,
      index: tuple[int, ...],
  ) -> tuple[Array]:

    ones_slice = jnp.ones([self.mean.shape[0]] + [1] * (self.mean.ndim - 1))

    output_slice = ones_slice / jnp.sqrt(self.variance)

    return (insert_slice_in_zeros(output_slice, self.mean.shape, (0,) + index),)


# TODO(jamesmartens): This class was copied from the TF K-FAC codebase and is
# untested with probable bugs. Test it?
@jax.tree_util.register_pytree_node_class
class NormalMeanVarianceNegativeLogProbLoss(DistributionNegativeLogProbLoss):
  """Negative log prob loss for a normal distribution with mean and variance.

  This class parameterizes a multivariate normal distribution with n independent
  dimensions. Unlike :class:`~NormalMeanNegativeLogProbLoss`, this class does
  not assume the variance is held constant. The Fisher Information for n = 1 is
  given by:

  F = [[1 / variance,                0],
       [           0, 0.5 / variance^2]]

  where the parameters of the distribution are concatenated into a single
  vector as ``[mean, variance]``. For n > 1, the mean parameter vector is
  concatenated with the variance parameter vector. For further details checkout
  the Wikipedia `page
  <https://en.wikipedia.org/wiki/Fisher_information#Multivariate_normal_distribution>`__.
  """

  def __init__(
      self,
      mean: Array,
      variance: Array,
      targets: Array | None = None,
      weight: Numeric = 1.0,
  ):
    """Initializes the loss instance.

    Args:
      mean: The mean of the normal distribution.
      variance: The variance of the normal distribution.
      targets: Optional targets to use for evaluation.
      weight: The weight of the loss.
    """
    if mean.ndim != 2:
      raise ValueError("Only 2D mean array is supported.")
    if variance.ndim != 2:
      raise ValueError("Only 2D variance array is supported.")
    self._mean = mean
    self._variance = variance
    self._targets = targets
    super().__init__(weight=weight)

  @property
  def targets(self) -> Array | None:
    return self._targets

  @property
  def parameter_independants(self) -> tuple[Numeric | None, ...]:
    return self._targets, self._weight

  @property
  def dist(self) -> distrax.MultivariateNormalDiag:
    return distrax.MultivariateNormalDiag(
        loc=self._mean, scale_diag=jnp.sqrt(self._variance))

  @property
  def params(self) -> tuple[Array, Array]:
    return self._mean, self._variance

  @property
  def _fisher_mean(self) -> Array:
    """The Fisher w.r.t. to the mean parameters."""
    return 1. / self._variance

  @property
  def _fisher_mean_factor(self) -> Array:
    """The Fisher factor w.r.t. to the mean parameters."""
    return jnp.sqrt(self._fisher_mean)

  @property
  def _fisher_var(self) -> Array:
    """The Fisher w.r.t. to the variance parameters."""
    return 1. / (2 * jnp.square(self._variance))

  @property
  def _fisher_var_factor(self) -> Array:
    """The Fisher factor w.r.t. to the variance parameters."""
    return 1. / (jnp.sqrt(2.) * self._variance)

  def multiply_fisher_unweighted(
      self,
      vector: Sequence[Array],
  ) -> tuple[Array, Array]:
    mean_vec, var_vec = vector
    return self._fisher_mean * mean_vec, self._fisher_var * var_vec

  def multiply_fisher_factor_unweighted(
      self,
      vector: Array,
  ) -> tuple[Array, Array]:
    mean_vec, var_vec = jnp.split(vector, 2, axis=-1)
    result_mean_vec = self._fisher_mean_factor * mean_vec
    result_var_vec = self._fisher_var_factor * var_vec
    return result_mean_vec, result_var_vec

  def multiply_fisher_factor_transpose_unweighted(
      self,
      vector: Sequence[Array],
  ) -> Array:
    mean_vec, var_vec = vector
    result_mean_vec = self._fisher_mean_factor * mean_vec
    result_var_vec = self._fisher_var_factor * var_vec
    return jnp.concatenate([result_mean_vec, result_var_vec], axis=-1)

  def multiply_fisher_factor_replicated_one_hot_unweighted(
      self,
      index: tuple[int, ...],
  ) -> tuple[Array, Array]:
    [index] = index

    if index < int(self._mean.shape[-1]):
      # Index corresponds to mean parameter.
      mean_slice = self._fisher_mean_factor[:, index][..., None]
      mean_output = insert_slice_in_zeros(
          mean_slice, self._mean.shape, [0, index])
      var_output = jnp.zeros_like(mean_output)

    else:
      index -= int(self._mean.shape[-1])
      # Index corresponds to variance parameter.
      var_slice = self._fisher_var_factor[:, index][..., None]
      var_output = insert_slice_in_zeros(
          var_slice, self._variance.shape, [0, index])
      mean_output = jnp.zeros_like(var_output)

    return mean_output, var_output

  @property
  def fisher_factor_inner_shape(self) -> Shape:
    return self._mean.shape[:-1] + (self._mean.shape[-1] * 2,)

  def multiply_ggn_unweighted(
      self,
      vector: Sequence[Array],
  ) -> tuple[Array, ...]:
    raise NotImplementedError()

  def multiply_ggn_factor_unweighted(
      self, vector: Array
  ) -> tuple[Array, ...]:
    raise NotImplementedError()

  def multiply_ggn_factor_transpose_unweighted(
      self,
      vector: Sequence[Array],
  ) -> Array:
    raise NotImplementedError()

  def multiply_ggn_factor_replicated_one_hot_unweighted(
      self,
      index: tuple[int, ...],
  ) -> tuple[Array, ...]:
    raise NotImplementedError()

  @property
  def ggn_factor_inner_shape(self) -> Shape:
    raise NotImplementedError()


@jax.tree_util.register_pytree_node_class
class MultiBernoulliNegativeLogProbLoss(DistributionNegativeLogProbLoss,
                                        NaturalParamsNegativeLogProbLoss):
  """Negative log prob loss for multiple Bernoulli distributions parametrized by logits.

  Represents N independent Bernoulli distributions where N = len(logits). Its
  Fisher Information matrix is given by ``F = diag(p * (1-p))``, where
  ``p = sigmoid(logits)``.

  As F is diagonal with positive entries, its factor B is
  ``B = diag(sqrt(p * (1-p)))``.
  """

  def __init__(
      self,
      logits: Array,
      targets: Array | None = None,
      weight: Numeric = 1.0,
  ):
    """Initializes the loss instance.

    Args:
      logits: The logits of the Bernoulli distribution.
      targets: Optional targets to use for evaluation.
      weight: The weight of the loss.
    """
    self._logits = logits
    self._targets = targets
    super().__init__(weight=weight)

  @property
  def targets(self) -> Array | None:
    return self._targets

  @property
  def parameter_independants(self) -> tuple[Numeric | None, ...]:
    return self._targets, self._weight

  @property
  def dist(self) -> distrax.Bernoulli:
    return distrax.Bernoulli(logits=self._logits, dtype=jnp.int32)

  @property
  def _probs(self) -> Array:
    """The probabilities of the underlying Bernoulli distribution."""
    return self.dist.probs  # pytype: disable=bad-return-type

  @property
  def params(self) -> tuple[Array]:
    return (self._logits,)

  @property
  def fisher_factor_inner_shape(self) -> Shape:
    return self._logits.shape

  def multiply_fisher_unweighted(
      self,
      vector: Sequence[Array]
  ) -> tuple[Array]:
    return (self._probs * (1 - self._probs) * vector[0],)

  def multiply_fisher_factor_unweighted(
      self,
      vector: Array
  ) -> tuple[Array]:
    return (utils.stable_sqrt(self._probs * (1 - self._probs)) * vector,)

  def multiply_fisher_factor_transpose_unweighted(
      self,
      vector: Sequence[Array]
  ) -> Array:
    # it's symmetric in this case
    return self.multiply_fisher_factor_unweighted(vector[0])[0]

  def multiply_fisher_factor_replicated_one_hot_unweighted(
      self,
      index: tuple[int, ...],
  ) -> tuple[Array]:

    probs_slice = jnp.expand_dims(self._probs[(slice(None),) + index],
                                  axis=range(1, len(self._probs.shape)))

    output_slice = utils.stable_sqrt(probs_slice * (1 - probs_slice))

    return (insert_slice_in_zeros(output_slice, self._logits.shape,
                                  (0,) + index),)


@jax.tree_util.register_pytree_node_class
class CategoricalLogitsNegativeLogProbLoss(DistributionNegativeLogProbLoss,
                                           NaturalParamsNegativeLogProbLoss):
  """Negative log prob loss for a categorical distribution parameterized by logits.


  Note that the Fisher (for a single case) of a categorical distribution, with
  respect to the natural parameters (i.e. the logits), is given by
  ``F = diag(p) - p*p^T``, where ``p = softmax(logits)``. F can be factorized as
  ``F = B * B^T``, where ``B = diag(q) - p*q^T`` and ``q`` is the entry-wise
  square root of ``p``. This is easy to verify using the fact that ``q^T*q = 1``
  .
  """

  def __init__(
      self,
      logits: Array,
      targets: Array | None = None,
      mask: Array | None = None,
      weight: Numeric = 1.0,
  ):
    """Initializes the loss instance.

    Args:
      logits: The logits of the Categorical distribution.
      targets: Optional targets to use for evaluation, which specify an integer
        index of the correct class. Must be of shape ``logits.shape[:-1]``.
      mask: Optional mask to apply to losses over the batch. Should be
        0/1-valued and of shape ``logits.shape[:-1]``. The tensors returned by
        ``evaluate`` and ``grad_of_evaluate``, as well as the various matrix
        vector products, will be multiplied by mask (with broadcasting to later
        dimensions).
      weight: The weight of the loss.
    """
    if (mask is not None and type(mask) is not object and  # pylint: disable=unidiomatic-typecheck
        mask.shape != logits.shape[:-1]):
      raise ValueError("If provided, mask.shape must be equal to "
                       "logits.shape[:-1].")

    self._logits = logits
    self._targets = targets
    self._mask = mask

    super().__init__(weight=weight)

  @property
  def targets(self) -> Array | None:
    return self._targets

  @property
  def mask(self) -> Array | None:
    return self._mask

  @property
  def parameter_independants(self) -> tuple[Numeric | None, ...]:
    return self._targets, self._mask, self._weight

  @property
  def dist(self) -> distrax.Categorical:
    return distrax.Categorical(logits=self._logits, dtype=jnp.int32)

  def _evaluate(self, targets: Array) -> Array:

    evl = super()._evaluate(targets)

    if self.mask is not None:
      return evl * self.mask

    else:
      return evl

  @property
  def _probs(self) -> Array:
    """The probabilities of the underlying Bernoulli distribution."""

    if self.mask is not None:
      return self.dist.probs * self.mask[..., None]
    else:
      return self.dist.probs

  @property
  def _sqrt_probs(self) -> Array:
    """The square root of ``self.probs``."""

    if self.mask is not None:
      return utils.stable_sqrt(self.dist.probs) * self.mask[..., None]
    else:
      return utils.stable_sqrt(self.dist.probs)

  @property
  def params(self) -> tuple[Array]:
    return (self._logits,)

  @property
  def fisher_factor_inner_shape(self) -> Shape:
    return self._logits.shape

  def multiply_fisher_unweighted(
      self,
      vector: Sequence[Array]
  ) -> tuple[Array]:

    assert len(vector) == 1

    probs = self._probs

    fisher_product = vector[0] * probs - probs * jnp.sum(
        vector[0] * probs, axis=-1, keepdims=True)

    return (fisher_product,)

  def multiply_fisher_factor_unweighted(
      self,
      vector: Array
  ) -> tuple[Array]:

    probs = self._probs

    sqrt_probs = self._sqrt_probs

    return (sqrt_probs * vector - probs * jnp.sum(
        sqrt_probs * vector, axis=-1, keepdims=True),)

  def multiply_fisher_factor_transpose_unweighted(
      self,
      vector: Sequence[Array]
  ) -> Array:

    assert len(vector) == 1

    probs = self._probs

    sqrt_probs = self._sqrt_probs

    return sqrt_probs * vector[0] - sqrt_probs * jnp.sum(
        probs * vector[0], axis=-1, keepdims=True)

  def multiply_fisher_factor_replicated_one_hot_unweighted(
      self,
      index: tuple[int, ...],
  ) -> tuple[Array]:

    probs = self._probs

    sqrt_probs_slice = jnp.expand_dims(self._sqrt_probs[(slice(None),) + index],
                                       axis=range(1, len(probs.shape)))

    padded_slice = insert_slice_in_zeros(
        sqrt_probs_slice, probs.shape, (0,) + index)

    return (padded_slice - probs * sqrt_probs_slice,)


@jax.tree_util.register_pytree_node_class
class OneHotCategoricalLogitsNegativeLogProbLoss(
    CategoricalLogitsNegativeLogProbLoss):
  """Neg log prob loss for a categorical distribution with one-hot targets.

  Identical to CategoricalLogitsNegativeLogProbLoss except that the underlying
  distribution is OneHotCategorical as opposed to Categorical. ``targets`` is
  vector-encoded instead of integer-encoded, and must have the same shape as
  ``logits``.
  """

  @property
  def dist(self) -> distrax.OneHotCategorical:
    return distrax.OneHotCategorical(logits=self._logits, dtype=jnp.int32)


def insert_slice_in_zeros(
    slice_to_insert: Array,
    zeros_shape: Sequence[int],
    position: Sequence[int],
) -> Array:
  """Inserts slice into a larger array of zeros.

  Forms a new array of shape ``zeros_shape``, which is zeros everywhere except
  for the slice given by the ``position`` argument.

  We assume that slice_to_insert.shape and zeros_shape are the same length, and
  with ``slice_to_insert.shape[i] == zeros_shape[i]`` or ``1`` for all ``i``.
  For ``i`` where slice_to_insert.shape[i] == 1, ``position[i]`` must be ``0``.

  Args:
    slice_to_insert: The slice to insert.
    zeros_shape: The shape of the new array.
    position: The position of ``slice_to_insert`` in the new tensor.

  Returns:
    The new array.

  Raises:
    ValueError: If the slice's shape at the given dim is not 1.
  """

  assert slice_to_insert.ndim == len(zeros_shape)
  assert slice_to_insert.ndim == len(position)

  pad_width = []

  for i in range(slice_to_insert.ndim):
    if slice_to_insert.shape[i] == 1:
      pad_width.append((position[i], zeros_shape[i] - position[i] - 1))
    else:
      assert slice_to_insert.shape[i] == zeros_shape[i]
      assert position[i] == 0
      pad_width.append((0, 0))

  return jnp.pad(slice_to_insert, pad_width)


def register_normal_predictive_distribution(
    mean: Array,
    targets: Array | None = None,
    variance: float = 0.5,
    weight: Numeric = 1.0,
    normalize_log_prob: bool = True,
) -> None:
  """Registers a normal predictive distribution.

  This corresponds to a squared error loss of the form
     ``weight/(2*var) * jnp.sum((targets - mean)**2) / batch_size``.

  NOTE: this function assumes you are *not* averaging over non-batch dimensions
  when computing the loss. e.g. if dimension 0 were the batch dimension, this
  corresponds to
  ``jnp.mean(jnp.sum((target - prediction)**2,
                     axis=range(1,target.ndims)), axis=0)``
  and not
  ``jnp.mean((target - prediction)**2)``.
  If your loss is of the latter form you can compensate for it by passing the
  appropriate value to ``weight``.

  Args:
    mean: An ND array defining the mean vector of the distribution. The first
      dimension will usually be the batch size, but doesn't need to be (unless
      using ``estimation_mode='fisher_exact'`` or
      ``estimation_mode='ggn_exact'`` in the optimizer/estimator).
    targets: (OPTIONAL) The targets for the loss function. Must have the same
      shape as ``mean``. Only required if using
      ``estimation_mode='fisher_empirical'`` in the optimizer/estimator.
      (Default: None)
    variance: The variance of the distribution. Must be a constant scalar,
      independent of the network's parameters. Note that the default value of
      0.5 corresponds to a standard squared error loss
      ``weight * jnp.sum((target - prediction)**2)``. If you want your squared
      error loss to be of the form
      ``0.5*coeff*jnp.sum((target - prediction)**2)`` you should use
      variance=1.0. (Default: 0.5)
    weight: A constant scalar coefficient that the log prob loss associated with
      this distribution is multiplied by. In general this is NOT equivalent to
      changing the temperature of the distribution, but in the case of normal
      distributions it may be. Note that this must be constant and independent
      of the network's parameters. (Default: 1.0)
    normalize_log_prob: Whether the negative log prob loss associated to this
      this distribution should include the additive normalization constant
      (which is constant and depends on ``variance``) that makes it a true log
      prob, and not just a squared error loss. Note that this has no effect on
      the behavior of optimizer with the exception of in niche situations where
      the loss value is computed from the registrations. e.g., when
      ``include_registered_loss_in_stats=True`` is used. (Default: True)
  """
  args, args_names = filter_none(
      mean=mean,
      targets=targets,
      variance=variance,
      weight=weight,
      normalize_log_prob=normalize_log_prob,
  )

  tags.loss_tag.bind(
      *args,
      meta=tags.LossMetaData(
          loss_class=NormalMeanNegativeLogProbLoss,
          parameter_dependants=args_names[:1],
          parameter_independants=args_names[1:],
          argument_names=tuple(args_names),
      )
  )


def register_squared_error_loss(
    prediction: Array,
    targets: Array | None = None,
    weight: Numeric = 1.0,
) -> None:
  """Registers a squared error loss function.

  This assumes a squared error loss of the form
  ``weight * jnp.sum((targets - prediction)**2) / batch_size``.

  If your loss uses a coefficient of 0.5 you need to set the ``weight`` argument
  to reflect this.

  NOTE: this function assumes you are *not* averaging over non-batch dimensions
  when computing the loss. e.g. if dimension 0 were the batch dimension, this
  corresponds to
  ``jnp.mean(jnp.sum((target - prediction)**2,
                     axis=range(1, target.ndims)), axis=0)``
  and not
  ``jnp.mean((target - prediction)**2)``
  If your loss is of the latter form you can compensate for it by passing the
  appropriate value to ``weight``.

  NOTE: even though ``prediction`` and ``targets`` are interchangeable in the
  definition of the squared error loss, they are not interchangeable in this
  function. ``prediction`` must be the output of your parameterized function
  (e.g. neural network), and ``targets`` must not depend on the parameters.
  Mixing the two up could lead to a silent failure of the curvature estimation.

  Args:
    prediction: The prediction made by the network (i.e. its output) as an ND
      array of floats. The first dimension will usually be the batch size, but
      doesn't need to be (unless using ``estimation_mode='fisher_exact'`` or
      ``estimation_mode='ggn_exact'`` in the optimizer/estimator).
    targets: (OPTIONAL) The targets for the loss function. Must have the same
      shape as ``prediction``. Only required if using
      ``estimation_mode='fisher_empirical'`` in the optimizer/estimator.
      (Default: None)
    weight: The constant scalar coefficient which this loss is multiplied by.
      Note that this must be constant and independent of the network's
      parameters. (Default: 1.0)
  """
  register_normal_predictive_distribution(
      mean=prediction,
      targets=targets,
      variance=0.5,
      weight=weight,
      normalize_log_prob=False,
  )


def register_multi_bernoulli_predictive_distribution(
    logits: Array,
    targets: Array | None = None,
    weight: Numeric = 1.0,
) -> None:
  """Registers a multi-Bernoulli predictive distribution.

  This corresponds to a sigmoid cross-entropy loss of the form
  ``weight * jnp.sum(sigmoid_cross_entropy(logits, targets)) / batch_size``.

  NOTE: this function assumes you are *not* averaging over non-batch dimensions
  when computing the loss. e.g. if dimension 0 were the batch dimension, this
  corresponds to
  ``jnp.mean(jnp.sum(sigmoid_cross_entropy(logits, targets),
                     axis=range(1, target.ndims)), axis=0)``
  and not
  ``jnp.mean(sigmoid_cross_entropy(logits, targets))``
  If your loss is of the latter form you can compensate for it by passing the
  appropriate value to ``weight``.

  NOTE: this is distinct from
  :func:`~register_categorical_predictive_distribution` and should not be
  confused with it.

  Args:
    logits: The logits of the distribution (i.e. its parameters) as a ND array
      of floats. The first dimension will usually be the batch size, but doesn't
      need to be (unless using ``estimation_mode='fisher_exact'`` or
      ``estimation_mode='ggn_exact'`` in the optimizer/estimator).
    targets: (OPTIONAL) The targets for the loss function. Must be of the same
      shape as ``logits``. Only required if using
      ``estimation_mode='fisher_empirical'`` in the optimizer/estimator.
      (Default: None)
    weight: The constant scalar coefficient that the log prob loss associated
      with this distribution is multiplied by. This is NOT equivalent to
      changing the temperature of the distribution since we don't renormalize
      the log prob in the objective function. Note that this must be constant
      and independent of the network's parameters. (Default: 1.0)
  """
  args, args_names = filter_none(
      logits=logits,
      targets=targets,
      weight=weight,
  )

  tags.loss_tag.bind(
      *args,
      meta=tags.LossMetaData(
          loss_class=MultiBernoulliNegativeLogProbLoss,
          parameter_dependants=args_names[:1],
          parameter_independants=args_names[1:],
          argument_names=tuple(args_names),
      )
  )


def register_sigmoid_cross_entropy_loss(
    logits: Array,
    targets: Array | None = None,
    weight: Numeric = 1.0,
) -> None:
  """Registers a sigmoid cross-entropy loss function.

  This assumes a sigmoid cross-entropy loss of the form
  ``weight * jnp.sum(sigmoid_cross_entropy(logits, targets)) / batch_size``.

  NOTE: this function assumes you are *not* averaging over non-batch dimensions
  when computing the loss. e.g. if dimension 0 were the batch dimension, this
  corresponds to
  ``jnp.mean(jnp.sum(sigmoid_cross_entropy(logits, targets),
                     axis=range(1, target.ndims)), axis=0)``
  and not
  ``jnp.mean(sigmoid_cross_entropy(logits, targets))``
  If your loss is of the latter form you can compensate for this by passing the
  appropriate value to ``weight``.

  NOTE: this function is distinct from
  :func:`~register_softmax_cross_entropy_loss` and should not be confused with
  it. It is similar to :func:`~register_multi_bernoulli_predictive_distribution`
  but without the explicit probabilistic interpretation. It behaves identically
  for now.

  Args:
    logits: The input logits of the loss as a ND array of floats. The first
      dimension will usually be the batch size, but doesn't need to be (unless
      using ``estimation_mode='fisher_exact'`` or
      ``estimation_mode='ggn_exact'`` in the optimizer/estimator).
    targets: (OPTIONAL) The targets for the loss function. Must be of the same
      shape as ``logits``. Only required if using
      ``estimation_mode='fisher_empirical'`` in the optimizer/estimator.
      (Default: None)
    weight: The constant scalar coefficient which this loss is multiplied by.
      Note that this must be constant and independent of the network's
      parameters. (Default: 1.0)
  """
  register_multi_bernoulli_predictive_distribution(
      logits=logits,
      targets=targets,
      weight=weight,
  )


def register_categorical_predictive_distribution(
    logits: Array,
    targets: Array | None = None,
    mask: Array | None = None,
    weight: Numeric = 1.0,
) -> None:
  """Registers a categorical predictive distribution.

  This corresponds to a softmax cross-entropy loss of the form

  ``weight * jnp.sum(softmax_cross_entropy(logits, targets)) / batch_size``,

  or in other words, the negative log probability of the distribution,
  multiplied by ``weight``.

  NOTE: this is distinct from
  :func:`~register_multi_bernoulli_predictive_distribution` and should not be
  confused with it.

  Args:
    logits: The logits of the distribution (i.e. its parameters) as an ND array
      of floats. The first dimension will usually be the batch size, but doesn't
      need to be (unless using ``estimation_mode='fisher_exact'`` or
      ``estimation_mode='ggn_exact'`` in the optimizer/estimator). The final
      dimension is the one over which the softmax is computed.
    targets: (OPTIONAL) The values at which the log probability of this
      distribution is evaluated (to give the loss).  Must be a (N-1)D array of
      integers with shape ``logits.shape[:-1]`` for integer-encoded targets, or
      ``logits.shape`` for vector-encoded targets. Only required if using
      ``estimation_mode='fisher_empirical'`` in the optimizer/estimator.
      (Default: None)
    mask: (OPTIONAL) Mask to apply to log probabilities generated by the
      distribution. Should be 0/1-valued and of shape ``logits.shape[:-1]``.
      Log probabilities corresponding to mask values of 0 will be treated
      as constant and equal to 0. (Default: None)
    weight: The constant scalar coefficient that the log prob loss associated
      with this distribution is multiplied by. This is NOT equivalent to
      changing the temperature of the distribution since we don't renormalize
      the log prob in the objective function. Note that this must be constant
      and independent of the network's parameters. (Default: 1.0)
  """
  if targets is not None:

    if targets.ndim == logits.ndim:
      loss_class = OneHotCategoricalLogitsNegativeLogProbLoss

    elif targets.ndim == logits.ndim - 1:
      loss_class = CategoricalLogitsNegativeLogProbLoss

    else:
      raise ValueError(f"The logits ndim is {logits.ndim} and the targets ndim "
                       f"must be either equal or one less than it, but is "
                       f"{targets.ndim}.")

  else:
    loss_class = CategoricalLogitsNegativeLogProbLoss

  args, args_names = filter_none(
      logits=logits,
      targets=targets,
      mask=mask,
      weight=weight,
  )

  tags.loss_tag.bind(
      *args,
      meta=tags.LossMetaData(
          loss_class=loss_class,
          parameter_dependants=args_names[:1],
          parameter_independants=args_names[1:],
          argument_names=tuple(args_names),
      ),
  )


def register_softmax_cross_entropy_loss(
    logits: Array,
    targets: Array | None = None,
    mask: Array | None = None,
    weight: Numeric = 1.0,
) -> None:
  """Registers a softmax cross-entropy loss function.

  This assumes a softmax cross-entropy loss of the form

  ``weight * jnp.sum(softmax_cross_entropy(logits, targets)) / batch_size``.

  NOTE:this is distinct from :func:`~register_sigmoid_cross_entropy_loss` and
  should not be confused with it. It is similar to
  :func:`~register_categorical_predictive_distribution` but without the explicit
  probabilistic interpretation. It behaves identically for now.

  Args:
    logits: The input logits of the loss as an ND array of floats. The first
      dimension will usually be the batch size, but doesn't need to be (unless
      using ``estimation_mode='fisher_exact'`` or
      ``estimation_mode='ggn_exact'`` in the optimizer/estimator).
      The final dimension is the one over which the softmax is computed.
    targets: (OPTIONAL) The targets for the loss function. Must be a (N-1)D
      array of integers with shape ``logits.shape[:-1]`` for integer-encoded
      targets, or ``logits.shape`` for vector-encoded targets. Only required if
      using ``estimation_mode='fisher_empirical'`` in the optimizer/estimator.
      (Default: None)
    mask: (OPTIONAL) Mask to apply to losses. Should be 0/1-valued and of shape
      ``logits.shape[:-1]``. Losses corresponding to mask values of 0 will be
      treated as constant and equal to 0. (Default: None)
    weight: The constant scalar coefficient which this loss is multiplied by.
      Note that this must be constant and independent of the network's
      parameters. (Default: 1.0)
  """
  register_categorical_predictive_distribution(
      logits=logits,
      targets=targets,
      mask=mask,
      weight=weight,
  )
