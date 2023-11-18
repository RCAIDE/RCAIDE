## @ingroup Methods-Thermal_Management-Batteries-Sizing
#
# Created: Jun 2023, M. Clarke

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------  
# RCAIDE Imports  
from RCAIDE.Analyses.Process   import Process 
from RCAIDE.Core import Units

# Python package imports  
import numpy as np  

## @ingroup Methods-Thermal_Management-Batteries-Sizing 
def wavy_channel_sizing_setup(): 
    
    # size the base config
    procedure = Process()
    
    # modify battery thermal management system
    procedure.modify_HAS = modify_wavy_channel_HAS

    # post process the results
    procedure.post_process = post_process
        
    return procedure
 

def modify_wavy_channel_HAS(nexus): 
    """ 
    """ 
    battery       = nexus.hrs_configurations.optimized.networks.all_electric.busses.bus.batteries.lithium_ion_nmc 
    has_opt       = battery.thermal_management_system.heat_aquisition_system
    
    # ------------------------------------------------------------------------------------------------------------------------
    # Unpack paramters  
    # ------------------------------------------------------------------------------------------------------------------------
     # Mass flow rate 
    m_coolant = has_opt.coolant_flow_rate         
    b         = has_opt.channel_side_thickness                
    d         = has_opt.channel_width                         
    theta     = has_opt.channel_contact_angle    
    c         = battery.cell.height 
    a         = has_opt.channel_top_thickness 
    T_bat     = has_opt.design_battery_operating_temperature
    Q_pack    = has_opt.design_heat_removed 
    N_mod     = battery.pack.number_of_modules
    Q_module  = Q_pack/N_mod 
    
    # Battery 
    d_cell    = battery.cell.diameter                    
    h_cell    = battery.cell.height                      
    A_cell    = np.pi*d_cell*h_cell       
    
    if has_opt.single_side_contact:
        contact_factor  = 1
        N_cells         = battery.module.geometrtic_configuration.parallel_count*2 
        N_lines_per_mod = battery.module.geometrtic_configuration.normal_count/2
        Q_line          = Q_module/N_lines_per_mod 
        m_coolant_line  = m_coolant/(N_mod*N_lines_per_mod )
    else:
        contact_factor = 2
        N_cells        = battery.module.geometrtic_configuration.parallel_count
        N_lines_per_mod = battery.module.geometrtic_configuration.normal_count
        Q_line         = Q_module/N_lines_per_mod
        m_coolant_line = m_coolant/(N_mod*N_lines_per_mod)
    
    channel  = has_opt.channel
    coolant  = has_opt.coolant
    AR       = d/c    
    T_i      = has_opt.coolant_inlet_temperature 
    n_pump   = 0.7

    # Channel Properties 
    channel_density = channel.density

    # Surface area of the channel 
    A_chan = contact_factor*N_cells*(theta/(2*np.pi))*A_cell 
 
    #Length of Channel 
    k_chan   = channel.thermal_conductivity  # Conductivity of the Channel (Replace with function)    
    L_extra  = 4*d_cell             # Assumption made by Zhao et al. 
    L_chan   = N_cells*(theta/2)*(d_cell+b+0.5*d)+L_extra

    # Hydraulic diameter    
    dh   = (4*c*d)/(2*(c+d))   

    # Thermophysical Properties of Coolant 
    rho  = coolant.density
    mu   = coolant.compute_absolute_viscosity(T_i)  
    cp   = coolant.compute_cp(T_i)
    Pr   = coolant.compute_prandtl_number(T_i) 
    k    = coolant.compute_thermal_conductivity(T_i)   

    #calculate the velocity of the fluid in the channel 
    v=rho*c*d*m_coolant_line

    # calculate the Reynolds Number 
    Re=(rho*dh*v)/mu

    # fanning friction factor (eq 32),  Nusselt Number (eq 12)   
    if Re< 2300:
        f= 24*(1-(1.3553*AR)+(1.9467*(AR**2))-(1.7012*(AR**3))+(0.9564*(AR**4))-(0.2537*(AR**5)))/Re
        Nu = 8.235*(1-(2.0421*AR)+(3.0853*(AR**2))-(2.4765*(AR**3))+(1.0578*(AR**4))-(0.1861*(AR**5)))   
    elif Re>=2300:
        f= (0.0791*(Re**(-0.25)))*(1.8075-0.1125*AR)
        Nu = ((f/2)*(Re-1000)*Pr)/(1+(12.7*((f/2)**0.5)*(Pr**(2/3)-1)))   
 
    # Calculate the pressure drop in the channel 
    dp     = 2*f*rho*v*v*L_chan/dh

    # Calculate the Power consumed
    Power   = m_coolant_line*dp/(n_pump*rho)

    # Mass calculations - Channel  
    rho_line        = channel_density*(2*a*((2*b)+d)+(2*b*c))
    mass_channel    = rho_line*L_chan

    # Mass calculations - Liquid 
    mass_liquid  = rho*c*d 
    total_mass   = mass_channel+mass_liquid 
 
    # heat transfer coefficient of the channeled coolant (eq 11)
    h = k*Nu/dh

    # Overall Heat Transfer Coefficient from battery surface to the coolant fluid (eq 10)
    U_total = 1/((1/h)+(b/k_chan))

    # Calculate NTU
    NTU = U_total*A_chan/(m_coolant_line*cp)

    # Calculate Outlet Temparture To ( eq 8)
    T_o = ((T_bat-T_i)*(1-np.exp(-NTU)))+T_i

    # Calculate the Log mean temperature 
    T_lm = ((T_bat-T_i)-(T_bat-T_o))/(np.log((T_bat-T_i)/(T_bat-T_o)))

    # Calculated Heat Convected 
    Q = U_total*A_chan*T_lm   
    
    # line level properties for optmization 
    has_opt.mass_properties.mass       = total_mass*N_mod*N_lines_per_mod
    has_opt.design_power_draw          = Power*N_mod*N_lines_per_mod
    has_opt.heat_removed               = Q 
    has_opt.heat_generated             = Q_line 
    has_opt.coolant_outlet_temperature = T_o
    has_opt.coolant_pressure_drop      = dp  
    
    return nexus     
# ----------------------------------------------------------------------
#   Post Process Results to give back to the optimizer
# ----------------------------------------------------------------------   
def post_process(nexus): 
    summary           = nexus.summary  
    battery           = nexus.hrs_configurations.optimized.networks.all_electric.busses.bus.batteries.lithium_ion_nmc       
    has_opt           = battery.thermal_management_system.heat_aquisition_system 
    Q_line_rem        = has_opt.heat_removed
    Q_line_gen        = has_opt.heat_generated          
    
    # calculate objective 
    total_mass        = has_opt.mass_properties.mass/100
    Power             = has_opt.design_power_draw
    summary.mass_power_objective =  (Power**2 + total_mass**2)**(0.5)  
    
    # calculate heat constraint  
    summary.heat_energy_constraint  = abs(Q_line_gen  -  Q_line_rem)      
 
    return nexus     