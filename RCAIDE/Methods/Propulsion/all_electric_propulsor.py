## @ingroup Methods-Propulsion
# RCAIDE/Methods/Propulsion/all_electric_propulsor.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Core import Units , Data 
from RCAIDE.Methods.Propulsion.compute_number_of_compoment_groups import compute_number_of_compoment_groups

# pacakge imports  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# compute_propulsor_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Propulsion
def compute_propulsor_performance(i,bus,propulsor_group_tag,motors,rotors,N_rotors,escs,conditions,voltage):
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
    conditions            - operating data structure              [-]
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

    ## run esc
    #if bus.fixed_voltage:
        
        ## Set rotor y-axis rotation                
        #rotor.inputs.omega           = bus_results[propulsor_group_tag].rotor.rpm * Units.rpm 
    
        ## Spin the rotor 
        #F, Q, P, Cp, outputs, etap = rotor.spin(conditions)  
        
        #bus_results[propulsor_group_tag].rotor.power_coefficient = Cp 
        
        ## run motor 
        #motor.outputs.torque   = Q* rotor.electric_propulsion_fraction
        #motor.outputs.omega    = rotor.inputs.omega  
        #motor.calculate_voltage_current_in_from_omega()    
        
        #esc.outputs.voltage   = motor.inputs.voltage  
        #esc.inputs.voltage    = voltage
        #esc.calculate_thottle_from_voltages() 
    #else: 
    esc.inputs.voltage   = voltage
    esc.calculate_voltage_out_from_throttle(bus_results[propulsor_group_tag].motor.throttle)
    esc.inputs.throttle  = bus_results[propulsor_group_tag].motor.throttle

    # Assign conditions to the rotor
    motor.inputs.voltage         = esc.outputs.voltage
    motor.inputs.rotor_CP        = bus_results[propulsor_group_tag].rotor.power_coefficient  
    motor.calculate_omega_out_from_power_coefficient(conditions)
    rotor.inputs.omega           = motor.outputs.omega 

    # Spin the rotor 
    F, Q, P, Cp, outputs, etap = rotor.spin(conditions)  
            
    # Check to see if magic thrust is needed, the ESC caps throttle at 1.1 already
    eta                = bus_results[propulsor_group_tag].motor.throttle 
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
    conditions.energy[bus.tag][propulsor_group_tag].rotor.torque            = Q
    conditions.energy[bus.tag][propulsor_group_tag].motor.throttle          = eta
    conditions.energy[bus.tag][propulsor_group_tag].rotor.power             = P
    conditions.energy[bus.tag][propulsor_group_tag].esc.throttle            = esc.inputs.throttle
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
    esc.calculate_current_in_from_throttle(bus_results[propulsor_group_tag].motor.throttle)
    total_current = esc.inputs.current
    

    return outputs , total_thrust , total_power , voltage, total_current 


# ----------------------------------------------------------------------------------------------------------------------
# compute_unique_propulsor_groups
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Propulsion
def compute_unique_propulsor_groups(bus): 
    '''Computes the unique rotor groups on a bus    
    
    Assumptions:
    None

    Source:
    N/A

    Inputs: 
    bus                     - bus control unit data structure [-]
    
    Outputs:  
    sorted_propulsors. 
        rotor_indexes       - rotor indexes                   [-]
        unique_rotor_tags   - rotor tags                      [string(s)]
        unique_motor_tags   - motor tags                      [string(s)]
        unique_esc_tags     - electronic speed rotor tags     [string(s)]
        N_rotors            - number of rotors                [-]

    Properties Used:
    N/A 
    '''
    
    motors                     = bus.motors 
    rotors                     = bus.rotors 
    escs                       = bus.electronic_speed_controllers
    active_propulsor_groups    = bus.active_propulsor_groups 
    N_active_propulsor_groups  = len(active_propulsor_groups)
    
    # determine propulsor group indexes 
    motor_group_indexes,motor_group_names,unique_motor_tags  = compute_number_of_compoment_groups(motors,active_propulsor_groups)
    rotor_group_indexes,rotor_groups_names,unique_rotor_tags = compute_number_of_compoment_groups(rotors,active_propulsor_groups)
    esc_group_indexes,esc_group_names,unique_esc_tags        = compute_number_of_compoment_groups(escs,active_propulsor_groups)   
    
    # make sure that each rotor has a motor and esc
    if (len(rotor_group_indexes)!=len(motor_group_indexes)) or (len(esc_group_indexes)!=len(motor_group_indexes)):
        assert('The number of rotors and/or esc is not the same as the number of motors')  
        
    # Count the number of unique pairs of rotors and motors 
    unique_rotor_groups,N_rotors   = np.unique(rotor_group_indexes, return_counts=True)
    unique_motor_groups,_          = np.unique(motor_group_indexes, return_counts=True)
    unique_esc_groups,_            = np.unique(esc_group_indexes, return_counts=True)
    if (unique_rotor_groups == unique_motor_groups).all() and (unique_esc_groups == unique_motor_groups).all(): # rotors and motors are paired  
        rotor_indexes = []
        motor_indexes = []
        esc_indexes   = []
        for group in range(N_active_propulsor_groups):
            rotor_indexes.append(np.where(unique_rotor_groups[group] == rotor_group_indexes)[0][0])
            motor_indexes.append(np.where(unique_motor_groups[group] == motor_group_indexes)[0][0])
            esc_indexes.append(np.where(unique_esc_groups[group] == esc_group_indexes)[0][0])  
    else: 
        rotor_indexes = rotor_group_indexes
        motor_indexes = motor_group_indexes
        esc_indexes   = esc_group_indexes
        N_rotors      = np.ones_like(motor_group_indexes)   
    
    sorted_propulsors = Data(rotor_indexes       = rotor_indexes,
                             unique_rotor_tags   = unique_rotor_tags,
                             unique_motor_tags   = unique_motor_tags,
                             unique_esc_tags     = unique_esc_tags,
                             N_rotors            = N_rotors)
    return sorted_propulsors