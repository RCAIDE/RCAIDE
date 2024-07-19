# digital_elevation_and_noise_hemispheres_test.py
#
# Created: Dec 2023 M. Clarke  
 
# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
# RCAIDE Imports 
import RCAIDE
from RCAIDE.Framework.Core import Units , Data 
from RCAIDE.Library.Plots import *     
from RCAIDE.Library.Methods.Noise.Metrics import *  
from RCAIDE.Library.Methods.Noise.Common.generate_microphone_locations        import generate_terrain_elevated_microphone_locations
from RCAIDE.Library.Mission.Common.compute_point_to_point_geospacial_data     import compute_point_to_point_geospacial_data

# Python imports
import matplotlib.pyplot as plt  
import sys 
import numpy as np     

# local imports 
sys.path.append('../../Vehicles')
from NASA_X57    import vehicle_setup, configs_setup     

# ----------------------------------------------------------------------
#   Main
# ---------------------------------------------------------------------- 
def main():    
    microphone_terrain_data =  generate_terrain_elevated_microphone_locations(topography_file   ='LA_Metropolitan_Area.txt',
                                                           ground_microphone_x_resolution    = 201,  
                                                           ground_microphone_y_resolution    = 101, 
                                                           ground_microphone_x_stencil       = 1,   
                                                           ground_microphone_y_stencil       = 1)    
    

    geospacial_data =  compute_point_to_point_geospacial_data(topography_file  = 'LA_Metropolitan_Area.txt',
                                                                                 departure_tag                         = 'A',
                                                                                 destination_tag                       = 'B',
                                                                                 departure_coordinates                 = [33.94067953101678, -118.40513722978149],
                                                                                 destination_coordinates               = [33.81713622114423, -117.92111163722772] )    
  
    
    plot_elevation_contours(topography_file   ='LA_Metropolitan_Area.txt',use_lat_long_coordinates = True, save_filename = "Elevation_Contours_Lat_Long")

    plot_elevation_contours(topography_file   ='LA_Metropolitan_Area.txt',use_lat_long_coordinates = False, save_filename = "Elevation_Contours_XY")  
      
    vehicle  = vehicle_setup()      
    vehicle.networks.all_electric.busses.bus.identical_propulsors     = False # only for regression     
    configs  = configs_setup(vehicle) 
    analyses = analyses_setup(configs,microphone_terrain_data,geospacial_data)  
    mission  = mission_setup(analyses,geospacial_data)
    missions = missions_setup(mission)  
    results  = missions.base_mission.evaluate()   
    
    regression_plotting_flag = False
    plot_results(results,regression_plotting_flag)   

    X57_SPL        = np.max(results.segments.climb.conditions.noise.total_SPL_dBA) 
    X57_SPL_true   = 55.032385258066725
    X57_diff_SPL   = np.abs(X57_SPL - X57_SPL_true)
    print('Error: ',X57_diff_SPL)
    assert np.abs((X57_SPL - X57_SPL_true)/X57_SPL_true) < 1e-3    
     
    return      

# ----------------------------------------------------------------------
#   Define the Vehicle Analyses
# ---------------------------------------------------------------------- 
def analyses_setup(configs,microphone_terrain_data,geospacial_data):

    analyses = RCAIDE.Framework.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis      = base_analysis(config,microphone_terrain_data,geospacial_data) 
        analyses[tag] = analysis

    return analyses  


