## @ingroup Analyses-Emissions
# RCAIDE/Framework/Analyses/Emissions/Emission_Index_Correlation_Method.py
# 
# 
# Created:  Jul 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Framework.Core import Data
from RCAIDE.Library.Methods.Emissions import  emissions_index_correlation_method
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
        settings                       = self.settings
        settings.emission_indices      =  Data() 
        settings.emission_indices.CO2 = 3.155  # kg/kg
        settings.emission_indices.H2O = 1.240  # kg/kg 
        settings.emission_indices.SO2 = 0.0008 # kg/kg
        
        return
            

    def evaluate_emissions(segment):
        """ 
        """
        # unpack  
        emissions_index_correlation_method(segment)  
        return
