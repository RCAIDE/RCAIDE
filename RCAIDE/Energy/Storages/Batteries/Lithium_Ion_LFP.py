## @ingroup Energy-Storages-Batteries
# RCAIDE/Energy/Storages/Batteries/Lithium_Ion_LiFePO4_18650.py
# (c) Copyright 2023 Aerospace Research Community LLC
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
from scipy.integrate    import  cumtrapz

# ----------------------------------------------------------------------------------------------------------------------
#  Lithium_Ion_LFP
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Storages-Batteries 
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
        self.tag                              = 'Lithium_Ion_LFP' 
         
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
    

    def energy_calc(self,numerics,conditions,bus_tag,battery_discharge_flag= True): 
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
                  resistive_losses                                         [Watts] 
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
        battery           = self 
        btms              = battery.thermal_management_system 
        I_bat             = battery.outputs.current
        P_bat             = battery.outputs.power   
        V_max             = battery.cell.maximum_voltage   
        T_current         = battery.pack.temperature   
        E_max             = conditions.energy[bus_tag][self.tag].pack.maximum_degraded_battery_energy
        E_current         = battery.pack.current_energy 
        Q_prior           = battery.cell.charge_throughput 
        R_growth_factor   = battery.cell.R_growth_factor
        E_growth_factor   = battery.cell.E_growth_factor 
        I                 = numerics.time.integrate
        D                 = numerics.time.differentiate
        
        # ---------------------------------------------------------------------------------
        # Compute battery electrical properties 
        # --------------------------------------------------------------------------------- 
        # Calculate the current going into one cell  
        n_series          = battery.pack.electrical_configuration.series  
        n_parallel        = battery.pack.electrical_configuration.parallel
        n_total           = n_series*n_parallel
        Nn                = battery.module.geometrtic_configuration.normal_count            
        Np                = battery.module.geometrtic_configuration.parallel_count          
        n_total_module    = Nn*Np     
        I_cell            = I_bat/n_parallel
 
        # ---------------------------------------------------------------------------------
        # Compute battery electrical properties 
        # ---------------------------------------------------------------------------------  
        # Update battery capacitance (energy) with aging factor
        E_max = E_max*E_growth_factor
        
        # Compute state of charge and depth of discarge of the battery
        initial_discharge_state = np.dot(I,P_bat) + E_current[0]
        SOC_old                 = np.divide(initial_discharge_state,E_max)
        
        SOC_old[SOC_old>1] = 1.
        SOC_old[SOC_old<0] = 0.
        
        # Compute internal resistance
        R_bat = -0.0169*(SOC_old**4) + 0.0418*(SOC_old**3) - 0.0273*(SOC_old**2) + 0.0069*(SOC_old) + 0.0043
        R_0   = R_bat*R_growth_factor 
        R_0[R_0<0] = 0.  # when battery isn't being called
        
        # Compute Heat power generated by all cells
        Q_heat_gen = (I_bat**2.)*R_0  
        
        # Compute cell temperature  
        btms_results = btms.compute_net_generated_battery_heat(battery,Q_heat_gen,numerics,conditions.freestream)
        T_current    = btms_results.operating_conditions.battery_current_temperature
    
        # Power going into the battery accounting for resistance losses
        P_loss = n_total*Q_heat_gen
        P      = -P_bat - np.abs(P_loss)       
        
        # Possible Energy going into the battery:
        energy_unmodified = np.dot(I,P)
    
        # Available capacity
        capacity_available = E_max - battery.pack.current_energy[0]
    
        # How much energy the battery could be overcharged by
        delta           = energy_unmodified -capacity_available
        delta[delta<0.] = 0.
    
        # Power that shouldn't go in
        ddelta = np.dot(D,delta) 
    
        # Power actually going into the battery
        P[P>0.] = P[P>0.] - ddelta[P>0.]
        E_bat = np.dot(I,P)
        E_bat = np.reshape(E_bat,np.shape(E_current)) #make sure it's consistent
        
        # Add this to the current state
        if np.isnan(E_bat).any():
            E_bat=np.ones_like(E_bat)*np.max(E_bat)
            if np.isnan(E_bat.any()): #all nans; handle this instance
                E_bat=np.zeros_like(E_bat)
                
        E_current = E_bat + E_current[0]
        
        SOC_new = np.divide(E_current,E_max)
        SOC_new[SOC_new>1] = 1.
        SOC_new[SOC_new<0] = 0. 
        DOD_new = 1 - SOC_new
          
        # Determine new charge throughput (the amount of charge gone through the battery)
        Q_total    = np.atleast_2d(np.hstack(( Q_prior[0] , Q_prior[0] + cumtrapz(abs(I_cell)[:,0], x   = numerics.time.control_points[:,0])/Units.hr ))).T      
                
        # A voltage model from Chen, M. and Rincon-Mora, G. A., "Accurate Electrical Battery Model Capable of Predicting
        # Runtime and I - V Performance" IEEE Transactions on Energy Conversion, Vol. 21, No. 2, June 2006, pp. 504-511
        V_normalized  = (-1.031*np.exp(-35.*SOC_new) + 3.685 + 0.2156*SOC_new - 0.1178*(SOC_new**2.) + 0.3201*(SOC_new**3.))/4.1
        V_oc = V_normalized * V_max
        V_oc[ V_oc > V_max] = V_max
        
        # Voltage under load:
        if battery_discharge_flag:
            V_ul    = V_oc  - I_cell*R_0
        else: 
            V_ul    = V_oc  + I_cell*R_0 
             
        # Pack outputs
        battery.pack.load_power                    = V_ul*n_series*I_bat
        battery.cell.depth_of_discharge            = DOD_new
        battery.pack.resistive_losses              = Q_heat_gen
        battery.pack.current_energy                = E_current
        battery.pack.temperature                   = T_current 
        battery.pack.voltage_open_circuit          = V_oc*n_series
        battery.pack.voltage_under_load            = V_ul*n_series
        battery.pack.current                       = I_cell
        battery.pack.heat_energy_generated         = Q_heat_gen 
        battery.pack.internal_resistance           = R_0 
        battery.cell.charge_throughput             = Q_total  
        battery.cell.state_of_charge               = SOC_new 
        battery.cell.temperature                   = T_current   
        battery.cell.voltage_open_circuit          = V_oc 
        battery.cell.current                       = I_cell 
        battery.cell.voltage_under_load            = V_ul 
        battery.cell.joule_heat_fraction           = np.zeros_like(V_ul)
        battery.cell.entropy_heat_fraction         = np.zeros_like(V_ul)  
        
        return      
    
    def assign_battery_unknowns(self,segment,bus,battery): 
        """ Appends unknowns specific to LFP cells which are unpacked from the mission solver and send to the network.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            state.unknowns.battery_voltage_under_load                [volts]
            segment                                                  [N.A]
            b_i                                                      [unitless]
    
            Outputs: 
            state.conditions.energy.battery.pack.voltage_under_load  [volts]
    
            Properties Used:
            N/A
        """             

        if bus.fixed_voltage == False: 
            battery_conditions                          = segment.state.conditions.energy[bus.tag][battery.tag]  
            battery_conditions.pack.voltage_under_load  = segment.state.unknowns[bus.tag + '_' + battery.tag + '_voltage_under_load']  
        
        return 
    
    def assign_battery_residuals(self,segment,bus,battery): 
        """ Packs the residuals specific to LFP cells to be sent to the mission solver.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            segment.state.conditions.energy:
                motor.torque                                [N-m]
                rotor.torque                                [N-m]
                voltage_under_load                          [volts]
            state.unknowns.battery_voltage_under_load       [volts] 
            b_i                                             [unitless]
            
            Outputs:
            None
    
            Properties Used:
            network.voltage                                 [volts]
        """     
        

        if bus.fixed_voltage == False:         
            battery_conditions = segment.state.conditions.energy[bus.tag][battery.tag]
            v_actual           = battery_conditions.pack.voltage_under_load
            v_predict          = segment.state.unknowns[bus.tag + '_' + battery.tag + '_voltage_under_load']  
            v_max              = bus.voltage
            
            # Return the residuals
            segment.state.residuals.network[bus.tag + '_' + battery.tag + 'voltage']  = (v_predict - v_actual)/v_max
        
        return 
    
    def append_battery_unknowns_and_residuals_to_segment(self,
                                                         segment,
                                                         bus,
                                                         battery,
                                                         estimated_voltage,
                                                         estimated_cell_temperature,
                                                         estimated_state_of_charge,
                                                         estimated_cell_current): 
        """ Sets up the information that the mission needs to run a mission segment using this network
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:    
            b_i                                              [unitless]
            estimated_voltage                                  [volts]
            estimated_battery_cell_temperature                     [Kelvin]
            estimated_battery_state_of_charges                 [unitless]
            estimated_battery_cell_currents                         [Amperes]
            
            Outputs
            None
            
            Properties Used:
            N/A
        """        
        
        ones_row = segment.state.ones_row 
        if bus.fixed_voltage == False:  
            segment.state.unknowns[bus.tag + '_' + battery.tag + '_voltage_under_load']  = estimated_voltage * ones_row(1)     
        
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
        print(' No aging model currently implemented for LFP cells. Pristine condition of \n '
              'the battery cell will be assigned each charge cycle')
        return  
 
  
      