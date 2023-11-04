
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports   
from RCAIDE.Core import Units , Data 
from RCAIDE.Methods.Thermal_Management.Batteries.Design.Conjugate_Heat_Removal.wavy_channel_geometry_setup    import wavy_channel_geometry_setup
from RCAIDE.Methods.Thermal_Management.Batteries.Design.Conjugate_Heat_Removal.wavy_channel_sizing_setup      import wavy_channel_sizing_setup
from RCAIDE.Optimization.Common             import Nexus
from RCAIDE.Optimization.Packages.scipy     import scipy_setup

# python packaged 
import numpy as np   
 
# Python package imports   
import numpy as np  
import time 

# ----------------------------------------------------------------------
#  Rotor Design
# ----------------------------------------------------------------------
## @ingroup Methods-Thermal_Management-Batteries
def design_wavy_channel_heat_removal_system(HRS,battery,single_side_contact=True, dry_mass=True,
                                       solver_name= 'SLSQP',iterations = 200,solver_sense_step = 1E-5,
                                       solver_tolerance = 1E-6,print_iterations = False):  
    """ 
    """ 
    if HRS.coolant_inlet_temperature == None:
        assert('specify coolant inlet temperature')
    elif HRS.design_battery_operating_temperature  == None:
        assert('specify design battery temperature')  
    elif HRS.design_heat_generated == None: 
        assert('specify heat generated') 
    
    # start optimization 
    ti                   = time.time()   
    optimization_problem = wavy_channel_design_problem_setup(HRS,battery,print_iterations)
    output               = scipy_setup.SciPy_Solve(optimization_problem,solver=solver_name, iter = iterations , sense_step = solver_sense_step,tolerance = solver_tolerance)  
    
    tf                   = time.time()
    elapsed_time         = round((tf-ti)/60,2)
    print('Channel Cooling hex Optimization Simulation Time: ' + str(elapsed_time) + ' mins')   
    
    # print optimization results 
    print (output)   
    HRS_opt = optimization_problem.hrs_configurations.optimized.networks.all_electric.busses.bus.batteries.lithium_ion_nmc.thermal_management_system.heat_removal_system
    HRS.mass_properties.mass       = HRS_opt.mass_properties.mass      
    HRS.design_power_draw          = HRS_opt.design_power_draw         
    HRS.design_heat_removed        = HRS_opt.design_heat_removed       
    HRS.coolant_outlet_temperature = HRS_opt.coolant_outlet_temperature
    HRS.coolant_pressure_ratio     = HRS_opt.coolant_pressure_ratio
    HRS.channel_side_thickness     = HRS_opt.channel_side_thickness     
    HRS.channel_width              = HRS_opt.channel_width          
    HRS.coolant_flow_rate          = HRS_opt.coolant_flow_rate  
    HRS.channel_contact_angle      = HRS_opt.channel_contact_angle   
     
    return HRS

## @ingroup Methods-Thermal_Management-Batteries-Sizing
def wavy_channel_design_problem_setup(HRS,battery,print_iterations):  
    
    nexus                        = Nexus()
    problem                      = Data()
    nexus.optimization_problem   = problem 
 
    b_0        = HRS.channel_side_thickness                           
    d_0        = HRS.channel_width          
    m_dot_0    = HRS.coolant_flow_rate  
    theta_0    = HRS.channel_contact_angle       

    # ---------------------------------------------------------------------------------------------------------- 
    # Design Variables 
    # ----------------------------------------------------------------------------------------------------------       
    inputs = []   
    #               variable   initial        upper limit   lower limit          scaling       units 
    inputs.append([ 'm_dot' ,  m_dot_0     ,0.1*m_dot_0    ,10*m_dot_0           , 1.0     ,  1*Units.less])  
    inputs.append([ 'b'     ,  b_0         ,0.5*b_0        , 1.5*b_0             , 1.0     ,  1*Units.less])  
    inputs.append([ 'd'     ,  d_0         ,0.5*d_0        , 1.5*d_0             , 1.0     ,  1*Units.less])  
    inputs.append([ 'theta' ,  theta_0     ,10*Units.degrees, 47.5*Units.degrees , 1.0     ,  1*Units.less])         
    problem.inputs = np.array(inputs,dtype=object)    
    
    # ----------------------------------------------------------------------------------------------------------
    # Objective
    # ---------------------------------------------------------------------------------------------------------- 
    problem.objective = np.array([  
                                 [  'Obj'  ,  10000   ,    1*Units.less] 
    ],dtype=object)
            

    # ----------------------------------------------------------------------------------------------------------
    # Constraints
    # ----------------------------------------------------------------------------------------------------------  
    constraints = []    
    constraints.append([ 'Q_con'         ,  '<'  ,  0.1 ,   1.0   , 1*Units.less])    
    constraints.append([ 'delta_T_con'   ,  '<'  ,  2.  ,   1.0   , 1*Units.less])     
    problem.constraints =  np.array(constraints,dtype=object)                
    
    # ----------------------------------------------------------------------------------------------------------
    #  Aliases
    # ---------------------------------------------------------------------------------------------------------- 
    aliases = [] 
    btms = 'hrs_configurations.optimized.networks.all_electric.busses.bus.batteries.lithium_ion_nmc.thermal_management_system.heat_removal_system'  
    aliases.append([ 'm_dot'       , btms + '.coolant_flow_rate'])    
    aliases.append([ 'b'           , btms + '.channel_side_thickness']) 
    aliases.append([ 'd'           , btms + '.channel_width']) 
    aliases.append([ 'theta'       , btms + '.channel_contact_angle']) 
    aliases.append([ 'Obj'         , 'summary.mass_power_objective' ])  
    aliases.append([ 'Q_con'       , 'summary.heat_energy_constraint'])   
    aliases.append([ 'delta_T_con' , 'summary.temperature_constraint'])      
    problem.aliases = aliases
    
    # -------------------------------------------------------------------
    #  Vehicles
    # ------------------------------------------------------------------- 
    nexus.hrs_configurations = wavy_channel_geometry_setup(HRS,battery)

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
    nexus.procedure         = wavy_channel_sizing_setup()
    
    # -------------------------------------------------------------------
    #  Summary
    # -------------------------------------------------------------------    
    nexus.summary         = Data()     
         
    return nexus