def base_analysis(vehicle,microphone_terrain_data,geospacial_data):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Framework.Analyses.Vehicle() 
 
    # ------------------------------------------------------------------
    #  Weights
    weights         = RCAIDE.Framework.Analyses.Weights.Weights_eVTOL()
    weights.vehicle = vehicle
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics          = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method() 
    aerodynamics.geometry = vehicle
    aerodynamics.settings.drag_coefficient_increment = 0.0000
    analyses.append(aerodynamics)   
 
    #  Noise Analysis   
    noise = RCAIDE.Framework.Analyses.Noise.Frequency_Domain_Buildup()   
    noise.geometry = vehicle
    noise.settings.mean_sea_level_altitude          = False  
    noise.settings.aircraft_departure_location      = geospacial_data.departure_location   
    noise.settings.aircraft_destination_location    = geospacial_data.destination_location       
    noise.settings.aircraft_departure_coordinates   = geospacial_data.departure_coordinates
    noise.settings.aircraft_destination_coordinates = geospacial_data.destination_coordinates
    noise.settings.ground_microphone_x_resolution   = microphone_terrain_data.ground_microphone_x_resolution           
    noise.settings.ground_microphone_y_resolution   = microphone_terrain_data.ground_microphone_y_resolution          
    noise.settings.ground_microphone_x_stencil      = microphone_terrain_data.ground_microphone_x_stencil             
    noise.settings.ground_microphone_y_stencil      = microphone_terrain_data.ground_microphone_y_stencil             
    noise.settings.ground_microphone_min_y          = microphone_terrain_data.ground_microphone_min_x                 
    noise.settings.ground_microphone_max_y          = microphone_terrain_data.ground_microphone_max_x                 
    noise.settings.ground_microphone_min_x          = microphone_terrain_data.ground_microphone_min_y                 
    noise.settings.ground_microphone_max_x          = microphone_terrain_data.ground_microphone_max_y            
    noise.settings.topography_file                  = microphone_terrain_data.topography_file  
    noise.settings.ground_microphone_locations      = microphone_terrain_data.ground_microphone_locations 
    noise.settings.ground_microphone_min_lat        = microphone_terrain_data.ground_microphone_min_lat 
    noise.settings.ground_microphone_max_lat        = microphone_terrain_data.ground_microphone_max_lat 
    noise.settings.ground_microphone_min_long       = microphone_terrain_data.ground_microphone_min_long
    noise.settings.ground_microphone_min_long       = microphone_terrain_data.ground_microphone_min_long        
    noise.settings.ground_microphone_coordinates    = microphone_terrain_data.ground_microphone_coordinates   
    analyses.append(noise)

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
#  Set Up Mission 
# ---------------------------------------------------------------------- 
def mission_setup(analyses,geospacial_data):      
    
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------
    mission       = RCAIDE.Framework.Mission.Sequential_Segments()
    mission.tag   = 'mission' 
    Segments      = RCAIDE.Framework.Mission.Segments  
    base_segment  = Segments.Segment()   
    base_segment.state.numerics.number_control_points  = 5 
    
    # ------------------------------------------------------------------
    #   Departure End of Runway Segment Flight 1 : 
    # ------------------------------------------------------------------ 

    segment = Segments.Climb.Linear_Speed_Constant_Rate(base_segment) 
    segment.tag = "climb"   
    segment.analyses.extend( analyses.base ) 
    segment.initial_battery_state_of_charge              = 0.89         
    segment.altitude_start                               = 10.0    * Units.feet  
    segment.altitude_end                                 = 500.0   * Units.feet 
    segment.air_speed_start                              = 100.    * Units['mph'] 
    segment.air_speed_end                                = 120.    * Units['mph'] 
    segment.climb_rate                                   = 50.     * Units['ft/min']         
    segment.true_course_angle                            = geospacial_data.true_course_angle
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.flight_controls.body_angle.active             = True                
       
    mission.append_segment(segment)  
     
    return mission

# ----------------------------------------------------------------------
#  Set Up Missions 
# ---------------------------------------------------------------------- 
def missions_setup(mission): 
 
    missions     = RCAIDE.Framework.Mission.Missions() 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions  


