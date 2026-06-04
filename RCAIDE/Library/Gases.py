# RCAIDE/Library/Gases.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: Apr 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import equinox as eqx
import jax.numpy as jnp

# RCAIDE imports


# ----------------------------------------------------------------------------------------------------------------------
#  Gases
# ----------------------------------------------------------------------------------------------------------------------

class GasComposition(eqx.Module):

    elements: tuple[str]            = eqx.field(default_factory=tuple)
    mass_fractions: tuple[float]    = eqx.field(default_factory=tuple)


class Gas(eqx.Module):

    tag:                    str     = eqx.field(static=True, default='Gas')
    molecular_mass:         float   = eqx.field(static=True, default=0.0)
    molar_mass:             float   = eqx.field(static=True, default=0.0)
    R:                      float   = eqx.field(static=True, default=8.314462)  # ideal gas constant (J/(mol·K))
    R_specific:             float   = eqx.field(static=True, default=0.0)
    specific_heat_capacity: float   = eqx.field(static=True, default=0.0)

    gamma_coefficients:     tuple = eqx.field(default_factory=tuple)
    Cp_coefficients:        tuple = eqx.field(default_factory=tuple)
    thermal_coefficients:   tuple = eqx.field(default_factory=tuple)

    composition:            GasComposition = eqx.field(default_factory=GasComposition)

    def __post_init__(self):
        self.molar_mass = self.R / self.R_specific

    def compute_density(self, T: float|jnp.ndarray=298.15, p: float|jnp.ndarray=101325.):
        return p / (self.R_specific * T)

    def compute_gamma(self, T: float|jnp.ndarray=298.15):
        return jnp.polyval(jnp.array(self.gamma_coefficients), T)

    def compute_Cp(self, T: float|jnp.ndarray=298.):
        return jnp.polyval(jnp.array(self.Cp_coefficients), T)

    def compute_thermal_conductivity(self, T: float|jnp.ndarray=298.):
        return jnp.polyval(jnp.array(self.thermal_coefficients), T)

    def compute_speed_of_sound(self, T: float|jnp.ndarray=298.):
        g = self.compute_gamma(T)
        return jnp.sqrt(g * self.R_specific * T)

    def compute_absolute_viscosity(self, T: float|jnp.ndarray=298.):
        raise NotImplementedError('Compute absolute viscosity not implemented for this gas')

    def compute_prandtl_number(self, T: float|jnp.ndarray=298.):
        return self.compute_absolute_viscosity(T) * self.specific_heat_capacity / self.compute_thermal_conductivity(T)

def _air_composition():
    return GasComposition(
        elements = ("O2", "Ar", "CO2", "N2"),
        mass_fractions=(0.20946, 0.00934, 0.00036, 0.78084)
    )

class Air(Gas):

    name                   : str = eqx.field(static=True, default='Air')
    molecular_mass         : float = eqx.field(static=True, default=28.96442)
    R_specific             : float = eqx.field(static=True, default=287.0528742)
    specific_heat_capacity : float = eqx.field(static=True, default=1006.)
    Cp_coefficients        : tuple[float] = eqx.field(static=True, default=(-7.357e-7, 0.001307, -0.5558, 1074.0))
    gamma_coefficients     : tuple[float] = eqx.field(static=True, default=(1.629e-10, -3.588e-7, 0.0001418, 1.386))
    thermal_coefficients   : tuple[float] = eqx.field(static=True, default=(1.4e-11, -4.57e-8, 9.89e-5, 3.99e-4))

    composition:            GasComposition  = eqx.field(static=True, default_factory=_air_composition)

    def compute_absolute_viscosity(self, T: float|jnp.ndarray=298.):
        return 1.458e-6 * (T ** 1.5) / (T + 110.4)

def _steam_composition():
    return GasComposition(
        elements = ('H20',),
        mass_fractions=(1.0,)
    )

class Steam(Gas):

    name                : str            = eqx.field(static=True, default='Steam')
    molecular_mass      : float          = eqx.field(static=True, default=18.0)
    R_specific          : float          = eqx.field(static=True, default=461.889)
    gamma_coefficients  : tuple[float]   = eqx.field(static=True, default=(1.33))
    Cp_coefficients     : tuple[float]   = eqx.field(static=True, default=(5e-9, 1e-4, .9202, 1524.7))

    composition         : GasComposition = eqx.field(static=True, default_factory=_steam_composition)

    def compute_absolute_viscosity(self, T=298.):

        return 1e-6

    def compute_thermal_conductivity(self, T=298.):
        raise NotImplementedError('Compute thermal conductivity not implemented steam.')

def _C02_composition():
    return GasComposition(
        elements = ('CO2',),
        mass_fractions=(1.0,)
    )

class CO2(Gas):

    name                    : str   = eqx.field(static=True, default='Carbon Dioxide')
    molecular_mass          : float = eqx.field(static=True, default=44.01)
    R_specific              : float = eqx.field(static=True, default=188.9)
    specific_heat_capacity  : float = eqx.field(static=True, default=839.)

    composition              : GasComposition = eqx.field(static=True, default_factory=_C02_composition)

    def compute_gamma(self, T=298.15):
        raise NotImplementedError('Compute gamma not implemented for carbon dioxide.')

    def compute_Cp(self, T=298.):
        raise NotImplementedError('Compute cp not implemented for carbon dioxide.')

    def compute_thermal_conductivity(self, T=298.):
        raise NotImplementedError('Compute thermal conductivity not implemented for carbon dioxide.')

    def compute_speed_of_sound(self, T=298.):
        raise NotImplementedError('Compute speed of sound not implemented for carbon dioxide.')

    def compute_absolute_viscosity(self, T=298.):
        raise NotImplementedError('Compute absolute viscosity not implemented for this gas')

    def compute_prandtl_number(self, T=298.):
        raise NotImplementedError('Compute Prandtl number not implemented for carbon dioxide.')

class O2(Gas):

    name                    : str   = eqx.field(static=True, default='Oxygen')
    molecular_mass          : float = eqx.field(static=True, default=32.00)
    R_specific              : float = eqx.field(static=True, default=259.84)
    specific_heat_capacity  : float = eqx.field(static=True, default=918.)







