# compute_heat_exhanger_factors_offdesign_performance.py
#
# Created : Dec 2022, C.R. Zhao
# Modified: Jun 2023, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------- 
from RCAIDE.Core import Data 
import numpy as np
import CoolProp.CoolProp as CoolProp 
from RCAIDE.Attributes.Gases import Air
from RCAIDE.Methods.Thermal_Management.Batteries.Conjugate_Cooling.compute_heat_exhanger_factors import compute_heat_exhanger_factors  

# ----------------------------------------------------------------------
#  Methods
# ----------------------------------------------------------------------
## @ingroup Methods-Thermal_Management-Batteries-Channel_Cooling 
def compute_surface_geometry_properties(b_c, b_h, beta_h, beta_c, d_H_h, d_H_c, L_c, L_h, H_stack, t_w): 
    """sizing of HEX with """
    
    # assume  N_p passages for the liquid and (N_p + 1) passages for the air
    N_p = (H_stack - b_c - 2 * t_w) / (b_h + b_c + 2 * t_w)

    # the frontal areas on both fluid sides
    A_fr_h                          = L_c * H_stack
    A_fr_c                          = L_h * H_stack

    # the heat exchanger volume between plates on both fluid sides
    V_p_h                           = L_h * L_c * N_p * b_h
    V_p_c                           = L_h * L_c * (N_p + 1) * b_c

    # the heat transfer areas
    A_h                             = beta_h * V_p_h
    A_c                             = beta_c * V_p_c

    # the minimum free-flow areas [cross-section area of the fluid passages]
    A_o_h                             = d_H_h * A_h / (4 * L_h)
    A_o_c                             = d_H_c * A_c / (4 * L_c)

    # the ratio of minimum free-flow area to the frontal area
    sigma_h                           = A_o_h / A_fr_h
    sigma_c                           = A_o_c / A_fr_c

    Surface_Geom_Properties = Data(
        N_p             = N_p,
        A_fr_h          = A_fr_h,
        A_fr_c          = A_fr_c,
        A_h             = A_h,
        A_c             = A_c,
        A_o_h           = A_o_h,
        A_o_c           = A_o_c,
        sigma_h         = sigma_h,
        sigma_c         = sigma_c)

    return Surface_Geom_Properties

