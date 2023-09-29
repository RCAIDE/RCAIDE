## @ingroup Analyses-Mission-Segments-Single_Point
# RCAIDE/Analyses/Mission/Segments/Single_Point/Set_Speed_Set_Altitude_No_Propulsion.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Methods                                  import skip   
from RCAIDE.Core                                     import Units 
from RCAIDE.Analyses.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Methods.Mission                          import Common,Segments


# Package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Set_Speed_Set_Altitude_No_Propulsion
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Analyses-Mission-Segments-Single_Point
class Set_Speed_Set_Altitude_No_Propulsion(Evaluate):
    """ This is a segment that is solved using a single point. A snapshot in time.
        We fix the speed and altitude. Throttle is solved from those.
    
        Assumptions:
        None
        
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
        #   User Inputs
        # --------------------------------------------------------------------------------------------------------------
        self.altitude                                = None
        self.air_speed                               = 10. * Units['km/hr']
        self.distance                                = 1.  * Units.km
        self.z_accel                                 = 0. # note that down is positive
        self.state.numerics.number_of_control_points = 1
         
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission Specific Unknowns and Residuals 
        # --------------------------------------------------------------------------------------------------------------  
        self.state.unknowns.body_angle = np.array([[0.0]])
        self.state.residuals.forces    = np.array([[0.0]]) 

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------             
        initialize                         = self.process.initialize 
        initialize.expand_state            = skip
        initialize.differentials           = skip
        initialize.conditions              = Segments.Single_Point.Set_Speed_Set_Altitude_No_Propulsion.initialize_conditions 
        iterate                            = self.process.iterate 
        iterate.unknowns.mission           = Segments.Single_Point.Set_Speed_Set_Altitude_No_Propulsion.unpack_unknowns 
        iterate.conditions.differentials   = skip 
        iterate.conditions.weights         = Common.Update.weights
        iterate.conditions.planet_position = skip 
        iterate.residuals.total_forces     = Segments.Single_Point.Set_Speed_Set_Altitude_No_Propulsion.residual_total_force 
        
        return

