# RCAIDE/Library/Compoments/Component.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  


from __future__ import annotations
from warnings import warn
from typing import TypeVar, List

# package imports 
import equinox as eqx
import jax.numpy as jnp

# RCAIDE imports
from RCAIDE.Library.Attributes.Materials import Solid, Aluminum

# ----------------------------------------------------------------------------------------------------------------------
#  Component
# ----------------------------------------------------------------------------------------------------------------------         


class ComponentFineness(eqx.Module):

    # Attribute     Type    Default Value
    effective:      float   = 1.0
    nose:           float   = 0.0
    tail:           float   = 0.0
    def __repr__(self):
        return f"Eff.: {self.effective}"


class ComponentDimensions(eqx.Module):

    # Attribute         Type    Default Value
    ordinal_direction:  bool    = eqx.field(static=True, default=False)

    reference:          float   = 0.0
    total:              float   = 0.0
    maximum:            float   = 0.0
    effective:          float   = 0.0

    projected:          float   = 0.0
    front_projected:    float   = 0.0
    top_projected:      float   = 0.0
    side_projected:     float   = 0.0

    def __repr__(self):
        return ""


class ComponentAreas(eqx.Module):

    # Attribute         Type    Default Value
    reference:          float   = 0.0
    total:              float   = 0.0
    maximum:            float   = 0.0
    effective:          float   = 0.0

    inflow:             float   = 0.0
    outflow:            float   = 0.0

    inlet:              float   = 0.0
    exit:               float   = 0.0

    projected:          float   = 0.0
    front_projected:    float   = 0.0
    top_projected:      float   = 0.0
    side_projected:     float   = 0.0

    wetted:             float   = 0.0
    exposed:            float   = 0.0

    def __repr__(self):
        return ""


class MaterialProperties(eqx.Module):

    # Attribute                 Type        Default Value
    tensile_stress_carrier:     Solid   = eqx.field(default_factory=Aluminum)
    torsional_stress_carrier:   Solid   = eqx.field(default_factory=Aluminum)
    shear_stress_carrier:       Solid   = eqx.field(default_factory=Aluminum)

    def __repr__(self):
        return ""

class MassProperties(eqx.Module):

    # Attribute                         Type        Default Value
    total:                              float       = 0.0
    empty:                              float       = 0.0
    subcomponent_total:                 float       = 0.0

    volume:                             float       = 1.0
    density:                            float       = 0.0

    center_of_gravity:                  jnp.ndarray  = eqx.field(default_factory=lambda: jnp.zeros(3))
    moments_of_inertia:                 jnp.ndarray  = eqx.field(default_factory=lambda: jnp.zeros((3, 3)))
    subcomponent_moments_of_inertia:    jnp.ndarray  = eqx.field(default_factory=lambda: jnp.zeros((3, 3)))


    def __repr__(self):
        return ""


class Component(eqx.Module):


    tag:                    str                   = eqx.field(static=True, default='Component')
    is_control_component:   bool                  = eqx.field(static=True, default=False)

    segments:               tuple[Component, ...] = eqx.field(default_factory=tuple)
    subcomponents:          tuple[Component, ...] = eqx.field(default_factory=tuple)
    origin:                 jnp.ndarray           = eqx.field(default_factory=lambda: jnp.zeros(3))

    # ---------------------------------------------------AREAS----------------------------------------------------------
    areas:                  ComponentAreas        = eqx.field(default_factory=ComponentAreas)

    # -------------------------------------------------DIMENSIONS-------------------------------------------------------
    lengths:                ComponentDimensions   = eqx.field(default_factory=ComponentDimensions)
    widths:                 ComponentDimensions   = eqx.field(default_factory=ComponentDimensions)
    heights:                ComponentDimensions   = eqx.field(default_factory=ComponentDimensions)
    diameters:              ComponentDimensions   = eqx.field(default_factory=ComponentDimensions)

    # -----------------------------------------------MASS & MATERIALS---------------------------------------------------
    mass_properties:        MassProperties        = eqx.field(default_factory=MassProperties)
    material_properties:    MaterialProperties    = eqx.field(default_factory=MaterialProperties)

    
    def __repr__(self):
        repr_str = self.tag + " - Subcomponents: [" + ', '.join([sc.tag for sc in self.subcomponents])+"]"
        return repr_str
    
    def __getitem__(self, item):
        if isinstance(item, (slice, int)):
            return self.subcomponents[item]
        elif isinstance(item, str):
            return getattr(self, item.replace(' ', '_').lower())
        else:
            raise TypeError(f"Indices must be int, slice, or str.")
    
    def __getattr__(self, item:str):
        if item.startswith("__") and item.endswith("__"):
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{item}'")
        for sc in self.subcomponents:
            if sc.get_field_name() == item:
                return sc

        raise AttributeError(f"'{self.tag}' has no attribute or subcomponent named '{item}'")

    def __bool__(self):
        return True

    def __len__(self):
        return len(self.subcomponents)

    def __iter__(self):
        return iter(self.subcomponents)
    
    def __contains__(self, item):
        if isinstance(item, str):
            return any(sc.get_field_name() == item for sc in self.subcomponents)
        
        return item in self.subcomponents

    def get_field_name(self):
        actual_tag = self.tag
        
        if not isinstance(actual_tag, str):
            if hasattr(actual_tag, 'value'):
                actual_tag = actual_tag.value
            else:
                raise AttributeError(f"Unable to resolve field name for {self}.")
        
        return actual_tag.replace(' ', '_').lower()

    def add_segment(self, segment: "Component", index: int | None = None):
        if index is None:
            # Append
            new_segments = self.segments + (segment,)
        else:
            # Insert at specific index
            new_segments = self.segments[:index] + (segment,) + self.segments[index:]

        # Functionally replace and return the new Component
        return eqx.tree_at(lambda c: c.segments, self, new_segments)
    
    def insert_segment(self, segment: "Component", index: int):
        new_segments = self.segments[:index] + (segment,) + self.segments[index:]
        
        return eqx.tree_at(lambda c: c.segments, self, new_segments)

    def replace_segment(self, segment: "Component", index: int):
        new_segments = self.segments[:index] + (segment,) + self.segments[index + 1:]
        
        return eqx.tree_at(lambda c: c.segments, self, new_segments)

    def add_subcomponent(self, subcomponent: "Component"):

        new_subcomponents = self.subcomponents + (subcomponent,)
        new_self = eqx.tree_at(lambda c: c.subcomponents, self, new_subcomponents)
    
        return new_self
    
    def insert_subcomponent(self, subcomponent: "Component", index: int):
        new_subcomponents = self.subcomponents[:index] + (subcomponent,) + self.subcomponents[index:]
        
        return eqx.tree_at(lambda c: c.subcomponents, self, new_subcomponents)

    def replace_subcomponent(self, subcomponent: "Component", index: int):
        new_subcomponents = self.subcomponents[:index] + (subcomponent,) + self.subcomponents[index + 1:]
        
        return eqx.tree_at(lambda c: c.subcomponents, self, new_subcomponents)

    def remove_subcomponent(self, index: int):
        new_subcomponents = self.subcomponents[:index] + self.subcomponents[index + 1:]

        return eqx.tree_at(lambda c: c.subcomponents, self, new_subcomponents)


class ControlComponent(Component):

    is_control_component:   bool = eqx.field(static=True, default=True)
    control_path:           tuple[str, ...] |None   = eqx.field(static=True, default_factory=tuple)
    control_path_indices:   tuple | None            = eqx.field(static=True, default_factory=lambda: (slice(None), 0))