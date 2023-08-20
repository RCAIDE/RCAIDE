## @ingroup Components-Energy-Thermal_Management 
# RCAIDE/Energy/Thermal_Management/No_Heat_Exchanger.py
# (c) Copyright The Board of Trustees of RCAIDE
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
    
    def compute_net_generated_battery_heat(self,battery,Q_heat_gen,numerics,freestream): 
        '''
        ''' 
    
        T_current                = battery.pack.temperature     
        cell_mass                = battery.cell.mass    
        Cp                       = battery.cell.specific_heat_capacity       
        I                        = numerics.time.integrate        
    
        # Calculate the current going into one cell   
        Nn                = battery.module.geometrtic_configuration.normal_count            
        Np                = battery.module.geometrtic_configuration.parallel_count    
        n_total_module    = Nn*Np  
        
        if n_total_module == 1: 
            # Using lumped model    
            Q_heat_gen_tot = Q_heat_gen
            P_net          = Q_heat_gen_tot  
    
        else:     
            Q_heat_gen_tot        = Q_heat_gen*n_total_module  
            P_net                 = Q_heat_gen_tot  
         
        dT_dt                  = P_net/(cell_mass*n_total_module*Cp)
        T_current              = T_current[0] + np.dot(I,dT_dt)    
 

        btms_results = Data()
        btms_results.operating_conditions = Data(battery_current_temperature = T_current,
                                                 heat_energy_generated       = Q_heat_gen_tot )   
        return btms_results
        
