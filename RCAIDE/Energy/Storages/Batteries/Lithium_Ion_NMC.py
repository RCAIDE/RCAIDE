## @ingroup Energy-Storages-Batteries
# RCAIDE/Energy/Storages/Batteries/Lithium_Ion_LiNiMnCoO2_18650.py
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
from RCAIDE.Methods.Power.Battery.State_Estimation_Models.LiNiMnCoO2_state_estimation_model import compute_NMC_cell_state_variables
from RCAIDE.Methods.Power.Battery.Common.compute_net_generated_battery_heat                 import compute_net_generated_battery_heat

# package imports 
import numpy as np
import os
from scipy.integrate    import  cumtrapz
from scipy.interpolate  import RegularGridInterpolator 

# ----------------------------------------------------------------------------------------------------------------------
#  Lithium_Ion_NMC
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Storages-Batteries 
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
        self.tag                              = 'Lithium_Ion_NMC'  

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
    
    def energy_calc(self,numerics,conditions,bus_tag,battery_discharge_flag = True ): 
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
        battery                  = self
        btms                     = battery.thermal_management_system
        I_bat                    = battery.outputs.current              # current coming out of battery 
        P_bat                    = battery.outputs.power                # power coming out of battery 
        electrode_area           = battery.cell.electrode_area 
        As_cell                  = battery.cell.surface_area  
        Q_prior                  = battery.cell.charge_throughput     
        T_cell                   = battery.cell.temperature       
        E_max                    = conditions.energy[bus_tag][self.tag].pack.maximum_initial_energy * conditions.energy[bus_tag][self.tag].cell.capacity_fade_factor
        E_current                = battery.pack.current_energy 
        battery_data             = battery.discharge_performance_map     
        I                        = numerics.time.integrate      
        D                        = numerics.time.differentiate

        # ---------------------------------------------------------------------------------
        # Compute battery electrical properties 
        # --------------------------------------------------------------------------------- 
        # Calculate the current going into one cell  
        n_series          = battery.pack.electrical_configuration.series  
        n_parallel        = battery.pack.electrical_configuration.parallel 
        Nn                = battery.module.geometrtic_configuration.normal_count            
        Np                = battery.module.geometrtic_configuration.parallel_count          
        n_total_module    = Nn*Np     
        I_cell            = I_bat/n_parallel
        
        # State of charge of the battery
        initial_discharge_state = np.dot(I,-P_bat) + E_current[0]
        SOC_old                 = np.divide(initial_discharge_state,E_max) 
          
        # Make sure things do not break by limiting current, temperature and current 
        SOC_old[SOC_old < 0.] = 0.  
        SOC_old[SOC_old > 1.] = 1.   
        
        T_cell[T_cell<272.65]  = 272.65
        T_cell[T_cell>322.65]  = 322.65
        
        battery.cell.temperature = T_cell
        battery.pack.temperature = T_cell
        
        # ---------------------------------------------------------------------------------
        # Compute battery cell temperature 
        # ---------------------------------------------------------------------------------
        # Determine temperature increase         
        sigma   = 139 # Electrical conductivity
        n       = 1
        F       = 96485 # C/mol Faraday constant    
        delta_S = -496.66*(SOC_old)**6 +  1729.4*(SOC_old)**5 + -2278 *(SOC_old)**4 +  1382.2 *(SOC_old)**3 + \
                  -380.47*(SOC_old)**2 +  46.508*(SOC_old)    + -10.692  
        
        i_cell         = I_cell/electrode_area # current intensity 
        q_dot_entropy  = -(T_cell)*delta_S*i_cell/(n*F)       
        q_dot_joule    = (i_cell**2)/sigma                   
        Q_heat_gen     = (q_dot_joule + q_dot_entropy)*As_cell 
        q_joule_frac   = q_dot_joule/(q_dot_joule + q_dot_entropy)
        q_entropy_frac = q_dot_entropy/(q_dot_joule + q_dot_entropy)

        # Compute cell temperature  
        btms_results = btms.compute_net_generated_battery_heat(battery,Q_heat_gen,numerics,conditions.freestream)
        T_current    = btms_results.operating_conditions.battery_current_temperature

        # Effective Power flowing through battery 
        P      = -(P_bat + np.abs(btms_results.operating_conditions.heat_energy_generated)) 
        
        # Compute State Variables
        V_ul  = compute_NMC_cell_state_variables(battery_data,SOC_old,T_cell,I_cell)
        
        # Li-ion battery interal resistance
        R_0      =  0.01483*(SOC_old**2) - 0.02518*SOC_old + 0.1036
        
        # Voltage under load: 
        V_oc      = V_ul + (I_cell * R_0) 
        
        # ---------------------------------------------------------------------------------
        # Compute updated state of battery 
        # ---------------------------------------------------------------------------------   
        
        # How much energy the battery could be overcharged by
        delta           =  np.dot(I,P) - E_current[0]
        delta[delta<0.] = 0.
    
        # Power that shouldn't go in
        ddelta = np.dot(D,delta) 
    
        # Power actually going into the battery
        P[P>0.] = P[P>0.] - ddelta[P>0.]
        E_bat = np.dot(I,P)
        E_bat = np.reshape(E_bat,np.shape(E_current)) # make sure it's consistent
        
        # Add this to the current state
        if np.isnan(E_bat).any():
            E_bat=np.ones_like(E_bat)*np.max(E_bat)
            if np.isnan(E_bat.any()): #all nans; handle this instance
                E_bat=np.zeros_like(E_bat)
                
        E_current = E_bat + E_current[0]
        
        # Determine new State of Charge 
        SOC_new = np.divide(E_current, E_max)
        SOC_new[SOC_new<0] = 0. 
        SOC_new[SOC_new>1] = 1.
        DOD_new = 1 - SOC_new 
        
        # Determine new charge throughput (the amount of charge gone through the battery)
        Q_total    = np.atleast_2d(np.hstack(( Q_prior[0] , Q_prior[0] + cumtrapz(I_cell[:,0], x = numerics.time.control_points[:,0])/Units.hr ))).T   
        
        # If SOC is negative, voltage under load goes to zero 
        V_ul[SOC_new < 0.] = 0. 
            
        # Pack outputs
        battery.pack.generated_heat                = btms_results.operating_conditions.heat_energy_generated
        battery.pack.load_power                    = V_ul*n_series*I_bat
        battery.pack.current_energy                = E_current
        battery.pack.temperature                   = T_current 
        battery.pack.current                       = I_bat
        battery.pack.voltage_open_circuit          = V_oc*n_series
        battery.pack.heat_energy_generated         = Q_heat_gen*n_total_module    
        battery.pack.internal_resistance           = R_0*n_series
        battery.pack.voltage_under_load            = V_ul*n_series 
        battery.pack.state_of_charge               = SOC_new
        battery.cell.voltage_open_circuit          = V_oc
        battery.cell.current                       = I_cell
        battery.cell.charge_throughput             = Q_total   
        battery.cell.state_of_charge               = SOC_new
        battery.cell.depth_of_discharge            = DOD_new
        battery.cell.voltage_under_load            = V_ul
        battery.cell.temperature                   = T_current 
        battery.cell.joule_heat_fraction           = q_joule_frac
        battery.cell.entropy_heat_fraction         = q_entropy_frac
        
        return battery 
       
    def assign_battery_unknowns(self,segment,bus,battery): 
        """ Appends unknowns specific to NMC cells which are unpacked from the mission solver and send to the network.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            segment.state.unknowns,battery
                .cell.temperature                    [Kelvin]
                .cell.state_of_charge                [unitless]
                .current                             [Amperes]
            b_i                                      [unitless]
    
            Outputs: 
            segment.state.conditions.energy.battery
                .cell.temperature                    [Kelvin]  
                .cell.state_of_charge                [unitless]
                .pack.current                        [Amperes]
    
            Properties Used:
            N/A
        """ 

        return     
    

    def assign_battery_residuals(self,segment,bus,battery): 
        """ Packs the residuals specific to NMC cells to be sent to the mission solver.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            self                - battery data structure              [unitless] 
            segment.state.conditions.energy:
                battery.cell.state_of_charge                          [unitless] 
                battery.cell.temperature                              [Kelvin]        
                battery.current                                       [Amperes]
            segment.state.unknowns.                         
                battery.cell.state_of_charge                          [unitless]
                battery.cell.temperature                              [Kelvin]  
                battery.current                                       [Amperes]
            b_i                                                       [unitless]

            Outputs:
            None
    
            Properties Used:
            None
        """       
        
        return  
    
    def append_battery_unknowns_and_residuals_to_segment(self,
                                                         segment, 
                                                         bus, 
                                                         battery,
                                                         estimated_voltage): 
        """ Sets up the information that the mission needs to run a mission segment using this network
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:  
            self                - battery data structure              [unitless]
            segment             - segment data struction              [unitless]
            estimated_voltage                                         [volts] 
            estimated_cell_temperature                                [Kelvin]
            estimated_state_of_charge                                 [unitless]
            estimated_cell_current                                    [Amperes]
            b_i                                                       [unitless]
            
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
        
        # Unpack battery properties
        battery                  = self
        battery_data             = battery.discharge_performance_map
        n_series                 = battery.pack.electrical_configuration.series  
        n_parallel               = battery.pack.electrical_configuration.parallel
        
        # Unpack segment state properties  
        SOC                      = battery_conditions.cell.state_of_charge
        T_cell                   = battery_conditions.cell.temperature
        I_cell                   = battery_conditions.pack.current/n_parallel 

        # Link Temperature and update
        battery.cell.temperature = T_cell
        
        # Compute State Variables
        V_ul_cell                = compute_NMC_cell_state_variables(battery_data,SOC,T_cell,I_cell) 
        
        # Voltage under load
        V_ul                     = n_series*V_ul_cell    
           
        return V_ul 
    
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
