## @ingroup Methods-Energy-Propulsion-Networks
# RCAIDE/Methods/Energy/Propulsion/Networks/internal_combustion_engine_propulsor.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Core import Units  

# pacakge imports  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# internal_combustion_engine_propulsor
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsion-Networks
def internal_combustion_engine_propulsor(fuel_line,state): 
    ''' Computes the performance of an internal combustion engine propulsor unit
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    fuel_line             - distrubution component class              [string] 
    state                 - operating data structure                  [-] 
     
    Outputs:       
    total_thrust         - thrust of fuel line                        [N]
    total_power          - power of fuel line                         [W]
    total_mdot           - mass flow rate of fuel line                [kg/s]
    
    Properties Used: 
    N.A.        
    '''
    conditions      = state.conditions
    total_mdot      = 0*state.ones_row(1) 
    total_power     = 0*state.ones_row(1)  
    total_thrust    = 0*state.ones_row(3) 
    for propulsor_index, propulsor in enumerate(fuel_line.propulsors): 
        if fuel_line.identical_propulsors == True and propulsor_index>0: 
            propulsor_0                           = list(fuel_line.propulsors.keys())[0] 
            ice_results_0                         = conditions.energy[fuel_line.tag][propulsor_0]
            noise_results_0                       = conditions.noise[fuel_line.tag][propulsor_0]  
            ice_results                           = conditions.energy[fuel_line.tag][propulsor.tag]  
            noise_results                         = conditions.noise[fuel_line.tag][propulsor.tag] 
            ice_results.mass_flow_rate            = ice_results_0.mass_flow_rate          
            ice_results.engine.power              = ice_results_0.engine.power            
            ice_results.engine.torque             = ice_results_0.engine.torque           
            ice_results.engine.throttle           = ice_results_0.engine.throttle         
            ice_results.rotor.torque              = ice_results_0.rotor.torque            
            ice_results.rotor.thrust              = ice_results_0.rotor.thrust            
            ice_results.rotor.rpm                 = ice_results_0.rotor.rpm               
            ice_results.rotor.tip_mach            = ice_results_0.rotor.tip_mach          
            ice_results.rotor.disc_loading        = ice_results_0.rotor.disc_loading      
            ice_results.rotor.power_loading       = ice_results_0.rotor.power_loading     
            ice_results.rotor.efficiency          = ice_results_0.rotor.efficiency        
            ice_results.rotor.figure_of_merit     = ice_results_0.rotor.figure_of_merit   
            noise_results.rotor                   = noise_results_0.rotor     
            total_mdot                            += fuel_line_results.fuel_flow_rate 
            total_power                           += ice_results.engine.power
            total_thrust                          += ice_results.rotor.thrust 

        else:   
            fuel_line_results       = conditions.energy[fuel_line.tag]
            ice_results             = fuel_line_results[propulsor.tag]
            noise_results           = conditions.noise[fuel_line.tag][propulsor.tag] 
            engine                  = propulsor.engine 
            rotor                   = propulsor.rotor 
        
            # Throttle the engine
            engine.inputs.omega  = ice_results.rotor.rpm * Units.rpm 
            
            # Run the engine
            engine.calculate_power_out_from_throttle(conditions,conditions.energy[fuel_line.tag].throttle)    
            torque     = engine.outputs.torque     
            
            # link
            rotor.inputs.omega = ice_results.rotor.rpm * Units.rpm 
        
            # Spin the rotor 
            F, Q, P, Cp, outputs, etap = rotor.spin(conditions) 
        
            # Check to see if magic thrust is needed, the ESC caps throttle at 1.1 already
            eta                 = conditions.energy[fuel_line.tag].throttle  
            P[eta>1.0]          = P[eta>1.0]*eta[eta>1.0]
            F[eta[:,0]>1.0,:]   = F[eta[:,0]>1.0,:]*eta[eta[:,0]>1.0,:]
        
            # Determine Conditions specific to this instantation of engine and rotors
            R                   = rotor.tip_radius
            rpm                 = engine.inputs.speed / Units.rpm 
            F_mag               = np.atleast_2d(np.linalg.norm(F, axis=1)).T  
        
            # Create the outputs 
            fuel_line_results.fuel_flow_rate      = engine.outputs.fuel_flow_rate
            ice_results.engine.power              = P 
            ice_results.engine.torque             = torque
            ice_results.engine.throttle           = eta 
            ice_results.rotor.torque              = Q
            ice_results.rotor.thrust              = F
            ice_results.rotor.rpm                 = rpm
            ice_results.rotor.tip_mach            = (R*rpm*Units.rpm)/conditions.freestream.speed_of_sound    
            ice_results.rotor.disc_loading        = (F_mag)/(np.pi*(R**2))             
            ice_results.rotor.power_loading       = (F_mag)/(P)    
            ice_results.rotor.efficiency          = etap
            ice_results.rotor.figure_of_merit     = outputs.figure_of_merit
            noise_results.rotor                   = outputs  
            total_power                           += P
            total_thrust                          += F 
            total_mdot                            += fuel_line_results.fuel_flow_rate         
            
    return  total_thrust , total_power ,total_mdot