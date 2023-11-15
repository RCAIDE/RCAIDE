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
from scipy.optimize import minimize,fsolve 
import numpy as np 
import scipy as sp  

## @ingroup Methods-Thermal_Management-Batteries-Sizing 
def atmospheric_air_HEX_sizing_setup(): 
    
    # size the base config
    procedure = Process()
    
    # modify battery thermal management system
    procedure.modify_hex = modify_crossflow_hex_size

    # post process the results
    procedure.post_process = post_process
        
    return procedure

def modify_crossflow_hex_size(nexus): 
    
    """ 
    """     
    hex_opt       = nexus.hex_configurations.optimized.networks.all_electric.busses.bus.batteries.lithium_ion_nmc.thermal_management_system.heat_exchanger
  
    # ------------------------------------------------------------------------------------------------------------------------
    # Unpack paramters  
    # ------------------------------------------------------------------------------------------------------------------------
    
    # Overall HEX properties
    eff_hex     = 0.8381     # Assigned design variable by user (fixed)
    delta_p_h   = 9.05e3 #Pa # Assigned design variable by user (fixed) 
    delta_p_c   = 8.79e3 #Pa # Assigned design variable by user (fixed) 
      
    # Inlet Temperatures 
    T_i_h       = hex_opt.coolant_temperature_of_hot_fluid #deg C # HRS input
    T_i_c       = hex_opt.inlet_temperature_of_cold_fluid #deg C # atmosphere
                
    # Inlet Pressures
    P_i_h       = hex_opt.coolant_inlet_pressure #Pa # HRS
    P_i_c       = hex_opt.inlet_pressure_of_cold_fluid #Pa # Fan (user)   
                
    # Hydraulic Diameters
    d_h_c       = hex_opt.coolant_hydraulic_diameter #m # optimized variable
    d_h_h       = hex_opt.air_hydraulic_diameter #m # optimized variable    
                
    # Fin Height/Spaceing 
    b_c         = 2.49e-3 #m # fixed variable
    b_h         = 2.49e-3 #m # fixed variable
                
    # Fin metal thickness
    delta_h     = 0.102e-3 #m
    delta_c     = 0.102e-3 #m
    
    # Platethickness
    delta_w     = hex_opt.t_w #m    
    
    # Strip edge exposed 
    l_s_h       = 3.175e-3 #m
    l_s_c       = 3.175e-3 #m
    
    #Fin and wall Conductivity 
    k_f         = hex_opt.k_f #W/mK  
    k_w         = hex_opt.k_w #W/mK  
    
    # Ratio of finned area to total area 
    Af_A_h      = hex_opt.coolant_channel_aspect_ratio  # fixed variable
    Af_A_c      = hex_opt.air_channel_aspect_ratio      # fixed variable    
    
    #Finned area density 
    beta_h      = 2254 #m^2/m^3 # fixed variable 
    beta_c      = 2254 #m^2/m^3 # fixed variable
    
    #mass flow rates of the fluids
    m_dot_h     = hex_opt.mass_flow_rate_of_hot_fluid #kg/s #HRS
    m_dot_c     = 2.00 #kg/s # Optimized variable
    
    #Efficiency 
    pump_efficiency  = hex_opt.pump_efficiency
    fan_efficiency   = hex_opt.fan_efficiency  
    
    #Define working fluids 
    air              = hex_opt.air
    coolant          = hex_opt.coolant    
    
    # Assumed inital values of j/f and efficiency 
    j_f_h,j_f_c        = 0.25,0.25
    eta_o_h, eta_o_c   = 0.8,0.8    
    
    # ------------------------------------------------------------------------------------------------------------------------      
    # Evaluate HEX Size (Sizing Problem) 
    # ------------------------------------------------------------------------------------------------------------------------    
    
    # Calculate the Outlet Temperatures 
    
    T_o_h   = T_i_h-eff_hex*(T_i_h-T_i_c)
    T_o_c   = T_i_c+(eff_hex*m_dot_h/m_dot_c)*(T_i_h-T_i_c)    
    
    # Evaluate the fluid properties at mean temperature 
    T_m_h   = (T_o_h+T_i_h)/2
    T_m_c   = (T_o_c+T_i_c)/2    
    
    # Evaluate the bulk Cp values 
    c_p_h   = coolant.compute_cp(T_m_h) #J/kg-K
    c_p_c   = air.compute_cp(T_m_c)     #J/kg-K
    
    
    # Maximum iterations and tolerance for convergence of c_p
    max_iterations_c_p    = 100
    tolerance_c_p         = 10
    
    for iteration in range(max_iterations_c_p):
        T_o_c         = T_i_c + (eff_hex * m_dot_h / (m_dot_c * c_p_c)) * (T_i_h - T_i_c)
        T_m_c         = (T_o_c + T_i_c) / 2
        c_p_c_new     = air.compute_cp(T_m_c)
                          
        if abs(c_p_c_new - c_p_c) < tolerance_c_p:
            c_p_c = c_p_c_new
            break
    
        c_p_c = c_p_c_new
    
    else:
        print("Error: Maximum iterations reached without convergence of specific heat of air. Continuing with last obtained value of c_p")
            
    # Fluid Properties are now evaluated based off the new outlet temperatures. 
    #Prandtl Number 
    Pr_h    = coolant.compute_prandtl_number(T_m_h)
    Pr_c    = air.compute_prandtl_number(T_m_c)
    
    #Absolute viscosity 
    mu_h    = coolant.compute_absolute_viscosity(T_m_h)
    mu_c    = air.compute_absolute_viscosity(T_m_c)

    # from the inlet and outlet pressures given the mean density is calcualted. 
    rho_h_i  = 0.4751 # kg/m^3
    rho_c_i  = 1.4726 # kg/m^3
    rho_h_o  = 0.8966 # kg/m^3
    rho_c_o  = 0.6817 # kg/m^3    
    rho_h_m  = 0.6212 # kg/m^3
    rho_c_m  = 0.9319 # kg/m^3

    # Heat Capacity 
    C_h              = m_dot_h*c_p_h
    C_c              = m_dot_c*c_p_c

    C_min, C_max = min(C_h, C_c), max(C_h, C_c)
    C_r            = C_min / C_max

    # Initial guess for NTU
    initial_guess  = 0.5
    NTU_data       = (C_r,eff_hex)
    # Solve for NTU using fsolve
    NTU_solution   = fsolve(equation, initial_guess,args = NTU_data )
    NTU            = NTU_solution[0] 

    # Assumed Values of NTU_h and NTU_c (Inital Guess)
    ntu_c   = NTU*2*C_r
    ntu_h   = NTU*2    # replace it with thr right values later 
    
    # Inital Compute Core Mass Velcoity
    G_h        = np.sqrt(2 * rho_h_m * delta_p_h / (Pr_h**(2/3)) * (eta_o_h * j_f_h) / ntu_h)
    G_c        = np.sqrt(2 * rho_c_m * delta_p_c / (Pr_c**(2/3)) * (eta_o_c * j_f_c) / ntu_c)
    
    
    check    =0
    
    while check==0: # Replace with for loop? Might result in an infinte loop
        
        # Calculate Reynolds Number
        Re_c       = G_c * d_h_c / mu_c
        Re_h       = G_h * d_h_h / mu_h


        # Calculate the colburn factor and friction factor using curve fitted values
        j_c            = 0.0131 * (Re_c / 1000)**(-0.415)
        j_h            = 0.0131 * (Re_h / 1000)**(-0.415)

        f_c            = 0.0514 * (Re_c / 1000)**(-0.471)
        f_h            = 0.0514 * (Re_h / 1000)**(-0.471)

        j_f_h          = j_h/f_h
        j_f_c          = j_c/f_c

        # Heat Transfer Coefficients
        h_h = j_h * G_h * c_p_h / (Pr_h**(2/3))
        h_c = j_c * G_c * c_p_c / (Pr_c**(2/3))

        m_f_h = (np.sqrt((2*h_h)/(k_f*delta_h)))*np.sqrt(1+(delta_h/l_s_h))
        m_f_c = (np.sqrt((2*h_c)/(k_f*delta_c)))*np.sqrt(1+(delta_c/l_s_c))


        l_f_h = b_h / 2 - delta_h
        l_f_c = b_c / 2 - delta_c

        # Fin Efficiency
        eta_f_h = np.tanh(m_f_h * l_f_h) / (m_f_h * l_f_h)
        eta_f_c = np.tanh(m_f_c * l_f_c) / (m_f_c * l_f_c)

        eta_o_h = 1 - (1 - eta_f_h) * Af_A_h
        eta_o_c = 1 - (1 - eta_f_c) * Af_A_c

        # Calculates the alpha to sub in the U equation coming up
        alpha_h = (b_h * beta_h) / (b_h + b_c + 2 * delta_w)
        alpha_c = (b_c * beta_c) / (b_h + b_c + 2 * delta_w)

        A_c_div_A_h = alpha_c / alpha_h

        # Calculate overall heat transfer without fouling
        U_h = 1 / ((1 / (eta_o_h * h_h)) + (A_c_div_A_h / (eta_o_c* h_c)))

        # Lets start calculating the geometrical properties now

        # Surface free flow Area, and Core dimensions
        A_h = NTU * C_h / U_h
        A_c = A_h * A_c_div_A_h

        # The minimum free flow area:
        A_o_h = m_dot_h / G_h
        A_o_c = m_dot_c / G_c

        # The airflow length is calculated as
        L_h = d_h_h * A_h / (4 * A_o_h)
        L_c = d_h_c * A_c / (4 * A_o_c)

        # ratio of the minimum free-flow area to the frontal area
        sigma_h = alpha_h * d_h_h / 4
        sigma_c = alpha_c * d_h_c / 4

        # the core frontal area on each fluid side
        A_f_h = A_o_h / sigma_h
        A_f_c = A_o_c / sigma_c

        # Calculate the height of the HEX PS the value of both L3 need to be almost the same, this is slightly different due to rounding off errors
        L_3_h = A_f_c / L_h
        L_3_c = A_f_h / L_c

        # ----------------------------------------------------------------------------------------------------------
        # Pressure Drop
        # ----------------------------------------------------------------------------------------------------------

        # Compute entrance and exit pressure loss coefficients (from the function that is already there)

        k_c_c = 0.36
        k_c_h = 0.36

        k_e_c = 0.42
        k_e_h = 0.42

        # Thermal Resistance on the hot and cold fluid sides

        R_h = 1 / (eta_o_h * h_h * A_h)
        R_c = 1 / (eta_o_c * h_c * A_c)

        # Compute Wall temperature
        T_w = (T_m_h + (R_h / R_c) * T_m_c) / (1 + R_h / R_c)

        # Considering temperature at wall effecting f value of 0.81 changes
        f_h_wall = f_h * np.power(((T_w + 273) / (273 + T_m_h)), 0.81)
        f_c_wall = f_c * np.power(((T_w + 273) / (273 + T_m_c)), 0.81)

        # Calculate Pressure Drop

        delta_p_c_updated = np.power(G_c, 2) / (2 * rho_c_i) * ((1 - np.power(sigma_c, 2) + k_c_c)
                                                              + 2 * (rho_c_i / rho_c_o - 1) + f_c_wall * 4 * L_c / d_h_c *
                                                      rho_c_i / rho_c_m
                                                       - (1 - np.power(sigma_c, 2) - k_e_c) * rho_c_i / rho_c_o)

        delta_p_h_updated = np.power(G_h, 2) / (2 * rho_h_i) * ((1 - np.power(sigma_h, 2) + k_c_h)
                                                              + 2 * (rho_h_i / rho_h_o - 1) + f_h_wall * 4 * L_h / d_h_h *
                                                      rho_h_i / rho_h_m
                                                       - (1 - np.power(sigma_h, 2) - k_e_h) * rho_h_i / rho_h_o)

        # Check if the pressure delta calculated is less than the threshold 

        res_c    = abs(delta_p_c_updated-delta_p_c)
        res_h    = abs(delta_p_h_updated-delta_p_h)


        if res_c <0.01 and res_h<0.01:

            check =1

        else:
            # Calculate the new core mass velocity

            G_h = np.sqrt((2 * rho_h_i * delta_p_h) / ((1 - np.power(sigma_h, 2) + k_c_h)
                                                    + 2 * (rho_h_i / rho_h_o - 1) + f_h_wall * 4 * L_h / d_h_h *
                                                          rho_h_i / rho_h_m
                                                              - (1 - np.power(sigma_h, 2) - k_e_h) * rho_h_i / rho_h_o))

            G_c = np.sqrt((2 * rho_c_i * delta_p_c) / ((1 - np.power(sigma_c, 2) + k_c_c)
                                                    + 2 * (rho_c_i / rho_c_o - 1) + f_c_wall * 4 * L_c / d_h_c *
                                                          rho_c_i / rho_c_m
                                                              - (1 - np.power(sigma_c, 2) - k_e_c) * rho_c_i / rho_c_o))      


    
 
 
 
 
    return nexus   


# Solve for NTU 
def equation(NTU,*data):
    C_r,eff_hex = data 
    return(1 - np.exp(((NTU**0.22)/C_r)*(np.exp(-C_r*(NTU**(0.78))) - 1 ))) - eff_hex
