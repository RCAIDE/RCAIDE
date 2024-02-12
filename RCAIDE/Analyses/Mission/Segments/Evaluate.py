## @ingroup Analyses-Mission-Segments
# RCAIDE/Analyses/Mission/Segment/Evaluate.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Core                              import Data 
from RCAIDE.Analyses.Mission.Segments         import Segment
from RCAIDE.Analyses.Mission.Common.Results   import Results
from RCAIDE.Methods.Mission                   import Common , Solver 
from RCAIDE.Analyses                          import Process  

# ----------------------------------------------------------------------------------------------------------------------
#  ANALYSES
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Analyses-Mission-Segments
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
        # Degrees of Freedom 
        # -------------------------------------------------------------- 
        self.degrees_of_freedom                                   = 2
        
        # --------------------------------------------------------------
        # Flight Controls 
        # --------------------------------------------------------------    
        self.body_angle_control                                   = Data()
        self.body_angle_control.active                            = False                 
        self.body_angle_control.initial_values                    = None  
        
        self.wind_angle_control                                   = Data()
        self.wind_angle_control.active                            = False                 
        self.wind_angle_control.initial_values                    = None   
        
        self.velocity_control                                     = Data()
        self.velocity_control.active                              = False                 
        self.velocity_control.initial_values                      = None   

        self.flight_path_angle_control                            = Data()
        self.flight_path_angle_control.active                     = False                 
        self.flight_path_angle_control.initial_values             = None   
        
        self.altitude_control                                     = Data()
        self.altitude_control.active                              = False                 
        self.altitude_control.initial_values                      = None         
             
        self.throttle_control                                     = Data() 
        self.throttle_control.active                              = False              
        self.throttle_control.assigned_propulsors                 = None       
        self.throttle_control.initial_values                      = None  
             
        self.elevator_deflection_control                          = Data() 
        self.elevator_deflection_control.active                   = False      
        self.elevator_deflection_control.assigned_control_surface = None
        self.elevator_deflection_control.initial_values           = None  
        
        self.flap_deflection_control                              = Data() 
        self.flap_deflection_control.active                       = False          
        self.flap_deflection_control.assigned_control_surface     = None
        self.flap_deflection_control.initial_values               = None  
             
        self.aileron_deflection_control                           = Data() 
        self.aileron_deflection_control.active                    = False      
        self.aileron_deflection_control.assigned_control_surface  = None
        self.aileron_deflection_control.initial_values            = None  
             
        self.thrust_vector_angle_control                          = Data() 
        self.thrust_vector_angle_control.active                   = False        
        self.thrust_vector_angle_control.assigned_propulsors      = None
        self.thrust_vector_angle_control.initial_values           = None  
             
        self.blade_pitch_angle_control                            = Data() 
        self.blade_pitch_angle_control.active                     = False          
        self.blade_pitch_angle_control.assigned_propulsors        = None
        self.blade_pitch_angle_control.initial_values             = None  
        
        self.RPM_control                                          = Data() 
        self.RPM_control.active                                   = False              
        self.RPM_control.assigned_propulsors                      = None
        self.RPM_control.initial_values                           = None  
        
        # --------------------------------------------------------------
        #   State
        # --------------------------------------------------------------
        
        # conditions
        self.temperature_deviation                                = 0.0     
        self.state.conditions.update(Results())
        
        # --------------------------------------------------------------
        #   The Solving Process
        # --------------------------------------------------------------
        
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

