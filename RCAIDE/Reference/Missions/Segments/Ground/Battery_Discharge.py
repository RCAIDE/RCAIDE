# RCAIDE/Framework/Functions/Segments/Ground/Battery_Disharge.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Reference.Missions.Segments.Evaluate import Evaluate
from RCAIDE.Reference.Core import Units
from RCAIDE.Library.Methods.skip                      import skip

# ----------------------------------------------------------------------------------------------------------------------
#  SEGMENT
# ---------------------------------------------------------------------------------------------------------------------- 
class Battery_Discharge(Evaluate):  
    """Discharging segment for battery"""  

    def __defaults__(self):  
        """ Specific flight segment defaults which can be modified after initializing.
        
            Assumptions:
                None
    
            Source:
                None
        """            
        
        # --------------------------------------------------------------
        #   User Inputs
        # --------------------------------------------------------------
        self.altitude               = None
        self.time                   = 1.0 * Units.seconds
        self.current                = 0
        self.overcharge_contingency = 1.10 
        self.true_course            = 0.0 * Units.degrees 

        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions specific processes
        # --------------------------------------------------------------------------------------------------------------       
        initialize                         = self.process.initialize 
        initialize.conditions              = RCAIDE.Framework.Mission.Mission.Segments.Ground.Battery_Charge_Discharge.initialize_conditions
        iterate                            = self.process.iterate 
        iterate.unknowns.mission           = skip
        iterate.conditions.aerodynamics    = skip
        iterate.conditions.stability       = skip  
        post_process                       = self.process.post_process  
        post_process.noise                 = skip
        
        return