def compute_offdesign_thermal_properties(atmospheric_conditions, m_dot_h=None, m_dot_c=None, C_R=None, eff_HEX=None, T_h_1=None, T_c_1=None,
                  A_o_h=None, A_o_c=None, d_H_h=None, d_H_c=None, AP_chan_h=None, AP_chan_c=None, k_f=None, t_f=None,
                  b_h=None, b_c=None, A_f_by_A_h=None, A_f_by_A_c=None, L_c=None, L_h=None, N_p=None, t_w=None,
                  k_w=None, A_h=None, A_c=None, p_c_2=None, p_h_2=None):
    """sizing of HEX with """
    # ---------------------------------------------------------------------------------
    # thermodynamic design
    # ---------------------------------------------------------------------------------
    # input parameters
    # hot fluid is water-based coolant
    # cold fluid is air 
     
    # output parameters 
    # hot fluid properties 
    rho_h                           = 1075               # kg/m^3
    k_h                             = 0.387              # W/m.K
    cp_h                            = 3300               # J/kg.K
    mu_h                            = 0.0019             # Pa.s
    Pr_h                            = cp_h * mu_h / k_h  # - [16.2]

    # cold fluid properties

    # ---------------------------------------------------------------------------------
    # Input the ambient air properties
    # --------------------------------------------------------------------------------- 
    air_density                     = atmospheric_conditions.density 
    air_dynamic_viscosity           = atmospheric_conditions.dynamic_viscosity 
    air_thermal_conductivity        = atmospheric_conditions.thermal_conductivity
    air_Prandtl_number              = atmospheric_conditions.prandtl_number

    # parameters                    values                                              units
    rho_c_1                         = air_density                                       # kg/m^3
    k_c_1                           = air_thermal_conductivity                          # W/m.K
    cp_c_1                          = air_Prandtl_number * air_thermal_conductivity / air_dynamic_viscosity   # J/kg.K
    mu_c_1                          = air_dynamic_viscosity                             # Pa.s
    Pr_c_1                          = air_Prandtl_number                                # -

    # outlet temperature of both fluid sides 
    # hot fluid
    T_h_2                           = T_h_1 - eff_HEX * (T_h_1 - T_c_1)
    T_h_m                           = (T_h_1 + T_h_2) / 2
    # cold fluid
    T_c_2                           = T_c_1 + eff_HEX * C_R * (T_h_1 - T_c_1)
    T_c_m                           = (T_c_1 + T_c_2) / 2

    #estimate the cold fluid properties 
    # cold fluid properties at the outlet side
    
    cold_fuild = Air() 
    rho_c_2     = cold_fuild.compute_density(T_c_2,p_c_2) 
    k_c_2       = cold_fuild.compute_thermal_conductivity(T_c_2,p_c_2) 
    cp_c_2      = cold_fuild.compute_cp(T_c_2,p_c_2)  
    mu_c_2      = cold_fuild.compute_absolute_viscosity(T_c_2,p_c_2) 
    Pr_c_2      = cold_fuild.compute_prandtl_number(T_c_2)  
     
    #rho_c_2     = np.atleast_2d(CoolProp.PropsSI('D', 'P', p_c_2, 'T', T_c_2, 'Air')).T
    #k_c_2       = np.atleast_2d(CoolProp.PropsSI('L', 'P', p_c_2, 'T', T_c_2, 'Air')).T
    #cp_c_2      = np.atleast_2d(CoolProp.PropsSI('C', 'P', p_c_2, 'T', T_c_2, 'Air')).T
    #mu_c_2      = np.atleast_2d(CoolProp.PropsSI('V', 'P', p_c_2, 'T', T_c_2, 'Air')).T
    #Pr_c_2      = np.atleast_2d(CoolProp.PropsSI('Prandtl', 'P', p_c_2, 'T', T_c_2, 'Air')).T

    # mean cold fluid properties
    rho_c_m                         = 2 / (1 / rho_c_1 + 1 / rho_c_2) 
    cp_c                            = (cp_c_1 + cp_c_2) / 2
    mu_c                            = (mu_c_1 + mu_c_2) / 2
    Pr_c                            = (Pr_c_1 + Pr_c_2) / 2

    #CMV and Re values 
    G_h                             = m_dot_h / A_o_h
    G_c                             = m_dot_c / A_o_c

    Re_h                            = G_h * d_H_h / mu_h
    Re_c                            = G_c * d_H_c / mu_c

    # todo modify the Re_h to have the same shape of Re_c
    Re_h                            = Re_h * np.ones_like(Re_c)
    
    #j and f factors for hot fluid side, assuming L > d_H 
    ii = Re_h <= 2300 
    f_h_1           = 14.227 / Re_h
    
    # assume constant axial wall heat flux with constant peripheral wall temperature, for AP_chan = 1
    Nu_h_1          = 3.608
    j_h_1           = Nu_h_1 / Re_h * np.power(Pr_h, -1 / 3)

    f_h_2           = 0.0791 * np.power(Re_h, -0.25) * (1.0875 - 0.1125 * AP_chan_h)
    # f_h_2 = 1 / (4 * np.power(1.8 * np.log10(Re_h / 7.7), 2))
    
    # use Gnielinski equation to calculate Nu for 0.5 < Pr < 2000, 3000 < Re < 5e6
    Nu_h_2          = (f_h_2 / 2) * (Re_h - 1000) * Pr_h / (1 + 12.7 * np.power((f_h_2 / 2), 0.5) * (np.power(Pr_h, 2 / 3) - 1))
    j_h_2           = Nu_h_2 / Re_h * np.power(Pr_h, -1 / 3)

    f_h                             = f_h_1 * ii + f_h_2 * (1 - ii)
    j_h                             = j_h_1 * ii + j_h_2 * (1 - ii)

    # j and f factors for cold fluid side, assuming L > d_H 
    jj = Re_c <= 2300

    f_c_1           = 24 * (1 - 1.3553 * np.power(1 / AP_chan_c, 1) + 1.9467 * np.power(1 / AP_chan_c, 2)
                            - 1.7012 * np.power(1 / AP_chan_c, 3) + 0.9564 * np.power(1 / AP_chan_c, 4) - 0.2537 * np.power(1 / AP_chan_c, 5)) / Re_c
    Nu_c_1          = 8.235 * (1 - 2.0421 * np.power(1 / AP_chan_c, 1) + 3.0853 * np.power(1 / AP_chan_c, 2)
                               - 2.4765 * np.power(1 / AP_chan_c, 3) + 1.0578 * np.power(1 / AP_chan_c, 4) - 0.1861 * np.power(1 / AP_chan_c, 5))
    j_c_1           = Nu_c_1 / Re_c * np.power(Pr_c, -1 / 3)

    f_c_2           = 0.0791 * np.power(Re_c, -0.25) * (1.0875 - 0.1125 * AP_chan_c)
    # f_c_2 = 1 / (4 * np.power(1.8 * np.log10(Re_c / 7.7), 2))
    
    # use Gnielinski equation to calculate Nu for 0.5 < Pr < 2000, 3000 < Re < 5e6
    Nu_c_2          = (f_c_2 / 2) * (Re_c - 1000) * Pr_c / (1 + 12.7 * np.power((f_c_2 / 2), 0.5) * (np.power(Pr_c, 2 / 3) - 1))
    j_c_2           = Nu_c_2 / Re_c * np.power(Pr_c, -1 / 3)

    f_c                             = f_c_1 * jj + f_c_2 * (1 - jj)
    j_c                             = j_c_1 * jj + j_c_2 * (1 - jj)

    # overall heat transfer coefficient, UA 
    h_h                             = j_h * G_h * cp_h / np.power(Pr_h, 2 / 3)
    h_c                             = j_c * G_c * cp_c / np.power(Pr_c, 2 / 3)
    
    # fin efficiency calculation
    m_h                             = np.sqrt(2 * h_h / k_f / t_f)
    l_h                             = b_h / 2 - t_f
    eta_f_h                         = np.tanh(m_h * l_h) / (m_h * l_h)
     
    m_c                             = np.sqrt(2 * h_c / k_f / t_f)
    l_c                             = b_c / 2 - t_f
    eta_f_c                         = np.tanh(m_c * l_c) / (m_c * l_c)
    # overall fin efficiency
    eta_o_h                         = 1 - (1 - eta_f_h) * A_f_by_A_h
    eta_o_c                         = 1 - (1 - eta_f_c) * A_f_by_A_c

    # wall resistance and overall conductance
    A_w                             = L_c * L_h * 2 * (N_p + 1)
    R_w                             = t_w / (k_w * A_w)
    UA                              = 1 / (1 / (eta_o_h * h_h * A_h) + R_w + 1 / (eta_o_c * h_c * A_c))

    # heat capacity ratio and NTU
    C_h                             = C_min = m_dot_h * cp_h
    C_c                             = m_dot_c * cp_c

    C_R                             = C_h / C_c
    NTU                             = UA / C_min
    eff_HEX                         = 1 - np.exp(np.power(NTU, 0.22) / C_R * (np.exp(- C_R * np.power(NTU, 0.78)) - 1))

    # compute heat duty and outlet temperature 
    Q                               = eff_HEX * C_min * (T_h_1 - T_c_1)
    T_h_2                           = T_h_1 - Q / C_h
    T_c_2                           = T_c_1 + Q / C_c

    # total output results  
    Thermo_OffDesign = Data(
        Q              = Q,
        T_h_2          = T_h_2,
        T_c_2          = T_c_2,
        C_R            = C_R,
        NTU            = NTU,
        eff_HEX        = eff_HEX, 
        T_h_1          = T_h_1,
        T_c_1          = T_c_1, 
        Re_h           = Re_h,
        Re_c           = Re_c,
        eta_o_h        = eta_o_h,
        eta_o_c        = eta_o_c,
        h_h            = h_h,
        h_c            = h_c,
        f_h            = f_h,
        f_c            = f_c,
        G_h            = G_h,
        G_c            = G_c,
        rho_c_1        = rho_c_1,
        rho_c_2        = rho_c_2,
        rho_c_m        = rho_c_m,
        T_c_m          = T_c_m,
        rho_h          = rho_h,
        mu_h           = mu_h,
        T_h_m          = T_h_m)

    return Thermo_OffDesign

