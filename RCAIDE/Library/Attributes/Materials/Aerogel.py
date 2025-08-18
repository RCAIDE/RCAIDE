# RCAIDE/Library/Attributes/Solids/Aerogel.py
# 
# Created: Aug 2025, S. Shekar
#
#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------
from RCAIDE.Framework.Core import Units
from .Solid import Solid 

#-------------------------------------------------------------------------------
# Aerogel Material
#------------------------------------------------------------------------------- 
class Aerogel(Solid): 
    """ 
    A class representing aerogel material properties for aerospace thermal 
    protection and insulation applications.

    Attributes
    ----------
    density : float
        Material density in kg/m³ (130).
    thermal_conductivity : float
        Heat conduction coefficient in W/(m·K) (0.0113).
    specific_heat_capacity : float
        Specific heat at constant pressure in J/(kg·K). Value must be defined 
        for thermal simulations (not provided by default).
    ultimate_tensile_strength : float
        Maximum tensile stress before failure in Pa. Typically very low for 
        aerogels (not set by default).
    ultimate_shear_strength : float
        Maximum shear stress before failure in Pa. Aerogels are brittle, so 
        this property is rarely used (not set by default).
    minimum_gage_thickness : float
        Minimum manufacturable thickness in meters (0.0 by default).

    Notes
    -----
    Aerogels are ultra-lightweight materials with extremely low density and 
    thermal conductivity, making them suitable for thermal insulation in 
    aerospace applications such as cryogenic fuel tanks, battery protection, 
    and thermal protection systems. However, their mechanical strength is 
    limited, so structural usage is not recommended.  

    **Definitions**

    'Aerogel'
        A class of synthetic porous ultralight materials derived from a gel, 
        where the liquid component is replaced with a gas.
    
    'Thermal Conductivity'
        The property of a material to conduct heat, measured in watts per 
        meter-kelvin.

    References
    ----------
    [1] Hüsing, N., & Schubert, U. (1998). Aerogels—airy materials: chemistry, 
        structure, and properties. Angewandte Chemie International Edition, 
        37(1-2), 22-45.
    [2] NASA Glenn Research Center. "Aerogel Insulation."  
        https://www.grc.nasa.gov/www/RT1997/5000/5430bell.html
    """

    def __defaults__(self):
        """
        Set default material properties at instantiation. 

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        * Assumes silica aerogel with typical bulk density and conductivity.
        * Mechanical strength values are not set due to brittleness of aerogels.
        """
        self.density                    = 130 * Units['kg/(m**3)']        
        self.thermal_conductivity       = 0.0113