# ----------------------------------------------------------------------
#  Plot Resuls 
# ---------------------------------------------------------------------- 
def plot_results(results,regression_plotting_flag): 
    
    noise_data   = post_process_noise_data(results)  
    
    # Plot noise hemisphere
    plot_noise_hemisphere(noise_data,
                          noise_level      = noise_data.SPL_dBA[1], 
                          min_noise_level  = 35,  
                          max_noise_level  = 90, 
                          noise_scale_label= 'SPL [dBA]',
                          show_figure      = regression_plotting_flag)     
    

    # Plot noise hemisphere with vehicle 
    plot_noise_hemisphere(noise_data,
                          noise_level      = noise_data.SPL_dBA[1], 
                          min_noise_level  = 35,  
                          max_noise_level  = 90, 
                          noise_scale_label= 'SPL [dBA]',
                          save_filename    = "Noise_Hemisphere_With_Aircraft", 
                          vehicle          = results.segments.climb.analyses.aerodynamics.geometry,
                          show_figure      = regression_plotting_flag)      
    
    
    # Plot noise level
    flight_times = np.array(['06:00:00','07:00:00','08:00:00','09:00:00','10:00:00','11:00:00','12:00:00','13:00:00','14:00:00','15:00:00'])  
      
    noise_data      = post_process_noise_data(results)   
    noise_data      = DNL_noise_metric(noise_data, flight_times,time_period = 24*Units.hours)
    noise_data      = Equivalent_noise_metric(noise_data, flight_times,time_period = 15*Units.hours)
    noise_data      = SENEL_noise_metric(noise_data, flight_times,time_period = 24*Units.hours)
    
    plot_noise_level(noise_data,
                    noise_level  = noise_data.SPL_dBA[0], 
                    save_filename="Sideline_Noise_Levels")  
    
    # Maximum Sound Pressure Level   
    plot_3D_noise_contour(noise_data,
                          noise_level      = np.max(noise_data.SPL_dBA,axis=0), 
                          min_noise_level  = 35,  
                          max_noise_level  = 90, 
                          noise_scale_label= 'SPL [dBA]',
                          save_filename    = "SPL_max_Noise_3D_Contour",
                          show_figure      = regression_plotting_flag)   
                        

    # Day Night Average Noise Level 
    plot_3D_noise_contour(noise_data,
                        noise_level      = noise_data.DNL,
                        min_noise_level  = 35,  
                        max_noise_level  = 90, 
                        noise_scale_label= 'DNL',
                        show_microphones = True, 
                        save_filename    = "DNL_Noise_3D_Contour",
                        show_figure      = regression_plotting_flag) 
    

    # Equivalent Noise Level
    plot_3D_noise_contour(noise_data,
                        noise_level      = noise_data.L_AeqT,
                        min_noise_level  = 35,  
                        max_noise_level  = 90, 
                        noise_scale_label= 'LAeqT',
                        show_trajectory  = True,
                        save_filename    = "LAeqT_Noise_3D_Contour",
                        show_figure      = regression_plotting_flag)    
    

    # 24-hr Equivalent Noise Level
    plot_3D_noise_contour(noise_data,
                       noise_level      = noise_data.L_AeqT,
                       min_noise_level  = 35,  
                       max_noise_level  = 90, 
                       noise_scale_label= '24hr-LAeqT',
                       save_filename    = "24hr_LAeqT_Noise_3D_Contour", 
                       use_lat_long_coordinates = False,                         
                       show_figure      = regression_plotting_flag)      
    

    # Single Event Noise Exposure Level
    plot_3D_noise_contour(noise_data,
                       noise_level      = noise_data.SENEL,
                       min_noise_level  = 35,  
                       max_noise_level  = 90, 
                       noise_scale_label= 'SENEL',
                       save_filename    = "SENEL_Noise_3D_Contour",
                       show_figure      = regression_plotting_flag)  


    noise_data      = post_process_noise_data(results)  
    noise_data      = Equivalent_noise_metric(noise_data, flight_times,time_period = 15*Units.hours)
    noise_data      = SENEL_noise_metric(noise_data, flight_times,time_period = 24*Units.hours)
    noise_data      = DNL_noise_metric(noise_data, flight_times,time_period = 24*Units.hours)
    
    # Maximum Sound Pressure Level   
    plot_2D_noise_contour(noise_data,
                        noise_level      = np.max(noise_data.SPL_dBA,axis=0), 
                        min_noise_level  = 35,  
                        max_noise_level  = 90, 
                        noise_scale_label= 'SPL [dBA]',
                        save_filename    = "SPL_max_Noise_2D_Contour",
                        show_elevation   = True,
                        use_lat_long_coordinates= False,
                        show_figure      = regression_plotting_flag)   
                        

    # Day Night Average Noise Level 
    plot_2D_noise_contour(noise_data,
                        noise_level      = noise_data.DNL,
                        min_noise_level  = 35,  
                        max_noise_level  = 90, 
                        noise_scale_label= 'DNL',
                        save_filename    = "DNL_Noise_2D_Contour",
                        show_figure      = regression_plotting_flag) 
    

    # Equivalent Noise Level
    plot_2D_noise_contour(noise_data,
                        noise_level      = noise_data.L_AeqT,
                        min_noise_level  = 35,  
                        max_noise_level  = 90, 
                        noise_scale_label= 'LAeqT',
                        save_filename    = "LAeqT_Noise_2D_Contour",
                        show_figure      = regression_plotting_flag)    
    

    # 24-hr Equivalent Noise Level
    plot_2D_noise_contour(noise_data,
                       noise_level      = noise_data.L_AeqT,
                       min_noise_level  = 35,  
                       max_noise_level  = 90, 
                       noise_scale_label= '24hr-LAeqT',
                       save_filename    = "24hr_LAeqT_Noise_2D_Contour",
                       show_figure      = regression_plotting_flag)      
    

    # Single Event Noise Exposure Level
    plot_2D_noise_contour(noise_data,
                       noise_level      = noise_data.SENEL,
                       min_noise_level  = 35,  
                       max_noise_level  = 90, 
                       noise_scale_label= 'SENEL',
                       save_filename    = "SENEL_Noise_2D_Contour",
                       show_figure      = regression_plotting_flag)      
    return  

if __name__ == '__main__': 
    main()    
    plt.show()
