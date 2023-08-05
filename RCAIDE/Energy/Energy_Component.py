## @ingroup Energy
# Energy_Component.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, E. Botero
# Modified: 

# ------------------------------------------------------------
#  Imports
# ------------------------------------------------------------

from Legacy.trunk.S.Core import Data

# ----------------------------------------------------------------------
#  Energy Component Class
# ----------------------------------------------------------------------
## @ingroup Energy
class Energy_Component(Data):
    """A class representing an energy component.
    
    Assumptions:
    None
    
    Source:
    N/A
    """      
    def __defaults__(self):
        """This sets the default inputs and outputs data structure.

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
        # function handles for input
        self.inputs  = Data()
        
        # function handles for output
        self.outputs = Data()
        
        return