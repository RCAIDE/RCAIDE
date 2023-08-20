## @ingroup Analyses-Mission-Segments-Conditions
# RCAIDE/Analyses/Mission/Segments/Conditions/Aerodynamics.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from .Basic      import Basic
from .Conditions import Conditions

# python imports
import numpy as np


# ----------------------------------------------------------------------------------------------------------------------
# Aerodynamics
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Analyses-Mission-Segments-Conditions
class Aerodynamics(Basic):
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
        
        self.tag                                              = 'aerodynamic_conditions'
        
        # start default row vectors
        ones_1col                                             = self.ones_row(1)  
        ones_3col                                             = self.ones_row(3)

        # wind frame conditions
        self.frames.wind                                      = Conditions()
        self.frames.wind.body_rotations                       = ones_3col * 0 # rotations in [X,Y,Z] -> [phi,theta,psi]
        self.frames.wind.velocity_vector                      = ones_3col * 0
        self.frames.wind.lift_force_vector                    = ones_3col * 0
        self.frames.wind.drag_force_vector                    = ones_3col * 0
        self.frames.wind.transform_to_inertial                = np.empty([0,0,0])
               
        # body frame conditions               
        self.frames.body.thrust_force_vector                  = ones_3col * 0
              
        # planet frame conditions              
        self.frames.planet                                    = Conditions()
        self.frames.planet.start_time                         = None
        self.frames.planet.latitude                           = ones_1col * 0
        self.frames.planet.longitude                          = ones_1col * 0
        self.frames.planet.true_course_angle                  = np.empty([0,0,0])
              
        # freestream conditions              
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

        # aerodynamics conditions
        self.aerodynamics                                     = Conditions()        
        self.aerodynamics.angle_of_attack                     = ones_1col * 0
        self.aerodynamics.side_slip_angle                     = ones_1col * 0
        self.aerodynamics.roll_angle                          = ones_1col * 0
        self.aerodynamics.lift_coefficient                    = ones_1col * 0
        self.aerodynamics.drag_coefficient                    = ones_1col * 0
        self.aerodynamics.lift_breakdown                      = Conditions()
        self.aerodynamics.drag_breakdown                      = Conditions()
        self.aerodynamics.drag_breakdown.parasite             = Conditions()
        self.aerodynamics.drag_breakdown.compressible         = Conditions()
        self.aerodynamics.drag_breakdown.induced              = Conditions()

        # stability conditions
        self.stability                                        = Conditions()        
        self.stability.static                                 = Conditions()
        self.stability.dynamic                                = Conditions() 
        self.stability.static.CM                              = ones_1col * 0
        self.stability.static.Cm_alpha                        = ones_1col * 0
        self.stability.static.static_margin                   = ones_1col * 0
        self.stability.dynamic.pitch_rate                     = ones_1col * 0
        self.stability.dynamic.roll_rate                      = ones_1col * 0
        self.stability.dynamic.yaw_rate                       = ones_1col * 0     
                         
        # aerodynamic derivative conditions                 
        self.aero_derivatives                                 = Conditions()
        self.aero_derivatives.dCL_dAlpha                      = ones_1col * 0
        self.aero_derivatives.dCD_dAlpha                      = ones_1col * 0
        self.aero_derivatives.dCL_dBeta                       = ones_1col * 0
        self.aero_derivatives.dCD_dBeta                       = ones_1col * 0
        self.aero_derivatives.dCL_dV                          = ones_1col * 0
        self.aero_derivatives.dCD_dV                          = ones_1col * 0
        self.aero_derivatives.dCL_dThrottle                   = ones_1col * 0
        self.aero_derivatives.dCD_dThrottle                   = ones_1col * 0

        # propulsion conditions
        self.energy                                           = Conditions()
        self.energy.throttle                                  = ones_1col * 0  
        self.energy.thrust_breakdown                          = Conditions()    
        
        # weights conditions        
        self.weights.vehicle_mass_rate                        = ones_1col * 0
        self.weights.vehicle_fuel_rate                        = ones_1col * 0
        self.weights.vehicle_additional_fuel_rate             = ones_1col * 0
        self.weights.has_additional_fuel                      = False
                
        # noise conditions        
        self.noise                                            = Conditions()
        self.noise.total                                      = Conditions()
        self.noise.sources                                    = Conditions() 
        self.noise.sources.rotors                             = Conditions()