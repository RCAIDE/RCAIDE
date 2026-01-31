# RCAIDE/Framework/State.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import chex
from dataclasses import field
from functools import reduce

# package imports
import RNUMPY as rp

import RCAIDE.Library.Components
# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import (
    Conditions, Numerics, FrameConditions, FreestreamConditions, MassConditions, EnergyNetworkConditions,
    AerodynamicsConditions, ControlsConditions, DynamicsConditions)

# ----------------------------------------------------------------------------------------------------------------------
#  State
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class State(Conditions):

    # Attribute         Type                        Default Value
    tag:                str                         = 'State'
    initials:           chex.dataclass              = None
    numerics:           Numerics                    = field(default_factory=Numerics)

    frames:             FrameConditions             = field(default_factory=FrameConditions)
    freestream:         FreestreamConditions        = field(default_factory=FreestreamConditions)

    mass:               MassConditions              = field(default_factory=MassConditions)
    energy:             EnergyNetworkConditions     = field(default_factory=EnergyNetworkConditions)
    aerodynamics:       AerodynamicsConditions      = field(default_factory=AerodynamicsConditions)

    controls:           ControlsConditions          = field(default_factory=ControlsConditions)
    dynamics:           DynamicsConditions          = field(default_factory=DynamicsConditions)

    unknowns:           rp.ndarray                  = field(default_factory=lambda: rp.zeros((1, 1)))
    residuals:          rp.ndarray                  = field(default_factory=lambda: rp.zeros((1, 1)))

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

    def unpack_unknowns(self):
        """
        Finds the active control variables and assigns the unknowns to their locations in state.
        """
        n_points    = self.numerics.number_of_control_points
        control_idx = 0
        for name, control_var in vars(self.controls).items():
            if hasattr(control_var, 'path'):
                if hasattr(control_var, 'active') and control_var.active:
                    # 1. Extract values
                    values = self.unknowns[control_idx : control_idx + n_points]
                    values = rp.reshape(values, (-1, 1))
                    
                    # 2. Split path into parent-path and attribute-name
                    # Note: This assumes control_var.path is a list or tuple of strings
                    parent_path = control_var.path[:-1]
                    attr_name   = control_var.path[-1]
                    # 3. Locate the parent object
                    parent = reduce(getattr, parent_path, self)
                    # 4. Perform the update via .at[].set() 
                    # returns modified view in NP, new array in JAX
                    current_val = getattr(parent, attr_name)
                    updated_val = current_val.at[control_var.path_indices].set(values.flatten())
                    # 5. Re-assign back to the state object
                    # This is critical for JAX compatibility
                    setattr(parent, attr_name, updated_val)
                    control_idx += n_points
        return

    def pack_residuals(self):
        """
        Pulls the active residual values from the dynamics and packs them into the residuals array.
        """

        n_points = self.numerics.number_of_control_points
        residual_list = []

        for name, residual in vars(self.dynamics).items():
            if hasattr(residual, 'active') and residual.active:
                residual_list.append(residual.value)

        if residual_list:
            self.residuals = rp.column_stack(residual_list)
        else: self.residuals = rp.empty(n_points, 0)

        return

    def build_controls_from_system(self, system: "System|Component", verbose=True) -> None:
        if verbose:
            print(f"Building controls from {system.tag}...")
        for component in system.subcomponents:
            self.build_controls_from_system(component)

            if system.is_control_component:
                if isinstance(component, RCAIDE.Library.Components.Wing):
                    self.controls.add_control_variable(
                        RCAIDE.Framework.Missions.SurfaceControlVariable(
                            tag=component.tag + "_deflection",
                            surfaces=[system],
                        )
                    )

                else:
                    self.controls.add_control_variable(
                        RCAIDE.Framework.Missions.ControlVariable(
                            tag=component.tag
                        )
                    )
                if verbose:
                    print(f"\tAdded controls.{system.get_field_name()} as a control variable.")
        if verbose:
            print(f"Completed building controls from {system.tag}.\n"
                  f"Controls may be activated for mission segments by setting "
                  f"segment.active_controls = ('control_variable', ...)")
        return


