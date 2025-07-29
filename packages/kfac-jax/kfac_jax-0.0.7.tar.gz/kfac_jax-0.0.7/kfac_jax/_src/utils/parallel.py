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
"""K-FAC utilities for multi-device execution."""
import functools
from typing import Callable, Sequence

import jax
from jax import core
from jax import lax
import jax.numpy as jnp

from kfac_jax._src.utils import types

jax_version = (
    jax.__version_info__ if hasattr(jax, "__version_info__")
    else tuple(map(int, jax.__version__.split("."))))


Array = types.Array
Numeric = types.Numeric
PRNGKey = types.PRNGKey
TArrayTree = types.TArrayTree


def in_pmap(axis_name: str | None) -> bool:
  """Returns whether we are in a pmap with the given axis name."""

  if axis_name is None:
    return False

  if jax_version >= (0, 4, 36):
    return axis_name in core.unsafe_get_axis_names_DO_NOT_USE()

  try:
    # The only way to know if we are under `jax.pmap` is to check if the
    # function call below raises a `NameError` or not.
    core.axis_frame(axis_name)

    return True

  except NameError:
    return False


def wrap_if_pmap(
    p_func: Callable[[TArrayTree, str], TArrayTree],
) -> Callable[[TArrayTree, str | None], TArrayTree]:
  """Wraps `p_func` to be executed only when inside a `jax.pmap` context."""

  @functools.wraps(p_func)
  def p_func_if_pmap(obj: TArrayTree, axis_name: str | None) -> TArrayTree:

    return p_func(obj, axis_name) if in_pmap(axis_name) else obj

  return p_func_if_pmap


# TODO(jamesmartens,botev): We no longer use wrap_if_pmap in the below
# definitions since it doesn't seem to transmit type info properly. Investigate?
def pmean_if_pmap(obj: TArrayTree, axis_name: str | None) -> TArrayTree:

  return lax.pmean(obj, axis_name) if in_pmap(axis_name) else obj


def psum_if_pmap(obj: TArrayTree, axis_name: str | None) -> TArrayTree:

  return lax.psum(obj, axis_name) if in_pmap(axis_name) else obj


pmap_mean = jax.pmap(lambda x: lax.pmean(x, "i"), axis_name="i")
pmap_sum = jax.pmap(lambda x: lax.psum(x, "i"), axis_name="i")


def index_if_not_scalar(value: Numeric, index: int = 0) -> Numeric:
  """Index `value` at axis 0 if it is not a scalar, otherwise return it."""

  if isinstance(value, Array):

    if value.ndim > 0:
      return value[index]
    else:
      return value

  elif isinstance(value, (float, int)):
    return value
  raise ValueError("The input should be an instance of `Numeric`.")


def get_first(obj: TArrayTree) -> TArrayTree:
  """Index the PyTree leaves `x` of `obj` by `x[0]` if they are not scalars."""
  return jax.tree_util.tree_map(index_if_not_scalar, obj)


def get_mean(obj: TArrayTree) -> TArrayTree:
  """Returns the average of `obj` over different devices."""
  return get_first(pmap_mean(obj))


def get_sum(obj: TArrayTree) -> TArrayTree:
  """Returns the sum of `obj` over different devices."""
  return get_first(pmap_sum(obj))


broadcast_all_local_devices = jax.pmap(lambda x: x)
pmap_zeros_like = jax.pmap(lambda x: jax.tree_util.tree_map(jnp.zeros_like, x))
jit_zeros_like = jax.jit(lambda x: jax.tree_util.tree_map(jnp.zeros_like, x))


def replicate_all_local_devices(obj: TArrayTree) -> TArrayTree:
  """Replicates `obj` to all local Jax devices."""
  if types.tree_is_empty(obj):
    return obj

  return jax.device_put_replicated(obj, devices=jax.local_devices())


def make_different_rng_key_on_all_devices(rng: PRNGKey) -> PRNGKey:
  """Makes a different PRNG for all Jax devices and processes."""

  rng = jax.random.fold_in(rng, jax.process_index())
  rng = jax.random.split(rng, jax.local_device_count())

  return broadcast_all_local_devices(rng)


p_split = jax.pmap(lambda key: tuple(jax.random.split(key)))
p_split_num = jax.pmap(lambda key, num: tuple(jax.random.split(key, num)),
                       static_broadcasted_argnums=1)


default_device_sync = None


def host_sync(
    obj: TArrayTree,
    sync_op: Callable[[TArrayTree, str], TArrayTree],
) -> TArrayTree:
  """Syncs `obj` across multiple hosts with the operation `sync_op`."""

  # The implementation here is to use the pmap syncing mechanisms but with only
  # the default device of each host. Technically we could do this with all
  # the devices on each host, but that would possibly be wasteful.

  if jax.process_count() > 1:

    # We set default_device_sync here because calling jax.local_devices during
    # the library import stage will break JAX.

    global default_device_sync

    if default_device_sync is None:

      default_devices = [jax.local_devices(process_index=p_idx)[0]
                         for p_idx in range(jax.process_count())]

      default_device_sync = jax.pmap(lambda x, sync_op: sync_op(x, "i"),
                                     devices=default_devices,
                                     axis_name="i",
                                     static_broadcasted_argnums=1)

    obj = jax.tree_util.tree_map(lambda x: jnp.expand_dims(x, axis=0), obj)

    return get_first(default_device_sync(obj, sync_op))

  return obj


