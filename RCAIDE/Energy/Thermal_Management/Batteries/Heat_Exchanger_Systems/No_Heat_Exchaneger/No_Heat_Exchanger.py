## @ingroup Energy-Thermal_Management-Batteries-Heat_Aquisition_Systems
# RCAIDE/Energy/Thermal_Management/Batteries/Heat_Aquisition_Systems/No_Removal_System.py
# (c) Copyright 2023 Aerospace Research Community LLC 
# 
# Created:  Dec 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
  
from RCAIDE.Energy.Energy_Component import Energy_Component   

# ----------------------------------------------------------------------------------------------------------------------
#  No_Heat_Exchanger
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Energy-Thermal_Management-Batteries-Heat_Aquisition_Systems
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
    
    
        
