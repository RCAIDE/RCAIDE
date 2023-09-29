## @ingroup Methods-Thermal_Management-Batteries-Sizing
# btms_sizing_setup.py 
#
# Created: Jun 2023, M. Clarke

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------  
# MARC Imports    
from MARC.Components.Energy.Thermal_Management.Batteries.Channel_Cooling.Wavy_Channel_Gas_Liquid_Heat_Exchanger                       import Wavy_Channel_Gas_Liquid_Heat_Exchanger 
from MARC.Components.Energy.Thermal_Management.Batteries.Atmospheric_Air_Convection_Cooling.Atmospheric_Air_Convection_Heat_Exchanger import Atmospheric_Air_Convection_Heat_Exchanger 

from MARC.Core                                                             import Units, Data   
from MARC.Optimization                                                     import Nexus   
from MARC.Methods.Thermal_Management.Batteries.Sizing.btms_geometry_setup  import air_convection_cooling_geometry_setup
from MARC.Methods.Thermal_Management.Batteries.Sizing.btms_geometry_setup  import channel_cooling_geometry_setup
from MARC.Methods.Thermal_Management.Batteries.Sizing.btms_procedure_setup import air_convection_cooling_procedure_setup
from MARC.Methods.Thermal_Management.Batteries.Sizing.btms_procedure_setup import channel_cooling_procedure_setup

# Python package imports   
import numpy as np  

