## @ingroup Framework-Analyses-Stability
# RCAIDE/Framework/Analyses/Stability/VLM_Perturbation_Method.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core                                  import Data , Units
from RCAIDE.Framework.Analyses                              import Process  
from RCAIDE.Framework.Analyses.Common.Process_Geometry      import Process_Geometry   
from RCAIDE.Library.Methods.Aerodynamics                    import Common
from RCAIDE.Library.Methods.Stability.VLM_stability_solver  import *  
from .Stability                                             import Stability 

# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  VLM_Perturbation_Method
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Framework-Analyses-Stability
class VLM_Perturbation_Method(Stability):  
    """ This is a subsonic stability buildup analysis based on a pertubation approch of the vortex lattice method.
    """      

    def __defaults__(self):
        """This sets the default values and methods for the analysis.         

        Assumptions:
           None

        Source:
            None 
        """          
        self.tag                                         = 'VLM_Perturbation_Method'  
        self.geometry                                    = Data()  
        self.process                                     = Process()
        self.process.initialize                          = Process()   

        # correction factors
        settings                                         = self.settings 
        settings.fuselage_lift_correction                = 1.14
        settings.trim_drag_correction_factor             = 1.02
        settings.wing_parasite_drag_form_factor          = 1.1
        settings.fuselage_parasite_drag_form_factor      = 2.3
        settings.maximum_lift_coefficient_factor         = 1.0        
        settings.lift_to_drag_adjustment                 = 0.  
        settings.oswald_efficiency_factor                = None
        settings.span_efficiency                         = None
        settings.viscous_lift_dependent_drag_factor      = 0.38
        settings.drag_coefficient_increment              = 0.0000
        settings.spoiler_drag_increment                  = 0.00 
        settings.maximum_lift_coefficient                = np.inf 
        settings.use_surrogate                           = True
        settings.recalculate_total_wetted_area           = False
        settings.propeller_wake_model                    = False 
        settings.discretize_control_surfaces             = False
        settings.model_fuselage                          = False   
        settings.begin_drag_rise_mach_number             = 0.95
        settings.end_drag_rise_mach_number               = 1.2
        settings.transonic_drag_multiplier               = 1.25   
        settings.peak_mach_number                        = 1.04
        settings.cross_sectional_area_calculation_type   = 'Fixed'     
        settings.wave_drag_type                          = 'Raymer'
        settings.volume_wave_drag_scaling                = 3.2  
        settings.fuselage_parasite_drag_begin_blend_mach = 0.91
        settings.fuselage_parasite_drag_end_blend_mach   = 0.99  
        settings.number_of_spanwise_vortices             = 25
        settings.number_of_chordwise_vortices            = 5
        settings.wing_spanwise_vortices                  = None
        settings.wing_chordwise_vortices                 = None
        settings.fuselage_spanwise_vortices              = None
        settings.fuselage_chordwise_vortices             = None  
        settings.spanwise_cosine_spacing                 = True
        settings.vortex_distribution                     = Data()   
        settings.model_fuselage                          = False    
        settings.leading_edge_suction_multiplier         = 1.0
        settings.propeller_wake_model                    = False
        settings.discretize_control_surfaces             = True 
        settings.use_VORLAX_matrix_calculation           = False
        settings.floating_point_precision                = np.float32
        settings.use_surrogate                           = True

        # conditions table, used for surrogate model training
        self.training                                 = Data()
        self.training.Mach                            = np.array([0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5])        
        self.training.angle_of_attack                 = np.array([-10, -7.5, -5, -2.5, 1E-12, 2.5, 5, 7.5, 10]) * Units.deg     
        self.training.sideslip_angle                  = np.array([0, 5]) * Units.deg
        self.training.aileron_deflection              = np.array([0, 1]) * Units.deg
        self.training.elevator_deflection             = np.array([0, 1]) * Units.deg   
        self.training.rudder_deflection               = np.array([0, 1]) * Units.deg
        self.training.flap_deflection                 = np.array([0, 1])* Units.deg 
        self.training.slat_deflection                 = np.array([0, 1]) * Units.deg                      
        self.training.u                               = np.array([0, 0.1])  
        self.training.v                               = np.array([0, 0.1])  
        self.training.w                               = np.array([0, 0.1])    
        self.training.pitch_rate                      = np.array([0, 0.01])  * Units.rad / Units.sec
        self.training.roll_rate                       = np.array([0, 0.3])  * Units.rad / Units.sec
        self.training.yaw_rate                        = np.array([0, 0.01])  * Units.rad / Units.sec

        self.surrogates                               = Data()
        
        self.aileron_flag                             = False 
        self.flap_flag                                = False 
        self.rudder_flag                              = False 
        self.elevator_flag                            = False 
        self.slat_flag                                = False 
    
        # build the evaluation process
        compute                                    = Process() 
        compute.lift                               = Process() 
        compute.lift.inviscid_wings                = None
        compute.lift.vortex                        = RCAIDE.Library.Methods.skip
        compute.lift.fuselage                      = Common.Lift.fuselage_correction
        compute.lift.total                         = Common.Lift.total_lift  
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
        compute.drag.untrimmed                     = Common.Drag.untrimmed_drag
        compute.drag.trimmed                       = Common.Drag.trimmed_drag
        compute.drag.spoiler                       = Common.Drag.spoiler_drag
        compute.drag.total                         = Common.Drag.total_drag
        self.process.compute                       = compute   
    
    def initialize(self): 
        """Initalizes the subsonic Vortex Lattice Method stabiltiy method.

        Assumptions:
            None

        Source:
            None

        Args:
            self     : stability analysis  [-] 

        Returs:
            None
        """           
        use_surrogate             = self.settings.use_surrogate  

        # If we are using the surrogate
        if use_surrogate == True: 
            # sample training data
            sample_training(self)

            # build surrogate
            build_surrogate(self)  

        if use_surrogate == True: 
            self.process.compute.lift.inviscid_wings  = evaluate_surrogate
        else:
            self.process.compute.lift.inviscid_wings  = evaluate_no_surrogate

    def evaluate(self,state: dict):
        """Vortex Lattice Method pertubation evaluate function which calls listed processes in the analysis method.

        Assumptions:
            None

        Source:
            None

        Args:
            self         : stability analysis     [-]
            state (dict) : flight conditions      [-]

        Returs:
             results (dict): stability results    [-]
        """                     
        settings = self.settings
        geometry = self.geometry 
        results  = self.process.compute(state,settings,geometry)

        return results