# RCAIDE/Analyses/Mission/Mission.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports   
import RCAIDE
from   RCAIDE.Core import Container as ContainerBase
from . import Segments

# ----------------------------------------------------------------------------------------------------------------------
# ANALYSIS
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Analyses-Mission
class Mission(Segments.Simple.Container):
    """ Mission.py: Top-level mission class
    
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

## @ingroup Analyses-Mission
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
        results = RCAIDE.Core.Data()
        
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
