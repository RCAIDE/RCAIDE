## @ingroup Methods-Thermal_Management-Batteries
# design_wavy_channel_heat_exchanger.py  

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------    
from RCAIDE.Core                            import Units, Data   
from RCAIDE.Methods.Thermal_Management.Batteries.Design.Heat_Exchanger_Systems.Cross_Flow_Heat_Exchanger.cross_flow_heat_exchanger_sizing_setup import cross_flow_heat_exchanger_sizing_setup 
from RCAIDE.Methods.Thermal_Management.Batteries.Design.Heat_Exchanger_Systems.Cross_Flow_Heat_Exchanger.cross_flow_heat_exchanger_geometry_setup import cross_flow_heat_exchanger_geometry_setup
from RCAIDE.Optimization.Common             import Nexus
from RCAIDE.Optimization.Packages.scipy     import scipy_setup

# Python package imports   
import numpy as np  
import time 

# ----------------------------------------------------------------------
#  Rotor Design
# ----------------------------------------------------------------------
## @ingroup Methods-Thermal_Management-Batteries
def design_cross_flow_heat_exchanger(HEX,HAS,battery, single_side_contact=True, dry_mass=True,
                                       solver_name= 'SLSQP',iterations = 200,solver_sense_step = 1E-5,
                                       solver_tolerance = 1E-6,print_iterations = False):  
    """ 
    """    
    
    
    # start optimization 
    ti                   = time.time()   
    optimization_problem = crossflow__heat_exchanger_design_problem_setup(HEX,HAS,print_iterations)
    output               = scipy_setup.SciPy_Solve(optimization_problem,solver=solver_name, iter = iterations , sense_step = solver_sense_step,tolerance = solver_tolerance)  
    
    tf                   = time.time()
    elapsed_time         = round((tf-ti)/60,2)
    print('HEX sizing optimization Simulation Time: ' + str(elapsed_time) + ' mins')   
    
    # print optimization results 
    print (output)  
     
    return HEX

## @ingroup Methods-Thermal_Management-Batteries-Sizing
def crossflow__heat_exchanger_design_problem_setup(HEX,HAS,print_iterations): 
    """"""
    
    nexus                        = Nexus()
    problem                      = Data()
    nexus.optimization_problem   = problem    
    
    
    # ---------------------------------------------------------------------------------------------------------- 
    # Design Variables 
    # ----------------------------------------------------------------------------------------------------------       
    inputs = []   
    #               variable   initial   lower limit   upper limit     scaling       units 
    inputs.append([ 'p_c_1'   ,   1     ,   0.001    , 1000000       , 1         ,  1*Units.less])
    inputs.append([ 'p_h_1'   ,   1     ,   0.001    , 1000000       , 1         ,  1*Units.less]) 
    inputs.append([ 'm_dot_c' ,   1     ,  0.1       , 100           , 1.0       ,  1*Units.less])  
   
        
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
    constraints.append([ 'L'         ,  '<'  ,  2.0 ,   1.0   , 1*Units.less])
    constraints.append([ 'W'         ,  '<'  ,  2.0 ,   1.0   , 1*Units.less])  
    constraints.append([ 'H'         ,  '<'  ,  2.0 ,   1.0   , 1*Units.less]) 
    problem.constraints =  np.array(constraints,dtype=object)                
    
    # -------------------------------------------------------------------
    #  Aliases
    # ------------------------------------------------------------------- 
    aliases = [] 
    btms = 'hex_configurations.optimized.networks.all_electric.busses.bus.batteries.lithium_ion_nmc.thermal_management_system.heat_exchanger'  
    aliases.append([ 'm_dot_c'     , btms + '.air_flow_rate' ])        
    aliases.append([ 'p_c_1'       , btms + '.air_inlet_pressure' ])       
    aliases.append([ 'p_h_1'       , btms + '.coolant_inlet_pressure' ])   
    aliases.append([ 'L'     , 'summary.stack_length' ])     
    aliases.append([ 'W'     , 'summary.stack_width' ])   
    aliases.append([ 'H'     , 'summary.stack_height' ])     
    aliases.append([ 'P_hex'   , 'summary.heat_exchanger_power' ])   
    problem.aliases = aliases
    
    # -------------------------------------------------------------------
    #  Vehicles
    # ------------------------------------------------------------------- 
    nexus.hex_configurations = cross_flow_heat_exchanger_geometry_setup(HEX,HAS)

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
    nexus.procedure         = cross_flow_heat_exchanger_sizing_setup()
    
    # -------------------------------------------------------------------
    #  Summary
    # -------------------------------------------------------------------    
    nexus.summary         = Data()     
         
    return nexus   