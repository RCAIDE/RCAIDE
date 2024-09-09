# RCAIDE/Library/Compoments/Mass_Properties.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE Imports 
from RCAIDE.Reference.Core import Data

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Mass_Properties
# ----------------------------------------------------------------------------------------------------------------------      
class Mass_Properties(Data):
    """ Mass properties for a physical component.
    """
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None

        Source:
            None 
        """     
        
        self.mass   = 0.0
        self.volume = 0.0
        self.center_of_gravity = np.array([[0.0,0.0,0.0]])
        
        self.moments_of_inertia = Data()
        self.moments_of_inertia.center = np.array([0.0,0.0,0.0])
        self.moments_of_inertia.tensor = np.array([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])