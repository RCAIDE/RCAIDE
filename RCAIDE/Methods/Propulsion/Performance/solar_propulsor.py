## @ingroup Methods-Propulsion
# RCAIDE/Methods/Propulsion/solar_propulsor.py
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
# compute_propulsor_performanc
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Propulsion
def solar_propulsor(i,bus,propulsor_group_tag,motors,rotors,N_rotors,escs,conditions,voltage):
    ''' Computes the perfomrance of an all electric propulsor unit
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs: 
    i                     - index of unique compoment             [-]
    bus_tag               - tag of bus                            [string]
    propulsor_group_tag   - tag of propulsor group                [string]
    motors                - data structure of motors              [-]
    rotors                - data structure of motors              [-]
    N_rotors              - number of rotors in propulsor group   [-]
    escs                  - data structure of motors              [-]
    state                 - operating data structure              [-]
    voltage               - system voltage                        [Volts]

    Outputs: 
    outputs              - propulsor operating outputs             [-]
    total_thrust         - thrust of propulsor group              [N]
    total_power          - power of propulsor group               [V]
    total_current        - current of propulsor group             [N]
    
    Properties Used: 
    N.A.        
    '''
    bus_results         = conditions.energy[bus.tag]
    unique_rotor_tags   = conditions.energy[bus.tag][propulsor_group_tag].unique_rotor_tags
    unique_motor_tags   = conditions.energy[bus.tag][propulsor_group_tag].unique_motor_tags
    unique_esc_tags     = conditions.energy[bus.tag][propulsor_group_tag].unique_esc_tags
    
    motor    = motors[unique_motor_tags[i]]
    rotor    = rotors[unique_rotor_tags[i]]
    esc      = escs[unique_esc_tags[i]]

    # Assign battery power
    esc.inputs.voltage   = voltage
    
    # Throttle the voltage 
    esc.calculate_voltage_out_from_throttle(bus_results[propulsor_group_tag].throttle)     
 
    # Assign conditions to the rotor
    motor.inputs.voltage         = esc.outputs.voltage
    motor.inputs.rotor_CP        = bus_results[propulsor_group_tag].rotor.power_coefficient  
    motor.calculate_omega_out_from_power_coefficient(conditions)
    rotor.inputs.omega           = motor.outputs.omega 

    # Spin the rotor 
    F, Q, P, Cp, outputs, etap = rotor.spin(conditions) 

    # Check to see if magic thrust is needed, the ESC caps throttle at 1.1 already
    eta                = bus_results[propulsor_group_tag].throttle 
    F[eta[:,0]  <=0.0] = 0.0
    P[eta[:,0]  <=0.0] = 0.0
    Q[eta[:,0]  <=0.0] = 0.0 
    P[eta>1.0]         = P[eta>1.0]*eta[eta>1.0]
    F[eta[:,0]>1.0,:]  = F[eta[:,0]>1.0,:]*eta[eta[:,0]>1.0,:]

    # Run the motor for current
    motor.calculate_current_out_from_omega()

    # Determine Conditions specific to this instantation of motor and rotors
    R                   = rotor.tip_radius
    rpm                 = motor.outputs.omega / Units.rpm
    F_mag               = np.atleast_2d(np.linalg.norm(F, axis=1)).T
    total_thrust        = F * N_rotors[i]
    total_power         = P * N_rotors[i]
    total_motor_current = N_rotors[i]*motor.outputs.current

    # Pack specific outputs
    conditions.energy[bus.tag][propulsor_group_tag].motor.efficiency        = motor.outputs.efficiency
    conditions.energy[bus.tag][propulsor_group_tag].motor.torque            = motor.outputs.torque
    conditions.energy[bus.tag][propulsor_group_tag].throttle                = eta
    conditions.energy[bus.tag][propulsor_group_tag].rotor.torque            = Q
    conditions.energy[bus.tag][propulsor_group_tag].rotor.thrust            = np.atleast_2d(np.linalg.norm(total_thrust ,axis = 1)).T
    conditions.energy[bus.tag][propulsor_group_tag].rotor.rpm               = rpm
    conditions.energy[bus.tag][propulsor_group_tag].rotor.tip_mach          = (R*rpm*Units.rpm)/conditions.freestream.speed_of_sound
    conditions.energy[bus.tag][propulsor_group_tag].rotor.disc_loading      = (F_mag)/(np.pi*(R**2))
    conditions.energy[bus.tag][propulsor_group_tag].rotor.power_loading     = (F_mag)/(P)
    conditions.energy[bus.tag][propulsor_group_tag].rotor.efficiency        = etap
    conditions.energy[bus.tag][propulsor_group_tag].rotor.figure_of_merit   = outputs.figure_of_merit
    conditions.noise.sources.rotors[rotor.tag]                              = outputs 

    # Detemine esc current 
    esc.outputs.current  = total_motor_current
    esc.calculate_current_in_from_throttle(bus_results[propulsor_group_tag].throttle)
    total_current = esc.inputs.current

    return outputs , total_thrust , total_power , total_current 