# RRCAIDE/Library/Methods/Thermal_Management/Reservoirs/Reservoir_Tank/compute_mixing_temperature.py


# Created:  Apr 2024, S. Shekar 

# ---------------------------------------------------------------------------------------------------------------------- 
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
import  RCAIDE

# ----------------------------------------------------------------------------------------------------------------------
#  Compute resultant temperature of the reservoir
# ----------------------------------------------------------------------------------------------------------------------
def compute_mixing_temperature(reservoir,state,coolant_line,delta_t,t_idx):
    
    """
     Computes the resultant temperature of the reservoir at each time step with coolant pouring in from the HAS and the HEX 
          
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
    
    # Current Reservoir temperature
    T_current                = state.conditions.energy.coolant_line[reservoir.tag].coolant_temperature[t_idx,0]
    
    # Reservior Properties
    coolant                  = reservoir.coolant 
    rho_coolant              = coolant.compute_density(T_current)
    Cp_RES                   = coolant.compute_cp(T_current)    
    volume                   = reservoir.volume
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
                mass_flow_HAS.append(state.conditions.energy[coolant_line.tag][HAS.tag].coolant_mass_flow_rate[t_idx+1] * delta_t)
                T_outlet_HAS .append(state.conditions.energy[coolant_line.tag][HAS.tag].outlet_coolant_temperature[t_idx+1])
                Cp_HAS.append( coolant.compute_cp(T_outlet_HAS))  
            else:
                pass
    
    for HEX in  coolant_line.heat_exchangers:
        mass_flow_HEX.append(state.conditions.energy[coolant_line.tag][HEX.tag].coolant_mass_flow_rate[t_idx+1] * delta_t)
        T_outlet_HEX .append(state.conditions.energy[coolant_line.tag][HEX.tag].outlet_coolant_temperature[t_idx+1])
        Cp_HEX.append( coolant.compute_cp(T_outlet_HEX))
            
    # Summing over HAS elements to find the total heat being added to the reservoir
    flux_HAS = sum(m * Cp * T for m, Cp, T in zip(mass_flow_HAS, Cp_HAS, T_outlet_HAS))
    
    # Summing over HEX elements to find the total heat being removed to the reservoir
    flux_HEX = sum(m * Cp * T for m, Cp, T in zip(mass_flow_HEX, Cp_HEX, T_outlet_HEX))
    
    # Computes the total mass that left the reservoir in a time step
    mass_total = sum (m_has+m_hex for m_has, m_hex in zip(mass_flow_HAS, mass_flow_HEX))
    
    # Computes the remaining mass in the reservoir
    mass_RES                = mass_coolant-mass_total
        
    # Computes the temperature in the reservoir after mixing from HAS and HEX
    T_final                 = (flux_HAS+flux_HEX+mass_RES*Cp_RES*T_current)/(mass_coolant*Cp_RES)

    state.conditions.energy[coolant_line.tag][reservoir.tag].coolant_temperature[t_idx+1,0] = T_final
    
    return 