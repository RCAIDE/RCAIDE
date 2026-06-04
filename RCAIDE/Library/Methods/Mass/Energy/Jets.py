# RCAIDE/Library/Methods/Mass/Propulsion/Jet_Mass_from_SLS.py
# (c) Copyright 2025 Aerospace Research Community LLC#
# Created:  May 2025, J. Smart
# Modified: 
# -------------------------------------------------------------------------------
#  Imports
# -------------------------------------------------------------------------------

# RCAIDE Imports

import RCAIDE.Library as rcl
import RCAIDE.Framework as rcf

from RCAIDE.Library.Methods.Energy.Converters.Turbofans import func_thrust_and_power

# -------------------------------------------------------------------------------
#  Functional/Library Version
# -------------------------------------------------------------------------------


def func_Jet_Mass_from_SLS(
    sls_thrust: float
):

    t_lbf = sls_thrust * 0.224809  # Convert to lbf
    mass = (0.4054 * t_lbf ** 0.9255) * 0.453592

    return mass


# -------------------------------------------------------------------------------
#  Stateful/Framework Version
# -------------------------------------------------------------------------------

def Jet_Mass_from_SLS(
    state: "rcf.State",
    system: "rcf.Aircraft",
    settings: "rcf.Settings",
    ):
    """
    Framework version of Jet_Mass_from_SLS. Assumes a turbofan engine.
    
    See Also
    --------
    func_Jet_Mass_from_SLS: 
        Functional implementation which this method calls.
    """

    for line in system.energy.lines:
        for jet in line.converters:

            jet: rcl.Components.Energy.Converters.TurbofanEngine

            if jet.design_thrust_parameters.SLS_thrust == 0.:

                T_ref = jet.reference_temperature

                F = func_thrust_and_power(
                    gamma=jet.working_fluid.compute_gamma(T_ref)
                )

                jet.design_thrust_parameters.SLS_thrust = F


            sls_thrust = jet.design_thrust_parameters.SLS_thrust

            jet_mass = func_Jet_Mass_from_SLS(sls_thrust)
            jet.mass_properties.total = jet_mass

    # TODO: Unpack results

    return state, system, settings
