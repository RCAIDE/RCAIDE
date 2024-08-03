# RCAIDE/Framework/Functions/Segments/Ground/Takeoff.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Missions.Mission import Evaluate
from RCAIDE.Reference.Core import Units, Data
from RCAIDE.Reference.Missions.Functions.Common import Unpack_Unknowns, Update, Residuals


# ----------------------------------------------------------------------------------------------------------------------
#  Takeoff
# ----------------------------------------------------------------------------------------------------------------------
class Takeoff(Evaluate):
    """ Segment for takeoff. Integrates equations of motion including rolling friction.
        
        Assumptions:
            Notes Regarding Friction Coefficients
            Dry asphalt or concrete: .04 brakes off, .4 brakes on
            Wet asphalt or concrete: .05 brakes off, .225 brakes on
            Icy asphalt or concrete: .02 brakes off, .08 brakes on
            Hard turf:               .05 brakes off, .4 brakes on
            Firm dirt:               .04 brakes off, .3 brakes on
            Soft turf:               .07 brakes off, .2 brakes on
            Wet grass:               .08 brakes off, .2 brakes on
        
        Source: 
            General Aviation Aircraft Design: Applied Methods and Procedures,
            by Snorri Gudmundsson, copyright 2014, published by Elsevier, Waltham,
            MA, USA [p.938] 
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
        self.velocity_start       = None
        self.velocity_end         = 150 * Units.knots
        self.friction_coefficient = 0.04
        self.throttle             = 1.0
        self.altitude             = 0.0
        self.true_course          = 0.0 * Units.degrees  

        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions Conditions
        # --------------------------------------------------------------------------------------------------------------          
        ones_row = self.state.ones_row  
        self.state.conditions.ground                              = Data() 
        self.state.conditions.ground.friction_coefficient         = ones_row(1) * 0.0
        self.state.conditions.frames.inertial.ground_force_vector = ones_row(3) * 0.0  

        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions specific processes
        # --------------------------------------------------------------------------------------------------------------  
        initialize                         = self.process.initialize
        initialize.conditions              = RCAIDE.Framework.Mission.Mission.Segments.Ground.Takeoff.initialize_conditions
        iterate                            = self.process.iterate   
        iterate.conditions.forces_ground   = Update.ground_forces
        iterate.unknowns.mission           = Unpack_Unknowns.ground
        iterate.residuals.flight_dynamics  = Residuals.flight_dynamics
        
        return


