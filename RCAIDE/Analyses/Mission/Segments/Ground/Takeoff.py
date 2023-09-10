## @ingroup Analyses-Mission-Segments-Ground
# RCAIDE/Analyses/Mission/Segments/Ground/Takeoff.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from .Ground                 import Ground
from RCAIDE.Methods.Missions import Segments as Methods 
from RCAIDE.Core             import Units

# ----------------------------------------------------------------------------------------------------------------------
#  Takeoff
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Analyses-Mission-Segments-Ground
class Takeoff(Ground):
    """ Segment for takeoff. Integrates equations of motion
        including rolling friction.
        
        Assumptions:
        Notes Regarding Friction Coefficients
        Dry asphalt or concrete: .04 brakes off, .4 brakes on
        Wet asphalt or concrete: .05 brakes off, .225 brakes on
        Icy asphalt or concrete: .02 brakes off, .08 brakes on
        Hard turf:               .05 brakes off, .4 brakes on
        Firm dirt:               .04 brakes off, .3 brakes on
        Soft turf:               .07 brakes off, .2 brakes on
        Wet grass:               .08 brakes off, .2 brakes on
        
        Source: General Aviation Aircraft Design: Applied Methods and Procedures,
        by Snorri Gudmundsson, copyright 2014, published by Elsevier, Waltham,
        MA, USA [p.938]
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
        #   USER INPUTS
        # -------------------------------------------------------------------------------------------------------------- 
        
        self.velocity_start       = None
        self.velocity_end         = 150 * Units.knots
        self.friction_coefficient = 0.04
        self.throttle             = 1.0
        self.altitude             = 0.0
        self.true_course_angle    = 0.0 * Units.degrees 
        
        # initials and unknowns
        ones_row_m1                               = self.state.ones_row_m1
        self.state.unknowns.velocity_x            = ones_row_m1(1) * 0.0
        self.state.unknowns.time                  = 100.
        self.state.residuals.final_velocity_error = 0.0
        self.state.residuals.forces               = ones_row_m1(1) * 0.0        

        # -------------------------------------------------------------------------------------------------------------- 
        #   SOLVING PROCESS
        # --------------------------------------------------------------------------------------------------------------  
        initialize            = self.process.initialize
        initialize.conditions = Methods.Ground.Takeoff.initialize_conditions
        
        return


