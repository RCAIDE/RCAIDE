## @ingroup Analyses-Mission-Segments-Conditions
# RCAIDE/Analyses/Mission/Segments/Conditions/Results.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Analyses.Mission.Common import Conditions

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
        self.frames.inertial.gravity_force_vector             = ones_3col * 0
        self.frames.inertial.total_force_vector               = ones_3col * 0
        self.frames.inertial.time                             = ones_1col * 0
        self.frames.inertial.aircraft_range                   = ones_1col * 0
        
        # body conditions
        self.frames.body                                      = Conditions()        
        self.frames.body.inertial_rotations                   = ones_3col * 0
        self.frames.body.thrust_force_vector                  = ones_3col * 0
        self.frames.body.transform_to_inertial                = np.empty([0,0,0]) 

        # wind frame conditions
        self.frames.wind                                      = Conditions()
        self.frames.wind.body_rotations                       = ones_3col * 0 # rotations in [X,Y,Z] -> [phi,theta,psi]
        self.frames.wind.velocity_vector                      = ones_3col * 0
        self.frames.wind.lift_force_vector                    = ones_3col * 0
        self.frames.wind.drag_force_vector                    = ones_3col * 0
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
        self.stability                                        = Conditions()        
        
        # static stability 
        self.stability.static                                 = Conditions()
        self.stability.static.CM                              = ones_1col * 0
        self.stability.static.Cm_alpha                        = ones_1col * 0
        self.stability.static.static_margin                   = ones_1col * 0
        
        # dynamic stability 
        self.stability.dynamic                                = Conditions() 
        self.stability.dynamic.pitch_rate                     = ones_1col * 0
        self.stability.dynamic.roll_rate                      = ones_1col * 0
        self.stability.dynamic.yaw_rate                       = ones_1col * 0     

        # ----------------------------------------------------------------------------------------------------------------------         
        # Noise 
        # ----------------------------------------------------------------------------------------------------------------------       
        self.noise                                            = Conditions()
        self.noise.total                                      = Conditions()
        self.noise.sources                                    = Conditions() 
        self.noise.sources.rotors                             = Conditions()

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
        self.weights.weight_breakdown                         = Conditions() 
        self.weights.vehicle_mass_rate                        = ones_1col * 0