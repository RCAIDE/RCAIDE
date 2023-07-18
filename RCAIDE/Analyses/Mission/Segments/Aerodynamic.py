## @ingroup Analyses-Mission-Segments
# RCAIDE/Analyses/Mission/Segment/Aerodynamic.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Analyses.Mission.Segments import Simple
from RCAIDE.Analyses.Mission.Segments import Conditions 
from RCAIDE.Methods.Missions          import Segments as Methods 
from RCAIDE.Analyses                  import Process

# Legacy imports
from Legacy.trunk.S.Methods.skip      import skip

# ----------------------------------------------------------------------------------------------------------------------
# Aerodynamic
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Analyses-Mission-Segments
class Aerodynamic(Simple):
    """ The third basic piece of a mission which each segment will expand upon
    
        Assumptions:
        There's a detailed process flow outline in defaults. A mission must be solved in that order.
        Assumes you're an atmospheric vehicle.
        
        Source:
        None
    """     
    
    def __defaults__(self):
        """This sets the default values.
    
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
        # self.example = 1.0
        
        # --------------------------------------------------------------------------------------------------------------
        #   STATE
        # --------------------------------------------------------------------------------------------------------------
        
        # conditions
        self.state.conditions.update( Conditions.Aerodynamics() )
        self.temperature_deviation = 0.0
        
        # --------------------------------------------------------------------------------------------------------------
        #   THE SOLVING PROCESS
        # --------------------------------------------------------------------------------------------------------------
        
        # --------------------------------------------------------------------------------------------------------------
        #   INITALIZE (BEFORE INTERATION)
        # --------------------------------------------------------------------------------------------------------------
        initialize                         = self.process.initialize 
        initialize.expand_state            = Methods.expand_state
        initialize.differentials           = Methods.Common.Numerics.initialize_differentials_dimensionless
        initialize.conditions              = None        
        
        # --------------------------------------------------------------------------------------------------------------
        #   CONVERGE (STARTS INTERATION)
        # --------------------------------------------------------------------------------------------------------------
        converge                           = self.process.converge 
        converge.converge_root             = Methods.converge_root        
        
        # --------------------------------------------------------------------------------------------------------------
        #   ITERATE
        # --------------------------------------------------------------------------------------------------------------
        iterate = self.process.iterate

        # Update Initials
        iterate.initials                   = Process()
        iterate.initials.time              = Methods.Common.Frames.initialize_time
        iterate.initials.weights           = Methods.Common.Weights.initialize_weights
        iterate.initials.inertial_position = Methods.Common.Frames.initialize_inertial_position
        iterate.initials.planet_position   = Methods.Common.Frames.initialize_planet_position
        
        # Unpack Unknowns
        iterate.unknowns                   = Process()
        iterate.unknowns.mission           = None  
        
        # Update Conditions
        iterate.conditions                 = Process()
        iterate.conditions.differentials   = Methods.Common.Numerics.update_differentials_time        
        iterate.conditions.altitude        = Methods.Common.Aerodynamics.update_altitude
        iterate.conditions.atmosphere      = Methods.Common.Aerodynamics.update_atmosphere
        iterate.conditions.gravity         = Methods.Common.Weights.update_gravity
        iterate.conditions.freestream      = Methods.Common.Aerodynamics.update_freestream
        iterate.conditions.orientations    = Methods.Common.Frames.update_orientations
        iterate.conditions.aerodynamics    = Methods.Common.Aerodynamics.update_aerodynamics
        iterate.conditions.stability       = Methods.Common.Aerodynamics.update_stability
        iterate.conditions.energy          = Methods.Common.Energy.update_thrust
        iterate.conditions.weights         = Methods.Common.Weights.update_weights
        iterate.conditions.forces          = Methods.Common.Frames.update_forces
        iterate.conditions.planet_position = Methods.Common.Frames.update_planet_position

        # Solve Residuals
        iterate.residuals = Process()

        # --------------------------------------------------------------------------------------------------------------
        #   FINALIZE (AFTER ITERATION)
        # ---------------------------------------------------------------------------------------------------------------
        finalize = self.process.finalize
        
        # Post Processing
        finalize.post_process                   = Process()        
        finalize.post_process.inertial_position = Methods.Common.Frames.integrate_inertial_horizontal_position
        finalize.post_process.stability         = Methods.Common.Aerodynamics.update_stability
        finalize.post_process.aero_derivatives  = skip
        finalize.post_process.noise             = Methods.Common.Noise.compute_noise
        
        return

