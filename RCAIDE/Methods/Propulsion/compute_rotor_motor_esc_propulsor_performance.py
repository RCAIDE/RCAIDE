# RCAIDE/Methods/Propulsion/compute_rotor_motor_esc_propulsor_performance.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Core import Units

# pacakge imports 
from copy import copy
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Propulsion
def compute_rotor_motor_esc_propulsor_performance(i,bus_tag,propulsor_group_tag,motors,rotors,N_rotors,escs,state,voltage): 
    ''' Computes the perfomrance of a propulsive unit comprising of rotors, motors and electronic speed controllers 
    
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
    bus_results         = state.conditions.energy[bus_tag]
    unique_rotor_tags   = state.conditions.energy[bus_tag][propulsor_group_tag].unique_rotor_tags
    unique_motor_tags   = state.conditions.energy[bus_tag][propulsor_group_tag].unique_motor_tags
    unique_esc_tags     = state.conditions.energy[bus_tag][propulsor_group_tag].unique_esc_tags  
    
    motor    = motors[unique_motor_tags[i]]
    rotor    = rotors[unique_rotor_tags[i]]
    esc      = escs[unique_esc_tags[i]]

    # Assign battery power
    esc.inputs.voltagein = voltage

    # Throttle the voltage
    esc.voltageout(bus_results[propulsor_group_tag].throttle)     

    # Set rotor y-axis rotation                
    rotor.inputs.y_axis_rotation = bus_results[propulsor_group_tag].y_axis_rotation  
 
    # Assign conditions to the rotor
    motor.inputs.voltage         = esc.outputs.voltageout
    motor.inputs.rotor_CP        = bus_results[propulsor_group_tag].rotor.power_coefficient  
    motor.omega(state.conditions) 
    rotor.inputs.omega           = motor.outputs.omega 

    # Spin the rotor 
    F, Q, P, Cp, outputs, etap = rotor.spin(state.conditions) 

    # Check to see if magic thrust is needed, the ESC caps throttle at 1.1 already
    eta                = bus_results[propulsor_group_tag].throttle 
    F[eta[:,0]  <=0.0] = 0.0
    P[eta[:,0]  <=0.0] = 0.0
    Q[eta[:,0]  <=0.0] = 0.0 
    P[eta>1.0]         = P[eta>1.0]*eta[eta>1.0]
    F[eta[:,0]>1.0,:]  = F[eta[:,0]>1.0,:]*eta[eta[:,0]>1.0,:]

    # Run the motor for current
    _ , etam =  motor.current()

    # Determine Conditions specific to this instantation of motor and rotors
    R                   = rotor.tip_radius
    rpm                 = motor.outputs.omega / Units.rpm
    F_mag               = np.atleast_2d(np.linalg.norm(F, axis=1)).T
    total_thrust        = F * N_rotors[i]
    total_power         = P * N_rotors[i]
    total_motor_current = N_rotors[i]*motor.outputs.current

    # Pack specific outputs
    state.conditions.energy[bus_tag][propulsor_group_tag].motor.efficiency        = etam  
    state.conditions.energy[bus_tag][propulsor_group_tag].motor.torque            = motor.outputs.torque
    state.conditions.energy[bus_tag][propulsor_group_tag].rotor.torque            = Q
    state.conditions.energy[bus_tag][propulsor_group_tag].rotor.thrust            = np.atleast_2d(np.linalg.norm(total_thrust ,axis = 1)).T
    state.conditions.energy[bus_tag][propulsor_group_tag].rotor.rpm               = rpm
    state.conditions.energy[bus_tag][propulsor_group_tag].rotor.tip_mach          = (R*rpm*Units.rpm)/state.conditions.freestream.speed_of_sound 
    state.conditions.energy[bus_tag][propulsor_group_tag].rotor.disc_loading      = (F_mag)/(np.pi*(R**2))                 
    state.conditions.energy[bus_tag][propulsor_group_tag].rotor.power_loading     = (F_mag)/(P)        
    state.conditions.energy[bus_tag][propulsor_group_tag].rotor.efficiency        = etap  
    state.conditions.energy[bus_tag][propulsor_group_tag].rotor.figure_of_merit   = outputs.figure_of_merit  
    state.conditions.energy[bus_tag][propulsor_group_tag].throttle                = eta 
    state.conditions.noise.sources.rotors[rotor.tag]                              = outputs 

    # Detemine esc current 
    esc.inputs.currentout = total_motor_current
    esc.currentin(state.conditions.energy[bus_tag][propulsor_group_tag].throttle)
    total_current = esc.outputs.currentin

    return outputs , total_thrust , total_power , total_current 