# RCAIDE/Analyses/Mission/Segments/Climb/Constant_Throttle_Constant_Speed.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Core                      import Units
from RCAIDE.Analyses                  import Process
from RCAIDE.Methods.Missions          import Segments as Methods  
from RCAIDE.Analyses.Mission.Segments import Aerodynamic
from RCAIDE.Analyses.Mission.Segments import Conditions 

# legacy imports 
from Legacy.trunk.S.Methods.skip      import skip 

# ----------------------------------------------------------------------------------------------------------------------
#  SEGMENT
# ---------------------------------------------------------------------------------------------------------------------- 
 
## @ingroup Analyses-Mission-Segments-Climb
class Constant_Throttle_Constant_Speed(Aerodynamic):
    """ Climb at a constant throttle setting and true airspeed. This segment may not always converge as the vehicle 
        could be deficient in thrust. Useful as a check to see the climb rate at the top of climb.
    
        Assumptions:
        You set a reasonable throttle setting that can provide enough thrust.
        
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
        self.altitude_start    = None # Optional
        self.altitude_end      = 10. * Units.km
        self.throttle          = 0.5
        self.air_speed         = None
        self.true_course_angle = 0.0 * Units.degrees            

        # -------------------------------------------------------------------------------------------------------------- 
        #   STATE
        # --------------------------------------------------------------------------------------------------------------      
        
        # conditions
        self.state.conditions.update( Conditions.Aerodynamics() )
        
        # initials and unknowns
        ones_row                       = self.state.ones_row
        self.state.unknowns.body_angle = ones_row(1) * 5.0 * Units.deg
        self.state.unknowns.wind_angle = ones_row(1) * 1.0 * Units.deg
        self.state.residuals.forces    = ones_row(2) * 0.0  
         
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  INITALIZE (BEFORE INTERATION)
        # -------------------------------------------------------------------------------------------------------------- 
        initialize                         = self.process.initialize 
        initialize.expand_state            = Methods.expand_state
        initialize.differentials           = Methods.Common.Numerics.initialize_differentials_dimensionless
        initialize.conditions              = Methods.Climb.Constant_Throttle_Constant_Speed.initialize_conditions
        initialize.velocities              = Methods.Climb.Constant_Throttle_Constant_Speed.update_velocity_vector_from_wind_angle
        initialize.differentials_altitude  = Methods.Climb.Constant_Throttle_Constant_Speed.update_differentials_altitude      
        
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
        iterate.initials.inertial_position = Methods.Common.Frames.initialize_inertial_position
        iterate.initials.planet_position   = Methods.Common.Frames.initialize_planet_position
        
        # Unpack Unknowns
        iterate.unknowns                   = Process()
        iterate.unknowns.mission           = Methods.Climb.Constant_Throttle_Constant_Speed.unpack_body_angle 
        
        # Update Conditions
        iterate.conditions                 = Process()
        iterate.conditions.velocities      = Methods.Climb.Constant_Throttle_Constant_Speed.update_velocity_vector_from_wind_angle
        iterate.conditions.differentials_a = Methods.Climb.Constant_Throttle_Constant_Speed.update_differentials_altitude
        iterate.conditions.differentials_b = Methods.Common.Numerics.update_differentials_time
        iterate.conditions.acceleration    = Methods.Common.Frames.update_acceleration
        iterate.conditions.altitude        = Methods.Common.Aerodynamics.update_altitude
        iterate.conditions.atmosphere      = Methods.Common.Aerodynamics.update_atmosphere
        iterate.conditions.gravity         = Methods.Common.Weights.update_gravity
        iterate.conditions.freestream      = Methods.Common.Aerodynamics.update_freestream
        iterate.conditions.orientations    = Methods.Common.Frames.update_orientations
        iterate.conditions.propulsion      = Methods.Common.Energy.update_thrust        
        iterate.conditions.aerodynamics    = Methods.Common.Aerodynamics.update_aerodynamics
        iterate.conditions.stability       = Methods.Common.Aerodynamics.update_stability
        iterate.conditions.weights         = Methods.Common.Weights.update_weights
        iterate.conditions.forces          = Methods.Common.Frames.update_forces
        iterate.conditions.planet_position = Methods.Common.Frames.update_planet_position
        
        # Solve Residuals
        iterate.residuals                  = Process()
        iterate.residuals.total_forces     = Methods.Climb.Common.residual_total_forces
        
        # -------------------------------------------------------------------------------------------------------------- 
        # FINALIZE (AFTER ITERATION)
        # --------------------------------------------------------------------------------------------------------------  
        finalize                                = self.process.finalize 
        finalize.post_process                   = Process()        
        finalize.post_process.inertial_position = Methods.Common.Frames.integrate_inertial_horizontal_position
        finalize.post_process.stability         = Methods.Common.Aerodynamics.update_stability
        finalize.post_process.aero_derivatives  = skip
        finalize.post_process.noise             = Methods.Common.Noise.compute_noise
       
        return

