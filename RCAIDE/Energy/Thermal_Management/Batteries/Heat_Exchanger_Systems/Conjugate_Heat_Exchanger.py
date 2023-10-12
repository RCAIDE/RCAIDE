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
from RCAIDE.Energy.Energy_Component            import Energy_Component  
from RCAIDE.Attributes.Coolants.Glycol_Water   import Glycol_Water  
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
        
        self.tag                                                                  = 'Conjugate_Heat_Exchanger'
        self.coolant                                                              = Glycol_Water()
        self.wavy_channel                                                         = Energy_Component() 
        self.wavy_channel.cross_section                                           = Data()
        self.heat_exchanger                                                       = Energy_Component() 
        self.heat_transfer_efficiency                                             = 1.0      
          
        # -----setting the default values for the different components
        # wavy channel: thermophysical properties 
        # parameters                                                              values     units
        self.wavy_channel.density                                                  = 2719   # kg/m^3
        self.wavy_channel.thermal_conductivity                                     = 202.4  # W/m.K
        self.wavy_channel.specific_heat_capacity                                   = 871    # J/kg.K
                               
        # wavy channel: geometric properties                       
        self.wavy_channel.cross_section.a                                          = 1e-3   # m
        self.wavy_channel.cross_section.b                                          = 5e-4   # m
        self.wavy_channel.cross_section.c                                          = 6.3e-2 # m
        self.wavy_channel.cross_section.d                                          = 2e-3   # m
        self.wavy_channel.contact_angle                                            = 47.5   # ^o
                       
        # heat exchanger: thermophysical properties                       
        self.heat_exchanger.density                                                = 2780   # kg/m^3
        self.heat_exchanger.thermal_conductivity                                   = 121    # W/m.K
        self.heat_exchanger.specific_heat_capacity                                 = 871    # J/kg.K
                               
        # heat exchanger: geometric properties                       
        # other parameters                       
        self.heat_exchanger.t_w                                                    = 5e-4   # m
        self.heat_exchanger.t_f                                                    = 1e-4   # m
        self.heat_exchanger.k_f                                                    = 121    # W/m.K
        self.heat_exchanger.k_w                                                    = 121    # W/m.K
                       
        self.pump_efficiency                                                       = 0.7
        self.fab_efficiency                                                        = 0.7

        # generic parameters required
        self.wavy_channel.Reynolds_number_of_coolant_in_chan                       = 1.
        self.wavy_channel.velocity_of_coolant_in_chan                              = 1.
        self.wavy_channel.contact_area_of_chan_with_batteries                      = 1.
        self.wavy_channel.hydraulic_diameter_of_chan                               = 1.
        self.wavy_channel.aspect_ratio_of_chan                                     = 1.
        self.wavy_channel.mass_flow_rate_of_one_module                             = 1.
        self.wavy_channel.contact_area_of_one_module                               = 1. 
        self.wavy_channel.mass_of_chan                                             = 1.
        self.wavy_channel.power_of_chan                                            = 1. 
        self.wavy_channel.channel_numbers_of_module                                = 1.
        
        self.heat_exchanger.fin_height_of_hot_fluid                                = 1.
        self.heat_exchanger.fin_height_of_cold_fluid                               = 1.
        self.heat_exchanger.finned_area_by_overall_area_at_hot_fluid               = 1.
        self.heat_exchanger.finned_area_by_overall_area_at_cold_fluid              = 1.
        self.heat_exchanger.area_density_of_hot_fluid                              = 1.
        self.heat_exchanger.area_density_of_cold_fluid                             = 1.
        self.heat_exchanger.number_of_plates                                       = 1.
        self.heat_exchanger.frontal_area_of_hot_fluid                              = 1.
        self.heat_exchanger.frontal_area_of_cold_fluid                             = 1.
        self.heat_exchanger.heat_transfer_area_of_hot_fluid                        = 1.
        self.heat_exchanger.heat_transfer_area_of_cold_fluid                       = 1.
        self.heat_exchanger.minimum_free_flow_area_of_hot_fluid                    = 1.
        self.heat_exchanger.minimum_free_flow_area_of_cold_fluid                   = 1.
        self.heat_exchanger.ratio_of_free_flow_area_to_frontal_area_of_hot_fluid   = 1.
        self.heat_exchanger.ratio_of_free_flow_area_to_frontal_area_of_cold_fluid  = 1. 
        self.heat_exchanger.mass_properties.mass                                   = 1.
        self.heat_exchanger.power_of_hex_fraction_of_hot_fluid                     = 1. 
        self.heat_exchanger.length_of_hot_fluid                                    = 1.
        self.heat_exchanger.length_of_cold_fluid                                   = 1.
        self.heat_exchanger.stack_height                                           = 1.
        self.heat_exchanger.hydraulic_diameter_of_hot_fluid_channel                = 1.
        self.heat_exchanger.aspect_ratio_of_hot_fluid_channel                      = 1.
        self.heat_exchanger.hydraulic_diameter_of_cold_fluid_channel               = 1.
        self.heat_exchanger.aspect_ratio_of_cold_fluid_channel                     = 1. 
                     
        self.heat_exchanger.mass_flow_rate_of_hot_fluid                            = 1.
        self.heat_exchanger.mass_flow_rate_of_cold_fluid                           = 1.
        self.heat_exchanger.pressure_ratio_of_hot_fluid                            = 1.
        self.heat_exchanger.pressure_ratio_of_cold_fluid                           = 1.
        self.heat_exchanger.pressure_at_inlet_of_hot_fluid                         = 1.
        self.heat_exchanger.inlet_temperature_of_hot_fluid                         = 1.

        # operating conditions
        self.operating_conditions = Data()
        self.operating_conditions.wavy_channel_inlet_temperature                   = 288.
        self.operating_conditions.wavy_channel_outlet_temperature                  = 1.
        self.operating_conditions.heat_exchanger_inlet_temperature_of_hot_fluid    = 1.
        self.operating_conditions.heat_exchanger_outlet_temperature_of_hot_fluid   = 1.
        self.operating_conditions.heat_exchanger_inlet_temperature_of_cold_fluid   = 1.
        self.operating_conditions.heat_exchanger_outlet_temperature_of_cold_fluid  = 1.
        self.operating_conditions.heat_extraction_from_battery_to_wavy_channel     = 1.
        self.operating_conditions.heat_dissipation_to_ambient_from_heat_exchanger  = 1.
        self.operating_conditions.heat_exchanger_effectiveness                     = 1.
        self.operating_conditions.wavy_channel_effectiveness                       = 1.
        self.operating_conditions.wavy_channel_power                               = 1.
        self.operating_conditions.heat_exchanger_power                             = 1.
        self.operating_conditions.battery_current_temperature                      = 1.
        
        self.kc_values = load_kc_values()
        self.ke_values = load_ke_values()
        
        return 
    
    def compute_net_generated_battery_heat(self,battery,Q_heat_gen,numerics,freestream): 
        btms_results  = 0 # out off design function 
        return btms_results





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
    
        
