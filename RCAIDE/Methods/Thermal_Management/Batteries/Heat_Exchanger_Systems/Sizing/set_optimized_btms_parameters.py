## @ingroupMethods-Thermal_Management-Batteries-Sizing
# set_optimized_parameters.py 
#
# Created: Jun 2023, M. Clarke
from RCAIDE.Attributes.Coolants.Glycol_Water import Glycol_Water
from RCAIDE.Attributes.Gases import Air

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------   

## @ingroup Methods-Thermal_Management-Batteries-Sizing
def set_optimized_parameters(battery,optimization_problem):
    """  
    """       
    
    btms      = battery.thermal_management_system 
    
    # ------------------------------------------------------------------------------------------------------------------------
    # Unpack paramters  
    # ------------------------------------------------------------------------------------------------------------------------
    # modified paramters  
    L_h                      = optimization_problem
    L_c                      = optimization_problem
    p_h_1                    = optimization_problem
    p_c_1                    = optimization_problem
    PI_c                     = optimization_problem
    PI_h                     = optimization_problem
    d_H_c                    = optimization_problem
    gamma_chan_c             = optimization_problem
    m_dot_h                  = optimization_problem
    m_dot_c                  = optimization_problem
    C_R                      = optimization_problem

    # specified paramters (can part of the optimizer) 
    Q_dot                    = btms.heat_dissipation_to_ambient_from_heat_exchanger # assume power at cruise 
    T_h_1                    = btms.heat_exchanger.inlet_temperature_of_hot_fluid   # assume temp for ideal operation 
    T_c_1                    = btms.heat_exchanger.inlet_temperature_of_cold_fluid  # assume atmosphere temp

    # unmodified paramters  
    D_cell                   = battery.cell.diameter
    H_cell                   = battery.cell.height
    total_cells              = battery.pack_config.total
    number_of_modules        = battery.module_config.number_of_modules 
    a                        = btms.wavy_channel.cross_section.a
    b                        = btms.wavy_channel.cross_section.b
    c                        = btms.wavy_channel.cross_section.c
    d                        = btms.wavy_channel.cross_section.d 
    theta                    = btms.wavy_channel.contact_angle 
    density_chan             = btms.wavy_channel.density 
    single_side_contact      = btms.wavy_channel.single_side_contact
    channels_per_module      = btms.wavy_channel.number_of_channels_per_module  
    rho_hex                  = btms.heat_exchanger.density  
    t_w                      = btms.heat_exchanger.t_w
    t_f                      = btms.heat_exchanger.t_f
    k_f                      = btms.heat_exchanger.k_f
    k_w                      = btms.heat_exchanger.k_w      
    density_hex              = btms.heat_exchanger.density    
    pump_efficiency          = btms.pump_efficiency
    fab_efficiency           = btms.fab_efficiency    

    # ------------------------------------------------------------------------------------------------------------------------    
    # compute properties of working fluids 
    # ------------------------------------------------------------------------------------------------------------------------  
    # glycol 
    Coolant_h           = Glycol_Water()
    rho_h               = Coolant_h.density
    mu_h                = Coolant_h.dynamic_viscosity  
    c_p_h_1             = Coolant_h.specific_heat_capacity
    Pr_h                = Coolant_h.compute_prandtl_number(T_h_1) 

    # air 
    Coolant_c           = Air()
    rho_c               = Coolant_c.density
    mu_c                = Coolant_c.dynamic_viscosity  
    c_p_c_1             = Coolant_c.specific_heat_capacity
    Pr_c                = Coolant_c.compute_prandtl_number(T_c_1) 

    # ------------------------------------------------------------------------------------------------------------------------     
    # compute wavy channel and heat exchanger geometry 
    # ------------------------------------------------------------------------------------------------------------------------  
    # contact area/length of a single battery cell
    if single_side_contact: 
        A_surf              = theta / 360 * np.pi * D_cell * H_cell                  
        L_surf              = theta / 360 * np.pi * (D_cell + b + d / 2) 
        L_chan              = total_cells * L_surf + 4 * D_cell 
    else :
        A_surf          = 2* theta / 360 * np.pi * D_cell * H_cell
        L_surf          = 2* theta / 360 * np.pi * D_cell * H_cell 
        L_chan          = 2* total_cells * L_surf + 4 * D_cell  

    # line density of the wavy channel 
    rho_line            = density_chan * (2 * a * (2 * b + d) + 2 * b * c)+ rho_h * c * d                 # eqn 19   
    d_H_h               = 2 * (c * d) / (c + d)
    gamma_chan_h        = d / c   
    area_chan_h         = c * d

    # calculate coolant velocity
    number_of_channels  = number_of_modules * channels_per_module
    m_dot_h_unit        = m_dot_h / number_of_channels
    u_h                 = m_dot_h_unit / (rho_h * area_chan_h)  

    # fin height
    b_f_h               = d_H_h * (1 + gamma_chan_h) / 2  # eqn 20
    b_f_c               = d_H_c * (1 + gamma_chan_c) / 2

    # finned area by overall area
    A_f_div_A_h         = gamma_chan_h / (gamma_chan_h + 1) # eqn 21 
    A_f_div_A_c         = gamma_chan_c / (gamma_chan_c + 1)

    # ------------------------------------------------------------------------------------------------------------------------  
    # Thermodynamic calculations with desired heat tranfer rate, and pressure ratios, and inlet pressures
    # ------------------------------------------------------------------------------------------------------------------------  
    C_h                = m_dot_h*c_p_h_1 
    C_c                = C_h/C_R  
    c_p_c_1            = C_c/m_dot_c
    T_h_2              = -Q_dot/C_h  + T_h_1
    T_c_2              =  Q_dot/C_c  + T_c_1   
    delta_p_h          = (1-PI_h)*p_h_1      
    delta_p_c          = (1-PI_c)*p_c_1  
    p_h_2              = p_h_1 - delta_p_h 
    p_c_2              = p_c_1 - delta_p_c 
    c_p_h_2            = Coolant_h.compute_cp(T_h_2,p_h_2)
    c_p_c_2            = Coolant_c.compute_cp(T_c_2,p_c_2)
    c_p_c              = (c_p_c_1 + c_p_c_2) / 2
    c_p_h              = (c_p_h_1 + c_p_h_2) / 2

    # ------------------------------------------------------------------------------------------------------------------------  
    #  STEP 2 : finding NTU  
    # ------------------------------------------------------------------------------------------------------------------------  
    sol                = minimize(solve_for_NTU, [1] , args=(Q_dot,C_h,T_h_1,T_c_1,C_R), method='SLSQP', bounds=[0,20], tol=1e-6)  # Eqn 28 and 29   
    NTU                = sol.x    

    A_0_h              = d_H_h * A_h / (4 * L_h)
    A_0_c              = d_H_c * A_c / (4 * L_c)
    G_h                = m_dot_h / A_0_h
    G_c                = m_dot_c / A_0_c  
    Re_h               = G_h*d_H_h/mu_h # Eqn 31 
    Re_c               = G_c*d_H_c/mu_c # Eqn 31 

    if Re_h < 2300:   
        f_h           = 14.227 / Re_h
        Nu_h          = 3.608 
    else:    
        f_h           = 0.0791 *  Re_h**(-0.25) * (1.0875 - 0.1125 * gamma_chan_h) 
        Nu_h          = (f_h/ 2) * (Re_h - 1000) * Pr_h / (1 + 12.7 *  (f_h/ 2)**(0.5) * ( Pr_h**(2 / 3) - 1))

    if Re_c < 2300:   
        f_c           = (24/Re_c)*(1 - 1.3553*gamma_chan_c + 1.9467*gamma_chan_c**2 - 1.7012*gamma_chan_c**3 + 0.9646*gamma_chan_c**4 - 0.2437*gamma_chan_c**5)
        Nu_c          = 8.235*(1 - 2.0421*gamma_chan_h  + 3.0853*gamma_chan_h**2 - 2.4765*gamma_chan_h**3 + 1.0578*gamma_chan_h**4 - 0.1861*gamma_chan_h **5)
    else:     
        f_c           = (0.0791*Re_c**(-0.25))*(1.0887 - 1.1125*gamma_chan_c)
        Nu_c          = ((f_c/2)*Re_c - 1000*Pr_c)/(1 + 12.7*((f_c/2)**(0.5))*(Pr_c**(2/3) - 1)) 

    j_h               =  (Nu_h * Pr_h**(-1/3))/ Re_h
    j_c               =  (Nu_c * Pr_c**(-1/3))/ Re_c   

    # convective heat transfer coefficent Eqn 34 
    h_h               = j_h * G_h * c_p_h /(Pr_h**(2/3))
    h_c               = j_c * G_c * c_p_c /(Pr_c**(2/3))

    m_f_h             = np.sqrt(2 * h_h / k_f / t_f)
    m_f_c             = np.sqrt(2 * h_c / k_f / t_f)

    l_f_h             = b_f_h / 2 - t_f
    l_f_c             = b_f_c / 2 - t_f

    eta_f_h           = np.tanh(m_f_h * l_f_h) / (m_f_h * l_f_h)  # eqn 35  
    eta_f_c           = np.tanh(m_f_c * l_f_c) / (m_f_c * l_f_c)

    # overall fin efficiency
    eta_0_h           = 1 - (1 - eta_f_h) * A_f_div_A_h
    eta_0_c           = 1 - (1 - eta_f_c) * A_f_div_A_c # eqn 36  

    if Re_c < 2300: 
        f_c           = (24/Re_c)*(1 - 1.3553*gamma_chan_c + 1.9467*gamma_chan_c**2 - 1.7012*gamma_chan_c**3 + 0.9646*gamma_chan_c**4 - 0.2437*gamma_chan_c**5)
    else:    
        f_c           = (0.0791*Re_c**(-0.25))*(1.0887 - 1.1125*gamma_chan_c) 

    # area density
    beta_h            = 4 * (1 + gamma_chan_h) / (d_H_h * (1 + gamma_chan_h) + 2 * gamma_chan_h * t_f) # Eqn 22
    beta_c            = 4 * (1 + gamma_chan_c) / (d_H_c * (1 + gamma_chan_c) + 2 * gamma_chan_c * t_f) 

    alpha_h           = (b_f_h*beta_h)/(b_f_c + b_f_h + 2*t_w)
    alpha_c           = (b_f_c*beta_c)/(b_f_c + b_f_h + 2*t_w)

    # the ratio of minimum free-flow area to the frontal area
    sigma_h           = alpha_h*d_H_h/ 4
    sigma_c           = alpha_c*d_H_h/ 4

    U_h               = 1/( (1/(eta_0_h*h_h) ) + ((alpha_c/alpha_h)/(eta_0_c*h_c))) # eqn 37
    A_h               = NTU * (C_h/U_h)       # eqn 38 a 
    A_c               = A_h*(alpha_c/alpha_h) # eqn 38 b    

    A_fr_h            = A_0_h/sigma_h # eqn 40
    A_fr_c            = A_0_c/sigma_c  
    H                 = A_fr_c /L_h 

    Ke_c, Kc_c        = compute_heat_exhanger_factors(btms.kc_values,btms.kc_values,sigma_c, Re_c)

    rho_c_1           = Coolant_c.compute_density(T_c_1,p_c_1)
    rho_c_2           = Coolant_c.compute_density(T_c_2,p_c_2)

    delta_p_h_new     = 2*f_h*(rho_h*(u_h**2))*(L_chan/d_H_h)
    rho_c_m           = 2/(1/rho_c_1 + 1/rho_c_2)
    delta_p_c_new     = (G_h**2 / (2 * rho_c_1)) * ((1 - sigma_c**2 + Kc_c)  + 2 * (rho_c_1 / rho_c_2 - 1) + f_c * 4 * L_c / d_H_c * rho_c_1 / rho_c_m  - (1 - sigma_c**2 - Ke_c) * rho_c_1 / rho_c_2)  #eqn 43 


    # ------------------------------------------------------------------------------------------------------------------------  
    #  System-level calculations
    # ------------------------------------------------------------------------------------------------------------------------  
    # masses 
    m_chan              = rho_line * L_chan  
    m_hex               = density_hex * L_h * A_fr_h * (1 - sigma_h - sigma_c) + rho_h * A_0_h * L_h

    # power 
    P_chan              = m_dot_h * delta_p_h  / ( rho_h * pump_efficiency) 
    u_c                 = m_dot_c/(rho_c*A_c)  
    P_hex               = m_dot_h * (delta_p_h / rho_h) / pump_efficiency  +  (m_dot_c*(delta_p_c/rho_c) +  (u_c**2)*0.5)/fab_efficiency

    # number of passes 
    N_p                 =  (H - b_f_c - 2 * t_w) / (b_f_h + b_f_c + 2 * t_w)


    # ---------------------------------------------------------------------------------
    # Pack outputs
    # ---------------------------------------------------------------------------------
    btms.wavy_channel.Reynolds_number_of_coolant_in_chan                       = btms.wavy_channel.Reynolds_number_of_coolant_in_chan                       
    btms.wavy_channel.velocity_of_coolant_in_chan                              = btms.wavy_channel.velocity_of_coolant_in_chan                              
    btms.wavy_channel.contact_area_of_chan_with_batteries                      = btms.wavy_channel.contact_area_of_chan_with_batteries                      
    btms.wavy_channel.hydraulic_diameter_of_chan                               = btms.wavy_channel.hydraulic_diameter_of_chan                               
    btms.wavy_channel.aspect_ratio_of_chan                                     = btms.wavy_channel.aspect_ratio_of_chan                                     
    btms.wavy_channel.mass_flow_rate_of_one_module                             = btms.wavy_channel.mass_flow_rate_of_one_module                             
    btms.wavy_channel.contact_area_of_one_module                               = btms.wavy_channel.contact_area_of_one_module      
    btms.wavy_channel.mass_of_chan                                             = btms.wavy_channel.mass_of_chan                                             
    btms.wavy_channel.power_of_chan                                            = btms.wavy_channel.power_of_chan         
    btms.heat_exchanger.fin_height_of_hot_fluid                                = btms.heat_exchanger.fin_height_of_hot_fluid                                
    btms.heat_exchanger.fin_height_of_cold_fluid                               = btms.heat_exchanger.fin_height_of_cold_fluid                               
    btms.heat_exchanger.finned_area_by_overall_area_at_hot_fluid               = btms.heat_exchanger.finned_area_by_overall_area_at_hot_fluid               
    btms.heat_exchanger.finned_area_by_overall_area_at_cold_fluid              = btms.heat_exchanger.finned_area_by_overall_area_at_cold_fluid              
    btms.heat_exchanger.area_density_of_hot_fluid                              = btms.heat_exchanger.area_density_of_hot_fluid                              
    btms.heat_exchanger.area_density_of_cold_fluid                             = btms.heat_exchanger.area_density_of_cold_fluid                             
    btms.heat_exchanger.number_of_plates                                       = btms.heat_exchanger.number_of_plates                                       
    btms.heat_exchanger.frontal_area_of_hot_fluid                              = btms.heat_exchanger.frontal_area_of_hot_fluid                              
    btms.heat_exchanger.frontal_area_of_cold_fluid                             = btms.heat_exchanger.frontal_area_of_cold_fluid                             
    btms.heat_exchanger.heat_transfer_area_of_hot_fluid                        = btms.heat_exchanger.heat_transfer_area_of_hot_fluid                        
    btms.heat_exchanger.heat_transfer_area_of_cold_fluid                       = btms.heat_exchanger.heat_transfer_area_of_cold_fluid                       
    btms.heat_exchanger.minimum_free_flow_area_of_hot_fluid                    = btms.heat_exchanger.minimum_free_flow_area_of_hot_fluid                    
    btms.heat_exchanger.minimum_free_flow_area_of_cold_fluid                   = btms.heat_exchanger.minimum_free_flow_area_of_cold_fluid                   
    btms.heat_exchanger.ratio_of_free_flow_area_to_frontal_area_of_hot_fluid   = btms.heat_exchanger.ratio_of_free_flow_area_to_frontal_area_of_hot_fluid   
    btms.heat_exchanger.ratio_of_free_flow_area_to_frontal_area_of_cold_fluid  = btms.heat_exchanger.ratio_of_free_flow_area_to_frontal_area_of_cold_fluid   
    btms.heat_exchanger.mass_properties.mass                                   = btms.heat_exchanger.mass_properties.mass                                   
    btms.heat_exchanger.power_of_hex_fraction_of_hot_fluid                     = btms.heat_exchanger.power_of_hex_fraction_of_hot_fluid           
  
    return battery