## @ingroup Analyses-Mission-Segments-Climb
# RCAIDE/Analyses/Mission/Segments/Climb/Optimized.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Analyses.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Analyses                             import Process 
from RCAIDE.Core                                 import Units  
from RCAIDE.Methods                              import skip 
from RCAIDE.Methods.Mission.Segments             import Climb
from RCAIDE.Methods.Mission                      import Common 

# ----------------------------------------------------------------------------------------------------------------------
#  Optimized
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Analyses-Mission-Segments-Climb
class Optimized(Evaluate):
    """ Optimize your climb segment. This is useful if you're not sure how your vehicle should climb.
        
        1) You can set any conditions parameter as the objective, for example setting time to climb or vehicle mass:
           segment.objective  = 'conditions.weights.total_mass[-1,0]' 
        2) The ending airspeed is an optional parameter. 
        3) This segment takes far longer to run than a normal segment. Wrapping this into a vehicle optimization
           has not yet been tested for robustness. 
    
        Assumptions:
        Can use SNOPT if you have it installed through PyOpt. But defaults to SLSQP through 
        Runs a linear true airspeed mission first to initialize conditions.
        
        Source:
        None
    """          
    
    def __defaults__(self):
        """ This sets the default solver flow. Anything in here can be modified after initializing a segment.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            None
        """          
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start         = None
        self.altitude_end           = None
        self.air_speed_start        = None
        self.air_speed_end          = None
        self.objective              = None  
        self.minimize               = True
        self.lift_coefficient_limit = 1.e20 
        self.seed_climb_rate        = 300. * Units['feet/min']
        self.algorithm              = 'SLSQP'
        self.true_course_angle      = 0.0 * Units.degrees    
        
        # -------------------------------------------------------------------------------------------------------------- 
        # Optimization Problem
        # --------------------------------------------------------------------------------------------------------------                
        self.state.inputs_last             = None
        self.state.objective_value         = 0.0
        self.state.constraint_values       = 0.0
           
        
        #  Initialize 
        initialize                         = self.process.initialize 
        initialize.solved_mission          = Climb.Optimized.solve_linear_speed_constant_rate 
        initialize.conditions              = skip  
        
        # Unpack Unknowns
        iterate                            = self.process.iterate  
        iterate.unknowns.mission           = Climb.Optimized.unpack_unknowns
        
        # Update Conditions
        iterate.conditions                 = Process()
        iterate.conditions.differentials   = Climb.Optimized.update_differentials
        iterate.conditions.kinematics      = Common.Update.kinematics 

        # Solve Residuals 
        iterate.residuals.total_forces     = Common.Residuals.climb_descent_forces         
        
        # Set outputs
        iterate.outputs                    = Process()   
        iterate.outputs.objective          = Climb.Optimized.objective
        iterate.outputs.constraints        = Climb.Optimized.constraints
        iterate.outputs.cache_inputs       = Climb.Optimized.cache_inputs 

        #  Post Process   
        post_process                       = self.process.post_process   
        post_process.inertial_position     = Common.Update.inertial_horizontal_position
        post_process.battery_age           = Common.Update.battery_age  
        post_process.noise                 = Common.Update.noise        
        
        return

