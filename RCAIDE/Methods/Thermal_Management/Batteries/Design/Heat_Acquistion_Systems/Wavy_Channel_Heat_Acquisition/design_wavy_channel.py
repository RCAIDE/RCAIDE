
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports   
from RCAIDE.Core import Units , Data 
from RCAIDE.Methods.Thermal_Management.Batteries.Design.Heat_Acquistion_Systems.Wavy_Channel_Heat_Acquisition.wavy_channel_sizing_setup      import wavy_channel_sizing_setup
from RCAIDE.Methods.Thermal_Management.Batteries.Design.Heat_Acquistion_Systems.Wavy_Channel_Heat_Acquisition.wavy_channel_geometry_setup    import wavy_channel_geometry_setup
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
def design_wavy_channel(HAS,battery,single_side_contact=True, dry_mass=True,
                                       solver_name= 'SLSQP',iterations = 200,solver_sense_step = 1E-6,
                                       solver_tolerance = 1E-5,print_iterations = False):  
    """ 
    """ 
    if HAS.coolant_inlet_temperature == None:
        assert('specify coolant inlet temperature')
    elif HAS.design_battery_operating_temperature  == None:
        assert('specify design battery temperature')  
    elif HAS.design_heat_removed  == None: 
        assert('specify heat generated') 
    
    # start optimization 
    ti                   = time.time()   
    optimization_problem = wavy_channel_design_problem_setup(HAS,battery,print_iterations)
    output               = scipy_setup.SciPy_Solve(optimization_problem,solver=solver_name, iter = iterations , sense_step = solver_sense_step,tolerance = solver_tolerance)  
    
    tf                   = time.time()
    elapsed_time         = round((tf-ti)/60,2)
    print('Channel Cooling hex Optimization Simulation Time: ' + str(elapsed_time) + ' mins')   
    
    # print optimization results 
    print (output)   
    HAS_opt = optimization_problem.hrs_configurations.optimized.networks.all_electric.busses.bus.batteries.lithium_ion_nmc.thermal_management_system.heat_aquisition_system
    HAS.mass_properties.mass       = HAS_opt.mass_properties.mass      
    HAS.design_power_draw          = HAS_opt.design_power_draw         
    HAS.design_heat_removed        = HAS_opt.design_heat_removed       
    HAS.coolant_outlet_temperature = HAS_opt.coolant_outlet_temperature
    HAS.coolant_pressure_drop      = HAS_opt.coolant_pressure_drop
    HAS.channel_side_thickness     = HAS_opt.channel_side_thickness     
    HAS.channel_width              = HAS_opt.channel_width          
    HAS.coolant_flow_rate          = HAS_opt.coolant_flow_rate  
    HAS.channel_contact_angle      = HAS_opt.channel_contact_angle   
     
    return HAS

## @ingroup Methods-Thermal_Management-Batteries-Sizing
def wavy_channel_design_problem_setup(HAS,battery,print_iterations):  
    
    nexus                        = Nexus()
    problem                      = Data()
    nexus.optimization_problem   = problem 
 
    b_0        = HAS.channel_side_thickness                           
    d_0        = HAS.channel_width          
    m_dot_0    = HAS.coolant_flow_rate  
    theta_0    = HAS.channel_contact_angle       

    # ---------------------------------------------------------------------------------------------------------- 
    # Design Variables 
    # ----------------------------------------------------------------------------------------------------------       
    inputs = []   
    #               variable   initial      lower limit      upper limit    scaling       units 
    inputs.append([ 'm_dot' ,  m_dot_0     ,    0.1       ,  10           , 1        ,  1*Units.less])   
    inputs.append([ 'd'     ,  d_0         ,   0.001      ,  0.01         , 1E-3     ,  1*Units.less])  
    inputs.append([ 'theta' ,  theta_0     ,10*Units.degrees, 47.5*Units.degrees , 1.0     ,  1*Units.less])         
    problem.inputs = np.array(inputs,dtype=object)    
    
    # ----------------------------------------------------------------------------------------------------------
    # Objective
    # ---------------------------------------------------------------------------------------------------------- 
    problem.objective = np.array([  
                                 [  'Obj'  ,  10   ,    1*Units.less] 
    ],dtype=object)
            

    # ----------------------------------------------------------------------------------------------------------
    # Constraints
    # ----------------------------------------------------------------------------------------------------------  
    constraints = []    
    constraints.append([ 'Q_con'         ,  '<'  ,  0.1 ,   1.0   , 1*Units.less])     
    problem.constraints =  np.array(constraints,dtype=object)                
    
    # ----------------------------------------------------------------------------------------------------------
    #  Aliases
    # ---------------------------------------------------------------------------------------------------------- 
    aliases = [] 
    btms = 'hrs_configurations.optimized.networks.all_electric.busses.bus.batteries.lithium_ion_nmc.thermal_management_system.heat_aquisition_system'  
    aliases.append([ 'm_dot'       , btms + '.coolant_flow_rate'])    
    aliases.append([ 'b'           , btms + '.channel_side_thickness']) 
    aliases.append([ 'd'           , btms + '.channel_width']) 
    aliases.append([ 'theta'       , btms + '.channel_contact_angle']) 
    aliases.append([ 'Obj'         , 'summary.mass_power_objective' ])  
    aliases.append([ 'Q_con'       , 'summary.heat_energy_constraint'])    
    problem.aliases = aliases
    
    # -------------------------------------------------------------------
    #  Vehicles
    # ------------------------------------------------------------------- 
    nexus.hrs_configurations = wavy_channel_geometry_setup(HAS,battery)

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