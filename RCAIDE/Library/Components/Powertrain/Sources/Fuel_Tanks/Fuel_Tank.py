# RCAIDE/Library/Components/Powertrain/Sources/Fuel_Tanks/Fuel_Tank.py
# 
# 
# Created:  Mar 2024, M. Clarke 
# Modified: Aug 2025, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Library.Components          import Component
from RCAIDE.Library.Methods.Powertrain.Sources.Fuel_Tanks  import * 
from RCAIDE.Library.Methods.Powertrain.Sources.Fuel_Tanks.Non_Integral_Tank import compute_generic_fuel_tank_volume

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Tank
# ---------------------------------------------------------------------------------------------------------------------     
class Fuel_Tank(Component):
    """
    Base class for aircraft fuel tank implementations
    
    Attributes
    ----------
    tag : str
        Identifier for the fuel tank (default: 'fuel_tank')
        
    fuel_selector_ratio : float
        Ratio of fuel flow allocation (default: 1.0)
        
    mass_properties.empty_mass : float
        Mass of empty tank structure [kg] (default: 0.0)
        
    secondary_fuel_flow : float
        Secondary fuel flow rate [kg/s] (default: 0.0)
        
    fuel : Component, optional
        Fuel type stored in tank (default: None)

    Notes
    -----
    The fuel tank base class provides common attributes and methods for
    different types of aircraft fuel tanks. It handles basic fuel storage
    and flow management functionality.

    See Also
    --------
    RCAIDE.Library.Components.Powertrain.Sources.Fuel_Tanks.Central_Fuel_Tank
        Center section fuel tank
    RCAIDE.Library.Components.Powertrain.Sources.Fuel_Tanks.Wing_Fuel_Tank
        Wing-mounted fuel tank
    """
    
    def __defaults__(self):
        """
        Sets default values for fuel tank attributes
        """          
        self.tag                                   = 'fuel_tank'
        self.mass_properties.empty_mass            = 0.0   
        self.mass_properties.fuel                  = 0.0
        self.volume_properties.internal_volume     = 0.0
        self.volume_properties.external_volume     = 0.0  
        self.secondary_fuel_flow_rate              = 0.0
        self.fuel_selector_ratio                   = 1.0    
        self.wall_clearance                        = 0.0
        self.wall_thickness                        = 0.0
        self.fuel                                  = None
        self.symmetric                             = True
        self.wing_tag                              = None
        self.fuselage_tag                          = None
        self.inner_length                          = 0.0
        self.outer_length                          = 0.0
        self.inner_diameter                        = 0.0
        self.outer_diameter                        = 0.0
 
    def append_operating_conditions(self,segment,fuel_line):  
        """
        Append fuel tank operating conditions for a flight segment
        
        Parameters
        ----------
        segment : Segment
            Flight segment containing state conditions
        fuel_line : Component
            Connected fuel line component
        """
        append_fuel_tank_conditions(self,segment, fuel_line)  
        return
    

    def compute_tank_properties(self,state,fuel_line):  
        """
        Append fuel tank operating conditions for a flight segment
        
        Parameters
        ----------
        segment : Segment
            Flight segment containing state conditions
        fuel_line : Component
            Connected fuel line component
        """
        compute_fuel_tank_properties(self,state, fuel_line)  
        return


    def compute_volume(self, wings, fuselages):
        """
        Compute the internal volume of an arbitrary fuel tank based on its location. 

        Parameters
        ----------
        wings : dict
            Dictionary containing wing components indexed by wing tag
        fuselages : dict
            Dictionary containing fuselage components indexed by fuselage tag

        Returns
        -------
        volume : float
            Internal volume of the fuel tank [m³] 

        **Major Assumptions**
            * Tank is fully integrated into the host component structure
            * Wing tanks use the space between front and rear spars
            * Fuselage tanks use the space between specified fuselage segments
            * Volume calculations assume truncated prism geometry for wing tanks
            * Volume calculations assume truncated cone geometry for fuselage tanks

        **Definitions**

        'Integral Tank'
            Fuel tank that is structurally integrated into the aircraft's primary
            structure (wing or fuselage) rather than being a separate component

        'Wing Integral Tank'
            Fuel tank that utilizes the space between wing spars and ribs for
            fuel storage, typically located in the wing box

        'Fuselage Integral Tank'
            Fuel tank that utilizes the space within fuselage segments for fuel
            storage, typically located between structural frames

        See Also
        --------
        RCAIDE.Library.Methods.Powertrain.Sources.Fuel_Tanks.Integral_Tank.compute_integral_tank_volume
            Equations for computing integral tank volume for both wing and fuselage tanks
        """   
        compute_generic_fuel_tank_volume(self) 
        return    