# RCAIDE/RCAIDE/Library/Methods/Weights/Correlation_Buildups/Propulsion/jet_mass_from_sls.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created:  Apr 2024, J. Smart
# Modified:

# ----------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------- 

from Legacy.trunk.S.Core import Units
from Legacy.trunk.S.Components.Energy import Networks as EN
import numpy as np

# -----------------------------------------------------------------------
# Functional/Library Version
# -----------------------------------------------------------------------

def func_jet_mass_from_sls(SLS_thrust: np.ndarray,
                           n_engines: np.ndarray,
                           engine_weight_factor: float = 1.6,
                           *args, **kwargs):
    """
    Calculates the dry mass of a jet engine based on its sea level static thrust.

    Parameters
    ----------
    SLS_thrust : float
        Thrust of the jet engine at sea level in pounds.

    Returns
    -------
    float
        Dry mass of the jet engine in pounds.

    """

    one_jet_mass            = 0.4054 * np.power(SLS_thrust/Units.lbf, 0.9255) * Units.lbm
    total_propulsor_mass    = engine_weight_factor * jet_masses * n_engines

    return



# -----------------------------------------------------------------------
# Stateful/Framework Version
# -----------------------------------------------------------------------

def jet_mass_from_sls(State, Settings, System):

    propulsor_list = [System.networks.propulsor \
                      for propulsor in System.networks \
                      if isinstance(propulsor, EN.Turbofan) \
                      or isinstance(propulsor, EN.Turbojet_Super) \
                      or isinstance(propulsor, EN.Propulsor_Surrogate)]

    SLS_thrust = np.asarray(
        [propulsor.sealevel_static_thrust \
         for propulsor in propulsor_list \
         if isinstance(propulsor, EN.Turbofan) \
         or isinstance(propulsor, EN.Turbojet_Super) \
         or isinstance(propulsor, EN.Propulsor_Surrogate)]
    )

    n_engines = np.asarray(
        [propulsor.number_of_engines \
         for propulsor in propulsor_list \
         if isinstance(propulsor, EN.Turbofan) \
         or isinstance(propulsor, EN.Turbojet_Super) \
         or isinstance(propulsor, EN.Propulsor_Surrogate)]
    )

    jet_masses, total_propulsor_masses = func_Jet_Mass_from_SLS(SLS_thrust, n_engines)

    for idx, propulsor in enumerate(propulsor_list):
        propulsor.mass_properties.total_mass = total_propulsor_masses[idx]
        propulsor.mass_properties.one_engine_mass = jet_masses[idx]

    return State, Settings, System
