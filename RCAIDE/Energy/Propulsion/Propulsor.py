## @ingroup Energy-Propulsion
# RCAIDE/Energy/Propulsion/Propusor.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Energy.Energy_Component                   import Energy_Component 

# ----------------------------------------------------------------------------------------------------------------------
#  Propusor
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Distributors
class Propulsor(Energy_Component):
    """  This controls the flow of energy into and from a battery-powered nework 
    
        Assumptions:
        None
        
        Source:
        None
    """
    
    
    def __defaults__(self):
        """ This sets the default values.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            None
        """          
        self.tag                          = 'propulsor'
        self.motor                        = None
        self.rotor                        = None
        self.ducted_fan                   = None
        self.electronic_speed_controller  = None  
        self.engine                       = None
        self.turbofan                     = None
        self.turbojet                     = None 
        
    