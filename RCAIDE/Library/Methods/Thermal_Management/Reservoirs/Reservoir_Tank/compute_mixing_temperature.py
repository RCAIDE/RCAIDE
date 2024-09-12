## @ingroup Library-Energy-Methods-Thermal_Management-Common
# RCAIDE/Library/Methods/Energy/Thermal_Management/Common/Reservoir/No_Reservoir/compute_mixing_temperature.py


# Created:  Apr 2024, S. Shekar 


import  RCAIDE

# ----------------------------------------------------------------------------------------------------------------------
#  Compute resultant temperature of the reservoir
# ----------------------------------------------------------------------------------------------------------------------
def compute_mixing_temperature(RES,state,coolant_line,dt,i):
    
    """
     Computes the resultant temperature of the reservoir at each time step with coolant pouring in from the HAS and the HEX 
          
          Inputs: 
                 HAS
                 HEX
                 battery_conditions
                 dt
                 i 
             
          Outputs:
                 RES.coolant.temperature
                 
          Assumptions: 
             N/A
        
          Source:

    
    """    
    
    # Current Reservoir temperature
    T_current                = state.conditions.energy.coolant_Line[RES.tag].coolant_temperature[i,0]
    
    # Reservior Properties
    coolant                  = RES.coolant 
    rho_coolant              = coolant.compute_density(T_current)
    Cp_RES                   = coolant.compute_cp(T_current)    
    volume                   = RES.volume
    mass_coolant             = rho_coolant*volume
    
    mass_flow_HAS  = []
    T_outlet_HAS   = []
    Cp_HAS         = []
    mass_flow_HEX  = []
    T_outlet_HEX   = []
    Cp_HEX         = []    
    
    for battery in  coolant_line.batteries:
        for HAS in battery:
            if isinstance(HAS, RCAIDE.Library.Components.Thermal_Management.Batteries.Liquid_Cooled_Wavy_Channel):
                mass_flow_HAS.append(state.conditions.energy[coolant_line.tag][HAS.tag].coolant_mass_flow_rate[i+1] * dt)
                T_outlet_HAS .append(state.conditions.energy[coolant_line.tag][HAS.tag].outlet_coolant_temperature[i+1])
                Cp_HAS.append( coolant.compute_cp(T_outlet_HAS))  
            else:
                pass
    
    for HEX in  coolant_line.heat_exchangers:
        #if isinstance(HEX, RCAIDE.Library.Components.Thermal_Management.Heat_Exchangers):
        mass_flow_HEX.append(state.conditions.energy[coolant_line.tag][HEX.tag].coolant_mass_flow_rate[i+1] * dt)
        T_outlet_HEX .append(state.conditions.energy[coolant_line.tag][HEX.tag].outlet_coolant_temperature[i+1])
        Cp_HEX.append( coolant.compute_cp(T_outlet_HEX))
            
    # Summing over HAS elements
    flux_HAS = sum(m * Cp * T for m, Cp, T in zip(mass_flow_HAS, Cp_HAS, T_outlet_HAS))
    
    # Summing over HEX elements
    flux_HEX = sum(m * Cp * T for m, Cp, T in zip(mass_flow_HEX, Cp_HEX, T_outlet_HEX))

    mass_total = sum (m_has+m_hex for m_has, m_hex in zip(mass_flow_HAS, mass_flow_HEX))
    mass_RES                = mass_coolant-mass_total
        
    T_final                 = (flux_HAS+flux_HEX+mass_RES*Cp_RES*T_current)/(mass_coolant*Cp_RES)

    state.conditions.energy[coolant_line.tag][RES.tag].coolant_temperature[i+1,0] = T_final
    
    return 
