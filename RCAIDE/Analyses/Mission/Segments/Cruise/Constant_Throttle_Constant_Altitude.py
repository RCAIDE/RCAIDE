## @ingroup Analyses-Mission-Segments-Cruise 
# RCAIDE/Analyses/Mission/Segments/Cruise/Constant_Throttle_Constant_Altitude.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Analyses.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Core                                 import Units   
from RCAIDE.Methods.Mission                      import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Throttle_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Analyses-Mission-Segments-Cruise
class Constant_Throttle_Constant_Altitude(Evaluate):
    """ Vehicle flies at a set throttle setting. Allows a vehicle to do a level acceleration.
    
        Assumptions:
        None
        
        Source:
        None
    """           
    
    
    # ------------------------------------------------------------------
    #   Data Defaults
    # ------------------------------------------------------------------  

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
        # User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.throttle          = None
        self.altitude          = None
        self.air_speed_start   = None
        self.air_speed_end     = 0.0 
        self.true_course_angle = 0.0 * Units.degrees  

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission Specific Unknowns and Residuals 
        # --------------------------------------------------------------------------------------------------------------          
        ones_row                                  = self.state.ones_row
        self.state.unknowns.body_angle            = ones_row(1) * 0.0
        self.state.unknowns.accel_x               = ones_row(1) * 1.
        self.state.unknowns.time                  = 100.
        self.state.residuals.final_velocity_error = 0.0
        self.state.residuals.forces               = ones_row(2) * 0.0
     
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize  
        initialize.conditions              = Segments.Cruise.Constant_Throttle_Constant_Altitude.initialize_conditions      
        iterate                            = self.process.iterate       
        iterate.conditions.velocity        = Segments.Cruise.Constant_Throttle_Constant_Altitude.integrate_velocity  
        iterate.residuals.total_forces     = Segments.Cruise.Constant_Throttle_Constant_Altitude.solve_residuals 
        iterate.unknowns.mission           = Segments.Cruise.Constant_Throttle_Constant_Altitude.unpack_unknowns                  

        return