## @ingroup Analyses-Mission-Segments-Transition
# RCAIDE/Analyses/Mission/Segments/Transition/Constant_Acceleration_Constant_Pitchrate_Constant_Altitude.py 
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Core                                     import Units 
from RCAIDE.Analyses.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Methods.Mission                          import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Acceleration_Constant_Pitchrate_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Analyses-Mission-Segments-Transition
class Constant_Acceleration_Constant_Pitchrate_Constant_Altitude(Evaluate):
    """ Vehicle accelerates at a constant rate between two airspeeds.
    
        Assumptions:
        None
        
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
        
        # --------------------------------------------------------------
        #   User Inputs
        # --------------------------------------------------------------
        self.altitude           = None
        self.acceleration       = 1.  * Units['m/s/s']
        self.air_speed_start    = None
        self.air_speed_end      = 1.0 * Units['m/s']        
        self.pitch_initial      = None
        self.pitch_final        = 0.0 * Units['rad']
        self.true_course_angle  = 0.0 * Units.degrees  
        

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission Specific Unknowns and Residuals 
        # -------------------------------------------------------------------------------------------------------------- 
        ones_row = self.state.ones_row
        self.state.residuals.forces   = ones_row(2) * 0.0  
         
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------          
        initialize                         = self.process.initialize 
        initialize.conditions              = Segments.Transition.Constant_Acceleration_Constant_Pitchrate_Constant_Altitude.initialize_conditions      
        iterate                            = self.process.iterate    
        iterate.residuals.total_forces     = Segments.Transition.Constant_Acceleration_Constant_Angle_Linear_Climb.residual_total_forces
        
        return