def compute_offdesign_pressure_properties(kc_vals,ke_vals,sigma_h=None, sigma_c=None, Re_h=None, Re_c=None, eta_o_h=None, eta_o_c=None,
                       h_h=None, h_c=None, A_h=None, A_c=None, f_c=None, f_h=None, L_h=None, L_c=None,
                       d_H_h=None, d_H_c=None, G_c=None, rho_c_1=None, rho_c_2=None, rho_c_m=None, T_m_c=None,
                       rho_h=None, G_h=None, mu_h=None, T_m_h=None, p_1_h=1.01325e5):
    '''
    Iteration to match design pressure ratios 
    ''' 

    # actual pressure drop calculation 
    # determine the entrance and exit coefficients  
    
    # cold fluid
    Kc_c, Ke_c                      = compute_heat_exhanger_factors(kc_vals,ke_vals,sigma_c, Re_c) 

    # update f factor based on wall temperature 
    R_h                             = 1 / (eta_o_h * h_h * A_h)  # hot fluid -- liquid coolant
    R_c                             = 1 / (eta_o_c * h_c * A_c)  # cold fluid -- air

    T_w                             = (T_m_h + (R_h / R_c) * T_m_c) / (1 + R_h / R_c)

    # air is being heated
    x = Re_c < 2300

    f_c_updated_1                   = f_c * np.power((T_w / T_m_c), 1)  # 1 < T_w / T_m_c < 3
    f_c_updated_2                   = f_c * np.power((T_w / T_m_c), -0.1)  # 1 < T_w / T_m_c < 2.4

    f_c_updated                     = f_c_updated_1 * x + f_c_updated_2 * (1 - x)

    # water is being cooled -- assume liquid coolant is water here
    mu_h_w                          = CoolProp.PropsSI('V', 'P', p_1_h, 'T', T_w, 'Water') 
    
    y = Re_h < 2300

    f_h_updated_1                   = f_h * np.power((mu_h_w / mu_h), 0.54)  # mu_h_w / mu_m_h > 1
    # valid for 2 < Pr < 140, 10^4 < Re < 1.25 * 10^5
    f_h_updated_2                   = f_h * np.power((mu_h_w / mu_h), -0.25)  # 1 < mu_h_w / mu_m_h < 40

    f_h_updated                     = f_h_updated_1 * y + f_h_updated_2 * (1 - y)
    
    # update for pressure drop 
    delta_p_h                       = 4 * np.power(G_h, 2) * f_h_updated * L_h / (2 * rho_h * d_H_h)

    delta_p_c                       = np.power(G_c, 2) / (2 * rho_c_1) * ((1 - np.power(sigma_c, 2) + Kc_c)
                                        + 2 * (rho_c_1 / rho_c_2 - 1) + f_c_updated * 4 * L_c / d_H_c * rho_c_1 / rho_c_m
                                        - (1 - np.power(sigma_c, 2) - Ke_c) * rho_c_1 / rho_c_2)

    # total output results 
    Pressure_OffDesign = Data(
        delta_p_h                       = delta_p_h,
        delta_p_c                       = delta_p_c)

    return Pressure_OffDesign

