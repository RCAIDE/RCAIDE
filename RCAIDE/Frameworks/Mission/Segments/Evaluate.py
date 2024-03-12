## @ingroup Frameworks-Mission-Segments
# RCAIDE/Frameworks/Mission/Segment/Evaluate.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Frameworks.Mission.Segments         import Segment
from RCAIDE.Frameworks.Mission.Common.Results   import Results
from RCAIDE.Methods.Mission                   import Common , Solver 
from RCAIDE.Frameworks.Analyses                          import Process  

# ----------------------------------------------------------------------------------------------------------------------
#  ANALYSES
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Frameworks-Mission-Segments
class Evaluate(Segment):
    """ Base process class used to analyze a vehicle in each flight segment  
    
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
        
        # --------------------------------------------------------------
        #   State
        # --------------------------------------------------------------
        
        # conditions
        self.temperature_deviation                                = 0.0     
        self.state.conditions.update(Results())
        
        # ---------------------------------------------------------------
        # Define Flight Controls and Residuals 
        # ---------------------------------------------------------------     
        self.flight_dynamics_and_controls()    
        
        # --------------------------------------------------------------
        #   Initialize - before iteration
        # -------------------------------------------------------------- 
        initialize                         = self.process.initialize 
        initialize.expand_state            = Solver.expand_state
        initialize.differentials           = Common.Initialize.differentials_dimensionless 
        initialize.conditions              = None 

        # --------------------------------------------------------------         
        #   Converge 
        # -------------------------------------------------------------- 
        converge = self.process.converge 
        converge.converge_root             = Solver.converge_root        

        # --------------------------------------------------------------          
        #   Iterate  
        # -------------------------------------------------------------- 
        iterate                            = self.process.iterate 
        iterate.initials                   = Process()
        iterate.initials.time              = Common.Initialize.time
        iterate.initials.weights           = Common.Initialize.weights
        iterate.initials.energy            = Common.Initialize.energy
        iterate.initials.inertial_position = Common.Initialize.inertial_position
        iterate.initials.planet_position   = Common.Initialize.planet_position
        
        # Unpack Unknowns
        iterate.unknowns                   = Process()
        
        # Update Conditions
        iterate.conditions = Process()
        iterate.conditions.differentials   = Common.Update.differentials_time     
        iterate.conditions.acceleration    = Common.Update.acceleration   
        iterate.conditions.altitude        = Common.Update.altitude
        iterate.conditions.atmosphere      = Common.Update.atmosphere
        iterate.conditions.gravity         = Common.Update.gravity
        iterate.conditions.freestream      = Common.Update.freestream
        iterate.conditions.orientations    = Common.Update.orientations
        iterate.conditions.energy          = Common.Update.thrust
        iterate.conditions.aerodynamics    = Common.Update.aerodynamics
        iterate.conditions.stability       = Common.Update.stability
        iterate.conditions.weights         = Common.Update.weights
        iterate.conditions.forces          = Common.Update.forces
        iterate.conditions.planet_position = Common.Update.planet_position

        # Solve Residuals
        iterate.residuals = Process()

        # --------------------------------------------------------------  
        #  Post Process   
        # -------------------------------------------------------------- 
        post_process                    = self.process.post_process   
        post_process.inertial_position  = Common.Update.inertial_horizontal_position
        post_process.battery_age        = Common.Update.battery_age  
        post_process.noise              = Common.Update.noise
        
        return

