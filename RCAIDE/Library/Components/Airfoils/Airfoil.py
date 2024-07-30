# RCAIDE/Compoments/Airfoils/Airfoil.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports     
from RCAIDE.Library.Components   import Component 
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Airfoil
# ----------------------------------------------------------------------------------------------------------------------  
class Airfoil(Component):
    """Default airfoil component class."""
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """         
        
        self.tag                        = 'Airfoil' 
        self.coordinate_file            = None     
        self.geometry                   = None
        self.polar_files                = None
        self.polars                     = None
        self.number_of_points           = 200
       