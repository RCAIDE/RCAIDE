## @ingroup Energy-Thermal_Management-Batteries-Heat_Removal_Systems
# RCAIDE/Energy/Thermal_Management/Batteries/Heat_Removal_Systems/No_Removal_System.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
from RCAIDE.Core import Data
from RCAIDE.Energy.Energy_Component import Energy_Component  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  No_Heat_Exchanger
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Energy-Thermal_Management-Batteries-Heat_Removal_Systems
class No_Heat_Exchanger(Energy_Component):
    """This provides output values for a direct convention heat exchanger of a bettery pack
    
    Assumptions:
    None
    
    Source:
    N/A
    """
    
    def __defaults__(self):  
        self.tag   = 'No_Heat_Exchanger'
        return
    

    def compute_heat_removed(self,hrs_results,Q_heat_gen,numerics,freestream): 
        hex_results = hrs_results # need to correct 
        return hex_results
    
    
        
