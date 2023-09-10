## @ingroup Analyses-Mission-Segments-Hover
# RCAIDE/Analyses/Mission/Segments/Hover/Hover.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports
from RCAIDE.Analyses.Mission.Segments import Aerodynamic
from RCAIDE.Analyses.Mission.Segments import Conditions 
from RCAIDE.Methods.Missions          import Segments as Methods
from RCAIDE.Methods                   import skip 
from RCAIDE.Analyses                  import Process 
from RCAIDE.Core                      import Units

# ----------------------------------------------------------------------------------------------------------------------
#  Hover
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Analyses-Mission-Segments-Hover
class Hover(Aerodynamic):
    """ A stationary hover for VTOL aircraft. No aerodynamic drag and lift are used, since there is no velocity.
    
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
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   USER INPUTS
        # -------------------------------------------------------------------------------------------------------------- 
        
        self.altitude           = None
        self.time               = 1.0 * Units.seconds
        self.true_course_angle  = 0.0 * Units.degrees 
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   STATE
        # --------------------------------------------------------------------------------------------------------------
        
        # conditions
        self.state.conditions.update( Conditions.Aerodynamics() )
        
        # initials and unknowns
        ones_row = self.state.ones_row
        self.state.unknowns.throttle   = ones_row(1) * 0.5
        self.state.residuals.force     = ones_row(1) * 0.0 
        
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  THE SOLVING PROCESS
        # -------------------------------------------------------------------------------------------------------------- 
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  INITALIZE (BEFORE INTERATION)
        # -------------------------------------------------------------------------------------------------------------- 
        initialize = self.process.initialize
        
        initialize.expand_state            = Methods.expand_state
        initialize.differentials           = Methods.Common.Numerics.initialize_differentials_dimensionless
        initialize.conditions              = Methods.Hover.Hover.initialize_conditions

        # -------------------------------------------------------------------------------------------------------------- 
        #  CONVERGE (STARTS INTERATION)
        # -------------------------------------------------------------------------------------------------------------- 
        converge                           = self.process.converge 
        converge.converge_root             = Methods.converge_root        

        # -------------------------------------------------------------------------------------------------------------- 
        #  ITERATE
        # --------------------------------------------------------------------------------------------------------------
        iterate                            = self.process.iterate 
        iterate.initials                   = Process()
        iterate.initials.time              = Methods.Common.Frames.initialize_time
        iterate.initials.weights           = Methods.Common.Weights.initialize_weights
        iterate.initials.energy            = Methods.Common.Energy.initialize_energy
        iterate.initials.inertial_position = Methods.Common.Frames.initialize_inertial_position
        iterate.initials.planet_position   = Methods.Common.Frames.initialize_planet_position
        
        # Unpack Unknowns
        iterate.unknowns                   = Process()
        iterate.unknowns.mission           = Methods.Hover.Common.unpack_unknowns
        
        # Update Conditions
        iterate.conditions                 = Process()
        iterate.conditions.differentials   = Methods.Common.Numerics.update_differentials_time
        iterate.conditions.altitude        = Methods.Common.Aerodynamics.update_altitude
        iterate.conditions.atmosphere      = Methods.Common.Aerodynamics.update_atmosphere
        iterate.conditions.gravity         = Methods.Common.Weights.update_gravity
        iterate.conditions.freestream      = Methods.Common.Aerodynamics.update_freestream
        iterate.conditions.orientations    = Methods.Common.Frames.update_orientations
        iterate.conditions.energy          = Methods.Common.Energy.update_thrust
        iterate.conditions.weights         = Methods.Common.Weights.update_weights
        iterate.conditions.forces          = Methods.Common.Frames.update_forces
        iterate.conditions.planet_position = Methods.Common.Frames.update_planet_position

        # Solve Residuals
        iterate.residuals = Process()     
        iterate.residuals.total_forces     = Methods.Hover.Common.residual_total_forces
        
        # -------------------------------------------------------------------------------------------------------------- 
        # FINALIZE (AFTER ITERATION)
        # -------------------------------------------------------------------------------------------------------------- 
        finalize = self.process.finalize
        
        # Post Processing
        finalize.post_process = Process()        
        finalize.post_process.inertial_position = Methods.Common.Frames.integrate_inertial_horizontal_position
        finalize.post_process.update_battery_age= Methods.Common.Energy.update_battery_age
        finalize.post_process.stability         = Methods.Common.Aerodynamics.update_stability
        finalize.post_process.aero_derivatives  = skip
        finalize.post_process.noise             = Methods.Common.Noise.compute_noise 
        
        return

