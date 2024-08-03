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
from RCAIDE.Library.Methods.Propulsors.Modulators.Electronic_Speed_Controller  import compute_voltage_out_from_throttle ,compute_current_in_from_throttle

# pacakge imports  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# compute_electric_rotor_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsors-Electric_Rotor_Propulsor
def compute_electric_rotor_performance(propulsor,voltage,state,bus,center_of_gravity= [[0.0, 0.0,0.0]]):  
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
    noise_conditions           = conditions.noise[bus.tag][propulsor.tag]
    electric_rotor_conditions  = conditions.energy[bus.tag][propulsor.tag] 
    motor                      = propulsor.motor 
    rotor                      = propulsor.rotor 
    esc                        = propulsor.electronic_speed_controller
    motor_conditions           = electric_rotor_conditions[motor.tag]
    rotor_conditions           = electric_rotor_conditions[rotor.tag]
    esc_conditions             = electric_rotor_conditions[esc.tag]
    eta                        = conditions.energy[bus.tag][propulsor.tag].throttle

    esc_conditions.inputs.voltage   = voltage
    compute_voltage_out_from_throttle(esc,eta) 

    # Assign conditions to the rotor
    motor_conditions.inputs.voltage         = esc_conditions.outputs.voltage
    motor_conditions.inputs.rotor_CP        = rotor_conditions.power_coefficient  
    motor.compute_omega(conditions)
    rotor_conditions.inputs.omega           = motor_conditions.outputs.omega
    #rotor_conditions.inputs.y_axis_rotation += electric_rotor_conditions.y_axis_rotation
    #rotor_conditions.inputs.pitch_command   += electric_rotor_conditions.rotor.pitch_command

    # Spin the rotor 
    F, Q, P, Cp, outputs, etap = rotor.spin(conditions)  

    # Check to see if magic thrust is needed, the ESC caps throttle at 1.1 already
    F[eta[:,0]  <=0.0] = 0.0
    P[eta[:,0]  <=0.0] = 0.0
    Q[eta[:,0]  <=0.0] = 0.0 
    P[eta>1.0]         = P[eta>1.0]*eta[eta>1.0]
    F[eta[:,0]>1.0,:]  = F[eta[:,0]>1.0,:]*eta[eta[:,0]>1.0,:]

    # Run the motor for current
    motor.compute_current_draw()

    # Determine Conditions specific to this instantation of motor and rotors
    R                   = rotor.tip_radius
    rpm                 = motor_conditions.outputs.omega / Units.rpm
    F_mag               = np.atleast_2d(np.linalg.norm(F, axis=1)).T 

    # Pack specific outputs
    motor_conditions.efficiency        = motor_conditions.outputs.efficiency
    motor_conditions.torque            = motor_conditions.outputs.torque
    rotor_conditions.torque            = Q 
    rotor_conditions.power             = P 
    rotor_conditions.thrust            = F
    rotor_conditions.rpm               = rpm
    rotor_conditions.tip_mach          = (R*rpm*Units.rpm)/conditions.freestream.speed_of_sound
    rotor_conditions.disc_loading      = (F_mag)/(np.pi*(R**2))
    rotor_conditions.power_loading     = (F_mag)/(P)
    rotor_conditions.efficiency        = etap
    rotor_conditions.figure_of_merit   = outputs.figure_of_merit
    noise_conditions.rotor                = outputs 

    # Detemine esc current 
    esc_conditions.outputs.current          = motor_conditions.outputs.current
    compute_current_in_from_throttle(esc,eta)
    esc_conditions.current   = esc_conditions.inputs.current  
    esc_conditions.power     = esc_conditions.inputs.power 


    # Compute forces and moments
    thrust                  = rotor_conditions.thrust 
    power                   = esc_conditions.power
    current                 = esc_conditions.current
    moment_vector           = 0*state.ones_row(3) 
    moment_vector[:,0]      = rotor.origin[0][0] -   center_of_gravity[0][0] 
    moment_vector[:,1]      = rotor.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2]      = rotor.origin[0][2]  -  center_of_gravity[0][2]
    moment                  =  np.cross(moment_vector, thrust)    
    rotor_conditions.moment = moment
    
    stored_results_flag     = True
    stored_propulsor_tag    = propulsor.tag   
    
    return thrust,moment,power,current, stored_results_flag,stored_propulsor_tag 
                
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
    electric_rotor_conditions_0               = conditions.energy[bus.tag][stored_propulsor_tag]
    noise_conditions_0                        = conditions.noise[bus.tag][stored_propulsor_tag]  
    conditions.energy[bus.tag][propulsor.tag] = electric_rotor_conditions_0  
    conditions.noise[bus.tag][propulsor.tag]  = noise_conditions_0   
    moment                                    = electric_rotor_conditions_0.rotor.moment 
    thrust                                    = electric_rotor_conditions_0.rotor.thrust 
    power                                     = electric_rotor_conditions_0.esc.power
    current                                   = electric_rotor_conditions_0.esc.current 
    
    return thrust,moment,power,current 