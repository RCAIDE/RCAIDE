## @ingroup Energy-Sources-Batteries
# RCAIDE/Energy/Sources/Batteries/Lithium_Ion_LiFePO4_18650.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports 
from RCAIDE.Core          import Units  
from .Lithium_Ion_Generic import Lithium_Ion_Generic 

# package imports 
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
#  Lithium_Ion_LFP
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Sources-Batteries 
class Lithium_Ion_LFP(Lithium_Ion_Generic):
    """ Specifies discharge/specific energy characteristics specific 
        18650 lithium-iron-phosphate-oxide battery cells.     
        
        Assumptions: 
        N/A 
        
        Source:
        # Cell Information 
        Saw, L. H., Yonghuang Ye, and A. A. O. Tay. "Electrochemical–thermal analysis of 
        18650 Lithium Iron Phosphate cell." Energy Conversion and Management 75 (2013): 
        162-174.
        
        # Electrode Area
        Muenzel, Valentin, et al. "A comparative testing study of commercial
        18650-format lithium-ion battery cells." Journal of The Electrochemical
        Society 162.8 (2015): A1592.
        
        # Cell Thermal Conductivities 
        (radial)
        Murashko, Kirill A., Juha Pyrhönen, and Jorma Jokiniemi. "Determination of the 
        through-plane thermal conductivity and specific heat capacity of a Li-ion cylindrical 
        cell." International Journal of Heat and Mass Transfer 162 (2020): 120330.
        
        (axial)
        Saw, L. H., Yonghuang Ye, and A. A. O. Tay. "Electrochemical–thermal analysis of 
        18650 Lithium Iron Phosphate cell." Energy Conversion and Management 75 (2013): 
        162-174.
        
        Inputs:
        None
        
        Outputs:
        None
        
        Properties Used:
        N/A
        """ 
    def __defaults__(self):
        self.tag                              = 'lithium_ion_lfp' 
         
        self.cell.diameter                    = 0.0185                                                   # [m]
        self.cell.height                      = 0.0653                                                   # [m]
        self.cell.mass                        = 0.03  * Units.kg                                         # [kg]
        self.cell.surface_area                = (np.pi*self.cell.height*self.cell.diameter) + (0.5*np.pi*self.cell.diameter**2)  # [m^2]
        self.cell.volume                      = np.pi*(0.5*self.cell.diameter)**2*self.cell.height       # [m^3] 
        self.cell.density                     = self.cell.mass/self.cell.volume                          # [kg/m^3]
        self.cell.electrode_area              = 0.0342                                                   # [m^2]  # estimated 
                                                        
        self.cell.maximum_voltage             = 3.6                                                      # [V]
        self.cell.nominal_capacity            = 1.5                                                      # [Amp-Hrs]
        self.cell.nominal_voltage             = 3.6                                                      # [V]
        self.cell.charging_voltage            = self.cell.nominal_voltage                                # [V]  
         
        self.watt_hour_rating                 = self.cell.nominal_capacity  * self.cell.nominal_voltage  # [Watt-hours]      
        self.specific_energy                  = self.watt_hour_rating*Units.Wh/self.cell.mass            # [J/kg]
        self.specific_power                   = self.specific_energy/self.cell.nominal_capacity          # [W/kg]   
        self.ragone.const_1                   = 88.818  * Units.kW/Units.kg
        self.ragone.const_2                   = -.01533 / (Units.Wh/Units.kg)
        self.ragone.lower_bound               = 60.     * Units.Wh/Units.kg
        self.ragone.upper_bound               = 225.    * Units.Wh/Units.kg         
        self.resistance                       = 0.022                                                    # [Ohms]
                                                        
        self.specific_heat_capacity           = 1115                                                     # [J/kgK] 
        self.cell.specific_heat_capacity      = 1115                                                     # [J/kgK] 
        self.cell.radial_thermal_conductivity = 0.475                                                    # [J/kgK]  
        self.cell.axial_thermal_conductivity  = 37.6                                                     # [J/kgK]   
        
        return
    

    def energy_calc(self,state,bus,battery_discharge_flag= True): 
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
        battery            = self  
        battery_conditions = state.conditions.energy[bus.tag][self.tag]    
        btms               = battery.thermal_management_system  
        HAS                = btms.heat_acquisition_system
        HEX                = btms.heat_exchanger_system
        I_bat              = battery.outputs.current
        P_bat              = battery.outputs.power   
        V_max              = battery.cell.maximum_voltage      
        E_max              = battery_conditions.pack.maximum_initial_energy * battery_conditions.cell.capacity_fade_factor
        E_pack             = battery_conditions.pack.energy    
        I_pack             = battery_conditions.pack.current                        #  battery.outputs.current 
        V_oc_pack          = battery_conditions.pack.voltage_open_circuit           #  battery.pack.voltage_open_circuit
        V_ul_pack          = battery_conditions.pack.voltage_under_load             #  battery.pack.voltage_under_load 
        P_pack             = battery_conditions.pack.power                          #  battery_power_draw   
        T_pack             = battery_conditions.pack.temperature                    #  battery.pack.temperature  
        Q_heat_pack        = battery_conditions.pack.heat_energy_generated          #  battery.pack.heat_energy_generated 
        R_0                = battery_conditions.pack.internal_resistance            #  battery.pack.internal_resistance  
        Q_heat_cell        = battery_conditions.cell.heat_energy_generated          #  battery.pack.heat_energy_generated
        SOC                = battery_conditions.cell.state_of_charge                #  battery.cell.state_of_charge 
        P_cell             = battery_conditions.cell.power                          #  battery.outputs.power/n_series
        E_cell             = battery_conditions.cell.energy                         #  battery.pack.current_energy/n_total   
        V_ul               = battery_conditions.cell.voltage_under_load             #  battery.cell.voltage_under_load    
        V_oc               = battery_conditions.cell.voltage_open_circuit           #  battery.cell.voltage_open_circuit  
        I_cell             = battery_conditions.cell.current                        #  abs(battery.cell.current)        
        T_cell             = battery_conditions.cell.temperature                    #  battery.cell.temperature
        Q_cell             = battery_conditions.cell.charge_throughput              #  battery.cell.charge_throughput  
        DOD_cell           = battery_conditions.cell.depth_of_discharge 
        time               = state.conditions.frames.inertial.time[:,0]  
        
        # ---------------------------------------------------------------------------------
        # Compute battery electrical properties 
        # --------------------------------------------------------------------------------- 
        # Calculate the current going into one cell  
        n_series          = battery.pack.electrical_configuration.series  
        n_parallel        = battery.pack.electrical_configuration.parallel 
        n_total           = battery.pack.electrical_configuration.total 
        
        delta_t           = np.diff(time)
        for t_idx in range(state.numerics.number_of_control_points):       
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
            R_bat                    = -0.0169*(SOC[t_idx]**4) + 0.0418*(SOC[t_idx]**3) - 0.0273*(SOC[t_idx]**2) + 0.0069*(SOC[t_idx]) + 0.0043
            R_0[t_idx]               = R_bat*battery_conditions.cell.resistance_growth_factor 
            R_0[t_idx][R_0[t_idx]<0] = 0.  
            
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
            # Current State 
            # --------------------------------------------------------------------------------------------------- 
            if t_idx != state.numerics.number_of_control_points-1:  
                # Compute cell temperature   
                HAS_results  = HAS.compute_heat_removed(battery,Q_heat_cell[t_idx],T_cell[t_idx],state,delta_t[t_idx],t_idx) 
                HEX_results  = HEX.compute_heat_removed(HAS_results,state,delta_t[t_idx],t_idx)
                
                # Temperature 
                T_cell[t_idx+1] = HAS_results.current_battery_temperature
                    
                # Compute state of charge and depth of discarge of the battery
                E_pack[t_idx+1]                          = E_pack[t_idx] -P_pack[t_idx]*delta_t[t_idx] 
                E_pack[t_idx+1][E_pack[t_idx+1] > E_max] = E_max 
                SOC[t_idx+1]                             = E_pack[t_idx+1]/E_max  
                SOC[t_idx+1][SOC[t_idx+1]>1]             = 1.
                SOC[t_idx+1][SOC[t_idx+1]<0]             = 0. 
                DOD_cell[t_idx+1]                        = 1 - SOC[t_idx+1] 
                
                # Determine new charge throughput (the amount of charge gone through the battery)
                Q_cell[t_idx+1]    = Q_cell[t_idx] + I_cell[t_idx]*delta_t[t_idx]/Units.hr
                        
        return     
    
    def compute_voltage(self,battery_conditions):
        """ Computes the voltage of a single LFP cell or a battery pack of LFP cells   
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:  
                state   - segment unknowns to define voltage [unitless]
            
            Outputs
                V_ul    - under-load voltage                 [volts]
             
            Properties Used:
            N/A
        """              

        return battery_conditions.pack.voltage_under_load 
    
    def update_battery_age(self,segment,increment_battery_age_by_one_day = False):   
        pass 
        return  
 
  
      