## @ingroup Methods-Thermal_Management-Batteries-Sizing
def btms_sizing_setup(battery,print_iterations): 
    """"""
    
    nexus                        = Nexus()
    problem                      = Data()
    nexus.optimization_problem   = problem 
    
    if type(battery.thermal_management_system) == Wavy_Channel_Gas_Liquid_Heat_Exchanger:   
        inputs = []  
        inputs.append([ 'd_H_h'   ,  10    , 1   , 15    , 10      ,  1*Units.less]) 
        inputs.append([ 'd_H_c'   ,  10    , 1   , 15    , 10      ,  1*Units.less]) 
        inputs.append([ 'gamma_h' ,  3    , 0.1  , 10    , 10      ,  1*Units.less]) 
        inputs.append([ 'gamma_c' ,  3    , 0.1  , 10    , 10      ,  1*Units.less]) 
        inputs.append([ 'm_dot_h' ,  1    , 0.1  , 3     , 1.0     ,  1*Units.less]) 
        inputs.append([ 'm_dot_c' ,  1    , 0.1  , 3     , 1.0     ,  1*Units.less]) 
        inputs.append([ 'PI_h'    ,  0.8  , 0.75 , 0.98  , 1.0     ,  1*Units.less])
        inputs.append([ 'PI_c'    ,  0.8  , 0.75 , 0.98  , 1.0     ,  1*Units.less])  
        inputs.append([ 'p_h_1'   ,  1    , 0.1  , 10    , 10      ,  1*Units.less])  
        inputs.append([ 'p_c_1'   ,  1    , 0.1  , 10    , 10      ,  1*Units.less])   
        inputs.append([ 'C_R'     ,  0.5  , 0.2  , 0.8   , 1.0     ,  1*Units.less])       
        problem.inputs = np.array(inputs,dtype=object)   
    
    
        # -------------------------------------------------------------------
        # Objective
        # ------------------------------------------------------------------- 
        problem.objective = np.array([  
                                     [  'objective'  ,  1.0   ,    1*Units.less] 
        ],dtype=object)
                
    
        # -------------------------------------------------------------------
        # Constraints
        # -------------------------------------------------------------------  
        constraints = []    
        constraints.append([ 'L_h_con'         ,  '<'  ,  1.7 ,   1.0   , 1*Units.less])    
        constraints.append([ 'L_c_con'         ,  '<'  ,  1.0 ,   1.0   , 1*Units.less])   
        constraints.append([ 'H_con'           ,  '<'  ,  0.2 ,   1.0   , 1*Units.less])  
        constraints.append([ 'm_hex_con'       ,  '>'  ,  0.0 ,   1.0   , 1*Units.less])  
        constraints.append([ 'N_p_con'         ,  '>'  ,  1.0 ,   1.0   , 1*Units.less])  
        constraints.append([ 'P_hex_con'       ,  '>'  ,  0.0 ,   1.0   , 1*Units.less])     
        problem.constraints =  np.array(constraints,dtype=object)                
        
        # -------------------------------------------------------------------
        #  Aliases
        # ------------------------------------------------------------------- 
        aliases = [] 
        aliases.append([ 'd_H_h'       , 'btms_configurations.networks.battery.thermal_management_system.heat_exchanger.hydraulic_diameter_of_hot_fluid_channel'])   
        aliases.append([ 'gamma_h'     , 'btms_configurations.networks.battery.thermal_management_system.heat_exchanger.aspect_ratio_of_hot_fluid_channel' ])   
        aliases.append([ 'd_H_c'       , 'btms_configurations.networks.battery.thermal_management_system.heat_exchanger.hydraulic_diameter_of_cold_fluid_channel'])   
        aliases.append([ 'gamma_c'     , 'btms_configurations.networks.battery.thermal_management_system.heat_exchanger.aspect_ratio_of_cold_fluid_channel' ])   
        aliases.append([ 'm_dot_h'     , 'btms_configurations.networks.battery.thermal_management_system.heat_exchanger.mass_flow_rate_of_hot_fluid' ])   
        aliases.append([ 'm_dot_c'     , 'btms_configurations.networks.battery.thermal_management_system.heat_exchanger.mass_flow_rate_of_cold_fluid' ])   
        aliases.append([ 'PI_c'        , 'btms_configurations.networks.battery.thermal_management_system.heat_exchanger.pressure_ratio_of_hot_fluid' ])   
        aliases.append([ 'PI_h'        , 'btms_configurations.networks.battery.thermal_management_system.heat_exchanger.pressure_ratio_of_cold_fluid' ])   
        aliases.append([ 'p_h_1'       , 'btms_configurations.networks.battery.thermal_management_system.heat_exchanger.pressure_at_inlet_of_hot_fluid' ])   
        aliases.append([ 'p_c_1'       , 'btms_configurations.networks.battery.thermal_management_system.heat_exchanger.pressure_at_inlet_of_cold_fluid' ])  
        aliases.append([ 'L_h_con'     , 'summary.length_of_hot_fluid_constraint'])   
        aliases.append([ 'L_c_con'     , 'summary.length_of_cold_fluid_constraint'])   
        aliases.append([ 'H_con'       , 'summary.stack_height_constraint' ])     
        aliases.append([ 'm_hex_con'   , 'summary.hex_mass_constraint'])    
        aliases.append([ 'N_p_con'     , 'summary.number_of_passes_constraint' ])   
        aliases.append([ 'P_hex_con'   , 'summary.heat_exchanger_power_draw_constraint' ])   
        problem.aliases = aliases
        
        # -------------------------------------------------------------------
        #  Vehicles
        # ------------------------------------------------------------------- 
        nexus.btms_configurations = air_convection_cooling_geometry_setup(battery)
    
        # -------------------------------------------------------------------
        #  Analyses
        # -------------------------------------------------------------------
        nexus.analyses = None 
        
        # -------------------------------------------------------------------
        #  Missions
        # -------------------------------------------------------------------
        nexus.missions = None
        
        # -------------------------------------------------------------------
        #  Procedure
        # -------------------------------------------------------------------    
        nexus.print_iterations  = print_iterations 
        nexus.procedure         = channel_cooling_procedure_setup()
        
        # -------------------------------------------------------------------
        #  Summary
        # -------------------------------------------------------------------    
        nexus.summary         = Data()     
        
        
    elif type(battery.thermal_management_system) == Atmospheric_Air_Convection_Heat_Exchanger:   
        pass 
    return nexus   