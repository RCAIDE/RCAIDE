# digital_elevation_and_noise_hemispheres_test.py
#
# Created: Apr 2021, M. Clarke  
 
# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
import RCAIDE
from RCAIDE.Framework.Core import Units , Data 
from RCAIDE.Library.Plots import *     
from RCAIDE.Library.Methods.Noise.Metrics import * 
from RCAIDE.Library.Methods.Performance.estimate_stall_speed                          import estimate_stall_speed  

# python import
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
    vehicle  = vehicle_setup()
    plot_3d_vehicle_vlm_panelization(vehicle, show_figure = False)
    configs  = configs_setup(vehicle) 
    analyses = analyses_setup(configs)  
    mission  = mission_setup(analyses,vehicle)
    missions = missions_setup(mission)  
    results  = missions.base_mission.evaluate() 
    regression_plotting_flag = False 
    noise_data = plot_results(results,regression_plotting_flag) 
 
 
    # dBA Verification checj
    dBA_true   = 69.36894727323475
    dBA        = noise_data.SPL_dBA[0,0,0]
    print('dBA: ' + str(dBA)) 
    diff_dBA                = np.abs(dBA  - dBA_true) 
    print('dBA difference: ' +  str(diff_dBA)) 
    assert np.abs((dBA  - dBA_true)/dBA_true) < 1e-6     
    
    return     
 

def base_analysis(vehicle):

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
    

    # ------------------------------------------------------------------
    #  Noise Analysis 
    # ------------------------------------------------------------------   
    noise = RCAIDE.Framework.Analyses.Noise.Frequency_Domain_Buildup()   
    noise.geometry = vehicle
    noise.settings.noise_hemisphere                       = True 
    noise.settings.noise_hemisphere_radius                = 20          
    noise.settings.noise_hemisphere_microphone_resolution = 3
    noise.settings.noise_hemisphere_phi_angle_bounds      = np.array([0,np.pi]) 
    noise.settings.noise_hemisphere_theta_angle_bounds    = np.array([np.pi/2,-np.pi/2])
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
#   Define the Vehicle Analyses
# ---------------------------------------------------------------------- 
def analyses_setup(configs):

    analyses = RCAIDE.Framework.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config) 
        analyses[tag] = analysis

    return analyses  
  

# ----------------------------------------------------------------------
#  Set Up Mission 
# ---------------------------------------------------------------------- 
def mission_setup(analyses,vehicle):  

    # Determine Stall Speed 
    vehicle_mass   = vehicle.mass_properties.max_takeoff
    reference_area = vehicle.reference_area
    altitude       = 0.0 
    CL_max         = 1.2  
    Vstall         = estimate_stall_speed(vehicle_mass,reference_area,altitude,CL_max)       
    
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------
    mission       = RCAIDE.Framework.Mission.Sequential_Segments()
    mission.tag   = 'mission' 
    Segments      = RCAIDE.Framework.Mission.Segments  
    base_segment  = Segments.Segment()   
    base_segment.state.numerics.number_of_control_points  = 5 
     
    # ------------------------------------------------------------------
    #   Constant Altitude Cruises 
    # ------------------------------------------------------------------   
    segment                                               = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag                                           = "Cruise" 
    segment.analyses.extend( analyses.base)                 
    segment.initial_battery_state_of_charge               = 0.89         
    segment.altitude                                      = 1000. * Units.ft 
    segment.air_speed                                     = Vstall*1.2       
    segment.distance                                      = 1000    
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.body_angle.active             = True                 
           
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
                          vehicle          = results.segments.cruise.analyses.aerodynamics.geometry,
                          show_figure      = regression_plotting_flag)      
    
     
    return noise_data 

if __name__ == '__main__': 
    main()    
    plt.show()
