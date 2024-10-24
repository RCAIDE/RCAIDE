# RCAIDE/Framework/Functions/Segments/Descent/Constant_Speed_Constant_Angle_Noise.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports
import RCAIDE
from RCAIDE.Framework.Core                       import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate  import Evaluate 
from RCAIDE.Framework.Mission.Functions import Common


# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Speed_Constant_Angle_Noise
# ----------------------------------------------------------------------------------------------------------------------    
class Constant_Speed_Constant_Angle_Noise(Evaluate):
    """ Fixed at a true airspeed the vehicle will descend at a constant angle. This is a specific segment for Noise.
        A vehicle performs a descent to landing in accordance with a certification points for landing noise.
        Don't use this segment unless you're planning on post process for noise. It is slower than the normal constant
        speed constand angle segment. 
    """     
    
    def __defaults__(self):
        """ Specific flight segment defaults which can be modified after initializing.
        
            Assumptions:
                None
    
            Source:
                None
        """  
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start    = None # Optional
        self.altitude_end      = 0.0 * Units.km
        self.descent_angle     = 3.  * Units.deg
        self.air_speed         = 100 * Units.m / Units.s
        self.true_course       = 0.0 * Units.degrees 
        
        self.state.numerics.discretization_method = RCAIDE.Library.Methods.Utilities.Chebyshev.linear_data 
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions specific processes
        # --------------------------------------------------------------------------------------------------------------  
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.expand_state            = RCAIDE.Framework.Mission.Mission.Segments.Descent.Constant_Speed_Constant_Angle_Noise.expand_state
        initialize.conditions              = RCAIDE.Framework.Mission.Mission.Segments.Descent.Constant_Speed_Constant_Angle_Noise.initialize_conditions
        iterate                            = self.process.iterate   
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        iterate.unknowns.mission           = Common.Unpack_Unknowns.attitude          
        
        return

