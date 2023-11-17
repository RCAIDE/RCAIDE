## @ingroup Methods-Thermal_Management-Batteries-Sizing
#
# Created: Jun 2023, M. Clarke

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------  
# RCAIDE Imports  
from RCAIDE.Analyses.Process   import Process 

# Python package imports  
import numpy as np  

## @ingroup Methods-Thermal_Management-Batteries-Sizing 
def wavy_channel_sizing_setup(): 
    
    # size the base config
    procedure = Process()
    
    # modify battery thermal management system
    procedure.modify_hrs = modify_wavy_channel_hrs

    # post process the results
    procedure.post_process = post_process
        
    return procedure
 

def modify_wavy_channel_hrs(nexus): 
    """ 
    """ 
    battery       = nexus.hrs_configurations.optimized.networks.all_electric.busses.bus.batteries.lithium_ion_nmc
    
    hrs_opt       = battery.thermal_management_system.heat_removal_system
    
    # ------------------------------------------------------------------------------------------------------------------------
    # Unpack paramters  
    # ------------------------------------------------------------------------------------------------------------------------
     # Mass flow rate  
     
    m_coolant = hrs_opt.coolant_flow_rate         
    b         = hrs_opt.channel_side_thickness                
    d         = hrs_opt.channel_width                         
    theta     = hrs_opt.channel_contact_angle    
    c         = battery.cell.height 
    a         = hrs_opt.channel_top_thickness 
    T_bat     = hrs_opt.design_battery_operating_temperature

    # Battery 
    d_cell    = battery.cell.diameter                    
    h_cell    = battery.cell.height                      
    A_cell    = np.pi*d_cell*h_cell                      
    N_battery = battery.pack.electrical_configuration.total 

    coolant  = hrs_opt.coolant
    AR       = d/c    
    T_i      = hrs_opt.coolant_inlet_temperature 
    n_pump   = 0.7

    # Channel Properties 
    channel_density = hrs_opt.channel_density

    # Surface area of the channel 
    A_chan = N_battery*theta*A_cell/360   
 
    #Length of Channel 
    k_chan   = hrs_opt.channel_thermal_conductivity                   # Conductivity of the Channel (Replace with function)    
    L_extra  = 4*d_cell             # Assumption made by Zhao et al. 
    L_chan   = N_battery*theta*np.pi*(d_cell+b+0.5*d)+L_extra

    # Hydraulic diameter    
    dh   = (4*c*d)/(2*(c+d))   

    # Thermophysical Properties of Coolant 
    rho  = coolant.density
    mu   = coolant.compute_absolute_viscosity(T_i)  
    cp   = coolant.compute_cp(T_i)
    Pr   = coolant.compute_prandtl_number(T_i) 
    k    = coolant.compute_thermal_conductivity(T_i)   

    # COMPUTE POWER  Q_convec  

    #calculate the velocity of the fluid in the channel 
    v=rho*c*d*m_coolant

    # calculate the Reynolds Number 
    Re=(rho*dh*v)/mu

    # fanning friction factor (eq 32)
    if Re< 2300:
        f= 24*(1-(1.3553*AR)+(1.9467*AR**2)-(1.7012*AR**3)+(0.9564*AR**4)-(0.2537*AR**5))
    elif Re>=2300:
        f= (0.0791*(Re**(-0.25)))*(1.8075-0.1125*AR)

    # Calculate the pressure drop in the channel 
    dp     = 2*f*rho*v*v*L_chan/dh

    # Calculate the Power consumed
    Power   = m_coolant*dp/(n_pump*rho)

    # Mass calculations - Channel  
    rho_line        = channel_density*(2*a*((2*b)+d)+(2*b*c))
    mass_channel    = rho_line*L_chan

    # Mass calculations - Liquid 
    mass_liquid  = rho*c*d 
    total_mass   = mass_channel+mass_liquid 

    #calculate the velocity of the fluid in the channel 
    v=rho*c*d*m_coolant

    # calculate the Reynolds Number 
    Re=(rho*dh*v)/mu

    # fanning friction factor (eq 32)
    if Re< 2300:
        f= 24*(1-(1.3553*AR)+(1.9467*AR**2)-(1.7012*AR**3)+(0.9564*AR**4)-(0.2537*AR**5))
    elif Re>=2300:
        f= (0.0791*(Re**(-0.25)))*(1.8075-0.1125*AR)

    # Nusselt Number (eq 12)   
    if Re< 2300:
        Nu= 8.235*(1-(2.0421*AR)+(3.0853*AR**2)-(2.4765*AR**3)+(1.0578*AR**4)-(0.1861*AR**5))    
    elif Re >= 2300:
        Nu = ((f/2)*(Re-1000)*Pr)/(1+(12.7*(f**0.5)*(Pr**(2/3)-1)))   

    # heat transfer coefficient of the channeled coolant (eq 11)
    h = k*Nu/dh

    # Overall Heat Transfer Coefficient from battery surface to the coolant fluid (eq 10)
    U_total = 1/((1/h)+(b/k_chan))

    # Calculate NTU
    NTU = U_total*A_chan/(m_coolant*cp)

    # Calculate Outlet Temparture To ( eq 8)
    T_o = ((T_bat-T_i)*(1-np.exp(-NTU)))+T_i

    # Calculate the Log mean temperature 
    T_lm = ((T_bat-T_i)-(T_bat-T_o))/(np.log((T_bat-T_i)/(T_bat-T_o)))

    # Calculated Heat Convected 
    Q_conv = U_total*A_chan*T_lm   
    
    hrs_opt.mass_properties.mass       = total_mass
    hrs_opt.design_power_draw          = Power
    hrs_opt.design_heat_removed        = Q_conv 
    hrs_opt.coolant_outlet_temperature = T_o
    hrs_opt.coolant_pressure_ratio     = dp
    
    return nexus     
# ----------------------------------------------------------------------
#   Post Process Results to give back to the optimizer
# ----------------------------------------------------------------------   
def post_process(nexus): 
    summary           = nexus.summary  
    battery           = nexus.hrs_configurations.optimized.networks.all_electric.busses.bus.batteries.lithium_ion_nmc      
    Cp_batery         = battery.cell.specific_heat_capacity 
    mass_battery      = battery.cell.mass    
    N_battery_series  = battery.pack.electrical_configuration.series 
    N_battery_parllel = battery.pack.electrical_configuration.parallel  
    hrs_opt           = battery.thermal_management_system.heat_removal_system
    Q_conv            = hrs_opt.design_heat_removed
    Q_gen             = hrs_opt.design_heat_generated                    
    
    # calculate objective 
    total_mass        = hrs_opt.mass_properties.mass
    Power             = hrs_opt.design_power_draw
    summary.mass_power_objective =  (Power**2 + total_mass**2)**(0.5)  
    
    # calculate heat constraint  
    summary.heat_energy_constraint  = abs(Q_gen - Q_conv)      
     
    # calculate temperature constraint  
    Q_net                         = Q_gen - Q_conv  
    summary.temperature_constraint= Q_net/(Cp_batery*mass_battery*N_battery_parllel*N_battery_series)     
 
    return nexus     