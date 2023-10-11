## @ingroup Methods-Power-Battery 
# compute_net_generated_battery_heat_liquid.py
# 
# Created : Dec 2022, C.R. Zhao
# Modified: Jun 2023, M. Clarke
 
import numpy as np 
from RCAIDE.Attributes.Coolants.Glycol_Water import Glycol_Water
from RCAIDE.Attributes.Solids.Aluminum       import Aluminum  
from RCAIDE.Methods.Thermal_Management.Batteries.Conjugate_Cooling.compute_heat_exhanger_offdesign_performance import compute_offdesign_pressure_properties
from RCAIDE.Methods.Thermal_Management.Batteries.Conjugate_Cooling.compute_heat_exhanger_offdesign_performance import compute_offdesign_thermal_properties
from RCAIDE.Methods.Thermal_Management.Batteries.Conjugate_Cooling.compute_heat_exhanger_offdesign_performance import compute_surface_geometry_properties
from RCAIDE.Methods.Thermal_Management.Batteries.Conjugate_Cooling.compute_heat_exhanger_offdesign_performance import compute_offdesign_geometry

# ----------------------------------------------------------------------
#  Methods
# ----------------------------------------------------------------------
## @ingroup Methods-Thermal_Management-Batteries-Channel_Cooling
def compute_net_generated_battery_heat_chan( battery, Q_heat_gen,numerics, btms):
    """Computes the net heat generated in a battery module during cycling.
    Assumptions:
    1) Battery pack cell heat transfer can be modelled as a cooling columns in a cross-flow
    2) Isothermal battery cell - the temperature at the center of the cell is the same at
    the surface of the cell

    Inputs:
        battery.
              h                         (heat transfer coefficient)  [W/(m^2*K)]
              As_cell                   (battery cell surface area)  [meters^2]
              H_cell                    (battery cell height)        [meters]
              T_ambient                 (ambient temperature)        [Kelvin]
              T_current                 (pack temperature)           [Kelvin]
              T_cell                    (battery cell temperature)   [Kelvin]
              heat_transfer_efficiency                               [unitless]

      Outputs:
        battery.
             net_power                                               [Watts]
    """
    # ---------------------------------------------------------------------
    #   Default code from the air cooling
    # --------------------------------------------------------------------- 
    T_ambient                = btms.atmosphere_conditions.temperature  
    T_current                = battery.pack.temperature      
    cell_mass                = battery.cell.mass
    Cp                       = battery.cell.specific_heat_capacity
    I                        = numerics.time.integrate
    heat_transfer_efficiency = btms.heat_transfer_efficiency  

    Nn                = battery.module.geometrtic_configuration.normal_count            
    Np                = battery.module.geometrtic_configuration.parallel_count   
    n_total_module    = Nn*Np   

    # ---------------------------------------------------------------------
    #   Input Thermophysical Properties
    # --------------------------------------------------------------------- 
    # coolant liquid
    Coolant      = Glycol_Water() 
    k_coolant    = Coolant.thermal_conductivity
    cp_coolant   = Coolant.specific_heat_capacity 
    Pr_coolant   = Coolant.Prandtl_number
    
    # wavy channel material
    Channel   = Aluminum() 
    k_chan    = Channel.thermal_conductivity 

    # ---------------------------------------------------------------------
    #   Calculate the Output Temperature
    # ---------------------------------------------------------------------
    # heat transfer coefficient & heat transfer area
    m_dot_h_module              = btms.wavy_channel.mass_flow_rate_of_one_module
    A_chan_module               = btms.wavy_channel.contact_area_of_one_module
    Re_coolant                  = btms.wavy_channel.Reynolds_number_of_coolant_in_chan
    gamma_chan                  = btms.wavy_channel.aspect_ratio_of_chan
    d_H                         = btms.wavy_channel.hydraulic_diameter_of_chan
    b                           = btms.wavy_channel.cross_section.b
    
    if Re_coolant <= 2300:
        # Nusselt number
        Nu = 8.235 * (1 - 2.0421 * gamma_chan + 3.0853 * np.power(gamma_chan, 2) - 2.4765 * np.power(gamma_chan, 3)
                      + 1.0578 * np.power(gamma_chan, 4) - 0.1861 * np.power(gamma_chan, 5))
        # Colburn factor
        j_coolant = Nu / Re_coolant * np.power(Pr_coolant, -1 / 3)
    else:
        # Colburn factor
        f_coolant = 1 / (4 * (1.8 * np.log10(Re_coolant / 7.7)) ** 2)
        # use Gnielinski equation to calculate Nu for 0.5 < Pr < 2000, 3000 < Re < 5e6
        Nu = (f_coolant / 2) * (Re_coolant - 1000) * Pr_coolant / (
                1 + 12.7 * np.power((f_coolant / 2), 0.5) * (np.power(Pr_coolant, 2 / 3) - 1))
        # Colburn factor
        j_coolant = Nu / Re_coolant * np.power(Pr_coolant, -1 / 3)

    # heat transfer coefficient of channeled coolant fluid
    h_coolant = k_coolant * Nu / d_H
    # total heat transfer coefficient
    h_tot = 1 / (1 / h_coolant + b / k_chan)

    # number of transfer units and effectiveness
    NTU                     = h_tot * A_chan_module / (m_dot_h_module * cp_coolant)
    eff_WavyChan            = 1 - np.exp(-NTU)

    # log mean temperature
    T_i                     = btms.operating_conditions.wavy_channel_inlet_temperature
    Tw_Ti                   = T_current - T_i
    Tw_To                   = Tw_Ti * np.exp(-NTU)
    dT_lm                   = (Tw_Ti - Tw_To) / np.log(Tw_Ti / Tw_To)

    # convective heat from the battery
    Q_convec                = heat_transfer_efficiency * h_tot * A_chan_module * dT_lm
    Q_convec[Tw_Ti == 0.]   = 0.

    # check the heat generated
    T_o                     = T_current - Tw_To
    Q_conv_check            = m_dot_h_module * cp_coolant * (T_o - T_i)
    delta_Q_conv = np.abs(Q_convec - Q_conv_check) 

    # check the wavy channel effectiveness
    eff_WavyChan_check      = (T_o - T_i) / (T_current - T_i)
    delta_eff_WavyChan      = np.abs(eff_WavyChan - eff_WavyChan_check)

    # net heat stored in the battery
    P_net                   = Q_heat_gen*n_total_module - Q_convec

    # temperature rise [update cell temperature]
    #print( P_net )
    dT_dt                   = P_net/(cell_mass*n_total_module*Cp)
    T_current               = T_current[0] + np.dot(I,dT_dt)
    T_current[T_ambient>T_current] = T_ambient[T_ambient>T_current]

    return T_current, Q_convec, T_o, eff_WavyChan


