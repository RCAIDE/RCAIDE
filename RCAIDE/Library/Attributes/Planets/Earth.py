## @ingroup Library-Attributes-Planets
# RCAIDE/Library/Attributes/Planets/Earth.py
# (c) Copyright 2023 Aerospace Research Community LLC
#
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------  
#  Imports
# ----------------------------------------------------------------------------------------------------------------------  
 
from .Planet                import Planet 

# ----------------------------------------------------------------------------------------------------------------------  
#  Earth Class
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Attributes-Planets
class Earth(Planet):
    """Class for planet Earth with defauk properties 
    
    Assumptions:
    None
    
    Source:
    None
    """
    def __defaults__(self):
        """This sets the default values.

        Assumptions:
        None

        Source:
        Values commonly available

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """         
        self.tag = 'Earth'
        self.mass              = 5.98e24  # kg
        self.mean_radius       = 6.371e6  # m
        self.sea_level_gravity = 9.80665  # m/s^2    

    def compute_gravity(self, H=0.0):
        """Compute the gravitational acceleration at altitude
            
        Assumptions:      

        Source:

        Inputs:
        H     [m] (Altitude)

        Outputs:
        g     [m/(s^2)] (Gravity)

        Properties Used:
        None
        """          
        # Unpack
        g0  = self.sea_level_gravity
        Re  = self.mean_radius 
        
        # Calculate gravity
        gh = g0*(Re/(Re+H))**2.0
        
        return gh