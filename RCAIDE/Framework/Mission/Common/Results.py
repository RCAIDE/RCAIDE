# RCAIDE/Framework/Functions/Segments/Conditions/Results.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Mission.Common import Conditions

# python imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------------------------------------------------- 
class Results(Conditions):
    """ This builds upon conditions, to add the data structure for aerodynamic mission analyses. 
    """ 
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            Coefficient subscritps:
                X      - force in X direction
                Y      - force in Y direction 
                Z      - force in Z direction
                
                lift  - force 
                drag  - force 
    
                L     - moment about X axis 
                M     - moment about Y axis 
                N     - moment about Z axis
                
                u     - velocity in X drection
                v     - velocity in Y drection
                w     - velocity in Z drection
                   
                p     - angular rate about X axis
                q     - angular rate about Y axis
                r     - angular rate about Z axis
    
        Source:
            None 
        """ 
        
        self.tag                                              = 'results' 
 
        # start default row vectors
        ones_1col                                             = self.ones_row(1)  
        ones_3col                                             = self.ones_row(3)
        
        # ----------------------------------------------------------------------------------------------------------------------         
        # Reference Values 
        # ----------------------------------------------------------------------------------------------------------------------  
        self.S_ref                                            = ones_1col * 0
        self.c_ref                                            = ones_1col * 0
        self.b_ref                                            = ones_1col * 0
        self.X_ref                                            = ones_1col * 0
        self.Y_ref                                            = ones_1col * 0
        self.Z_ref                                            = ones_1col * 0     
        
        # ----------------------------------------------------------------------------------------------------------------------         
        # Frames 
        # ---------------------------------------------------------------------------------------------------------------------- 
        self.frames                                           = Conditions()
        
        # inertial conditions
        self.frames.inertial                                                   = Conditions()        
        self.frames.inertial.position_vector                                   = ones_3col * 0
        self.frames.inertial.velocity_vector                                   = ones_3col * 0
        self.frames.inertial.acceleration_vector                               = ones_3col * 0
        self.frames.inertial.angular_velocity_vector                           = ones_3col * 0
        self.frames.inertial.angular_acceleration_vector                       = ones_3col * 0
        self.frames.inertial.gravity_force_vector                              = ones_3col * 0
        self.frames.inertial.total_force_vector                                = ones_3col * 0
        self.frames.inertial.total_moment_vector                               = ones_3col * 0
        self.frames.inertial.time                                              = ones_1col * 0
        self.frames.inertial.aircraft_range                                    = ones_1col * 0
                                                                               
        # body conditions                                                      
        self.frames.body                                                       = Conditions()        
        self.frames.body.inertial_rotations                                    = ones_3col * 0
        self.frames.body.thrust_force_vector                                   = ones_3col * 0
        self.frames.body.moment_vector                                         = ones_3col * 0
        self.frames.body.transform_to_inertial                                 = np.empty([0,0,0])
                                                                               
        # wind frame conditions                                                
        self.frames.wind                                                       = Conditions()
        self.frames.wind.body_rotations                                        = ones_3col * 0 # rotations in [X,Y,Z] -> [phi,theta,psi]
        self.frames.wind.velocity_vector                                       = ones_3col * 0
        self.frames.wind.force_vector                                          = ones_3col * 0
        self.frames.wind.moment_vector                                         = ones_3col * 0
        self.frames.wind.transform_to_inertial                                 = np.empty([0,0,0]) 
                                                                               
        # planet frame conditions                                              
        self.frames.planet                                                     = Conditions()
        self.frames.planet.start_time                                          = None
        self.frames.planet.latitude                                            = ones_1col * 0
        self.frames.planet.longitude                                           = ones_1col * 0
        self.frames.planet.true_course                                         = np.empty([0,0,0])

        # ----------------------------------------------------------------------------------------------------------------------         
        # Freestream 
        # ----------------------------------------------------------------------------------------------------------------------    
        self.freestream                                                        = Conditions()        
        self.freestream.velocity                                               = ones_1col * 0
        self.freestream.u                                                      = ones_1col * 0
        self.freestream.v                                                      = ones_1col * 0
        self.freestream.w                                                      = ones_1col * 0
        self.freestream.mach_number                                            = ones_1col * 0
        self.freestream.pressure                                               = ones_1col * 0
        self.freestream.temperature                                            = ones_1col * 0
        self.freestream.density                                                = ones_1col * 0
        self.freestream.speed_of_sound                                         = ones_1col * 0
        self.freestream.dynamic_viscosity                                      = ones_1col * 0
        self.freestream.altitude                                               = ones_1col * 0
        self.freestream.gravity                                                = ones_1col * 0
        self.freestream.reynolds_number                                        = ones_1col * 0
        self.freestream.dynamic_pressure                                       = ones_1col * 0
        self.freestream.delta_ISA                                              = ones_1col * 0

        # ----------------------------------------------------------------------------------------------------------------------         
        # Aerodynamics
        # ----------------------------------------------------------------------------------------------------------------------  
        self.aerodynamics                                                      = Conditions() 
                                                                               
        # aerdynamic angles                                                    
        self.aerodynamics.angles                                               = Conditions()
        self.aerodynamics.angles.alpha                                         = ones_1col * 0
        self.aerodynamics.angles.beta                                          = ones_1col * 0
        self.aerodynamics.angles.phi                                           = ones_1col * 0 
                                                                               
        # aerodynamic coefficients                                             
        self.aerodynamics.coefficients                                         = Conditions()
        self.aerodynamics.coefficients.lift                                    = ones_1col * 0
        self.aerodynamics.coefficients.drag                                    = ones_1col * 0     
                                                                               
        # aerodynamic coefficients                                             
        self.aerodynamics.coefficients                                         = Conditions()
        self.aerodynamics.coefficients.lift                                    = Conditions()
        self.aerodynamics.coefficients.lift.total                              = ones_1col * 0 
        self.aerodynamics.coefficients.lift.inviscid_wings                     = Conditions()
        self.aerodynamics.coefficients.lift.compressible_wings                 = Conditions() 
        self.aerodynamics.coefficients.drag                                    = Conditions()  
        self.aerodynamics.coefficients.drag.total                              = ones_1col * 0   
        self.aerodynamics.coefficients.drag.parasite                           = Conditions()
        self.aerodynamics.coefficients.drag.compressible                       = Conditions()
        self.aerodynamics.coefficients.drag.miscellaneous                      = Conditions()
        self.aerodynamics.coefficients.drag.induced                            = Conditions()
        self.aerodynamics.coefficients.drag.induced.inviscid_wings             = Conditions()
        self.aerodynamics.coefficients.drag.induced.total                      = ones_1col * 0  
        self.aerodynamics.coefficients.drag.spoiler                            = Conditions()

        # ----------------------------------------------------------------------------------------------------------------------
        # Control Surfaces 
        # ----------------------------------------------------------------------------------------------------------------------
        self.control_surfaces                                                  = Conditions()

        self.control_surfaces.aileron                                          = Conditions()
        self.control_surfaces.aileron.deflection                               = ones_1col * 0 
        self.control_surfaces.aileron.static_stability                         = Conditions()
        self.control_surfaces.aileron.static_stability.coefficients            = Conditions() 
        self.control_surfaces.aileron.static_stability.coefficients.lift       = ones_1col * 0        
        self.control_surfaces.aileron.static_stability.coefficients.drag       = ones_1col * 0           
        self.control_surfaces.aileron.static_stability.coefficients.X          = ones_1col * 0           
        self.control_surfaces.aileron.static_stability.coefficients.Y          = ones_1col * 0           
        self.control_surfaces.aileron.static_stability.coefficients.Z          = ones_1col * 0         
        self.control_surfaces.aileron.static_stability.coefficients.L          = ones_1col * 0         
        self.control_surfaces.aileron.static_stability.coefficients.M          = ones_1col * 0         
        self.control_surfaces.aileron.static_stability.coefficients.N          = ones_1col * 0           
        self.control_surfaces.aileron.static_stability.coefficients.e          = ones_1col * 0
        
        self.control_surfaces.elevator                                         = Conditions()
        self.control_surfaces.elevator.deflection                              = ones_1col * 0 
        self.control_surfaces.elevator.static_stability                        = Conditions()
        self.control_surfaces.elevator.static_stability.coefficients           = Conditions() 
        self.control_surfaces.elevator.static_stability.coefficients.lift      = ones_1col * 0        
        self.control_surfaces.elevator.static_stability.coefficients.drag      = ones_1col * 0           
        self.control_surfaces.elevator.static_stability.coefficients.X         = ones_1col * 0           
        self.control_surfaces.elevator.static_stability.coefficients.Y         = ones_1col * 0           
        self.control_surfaces.elevator.static_stability.coefficients.Z         = ones_1col * 0         
        self.control_surfaces.elevator.static_stability.coefficients.L         = ones_1col * 0         
        self.control_surfaces.elevator.static_stability.coefficients.M         = ones_1col * 0         
        self.control_surfaces.elevator.static_stability.coefficients.N         = ones_1col * 0           
        self.control_surfaces.elevator.static_stability.coefficients.e         = ones_1col * 0
        
        self.control_surfaces.rudder                                           = Conditions()
        self.control_surfaces.rudder.deflection                                = ones_1col * 0 
        self.control_surfaces.rudder.static_stability                          = Conditions()
        self.control_surfaces.rudder.static_stability.coefficients             = Conditions() 
        self.control_surfaces.rudder.static_stability.coefficients.lift        = ones_1col * 0         
        self.control_surfaces.rudder.static_stability.coefficients.drag        = ones_1col * 0          
        self.control_surfaces.rudder.static_stability.coefficients.X           = ones_1col * 0          
        self.control_surfaces.rudder.static_stability.coefficients.Y           = ones_1col * 0          
        self.control_surfaces.rudder.static_stability.coefficients.Z           = ones_1col * 0         
        self.control_surfaces.rudder.static_stability.coefficients.L           = ones_1col * 0         
        self.control_surfaces.rudder.static_stability.coefficients.M           = ones_1col * 0         
        self.control_surfaces.rudder.static_stability.coefficients.N           = ones_1col * 0           
        self.control_surfaces.rudder.static_stability.coefficients.e           = ones_1col * 0
        
        self.control_surfaces.flap                                             = Conditions()
        self.control_surfaces.flap.deflection                                  = ones_1col * 0 
        self.control_surfaces.flap.static_stability                            = Conditions()
        self.control_surfaces.flap.static_stability.coefficients               = Conditions() 
        self.control_surfaces.flap.static_stability.coefficients.lift          = ones_1col * 0        
        self.control_surfaces.flap.static_stability.coefficients.drag          = ones_1col * 0           
        self.control_surfaces.flap.static_stability.coefficients.X             = ones_1col * 0           
        self.control_surfaces.flap.static_stability.coefficients.Y             = ones_1col * 0           
        self.control_surfaces.flap.static_stability.coefficients.Z             = ones_1col * 0         
        self.control_surfaces.flap.static_stability.coefficients.L             = ones_1col * 0         
        self.control_surfaces.flap.static_stability.coefficients.M             = ones_1col * 0         
        self.control_surfaces.flap.static_stability.coefficients.N             = ones_1col * 0           
        self.control_surfaces.flap.static_stability.coefficients.e             = ones_1col * 0
        
        self.control_surfaces.slat                                             = Conditions()
        self.control_surfaces.slat.deflection                                  = ones_1col * 0 
        self.control_surfaces.slat.static_stability                            = Conditions()
        self.control_surfaces.slat.static_stability.coefficients               = Conditions() 
        self.control_surfaces.slat.static_stability.coefficients.lift          = ones_1col * 0         
        self.control_surfaces.slat.static_stability.coefficients.drag          = ones_1col * 0          
        self.control_surfaces.slat.static_stability.coefficients.X             = ones_1col * 0          
        self.control_surfaces.slat.static_stability.coefficients.Y             = ones_1col * 0          
        self.control_surfaces.slat.static_stability.coefficients.Z             = ones_1col * 0         
        self.control_surfaces.slat.static_stability.coefficients.L             = ones_1col * 0         
        self.control_surfaces.slat.static_stability.coefficients.M             = ones_1col * 0         
        self.control_surfaces.slat.static_stability.coefficients.N             = ones_1col * 0           
        self.control_surfaces.slat.static_stability.coefficients.e             = ones_1col * 0

        # ----------------------------------------------------------------------------------------------------------------------
        # Stability 
        # ----------------------------------------------------------------------------------------------------------------------  
        self.stability                                                         = Conditions()
        self.static_stability                                                  = Conditions()
 
        self.static_stability.forces                                           = Conditions()
        self.static_stability.forces.lift                                      = ones_1col * 0
        self.static_stability.forces.drag                                      = ones_1col * 0
        self.static_stability.forces.X                                         = ones_1col * 0
        self.static_stability.forces.Y                                         = ones_1col * 0
        self.static_stability.forces.Z                                         = ones_1col * 0
                                                                               
        self.static_stability.moments                                          = Conditions()
        self.static_stability.moments.L                                        = ones_1col * 0
        self.static_stability.moments.M                                        = ones_1col * 0
        self.static_stability.moments.N                                        = ones_1col * 0
                                                                               
        self.static_stability.static_margin                                    = ones_1col * 0
        self.static_stability.neutral_point                                    = ones_1col * 0
        self.static_stability.spiral_criteria                                  = ones_1col * 0 
        self.static_stability.pitch_rate                                       = ones_1col * 0
        self.static_stability.roll_rate                                        = ones_1col * 0
        self.static_stability.yaw_rate                                         = ones_1col * 0 
                                                                               
        self.static_stability.coefficients                                     = Conditions()
        self.static_stability.coefficients.lift                                = ones_1col * 0
        self.static_stability.coefficients.drag                                = ones_1col * 0
        self.static_stability.coefficients.X                                   = ones_1col * 0
        self.static_stability.coefficients.Y                                   = ones_1col * 0
        self.static_stability.coefficients.Z                                   = ones_1col * 0
        self.static_stability.coefficients.L                                   = ones_1col * 0
        self.static_stability.coefficients.M                                   = ones_1col * 0
        self.static_stability.coefficients.N                                   = ones_1col * 0  
                                                                               
        self.static_stability.derivatives                                      = Conditions()
                                                                               
        # stability axis                                                       
        self.static_stability.derivatives.Clift_alpha                          = ones_1col * 0
        self.static_stability.derivatives.Clift_beta                           = ones_1col * 0
        self.static_stability.derivatives.Clift_delta_a                        = ones_1col * 0
        self.static_stability.derivatives.Clift_delta_e                        = ones_1col * 0
        self.static_stability.derivatives.Clift_delta_r                        = ones_1col * 0
        self.static_stability.derivatives.Clift_delta_f                        = ones_1col * 0
        self.static_stability.derivatives.Clift_delta_s                        = ones_1col * 0
        self.static_stability.derivatives.Cdrag_alpha                          = ones_1col * 0
        self.static_stability.derivatives.Cdrag_beta                           = ones_1col * 0
        self.static_stability.derivatives.Cdrag_delta_a                        = ones_1col * 0
        self.static_stability.derivatives.Cdrag_delta_e                        = ones_1col * 0
        self.static_stability.derivatives.Cdrag_delta_r                        = ones_1col * 0
        self.static_stability.derivatives.Cdrag_delta_f                        = ones_1col * 0
        self.static_stability.derivatives.Cdrag_delta_s                        = ones_1col * 0
        self.static_stability.derivatives.CX_alpha                             = ones_1col * 0
        self.static_stability.derivatives.CX_beta                              = ones_1col * 0
        self.static_stability.derivatives.CX_delta_a                           = ones_1col * 0
        self.static_stability.derivatives.CX_delta_e                           = ones_1col * 0
        self.static_stability.derivatives.CX_delta_r                           = ones_1col * 0
        self.static_stability.derivatives.CX_delta_f                           = ones_1col * 0
        self.static_stability.derivatives.CX_delta_s                           = ones_1col * 0
        self.static_stability.derivatives.CY_alpha                             = ones_1col * 0
        self.static_stability.derivatives.CY_beta                              = ones_1col * 0
        self.static_stability.derivatives.CY_delta_a                           = ones_1col * 0
        self.static_stability.derivatives.CY_delta_e                           = ones_1col * 0
        self.static_stability.derivatives.CY_delta_r                           = ones_1col * 0
        self.static_stability.derivatives.CY_delta_f                           = ones_1col * 0
        self.static_stability.derivatives.CY_delta_s                           = ones_1col * 0
        self.static_stability.derivatives.CZ_alpha                             = ones_1col * 0
        self.static_stability.derivatives.CZ_beta                              = ones_1col * 0
        self.static_stability.derivatives.CZ_delta_a                           = ones_1col * 0
        self.static_stability.derivatives.CZ_delta_e                           = ones_1col * 0
        self.static_stability.derivatives.CZ_delta_r                           = ones_1col * 0
        self.static_stability.derivatives.CZ_delta_f                           = ones_1col * 0
        self.static_stability.derivatives.CZ_delta_s                           = ones_1col * 0
        self.static_stability.derivatives.CL_alpha                             = ones_1col * 0
        self.static_stability.derivatives.CL_beta                              = ones_1col * 0
        self.static_stability.derivatives.CL_delta_a                           = ones_1col * 0
        self.static_stability.derivatives.CL_delta_e                           = ones_1col * 0
        self.static_stability.derivatives.CL_delta_r                           = ones_1col * 0
        self.static_stability.derivatives.CL_delta_f                           = ones_1col * 0
        self.static_stability.derivatives.CL_delta_s                           = ones_1col * 0
        self.static_stability.derivatives.CM_alpha                             = ones_1col * 0
        self.static_stability.derivatives.CM_beta                              = ones_1col * 0
        self.static_stability.derivatives.CM_delta_a                           = ones_1col * 0
        self.static_stability.derivatives.CM_delta_e                           = ones_1col * 0
        self.static_stability.derivatives.CM_delta_r                           = ones_1col * 0
        self.static_stability.derivatives.CM_delta_f                           = ones_1col * 0
        self.static_stability.derivatives.CM_delta_s                           = ones_1col * 0
        self.static_stability.derivatives.CN_alpha                             = ones_1col * 0
        self.static_stability.derivatives.CN_beta                              = ones_1col * 0
        self.static_stability.derivatives.CN_delta_a                           = ones_1col * 0
        self.static_stability.derivatives.CN_delta_e                           = ones_1col * 0
        self.static_stability.derivatives.CN_delta_r                           = ones_1col * 0
        self.static_stability.derivatives.CN_delta_f                           = ones_1col * 0
        self.static_stability.derivatives.CN_delta_s                           = ones_1col * 0
        
        # body axis derivatives
        self.static_stability.derivatives.Clift_u                              = ones_1col * 0
        self.static_stability.derivatives.Clift_v                              = ones_1col * 0
        self.static_stability.derivatives.Clift_w                              = ones_1col * 0 
        self.static_stability.derivatives.Cdrag_u                              = ones_1col * 0
        self.static_stability.derivatives.Cdrag_v                              = ones_1col * 0
        self.static_stability.derivatives.Cdrag_w                              = ones_1col * 0         
        self.static_stability.derivatives.CX_u                                 = ones_1col * 0
        self.static_stability.derivatives.CX_v                                 = ones_1col * 0
        self.static_stability.derivatives.CX_w                                 = ones_1col * 0
        self.static_stability.derivatives.CY_u                                 = ones_1col * 0
        self.static_stability.derivatives.CY_v                                 = ones_1col * 0
        self.static_stability.derivatives.CY_w                                 = ones_1col * 0
        self.static_stability.derivatives.CZ_u                                 = ones_1col * 0
        self.static_stability.derivatives.CZ_v                                 = ones_1col * 0
        self.static_stability.derivatives.CZ_w                                 = ones_1col * 0
        self.static_stability.derivatives.CL_u                                 = ones_1col * 0
        self.static_stability.derivatives.CL_v                                 = ones_1col * 0
        self.static_stability.derivatives.CL_w                                 = ones_1col * 0
        self.static_stability.derivatives.CM_u                                 = ones_1col * 0
        self.static_stability.derivatives.CM_v                                 = ones_1col * 0
        self.static_stability.derivatives.CM_w                                 = ones_1col * 0
        self.static_stability.derivatives.CN_u                                 = ones_1col * 0
        self.static_stability.derivatives.CN_v                                 = ones_1col * 0
        self.static_stability.derivatives.CN_w                                 = ones_1col * 0
        
        self.static_stability.derivatives.Clift_p                              = ones_1col * 0
        self.static_stability.derivatives.Clift_q                              = ones_1col * 0
        self.static_stability.derivatives.Clift_r                              = ones_1col * 0
        self.static_stability.derivatives.Cdrag_p                              = ones_1col * 0
        self.static_stability.derivatives.Cdrag_q                              = ones_1col * 0
        self.static_stability.derivatives.Cdrag_r                              = ones_1col * 0         
        self.static_stability.derivatives.CX_p                                 = ones_1col * 0
        self.static_stability.derivatives.CX_q                                 = ones_1col * 0
        self.static_stability.derivatives.CX_r                                 = ones_1col * 0
        self.static_stability.derivatives.CY_p                                 = ones_1col * 0
        self.static_stability.derivatives.CY_q                                 = ones_1col * 0
        self.static_stability.derivatives.CY_r                                 = ones_1col * 0
        self.static_stability.derivatives.CZ_p                                 = ones_1col * 0
        self.static_stability.derivatives.CZ_q                                 = ones_1col * 0
        self.static_stability.derivatives.CZ_r                                 = ones_1col * 0
        self.static_stability.derivatives.CL_p                                 = ones_1col * 0
        self.static_stability.derivatives.CL_q                                 = ones_1col * 0
        self.static_stability.derivatives.CL_r                                 = ones_1col * 0
        self.static_stability.derivatives.CM_p                                 = ones_1col * 0
        self.static_stability.derivatives.CM_q                                 = ones_1col * 0
        self.static_stability.derivatives.CM_r                                 = ones_1col * 0
        self.static_stability.derivatives.CN_p                                 = ones_1col * 0
        self.static_stability.derivatives.CN_q                                 = ones_1col * 0
        self.static_stability.derivatives.CN_r                                 = ones_1col * 0 
                                                                               
        # dynamic stability                                                    
        self.dynamic_stability                                                 = Conditions()
        self.dynamic_stability.LongModes                                       = Conditions()
        self.dynamic_stability.LatModes                                        = Conditions()

        # ----------------------------------------------------------------------------------------------------------------------         
        # Noise 
        # ----------------------------------------------------------------------------------------------------------------------       
        self.noise                                            = Conditions() 

        # ----------------------------------------------------------------------------------------------------------------------         
        # Energy
        # ---------------------------------------------------------------------------------------------------------------------- 
        self.energy                                           = Conditions()
        self.energy.throttle                                  = ones_1col * 0  
        self.energy.thrust_breakdown                          = Conditions()     
        
        # ----------------------------------------------------------------------------------------------------------------------         
        # Weights 
        # ----------------------------------------------------------------------------------------------------------------------     
        self.weights                                          = Conditions() 
        self.weights.total_mass                               = ones_1col * 0
        self.weights.total_moment_of_inertia                  = ones_3col * 0  
        self.weights.weight_breakdown                         = Conditions()
        self.weights.vehicle_mass_rate                        = ones_1col * 0