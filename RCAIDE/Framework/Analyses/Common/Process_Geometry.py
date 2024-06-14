## @ingroup Framework-Analyses-Common
# RCAIDE/Framework/Analyses/Common/Process_Geometry.py
# (c) Copyright 2023 Aerospace Research Community LLC

# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Core import Data
from RCAIDE.Framework.Analyses import Process

# ----------------------------------------------------------------------------------------------------------------------
#  Analysis
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Framework-Analyses-Common
class Process_Geometry(Process):
    """A process for evaluate over a component group.
    """            
    def __init__(self,geometry_key):
        """Sets the geometry key for this process.

        Assumptions:
        None

        Source:
        N/A 
        """          
        self.geometry_key = None
    
    def evaluate(self,state,settings,geometry):
        """Evaluates preset processes for each component.

        Assumptions:
            None

        Source:
            N/A

        Args:
            state    : flight conditions [unitless]
            setting  : geometry settings [unitless]
            geometry : RCAIDE aircraft   [unitless]

        Returns
            None 
        """             
        geometry_items = geometry.deep_get(self.geometry_key)
        
        results = Data()
        
        for key, this_geometry in geometry_items.items():
            result = Process.evaluate(self,state,settings,this_geometry)
            results[key] = result
            
        return results
        
        
        
        