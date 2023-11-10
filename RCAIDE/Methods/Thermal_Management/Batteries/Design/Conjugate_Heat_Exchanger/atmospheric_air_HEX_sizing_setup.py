## @ingroup Methods-Thermal_Management-Batteries-Sizing
#
# Created: Jun 2023, M. Clarke

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------  
# RCAIDE Imports 
import RCAIDE 
from RCAIDE.Core                                                  import Units   
from RCAIDE.Analyses.Process                                      import Process     
from RCAIDE.Methods.Thermal_Management.Batteries.Performance.Conjugate_Heat_Exchanger.compute_heat_exhanger_factors import compute_heat_exhanger_factors
from RCAIDE.Attributes.Coolants.Glycol_Water import Glycol_Water
from RCAIDE.Attributes.Gases import Air

# Python package imports 
from scipy.optimize import minimize  
import numpy as np 
import scipy as sp  

## @ingroup Methods-Thermal_Management-Batteries-Sizing 
def atmospheric_air_HEX_sizing_setup(): 
    
    # size the base config
    procedure = Process()
    
    # modify battery thermal management system
    procedure.modify_hex = modify_channel_cooling_hex

    # post process the results
    procedure.post_process = post_process
        
    return procedure
 

def modify_channel_cooling_hex(nexus): 
    """ 
    """     
    hex_opt       = nexus.hex_configurations.optimized.networks.all_electric.busses.bus.batteries.lithium_ion_nmc.thermal_management_system.heat_exchanger
  
    # ------------------------------------------------------------------------------------------------------------------------
    # Unpack paramters  
    # ------------------------------------------------------------------------------------------------------------------------
  
    # fixed paramters   
    rho_hex          = hex_opt.density  
    t_w              = hex_opt.t_w
    t_f              = hex_opt.t_f
    k_f              = hex_opt.k_f
    k_w              = hex_opt.k_w      
    density_hex      = hex_opt.density    
    pump_efficiency  = hex_opt.pump_efficiency
    fan_efficiency   = hex_opt.fan_efficiency  
    
    # fixed operating paramters 
    Q                = hex_opt.heat_removed_from_system  
    air              = hex_opt.air
    coolant          = hex_opt.coolant
    T_h_1            = hex_opt.coolant_temperature_of_hot_fluid                   
    T_c_1            = hex_opt.inlet_temperature_of_cold_fluid   
    m_dot_h          = hex_opt.mass_flow_rate_of_hot_fluid  
    p_h_1            = hex_opt.coolant_inlet_pressure   
    
    # optimizer parameters  
    p_c_1            = hex_opt.inlet_pressure_of_cold_fluid  
    PI_h_guess       = hex_opt.coolant_pressure_ratio   
    C_R              = hex_opt.heat_capacity_ratio  
    d_H_h            = hex_opt.coolant_hydraulic_diameter
    d_H_c            = hex_opt.air_hydraulic_diameter
    AR_h             = hex_opt.coolant_channel_aspect_ratio
    AR_c             = hex_opt.air_channel_aspect_ratio

    # ------------------------------------------------------------------------------------------------------------------------      
    # computed parameters  
    # ------------------------------------------------------------------------------------------------------------------------  
    c_p_h_1          = coolant.compute_cp(T_h_1,p_h_1)  
    PI_c_guess       = hex_opt.air_pressure_ratio  
    delta_p_h_true   = (1- PI_h_guess)*p_h_1
    eta_0_c_guess    = 0 # Sai, I am not sure if these can be put in the optimizer since they are also computed below 
    eta_0_h_guess    = 0 # Sai, I am not sure if these can be put in the optimizer since they are also computed below 
    j_div_f_c_guess  = 0 # Sai, I am not sure if these can be put in the optimizer since they are also computed below 
    j_div_f_h_guess  = 0 # Sai, I am not sure if these can be put in the optimizer since they are also computed below 
    b_f_h            = 0 # Sai, I am not sure if these can be put in the optimizer since they are also computed below 
    b_f_c            = 0 # Sai, I am not sure if these can be put in the optimizer since they are also computed below     

    
    
    # ------------------------------------------------------------------------------------------------------------------------      
    # Evaluate HEX Size (Sizing Problem) 
    # ------------------------------------------------------------------------------------------------------------------------    
    
    #Calculate C_h and C_c
    C_h                = m_dot_h*c_p_h_1 
    C_c                = C_h/C_R   
    
    #Calculate Outlet Temperatures 
    T_h_2              = -Q/C_h  + T_h_1              # eqn 25a 
    T_c_2              =  Q/C_c  + T_c_1              # eqn 25a    
    
   
    eff_HEX            = Q/(C_h*(T_h_1 -T_c_1 ) )               # eqn 27  
    
    sol                = minimize(solve_for_NTU, [1] , args=(Q,C_h,T_h_1,T_c_1,C_R), method='SLSQP', bounds=[0,20], tol=1e-6)  # Eqn 28 and 29   
    NTU                = sol.x   # eqn 29    
    
    #Determine Hot and cold side NTU
    ntu_c              = 1.1*C_R*NTU   
    ntu_h              = 10*NTU     
    
    #Inital Guess values for core mass compute
    eta_0_c_inita = 0.8
    eta_0_h_inita = 0.8
    
    div_f_c_inital  =0.25
    div_f_h_inital  =0.25
    
    # Inital Compute Core Mass Velcoity 
    G_c                = np.sqrt(2*rho_c_m*delta_p_c/(Pr_c**(2/3)) * (eta_0_c_inital*j_div_f_c_inital)/ntu_c  ) # eqn 30 
    G_h                = np.sqrt(2*rho_h_m*delta_p_c/(Pr_h**(2/3)) * (eta_0_h_inital*j_div_f_h_inital)/ntu_h  )    
    
    #Compute Reunolds Number 
    Re_h               = G_h*d_H_h/mu_h # Eqn 31 
    Re_c               = G_c*d_H_c/mu_c # Eqn 31     
    
    # Nusselt Number (eq 12)   
    if Re_c< 2300:
        Nu_c= 8.235*(1-(2.0421*AR_c)+(3.0853*AR_c**2)-(2.4765*AR_c**3)+(1.0578*AR_c**4)-(0.1861*AR_c**5))    
    elif Re_c >= 2300:
        Nu_c = ((f_c/2)*(Re_c-1000)*Pr_c)/(1+(12.7*(f_c**0.5)*(Pr_c**(2/3)-1)))     
        
    # Calculates Colburn Factor 
    
    j_h               =  (Nu_h * Pr_h**(-1/3))/ Re_h
    j_c               =  (Nu_c * Pr_c**(-1/3))/ Re_c       
    
    
    
    
    
    # ------------------------------------------------------------------------------------------------------------------------      
    # Evaluate HEX Performance (Rating Problem) 
    # ------------------------------------------------------------------------------------------------------------------------     
    
    # b_c, b_h, beta_h, beta_c, d_H_h, d_H_c, L_c, L_h, H_stack, t_w Need to bring in these variables as inital guesses. Everything is 1.0 exceot t_w=5e-4 
    
    #Caluclates the Surface Geometry Porperties 
    
    # Calculates the number of hot fluid passages eq (47)
    # Np+1 is considered the number iof passes for air, this is a common practice to minimize the heat losses to ambient 
    N_p = (H_stack - b_c - 2 * t_w) / (b_h + b_c + 2 * t_w)
    
    # the frontal areas on both fluid sides eq (48)
    A_fr_h                          = L_c * H_stack
    A_fr_c                          = L_h * H_stack    
    
    # the heat exchanger volume between plates on both fluid sides
    V_p_h                           = L_h * L_c * N_p * b_h
    V_p_c                           = L_h * L_c * (N_p + 1) * b_c

    # the heat transfer areas eq (49)
    A_h                             = beta_h * V_p_h
    A_c                             = beta_c * V_p_c    

    # the minimum free-flow areas [cross-section area of the fluid passages] (50)
    A_o_h                             = d_H_h * A_h / (4 * L_h)
    A_o_c                             = d_H_c * A_c / (4 * L_c)    

    # the ratio of minimum free-flow area to the frontal area (51)
    sigma_h                           = A_o_h / A_fr_h
    sigma_c                           = A_o_c / A_fr_c
    
    
    # Inital Assumption of eff_Hex=0.5; 
    #C_r=0.5; (Why?) 
    #p_c_2=p_c_1 Freestream pressure
    
    #The thermal Calculations 
    
    # Calculate the inital outlet temperature and mean temperatures with the guess values of eff. 
    
    # hot fluid eq (52a)
    T_h_2                           = T_h_1 - eff_HEX * (T_h_1 - T_c_1)
    T_h_m                           = (T_h_1 + T_h_2) / 2
  
    # Air Temperature eq (52b)
    T_c_2                           = T_c_1 + eff_HEX * C_R * (T_h_1 - T_c_1)
    T_c_m                           = (T_c_1 + T_c_2) / 2
    
    
    #*add thermal property calcilatyions*
    
    
    #CMV and Re values eq(31)
    G_h                             = m_dot_h / A_o_h #m_dot_h is assumed to be 1 (defaults) to start with. But then use eq 30 to calculate the inital reynaolds number. 
    G_c                             = m_dot_c / A_o_c #m_dot_c is assumed to be 1 to start with 

    Re_h                            = G_h * d_H_h / mu_h
    Re_c                            = G_c * d_H_c / mu_c    
    
    # Calculate friction factor, Nusselt Number, Colburn factor for hot fluid eq(32, 12, 33)
    if Re_h< 2300:
        f_h         = 24*(1-(1.3553*AR_h)+(1.9467*AR_h**2)-(1.7012*AR_h**3)+(0.9564*AR_h**4)-(0.2537*AR_h**5))      #Inital Value of AR_h needs to be defined in defaults
        Nu_h        = 8.235*(1-(2.0421*AR_h)+(3.0853*AR_h**2)-(2.4765*AR_h**3)+(1.0578*AR_h**4)-(0.1861*AR_h**5))   # IMP: Assumed contant values of Nu and f for AR=1 in original code 
        j_h         = (Nu_h * Pr_h**(-1/3))/ Re_h
    elif Re_h>=2300:
        f_h         = (0.0791*(Re_h**(-0.25)))*(1.8075-0.1125*AR_h)    
        Nu_h        = ((f_h/2)*(Re_h-1000)*Pr_h)/(1+(12.7*(f_h**0.5)*(Pr_h**(2/3)-1)))  
        j_h         = (Nu_h * Pr_h**(-1/3))/ Re_h
        
    # Calculate friction factor, Nusselt Number, Colburn factor for cold fluid eq(32, 12, 33)
        
    if Re_c< 2300:
        f_c         = 24*(1-(1.3553*AR_c)+(1.9467*AR_c**2)-(1.7012*AR_c**3)+(0.9564*AR_c**4)-(0.2537*AR_c**5))
        Nu_c        = 8.235*(1-(2.0421*AR_c)+(3.0853*AR_c**2)-(2.4765*AR_c**3)+(1.0578*AR_c**4)-(0.1861*AR_c**5)) 
        j_c         = (Nu_c * Pr_c**(-1/3))/ Re_c
    elif Re_c>=2300:
        f_c         = (0.0791*(Re_c**(-0.25)))*(1.8075-0.1125*AR_c)
        Nu_c        = ((f_c/2)*(Re_c-1000)*Pr_c)/(1+(12.7*(f_c**0.5)*(Pr_c**(2/3)-1)))  
        j_c         = (Nu_c * Pr_c**(-1/3))/ Re_c
    
    # convective heat transfer coefficent Eqn 34  
    h_h               = j_h * G_h * c_p_h /(Pr_h**(2/3)) 
    h_c               = j_c * G_c * c_p_c /(Pr_c**(2/3))
   
    # Geomtric fin property calcualtions 
    m_f_h             = np.sqrt(2 * h_h / k_f / t_f) #k_f=121W/m.K
    m_f_c             = np.sqrt(2 * h_c / k_f / t_f)# t_f= 1e-4m fin thickness 

    l_f_h             = b_h / 2 - t_f
    l_f_c             = b_c / 2 - t_f

    # Fin Efficiency Eq (35)
    eta_f_h           = np.tanh(m_f_h * l_f_h) / (m_f_h * l_f_h)   
    eta_f_c           = np.tanh(m_f_c * l_f_c) / (m_f_c * l_f_c)

    # overall fin efficiency Eq (36)
    eta_0_h           = 1 - (1 - eta_f_h) * A_f_div_A_h        # A_f/A_h inital value is 1.0    
    eta_0_c           = 1 - (1 - eta_f_c) * A_f_div_A_c        # A_f/A_c inital value is 1.0       

    # Calculates the Overall Heat Transfer modified eq(37) 
    A_w               = L_c * L_h * 2 * (N_p + 1)
    R_w               = t_w / (k_w * A_w) #k_w= 121 w/m.K
    UA                = 1 / (1 / (eta_0_h* h_h * A_h) + R_w + 1 / (eta_0_c * h_c * A_c))
    
    
    # This step we updates the values of eff_Hex, Cr
  
    C_h                             = m_dot_h*cp_h
    C_c                             = m_dot_c*cp_c
    #Calcualting C_min
    if C_h> C_c:
        C_min=C_c
    else:
        C_min=C_h
        
    C_R                             = C_h / C_c
    NTU                             = UA / C_min
    eff_HEX                         = 1 - np.exp(np.power(NTU, 0.22) / C_R * (np.exp(- C_R * np.power(NTU, 0.78)) - 1))  # Eq 29
    
    # Recomutes the temperatures based off the new effectivenss eq(25a) and eq (25b)
    Q                               = eff_HEX * C_min * (T_h_1 - T_c_1)
    T_h_2                           = T_h_1 - Q / C_h
    T_c_2                           = T_c_1 + Q / C_c
    
    # Pressure Drop Calculations (Use updated values from the thermal calculations)
    
    #Calculate wall temperature 
    R_h                             = 1 / (eta_o_h * h_h * A_h)  # hot fluid -- liquid coolant
    R_c                             = 1 / (eta_o_c * h_c * A_c)  # cold fluid -- air
    
    T_w                             = (T_h_m + (R_h / R_c) * T_c_m) / (1 + R_h / R_c) #calculates wall temperature 
    
    #Calculate friction factor for HEX cold side  (Temperature dependenat property effects of gases, Table 7.12 and eq 7.157 from the textbook)
    if Re_c< 2300: 
        f_c_updated              = f_c * np.power((T_w / T_c_m), 1)  
    else:
        f_c_updated              = f_c * np.power((T_w / T_c_m), -0.1)
    
    #Calculate friction factor for HEX cold side  (Temperature dependenat property effects of gases, Table 7.12 and eq 7.158 from the textbook)
    #include the function to calculate coolant viscoscity at wall temp
    if Re_h< 2300:
        f_h_updated          = f_h * np.power((mu_h_w / mu_h), 0.54)  # mu_h_w / mu_m_h > 1 Given viscoscity at wall and bulk viscoscity
    else:
        f_h_updated          = f_h * np.power((mu_h_w / mu_h), -0.25)  # 1 < mu_h_w / mu_m_h < 40
        
    
    # Computes the heat exchanger enterance and exit coefficients 
    Ke_c, Kc_c        = compute_heat_exhanger_factors(hex_opt.kc_values,hex_opt.kc_values,sigma_c, Re_c)
    
    #Calcuate the pressure drop
    delta_p_h                       = 4 * np.power(G_h, 2) * f_h_updated * L_h / (2 * rho_h * d_H_h)

    delta_p_c                       = np.power(G_c, 2) / (2 * rho_c_1) * ((1 - np.power(sigma_c, 2) + Kc_c)
                                        + 2 * (rho_c_1 / rho_c_2 - 1) + f_c_updated * 4 * L_c / d_H_c * rho_c_1 / rho_c_m
                                        - (1 - np.power(sigma_c, 2) - Ke_c) * rho_c_1 / rho_c_2) #eq 9.20 
    
    
    
    
    
    
    
    
    
    
    
    
    # ------------------------------------------------------------------------------------------------------------------------  
    #  Compute residuals 
    # ------------------------------------------------------------------------------------------------------------------------  
    # j/c 
    j_div_f_c_true     = j_c/f_c
    j_div_f_h_true     = j_h/f_h
    nexus.results.j_div_f_c_residual = j_div_f_c_guess-j_div_f_c_true 
    nexus.results.j_div_f_h_residual = j_div_f_h_guess-j_div_f_h_true 
    
    # overall efficiency 
    nexus.results.eta_0_c_residual   = eta_0_c_guess - eta_0_c
    nexus.results.eta_0_h_residual   = eta_0_h_guess - eta_0_h
    
    # pressure ratios 
    PI_c_true          = 1-delta_p_c_true/p_c_1
    PI_h_true          = 1-delta_p_h_true/p_h_1 
    nexus.results.PI_c_residual      = PI_c_guess - PI_c_true
    nexus.results.PI_h_residual      = PI_h_guess - PI_h_true
    
    # ------------------------------------------------------------------------------------------------------------------------  
    #  Pack results   
    # ------------------------------------------------------------------------------------------------------------------------  
    nexus.results.stack_height                    = H  
    nexus.results.heat_exchanger_mass             = m_hex
    nexus.results.number_of_passes                = N_p
    nexus.results.power_draw                     = P_hex  
    
    return nexus    

def solve_for_NTU(NTU,Q,C_h,T_h_1,T_c_1,C_R): 
    return Q/(C_h*(T_h_1 - T_c_1)) - (1 - np.exp(((NTU[0]**0.22)/C_R)*(np.exp(-C_R*(NTU[0]**0.78))))) # Eqn 28 and 29   
 

# ----------------------------------------------------------------------
#   Post Process Results to give back to the optimizer
# ----------------------------------------------------------------------   
def post_process(nexus):
    battery       = nexus.hrs_configurations.optimized.networks.all_electric.busses.bus.batteries.lithium_ion_nmc 
    hex_opt       = battery.thermal_management_system.heat_exchanger
    
    summary             = nexus.summary   
    # -------------------------------------------------------
    # Objective 
    # -------------------------------------------------------   
    summary.objective      = nexus.results.power_draw 
    

    # -------------------------------------------------------
    # Constraints 
    # -------------------------------------------------------       
    
 
    return nexus     