# B737_noise.py
#
# Created: Apr 2021, M. Clarke 

""" setup file for the X57-Maxwell Electric Aircraft to valdiate noise in a climb segment
"""
 
# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import RCAIDE
from RCAIDE.Core import Units , Data 
from RCAIDE.Visualization import *      
from RCAIDE.Methods.Geometry.Two_Dimensional.Planform import wing_planform
from RCAIDE.Methods.Noise.Certification import turbofan_sideline_noise, turbofan_flyover_noise, turbofan_approach_noise 

import sys
import matplotlib.pyplot as plt 
import numpy as np     
from copy import deepcopy

# local imports 
sys.path.append('../../Vehicles')
from Embraer_190    import vehicle_setup as vehicle_setup
from Embraer_190    import configs_setup as configs_setup 

# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main():     

    # vehicle data
    vehicle                           = vehicle_setup()
    vehicle.wings.main_wing.control_surfaces.flap.configuration_type = 'triple_slotted'  
    vehicle.wings.main_wing.high_lift = True
    vehicle.wings.main_wing           = wing_planform(vehicle.wings.main_wing)
    
    # Set up configs
    configs           = configs_setup(vehicle) 
    analyses          = analyses_setup(configs) 
    
    mission           = baseline_mission_setup(analyses)
    basline_missions  = baseline_missions_setup(mission )     
    baseline_results  = basline_missions.base_mission.evaluate()   
    
    # certification calculations  
    mission           = sideline_mission_setup(analyses)
    sideline_missions = sideline_missions_setup(mission)     
    sideline_SPL      = turbofan_sideline_noise(sideline_missions,configs)  
    print('Sideline Noise: ',sideline_SP)

    mission           = flyover_mission_setup(analyses)
    flyover_missions  = flyover_missions_setup(mission )         
    flyover_SPL       = turbofan_flyover_noise(flyover_missions,configs)   
    print('Flyover Noise: ',flyover_SPL)

    mission           = approach_mission_setup(analyses)
    approach_missions = approach_missions_setup(mission)         
    approach_SPL      = turbofan_approach_noise(approach_missions,configs) 
    print('Approach Noise: ',approach_SPL)
    
    # SPL of rotor check during hover
    print('\n\n SAE Turbofan Aircraft Noise Model')
    B737_SPL        = baseline_results.segments.climb_1.conditions.noise.total_SPL_dBA[3][0]
    B737_SPL_true   = 21.799191185936067 
    B737_diff_SPL   = np.abs(B737_SPL - B737_SPL_true)
    print('SPL difference: ',B737_diff_SPL)
    assert np.abs((B737_SPL - B737_SPL_true)/B737_SPL_true) < 1e-6    
    return     
  
 

def base_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Analyses.Vehicle() 

    # ------------------------------------------------------------------
    #  Weights
    # ------------------------------------------------------------------
    weights = RCAIDE.Analyses.Weights.Weights_Transport()
    weights.vehicle = vehicle
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    # ------------------------------------------------------------------
    aerodynamics = RCAIDE.Analyses.Aerodynamics.Subsonic_VLM() 
    aerodynamics.geometry = vehicle
    aerodynamics.settings.drag_coefficient_increment = 0.0000 
    analyses.append(aerodynamics)

    # ------------------------------------------------------------------
    #  Noise Analysis
    # ------------------------------------------------------------------
    noise = RCAIDE.Analyses.Noise.Correlation_Buildup()   
    noise.geometry = vehicle          
    analyses.append(noise)

    # ------------------------------------------------------------------
    #  Energy
    # ------------------------------------------------------------------
    energy= RCAIDE.Analyses.Energy.Energy()
    energy.networks = vehicle.networks 
    analyses.append(energy)

    # ------------------------------------------------------------------
    #  Planet Analysis
    # ------------------------------------------------------------------
    planet = RCAIDE.Analyses.Planets.Planet()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    # ------------------------------------------------------------------
    atmosphere = RCAIDE.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   
 
    return analyses   
# ----------------------------------------------------------------------
#   Define the Vehicle Analyses
# ----------------------------------------------------------------------

def analyses_setup(configs):

    analyses = RCAIDE.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config)
        analyses[tag] = analysis

    return analyses 
 

