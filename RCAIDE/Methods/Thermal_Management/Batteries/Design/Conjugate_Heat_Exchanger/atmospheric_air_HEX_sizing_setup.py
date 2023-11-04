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
  
    # fized paramters   
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
    # Hex Geometry 
    # ------------------------------------------------------------------------------------------------------------------------  
    A_f_div_A_h        = AR_h/(1+AR_h) # eqn 21 
    A_f_div_A_c        = AR_c/(1+AR_c)
    
    # ------------------------------------------------------------------------------------------------------------------------  
    # Thermodynamic calculations with desired heat tranfer rate, and pressure ratios, and inlet pressures
    # ------------------------------------------------------------------------------------------------------------------------  
    C_h                = m_dot_h*c_p_h_1 
    C_c                = C_h/C_R   
    T_h_2              = -Q/C_h  + T_h_1              # eqn 25a 
    T_c_2              =  Q/C_c  + T_c_1              # eqn 25a    
    c_p_c_1            = air.compute_cp(T_c_1,p_c_1)
    m_dot_c            = C_c/c_p_c_1                  # eqn 26  
    hex_effectiveness  = Q/(C_h*(T_h_1 -T_c_1 ) )     # eqn 27  
    delta_p_h          = (1-PI_h_guess)*p_h_1         # eqn 28 
    delta_p_c          = (1-PI_c_guess)*p_c_1       
    
    # ------------------------------------------------------------------------------------------------------------------------  
    #  STEP 2 : finding NTU  
    # ------------------------------------------------------------------------------------------------------------------------  
    sol                = minimize(solve_for_NTU, [1] , args=(Q,C_h,T_h_1,T_c_1,C_R), method='SLSQP', bounds=[0,20], tol=1e-6)  # Eqn 28 and 29   
    NTU                = sol.x   # eqn 29
                
    ntu_c              = 1.1*C_R*NTU   
    ntu_h              = 10*NTU 
                  
    Pr_c               = air.compute_Pr(T_c_1,p_c_1)
    Pr_h               = coolant.compute_Pr(T_c_1,p_c_1)
    mu_h               = air.compute_dynamic_viscosity(T_c_1,p_c_1)
    mu_c               = coolant.compute_dynamic_viscosity(T_c_1,p_c_1)
                
    p_h_2              = p_h_1  - delta_p_h
    p_c_2              = p_c_1  - delta_p_c
    rho_h_1            = coolant.density(T_h_1,p_h_1)
    rho_h_2            = coolant.density(T_h_2,p_h_2)
    rho_c_m            =  2/(1/rho_c_1 + 1/rho_c_2)
    rho_h_m            =  2/(1/rho_h_1 + 1/rho_h_2)
            
    G_c                = np.sqrt(2*rho_c_m*delta_p_c/(Pr_c**(2/3)) * (eta_0_c_guess*j_div_f_c_guess)/ntu_c  ) # eqn 30 
    G_h                = np.sqrt(2*rho_h_m*delta_p_c/(Pr_h**(2/3)) * (eta_0_h_guess*j_div_f_h_guess)/ntu_h  )
                    
    Re_h               = G_h*d_H_h/mu_h # Eqn 31 
    Re_c               = G_c*d_H_c/mu_c # Eqn 31  
     
    # hot fluid 
    # fanning friction factor (eq 32)
    if Re_c< 2300:
        f_c= 24*(1-(1.3553*AR_c)+(1.9467*AR_c**2)-(1.7012*AR_c**3)+(0.9564*AR_c**4)-(0.2537*AR_c**5))
    elif Re_c>=2300:
        f_c= (0.0791*(Re_c**(-0.25)))*(1.8075-0.1125*AR_c)

    # Nusselt Number (eq 12)   
    if Re_c< 2300:
        Nu_c= 8.235*(1-(2.0421*AR_c)+(3.0853*AR_c**2)-(2.4765*AR_c**3)+(1.0578*AR_c**4)-(0.1861*AR_c**5))    
    elif Re_c >= 2300:
        Nu_c = ((f_c/2)*(Re_c-1000)*Pr_c)/(1+(12.7*(f_c**0.5)*(Pr_c**(2/3)-1)))  

     
    # hot fluid 
    # fanning friction factor (eq 32)
    if Re_h< 2300:
        f_h= 24*(1-(1.3553*AR_h)+(1.9467*AR_h**2)-(1.7012*AR_h**3)+(0.9564*AR_h**4)-(0.2537*AR_h**5))
    elif Re_h>=2300:
        f_h= (0.0791*(Re_h**(-0.25)))*(1.8075-0.1125*AR_h)

    # Nusselt Number (eq 12)   
    if Re_h< 2300:
        Nu_h= 8.235*(1-(2.0421*AR_h)+(3.0853*AR_h**2)-(2.4765*AR_h**3)+(1.0578*AR_h**4)-(0.1861*AR_h**5))    
    elif Re_h >= 2300:
        Nu_h = ((f_h/2)*(Re_h-1000)*Pr_h)/(1+(12.7*(f_h**0.5)*(Pr_h**(2/3)-1)))  
            
    j_h               =  (Nu_h * Pr_h**(-1/3))/ Re_h
    j_c               =  (Nu_c * Pr_c**(-1/3))/ Re_c   

    # convective heat transfer coefficent Eqn 34  
    h_h               = j_h * G_h * c_p_h /(Pr_h**(2/3)) # not sure what cp value to use here  
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
    
    # area density
    beta_h            = 4 * (1 + AR_h) / (d_H_h * (1 + AR_h) + 2 * AR_h * t_f) # Eqn 22
    beta_c            = 4 * (1 + AR_c) / (d_H_c * (1 + AR_c) + 2 * AR_c * t_f) 
                     
    alpha_h           = (b_f_h*beta_h)/(b_f_c + b_f_h + 2*t_w)
    alpha_c           = (b_f_c*beta_c)/(b_f_c + b_f_h + 2*t_w)

    # the ratio of minimum free-flow area to the frontal area
    sigma_h           = alpha_h*d_H_h/ 4
    sigma_c           = alpha_c*d_H_c/ 4
 
    U_h               = 1/( (1/(eta_0_h*h_h) ) + ((alpha_c/alpha_h)/(eta_0_c*h_c))) # eqn 37
    A_h               = NTU * (C_h/U_h)       # eqn 38 a 
    A_c               = A_h*(alpha_c/alpha_h) # eqn 38 b  
    
    A_0_h              = m_dot_h/G_c
    A_0_c              = m_dot_c/G_h 
                      
    A_fr_h            = A_0_h/sigma_h # eqn 40
    A_fr_c            = A_0_c/sigma_c  
    
    L_h               = A_h*d_H_h/(4*A_0_c) # eqn 41
    L_c               = A_c*d_H_c/(4*A_0_h)
    
    H                 = A_fr_c /L_h # eqn 42
                      
    Ke_c, Kc_c        = compute_heat_exhanger_factors(hex_opt.kc_values,hex_opt.kc_values,sigma_c, Re_c)
    
    # get density of fluids 
    rho_c_1           = air.compute_density(T_c_1,p_c_1)
    rho_c_2           = air.compute_density(T_c_2,p_c_2) 
    
    # asssume mean densities are used in computations of pressure losses 
    rho_c = (rho_c_1 +rho_c_2)/2
    rho_h = (rho_h_1 +rho_h_2)/2
                      
    rho_c_m           = 2/(1/rho_c_1 + 1/rho_c_2)
    delta_p_c_true    = (G_h**2 / (2 * rho_c_1)) * ((1 - sigma_c**2 + Kc_c)  + 2 * (rho_c_1 / rho_c_2 - 1)\
                    + f_c * 4 * L_c / d_H_c * rho_c_1 / rho_c_m  - (1 - sigma_c**2 - Ke_c) * rho_c_1 / rho_c_2)  #eqn 43 
  

    # ------------------------------------------------------------------------------------------------------------------------  
    #  System-level calculations
    # ------------------------------------------------------------------------------------------------------------------------  
    # masses (eqn 45)
    V_hex             = L_c*L_h*H
    m_hex             = density_hex * V_hex * (1 - sigma_h - sigma_c)  
    
    # power (eqn 46)
    u_c               = m_dot_c/(rho_c*A_c)  
    P_hex             = m_dot_h * (delta_p_h / rho_h) / pump_efficiency  +  (m_dot_c*(delta_p_c/rho_c) +  (u_c**2)*0.5)/fan_efficiency
    
    # number of passes 
    N_p               =  (H - b_f_c - 2 * t_w) / (b_f_h + b_f_c + 2 * t_w) 
    
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