## @ingroup Energy-Sources-Batteries
# RCAIDE/Energy/Sources/Batteries/Lithium_Ion_LiNiMnCoO2_18650.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports
import RCAIDE
from RCAIDE.Core                                                                            import Units , Data
from .Lithium_Ion_Generic                                                                   import Lithium_Ion_Generic  
from RCAIDE.Methods.Energy.Sources.Battery.State_Estimation_Models.LiNiMnCoO2_state_estimation_model import compute_NMC_cell_state_variables 

# package imports 
import numpy as np
import os 
from scipy.interpolate  import RegularGridInterpolator 

# ----------------------------------------------------------------------------------------------------------------------
#  Lithium_Ion_NMC
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Sources-Batteries 
class Lithium_Ion_NMC(Lithium_Ion_Generic):
    """ Specifies discharge/specific energy characteristics specific 
        18650 lithium-nickel-manganese-cobalt-oxide battery cells     
        
        Assumptions:
        Convective Thermal Conductivity Coefficient corresponds to forced
        air cooling in 35 m/s air 
        
        Source:
        Automotive Industrial Systems Company of Panasonic Group, Technical Information of 
        NCR18650G, URL https://www.imrbatteries.com/content/panasonic_ncr18650g.pdf
        
        convective  heat transfer coefficient, h 
        Jeon, Dong Hyup, and Seung Man Baek. "Thermal modeling of cylindrical 
        lithium ion battery during discharge cycle." Energy Conversion and Management
        52.8-9 (2011): 2973-2981.
        
        thermal conductivity, k 
        Yang, Shuting, et al. "A Review of Lithium-Ion Battery Thermal Management 
        System Strategies and the Evaluate Criteria." Int. J. Electrochem. Sci 14
        (2019): 6077-6107.
        
        specific heat capacity, Cp
        (axial and radial)
        Yang, Shuting, et al. "A Review of Lithium-Ion Battery Thermal Management 
        System Strategies and the Evaluate Criteria." Int. J. Electrochem. Sci 14
        (2019): 6077-6107.
        
        # Electrode Area
        Muenzel, Valentin, et al. "A comparative testing study of commercial
        18650-format lithium-ion battery cells." Journal of The Electrochemical
        Society 162.8 (2015): A1592.
        
        Inputs:
        None
        
        Outputs:
        None
        
        Properties Used:
        N/A
    """       
    
    def __defaults__(self):    
        self.tag                              = 'lithium_ion_nmc'  

        self.cell.diameter                    = 0.0185                                                   # [m]
        self.cell.height                      = 0.0653                                                   # [m]
        self.cell.mass                        = 0.048 * Units.kg                                         # [kg]
        self.cell.surface_area                = (np.pi*self.cell.height*self.cell.diameter) + (0.5*np.pi*self.cell.diameter**2)  # [m^2]
        self.cell.volume                      = np.pi*(0.5*self.cell.diameter)**2*self.cell.height 
        self.cell.density                     = self.cell.mass/self.cell.volume                          # [kg/m^3]  
        self.cell.electrode_area              = 0.0342                                                   # [m^2] 
                                                                                               
        self.cell.maximum_voltage             = 4.2                                                      # [V]
        self.cell.nominal_capacity            = 3.55                                                     # [Amp-Hrs]
        self.cell.nominal_voltage             = 3.6                                                      # [V] 
        self.cell.charging_voltage            = self.cell.nominal_voltage                                # [V] 
        
        self.watt_hour_rating                 = self.cell.nominal_capacity  * self.cell.nominal_voltage  # [Watt-hours]      
        self.specific_energy                  = self.watt_hour_rating*Units.Wh/self.cell.mass            # [J/kg]
        self.specific_power                   = self.specific_energy/self.cell.nominal_capacity          # [W/kg]   
        self.resistance                       = 0.025                                                    # [Ohms]
                                                                                                         
        self.specific_heat_capacity           = 1108                                                     # [J/kgK]  
        self.cell.specific_heat_capacity      = 1108                                                     # [J/kgK]    
        self.cell.radial_thermal_conductivity = 0.4                                                      # [J/kgK]  
        self.cell.axial_thermal_conductivity  = 32.2                                                     # [J/kgK] # estimated  
                                              
        battery_raw_data                      = load_battery_results()                                                   
        self.discharge_performance_map        = create_discharge_performance_map(battery_raw_data)  
         
        return  
    
    def energy_calc(self,state,bus,battery_discharge_flag= True): 
        '''This is an electric cycle model for 18650 lithium-nickel-manganese-cobalt-oxide
           battery cells. The model uses experimental data performed
           by the Automotive Industrial Systems Company of Panasonic Group 
              
           Sources:  
           Internal Resistance Model:
           Zou, Y., Hu, X., Ma, H., and Li, S. E., "Combined State of Charge and State of
           Health estimation over lithium-ion battery cellcycle lifespan for electric 
           vehicles,"Journal of Power Sources, Vol. 273, 2015, pp. 793-803.
           doi:10.1016/j.jpowsour.2014.09.146,URLhttp://dx.doi.org/10.1016/j.jpowsour.2014.09.146. 
            
           Battery Heat Generation Model and  Entropy Model:
           Jeon, Dong Hyup, and Seung Man Baek. "Thermal modeling of cylindrical lithium ion 
           battery during discharge cycle." Energy Conversion and Management 52.8-9 (2011): 
           2973-2981. 
           
           Assumtions:
           1) All battery modules exhibit the same themal behaviour. 
           
           Inputs:
             battery.
                   I_bat             (maximum_energy)                      [Joules]
                   cell_mass         (battery cell mass)                   [kilograms]
                   Cp                (battery cell specific heat capacity) [J/(K kg)] 
                   t                 (battery age in days)                 [days] 
                   T_ambient         (ambient temperature)                 [Kelvin]
                   T_current         (pack temperature)                    [Kelvin]
                   T_cell            (battery cell temperature)            [Kelvin]
                   E_max             (max energy)                          [Joules]
                   E_current         (current energy)                      [Joules]
                   Q_prior           (charge throughput)                   [Amp-hrs]
                   R_growth_factor   (internal resistance growth factor)   [unitless]
           
             inputs.
                   I_bat             (current)                             [amps]
                   P_bat             (power)                               [Watts]
           
           Outputs:
             battery.
                  current_energy                                           [Joules]
                  temperature                                              [Kelvin]
                  heat_energy_generated                                    [Watts]
                  load_power                                               [Watts]
                  current                                                  [Amps]
                  battery_voltage_open_circuit                             [Volts]
                  charge_throughput                                        [Amp-hrs]
                  internal_resistance                                      [Ohms]
                  battery_state_of_charge                                  [unitless]
                  depth_of_discharge                                       [unitless]
                  battery_voltage_under_load                               [Volts]
           
        '''
        
        
        # Unpack varibles 
        battery            = self  
        battery_conditions = state.conditions.energy[bus.tag][self.tag]    
        btms               = battery.thermal_management_system 
        HAS                = btms.heat_acquisition_system
        HEX                = btms.heat_exchanger_system
        electrode_area     = battery.cell.electrode_area 
        As_cell            = battery.cell.surface_area           
        battery_data       = battery.discharge_performance_map  
        I_bat              = battery.outputs.current
        P_bat              = battery.outputs.power      
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
            I_cell[t_idx]        = I_bat[t_idx]/n_parallel   
  
            # ---------------------------------------------------------------------------------
            # Compute battery cell temperature 
            # ---------------------------------------------------------------------------------
            R_0[t_idx]               =  0.01483*(SOC[t_idx]**2) - 0.02518*SOC[t_idx] + 0.1036  
            R_0[t_idx][R_0[t_idx]<0] = 0. 
            
            # Determine temperature increase         
            sigma                 = 139 # Electrical conductivity
            n                     = 1
            F                     = 96485 # C/mol Faraday constant    
            delta_S               = -496.66*(SOC[t_idx])**6 +  1729.4*(SOC[t_idx])**5 + -2278 *(SOC[t_idx])**4 +  1382.2 *(SOC[t_idx])**3 + \
                                    -380.47*(SOC[t_idx])**2 +  46.508*(SOC[t_idx])    + -10.692  
            
            i_cell                = I_cell[t_idx]/electrode_area # current intensity 
            q_dot_entropy         = -(T_cell[t_idx])*delta_S*i_cell/(n*F)       
            q_dot_joule           = (i_cell**2)/sigma                   
            Q_heat_cell[t_idx]    = (q_dot_joule + q_dot_entropy)*As_cell 
            Q_heat_pack[t_idx]    = Q_heat_cell[t_idx]*n_total  
                  
            V_ul[t_idx]           = compute_NMC_cell_state_variables(battery_data,SOC[t_idx],T_cell[t_idx],I_cell[t_idx]) 
            
            V_oc[t_idx]           = V_ul[t_idx] + (I_cell[t_idx] * R_0[t_idx])              
            
            # Effective Power flowing through battery 
            P_pack[t_idx]         = P_bat[t_idx]  - np.abs(Q_heat_pack[t_idx]) 
                
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
        
        return battery   
    
    def compute_voltage(self,battery_conditions):  
        """ Computes the voltage of a single NMC cell or a battery pack of NMC cells  
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:  
                self                - battery data structure             [unitless]
                battery_conditions  - segment unknowns to define voltage [unitless]
            
            Outputs
                V_ul                - under-load voltage                 [volts]
             
            Properties Used:
            N/A
        """              
        return battery_conditions.pack.voltage_under_load 
    
    def update_battery_age(self,battery_conditions,increment_battery_age_by_one_day = False):  
        """ This is an aging model for 18650 lithium-nickel-manganese-cobalt-oxide batteries. 
       
        Source: 
        Schmalstieg, Johannes, et al. "A holistic aging model for Li (NiMnCo) O2
        based 18650 lithium-ion batteries." Journal of Power Sources 257 (2014): 325-334.
          
        Assumptions:
        None
    
        Inputs:
          segment.conditions.energy. 
             battery.cycle_in_day                                                   [unitless]
             battery.cell.temperature                                               [Kelvin] 
             battery.voltage_open_circuit                                           [Volts] 
             battery.charge_throughput                                              [Amp-hrs] 
             battery.cell.state_of_charge                                           [unitless] 
        
        Outputs:
           segment.conditions.energy.
             battery.capacity_fade_factor     (internal resistance growth factor)   [unitless]
             battery.resistance_growth_factor (capactance (energy) growth factor)   [unitless]  
             
        Properties Used:
        N/A 
        """    
        n_series   = self.pack.electrical_configuration.series
        SOC        = battery_conditions.cell.state_of_charge
        V_ul       = battery_conditions.pack.voltage_under_load/n_series
        t          = battery_conditions.cell.cycle_in_day         
        Q_prior    = battery_conditions.cell.charge_throughput[-1,0] 
        Temp       = np.mean(battery_conditions.cell.temperature) 
        
        # aging model  
        delta_DOD = abs(SOC[0][0] - SOC[-1][0])
        rms_V_ul  = np.sqrt(np.mean(V_ul**2)) 
        alpha_cap = (7.542*np.mean(V_ul) - 23.75) * 1E6 * np.exp(-6976/(Temp))  
        alpha_res = (5.270*np.mean(V_ul) - 16.32) * 1E5 * np.exp(-5986/(Temp))  
        beta_cap  = 7.348E-3 * (rms_V_ul - 3.667)**2 +  7.60E-4 + 4.081E-3*delta_DOD
        beta_res  = 2.153E-4 * (rms_V_ul - 3.725)**2 - 1.521E-5 + 2.798E-4*delta_DOD
        
        E_fade_factor   = 1 - alpha_cap*(t**0.75) - beta_cap*np.sqrt(Q_prior)   
        R_growth_factor = 1 + alpha_res*(t**0.75) + beta_res*Q_prior  
        
        battery_conditions.cell.capacity_fade_factor     = np.minimum(E_fade_factor,battery_conditions.cell.capacity_fade_factor)
        battery_conditions.cell.resistance_growth_factor = np.maximum(R_growth_factor,battery_conditions.cell.resistance_growth_factor)
        
        if increment_battery_age_by_one_day:
            battery_conditions.cell.cycle_in_day += 1 # update battery age by one day 
      
        return  