def baseline_mission_setup(analyses): 
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------ 
    mission      = RCAIDE.Analyses.Mission.Sequential_Segments()
    mission.tag  = 'base_mission' 
    Segments     = RCAIDE.Analyses.Mission.Segments 
    base_segment = Segments.Segment() 

    # ------------------------------------------------------------------
    #   First Climb Segment: constant Mach, constant segment angle 
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_1" 
    segment.analyses.extend( analyses.takeoff ) 
    segment.altitude_start = 0.001   * Units.km
    segment.altitude_end   = 3.0   * Units.km
    segment.air_speed      = 125.0 * Units['m/s']
    segment.climb_rate     = 6.0   * Units['m/s'] 
    segment = analyses.base.energy.networks.turbofan_engine.add_unknowns_and_residuals_to_segment(segment)
    mission.append_segment(segment) 

    # ------------------------------------------------------------------
    #   Second Climb Segment: constant Speed, constant segment angle 
    # ------------------------------------------------------------------     
    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_2" 
    segment.analyses.extend( analyses.base ) 
    segment.altitude_end   = 8.0   * Units.km
    segment.air_speed      = 190.0 * Units['m/s']
    segment.climb_rate     = 6.0   * Units['m/s']  
    segment = analyses.base.energy.networks.turbofan_engine.add_unknowns_and_residuals_to_segment(segment)
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Third Climb Segment: constant Mach, constant segment angle 
    # ------------------------------------------------------------------   
    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_3" 
    segment.analyses.extend( analyses.base ) 
    segment.altitude_end = 10.668 * Units.km
    segment.air_speed    = 226.0  * Units['m/s']
    segment.climb_rate   = 3.0    * Units['m/s'] 
    segment = analyses.base.energy.networks.turbofan_engine.add_unknowns_and_residuals_to_segment(segment)
    mission.append_segment(segment) 

    # ------------------------------------------------------------------    
    #   Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------     
    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise" 
    segment.analyses.extend( analyses.base ) 
    segment.air_speed  = 230.412 * Units['m/s']
    segment.distance   = (3933.65 + 770 - 92.6) * Units.km 
    segment = analyses.base.energy.networks.turbofan_engine.add_unknowns_and_residuals_to_segment(segment)
    mission.append_segment(segment) 

    # ------------------------------------------------------------------
    #   First Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------ 
    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_1" 
    segment.analyses.extend( analyses.base ) 
    segment.altitude_end = 8.0   * Units.km
    segment.air_speed    = 220.0 * Units['m/s']
    segment.descent_rate = 4.5   * Units['m/s'] 
    segment = analyses.base.energy.networks.turbofan_engine.add_unknowns_and_residuals_to_segment(segment)
    mission.append_segment(segment) 

    # ------------------------------------------------------------------
    #   Second Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------ 
    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_2" 
    segment.analyses.extend( analyses.base ) 
    segment.altitude_end = 6.0   * Units.km
    segment.air_speed    = 195.0 * Units['m/s']
    segment.descent_rate = 5.0   * Units['m/s'] 
    segment = analyses.base.energy.networks.turbofan_engine.add_unknowns_and_residuals_to_segment(segment)
    mission.append_segment(segment) 

    # ------------------------------------------------------------------
    #   Third Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------ 
    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_3" 
    segment.analyses.extend( analyses.base ) 
    segment.altitude_end = 4.0   * Units.km
    segment.air_speed    = 170.0 * Units['m/s']
    segment.descent_rate = 5.0   * Units['m/s'] 
    segment = analyses.base.energy.networks.turbofan_engine.add_unknowns_and_residuals_to_segment(segment)
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Fourth Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------ 
    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_4" 
    segment.analyses.extend( analyses.base ) 
    segment.altitude_end = 2.0   * Units.km
    segment.air_speed    = 150.0 * Units['m/s']
    segment.descent_rate = 5.0   * Units['m/s'] 
    segment = analyses.base.energy.networks.turbofan_engine.add_unknowns_and_residuals_to_segment(segment)
    mission.append_segment(segment)
 

    # ------------------------------------------------------------------
    #   Fifth Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------ 
    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_5" 
    segment.analyses.extend( analyses.landing) 
    segment.altitude_end = 0.0   * Units.km
    segment.air_speed    = 145.0 * Units['m/s']
    segment.descent_rate = 3.0   * Units['m/s'] 
    segment = analyses.base.energy.networks.turbofan_engine.add_unknowns_and_residuals_to_segment(segment)
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Mission definition complete    
    # ------------------------------------------------------------------

    return mission 

def flyover_mission_setup(analyses):

    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------ 
    mission      = RCAIDE.Analyses.Mission.Sequential_Segments()
    mission.tag  = 'base_mission' 
    Segments     = RCAIDE.Analyses.Mission.Segments 
    base_segment = Segments.Segment() 
   
    # ------------------------------------------------------------------
    #   Mission for Takeoff Noise
    # ------------------------------------------------------------------      
    takeoff                          = RCAIDE.Analyses.Mission.Sequential_Segments()
    takeoff.tag                      = 'takeoff'   
    Segments                         = RCAIDE.Analyses.Mission.Segments 
    base_segment                     = Segments.Segment() 
    
    # Climb Segment: Constant throttle, constant speed
    segment                           = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag                       = "climb"    
    segment.analyses.extend(analyses.base )  
    segment.altitude_start            =  35. *  Units.fts
    segment.altitude_end              = 304.8 *  Units.meter
    segment.air_speed                 = 85.4 * Units['m/s']
    segment.throttle                  = 1.   
    segment = analyses.base.energy.networks.turbofan_engine.add_unknowns_and_residuals_to_segment(segment)
    takeoff.append_segment(segment)

    # Cutback Segment: Constant speed, constant segment angle
    segment                           = Segments.Climb.Constant_Speed_Constant_Angle(base_segment)
    segment.tag                       = "cutback"     
    segment.analyses.extend(analyses.base )
    segment.air_speed                 = 85.4 * Units['m/s']
    segment.climb_angle               = 2.86  * Units.degrees 
    segment = analyses.base.energy.networks.turbofan_engine.add_unknowns_and_residuals_to_segment(segment)
    takeoff.append_segment(segment)   

    return takeoff

