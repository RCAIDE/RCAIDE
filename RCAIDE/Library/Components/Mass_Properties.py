## @ingroup Components 
# RCAIDE/Compoments/Mass_Properties.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE Imports 
from RCAIDE.Frameworks.Core import Data

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Mass_Properties
# ----------------------------------------------------------------------------------------------------------------------        
## @ingroup Components
class Mass_Properties(Data):
    """ Mass properties for a physical component
        
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
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            None
        """         
        
        self.mass   = 0.0
        self.volume = 0.0
        self.center_of_gravity = np.array([[0.0,0.0,0.0]])
        
        self.moments_of_inertia = Data()
        self.moments_of_inertia.center = np.array([0.0,0.0,0.0])
        self.moments_of_inertia.tensor = np.array([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])