## @ingroup Analyses-Emissions
# RCAIDE/Framework/Analyses/Emissions/Emission_Index_Correlation_Method.py
# 
# 
# Created:  Jul 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Library.Methods.Emissions import  emissions_index_correlation 
from .Emissions            import Emissions 
  

# ----------------------------------------------------------------------------------------------------------------------
#  Correlation_Buildup
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Analyses-Emissions
class Emission_Index_Correlation_Method(Emissions): 
    """ Emissions Index Correlation Method
    """    
    
    def __defaults__(self): 
        """This sets the default values and methods for the analysis.
    
            Assumptions:
            None
    
            Source:
            None 
            """             
        return
            

    def evaluate_emissions(self,segment):
        """The default evaluate function.

        Assumptions:
        None

        Source:
        None 

        Inputs:
        self   - emissions analyses 
        state  - flight conditions 

        Outputs:
        results  
        """      
        # unpack  
        emissions_index_correlation(self, segment)  
        return