def create_discharge_performance_map(battery_raw_data):
    """ Creates discharge and charge response surface for 
        LiNiMnCoO2 battery cells 
        
        Source:
        N/A
        
        Assumptions:
        N/A
        
        Inputs: 
            
        Outputs: 
        battery_data

        Properties Used:
        N/A
                                
    """  
    
    # Process raw data 
    processed_data = process_raw_data(battery_raw_data)
    
    # Create performance maps 
    battery_data = create_response_surface(processed_data) 
    
    return battery_data

def create_response_surface(processed_data):
    
    battery_map             = Data() 
    amps                    = np.linspace(0, 8, 5)
    temp                    = np.linspace(0, 50, 6) +  272.65
    SOC                     = np.linspace(0, 1, 15)
    battery_map.Voltage     = RegularGridInterpolator((amps, temp, SOC), processed_data.Voltage,bounds_error=False,fill_value=None)
    battery_map.Temperature = RegularGridInterpolator((amps, temp, SOC), processed_data.Temperature,bounds_error=False,fill_value=None) 
     
    return battery_map 

def process_raw_data(raw_data):
    """ Takes raw data and formats voltage as a function of SOC, current and temperature
        
        Source 
        N/A
        
        Assumptions:
        N/A
        
        Inputs:
        raw_Data     
            
        Outputs: 
        procesed_data 

        Properties Used:
        N/A
                                
    """
    processed_data = Data()
     
    processed_data.Voltage        = np.zeros((5,6,15,2)) # current , operating temperature , SOC vs voltage      
    processed_data.Temperature    = np.zeros((5,6,15,2)) # current , operating temperature , SOC vs temperature 
    
    # Reshape  Data          
    raw_data.Voltage 
    for i, Amps in enumerate(raw_data.Voltage):
        for j , Deg in enumerate(Amps):
            min_x    = 0 
            max_x    = max(Deg[:,0])
            x        = np.linspace(min_x,max_x,15)
            y        = np.interp(x,Deg[:,0],Deg[:,1])
            vec      = np.zeros((15,2))
            vec[:,0] = x/max_x
            vec[:,1] = y
            processed_data.Voltage[i,j,:,:]= vec   
            
    for i, Amps in enumerate(raw_data.Temperature):
        for j , Deg in enumerate(Amps):
            min_x    = 0   
            max_x    = max(Deg[:,0])
            x        = np.linspace(min_x,max_x,15)
            y        = np.interp(x,Deg[:,0],Deg[:,1])
            vec      = np.zeros((15,2))
            vec[:,0] = x/max_x
            vec[:,1] = y
            processed_data.Temperature[i,j,:,:]= vec     
    
    return  processed_data  

def load_battery_results(): 
    '''Load experimental raw data of NMC cells 
    
    Source:
    Automotive Industrial Systems Company of Panasonic Group, Technical Information of 
    NCR18650G, URL https://www.imrbatteries.com/content/panasonic_ncr18650g.pdf
    
    Assumptions:
    N/A
    
    Inputs: 
    N/A
        
    Outputs: 
    battery_data

    Properties Used:
    N/A  
    '''    
    ospath    = os.path.abspath(__file__)
    separator = os.path.sep
    rel_path  = os.path.dirname(ospath) + separator     
    return RCAIDE.External_Interfaces.RCAIDE.load(rel_path+ 'NMC_Raw_Data.res')
