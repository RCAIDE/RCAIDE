## @ingroup Analyses-Mission-Segments-Descent
# RCAIDE/Analyses/Mission/Segments/Descent/Constant_Speed_Constant_Angle_Noise.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports
import RCAIDE
from RCAIDE.Core                                 import Units 
from RCAIDE.Analyses.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Methods.Mission                      import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------  
#  Constant_Speed_Constant_Angle_Noise
# ----------------------------------------------------------------------------------------------------------------------   

## @ingroup Analyses-Mission-Segments-Descent
class Constant_Speed_Constant_Angle_Noise(Evaluate):
    """ Fixed at a true airspeed the vehicle will descend at a constant angle. This is a specific segment for Noise.
        A vehicle performs a descent to landing in accordance with a certification points for landing noise.
        Don't use this segment unless you're planning on post process for noise. It is slower than the normal constant
        speed constand angle segment.
    
        Assumptions:
        The points are linearly spaced rather than chebyshev spaced to give the proper "microphone" locations.
        
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
        self.altitude_start    = None # Optional
        self.altitude_end      = 0.0 * Units.km
        self.descent_angle     = 3.  * Units.deg
        self.air_speed         = 100 * Units.m / Units.s
        self.true_course_angle = 0.0 * Units.degrees 
        
        self.state.numerics.discretization_method = RCAIDE.Methods.Utilities.Chebyshev.linear_data
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission Specific Unknowns and Residuals 
        # --------------------------------------------------------------------------------------------------------------    
        self.body_angle_control.active             = True            
        self.body_angle_control.initial_values     = [[3.0 * Units.degrees]]  
        self.throttle_control.active               = True
        self.throttle_control.propulsor_list       = None
        self.throttle_control.initial_values       = [[0.5]]       
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------  
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.expand_state            = Segments.Descent.Constant_Speed_Constant_Angle_Noise.expand_state
        initialize.conditions              = Segments.Descent.Constant_Speed_Constant_Angle_Noise.initialize_conditions
        iterate                            = self.process.iterate   
        iterate.residuals.total_forces     = Common.Residuals.climb_descent_forces 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.climb_descent          
        
        return

