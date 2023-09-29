## @ingroup Energy-Converters
# RCAIDE/Energy/Converters/Propeller.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
 # RCAIDE imports 
from .Rotor import Rotor

# ----------------------------------------------------------------------------------------------------------------------
#  Propeller
# ----------------------------------------------------------------------------------------------------------------------     
## @ingroup Energy-Converters
class Propeller(Rotor):
    """This is a propeller component, and is a sub-class of rotor.
    
    Assumptions:
    None
    
    Source:
    None
    """     
    def __defaults__(self):
        """This sets the default values for the component to function.
        
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

        self.tag                       = 'propeller'
        self.orientation_euler_angles  = [0.,0.,0.] # This is X-direction thrust in vehicle frame
        self.use_2d_analysis           = False       
        self.variable_pitch            = False
        
