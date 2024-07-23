# Regression/scripts/Tests/turbofan_network_test.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core import Units  
from RCAIDE.Library.Plots                 import *       

# python imports     
import numpy as np  
import sys
import matplotlib.pyplot as plt  

# local imports 
sys.path.append('../../Vehicles')
from Embraer_190    import vehicle_setup as vehicle_setup
from Embraer_190    import configs_setup as configs_setup 


# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------  
def main():      
    # vehicle data
    vehicle  = vehicle_setup()

    # plot vehicle 
    plot_3d_vehicle(vehicle, 
                    min_x_axis_limit            = 0,
                    max_x_axis_limit            = 40,
                    min_y_axis_limit            = -20,
                    max_y_axis_limit            = 20,
                    min_z_axis_limit            = -20,
                    max_z_axis_limit            = 20,
                    show_figure                 = False 
                    )        
    
    # Set up vehicle configs
    configs  = configs_setup(vehicle)

    # create analyses
    analyses = analyses_setup(configs)

    # mission analyses 
    mission = mission_setup(analyses)
    
    # create mission instances (for multiple types of missions)
    missions = missions_setup(mission) 
     
    # mission analysis 
    results = missions.base_mission.evaluate()  
    
    # plot the results
    plot_results(results)  
        
    return 

  
def analyses_setup(configs):

    analyses = RCAIDE.Framework.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config)
        analyses[tag] = analysis

    return analyses

def base_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Framework.Analyses.Vehicle_Analyses()
    
    # ------------------------------------------------------------------
    #  Weights
    weights         = RCAIDE.Framework.Analyses.Weights.Weights_Transport()
    weights.vehicle = vehicle
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics          = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method() 
    aerodynamics.geometry = vehicle
    aerodynamics.settings.number_of_spanwise_vortices   = 25
    aerodynamics.settings.number_of_chordwise_vortices  = 5     
    analyses.append(aerodynamics)   

    # ------------------------------------------------------------------
    #  Energy
    energy          = RCAIDE.Framework.Analyses.Energy.Energy()
    energy.networks = vehicle.networks 
    analyses.append(energy)

    # ------------------------------------------------------------------
    #  Planet Analysis
    planet = RCAIDE.Framework.Analyses.Planets.Planet()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   

    # done!
    return analyses    

# ----------------------------------------------------------------------
#   Define the Mission
# ----------------------------------------------------------------------
 
