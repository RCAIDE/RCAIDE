## @ingroup Methods-Energy-Propulsors-Converters-DC_Motor
# RCAIDE/Methods/Energy/Propulsors/Converters/DC_Motor/design_motor.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    

# package imports 
from scipy.optimize import minimize 

## @ingroup Methods-Energy-Propulsors-Converters-DC_Motor
def design_motor(motor):
    ''' Optimizes the motor to obtain the best combination of speed constant and resistance values
    by essentially sizing the motor for a design RPM value. Note that this design RPM 
    value can be compute from design tip mach  
    
    Assumptions:
    motor design performance occurs at 90% nominal voltage to account for off design conditions 
    
    Source:
    N/A
    
    Inputs:
    motor                         [-]  
      
    motor.     
      no_load_current             [amps]
      mass_properties.mass        [kg]
           
    Outputs:     
    motor.     
      speed_constant              [untiless]
      design_torque               [Nm] 
      motor.resistance            [Ohms]
      motor.angular_velocity      [rad/s]
      motor.origin                [m]
    '''    
      
    # design conditions for motor 
    io                          = motor.no_load_current
    v                           = motor.nominal_voltage
    omeg                        = motor.angular_velocity     
    etam                        = motor.efficiency 
    Q                           = motor.design_torque 
    
    # solve for speed constant   
    opt_params = optimize_kv(io, v , omeg,  etam ,  Q)
    
    Kv  =  opt_params[0]
    Res =  opt_params[1]    
    
    motor.speed_constant   = Kv 
    motor.resistance       = Res 
    
    return motor 
  
## @ingroup Methods-Energy-Propulsors
def optimize_kv(io, v , omeg,  etam ,  Q, kv_lower_bound =  0.01, Res_lower_bound = 0.001, kv_upper_bound = 100, Res_upper_bound = 10 ): 
    ''' Optimizer for compute_optimal_motor_parameters function  
    
    Source:
    N/A
    
    Inputs:
    motor    (to be modified)
    
    Outputs:
    motor.
      speed_constant     [untiless]
      no_load_current    [amps]
    '''        
    # objective  
    
    args = (v , omeg,  etam , Q , io )
    
    hard_cons = [{'type':'eq', 'fun': hard_constraint_1,'args': args},
                 {'type':'eq', 'fun': hard_constraint_2,'args': args}]
    
    slack_cons = [{'type':'eq', 'fun': slack_constraint_1,'args': args},
                  {'type':'eq', 'fun': slack_constraint_2,'args': args}] 
   
    
    bnds = ((kv_lower_bound, kv_upper_bound), (Res_lower_bound , Res_upper_bound)) 
    
    # try hard constraints to find optimum motor parameters
    sol = minimize(objective, [0.5, 0.1], args=(v , omeg,  etam , Q , io) , method='SLSQP', bounds=bnds, tol=1e-6, constraints=hard_cons) 
    
    if sol.success == False:
        # use slack constraints  if optimum motor parameters cannot be found 
        print('\n Optimum motor design failed. Using slack constraints')
        sol = minimize(objective, [0.5, 0.1], args=(v , omeg,  etam , Q , io) , method='SLSQP', bounds=bnds, tol=1e-6, constraints=slack_cons)
         
        if sol.success == False:
            assert('\n Slack contraints failed') 
    return sol.x   
  
# objective function
def objective(x, v , omeg,  etam , Q , io ): 
    return (v - omeg/x[0])/x[1]   

# hard efficiency constraint
def hard_constraint_1(x, v , omeg,  etam , Q , io ): 
    return etam - (1- (io*x[1])/(v - omeg/x[0]))*(omeg/(v*x[0]))   

# hard torque equality constraint
def hard_constraint_2(x, v , omeg,  etam , Q , io ): 
    return ((v - omeg/x[0])/x[1] - io)/x[0] - Q  

# slack efficiency constraint 
def slack_constraint_1(x, v , omeg,  etam , Q , io ): 
    return abs(etam - (1- (io*x[1])/(v - omeg/x[0]))*(omeg/(v*x[0]))) - 0.2

# slack torque equality constraint 
def slack_constraint_2(x, v , omeg,  etam , Q , io ): 
    return  abs(((v - omeg/x[0])/x[1] - io)/x[0] - Q) - 200 