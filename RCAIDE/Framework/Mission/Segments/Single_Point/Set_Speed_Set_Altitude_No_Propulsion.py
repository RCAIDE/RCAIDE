## @ingroup Framework-Mission-Segments-Single_Point
# RCAIDE/Framework/Mission/Segments/Single_Point/Set_Speed_Set_Altitude_No_Propulsion.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Library.Methods                          import skip   
from RCAIDE.Framework.Core                           import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate      import Evaluate
from RCAIDE.Library.Mission                          import Common,Segments 

# ----------------------------------------------------------------------------------------------------------------------
#  Set_Speed_Set_Altitude_No_Propulsion
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Framework-Mission-Segments-Single_Point
class Set_Speed_Set_Altitude_No_Propulsion(Evaluate):
    """ This is a segment that is solved using a single point. A snapshot in time.
        We fix the speed and altitude. Throttle is solved from those. 
    """        
    
    def __defaults__(self):
        """ Specific flight segment defaults which can be modified after initializing.
        
            Assumptions:
                None
    
            Source:
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
        iterate.conditions.differentials   = skip 
        iterate.conditions.weights         = Common.Update.weights
        iterate.conditions.planet_position = skip 
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation
        
        return

