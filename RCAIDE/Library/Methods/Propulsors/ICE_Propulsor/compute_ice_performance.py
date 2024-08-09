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
def compute_ice_performance(ice_propeller,state,fuel_line,center_of_gravity= [[0.0, 0.0,0.0]]):  
    ''' Computes the perfomrance of one ice_propeller
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure        [-]  
    fuel_line            - fuelline                                   [-] 
    ice_propeller        - ice_propeller data structure               [-] 
    total_thrust         - thrust of ice_propeller group              [N]
    total_power          - power of ice_propeller group               [W] 

    Outputs:  
    total_thrust         - thrust of ice_propeller group              [N]
    total_power          - power of ice_propeller group               [W] 
    stored_results_flag  - boolean for stored results                 [-]     
    stored_propulsor_tag - name of ice_propeller with stored results  [-]
    
    Properties Used: 
    N.A.        
    '''  
    conditions              = state.conditions  
    ice_conditions          = conditions.energy[fuel_line.tag][ice_propeller.tag]
    noise_conditions        = conditions.noise[fuel_line.tag][ice_propeller.tag] 
    engine                  = ice_propeller.engine 
    propeller               = ice_propeller.propeller
    eta                     = ice_conditions.throttle  
    RPM                     = ice_conditions.engine.rpm

    # Throttle the engine
    ice_conditions.engine.inputs.speed    = RPM * Units.rpm
    ice_conditions.engine.throttle        = eta 
    compute_power_from_throttle(engine,ice_conditions,conditions)    
    torque                                = ice_conditions.engine.torque     
     
    # Run the propeller to get the power
    propeller_conditions                = ice_conditions[propeller.tag]
    propeller_conditions.omega          = RPM * Units.rpm 
    F,M,Q,P,Cp,etap                     = compute_rotor_performance(ice_propeller,state,fuel_line,center_of_gravity)  

    # Check to see if magic thrust is needed, the ESC caps throttle at 1.1 already
    P[eta>1.0]          = P[eta>1.0]*eta[eta>1.0]
    F[eta[:,0]>1.0,:]   = F[eta[:,0]>1.0,:]*eta[eta[:,0]>1.0,:]

    # Determine Conditions specific to this instantation of engine and rotors
    R                   = propeller.tip_radius
    rpm                 = ice_conditions.engine.inputs.speed / Units.rpm 
    F_mag               = np.atleast_2d(np.linalg.norm(F, axis=1)).T  

    # Create the outputs 
    ice_conditions.fuel_flow_rate            = ice_conditions.engine.outputs.fuel_flow_rate  
    ice_conditions.engine.power              = P 
    ice_conditions.engine.torque             = torque
    ice_conditions.throttle                  = eta 
    ice_conditions.rotor.torque              = Q
    ice_conditions.rotor.thrust              = F
    ice_conditions.rotor.rpm                 = rpm
    ice_conditions.rotor.tip_mach            = (R*rpm*Units.rpm)/conditions.freestream.speed_of_sound    
    ice_conditions.rotor.disc_loading        = (F_mag)/(np.pi*(R**2))             
    ice_conditions.rotor.power_loading       = (F_mag)/(P)    
    ice_conditions.rotor.efficiency          = etap
    ice_conditions.rotor.figure_of_merit     = outputs.figure_of_merit
    noise_conditions.rotor                   = outputs
    power                                    = P
    thrust                                   = F  
    stored_results_flag                      = True
    stored_propulsor_tag                     = ice_propeller.tag
    
    # Compute forces and moments
    moment_vector      = 0*state.ones_row(3)
    F                  = 0*state.ones_row(3)
    F[:,0]             = ice_conditions.thrust[:,0]
    moment_vector[:,0] = ice_propeller.origin[0][0] -   center_of_gravity[0][0] 
    moment_vector[:,1] = ice_propeller.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2] = ice_propeller.origin[0][2]  -  center_of_gravity[0][2]
    M                  = np.cross(moment_vector, F)   
    moment             = M 
    
    return thrust,moment,power,stored_results_flag,stored_propulsor_tag 
    
    
    
def reuse_stored_ice_data(ice_propeller,state,fuel_line,stored_propulsor_tag,center_of_gravity= [[0.0, 0.0,0.0]]):
    '''Reuses results from one ice_propeller for identical propulsors
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure        [-]  
    fuel_line            - fuel line                                  [-] 
    ice_propeller        - ice_propeller data structure               [-] 
    total_thrust         - thrust of ice_propeller group              [N]
    total_power          - power of ice_propeller group               [W] 

    Outputs:  
    total_thrust         - thrust of ice_propeller group              [N]
    total_power          - power of ice_propeller group               [W] 
    
    Properties Used: 
    N.A.        
    ''' 
    conditions                                          = state.conditions  
    ice_conditions_0                                    = conditions.energy[fuel_line.tag][stored_propulsor_tag]
    noise_conditions_0                                  = conditions.noise[fuel_line.tag][stored_propulsor_tag]   
    conditions.energy[fuel_line.tag][ice_propeller.tag] = ice_conditions_0
    conditions.noise[fuel_line.tag][ice_propeller.tag]  = noise_conditions_0
    
    # compute moment  
    moment_vector      = 0*state.ones_row(3)
    F                  = 0*state.ones_row(3)
    F[:,0]             = ice_conditions_0.thrust[:,0] 
    moment_vector[:,0] = ice_propeller.origin[0][0] -   center_of_gravity[0][0] 
    moment_vector[:,1] = ice_propeller.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2] = ice_propeller.origin[0][2]  -  center_of_gravity[0][2]
    moment             = np.cross(moment_vector, F) 
     
    power   = conditions.energy[fuel_line.tag][ice_propeller.tag].engine.power
    thrust  = conditions.energy[fuel_line.tag][ice_propeller.tag].rotor.thrust 
 
    return thrust,moment,power 

            
               