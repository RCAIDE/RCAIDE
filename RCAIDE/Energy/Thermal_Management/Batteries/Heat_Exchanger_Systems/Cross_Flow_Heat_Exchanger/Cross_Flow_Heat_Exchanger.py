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
from RCAIDE.Methods.Thermal_Management.Batteries.Design.Heat_Exchanger_Systems.Cross_Flow_Heat_Exchanger.compute_heat_exhanger_factors  import compute_heat_exhanger_factors

 
import os 

# ----------------------------------------------------------------------------------------------------------------------
#  Atmospheric_Air_Convection_Heat_Exchanger
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Energy-Thermal_Management-Batteries-Heat_Removal_Systems   
class Cross_Flow_Heat_Exchanger(Energy_Component):
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
        Surface Designation of 1/8-19.86 with strip fins. 

        Source:
        Kays, W.M. and London, A.L. (1998) Compact Heat Exchangers. 3rd Edition, McGraw-Hill, New York.
        """         
        
        self.tag                                                    = 'Cross_flow_Heat_Exchanger'
        self.coolant                                                = Glycol_Water() 
        self.air                                                    = Air() 
                           
        # heat exchanger: thermophysical properties                       
        
        self.heat_exchanger_efficiency                              = 0.8381
        self.density                                                = 8440   # kg/m^3
        self.thermal_conductivity                                   = 121    # W/m.K
        self.specific_heat_capacity                                 = 871    # J/kg.K 
        
        
        # heat exchanger: geometric properties     
        
        # Plate thickness                       
        self.t_w                                                    = 5e-4   # m
        
        # Fin Thickness
        self.t_f                                                    = 1e-4   # m
                       
        self.fin_spacing_cold                                       = 2.54e-3 #m
        self.fin_spacing_hot                                        = 2.54e-3 #m
        
         # Fin metal thickness
        self.fin_metal_thickness_hot                                = 0.102e-3 #m
        self.fin_metal_thickness_cold                               = 0.102e-3 #m
        
        # Strip edge exposed 
        self.fin_exposed_strip_edge_hot                             = 3.175e-3 #m
        self.fin_exposed_strip_edge_cold                            = 3.175e-3 #m
        
        #Finned area density 
        self.fin_area_density_hot                                   = 2254 #m^2/m^3 
        self.fin_area_density_cold                                  = 2254 #m^2/m^3 
        
        # Ratio of finned area to total area 
        self.finned_area_to_total_area_hot                          = 0.785
        self.finned_area_to_total_area_cold                         = 0.785
        
        #Hydraullic Diameter
        self.coolant_hydraulic_diameter                             = 1.54e-3  #m
        self.air_hydraulic_diameter                                 = 1.54e-3  #m
        
        #Fin and wall Conductivity 
        self.k_f                                                    = 121    # W/m.K
        self.k_w                                                    = 121    # W/m.K        
        
        #Efficiency 
        self.pump_efficiency                                        = 0.7
        self.fan_efficiency                                         = 0.7 
        
        
        # Operating Conditions
        
        # Limiting Pressure Drop
        self.pressure_drop_hot                                      = 9.05e3 #Pa 
        self.pressure_drop_cold                                     = 8.79e3 #Pa 
        
        
        # Enterance and Exit pressure loss coefficients  
        self.kc_values                                             = load_kc_values()
        self.ke_values                                             = load_ke_values()
        
        return 
    

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
    
        
