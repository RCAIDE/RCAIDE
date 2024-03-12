## @ingroup Analyses-Aerodynamics
# RCAIDE/Analyses/Aerodynamics/Supersonic_VLM.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
import RCAIDE
from RCAIDE.Core                                          import Data
from RCAIDE.Frameworks.Analyses                                      import Process 
from RCAIDE.Methods.Aerodynamics                          import Common
from .Aerodynamics                                        import Aerodynamics 
from RCAIDE.Frameworks.Analyses.Aerodynamics.Common.Process_Geometry import Process_Geometry
from RCAIDE.Frameworks.Analyses.Aerodynamics.Common.Vortex_Lattice   import Vortex_Lattice

# package imports 
import numpy as np  

# ----------------------------------------------------------------------
#  Class
# ----------------------------------------------------------------------
## @ingroup Analyses-Aerodynamics
class Supersonic_VLM(Aerodynamics):
    """This is a supersonic aerodynamic buildup analysis based on the vortex lattice method

    Assumptions:
    None

    Source:
    Primarily based on adg.stanford.edu, see methods for details
    """ 
    def __defaults__(self):
        """This sets the default values and methods for the analysis.

        Assumptions:
        None

        Source:
        Concorde data used for determining defaults can be found in "Supersonic drag reduction technology in the 
        scaled supersonic experimental airplane project by JAXA" by Kenji Yoshida
        https://www.sciencedirect.com/science/article/pii/S0376042109000177

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """         
        self.tag = 'Supersonic_Zero'
        self.geometry                               = Data()  
        self.process                                = Process()
        self.process.initialize                     = Process()   
        
        # correction factors
        settings                                         = self.settings
        settings.fuselage_lift_correction                = 1.14
        settings.trim_drag_correction_factor             = 1.02
        settings.wing_parasite_drag_form_factor          = 1.1
        settings.fuselage_parasite_drag_form_factor      = 2.3
        settings.viscous_lift_dependent_drag_factor      = 0.38
        settings.lift_to_drag_adjustment                 = 0.0000
        settings.drag_coefficient_increment              = 0.0000
        settings.spoiler_drag_increment                  = 0.00 
        settings.oswald_efficiency_factor                = None
        settings.span_efficiency                         = None
        settings.maximum_lift_coefficient                = np.inf 
        settings.begin_drag_rise_mach_number             = 0.95
        settings.end_drag_rise_mach_number               = 1.2
        settings.transonic_drag_multiplier               = 1.25 
        settings.number_spanwise_vortices                = None 
        settings.number_chordwise_vortices               = None 
        settings.use_surrogate                           = True 
        settings.propeller_wake_model                    = False
        settings.model_fuselage                          = False
        settings.recalculate_total_wetted_area           = False
        settings.model_nacelle                           = False
        settings.discretize_control_surfaces             = False 
        settings.peak_mach_number                        = 1.04
        settings.cross_sectional_area_calculation_type   = 'Fixed'     
        settings.wave_drag_type                          = 'Raymer'
        settings.volume_wave_drag_scaling                = 3.2  
        settings.fuselage_parasite_drag_begin_blend_mach = 0.91
        settings.fuselage_parasite_drag_end_blend_mach   = 0.99 
        settings.number_spanwise_vortices                = 15
        settings.number_chordwise_vortices               = 5
        
        
        # build the evaluation process
        compute                                    = Process() 
        compute.lift                               = Process() 
        compute.lift.inviscid_wings                = Vortex_Lattice() 
        compute.lift.fuselage                      = Common.Lift.fuselage_correction
        compute.lift.total                         = Common.Lift.aircraft_total 
        compute.drag                               = Process()
        compute.drag.compressibility               = Process()
        compute.drag.compressibility.total         = Common.Drag.compressibility_drag_total   
        compute.drag.parasite                      = Process()
        compute.drag.parasite.wings                = Process_Geometry('wings')
        compute.drag.parasite.wings.wing           = Common.Drag.parasite_drag_wing 
        compute.drag.parasite.fuselages            = Process_Geometry('fuselages')
        compute.drag.parasite.fuselages.fuselage   = Common.Drag.parasite_drag_fuselage 
        compute.drag.parasite.booms                = Process_Geometry('booms')
        compute.drag.parasite.booms.boom           = Common.Drag.parasite_drag_fuselage
        compute.drag.parasite.nacelles             = Process_Geometry('nacelles')
        compute.drag.parasite.nacelles.nacelle     = Common.Drag.parasite_drag_nacelle  
        compute.drag.parasite.total                = Common.Drag.parasite_total
        compute.drag.induced                       = Common.Drag.induced_drag_aircraft
        compute.drag.miscellaneous                 = Common.Drag.miscellaneous_drag_aircraft 
        compute.drag.untrimmed                     = Common.Drag.untrimmed
        compute.drag.trim                          = Common.Drag.trim
        compute.drag.spoiler                       = Common.Drag.spoiler_drag
        compute.drag.total                         = Common.Drag.total_aircraft 
        self.process.compute                       = compute 
        
         
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