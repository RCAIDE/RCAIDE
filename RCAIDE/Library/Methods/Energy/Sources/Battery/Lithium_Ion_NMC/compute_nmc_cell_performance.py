## @ingroup Library-Methods-Energy-Sources-Battery-Lithium_Ion_NMC
# RCAIDE/Library/Methods/Energy/Sources/Battery/Lithium_Ion_NMC/compute_nmc_cell_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Feb 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
import numpy as np  
 
# ----------------------------------------------------------------------------------------------------------------------
# compute_nmc_cell_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Sources-Batteries-Lithium_Ion_NMC 
def compute_nmc_cell_performance(battery,state,bus,battery_discharge_flag): 
    """This is an electric cycle model for 18650 lithium-nickel-manganese-cobalt-oxide
       battery cells. The model uses experimental data performed
       by the Automotive Industrial Systems Company of Panasonic Group 

       Sources:  
       1) Internal Resistance Model:
          Zou, Y., Hu, X., Ma, H., and Li, S. E., "Combined State of Charge and State of
          Health estimation over lithium-ion battery cellcycle lifespan for electric 
          vehicles,"Journal of Power Sources, Vol. 273, 2015, pp. 793-803.
          doi:10.1016/j.jpowsour.2014.09.146,URLhttp://dx.doi.org/10.1016/j.jpowsour.2014.09.146. 
    
       3) Battery Heat Generation Model and  Entropy Model:
          Jeon, Dong Hyup, and Seung Man Baek. "Thermal modeling of cylindrical lithium ion 
          battery during discharge cycle." Energy Conversion and Management 52.8-9 (2011): 
          2973-2981. 

       Assumtions:
       1) All battery modules exhibit the same themal behaviour. 

       Args:
            battery.
                .thermal_management_system (dict): battery thermal management system    [-]
                .I_bat            (numpy.ndarray): currnet                              [Amperes]
                .cell_mass                (float): battery cell mass                    [kilograms]
                .Cp                       (float): battery cell specific heat capacity  [J/(K kg)] 
                .E_max                    (float): max energy                           [Joules]
                .E_current                (float): current energy                       [Joules]
                .Q_prior                  (float): charge throughput                    [Amp-hrs]
                .R_growth_factor          (float): internal resistance growth factor    [unitless]
                .E_growth_factor          (float): capactance (energy) growth factor    [unitless]  
                .inputs.I_bat            (current):                                     [amps]
                .inputs.P_bat              (power):                                     [Watts]
            state                           (dict): operating conditions                [-]
            bus                             (dict): data structure of electric bus      [-]
            battery_discharge_flag       (boolean): current flow flag                   [unitless] 
       
       Returns:
           None 
        
    """ 

    # Unpack varibles 
    battery            = battery  
    battery_conditions = state.conditions.energy[bus.tag][battery.tag]    
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

        V_ul[t_idx]           = compute_nmc_cell_state(battery_data,SOC[t_idx],T_cell[t_idx],I_cell[t_idx]) 

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

## @ingroup Library-Methods-Energy-Sources-Lithium_Ion_NMC
def compute_nmc_cell_state(battery_data,SOC,T,I):
    """This computes the electrical state variables of a lithium ion 
    battery cell with a  lithium-nickel-cobalt-aluminum oxide cathode 
    chemistry from look-up tables 
     
    Assumtions: 
       None
    
    Source:  
       None  
     
    Args:
        SOC           (numpy.ndarray): state of charge of cell     [unitless]
        battery_data           (dict): look-up data structure      [unitless]
        T             (numpy.ndarray): battery cell temperature    [Kelvin]
        I             (numpy.ndarray): battery cell current        [Amperes]
    
    Returns:  
        V_ul          (numpy.ndarray): under-load voltage          [Volts] 
        
    """  
    # Make sure things do not break by limiting current, temperature and current 
    SOC[SOC < 0.]   = 0.  
    SOC[SOC > 1.]   = 1.    
    DOD             = 1 - SOC 
    
    T[np.isnan(T)] = 302.65
    T[T<272.65]    = 272.65 # model does not fit for below 0  degrees
    T[T>322.65]    = 322.65 # model does not fit for above 50 degrees
     
    I[I<0.0]       = 0.0
    I[I>8.0]       = 8.0   
     
    pts            = np.hstack((np.hstack((I, T)),DOD  )) # amps, temp, SOC   
    V_ul           = np.atleast_2d(battery_data.Voltage(pts)[:,1]).T  
    
    return V_ul