## @ingroup Library-Components-Airfoils
# RCAIDE/Compoments/Airfoils/Airfoil.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports     
from RCAIDE.Library.Components   import Component 
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Airfoil
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Components-Airfoils 
class Airfoil(Component):
    def __defaults__(self):
        """This sets the default values of a airfoil defined in RCAIDE.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """         
        
        self.tag                        = 'Airfoil' 
        self.coordinate_file            = None     
        self.geometry                   = None
        self.polar_files                = None
        self.polars                     = None
        self.prev                       = None
        self.next                       = None
        self.number_of_points           = 200
       