## @ingroup Methods-Propulsion
# RCAIDE/Methods/Propulsion/all_electric_propulsor.py
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
# all_electric_propulsor
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Propulsion
def all_electric_propulsor(bus,state,voltage):
    ''' Computes the perfomrance of an all electric propulsor unit
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs: 
    i                     - index of unique compoment             [-]
    bus_tag               - tag of bus                            [string] 
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
    

    conditions      = state.conditions
    total_power     = 0*state.ones_row(1) 
    total_current   = 0*state.ones_row(1) 
    total_thrust    = 0*state.ones_row(3) 
    for propulsor_index, propulsor in enumerate(bus.propulsors): 
        if bus.identical_propulsors == True and propulsor_index>0: 
            propulsor_0                            = list(bus.propulsors.keys())[0] 
            energy_results_0                       = conditions.energy[bus.tag][propulsor_0]
            noise_results_0                        = conditions.noise[bus.tag][propulsor_0]  
            energy_results                         = conditions.energy[bus.tag][propulsor.tag] 
            noise_results                          = conditions.noise[bus.tag][propulsor.tag]
            energy_results.motor.efficiency        = energy_results_0.motor.efficiency      
            energy_results.motor.torque            = energy_results_0.motor.torque          
            energy_results.rotor.torque            = energy_results_0.rotor.torque        
            energy_results.rotor.power             = energy_results_0.rotor.power            
            energy_results.rotor.thrust            = energy_results_0.rotor.thrust          
            energy_results.rotor.rpm               = energy_results_0.rotor.rpm             
            energy_results.rotor.tip_mach          = energy_results_0.rotor.tip_mach        
            energy_results.rotor.disc_loading      = energy_results_0.rotor.disc_loading    
            energy_results.rotor.power_loading     = energy_results_0.rotor.power_loading   
            energy_results.rotor.efficiency        = energy_results_0.rotor.efficiency      
            energy_results.rotor.figure_of_merit   = energy_results_0.rotor.figure_of_merit 
            energy_results.esc.current             = energy_results_0.esc.current   
            energy_results.rotor.power_coefficient = energy_results_0.rotor.power_coefficient  
            energy_results.esc.power               = energy_results_0.esc.power     
            noise_results.rotor                    = noise_results_0.rotor    
            total_thrust                           += energy_results_0.rotor.thrust 
            total_power                            += energy_results_0.esc.power
            total_current                          += energy_results_0.esc.current 
             
        else:  
            noise_results        = conditions.noise[bus.tag][propulsor.tag]
            energy_results       = conditions.energy[bus.tag][propulsor.tag] 
            motor                = propulsor.motor 
            rotor                = propulsor.rotor 
            esc                  = propulsor.electronic_speed_controller 
         
            esc.inputs.voltage   = voltage
            esc.calculate_voltage_out_from_throttle(conditions.energy[bus.tag].throttle) 
        
            # Assign conditions to the rotor
            motor.inputs.voltage         = esc.outputs.voltage
            motor.inputs.rotor_CP        = energy_results.rotor.power_coefficient  
            motor.calculate_omega_out_from_power_coefficient(conditions)
            rotor.inputs.omega           = motor.outputs.omega 
        
            # Spin the rotor 
            F, Q, P, Cp, outputs, etap = rotor.spin(conditions)  
                    
            # Check to see if magic thrust is needed, the ESC caps throttle at 1.1 already
            eta                = conditions.energy[bus.tag].throttle
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
        
            # Pack specific outputs
            energy_results.motor.efficiency        = motor.outputs.efficiency
            energy_results.motor.torque            = motor.outputs.torque
            energy_results.rotor.torque            = Q 
            energy_results.rotor.power             = P 
            energy_results.rotor.thrust            = F
            energy_results.rotor.rpm               = rpm
            energy_results.rotor.tip_mach          = (R*rpm*Units.rpm)/conditions.freestream.speed_of_sound
            energy_results.rotor.disc_loading      = (F_mag)/(np.pi*(R**2))
            energy_results.rotor.power_loading     = (F_mag)/(P)
            energy_results.rotor.efficiency        = etap
            energy_results.rotor.figure_of_merit   = outputs.figure_of_merit
            noise_results.rotor                    = outputs 
        
            # Detemine esc current 
            esc.outputs.current          = motor.outputs.current
            esc.calculate_current_in_from_throttle(eta)
            energy_results.esc.current   = esc.inputs.current  
            energy_results.esc.power     = esc.inputs.power
            
            total_thrust  += energy_results.rotor.thrust 
            total_power   += energy_results.esc.power
            total_current += energy_results.esc.current
            
    return total_thrust , total_power ,  total_current