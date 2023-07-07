# RCAIDE/Energy/Converters/Lift_Rotor.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports 
from .Rotor import Rotor

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  LIFT ROTOR CLASS
# ----------------------------------------------------------------------------------------------------------------------           
## @ingroup Energy-Converters
class Lift_Rotor(Rotor):
    """This is a lift rotor component, and is a sub-class of rotor.
    
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

        self.tag                       = 'lift_rotor'
        self.orientation_euler_angles  = [0.,np.pi/2.,0.] # This is Z-direction thrust up in vehicle frame
        self.use_2d_analysis           = False
        self.variable_pitch            = False
        