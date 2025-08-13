# RCAIDE/Library/Attributes/Solids/Aluminum.py
# 
 

# Created: 

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------
from RCAIDE.Framework.Core import Units
from .Solid import Solid 

#-------------------------------------------------------------------------------
# Aluminum for ****
#------------------------------------------------------------------------------- 
class Polyurethane_Foam(Solid): 
    """ 
    REDO
    A class representing

    Attributes
    ----------
    density : float
        Material density in kg/m³ (2700)
    thermal_conductivity : float
        Heat conduction coefficient in W/(m·K) (202.4)
    specific_heat_capacity : float
        Specific heat at constant pressure in J/(kg·K) (871)
    ultimate_tensile_strength : float
        Maximum tensile stress before failure in Pa (310e6)
    ultimate_shear_strength : float
        Maximum shear stress before failure in Pa (206e6)
    ultimate_bearing_strength : float
        Maximum bearing stress before failure in Pa (607e6)
    yield_tensile_strength : float
        Stress at which material begins to deform plastically in Pa (276e6)
    yield_shear_strength : float
        Shear stress at which material begins to deform plastically in Pa (206e6)
    yield_bearing_strength : float
        Bearing stress at which material begins to deform plastically in Pa (386e6)
    minimum_gage_thickness : float
        Minimum manufacturable thickness in m (0.0)

    Notes
    -----
    This class implements standard 6061-T6 aluminum properties for both structural 
    and thermal applications. The thermal properties are particularly relevant for 
    battery cooling applications.

    **Definitions**
    
    'Ultimate Strength'
        The maximum stress that a material can withstand before failure
    
    'Yield Strength'
        The stress at which a material begins to deform plastically
    
    'Thermal Conductivity'
        The property of a material to conduct heat, measured in watts per meter-kelvin

    References
    ----------
   
    """

    def __defaults__(self):
        """Sets material properties at instantiation. 

        Assumptions:
            None
    
        Source:
       
        """

        self.density                    = 32* Units['kg/(m**3)']        
        self.thermal_conductivity       = 0.022
        # self.specific_heat_capacity     = 871 
        # self.ultimate_tensile_strength  = 310e6 * Units.Pa
        # self.ultimate_shear_strength    = 206e6 * Units.Pa
        # self.ultimate_bearing_strength  = 607e6 * Units.Pa
        #self.yield_tensile_strength     = 548*1e6* Units.Pa
        # self.yield_shear_strength       = 206e6 * Units.Pa
        # self.yield_bearing_strength     = 386e6 * Units.Pa
        # self.minimum_gage_thickness     = 0.0   * Units.m
        # self.density                    = 2700. * Units['kg/(m**3)']        
