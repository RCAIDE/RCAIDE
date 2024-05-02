## @ingroup Analyses-Mission-Segments-Conditions
# RCAIDE/Framework/Analyses/Mission/Segments/Conditions/Results.py
# 
# 
# Created:  Jul 2023, M. Clarke 

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

## @ingroup Analyses-Mission-Segments-Conditions
class Results(Conditions):
    """ This builds upon Basic, which itself builds on conditions, to add the data structure for aerodynamic mission analyses.
    
        Assumptions:
        None
        
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
        
        self.tag                                              = 'results' 
 
        # start default row vectors
        ones_1col                                             = self.ones_row(1)  
        ones_3col                                             = self.ones_row(3)
        
        # ----------------------------------------------------------------------------------------------------------------------         
        # Frames 
        # ---------------------------------------------------------------------------------------------------------------------- 
        self.frames                                           = Conditions() 
        
        # inertial conditions
        self.frames.inertial                                  = Conditions()        
        self.frames.inertial.position_vector                  = ones_3col * 0
        self.frames.inertial.velocity_vector                  = ones_3col * 0
        self.frames.inertial.acceleration_vector              = ones_3col * 0
        self.frames.inertial.angular_velocity_vector          = ones_3col * 0
        self.frames.inertial.angular_acceleration_vector      = ones_3col * 0
        self.frames.inertial.gravity_force_vector             = ones_3col * 0
        self.frames.inertial.total_force_vector               = ones_3col * 0
        self.frames.inertial.total_moment_vector              = ones_3col * 0
        self.frames.inertial.time                             = ones_1col * 0
        self.frames.inertial.aircraft_range                   = ones_1col * 0
        
        # body conditions
        self.frames.body                                      = Conditions()        
        self.frames.body.inertial_rotations                   = ones_3col * 0
        self.frames.body.thrust_force_vector                  = ones_3col * 0
        self.frames.body.moment_vector                        = ones_3col * 0
        self.frames.body.transform_to_inertial                = np.empty([0,0,0])

        # wind frame conditions
        self.frames.wind                                      = Conditions()
        self.frames.wind.body_rotations                       = ones_3col * 0 # rotations in [X,Y,Z] -> [phi,theta,psi]
        self.frames.wind.velocity_vector                      = ones_3col * 0
        self.frames.wind.force_vector                         = ones_3col * 0
        self.frames.wind.moment_vector                        = ones_3col * 0
        self.frames.wind.transform_to_inertial                = np.empty([0,0,0]) 
              
        # planet frame conditions              
        self.frames.planet                                    = Conditions()
        self.frames.planet.start_time                         = None
        self.frames.planet.latitude                           = ones_1col * 0
        self.frames.planet.longitude                          = ones_1col * 0
        self.frames.planet.true_course_angle                  = np.empty([0,0,0])

        # ----------------------------------------------------------------------------------------------------------------------         
        # Freestream 
        # ----------------------------------------------------------------------------------------------------------------------    
        self.freestream                                       = Conditions()        
        self.freestream.velocity                              = ones_1col * 0
        self.freestream.mach_number                           = ones_1col * 0
        self.freestream.pressure                              = ones_1col * 0
        self.freestream.temperature                           = ones_1col * 0
        self.freestream.density                               = ones_1col * 0
        self.freestream.speed_of_sound                        = ones_1col * 0
        self.freestream.dynamic_viscosity                     = ones_1col * 0
        self.freestream.altitude                              = ones_1col * 0
        self.freestream.gravity                               = ones_1col * 0
        self.freestream.reynolds_number                       = ones_1col * 0
        self.freestream.dynamic_pressure                      = ones_1col * 0
        self.freestream.delta_ISA                             = ones_1col * 0

        # ----------------------------------------------------------------------------------------------------------------------         
        # Aerodynamics
        # ----------------------------------------------------------------------------------------------------------------------  
        self.aerodynamics                                     = Conditions() 
        
        # aerdynamic angles 
        self.aerodynamics.angles                              = Conditions()
        self.aerodynamics.angles.alpha                        = ones_1col * 0
        self.aerodynamics.angles.beta                         = ones_1col * 0
        self.aerodynamics.angles.gamma                        = ones_1col * 0
        self.aerodynamics.angles.phi                          = ones_1col * 0

        # aerodynamic coefficients 
        self.aerodynamics.coefficients                        = Conditions()
        self.aerodynamics.coefficients.lift                   = ones_1col * 0
        self.aerodynamics.coefficients.drag                   = ones_1col * 0
        
        # aerodynamic derivatives
        self.aerodynamics.derivatives                         = Conditions()
        self.aerodynamics.derivatives.dCL_dAlpha              = ones_1col * 0
        self.aerodynamics.derivatives.dCD_dAlpha              = ones_1col * 0
        self.aerodynamics.derivatives.dCL_dBeta               = ones_1col * 0
        self.aerodynamics.derivatives.dCD_dBeta               = ones_1col * 0
        self.aerodynamics.derivatives.dCL_dV                  = ones_1col * 0
        self.aerodynamics.derivatives.dCD_dV                  = ones_1col * 0
        self.aerodynamics.derivatives.dCL_dThrottle           = ones_1col * 0
        self.aerodynamics.derivatives.dCD_dThrottle           = ones_1col * 0
        
        self.aerodynamics.lift_breakdown                      = Conditions()
        self.aerodynamics.drag_breakdown                      = Conditions()
        self.aerodynamics.drag_breakdown.parasite             = Conditions()
        self.aerodynamics.drag_breakdown.compressible         = Conditions()
        self.aerodynamics.drag_breakdown.induced              = Conditions()

        # ----------------------------------------------------------------------------------------------------------------------
        # Stability
        # ----------------------------------------------------------------------------------------------------------------------
        self.control_surfaces                                 = Conditions()
        self.control_surfaces.elevator                        = Conditions()
        self.control_surfaces.elevator.deflection             = ones_1col * 0
        self.control_surfaces.rudder                          = Conditions()
        self.control_surfaces.rudder.deflection               = ones_1col * 0
        self.control_surfaces.flap                            = Conditions()
        self.control_surfaces.flap.deflection                 = ones_1col * 0
        self.control_surfaces.slat                            = Conditions()
        self.control_surfaces.slat.deflection                 = ones_1col * 0
        self.control_surfaces.aileron                         = Conditions()
        self.control_surfaces.aileron.deflection              = ones_1col * 0

        # ----------------------------------------------------------------------------------------------------------------------
        # Stability 
        # ----------------------------------------------------------------------------------------------------------------------  
        self.stability                                 = Conditions()
        self.stability.static                          = Conditions()

        # static stability
        self.stability.static_margin                   = ones_1col * 0

        self.stability.static.coefficients             = Conditions()
        self.stability.static.coefficients.lift        = ones_1col * 0
        self.stability.static.coefficients.drag        = ones_1col * 0
        self.stability.static.coefficients.CX          = ones_1col * 0
        self.stability.static.coefficients.CY          = ones_1col * 0
        self.stability.static.coefficients.CZ          = ones_1col * 0
        self.stability.static.coefficients.CL          = ones_1col * 0
        self.stability.static.coefficients.CM          = ones_1col * 0
        self.stability.static.coefficients.CN          = ones_1col * 0
        self.stability.static.coefficients.CM0         = ones_1col * 0

        self.stability.static.derivatives              = Conditions()
        self.stability.static.derivatives.CM_delta_e   = ones_1col * 0
        self.stability.static.derivatives.dCM_dalpha   = ones_1col * 0
        self.stability.static.derivatives.dCn_dbeta    = ones_1col * 0
        self.stability.static.derivatives.dCl_dbeta    = ones_1col * 0
        self.stability.static.derivatives.dCY_dbeta    = ones_1col * 0
        self.stability.static.derivatives.dCL_dalpha   = ones_1col * 0
        self.stability.static.derivatives.dCl_ddelta_a = ones_1col * 0
        self.stability.static.derivatives.dCn_ddelta_a = ones_1col * 0
        self.stability.static.derivatives.dCn_ddelta_r = ones_1col * 0

        
        # dynamic stability
        self.stability.dynamic                         = Conditions()
        self.stability.dynamic.pitch_rate              = ones_1col * 0
        self.stability.dynamic.roll_rate               = ones_1col * 0
        self.stability.dynamic.yaw_rate                = ones_1col * 0
        #self.stability.dynamic.derivatives.dCY_dp      = ones_1col * 0 # If uncomment this, there is an error. why?


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
        self.weights.total_moment_of_inertia                  = ones_3col * 0 # 3 total I(I_xx, I_yy, I_zz)? or 9(including I_xz etc)?
        self.weights.weight_breakdown                         = Conditions()
        self.weights.vehicle_mass_rate                        = ones_1col * 0