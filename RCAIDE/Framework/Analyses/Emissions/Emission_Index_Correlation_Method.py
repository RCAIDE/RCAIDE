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
 
 
# package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Correlation_Buildup
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Analyses-Emissions
class Emission_Index_Correlation_Method(Emissions): 
    """ 
    """    
    
    def __defaults__(self): 
        """ 
        """   
        return
            

    def evaluate_emissions(self,segment):
        """ 
        """
        # unpack  
        emissions_index_correlation(self, segment)  
        return
