## @ingroup Energy-Thermal_Management-Batteries-Heat_Removal_Systems
# RCAIDE/Energy/Thermal_Management/Batteries/Heat_Removal_Systems/Conjugate_Heat_Exchanger.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
import numpy as np 
from RCAIDE.Core import Data 
from RCAIDE.Energy.Energy_Component                            import Energy_Component  
from RCAIDE.Attributes.Coolants.Glycol_Water                   import Glycol_Water  
from RCAIDE.Attributes.Gases                                   import Air
from RCAIDE.Methods.Thermal_Management.Batteries.Performance.Conjugate_Heat_Exchanger  import compute_offdesign_pressure_properties
from RCAIDE.Methods.Thermal_Management.Batteries.Performance.Conjugate_Heat_Exchanger  import compute_offdesign_thermal_properties
from RCAIDE.Methods.Thermal_Management.Batteries.Performance.Conjugate_Heat_Exchanger  import compute_surface_geometry_properties
from RCAIDE.Methods.Thermal_Management.Batteries.Performance.Conjugate_Heat_Exchanger  import compute_offdesign_geometry
 
import os 

# ----------------------------------------------------------------------------------------------------------------------
#  Atmospheric_Air_Convection_Heat_Exchanger
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Energy-Thermal_Management-Batteries-Heat_Removal_Systems   
class Conjugate_Heat_Exchanger(Energy_Component):
    """This provides output values for a wavy channel gas-liquid heat exchanger compoment 
    of a battery thermal management system
    
    Assumptions:
    None
    
    Source:
    N/A
    """
    
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
        None

        Source:
        source: Zhao C, Sousa A C M, Jiang F. Minimization of thermal non-uniformity in lithium-ion battery pack
        cooled by channeled liquid flow[J]. International journal of heat and mass transfer, 2019, 129: 660-670.

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """         
        
        self.tag                                                    = 'Conjugate_Heat_Exchanger'
        self.coolant                                                = Glycol_Water() 
        self.air                                                    = Air() 
                           
        # heat exchanger: thermophysical properties                       
        self.density                                                = 2780   # kg/m^3
        self.thermal_conductivity                                   = 121    # W/m.K
        self.specific_heat_capacity                                 = 871    # J/kg.K
                               
        # heat exchanger: geometric properties                       
        # other parameters                       
        self.t_w                                                    = 5e-4   # m
        self.t_f                                                    = 1e-4   # m
        self.k_f                                                    = 121    # W/m.K
        self.k_w                                                    = 121    # W/m.K
                       
        self.pump_efficiency                                        = 0.7
        self.fab_efficiency                                         = 0.7 
        
        self.fin_height_of_hot_fluid                                = 1.
        self.fin_height_of_cold_fluid                               = 1.
        self.finned_area_by_overall_area_at_hot_fluid               = 1.
        self.finned_area_by_overall_area_at_cold_fluid              = 1.
        self.area_density_of_hot_fluid                              = 1.
        self.area_density_of_cold_fluid                             = 1.
        self.number_of_plates                                       = 1.
        self.frontal_area_of_hot_fluid                              = 1.
        self.frontal_area_of_cold_fluid                             = 1.
        self.heat_transfer_area_of_hot_fluid                        = 1.
        self.heat_transfer_area_of_cold_fluid                       = 1.
        self.minimum_free_flow_area_of_hot_fluid                    = 1.
        self.minimum_free_flow_area_of_cold_fluid                   = 1.
        self.ratio_of_free_flow_area_to_frontal_area_of_hot_fluid   = 1.
        self.ratio_of_free_flow_area_to_frontal_area_of_cold_fluid  = 1. 
        self.mass_properties.mass                                   = 1.
        self.power_of_hex_fraction_of_hot_fluid                     = 1. 
        self.length_of_hot_fluid                                    = 1.
        self.length_of_cold_fluid                                   = 1.
        self.stack_height                                           = 1.
        self.hydraulic_diameter_of_hot_fluid_channel                = 1.
        self.aspect_ratio_of_hot_fluid_channel                      = 1.
        self.air_hydraulic_diameter               = 1.
        self.aspect_ratio_of_cold_fluid_channel                     = 1. 
                     
        self.mass_flow_rate_of_hot_fluid                            = 1.
        self.air_flow_rate                           = 1.
        self.coolant_pressure_ratio                            = 1.
        self.air_pressure_ratio                           = 1.
        self.coolant_inlet_pressure                         = 1.
        self.inlet_temperature_of_hot_fluid                         = 1.

        # operating conditions
        self.operating_conditions = Data() 
        self.operating_conditions.hot_fluid_inlet_temperature   = 1.
        self.operating_conditions.hot_fluid_outlet_temperature   = 1.
        self.operating_conditions.cold_fluid_inlet_temperature   = 1.
        self.operating_conditions.cold_fluid_outlet_temperature   = 1. 
        self.operating_conditions.heat_dissipation_to_ambient  = 1.
        self.effectiveness                     = 1. 
        self.operating_conditions.heat_exchanger_power         = 1. 
        
        self.kc_values = load_kc_values()
        self.ke_values = load_ke_values()
        
        return 
    
    def compute_heat_removed(self,hrs_results,Q_heat_gen,numerics,freestream):  
        """input parameters"""
        
        heat_exchanger = self 
        
        # cold/hot fluids sides rectangular channel geometries 
        # cold fluid side [air]
        d_H_c                           = heat_exchanger.air_hydraulic_diameter
        AP_chan_c                       = heat_exchanger.aspect_ratio_of_cold_fluid_channel
        b_c                             = heat_exchanger.fin_height_of_cold_fluid
        beta_c                          = heat_exchanger.area_density_of_cold_fluid
        A_f_by_A_c                      = heat_exchanger.finned_area_by_overall_area_at_cold_fluid
        L_c                             = heat_exchanger.length_of_cold_fluid
    
        # hot fluid side [liquid]
        d_H_h                           = heat_exchanger.hydraulic_diameter_of_hot_fluid_channel
        AP_chan_h                       = heat_exchanger.aspect_ratio_of_hot_fluid_channel
        b_h                             = heat_exchanger.fin_height_of_hot_fluid
        beta_h                          = heat_exchanger.area_density_of_hot_fluid
        A_f_by_A_h                      = heat_exchanger.finned_area_by_overall_area_at_hot_fluid
        L_h                             = heat_exchanger.length_of_hot_fluid
    
        # other parameters
        H_stack                         = heat_exchanger.stack_height
        t_w                             = heat_exchanger.t_w
        t_f                             = heat_exchanger.t_f
        k_f                             = heat_exchanger.k_f
        k_w                             = heat_exchanger.k_w
    
        # cold/hot fluids thermodynamic properties at the inlet sides 
        # cold fluid side
        T_c_1                           = freestream.temperature
        p_c_1                           = freestream.pressure
        m_dot_c                         = heat_exchanger.air_flow_rate  # kg/s
        
        # hot fluid side
        T_h_1                           = T_h_1                                             # K
        p_h_1                           = heat_exchanger.coolant_inlet_pressure
        m_dot_h                         = heat_exchanger.mass_flow_rate_of_hot_fluid        # kg/s 
    
        # step-1: surface geometrical properties 
        res1 = compute_surface_geometry_properties(b_c, b_h, beta_h, beta_c, d_H_h, d_H_c, L_c, L_h, H_stack, t_w)
    
        # step-2: thermo design
        eff_HEX                         = 0.5
        C_R                             = 0.5
        p_c_2                           = p_c_1
        i_index                         = 0
        
        # first estimation
        res2 = compute_offdesign_thermal_properties(freestream, m_dot_h=m_dot_h, m_dot_c=m_dot_c, C_R=C_R, eff_HEX=eff_HEX,
                                                     T_h_1=T_h_1, T_c_1=T_c_1, p_c_2=p_c_2, d_H_h=d_H_h, d_H_c=d_H_c, AP_chan_h=AP_chan_h, AP_chan_c=AP_chan_c,
                                                     k_f=k_f, t_f=t_f, t_w=t_w, k_w=k_w, b_h=b_h, b_c=b_c, A_f_by_A_h=A_f_by_A_h, A_f_by_A_c=A_f_by_A_c,
                                                     L_c=L_c, L_h=L_h, N_p=res1.N_p, A_h=res1.A_h, A_c=res1.A_c, A_o_h=res1.A_o_h, A_o_c=res1.A_o_c)
    
        res3 = compute_offdesign_pressure_properties(heat_exchanger.kc_values,heat_exchanger.ke_values,sigma_h=res1.sigma_h, sigma_c=res1.sigma_c, Re_h=res2.Re_h, Re_c=res2.Re_c,
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
    
            res2 = compute_offdesign_thermal_properties(freestream, m_dot_h=m_dot_h, m_dot_c=m_dot_c, C_R=C_R, eff_HEX=eff_HEX,
                                                     T_h_1=T_h_1, T_c_1=T_c_1, p_c_2=p_c_2, d_H_h=d_H_h, d_H_c=d_H_c, AP_chan_h=AP_chan_h, AP_chan_c=AP_chan_c,
                                                     k_f=k_f, t_f=t_f, t_w=t_w, k_w=k_w, b_h=b_h, b_c=b_c, A_f_by_A_h=A_f_by_A_h, A_f_by_A_c=A_f_by_A_c,
                                                     L_c=L_c, L_h=L_h, N_p=res1.N_p, A_h=res1.A_h, A_c=res1.A_c, A_o_h=res1.A_o_h, A_o_c=res1.A_o_c)
    
            # iteration loop until all components satisfied
            res3 = compute_offdesign_pressure_properties(heat_exchanger.kc_values,heat_exchanger.ke_values,sigma_h=res1.sigma_h, sigma_c=res1.sigma_c, Re_h=res2.Re_h, Re_c=res2.Re_c,
                                                           eta_o_h=res2.eta_o_h, eta_o_c=res2.eta_o_c, h_h=res2.h_h, h_c=res2.h_c,
                                                           A_h=res1.A_h, A_c=res1.A_c, f_c=res2.f_c, f_h=res2.f_h, L_h=L_h, L_c=L_c,
                                                           d_H_h=d_H_h, d_H_c=d_H_c, G_c=res2.G_c, G_h=res2.G_h,
                                                           rho_c_1=res2.rho_c_1, rho_c_2=res2.rho_c_2, rho_c_m=res2.rho_c_m, T_m_c=res2.T_c_m,
                                                           rho_h=res2.rho_h, mu_h=res2.mu_h, T_m_h=res2.T_h_m) 
            i_index += 1
    
        res4 = compute_offdesign_geometry(H_stack=H_stack, L_c=L_c, m_dot_h=m_dot_h, L_h=L_h, m_dot_c=m_dot_c, sigma_h=res1.sigma_h, sigma_c=res1.sigma_c,
                                                      N_p=res1.N_p, rho_h=res2.rho_h, rho_c_m=res2.rho_c_m, rho_c_2=res2.rho_c_2, rho_c_1=res2.rho_c_1, G_c=res2.G_c,
                                                      delta_p_h=res3.delta_p_h, delta_p_c=res3.delta_p_c) 
        hex_results = Data()
        return   hex_results


def load_kc_values(): 
    ospath    = os.path.abspath(__file__)
    separator = os.path.sep
    rel_path  = os.path.dirname(ospath) + separator   
    x         = np.loadtxt(rel_path + 'rectangular_passage_Kc.csv', dtype=float, delimiter=',', comments='Kc') 
    return x 

def load_ke_values():  
    ospath    = os.path.abspath(__file__)
    separator = os.path.sep
    rel_path  = os.path.dirname(ospath) + separator 
    x         = np.loadtxt(rel_path +'rectangular_passage_Ke.csv', dtype=float, delimiter=',', comments='Ke')
    return x 
    
        
