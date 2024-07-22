# RCAIDE/Framework/Analyses/Process.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Framework.Core import Container
from RCAIDE.Framework.Core import Data

# ----------------------------------------------------------------------------------------------------------------------
# Process
# ----------------------------------------------------------------------------------------------------------------------  
class Process(Container):
    """The top level process container class 
    """      
    def evaluate(self,*args,**kwarg):
        """Execute the evaluate functions of the analyses stored in the container.
                
            Assumptions:
                None
                                            
            Source:
                None
                                            
            Args:
                self  : class                           [-] 
                args  : arguments of the class          [-]
                kwarg : keyword arguments of the classs [-]
                                            
            Returns:
                resutls : results of the Evaluate Functions [-]
                
            """        
        
        results = Data() 
        
        for tag,step in self.items():  
            
            if hasattr(step,'evaluate'): 
                result = step.evaluate(*args,**kwarg)
            else:
                result = step(*args,**kwarg)
                
            results[tag] = result
         
        return results