## @ingroup Library-Methods-Energy-Propulsors-Common 
# RCAIDE/Library/Methods/Energy/Propulsors/Common/compute_static_sea_level_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE Imports
import RCAIDE  

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Design Turbofan
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Energy-Propulsors-Common
def compute_static_sea_level_performance(propulsor):
    """Compute static sea level performance of a propulsor     
    
    Assumtions:
       None 
    
    Source:
        None 
    
    Args:
        propulsor (dict): propulsor data structure [-]
    
    Returns:
        None 
    
    """  
    # Step 28: Static Sea Level Thrust  
    planet     = RCAIDE.Library.Attributes.Planets.Earth()
    atmosphere_sls = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmo_data      = atmosphere_sls.compute_values(0.0,0.0)
    
    p   = atmo_data.pressure          
    T   = atmo_data.temperature       
    rho = atmo_data.density          
    a   = atmo_data.speed_of_sound    
    mu  = atmo_data.dynamic_viscosity     

    # setup conditions 
    fuel_line                               = RCAIDE.Library.Components.Energy.Distribution.Fuel_Line()    
    fuel_tank                               = RCAIDE.Library.Components.Energy.Fuel_Tanks.Fuel_Tank()  
    fuel                                    = RCAIDE.Library.Attributes.Propellants.Aviation_Gasoline()    
    fuel_tank.fuel                          = fuel  
    fuel_line.fuel_tanks.append(fuel_tank)  
    fuel_line.propulsors.append(propulsor)  
        
    sls_conditions = RCAIDE.Framework.Mission.Common.Results()

    # freestream conditions    
    sls_conditions.freestream.altitude                    = np.atleast_1d(0)
    sls_conditions.freestream.mach_number                 = np.atleast_1d(0.01)
    sls_conditions.freestream.pressure                    = np.atleast_1d(p)
    sls_conditions.freestream.temperature                 = np.atleast_1d(T)
    sls_conditions.freestream.density                     = np.atleast_1d(rho)
    sls_conditions.freestream.dynamic_viscosity           = np.atleast_1d(mu)
    sls_conditions.freestream.gravity                     = np.atleast_2d(planet.sea_level_gravity)
    sls_conditions.freestream.isentropic_expansion_factor = np.atleast_1d(propulsor.working_fluid.compute_gamma(T,p))
    sls_conditions.freestream.Cp                          = np.atleast_1d(propulsor.working_fluid.compute_cp(T,p))
    sls_conditions.freestream.R                           = np.atleast_1d(propulsor.working_fluid.gas_specific_constant)
    sls_conditions.freestream.speed_of_sound              = np.atleast_1d(a)
    sls_conditions.freestream.velocity                    = np.atleast_1d(a*0.01)   

    # initialize data structure for propulsor operating conditions (for energy ) 
    sls_conditions.energy[fuel_line.tag]                                  = RCAIDE.Framework.Mission.Common.Conditions()  
    sls_conditions.energy[fuel_line.tag][fuel_tank.tag]                   = RCAIDE.Framework.Mission.Common.Conditions()  
    sls_conditions.energy[fuel_line.tag][fuel_tank.tag].mass_flow_rate    = np.zeros((1,1))     
    sls_conditions.energy[fuel_line.tag][fuel_tank.tag].mass              = np.zeros((1,1))   
    sls_conditions.energy[fuel_line.tag][propulsor.tag]                    = RCAIDE.Framework.Mission.Common.Conditions() 
    sls_conditions.energy[fuel_line.tag][propulsor.tag].throttle           = np.array([[1.0]])
    sls_conditions.energy[fuel_line.tag][propulsor.tag].y_axis_rotation    = np.zeros((1,1)) 
    sls_conditions.energy[fuel_line.tag][propulsor.tag].thrust             = np.zeros((1,1))
    sls_conditions.energy[fuel_line.tag][propulsor.tag].power              = np.zeros((1,1))
    

    # initialize data structure for propulsor operating conditions (for noise )       
    sls_conditions.noise[fuel_line.tag]                                 = RCAIDE.Framework.Mission.Common.Conditions()              
    sls_conditions.noise[fuel_line.tag][propulsor.tag]                  = RCAIDE.Framework.Mission.Common.Conditions() 
    
    total_power     = np.zeros((3,1))
    total_thrust    = np.zeros((1,1))
    
    if type(propulsor) == RCAIDE.Library.Components.Propulsors.Turbofan:
        sls_conditions.noise[fuel_line.tag][propulsor.tag].turbofan         = RCAIDE.Framework.Mission.Common.Conditions()
        RCAIDE.Library.Methods.Energy.Propulsors.Turbofan_Propulsor.compute_performance(sls_conditions,fuel_line,propulsor,total_thrust,total_power)
        
    propulsor.sealevel_static_thrust = propulsor.outputs.thrust 
    return 