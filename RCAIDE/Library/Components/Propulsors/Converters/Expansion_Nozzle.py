# RCAIDE/Library/Components/Propulsors/Converters/Expansion_Nozzle.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Feb 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from RCAIDE.Library.Components                      import Component  
 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Expansion Nozzle
# ----------------------------------------------------------------------------------------------------------------------
class Expansion_Nozzle(Component):
    """This is a nozzle component intended for use in expansion. 
    """
    
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
            1. Pressure ratio and efficiency do not change with varying conditions.
            2. Subsonic or choked output.

        Source:
            https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/
        """          
        #set the defaults
        self.tag = 'Nozzle'
        self.polytropic_efficiency           = 1.0
        self.pressure_ratio                  = 1.0 