def sideline_mission_setup(analyses): 
    
    # ------------------------------------------------------------------
    #   Mission for Sideline Noise
    # ------------------------------------------------------------------     
    sideline_takeoff                  = RCAIDE.Analyses.Mission.Sequential_Segments()
    sideline_takeoff.tag              = 'sideline_takeoff' 
    Segments     = RCAIDE.Analyses.Mission.Segments 
    base_segment = Segments.Segment() 
    
    segment                           = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    segment.tag                       = "climb"    
    segment.analyses.extend(analyses.base) 
    segment.altitude_start            =  35. *  Units.fts
    segment.altitude_end              = 1600 *  Units.fts
    segment.air_speed                 = 85.4 * Units['m/s']
    segment.throttle                  = 1.  
    ones_row                          = segment.state.ones_row
    segment.state.unknowns.body_angle = ones_row(1) * 12. * Units.deg  
    segment.state.unknowns.wind_angle = ones_row(1) * 5. * Units.deg  
    segment = analyses.base.energy.networks.turbofan_engine.add_unknowns_and_residuals_to_segment(segment)
    sideline_takeoff.append_segment(segment)   
    
    return sideline_takeoff

def approach_mission_setup(analyses):
      
    # -------------------   -----------------------------------------------
    #   Mission for Landing Noise
    # ------------------------------------------------------------------    
    landing                           = RCAIDE.Analyses.Mission.Sequential_Segments()
    landing.tag                       = 'landing'    
    Segments                          = RCAIDE.Analyses.Mission.Segments 
    base_segment                      = Segments.Segment() 
    
    segment                           = Segments.Descent.Constant_Speed_Constant_Angle(base_segment)
    segment.tag                       = "descent"
    segment.analyses.extend(analyses.base )   
    segment.altitude_start            = 2.0   * Units.km
    segment.altitude_end              = 0.
    segment.air_speed                 = 67. * Units['m/s']
    segment.descent_angle             = 3.0   * Units.degrees  
    segment = analyses.base.energy.networks.turbofan_engine.add_unknowns_and_residuals_to_segment(segment)
    landing.append_segment(segment)
    
    return landing
    
    
def baseline_missions_setup(base_mission):

    # the mission container
    missions     = RCAIDE.Analyses.Mission.Missions() 

    # ------------------------------------------------------------------
    #   Base Mission
    # ------------------------------------------------------------------ 
    base_mission.tag  = 'base_mission'
    missions.append(base_mission)

    # ------------------------------------------------------------------
    #   Mission for Constrained Fuel
    # ------------------------------------------------------------------  
    fuel_mission           =  deepcopy(base_mission) 
    fuel_mission.tag       = 'fuel'
    fuel_mission.range     = 1277. * Units.nautical_mile
    fuel_mission.payload   = 19000.
    missions.append(fuel_mission)   

    # ------------------------------------------------------------------
    #   Mission for Constrained Short Field
    # ------------------------------------------------------------------    
    short_field            =  deepcopy(base_mission) 
    short_field.tag        = 'short_field'   
    missions.append(short_field) 
    
    # ------------------------------------------------------------------
    #   Mission for Fixed Payload
    # ------------------------------------------------------------------    
    payload         =  deepcopy(base_mission) 
    payload.tag     = 'payload'
    payload.range   = 2316. * Units.nautical_mile
    payload.payload = 19000.
    missions.append(payload) 
     
    return missions  

def sideline_missions_setup(base_mission,analyses): 
    missions          = RCAIDE.Analyses.Mission.Missions()  
    base_mission.tag  = 'sideline_mission'
    missions.append(base_mission)  
    return missions  

def flyover_missions_setup(base_mission,analyses): 
    missions          = RCAIDE.Analyses.Mission.Missions()  
    base_mission.tag  = 'flyover_mission'
    missions.append(base_mission) 
     
    return missions 

def approach_missions_setup(base_mission,analyses): 
    missions          = RCAIDE.Analyses.Mission.Missions()  
    base_mission.tag  = 'approach_mission'
    missions.append(base_mission)  
    return missions 

if __name__ == '__main__': 
    main()    
    plt.show()
