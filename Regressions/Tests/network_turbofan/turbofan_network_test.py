# Regression/scripts/Tests/turbofan_network_test.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
import RCAIDE
from RCAIDE.Core import Units  
from RCAIDE.Plots            import *       

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
    
    # plot vehicle 
    plot_3d_vehicle(configs.base,
                    show_wing_control_points    = False,
                    show_rotor_wake_vortex_core = False,
                    min_x_axis_limit            = 0,
                    max_x_axis_limit            = 40,
                    min_y_axis_limit            = -20,
                    max_y_axis_limit            = 20,
                    min_z_axis_limit            = -20,
                    max_z_axis_limit            = 20,
                    show_figure                 = False)         
        
    return 

  
def analyses_setup(configs):

    analyses = RCAIDE.Frameworks.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config)
        analyses[tag] = analysis

    return analyses

def base_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Frameworks.Analyses.Vehicle() 
    
    # ------------------------------------------------------------------
    #  Weights
    weights         = RCAIDE.Frameworks.Analyses.Weights.Weights_Transport()
    weights.vehicle = vehicle
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics          = RCAIDE.Frameworks.Analyses.Aerodynamics.Subsonic_VLM() 
    aerodynamics.geometry = vehicle
    aerodynamics.settings.number_spanwise_vortices   = 25
    aerodynamics.settings.number_chordwise_vortices  = 5     
    analyses.append(aerodynamics)   

    # ------------------------------------------------------------------
    #  Energy
    energy          = RCAIDE.Frameworks.Analyses.Energy.Energy()
    energy.networks = vehicle.networks 
    analyses.append(energy)

    # ------------------------------------------------------------------
    #  Planet Analysis
    planet = RCAIDE.Frameworks.Analyses.Planets.Planet()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere = RCAIDE.Frameworks.Analyses.Atmospheric.US_Standard_1976()
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

    mission = RCAIDE.Frameworks.Mission.Sequential_Segments()
    mission.tag = 'the_mission'
  
    Segments = RCAIDE.Frameworks.Mission.Segments 
    base_segment = Segments.Segment()


    # ------------------------------------------------------------------
    #   First Climb Segment: Constant Speed Constant Rate  
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_1" 
    segment.analyses.extend( analyses.takeoff ) 
    segment.altitude_start = 0.0   * Units.km
    segment.altitude_end   = 3.0   * Units.km
    segment.air_speed      = 125.0 * Units['m/s']
    segment.climb_rate     = 6.0   * Units['m/s']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                         = True  
    segment.flight_dynamics.force_z                         = True     
      
    # define flight controls   
    segment.flight_controls.throttle.active                 = True           
    segment.flight_controls.throttle.assigned_propulsors    = [['starboard_propulsor','port_propulsor']]
    segment.flight_controls.throttle.initial_guess          = True 
    segment.flight_controls.throttle.initial_guess_values   = [[0.5,0.5]] 
    segment.flight_controls.body_angle.active               = True               
    segment.flight_controls.body_angle.initial_guess        = True 
    segment.flight_controls.body_angle.initial_guess_values = [[3*Units.degrees]]    
      
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Second Climb Segment: Constant Speed Constant Rate  
    # ------------------------------------------------------------------    

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_2" 
    segment.analyses.extend( analyses.cruise ) 
    segment.altitude_end                                   = 8.0   * Units.km
    segment.air_speed                                      = 190.0 * Units['m/s']
    segment.climb_rate                                     = 6.0   * Units['m/s']   
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]  
    segment.flight_controls.body_angle.active             = True                   
     
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Third Climb Segment: Constant Speed Constant Rate  
    # ------------------------------------------------------------------    

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_3" 
    segment.analyses.extend( analyses.cruise ) 
    segment.altitude_end = 10.5   * Units.km
    segment.air_speed    = 226.0  * Units['m/s']
    segment.climb_rate   = 3.0    * Units['m/s']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]  
    segment.flight_controls.body_angle.active             = True                
      
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
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.flight_controls.body_angle.active             = True                
    
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   First Descent Segment: Constant Speed Constant Rate  
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_1" 
    segment.analyses.extend( analyses.cruise ) 
    segment.altitude_start = 10.5 * Units.km 
    segment.altitude_end   = 8.0   * Units.km
    segment.air_speed      = 220.0 * Units['m/s']
    segment.descent_rate   = 4.5   * Units['m/s']   
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]  
    segment.flight_controls.body_angle.active             = True                
     
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Second Descent Segment: Constant Speed Constant Rate  
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_2" 
    segment.analyses.extend( analyses.landing ) 
    segment.altitude_end = 6.0   * Units.km
    segment.air_speed    = 195.0 * Units['m/s']
    segment.descent_rate = 5.0   * Units['m/s']   
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.flight_controls.body_angle.active             = True                 
     
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Third Descent Segment: Constant Speed Constant Rate  
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_3"  
    segment.analyses.extend( analyses.landing ) 
    segment.altitude_end = 4.0   * Units.km
    segment.air_speed    = 170.0 * Units['m/s']
    segment.descent_rate = 5.0   * Units['m/s']   
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.flight_controls.body_angle.active             = True                
     
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Fourth Descent Segment: Constant Speed Constant Rate  
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_4" 
    segment.analyses.extend( analyses.landing ) 
    segment.altitude_end = 2.0   * Units.km
    segment.air_speed    = 150.0 * Units['m/s']
    segment.descent_rate = 5.0   * Units['m/s']   
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.flight_controls.body_angle.active             = True                  
     
    mission.append_segment(segment) 


    # ------------------------------------------------------------------
    #   Fifth Descent Segment:Constant Speed Constant Rate  
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_5" 
    segment.analyses.extend( analyses.landing ) 
    segment.altitude_end                                  = 0.0   * Units.km
    segment.air_speed                                     = 145.0 * Units['m/s']
    segment.descent_rate                                  = 3.0   * Units['m/s']    
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.flight_controls.body_angle.active             = True                
    
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Mission definition complete    
    # ------------------------------------------------------------------

    return mission

 

def missions_setup(mission): 
 
    missions     = RCAIDE.Frameworks.Mission.Missions() 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions  


def plot_results(results):  
     
    # Plot Aerodynamic Forces 
    plot_aerodynamic_forces(results)
    
    # Plot Aerodynamic Coefficients 
    plot_aerodynamic_coefficients(results)
    
    # Plot Static Stability Coefficients 
    plot_stability_coefficients(results)    
    
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