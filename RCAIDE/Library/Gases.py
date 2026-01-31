# RCAIDE/Library/Gases.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: Apr 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import chex
from dataclasses import field

# package imports
import RNUMPY as rp

# RCAIDE imports


# ----------------------------------------------------------------------------------------------------------------------
#  Gases
# ----------------------------------------------------------------------------------------------------------------------

@chex.dataclass(kw_only=True)
class GasComposition:

    elements: list = field(default_factory=list)
    mass_fractions: list = field(default_factory=list)


@chex.dataclass(kw_only=True)
class Gas:

    tag:                   str     = 'Gas'

    molecular_mass:         float   = 0.0
    molar_mass:             float   = 0.0

    R:                      float   = 8.314462  # ideal gas constant (J/(mol·K))
    R_specific:             float   = 0.0

    specific_heat_capacity: float   = 0.0

    gamma_coefficients:     list = field(default_factory=list)
    cp_coefficients:        list = field(default_factory=list)
    thermal_coefficients:   list = field(default_factory=list)

    composition:            GasComposition = field(default_factory=GasComposition)

    def __post_init__(self):
        self.molar_mass = self.R / self.R_specific

    def compute_density(self, T=298.15, p=101325.):
        return p / (self.R_specific * T)

    def compute_gamma(self, T=298.15):
        return rp.polyval(self.gamma_coefficients, T)

    def compute_cp(self, T=298.):
        return rp.polyval(self.cp_coefficients, T)

    def compute_thermal_conductivity(self, T=298.):
        return rp.polyval(self.thermal_coefficients, T)

    def compute_speed_of_sound(self, T=298.):
        g = self.compute_gamma(T)
        return rp.sqrt(g * self.R_specific * T)

    def compute_absolute_viscosity(self, T=298.):
        raise NotImplementedError('Compute absolute viscosity not implemented for this gas')

    def compute_prandtl_number(self, T=298.):
        return self.compute_absolute_viscosity(T) * self.specific_heat_capacity / self.compute_thermal_conductivity(T)


@chex.dataclass(kw_only=True)
class Air(Gas):

    name                    = 'Air'

    molecular_mass          = 28.96442

    R_specific              = 287.0528742

    specific_heat_capacity  = 1006.

    cp_coefficients         = [-7.357e-7, 0.001307, -0.5558, 1074.0]
    gamma_coefficients      = [1.629e-10, -3.588e-7, 0.0001418, 1.386]
    thermal_coefficients    = [1.4e-11, -4.57e-8, 9.89e-5, 3.99e-4]

    def __post_init__(self):

        self.composition.O2         = 0.20946
        self.composition.Ar         = 0.00934
        self.composition.CO2        = 0.00036
        self.composition.N2         = 0.78084

    def compute_absolute_viscosity(self, T=298.):
        return 1.458e-6 * (T ** 1.5) / (T + 110.4)


@chex.dataclass(kw_only=True)
class Steam(Gas):

    name            = 'Steam'

    molecular_mass  = 18.0
    R_specific      = 461.889

    gamma_coefficients = [1.33]
    cp_coefficients    = [5e-9, 1e-4, .9202, 1524.7]

    def __post_init__(self):

        self.composition.H2O       = 1.0

    def compute_absolute_viscosity(self, T=298.):

        return 1e-6

    def compute_thermal_conductivity(self, T=298.):
        raise NotImplementedError('Compute thermal conductivity not implemented steam.')


@chex.dataclass(kw_only=True)
class CO2(Gas):

    name            = 'Carbon Dioxide'

    molecular_mass  = 44.01
    R_specific      = 188.9

    specific_heat_capacity = 839.

    def __post_init__(self):

        self.composition.CO2       = 1.0

    def compute_gamma(self, T=298.15):
        raise NotImplementedError('Compute gamma not implemented for carbon dioxide.')

    def compute_cp(self, T=298.):
        raise NotImplementedError('Compute cp not implemented for carbon dioxide.')

    def compute_thermal_conductivity(self, T=298.):
        raise NotImplementedError('Compute thermal conductivity not implemented for carbon dioxide.')

    def compute_speed_of_sound(self, T=298.):
        raise NotImplementedError('Compute speed of sound not implemented for carbon dioxide.')

    def compute_absolute_viscosity(self, T=298.):
        raise NotImplementedError('Compute absolute viscosity not implemented for this gas')

    def compute_prandtl_number(self, T=298.):
        raise NotImplementedError('Compute Prandtl number not implemented for carbon dioxide.')


@chex.dataclass(kw_only=True)
class O2(Gas):

    name            = 'Oxygen'

    molecular_mass  = 32.00
    R_specific      = 259.84

    specific_heat_capacity = 918.

    def __post_init__(self):

        self.composition.O2       = 1.0







