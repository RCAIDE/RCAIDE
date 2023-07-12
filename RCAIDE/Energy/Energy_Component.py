## @ingroup Energy
# Energy_Component.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, E. Botero
# Modified: 

# ------------------------------------------------------------
#  Imports
# ------------------------------------------------------------

from Legacy.trunk.S.Core import Data 
from RCAIDE.Components.Component import Component
# ----------------------------------------------------------------------
#  Energy Component Class
# ----------------------------------------------------------------------
## @ingroup Energy
class Energy_Component(Component):
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