def compute_net_generated_battery_heat_hex(btms, T_h_1):
    """input parameters"""
    
    
    # cold/hot fluids sides rectangular channel geometries 
    # cold fluid side [air]
    d_H_c                           = btms.heat_exchanger.hydraulic_diameter_of_cold_fluid_channel
    AP_chan_c                       = btms.heat_exchanger.aspect_ratio_of_cold_fluid_channel
    b_c                             = btms.heat_exchanger.fin_height_of_cold_fluid
    beta_c                          = btms.heat_exchanger.area_density_of_cold_fluid
    A_f_by_A_c                      = btms.heat_exchanger.finned_area_by_overall_area_at_cold_fluid
    L_c                             = btms.heat_exchanger.length_of_cold_fluid

    # hot fluid side [liquid]
    d_H_h                           = btms.heat_exchanger.hydraulic_diameter_of_hot_fluid_channel
    AP_chan_h                       = btms.heat_exchanger.aspect_ratio_of_hot_fluid_channel
    b_h                             = btms.heat_exchanger.fin_height_of_hot_fluid
    beta_h                          = btms.heat_exchanger.area_density_of_hot_fluid
    A_f_by_A_h                      = btms.heat_exchanger.finned_area_by_overall_area_at_hot_fluid
    L_h                             = btms.heat_exchanger.length_of_hot_fluid

    # other parameters
    H_stack                         = btms.heat_exchanger.stack_height
    t_w                             = btms.heat_exchanger.t_w
    t_f                             = btms.heat_exchanger.t_f
    k_f                             = btms.heat_exchanger.k_f
    k_w                             = btms.heat_exchanger.k_w

    # cold/hot fluids thermodynamic properties at the inlet sides 
    # cold fluid side
    T_c_1                           = btms.atmosphere_conditions.temperature
    p_c_1                           = btms.atmosphere_conditions.pressure
    m_dot_c                         = btms.heat_exchanger.mass_flow_rate_of_cold_fluid  # kg/s
    
    # hot fluid side
    T_h_1                           = T_h_1                                             # K
    p_h_1                           = btms.heat_exchanger.pressure_at_inlet_of_hot_fluid
    m_dot_h                         = btms.mass_flow_rate_of_hot_fluid                  # kg/s 

    # step-1: surface geometrical properties 
    res1 = compute_surface_geometry_properties(b_c, b_h, beta_h, beta_c, d_H_h, d_H_c, L_c, L_h, H_stack, t_w)

    # step-2: thermo design
    eff_HEX                         = 0.5
    C_R                             = 0.5
    p_c_2                           = p_c_1
    i_index                         = 0
    
    # first estimation
    res2 = compute_offdesign_thermal_properties(btms.atmosphere_conditions, m_dot_h=m_dot_h, m_dot_c=m_dot_c, C_R=C_R, eff_HEX=eff_HEX,
                                                 T_h_1=T_h_1, T_c_1=T_c_1, p_c_2=p_c_2, d_H_h=d_H_h, d_H_c=d_H_c, AP_chan_h=AP_chan_h, AP_chan_c=AP_chan_c,
                                                 k_f=k_f, t_f=t_f, t_w=t_w, k_w=k_w, b_h=b_h, b_c=b_c, A_f_by_A_h=A_f_by_A_h, A_f_by_A_c=A_f_by_A_c,
                                                 L_c=L_c, L_h=L_h, N_p=res1.N_p, A_h=res1.A_h, A_c=res1.A_c, A_o_h=res1.A_o_h, A_o_c=res1.A_o_c)

    res3 = compute_offdesign_pressure_properties(btms.kc_values,btms.ke_values,sigma_h=res1.sigma_h, sigma_c=res1.sigma_c, Re_h=res2.Re_h, Re_c=res2.Re_c,
                                               eta_o_h=res2.eta_o_h, eta_o_c=res2.eta_o_c, h_h=res2.h_h, h_c=res2.h_c,
                                               A_h=res1.A_h, A_c=res1.A_c, f_c=res2.f_c, f_h=res2.f_h, L_h=L_h, L_c=L_c,
                                               d_H_h=d_H_h, d_H_c=d_H_c, G_c=res2.G_c, G_h=res2.G_h,
                                               rho_c_1=res2.rho_c_1, rho_c_2=res2.rho_c_2, rho_c_m=res2.rho_c_m, T_m_c=res2.T_c_m,
                                               rho_h=res2.rho_h, mu_h=res2.mu_h, T_m_h=res2.T_h_m)
 
    # iteration loop until all components satisfied
    while i_index < 4:

        eff_HEX                         = res2.eff_HEX
        C_R                             = res2.C_R
        p_c_2                           = p_c_1 - res3.delta_p_c

        res2 = compute_offdesign_thermal_properties(btms.atmosphere_conditions, m_dot_h=m_dot_h, m_dot_c=m_dot_c, C_R=C_R, eff_HEX=eff_HEX,
                                                 T_h_1=T_h_1, T_c_1=T_c_1, p_c_2=p_c_2, d_H_h=d_H_h, d_H_c=d_H_c, AP_chan_h=AP_chan_h, AP_chan_c=AP_chan_c,
                                                 k_f=k_f, t_f=t_f, t_w=t_w, k_w=k_w, b_h=b_h, b_c=b_c, A_f_by_A_h=A_f_by_A_h, A_f_by_A_c=A_f_by_A_c,
                                                 L_c=L_c, L_h=L_h, N_p=res1.N_p, A_h=res1.A_h, A_c=res1.A_c, A_o_h=res1.A_o_h, A_o_c=res1.A_o_c)

        # iteration loop until all components satisfied
        res3 = compute_offdesign_pressure_properties(btms.kc_values,btms.ke_values,sigma_h=res1.sigma_h, sigma_c=res1.sigma_c, Re_h=res2.Re_h, Re_c=res2.Re_c,
                                                       eta_o_h=res2.eta_o_h, eta_o_c=res2.eta_o_c, h_h=res2.h_h, h_c=res2.h_c,
                                                       A_h=res1.A_h, A_c=res1.A_c, f_c=res2.f_c, f_h=res2.f_h, L_h=L_h, L_c=L_c,
                                                       d_H_h=d_H_h, d_H_c=d_H_c, G_c=res2.G_c, G_h=res2.G_h,
                                                       rho_c_1=res2.rho_c_1, rho_c_2=res2.rho_c_2, rho_c_m=res2.rho_c_m, T_m_c=res2.T_c_m,
                                                       rho_h=res2.rho_h, mu_h=res2.mu_h, T_m_h=res2.T_h_m) 
        i_index += 1

    res4 = compute_offdesign_geometry(H_stack=H_stack, L_c=L_c, m_dot_h=m_dot_h, L_h=L_h, m_dot_c=m_dot_c, sigma_h=res1.sigma_h, sigma_c=res1.sigma_c,
                                                  N_p=res1.N_p, rho_h=res2.rho_h, rho_c_m=res2.rho_c_m, rho_c_2=res2.rho_c_2, rho_c_1=res2.rho_c_1, G_c=res2.G_c,
                                                  delta_p_h=res3.delta_p_h, delta_p_c=res3.delta_p_c) 
    return res1, res2, res3, res4




