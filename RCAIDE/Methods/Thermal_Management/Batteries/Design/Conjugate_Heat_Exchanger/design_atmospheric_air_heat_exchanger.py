## @ingroup Methods-Thermal_Management-Batteries
# design_wavy_channel_heat_exchanger.py  

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------    
from RCAIDE.Core                            import Units, Data   
from RCAIDE.Methods.Thermal_Management.Batteries.Design.Conjugate_Heat_Exchanger.atmospheric_air_HEX_geometry_setup    import atmospheric_air_HEX_geometry_setup
from RCAIDE.Methods.Thermal_Management.Batteries.Design.Conjugate_Heat_Exchanger.atmospheric_air_HEX_sizing_setup      import atmospheric_air_HEX_sizing_setup  
from RCAIDE.Optimization.Common             import Nexus
from RCAIDE.Optimization.Packages.scipy     import scipy_setup

# Python package imports   
import numpy as np  
import time 

# ----------------------------------------------------------------------
#  Rotor Design
# ----------------------------------------------------------------------
## @ingroup Methods-Thermal_Management-Batteries
def design_atmospheric_air_heat_exchanger(HEX,HRS,battery, single_side_contact=True, dry_mass=True,
                                       solver_name= 'SLSQP',iterations = 200,solver_sense_step = 1E-5,
                                       solver_tolerance = 1E-6,print_iterations = False):  
    """ 
    """    
    # Unpack rotor geometry   
    
    # start optimization 
    ti                   = time.time()   
    optimization_problem = atmospheric_air_heat_exchanger_design_problem_setup(HEX,HRS,print_iterations)
    output               = scipy_setup.SciPy_Solve(optimization_problem,solver=solver_name, iter = iterations , sense_step = solver_sense_step,tolerance = solver_tolerance)  
    
    tf                   = time.time()
    elapsed_time         = round((tf-ti)/60,2)
    print('Channel Cooling hex Optimization Simulation Time: ' + str(elapsed_time) + ' mins')   
    
    # print optimization results 
    print (output)  
     
    return HEX

## @ingroup Methods-Thermal_Management-Batteries-Sizing
def atmospheric_air_heat_exchanger_design_problem_setup(HEX,HRS,print_iterations): 
    """"""
    
    nexus                        = Nexus()
    problem                      = Data()
    nexus.optimization_problem   = problem    
    
    
    # ---------------------------------------------------------------------------------------------------------- 
    # Design Variables 
    # ----------------------------------------------------------------------------------------------------------       
    inputs = []   
    #               variable   initial   upper limit   lower limit     scaling       units 
    inputs.append([ 'd_H_c'   ,  10    , 1               , 15            , 10      ,  1*Units.less])  
    inputs.append([ 'd_H_h'   ,  10    , 1               , 15            , 10      ,  1*Units.less]) 
    inputs.append([ 'gamma_c' ,  3     , 0.1             , 10            , 10      ,  1*Units.less])  
    inputs.append([ 'gamma_h' ,  3     , 0.1             , 10            , 10      ,  1*Units.less])  
    inputs.append([ 'm_dot_c' ,  1     , 0.1             , 3             , 1.0     ,  1*Units.less])  
    inputs.append([ 'PI_c'    ,  0.8   , 0.75            , 0.98          , 1.0     ,  1*Units.less])   
    inputs.append([ 'p_c_1'   ,  1     , 0.1             , 10            , 10      ,  1*Units.less])   
    inputs.append([ 'C_R'     ,  0.5   , 0.2             , 0.8           , 1.0     ,  1*Units.less])       
    problem.inputs = np.array(inputs,dtype=object)   

    # ----------------------------------------------------------------------------------------------------------
    # Objective
    # ---------------------------------------------------------------------------------------------------------- 
    problem.objective = np.array([  
                                 [  'P_hex'  ,  1.0   ,    1*Units.less] 
    ],dtype=object)
            

    # ----------------------------------------------------------------------------------------------------------
    # Constraints
    # ----------------------------------------------------------------------------------------------------------  
    constraints = []    
    #constraints.append([ 'L_h_con'         ,  '<'  ,  1.7 ,   1.0   , 1*Units.less])    # not sure of the constraints yet 
    #constraints.append([ 'L_c_con'         ,  '<'  ,  1.0 ,   1.0   , 1*Units.less])   
    #constraints.append([ 'H_con'           ,  '<'  ,  0.2 ,   1.0   , 1*Units.less])  
    #constraints.append([ 'm_hex_con'       ,  '>'  ,  0.0 ,   1.0   , 1*Units.less])  
    #constraints.append([ 'N_p_con'         ,  '>'  ,  1.0 ,   1.0   , 1*Units.less])   
    problem.constraints =  np.array(constraints,dtype=object)                
    
    # -------------------------------------------------------------------
    #  Aliases
    # ------------------------------------------------------------------- 
    aliases = [] 
    btms = 'hex_configurations.optimized.networks.all_electric.busses.bus.batteries.lithium_ion_nmc.thermal_management_system.heat_exchanger'  
    aliases.append([ 'd_H_c'       , btms + '.air_hydraulic_diameter'])   
    aliases.append([ 'd_H_h'       , btms + '.coolant_hydraulic_diameter'])   
    aliases.append([ 'gamma_h'     , btms + '.coolant_channel_aspect_ratio' ])  
    aliases.append([ 'gamma_c'     , btms + '.air_channel_aspect_ratio' ])    
    aliases.append([ 'm_dot_c'     , btms + '.air_flow_rate' ])       
    aliases.append([ 'C_R'         , btms + '.heat_capacity_rato' ])    
    aliases.append([ 'PI_c'        , btms + '.air_pressure_ratio' ])     
    aliases.append([ 'p_c_1'       , btms + '.air_inlet_pressure' ])  
    #aliases.append([ 'L_h_con'     , 'summary.length_of_hot_fluid_constraint'])   
    #aliases.append([ 'L_c_con'     , 'summary.length_of_cold_fluid_constraint'])   
    #aliases.append([ 'H_con'       , 'summary.stack_height_constraint' ])     
    #aliases.append([ 'm_hex_con'   , 'summary.hex_mass_constraint'])    
    #aliases.append([ 'N_p_con'     , 'summary.number_of_passes_constraint' ])   
    aliases.append([ 'P_hex'   , 'summary.heat_exchanger_power' ])   
    problem.aliases = aliases
    
    # -------------------------------------------------------------------
    #  Vehicles
    # ------------------------------------------------------------------- 
    nexus.hex_configurations = atmospheric_air_HEX_geometry_setup(HEX,HRS)

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
    nexus.procedure         = atmospheric_air_HEX_sizing_setup()
    
    # -------------------------------------------------------------------
    #  Summary
    # -------------------------------------------------------------------    
    nexus.summary         = Data()     
         
    return nexus   