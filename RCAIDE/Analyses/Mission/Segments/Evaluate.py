## @ingroup Analyses-Mission-Segments
# RCAIDE/Analyses/Mission/Segment/Evaluate.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Analyses.Mission.Segments         import Segment
from RCAIDE.Analyses.Mission.Common.Results   import Results
from RCAIDE.Methods.Mission                   import Common , Solver 
from RCAIDE.Analyses                          import Process  

# ----------------------------------------------------------------------------------------------------------------------
#  ANALYSES
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Analyses-Mission-Segments
class Evaluate(Segment):
    """  
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
        self.temperature_deviation   = 0.0
        # --------------------------------------------------------------
        #   State
        # --------------------------------------------------------------
        
        # conditions
        self.state.conditions.update(Results())
        
        # --------------------------------------------------------------
        #   The Solving Process
        # --------------------------------------------------------------
        
        # --------------------------------------------------------------
        #   Initialize - before iteration
        # -------------------------------------------------------------- 
        initialize                         = self.process.initialize 
        initialize.expand_state            = Solver.expand_state
        initialize.differentials           = Common.Initalize.differentials_dimensionless 
        initialize.conditions              = None
        #initialize.aerodynamics            = Common.Initalize.aerodynamics

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
        iterate.initials.time              = Common.Initalize.time
        iterate.initials.weights           = Common.Initalize.weights
        iterate.initials.energy            = Common.Initalize.energy
        iterate.initials.inertial_position = Common.Initalize.inertial_position
        iterate.initials.planet_position   = Common.Initalize.planet_position
        
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

