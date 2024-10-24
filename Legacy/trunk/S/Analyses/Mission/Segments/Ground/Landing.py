## @ingroup Analyses-Functions-Segments-Hover
# Landing.py
#
# Created:  
# Modified: Feb 2016, Andrew Wendorff

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------


# SUAVE imports
from .Ground import Ground
from Legacy.trunk.S.Methods.Missions import Segments as Methods

# Units
from Legacy.trunk.S.Core import Units

# ----------------------------------------------------------------------
#  Class
# ----------------------------------------------------------------------

## @ingroup Analyses-Functions-Segments-Hover
class Landing(Ground):
    """ Segment for landing. Integrates equations of motion
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

        self.velocity_start       = 150 * Units.knots
        self.velocity_end         = 0.0
        self.friction_coefficient = 0.4
        self.throttle             = 0.0
        self.altitude             = 0.0
        self.true_course          = 0.0 * Units.degrees 
        
        # initials and unknowns
        ones_row_m1 = self.state.ones_row_m1
        self.state.unknowns.velocity_x            = ones_row_m1(1) * 0.0
        self.state.unknowns.time                  = 100.
        self.state.residuals.final_velocity_error = 0.0
        self.state.residuals.forces               = ones_row_m1(1) * 0.0               
        
        # --------------------------------------------------------------
        #   The Solving Process
        # --------------------------------------------------------------
    
        initialize = self.process.initialize
        initialize.conditions_ground = Methods.Ground.Landing.initialize_conditions

        return