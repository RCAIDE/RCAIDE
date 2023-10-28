# Regression/scripts/Tests/network_solar/solar_netwwork_test.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 

import RCAIDE
from RCAIDE.Core                                                     import Units , Data
from RCAIDE.Visualization                                            import *      
from RCAIDE.Visualization.Geometry.Three_Dimensional.plot_3d_vehicle import plot_3d_vehicle 

# python imports 
import matplotlib.pyplot as plt    
import numpy as np
import copy, time 

# local imports 
import sys 
sys.path.append('../../Vehicles') 
from Solar_UAV import vehicle_setup, configs_setup

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
    mission  = mission_setup(analyses) 

    # create mission instances (for multiple types of missions)
    missions = missions_setup(mission) 

    # mission analysis 
    results = missions.base_mission.evaluate()  
       
    ## plt the old results
    plot_mission(results) 
    
    # Check Results 
    F       = results.segments.cruise.conditions.frames.body.thrust_force_vector[1,0]
    rpm     = results.segments.cruise.conditions.energy.bus.propulsor.rotor.rpm[1,0]
    current = results.segments.cruise.conditions.energy.bus.Generic_Lithium_Ion_Battery_Cell.pack.current[1,0]
    energy  = results.segments.cruise.conditions.energy.bus.Generic_Lithium_Ion_Battery_Cell.pack.energy[8,0]  
    
    # Truth results

    truth_F   = 82.50753846534745
    truth_rpm = 194.40119841312963
    truth_i   = -88.56579017873031
    truth_bat = 124499438.4272672
    
    #print('battery energy')
    #print(energy)
    #print('\n')
    
    #error = Data()
    #error.Thrust   = np.max(np.abs((F-truth_F)/truth_F))
    #error.RPM      = np.max(np.abs((rpm-truth_rpm)/truth_rpm))
    #error.Current  = np.max(np.abs((current-truth_i)/truth_i))
    #error.Battery  = np.max(np.abs((energy-truth_bat)/truth_bat))
    
    #print(error)
    
    #for k,v in list(error.items()):
        #assert(np.abs(v)<1e-6)
 
    # Plot vehicle 
    plot_3d_vehicle(configs.base, save_figure = False, show_wing_control_points = True,show_figure = False)
    
    return


# ----------------------------------------------------------------------        
#   Setup Analyses
# ----------------------------------------------------------------------  

def analyses_setup(configs):
    
    analyses = RCAIDE.Analyses.Analysis.Container()
    
    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config)
        analyses[tag] = analysis
    
    return analyses

# ----------------------------------------------------------------------        
#   Define Base Analysis
# ----------------------------------------------------------------------  

def base_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses                             = RCAIDE.Analyses.Vehicle() 
    
    # ------------------------------------------------------------------
    #  Weights
    weights                              = RCAIDE.Analyses.Weights.Weights_UAV() 
    weights.vehicle                      = vehicle
    analyses.append(weights)
    
    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics                                     = RCAIDE.Analyses.Aerodynamics.Fidelity_Zero() 
    aerodynamics.geometry                            = vehicle
    aerodynamics.settings.drag_coefficient_increment = 0.0000
    aerodynamics.settings.span_efficiency            = 0.98
    analyses.append(aerodynamics)
    
    # ------------------------------------------------------------------
    #  Energy
    energy                               = RCAIDE.Analyses.Energy.Energy()
    energy.networks                      = vehicle.networks  
    analyses.append(energy) 
    
    # ------------------------------------------------------------------
    #  Planet Analysis
    planet                               = RCAIDE.Analyses.Planets.Planet()
    analyses.append(planet)
    
    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere                           = RCAIDE.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet           = planet.features
    analyses.append(atmosphere)   
 
    return analyses    


# ----------------------------------------------------------------------
#   Define the Mission
# ----------------------------------------------------------------------
def mission_setup(analyses):
    
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------

    mission = RCAIDE.Analyses.Mission.Sequential_Segments()
    mission.tag = 'The Test Mission' 
    mission.atmosphere  = RCAIDE.Attributes.Atmospheres.Earth.US_Standard_1976()
    mission.planet      = RCAIDE.Attributes.Planets.Earth()
    
    # unpack Segments module
    Segments = RCAIDE.Analyses.Mission.Segments
    
    # base segment
    base_segment = Segments.Segment() 
    
    # ------------------------------------------------------------------    
    #   Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------    
    
    segment                                 = RCAIDE.Analyses.Mission.Segments.Cruise.Constant_Mach_Constant_Altitude(base_segment)
    segment.tag                             = "cruise" 
    segment.analyses.extend( analyses.base) 
    segment.start_time                      = time.strptime("Tue, Jun 21 11:30:00  2020", "%a, %b %d %H:%M:%S %Y",)
    segment.altitude                        = 15.0  * Units.km 
    segment.mach_number                     = 0.1
    segment.distance                        = 3050.0 * Units.km
    segment.initial_battery_state_of_charge = 0.3  
    segment.latitude                        = 37.4300     
    segment.longitude                       = -122.1700   
    segment = analyses.base.energy.networks.solar.add_unknowns_and_residuals_to_segment(segment)    
    
    
    mission.append_segment(segment)    

    # ------------------------------------------------------------------    
    #   Mission definition complete    
    # ------------------------------------------------------------------
    
    return mission 


def missions_setup(mission): 

    missions     = RCAIDE.Analyses.Mission.Missions()

    # base mission 
    mission.tag  = 'base_mission'
    missions.append(mission)

    return missions  

# ----------------------------------------------------------------------
#   Plot Mission
# ----------------------------------------------------------------------

def plot_mission(results):     
    
    # Plot Propeller Performance 
    plot_rotor_conditions(results)
    
    # Plot Power and Disc Loading
    plot_disc_and_power_loading(results)
    
    # Plot Solar Radiation Flux
    plot_solar_network_conditions(results) 
    
    return 

# ----------------------------------------------------------------------        
#   Call Main
# ----------------------------------------------------------------------    

if __name__ == '__main__':
    main()
    plt.show()
