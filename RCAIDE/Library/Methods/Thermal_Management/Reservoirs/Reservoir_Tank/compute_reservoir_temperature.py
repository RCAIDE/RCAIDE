# RCAIDE/Library/Methods/Thermal_Management/Reservoirs/Reservoir_Tank/compute_reservoir_temperature.py
#
#
# Created:  Apr 2024, S. Shekar 

# ----------------------------------------------------------------------------------------------------------------------
#  Compute heat loss to environment 
# ----------------------------------------------------------------------------------------------------------------------
def compute_reservoir_temperature(reservoir,state,coolant_line,delta_t,t_idx):
    """
     Computes the resultant temperature of the reservoir at each time step with coolant exchanging heat to the environment
          
          Inputs: 
                 reservoir          (Reservoir Data Structure)
                 coolant_line       (Coolant Line Data Structure)
                 delta_t
                 t_idx 
             
          Outputs:
                 reservoir.coolant.temperature
                 
          Assumptions: 
             N/A
        
          Source:
          None
    """  
    
    # Ambient Air Temperature 
    T_ambient                   = state.conditions.freestream.temperature[t_idx,0] 
    
    # properties of Reservoir
    A_surface                  = reservoir.surface_area
    volume                     = reservoir.volume
    T_current                  = state.conditions.energy.coolant_line[reservoir.tag].coolant_temperature[t_idx+1,0]
    thickness                  = reservoir.thickness
    conductivity               = reservoir.material.conductivity
    emissivity_res             = reservoir.material.emissivity
    
    #Coolant Properties
    coolant                    = reservoir.coolant 
    Cp                         = coolant.compute_cp(T_current)
    rho_coolant                = coolant.compute_density(T_current)

    # Heat Transfer properties
    conductivity               = reservoir.material.conductivity / 10
    sigma                       = 5.69e-8   #Stefan Boltzman Constant
    h                           = 1        #[W/m^2-k]
    emissivity_air              = 0.9
    

    # Heat Transfer due to conduction. 
    dQ_dt_cond                  = conductivity*A_surface*(T_current-T_ambient)/(thickness)

    # Heat Transfer dur to natural convention 
    dQ_dt_conv                  = h*A_surface*(T_current-T_ambient)

    # Heat Transfer due to radiation 
    dQ_dt_rad                   = sigma*A_surface*((emissivity_res*T_current**4)-(emissivity_air*T_ambient**4)) 

    dQ_dt                       = (dQ_dt_cond+dQ_dt_conv+dQ_dt_rad)
    
    # Compute mass of coolant present in the reservoir
    mass_coolant               = rho_coolant*volume
    
    # Compute the change in temperature due to the heat lost or gained from the environment
    dT_dt                       = dQ_dt/(mass_coolant*Cp)
    T_current                   = T_current - dT_dt*delta_t
    
    # Update the reservoir temperature
    state.conditions.energy[coolant_line.tag][reservoir.tag].coolant_temperature[t_idx+1,0] = T_current

    return