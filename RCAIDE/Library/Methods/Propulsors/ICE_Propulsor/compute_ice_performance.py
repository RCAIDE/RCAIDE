## @ingroup Methods-Energy-Propulsors-ICE_Propulsor
# RCAIDE/Methods/Energy/Propulsors/ICE_Propulsor/compute_ice_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Framework.Core import Units  
from RCAIDE.Library.Methods.Propulsors.Converters.Engine import compute_power_from_throttle
from RCAIDE.Library.Methods.Propulsors.Converters.Rotor.compute_rotor_performance import  compute_rotor_performance

# pacakge imports  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# compute_ice_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsors-ICE_Propulsor
def compute_ice_performance(propulsor,state,fuel_line,center_of_gravity= [[0.0, 0.0,0.0]]):  
    ''' Computes the perfomrance of one propulsor
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure        [-]  
    fuel_line            - fuelline                                   [-] 
    propulsor        - propulsor data structure               [-] 
    total_thrust         - thrust of propulsor group              [N]
    total_power          - power of propulsor group               [W] 

    Outputs:  
    total_thrust         - thrust of propulsor group              [N]
    total_power          - power of propulsor group               [W] 
    stored_results_flag  - boolean for stored results                 [-]     
    stored_propulsor_tag - name of propulsor with stored results  [-]
    
    Properties Used: 
    N.A.        
    '''  
    conditions              = state.conditions  
    ice_conditions          = conditions.energy[fuel_line.tag][propulsor.tag]
    engine                  = propulsor.engine 
    propeller               = propulsor.propeller
    eta                     = ice_conditions.throttle
    engine_conditions       = ice_conditions[engine.tag]
    RPM                     = engine_conditions.rpm

    # Throttle the engine
    engine_conditions.speed           = RPM * Units.rpm
    engine_conditions.throttle        = eta 
    compute_power_from_throttle(engine,engine_conditions,conditions)        
     
    # Run the propeller to get the power
    propeller_conditions                = ice_conditions[propeller.tag]
    propeller_conditions.omega          = RPM * Units.rpm 
    propeller_conditions.throttle       = engine_conditions.throttle
    compute_rotor_performance(propulsor,state,fuel_line,center_of_gravity)
    
    # Create the outputs
    ice_conditions.fuel_flow_rate            = engine_conditions.fuel_flow_rate  
    stored_results_flag                      = True
    stored_propulsor_tag                     = propulsor.tag 


    # compute total forces and moments from propulsor (future work would be to add moments from motors)
    conditions.energy[fuel_line.tag][propulsor.tag].thrust      = conditions.energy[fuel_line.tag][propulsor.tag][propeller.tag].thrust 
    conditions.energy[fuel_line.tag][propulsor.tag].moment      = conditions.energy[fuel_line.tag][propulsor.tag][propeller.tag].moment
    conditions.energy[fuel_line.tag][propulsor.tag].power       = conditions.energy[fuel_line.tag][propulsor.tag][propeller.tag].power 
    T  = conditions.energy[fuel_line.tag][propulsor.tag].thrust 
    M  = conditions.energy[fuel_line.tag][propulsor.tag].moment 
    P  = conditions.energy[fuel_line.tag][propulsor.tag].power 
    
    return T,M,P,stored_results_flag,stored_propulsor_tag 
    
    
    
def reuse_stored_ice_data(propulsor,state,fuel_line,stored_propulsor_tag,center_of_gravity= [[0.0, 0.0,0.0]]):
    '''Reuses results from one propulsor for identical propulsors
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure        [-]  
    fuel_line            - fuel line                                  [-] 
    propulsor        - propulsor data structure               [-] 
    total_thrust         - thrust of propulsor group              [N]
    total_power          - power of propulsor group               [W] 

    Outputs:  
    total_thrust         - thrust of propulsor group              [N]
    total_power          - power of propulsor group               [W] 
    
    Properties Used: 
    N.A.        
    ''' 


    conditions   = state.conditions 
    engine       = propulsor.engine
    propeller    = propulsor.propeller 
    engine_0     = fuel_line.propulsors[stored_propulsor_tag].engine
    propeller_0  = fuel_line.propulsors[stored_propulsor_tag].propeller  
    
    conditions.energy[fuel_line.tag][propulsor.tag][engine.tag]        = conditions.energy[fuel_line.tag][stored_propulsor_tag][engine_0.tag]
    conditions.energy[fuel_line.tag][propulsor.tag][propeller.tag]        = conditions.energy[fuel_line.tag][stored_propulsor_tag][propeller_0.tag] 
  
    thrust                  = conditions.energy[fuel_line.tag][propulsor.tag][propeller.tag].thrust 
    power                   = conditions.energy[fuel_line.tag][propulsor.tag][propeller.tag].power 
    
    moment_vector           = 0*state.ones_row(3) 
    moment_vector[:,0]      = propeller.origin[0][0]  -  center_of_gravity[0][0] 
    moment_vector[:,1]      = propeller.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2]      = propeller.origin[0][2]  -  center_of_gravity[0][2]
    moment                  =  np.cross(moment_vector, thrust)
    
    conditions.energy[fuel_line.tag][propulsor.tag][propeller.tag].moment = moment  
    conditions.energy[fuel_line.tag][propulsor.tag].thrust            = thrust   
    conditions.energy[fuel_line.tag][propulsor.tag].moment            = moment  
    conditions.energy[fuel_line.tag][propulsor.tag].power             = power
 
    return thrust,moment,power 

            
               