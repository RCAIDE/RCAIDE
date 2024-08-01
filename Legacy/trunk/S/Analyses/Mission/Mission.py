## @ingroup Analyses-Functions
# Functions.py
#
# Created:  
# Modified: Feb 2016, Andrew Wendorff

""" Functions.py: Top-level mission class """

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import Legacy.trunk.S as SUAVE
from Legacy.trunk.S.Core import Container as ContainerBase
from . import Segments

# ----------------------------------------------------------------------
#   Class
# ----------------------------------------------------------------------

## @ingroup Analyses-Functions
class Mission(Segments.Simple.Container):
    """ Functions.py: Top-level mission class
    
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
        self.tag = 'mission'
        
        # see Segments.Simple.Container
        
    def finalize(self):
        """ Stub
    
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
        pass
    
    

# ----------------------------------------------------------------------
#   Container Class
# ----------------------------------------------------------------------

## @ingroup Analyses-Functions
class Container(ContainerBase):
    """ Container for mission
    
        Assumptions:
        None
        
        Source:
        None
    """    
    
    def evaluate(self,state=None):
        """ Go through the missions, run through them, save the results
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            state   [Data()]
    
            Outputs:
            Results [Data()]
    
            Properties Used:
            None
        """         
        results = SUAVE.Core.Data()
        
        for key,mission in self.items():
            result = mission.evaluate(state)
            results[key] = result
            
        return results
    
    def finalize(self):
        """ Stub
    
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
        pass

# Link container
Mission.Container = Container
