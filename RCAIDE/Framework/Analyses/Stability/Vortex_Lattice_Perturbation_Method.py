## @ingroup Analyses-Aerodynamics
# RCAIDE/Framework/Analyses/Aerodynamics/Subsonic_VLM_Perturbation_Method.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core                                     import Data, Units
from RCAIDE.Framework.Analyses                                 import Process 
from RCAIDE.Library.Methods.Aerodynamics                       import Common
from .Stability                                                import Stability  
from RCAIDE.Framework.Analyses.Common.Process_Geometry         import Process_Geometry 
from RCAIDE.Library.Methods.Aerodynamics.Vortex_Lattice_Method import *   

# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Vortex_Lattice_Perturbation_Method
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Analyses-Aerodynamics
class Vortex_Lattice_Perturbation_Method(Stability):
    """This is a subsonic aerodynamic buildup analysis based on the vortex lattice method

     Assumptions:
     Stall effects are negligible 
 
     Source:
     N/A
 
     Inputs:
     None
 
     Outputs:
     None
 
     Properties Used:
     N/A 
    """      
    
    def __defaults__(self):
        """This sets the default values and methods for the analysis.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """          
        self.tag                                    = 'Subsonic_Zero_VLM'  
        self.geometry                               = Data()  
        self.process                                = Process()
        self.process.initialize                     = Process()   
        
        # correction factors
        settings                                    = self.settings
        settings.fuselage_lift_correction           = 1.14
        settings.trim_drag_correction_factor        = 1.02
        settings.wing_parasite_drag_form_factor     = 1.1
        settings.fuselage_parasite_drag_form_factor = 2.3
        settings.maximum_lift_coefficient_factor    = 1.0        
        settings.lift_to_drag_adjustment            = 0.  
        settings.viscous_lift_dependent_drag_factor = 0.38
        settings.drag_coefficient_increment         = 0.0000
        settings.spoiler_drag_increment             = 0.00 
        settings.leading_edge_suction_multiplier    = 1.0  
        settings.maximum_lift_coefficient           = np.inf 
        settings.oswald_efficiency_factor           = None
        settings.span_efficiency                    = None
        settings.recalculate_total_wetted_area      = False
        settings.propeller_wake_model               = False 
        settings.model_fuselage                     = False 
        settings.discretize_control_surfaces        = True 
        settings.use_surrogate                      = True
        settings.trim_aircraft                      = True 
        
        settings.number_of_spanwise_vortices        = 15
        settings.number_of_chordwise_vortices       = 5
        settings.wing_spanwise_vortices             = None
        settings.wing_chordwise_vortices            = None
        settings.fuselage_spanwise_vortices         = None
        settings.fuselage_chordwise_vortices        = None  
        settings.spanwise_cosine_spacing            = True
        settings.vortex_distribution                = Data()  
        settings.use_VORLAX_matrix_calculation      = False
        settings.floating_point_precision           = np.float32 
    

        # conditions table, used for surrogate model training
        self.training                              = Data()
       
        self.training.angle_of_attack              = np.array([-10, -7.5, -5, -2.5, 1E-12, 2.5, 5, 7.5, 10, 12., 45., 75.]) * Units.deg 
        self.training.Mach                         = np.array([0.1 , 0.2 , 0.3,  0.5,  0.75 , 0.85 , 0.9, 1.3, 1.35 , 1.5 , 2.0, 2.25 , 2.5  , 3.0  , 3.5])  
        
        self.training.subsonic                     = None
        self.training.supersonic                   = None
        self.training.transonic                    = None
              
        self.training.sideslip_angle               = np.array([5.0 , 0.0]) * Units.deg
        self.training.aileron_deflection           = np.array([1.0 , 0.0]) * Units.deg
        self.training.elevator_deflection          = np.array([1.0 , 0.0]) * Units.deg   
        self.training.rudder_deflection            = np.array([1.0 , 0.0]) * Units.deg
        self.training.flap_deflection              = np.array([1.0 , 0.0])* Units.deg 
        self.training.slat_deflection              = np.array([1.0 , 0.0]) * Units.deg                      
        self.training.u                            = np.array([0.1 , 0.0])  
        self.training.v                            = np.array([0.1 , 0.0])  
        self.training.w                            = np.array([0.1 , 0.0])    
        self.training.pitch_rate                   = np.array([0.0 , 0.01])  * Units.rad / Units.sec
        self.training.roll_rate                    = np.array([0.3 , 0.0])  * Units.rad / Units.sec
        self.training.yaw_rate                     = np.array([0.01, 0.0])  * Units.rad / Units.sec
     
        # control surface flags 
        self.aileron_flag                          = False 
        self.flap_flag                             = False 
        self.rudder_flag                           = False 
        self.elevator_flag                         = False 
        self.slat_flag                             = False
        
        # blending function 
        self.hsub_min                              = 0.85
        self.hsub_max                              = 0.95
        self.hsup_min                              = 1.05
        self.hsup_max                              = 1.25 
    
        # surrogoate models
        self.surrogates                            = Data() 
        

    def initialize(self):  
        use_surrogate             = self.settings.use_surrogate  

        # If we are using the surrogate
        if use_surrogate == True: 
            # sample training data
            train_VLM_surrogates(self)

            # build surrogate
            build_VLM_surrogates(self)  
    
        # build the evaluation process
        compute                                    = Process() 
        compute.lift                               = Process()
        if use_surrogate == True: 
            compute.lift.inviscid_wings                = evaluate_surrogate
        else:
            compute.lift.inviscid_wings  = evaluate_no_surrogate
        compute.lift.vortex                        = RCAIDE.Library.Methods.skip
        compute.lift.fuselage                      = Common.Lift.fuselage_correction 
        compute.drag                               = Process()
        compute.drag.parasite                      = Process()
        compute.drag.parasite.wings                = Process_Geometry('wings')
        compute.drag.parasite.wings.wing           = Common.Drag.parasite_drag_wing 
        compute.drag.parasite.fuselages            = Process_Geometry('fuselages')
        compute.drag.parasite.fuselages.fuselage   = Common.Drag.parasite_drag_fuselage
        compute.drag.parasite.booms                = Process_Geometry('booms')
        compute.drag.parasite.booms.boom           = Common.Drag.parasite_drag_fuselage 
        compute.drag.parasite.nacelles             = Common.Drag.parasite_drag_nacelle
        compute.drag.parasite.pylons               = Common.Drag.parasite_drag_pylon
        compute.drag.parasite.total                = Common.Drag.parasite_total
        compute.drag.induced                       = Common.Drag.induced_drag_aircraft
        compute.drag.compressibility               = Process()
        compute.drag.compressibility.wings         = Process_Geometry('wings')
        compute.drag.compressibility.wings.wing    = Common.Drag.compressibility_drag_wing
        compute.drag.compressibility.total         = Common.Drag.compressibility_drag_wing_total
        compute.drag.miscellaneous                 = Common.Drag.miscellaneous_drag_aircraft
        compute.drag.untrimmed_drag                = Common.Drag.untrimmed_drag
        compute.drag.trimmed_drag                  = Common.Drag.trimmed_drag
        compute.drag.spoiler                       = Common.Drag.spoiler_drag
        compute.drag.total                         = Common.Drag.total_drag
        compute.stability                          = Process()
        compute.stability.dynamic_modes            = RCAIDE.Library.Methods.Stability.Common.compute_dynamic_flight_modes 
        self.process.compute                       = compute            

        return 
    
         
    def evaluate(self,state):
        """The default evaluate function.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        results   <RCAIDE data class>

        Properties Used:
        self.settings
        self.geometry
        """          
        settings = self.settings
        geometry = self.geometry 
        results  = self.process.compute(state,settings,geometry)
        
        return results