# RCAIDE/Framework/State.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team
# Modified: Mar 2026, J.Smart

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from typing import TYPE_CHECKING
from functools import reduce

# package imports
import jax
import jax.numpy as jnp
import equinox as eqx

if TYPE_CHECKING:
    from RCAIDE.Framework import System
    from RCAIDE.Library import Component

import RCAIDE.Library.Components
# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import (
    Conditions, Numerics, FrameConditions, FreestreamConditions, MassConditions, EnergyNetworkConditions,
    AerodynamicsConditions, StabilityConditions, ControlsConditions, DynamicsConditions)

# ----------------------------------------------------------------------------------------------------------------------
#  State
# ----------------------------------------------------------------------------------------------------------------------

class SolverConditions(Conditions):

    tag: str = eqx.field(static=True, default='Solver Conditions')

    unknowns:           jnp.ndarray                 = eqx.field(default_factory=lambda: jnp.empty(0))
    residuals:          jnp.ndarray                 = eqx.field(default_factory=lambda: jnp.empty(0))
    

class State(Conditions):

    # Attribute         Type                        Default Value
    tag:                str                         = eqx.field(static=True, default='State')
    
    initials:           eqx.Module | None           = None
    numerics:           Numerics                    = eqx.field(default_factory=Numerics)

    frames:             FrameConditions             = eqx.field(default_factory=FrameConditions)
    freestream:         FreestreamConditions        = eqx.field(default_factory=FreestreamConditions)

    mass:               MassConditions              = eqx.field(default_factory=MassConditions)
    energy:             EnergyNetworkConditions     = eqx.field(default_factory=EnergyNetworkConditions)
    aerodynamics:       AerodynamicsConditions      = eqx.field(default_factory=AerodynamicsConditions)
    stability:          StabilityConditions         = eqx.field(default_factory=StabilityConditions)

    controls:           ControlsConditions          = eqx.field(default_factory=ControlsConditions)
    dynamics:           DynamicsConditions          = eqx.field(default_factory=DynamicsConditions)

    solver:             SolverConditions            = eqx.field(default_factory=SolverConditions)

    

    def check_controls(self, verbose=True) -> bool:
        """
        Checks that the number of active controls is equal to the number of active dynamics residuals.
        """

        valid_controls = (self.controls.count_active_controls() == self.dynamics.count_active_residuals())

        if verbose:
            if valid_controls:
                print("Number of active controls matches number of active dynamics residuals.")
            else:
                print("Number of active controls does not match number of active dynamics residuals.")

            print(f"\nCurrent active controls:")
            for control in self.controls.get_active_controls():
                print(f"- {control.tag}")

            print(f"\nCurrent active dynamics residuals:")
            for residual in self.dynamics.get_active_residuals():
                print(f"- {residual.tag}")

        return valid_controls
    
    def unpack_unknowns(self, unknowns):
        n_points = int(self.numerics.number_of_control_points) 
        
        # 1. Grab the perfectly static routing table
        routing_table = self.controls.active_routing_table

        # 2. Extract all targets in one shot
        def get_all_targets(s):
            targets = []
            for path, _ in routing_table:
                targets.append(reduce(getattr, path, s))
            return tuple(targets)

        current_targets = get_all_targets(self)
        new_arrays = []
        control_idx = 0

        # 3. Slice and set
        for i, (_, path_indices) in enumerate(routing_table):
            values = unknowns[control_idx : control_idx + n_points]
            
            current_array = current_targets[i]
            new_array = current_array.at[path_indices].set(values)
            
            new_arrays.append(new_array)
            control_idx += n_points

        # 4. Swap all arrays in a single JAX graph node
        return eqx.tree_at(get_all_targets, self, tuple(new_arrays))

    def pack_residuals(self):
        """
        Pulls the active residual values from the dynamics and packs them into the residuals array.
        """

        residual_list = []

        residual_list = [res.value for res in self.dynamics.get_active_residuals()]

        if residual_list:
            stacked_residuals = jnp.concatenate(residual_list)
        else:
            stacked_residuals = jnp.empty((0,))

        return eqx.tree_at(lambda s: s.solver.residuals, self, stacked_residuals)


    def build_controls_from_system(self, system: "System|Component", verbose=True) -> None:
        
        new_controls = self.controls
        surface_controls = []
        direct_controls = []
        unbound_controls = []

        
        if verbose:
            print(f"Building controls from {system.tag}...")
        
        for component in system.subcomponents:
            self.build_controls_from_system(component)

            if component.is_control_component:
                if isinstance(component, RCAIDE.Library.Components.Wing):
                    new_controls = self.controls.add_control_variable(
                        RCAIDE.Framework.Missions.Conditions.Controls.SurfaceControlVariable(
                            tag=component.tag + "_deflection",
                            surfaces=(system,),
                        )
                    )
                    surface_controls.append(component.tag + "_deflection")

                else:
                    unbound = False
                    if hasattr(component, "control_path"): path = component.control_path
                    else: path = (); unbound = True

                    if hasattr(component, "control_path_indices"): indices = component.control_path_indices
                    else: indices = (slice(None), 0); unbound = True

                    if unbound: unbound_controls.append(component.tag)

                    new_controls = self.controls.add_control_variable(
                        RCAIDE.Framework.Missions.Conditions.Controls.DirectControlVariable(
                            tag=component.tag,
                            path=path,
                            path_indices=indices,
                        )
                    )
                    if not unbound: direct_controls.append(component.tag)

                if verbose:
                    if surface_controls:
                        print(f"Added the following aerodynamic surface controls:" +
                              "\n\t- ".join(surface_controls))
                    if direct_controls:
                        print(f"Added the following direct controls:" +
                              "\n\t- ".join(direct_controls))
                    if unbound_controls:
                        print(f"The following control components were found, but without path information."
                              f"They may not function as intended:"
                              "\n\t- ".join(unbound_controls))
        
        if verbose:
            print(f"Completed building controls from {system.tag}.\n"
                  f"Controls may be activated for mission segments by setting "
                  f"segment.active_controls = ('control_variable', ...)")
        
        return eqx.tree_at(lambda s: s.controls, self, new_controls)


