## @ingroup Frameworks-Mission-Segments-Single_Point
# RCAIDE/Frameworks/Mission/Segments/Single_Point/Set_Speed_Set_Altitude_No_Propulsion.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Library.Methods                                  import skip   
from RCAIDE.Frameworks.Core                                     import Units 
from RCAIDE.Frameworks.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Library.Methods.Mission                          import Common,Segments


# Package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Set_Speed_Set_Altitude_No_Propulsion
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Frameworks-Mission-Segments-Single_Point
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
        self.acceleration_z                          = 0. # note that down is positive
        self.state.numerics.number_of_control_points = 1

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------             
        initialize                         = self.process.initialize 
        initialize.expand_state            = skip
        initialize.differentials           = skip
        initialize.conditions              = Segments.Single_Point.Set_Speed_Set_Altitude_No_Propulsion.initialize_conditions 
        iterate                            = self.process.iterate  
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation    
        iterate.conditions.differentials   = skip 
        iterate.conditions.weights         = Common.Update.weights
        iterate.conditions.planet_position = skip 
        iterate.residuals.total_forces     = Common.Residuals.level_flight_forces
        
        return