def compute_offdesign_geometry(rho_HEX=2780, eff_FAN=0.7, eff_PUMP=0.7, rho_h=None, N_p=None, H_stack=None,
                        sigma_h=None, L_c=None, m_dot_h=None, delta_p_h=None,
                        sigma_c=None, L_h=None, m_dot_c=None, delta_p_c=None,
                        rho_c_m=None, G_c=None, rho_c_2=None, rho_c_1=None):

    """step4: design results
    
    """ 

    A_base_c = L_c * L_h * 2 * (N_p + 1)
    A_base_h = L_c * L_h * 2 * N_p 
    A_fr_c   = L_h * H_stack
    A_fr_h   = L_c * H_stack 
    m_HEX    = rho_HEX * L_h * A_fr_h * (1 - sigma_h - sigma_c) * 1.1

    P_HEX_c  = m_dot_c * (delta_p_c / rho_c_m - 0.5 * np.power(G_c, 2) * (1 / np.power(rho_c_2, 2) - 1 / np.power(rho_c_1, 2))) / eff_FAN / 1e3
    P_HEX_h  = m_dot_h * (delta_p_h / rho_h) / eff_PUMP / 1e3

    P_HEX    = (P_HEX_c + P_HEX_h) * 0.9

    # total output results
    OffDesign_Results = Data(
        A_base_c                        = A_base_c,
        A_base_h                        = A_base_h,
        A_fr_c                          = A_fr_c,
        A_fr_h                          = A_fr_h,
        m_HEX                           = m_HEX,
        P_HEX_c                         = P_HEX_c,
        P_HEX_h                         = P_HEX_h,
        P_HEX                           = P_HEX)

    return OffDesign_Results