def host_all_gather(x: TArrayTree) -> TArrayTree:
  """Gathers on every host the values of the PyTree leaves `x`."""
  return host_sync(x, lax.all_gather)


def host_mean(x: TArrayTree) -> TArrayTree:
  """Computes the mean of the PyTree leaves of `x` over multiple hosts."""
  return host_sync(x, lax.pmean)


def sync_and_divide_value(
    value: TArrayTree,
    counter: Numeric,
    axis_name: str | None = None,
) -> TArrayTree:
  """Computes the mean of `value` over all hosts and divides it by `counter`."""
  value = jax.tree_util.tree_map(lambda x: x / counter, value)
  return pmean_if_pmap(value, axis_name)


jit_sync_and_divide_value = jax.jit(sync_and_divide_value)
pmap_sync_and_divide_value = jax.pmap(
    functools.partial(sync_and_divide_value, axis_name="i"),
    axis_name="i",
)


# We might be able to change this to "return jnp.array(x)" in newer JAX
# versions. Or maybe we can use jnp.copy now?
def copy_array(x: Array) -> Array:
  """Copies a Jax array so that it can be donated freely."""
  return x + jnp.zeros_like(x)


copy_obj = jax.jit(lambda x: jax.tree_util.tree_map(copy_array, x))
_pmap_copy_obj = jax.pmap(copy_obj)


def pmap_copy_obj(x: TArrayTree | None) -> TArrayTree | None:

  # pmap will fail to work if passed a totally empty tree
  if x is None:
    return None

  if types.tree_is_empty(x):
    # this does a shallow copy of the tree similar to .copy():
    (flattened, structure) = jax.tree_util.tree_flatten(x)
    return jax.tree_util.tree_unflatten(structure, flattened)

  return _pmap_copy_obj(x)


def distribute_thunks(
    thunks: Sequence[Callable[[], TArrayTree]],
    pmap_axis_name: str,
    ) -> TArrayTree:
  """Distributes the computation of a list of thunks over the pmapped devices.

  Given a list of thunks, this function distributes their computation over the
  devices of the current pmap in a round-robin fashion, syncronizes the results
  across devices, and then returns them as a sequence of PyTrees.

  Note that this function is meant to be used in a compiled context, and may
  call ``thunk[i]()`` several times for each i, with all but one call getting
  "optimized away" by XLA.

  Args:
    thunks: A sequence of callables performing the desired computations. Each
      callable must take zero arguments and return a PyTree of JAX arrays. As
      with callables passed to (most) standard JAX API functions, these need to
      be stateless and free of side effects. The output of each callable must be
      the same regardless of the device it is executed on.
    pmap_axis_name: The name of the pmap axis to use.

  Returns:
    A sequence of PyTrees that are the output of the corresponding element of
    ``thunks``.
  """

  # The strategy here is to make a callable for each device which executes only
  # the thunks i such that i % total_devices == device_index, and returns a tree
  # of zeros for the remaining thunks. We then do a lax.switch over these based
  # on device_index, and return psum over these. Note that the more obvious way
  # of doing this, which is to perform a psum over the output of a sequence of
  # lax.cond calls (with one for each thunk), won't work in general. This is
  # because in order to save memory, XLA will sometimes elect to execute these
  # conds sequentially instead of in parallel.

  if not in_pmap(pmap_axis_name):
    raise ValueError(f"Provided pmap_axis_name {pmap_axis_name} is not a valid "
                     "pmap axis in current pmap (or this function was not "
                     "called in a pmap).")

  assert pmap_axis_name is not None

  total_devices = lax.psum(1, axis_name=pmap_axis_name)  # returns a constant
  current_device_index = lax.axis_index(pmap_axis_name)

  # This should get optimized away by XLA since we don't use the values:
  dummy_output_trees = tuple(thunk() for thunk in thunks)

  def make_branch(device_index):

    def branch():
      """Execute only thunks i such that i % total_devices == device_index."""

      outs = []
      for i in range(len(thunks)):

        if i % total_devices == device_index:
          outs.append(thunks[i]())
        else:
          outs.append(
              jax.tree_util.tree_map(jnp.zeros_like, dummy_output_trees[i]))

      return tuple(outs)

    return branch

  branches = tuple(make_branch(device_index)
                   for device_index in range(total_devices))

  output_trees = jax.lax.switch(current_device_index, branches)

  return jax.lax.psum(output_trees, axis_name=pmap_axis_name)
