# RCAIDE/utils.py
# (c) Copyright 2026 Aerospace Research Community LLC
#
# Created: Apr 2026, J. Smart
# Modified: Apr 2026, J. Smart

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import os

from typing import TYPE_CHECKING, Self, Callable
from dataclasses import dataclass
from pathlib import Path

import jax
import jax.numpy as jnp
import equinox as eqx

# --- Framework Imports (Strictly for Type Hinting to avoid Circular Imports) ---
if TYPE_CHECKING:
    from RCAIDE.Framework.State import State
    from RCAIDE.Framework.System import System
    from RCAIDE.Framework.Settings import Settings

# ----------------------------------------------------------------------------------------------------------------------
#  Utility Functions
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------
# Programmatic Helpers
#----------------------------------------------------------

def get_RCAIDE_root():
    return Path(os.path.dirname(os.path.abspath(__file__))).parents[0].resolve()

# ---------------------------------------------------------
# Input/Output Function Decorators
# ---------------------------------------------------------

def inputs(*dependencies: str):
    def decorator(func: Callable):
        func._inputs = set(dependencies)
        return func
    return decorator


def outputs(*outputs: str):
    def decorator(func: Callable):
        func._outputs = set(outputs)
        return func
    return decorator

# ---------------------------------------------------------
# Find Targets from Path in PyTrees
# ---------------------------------------------------------

class Token(eqx.Module):

    state: eqx.Module
    system: eqx.Module
    settings: eqx.Module

@dataclass(frozen=True)
class PathTuple:
    
    path: tuple
    slice_obj: slice

    def __init__(self, path: tuple | Self = (slice(None),)):
        if isinstance(path, PathTuple):
            object.__setattr__(self, 'path', path.path)
            object.__setattr__(self, 'slice_obj', path.slice_obj)
            
        else:
            if isinstance(path[-1], slice):
                object.__setattr__(self, 'path', path[:-1])
                object.__setattr__(self, 'slice_obj', path[-1])
            else:
                object.__setattr__(self, 'path', path)
                object.__setattr__(self, 'slice_obj', slice(None))

    def __len__(self):
        return len(self.path)

def get_parent_target(obj, path_tuple: PathTuple):
    """Gets the full PyTree leaf, ignoring the slice."""
    for key in path_tuple.path:
        if isinstance(obj, dict):
            obj = obj[key]
        else:
            obj = getattr(obj, key)
    return obj

def get_target(obj, path_tuple: PathTuple):
    """Gets the target and applies the slice if one exists."""
    parent = get_parent_target(obj, path_tuple)
    if hasattr(parent, "__getitem__") and path_tuple.slice_obj != slice(None):
        return parent[path_tuple.slice_obj]
    return parent

def get_all_parents(s, input_map):
    return tuple(get_parent_target(s, path) for path in input_map)

def get_all_targets(s, input_map):
    return tuple(get_target(s, path) for path in input_map)

# ---------------------------------------------------------
# PyTree Deltas
# ---------------------------------------------------------

def compute_tree_delta(old_tree, new_tree):
    """Find changes between two identically structured PyTrees."""
    old_leaves, _ = jax.tree_util.tree_flatten(old_tree)
    new_leaves, _ = jax.tree_util.tree_flatten(new_tree)

    changed_indices = []
    changed_leaves = []

    for i, (old, new) in enumerate(zip(old_leaves, new_leaves)):
        # Handle unchanged leaves
        if old is new: continue
        if isinstance(old, jnp.ndarray) and isinstance(new, jnp.ndarray):
            if old.shape == new.shape and jnp.all(old == new): continue

        changed_indices.append(i)
        changed_leaves.append(new)

    return changed_indices, changed_leaves

def apply_tree_delta(base_tree, delta_indices, delta_leaves):

    """Reconstructs new tree from base tree and delta."""
    old_leaves, treedef = jax.tree_util.tree_flatten(base_tree)
    new_leaves = list(old_leaves)
    for idx, leaf in zip(delta_indices, delta_leaves):
        new_leaves[idx] = leaf

    return jax.tree_util.tree_unflatten(treedef, new_leaves)

# ---------------------------------------------------------
# General Mathematical Utilities
# ---------------------------------------------------------

@jax.jit
def cubic_spline_blender(x, start, end):

    eta = (x - start) / (end - start)
    eta_clamped = jnp.clip(eta, 0.1, 1.0)
    y = -2.0 * eta_clamped ** 3 + 3.0 * eta_clamped ** 2
    return y


if __name__ == '__main__':
    print(get_RCAIDE_root())