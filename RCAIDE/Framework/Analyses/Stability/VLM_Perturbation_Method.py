## @ingroup Framework-Analyses-Stability
# RCAIDE/Framework/Analyses/Stability/VLM_Perturbation_Method.py
# 
# 
# Created:  Mar 2023, M. Clarke
# Updated:  May 2024, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core                                          import Data
from RCAIDE.Framework.Analyses                                      import Process  
from RCAIDE.Library.Methods.Aerodynamics                            import Common
from .Stability                                                     import Stability 
from RCAIDE.Framework.Analyses.Stability.Common.Vortex_Lattice      import Vortex_Lattice
from RCAIDE.Framework.Analyses.Aerodynamics.Common.Process_Geometry import Process_Geometry   

# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  VLM_Perturbation_Method
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Framework-Analyses-Aerodynamics
class VLM_Perturbation_Method(Stability):  
    """ 
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
        settings.number_of_spanwise_vortices             = None 
        settings.number_of_chordwise_vortices            = None 
        settings.use_surrogate                           = True
        settings.recalculate_total_wetted_area           = False
        settings.propeller_wake_model                    = False 
        settings.discretize_control_surfaces             = False
        settings.model_fuselage                          = False                
        settings.model_nacelle                           = False 
        settings.begin_drag_rise_mach_number             = 0.95
        settings.end_drag_rise_mach_number               = 1.2
        settings.transonic_drag_multiplier               = 1.25   
        settings.peak_mach_number                        = 1.04
        settings.cross_sectional_area_calculation_type   = 'Fixed'     
        settings.wave_drag_type                          = 'Raymer'
        settings.volume_wave_drag_scaling                = 3.2  
        settings.fuselage_parasite_drag_begin_blend_mach = 0.91
        settings.fuselage_parasite_drag_end_blend_mach   = 0.99  

        # build the evaluation process
        compute                                          = Process() 
        compute.lift                                     = Process() 
        compute.lift.inviscid_wings                      = Vortex_Lattice() 
        compute.lift.vortex                              = RCAIDE.Library.Methods.skip
        compute.lift.fuselage                            = Common.Lift.fuselage_correction
        compute.lift.total                               = Common.Lift.aircraft_total  
        compute.drag                                     = Process()
        compute.drag.parasite                            = Process()
        compute.drag.parasite.wings                      = Process_Geometry('wings')
        compute.drag.parasite.wings.wing                 = Common.Drag.parasite_drag_wing 
        compute.drag.parasite.fuselages                  = Process_Geometry('fuselages')
        compute.drag.parasite.fuselages.fuselage         = Common.Drag.parasite_drag_fuselage
        compute.drag.parasite.booms                      = Process_Geometry('booms')
        compute.drag.parasite.booms.boom                 = Common.Drag.parasite_drag_fuselage
        compute.drag.parasite.nacelles                   = Process_Geometry('nacelles')
        compute.drag.parasite.nacelles.nacelle           = Common.Drag.parasite_drag_nacelle
        compute.drag.parasite.pylons                     = Common.Drag.parasite_drag_pylon
        compute.drag.parasite.total                      = Common.Drag.parasite_total
        compute.drag.induced                             = Common.Drag.induced_drag_aircraft
        compute.drag.compressibility                     = Process()
        compute.drag.compressibility.wings               = Process_Geometry('wings')
        compute.drag.compressibility.wings.wing          = Common.Drag.compressibility_drag_wing
        compute.drag.compressibility.total               = Common.Drag.compressibility_drag_wing_total
        compute.drag.miscellaneous                       = Common.Drag.miscellaneous_drag_aircraft_ESDU
        compute.drag.untrimmed                           = Common.Drag.untrimmed
        compute.drag.trim                                = Common.Drag.trim
        compute.drag.spoiler                             = Common.Drag.spoiler_drag
        compute.drag.total                               = Common.Drag.total_aircraft 
        self.process.compute                             = compute   

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