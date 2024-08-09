## @ingroup Methods-Energy-Propulsors-Electric_Rotor_Propulsor
# RCAIDE/Methods/Energy/Propulsors/Electric_Rotor_Propulsor/compute_electric_rotor_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Framework.Core import Units
from RCAIDE.Library.Methods.Propulsors.Modulators.Electronic_Speed_Controller.compute_esc_performance  import * 
from RCAIDE.Library.Methods.Propulsors.Converters.DC_Motor.compute_motor_performance                   import *
from RCAIDE.Library.Methods.Propulsors.Converters.Rotor.compute_rotor_performance                      import * 


# pacakge imports  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# compute_electric_rotor_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsors-Electric_Rotor_Propulsor
def compute_electric_rotor_performance(propulsor,state,bus,voltage,center_of_gravity= [[0.0, 0.0,0.0]]):   
    ''' Computes the perfomrance of one propulsor
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure    [-] 
    voltage              - system voltage                         [V]
    bus                  - bus                                    [-] 
    propulsor            - propulsor data structure               [-] 
    total_thrust         - thrust of propulsor group              [N]
    total_power          - power of propulsor group               [W]
    total_current        - current of propulsor group             [A]

    Outputs:  
    total_thrust         - thrust of propulsor group              [N]
    total_power          - power of propulsor group               [W]
    total_current        - current of propulsor group             [A]
    stored_results_flag  - boolean for stored results             [-]     
    stored_propulsor_tag - name of propulsor with stored results  [-]
    
    Properties Used: 
    N.A.        
    ''' 
    conditions                 = state.conditions    
    electric_rotor_conditions  = conditions.energy[bus.tag][propulsor.tag] 
    motor                      = propulsor.motor 
    rotor                      = propulsor.rotor 
    esc                        = propulsor.electronic_speed_controller
    motor_conditions           = electric_rotor_conditions[motor.tag]
    rotor_conditions           = electric_rotor_conditions[rotor.tag]
    esc_conditions             = electric_rotor_conditions[esc.tag]
    eta                        = conditions.energy[bus.tag][propulsor.tag].throttle

    esc_conditions.inputs.voltage   = voltage
    esc_conditions.throttle         = eta 
    compute_voltage_out_from_throttle(esc,esc_conditions,conditions)

    # Assign conditions to the rotor
    motor_conditions.inputs.voltage                   = esc_conditions.outputs.voltage
    motor_conditions.inputs.rotor_power_coefficient   = rotor_conditions.power_coefficient  
    compute_RPM_and_torque_from_power_coefficent_and_voltage(motor,motor_conditions,conditions)
    
    # Spin the rotor 
    rotor_conditions.omega       = motor_conditions.outputs.omega
    rotor_conditions.throttle    = esc_conditions.throttle 
    compute_rotor_performance(propulsor,state,bus,center_of_gravity)  

    # Run the motor for current
    compute_current_from_RPM_and_voltage(motor,motor_conditions,conditions)
 
    # Pack specific outputs
    motor_conditions.efficiency        = motor_conditions.outputs.efficiency
    motor_conditions.torque            = motor_conditions.outputs.torque 

    # Detemine esc current 
    esc_conditions.outputs.current = motor_conditions.outputs.current
    compute_current_in_from_throttle(esc,esc_conditions,conditions)
    esc_conditions.current   = esc_conditions.inputs.current  
    esc_conditions.power     = esc_conditions.inputs.power 
    
    stored_results_flag     = True
    stored_propulsor_tag    = propulsor.tag 
    
    # compute total forces and moments from propulsor (future work would be to add moments from motors)
    conditions.energy[bus.tag][propulsor.tag].thrust      = conditions.energy[bus.tag][propulsor.tag][rotor.tag].thrust 
    conditions.energy[bus.tag][propulsor.tag].moment      = conditions.energy[bus.tag][propulsor.tag][rotor.tag].moment 
    
    T  = conditions.energy[bus.tag][propulsor.tag].thrust 
    M  = conditions.energy[bus.tag][propulsor.tag].moment 
    P  = esc_conditions.power
    I  = esc_conditions.current
    
    return T,M,P,I, stored_results_flag,stored_propulsor_tag 
                
def reuse_stored_electric_rotor_data(propulsor,state,bus,stored_propulsor_tag,center_of_gravity= [[0.0, 0.0,0.0]]):
    '''Reuses results from one propulsor for identical propulsors
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure    [-] 
    voltage              - system voltage                         [V]
    bus                  - bus                                    [-] 
    propulsors           - propulsor data structure               [-] 
    total_thrust         - thrust of propulsor group              [N]
    total_power          - power of propulsor group               [W]
    total_current        - current of propulsor group             [A]

    Outputs:  
    total_thrust         - thrust of propulsor group              [N]
    total_power          - power of propulsor group               [W]
    total_current        - current of propulsor group             [A] 
    
    Properties Used: 
    N.A.        
    ''' 
    conditions                                = state.conditions

    motor                      = propulsor.motor 
    rotor                      = propulsor.rotor 
    esc                        = propulsor.electronic_speed_controller  
    motor_0                    = bus[stored_propulsor_tag].motor 
    rotor_0                    = bus[stored_propulsor_tag].rotor 
    esc_0                      = bus[stored_propulsor_tag].electronic_speed_controller
    
    electric_rotor_energy_conditions_0                          = conditions.energy[bus.tag][stored_propulsor_tag]
    electric_rotor_noise_conditions_0                           = conditions.noise[bus.tag][stored_propulsor_tag]
    conditions.energy[bus.tag][propulsor.tag][motor.tag]        = electric_rotor_energy_conditions_0[motor_0.tag]
    conditions.energy[bus.tag][propulsor.tag][rotor.tag]        = electric_rotor_energy_conditions_0[rotor_0.tag]
    conditions.energy[bus.tag][propulsor.tag][esc.tag]          = electric_rotor_energy_conditions_0[esc_0.tag]

    conditions.noise[bus.tag][propulsor.tag][motor.tag]         = electric_rotor_noise_conditions_0[motor_0.tag]
    conditions.noise[bus.tag][propulsor.tag][rotor.tag]         = electric_rotor_noise_conditions_0[rotor_0.tag]
    conditions.noise[bus.tag][propulsor.tag][esc.tag]           = electric_rotor_noise_conditions_0[esc_0.tag]   
     
    thrust                  = electric_rotor_energy_conditions_0.rotor.thrust 
    power                   = electric_rotor_energy_conditions_0.esc.power
    current                 = electric_rotor_energy_conditions_0.esc.current
    
    moment_vector           = 0*state.ones_row(3) 
    moment_vector[:,0]      = rotor.origin[0][0]  -  center_of_gravity[0][0] 
    moment_vector[:,1]      = rotor.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2]      = rotor.origin[0][2]  -  center_of_gravity[0][2]
    moment                  =  np.cross(moment_vector, thrust)
    
    conditions.energy[bus.tag][propulsor.tag][rotor.tag].moment = moment  
    conditions.energy[bus.tag][propulsor.tag].thrust            = thrust   
    conditions.energy[bus.tag][propulsor.tag].moment            = moment  
    
    return thrust,moment,power,current 