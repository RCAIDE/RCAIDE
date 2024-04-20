## @ingroup Library-Compoments
# RCAIDE/Library/Compoments/Envelope.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
 
from RCAIDE.Framework.Core import Data  

# ----------------------------------------------------------------------------------------------------------------------
#  Envelope
# ----------------------------------------------------------------------------------------------------------------------   
class Envelope(Data):
    """ Flight envelope for a vehicle
    """    
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
           None
        
        Source:
           None
        """          
        self.tag = 'Envelope'

        self.ultimate_load                                 = 0.0
        self.limit_load                                    = 0.0
                                         
        self.limit_loads                                   = Data()
                                
        self.alpha_maximum                                 = 0.0
        self.alt_vc                                        = 0.0
        self.alt_gust                                      = 0.0
        self.max_ceiling                                   = 0.0
        self.maximum_dynamic_pressure                      = 0.0
        self.maximum_mach_operational                      = 0.0

        self.maneuver                                      = Data()
        self.maneuver.load_alleviation_factor              = 0.0
        self.maneuver.equivalent_speed                     = Data()
        self.maneuver.equivalent_speed.velocity_max_gust   = 0
        self.maneuver.equivalent_speed.velocity_max_cruise = 0
        self.maneuver.equivalent_speed.velocity_max_dive   = 0
        self.maneuver.load_factor                          = Data()
        self.maneuver.load_factor.velocity_max_gust        = 0
        self.maneuver.load_factor.velocity_max_cruise      = 0
        self.maneuver.load_factor.velocity_max_dive        = 0

        self.gust                                          = Data()
        self.gust.load_alleviation_factor                  = 0.0
        self.gust.equivalent_speed                         = Data()
        self.gust.equivalent_speed.velocity_max_gust       = 0
        self.gust.equivalent_speed.velocity_max_cruise     = 0
        self.gust.equivalent_speed.velocity_max_dive       = 0
    
        self.gust.load_factor                              = Data()
        self.gust.load_factor.velocity_max_gust            = 0
        self.gust.load_factor.velocity_max_cruise          = 0
        self.gust.load_factor.velocity_max_dive            = 0
