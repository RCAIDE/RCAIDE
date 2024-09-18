## @ingroup Methods-Energy-Sources-Battery-Lithium_Ion_Generic
# RCAIDE/Methods/Energy/Sources/Battery/Lithium_Ion_Generic/compute_generic_li_cell_performance.py
# 
# 
# Created:  Feb 2024, M. Clarke
# Modified: Sep 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from RCAIDE.Framework.Core     import Units 
import numpy as np    
 
# ----------------------------------------------------------------------------------------------------------------------
# compute_generic_li_cell_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Sources-Batteries-Lithium_Ion_Generic 
def compute_generic_li_cell_performance(battery,state,bus,coolant_lines,t_idx, delta_t,battery_discharge_flag): 
    """This is an electric cycle model for 18650 lithium-iron_phosphate battery cells. It
       models losses based on an empirical correlation Based on method taken 
       from Datta and Johnson.
       
       Assumptions: 
       1) Constant Peukart coefficient
       2) All battery modules exhibit the same themal behaviour.
       
       Source:
       Internal Resistance:
       Nikolian, Alexandros, et al. "Complete cell-level lithium-ion electrical ECM model 
       for different chemistries (NMC, LFP, LTO) and temperatures (− 5° C to 45° C)–
       Optimized modelling techniques." International Journal of Electrical Power &
       Energy Systems 98 (2018): 133-146.
      
       Voltage:
       Chen, M. and Rincon-Mora, G. A., "Accurate Electrical
       Battery Model Capable of Predicting Runtime and I - V Performance" IEEE
       Transactions on Energy Conversion, Vol. 21, No. 2, June 2006, pp. 504-511
       
       Inputs:
         battery. 
               I_bat             (currnet)                             [Amperes]
               cell_mass         (battery cell mass)                   [kilograms]
               Cp                (battery cell specific heat capacity) [J/(K kg)] 
               E_max             (max energy)                          [Joules]
               E_current         (current energy)                      [Joules]
               Q_prior           (charge throughput)                   [Amp-hrs]
               R_growth_factor   (internal resistance growth factor)   [unitless]
               E_growth_factor   (capactance (energy) growth factor)   [unitless] 
           
         inputs.
               I_bat             (current)                             [amps]
               P_bat             (power)                               [Watts]
       
       Outputs:
         battery.          
              current_energy                                           [Joules]
              heat_energy_generated                                         [Watts] 
              load_power                                               [Watts]
              current                                                  [Amps]
              battery_voltage_open_circuit                             [Volts]
              cell.temperature                                         [Kelvin]
              cell.charge_throughput                                   [Amp-hrs]
              internal_resistance                                      [Ohms]
              battery_state_of_charge                                  [unitless]
              depth_of_discharge                                       [unitless]
              battery_voltage_under_load                               [Volts]   
        
    """ 
    

    # Unpack varibles 
    battery_conditions = state.conditions.energy[bus.tag][battery.tag]       
    I_bat              = battery_conditions.pack.current_draw
    P_bat              = battery_conditions.pack.power_draw
    cell_mass          = battery.cell.mass    
    Cp                 = battery.cell.specific_heat_capacity       
    V_max              = battery.cell.maximum_voltage                 
    E_max              = battery_conditions.pack.maximum_initial_energy * battery_conditions.cell.capacity_fade_factor
    E_pack             = battery_conditions.pack.energy    
    I_pack             = battery_conditions.pack.current                        
    V_oc_pack          = battery_conditions.pack.voltage_open_circuit           
    V_ul_pack          = battery_conditions.pack.voltage_under_load             
    P_pack             = battery_conditions.pack.power                          
    T_pack             = battery_conditions.pack.temperature                    
    Q_heat_pack        = battery_conditions.pack.heat_energy_generated          
    R_0                = battery_conditions.pack.internal_resistance            
    Q_heat_cell        = battery_conditions.cell.heat_energy_generated          
    SOC                = battery_conditions.cell.state_of_charge                
    P_cell             = battery_conditions.cell.power                          
    E_cell             = battery_conditions.cell.energy                         
    V_ul               = battery_conditions.cell.voltage_under_load             
    V_oc               = battery_conditions.cell.voltage_open_circuit           
    I_cell             = battery_conditions.cell.current                        
    T_cell             = battery_conditions.cell.temperature                    
    Q_cell             = battery_conditions.cell.charge_throughput              
    DOD_cell           = battery_conditions.cell.depth_of_discharge 
    
    
    # ---------------------------------------------------------------------------------
    # Compute battery electrical properties 
    # --------------------------------------------------------------------------------- 
    # Calculate the current going into one cell  
    n_series          = battery.pack.electrical_configuration.series  
    n_parallel        = battery.pack.electrical_configuration.parallel 
    n_total           = battery.pack.electrical_configuration.total
    
    # ---------------------------------------------------------------------------------
    # Examine Thermal Management System
    # ---------------------------------------------------------------------------------
    HAS = None  
    for coolant_line in coolant_lines:
        for tag, item in  coolant_line.items():
            if tag == 'batteries':
                for sub_tag, sub_item in item.items():
                    if sub_tag == battery.tag:
                        for btms in  sub_item:
                            HAS = btms     
   
    # ---------------------------------------------------------------------------------------------------
    # Current State 
    # ---------------------------------------------------------------------------------------------------
    I_cell[t_idx]  = I_bat[t_idx]/n_parallel  
    
    # A voltage model from Chen, M. and Rincon-Mora, G. A., "Accurate Electrical Battery Model Capable of Predicting
    # Runtime and I - V Performance" IEEE Transactions on Energy Conversion, Vol. 21, No. 2, June 2006, pp. 504-511
    V_normalized  = (-1.031*np.exp(-35.*SOC[t_idx]) + 3.685 + 0.2156*SOC[t_idx] - 0.1178*(SOC[t_idx]**2.) + 0.3201*(SOC[t_idx]**3.))/4.1
    V_oc[t_idx] = V_normalized * V_max
    V_oc[t_idx][V_oc[t_idx] > V_max] = V_max
         
    # Voltage under load:
    if battery_discharge_flag:
        V_ul[t_idx]    = V_oc[t_idx]  - I_cell[t_idx]*R_0[t_idx]
    else: 
        V_ul[t_idx]    = V_oc[t_idx]  + I_cell[t_idx]*R_0[t_idx]
        
    # Compute internal resistance
    R_bat        = -0.0169*(SOC[t_idx]**4) + 0.0418*(SOC[t_idx]**3) - 0.0273*(SOC[t_idx]**2) + 0.0069*(SOC[t_idx]) + 0.0043
    R_0[t_idx]   = R_bat*battery_conditions.cell.resistance_growth_factor 
    
    # Compute Heat power generated by all cells
    Q_heat_cell[t_idx] = (I_cell[t_idx]**2.)*R_0[t_idx]
    Q_heat_pack[t_idx] = (I_pack[t_idx]**2.)*R_0[t_idx]
    
    # Effective Power flowing through battery 
    P_pack[t_idx]   = P_bat[t_idx]  - np.abs(Q_heat_pack[t_idx])
    
        
    # store remaining variables 
    I_pack[t_idx]         = I_bat[t_idx]  
    V_oc_pack[t_idx]      = V_oc[t_idx]*n_series 
    V_ul_pack[t_idx]      = V_ul[t_idx]*n_series  
    T_pack[t_idx]         = T_cell[t_idx] 
    P_cell[t_idx]         = P_pack[t_idx]/n_total  
    E_cell[t_idx]         = E_pack[t_idx]/n_total  

    # ---------------------------------------------------------------------------------------------------
    # Future State 
    # --------------------------------------------------------------------------------------------------- 
    if t_idx != state.numerics.number_of_control_points-1:  
        # Compute cell temperature
        if HAS is not None:
            T_cell[t_idx+1] = HAS.compute_thermal_performance(battery,coolant_line, Q_heat_cell[t_idx],T_cell[t_idx],state,delta_t[t_idx],t_idx)
        else:
            # Considers a thermally insulated system and the heat piles on in the system
            Q_heat_pack[t_idx+1]  = Q_heat_cell[t_idx]*battery.pack.electrical_configuration.total
            dT_dt                 = Q_heat_cell[t_idx]/(cell_mass*Cp)
            T_cell[t_idx+1]       =  T_cell[t_idx] + dT_dt*delta_t[t_idx]
                
        # Compute state of charge and depth of discarge of the battery
        E_pack[t_idx+1]                          = E_pack[t_idx] -P_pack[t_idx]*delta_t[t_idx]
        E_pack[t_idx+1][E_pack[t_idx+1] > E_max] = E_max 
        SOC[t_idx+1]                             = E_pack[t_idx+1]/E_max 
        DOD_cell[t_idx+1]                        = 1 - SOC[t_idx+1] 
        
        # Determine new charge throughput (the amount of charge gone through the battery)
        Q_cell[t_idx+1]    = Q_cell[t_idx] + I_cell[t_idx]*delta_t[t_idx]/Units.hr
                    
    return       