def mission_setup(analyses):

    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------

    mission = RCAIDE.Framework.Mission.Sequential_Segments()
    mission.tag = 'the_mission'
  
    Segments = RCAIDE.Framework.Mission.Segments 
    base_segment = Segments.Segment()


    # ------------------------------------------------------------------
    #   First Climb Segment: Constant Speed Constant Rate  
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_1" 
    segment.analyses.extend( analyses.takeoff ) 
    segment.altitude_start = 0.0   * Units.km
    segment.altitude_end   = 500   * Units.feet
    segment.air_speed      = 125.0 * Units['m/s']
    segment.climb_rate     = 6.0   * Units['m/s']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                         = True  
    segment.flight_dynamics.force_z                         = True     
      
    # define flight controls   
    segment.assigned_control_variables.throttle.active                 = True           
    segment.assigned_control_variables.throttle.assigned_propulsors    = [['starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.throttle.initial_guess   = [[0.5,0.5]] 
    segment.assigned_control_variables.body_angle.active               = True 
    segment.assigned_control_variables.body_angle.initial_guess = [[3*Units.degrees]]    
      
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   First Climb Segment: Constant Speed Constant Rate  
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_2" 
    segment.analyses.extend( analyses.cutback )  
    segment.altitude_end   = 3.0   * Units.km
    segment.air_speed      = 125.0 * Units['m/s']
    segment.climb_rate     = 6.0   * Units['m/s']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                         = True  
    segment.flight_dynamics.force_z                         = True     
      
    # define flight controls   
    segment.assigned_control_variables.throttle.active                 = True           
    segment.assigned_control_variables.throttle.assigned_propulsors    = [['starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.throttle.initial_guess          = [[0.5,0.5]] 
    segment.assigned_control_variables.body_angle.active               = True 
    segment.assigned_control_variables.body_angle.initial_guess        = [[3*Units.degrees]]    
      
    mission.append_segment(segment)
    
    
    # ------------------------------------------------------------------
    #   Second Climb Segment: Constant Speed Constant Rate  
    # ------------------------------------------------------------------    

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_3" 
    segment.analyses.extend( analyses.cruise ) 
    segment.altitude_end                                   = 8.0   * Units.km
    segment.air_speed                                      = 190.0 * Units['m/s']
    segment.climb_rate                                     = 6.0   * Units['m/s']   
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]  
    segment.assigned_control_variables.body_angle.active             = True                   
     
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Third Climb Segment: Constant Speed Constant Rate  
    # ------------------------------------------------------------------    

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_4" 
    segment.analyses.extend( analyses.cruise ) 
    segment.altitude_end = 10.5   * Units.km
    segment.air_speed    = 226.0  * Units['m/s']
    segment.climb_rate   = 3.0    * Units['m/s']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]  
    segment.assigned_control_variables.body_angle.active             = True                
      
    mission.append_segment(segment)


    # ------------------------------------------------------------------    
    #   Cruise Segment: Constant Speed Constant Altitude
    # ------------------------------------------------------------------    

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise" 
    segment.analyses.extend( analyses.cruise ) 
    segment.altitude  = 10.668 * Units.km  
    segment.air_speed = 230.412 * Units['m/s']
    segment.distance  = 1000 * Units.nmi    
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.body_angle.active             = True                
    
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   First Descent Segment: Constant Speed Constant Rate  
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_1" 
    segment.analyses.extend( analyses.cruise ) 
    segment.altitude_start                                = 10.5 * Units.km 
    segment.altitude_end                                  = 8.0   * Units.km
    segment.air_speed                                     = 220.0 * Units['m/s']
    segment.descent_rate                                  = 4.5   * Units['m/s']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.body_angle.active             = True                
    
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Second Descent Segment: Constant Speed Constant Rate  
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag  = "descent_2" 
    segment.analyses.extend( analyses.cruise ) 
    segment.altitude_end                                  = 6.0   * Units.km
    segment.air_speed                                     = 195.0 * Units['m/s']
    segment.descent_rate                                  = 5.0   * Units['m/s']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.body_angle.active             = True                
    
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Third Descent Segment: Constant Speed Constant Rate  
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_3"  
    segment.analyses.extend( analyses.cruise ) 
    segment.altitude_end                                  = 4.0   * Units.km
    segment.air_speed                                     = 170.0 * Units['m/s']
    segment.descent_rate                                  = 5.0   * Units['m/s']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.body_angle.active             = True                
    
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Fourth Descent Segment: Constant Speed Constant Rate  
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_4" 
    segment.analyses.extend( analyses.cruise ) 
    segment.altitude_end                                  = 2.0   * Units.km
    segment.air_speed                                     = 150.0 * Units['m/s']
    segment.descent_rate                                  = 5.0   * Units['m/s']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.body_angle.active             = True                
    
    mission.append_segment(segment)



    # ------------------------------------------------------------------
    #   Fifth Descent Segment:Constant Speed Constant Rate  
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_5" 
    segment.analyses.extend( analyses.approach ) 
    segment.altitude_end                                  = 0.0   * Units.km
    segment.air_speed                                     = 145.0 * Units['m/s']
    segment.descent_rate                                  = 3.0   * Units['m/s']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.body_angle.active             = True                
    
    mission.append_segment(segment)
    
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    #   Landing Roll
    # ------------------------------------------------------------------------------------------------------------------------------------ 

    segment = Segments.Ground.Landing(base_segment)
    segment.tag = "Landing"

    segment.analyses.extend( analyses.reverse_thrust ) 
    segment.velocity_start                                = 145.0 * Units['m/s']
    segment.velocity_end                                  = 10 * Units.knots 
    segment.friction_coefficient                          = 0.4
    segment.altitude                                      = 0.0 

    segment.flight_dynamics.force_x                         = True      
    
    segment.assigned_control_variables.elapsed_time.active           = True  
    segment.assigned_control_variables.elapsed_time.initial_guess    = [[30.]]  
    mission.append_segment(segment)     


    # ------------------------------------------------------------------
    #   Mission definition complete    
    # ------------------------------------------------------------------


    return mission

 

def missions_setup(mission): 
 
    missions     = RCAIDE.Framework.Mission.Missions() 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions  


def plot_results(results):  
     
    # Plot Aerodynamic Forces 
    plot_aerodynamic_forces(results)
    
    # Plot Aerodynamic Coefficients 
    plot_aerodynamic_coefficients(results) 
    
    # Drag Components
    plot_drag_components(results)
    
    # Plot Altitude, sfc, vehicle weight 
    plot_altitude_sfc_weight(results)
    
    # Plot Velocities 
    plot_aircraft_velocities(results)  
          
    return

if __name__ == '__main__': 
    main()    
    plt.show() 