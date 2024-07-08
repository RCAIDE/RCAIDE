# RCAIDE/Framework/Analyses/Common/Process_Geometry.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Core import Data
from RCAIDE.Framework.Analyses import Process

# ----------------------------------------------------------------------------------------------------------------------
#  Analysis
# ---------------------------------------------------------------------------------------------------------------------- 
class Process_Geometry(Process):
    """A process for evaluate over a component group.

    Assumptions:
        None

    Source:
        None
    """      
    
    geometry_key = None
    
    def __init__(self,geometry_key: str):
        """Sets the geometry key for this process.

        Assumptions:
            None

        Source:
            None

        Args:
            self         (dict): geoemtry data structure [-] 
            geometry_key (dict): data object             [string]

        Returns:
            None 
        """          
        self.geometry_key = geometry_key
    
    def evaluate(self,state,settings,geometry):
        """Evaluates preset processes for each component.

        Assumptions:
            None

        Source:
            None

        Args:
            self     (dict): geoemtry data structure             [-] 
            state    (dict): flight conditions                   [-]
            setting  (dict): settings of geometry data structure [-]
            geometry (dict): geometry data structure             [-]

        Returns:
            None 
        """             
        geometry_items = geometry.deep_get(self.geometry_key)
        
        results = Data()
        
        for key, this_geometry in geometry_items.items():
            result = Process.evaluate(self,state,settings,this_geometry)
            results[key] = result
            
        return results
        
        
        
