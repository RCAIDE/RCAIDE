# Regression/scripts/Tests/network_solar/solar_netwwork_test.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 

import RCAIDE
from RCAIDE.Core                                                     import Units , Data,
from RCAIDE.Visualization                                            import *      
from RCAIDE.Visualization.Geometry.Three_Dimensional.plot_3d_vehicle import plot_3d_vehicle 

# python imports 
import matplotlib.pyplot as plt    
import numpy as np
import copy, time 

# local imports 
import sys 
sys.path.append('../Vehicles') 
from Solar_UAV import vehicle_setup, configs_setup

# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------  
def main():
    
 
    # vehicle data
    vehicle  = vehicle_setup()
    configs  = configs_setup(vehicle)
    
    # vehicle analyses
    configs_analyses = analyses_setup(configs)
    
    # mission analyses
    mission  = mission_setup(configs_analyses,vehicle)
    missions_analyses = missions_setup(mission)

    analyses = RCAIDE.Analyses.Analysis.Container()
    analyses.configs  = configs_analyses
    analyses.missions = missions_analyses
    
    configs.finalize()
    analyses.finalize()    
    
    # weight analysis
    weights = analyses.configs.base.weights    
    
    # mission analysis
    mission = analyses.missions.base
    results = mission.evaluate()  

    ## plt the old results
    plot_mission(results) 
    
    # Check Results 
    F       = results.segments.cruise1.conditions.frames.body.thrust_force_vector[1,0]
    rpm     = results.segments.cruise1.conditions.propulsion.propulsor_group_0.rotor.rpm[1,0]
    current = results.segments.cruise1.conditions.propulsion.battery.pack.current[1,0]
    energy  = results.segments.cruise1.conditions.propulsion.battery.pack.energy[8,0]  
    
    # Truth results

    truth_F   = 82.50753846534745
    truth_rpm = 194.40119841312963
    truth_i   = -88.56579017873031
    truth_bat = 124628733.86762737
    
    print('battery energy')
    print(energy)
    print('\n')
    
    error = Data()
    error.Thrust   = np.max(np.abs((F-truth_F)/truth_F))
    error.RPM      = np.max(np.abs((rpm-truth_rpm)/truth_rpm))
    error.Current  = np.max(np.abs((current-truth_i)/truth_i))
    error.Battery  = np.max(np.abs((energy-truth_bat)/truth_bat))
    
    print(error)
    
    for k,v in list(error.items()):
        assert(np.abs(v)<1e-6)
 
    # Plot vehicle 
    plot_3d_vehicle(configs.cruise, save_figure = False, show_wing_control_points = True,show_figure = False)
    
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
    analyses = RCAIDE.Analyses.Vehicle()
    
    # ------------------------------------------------------------------
    #  Basic Geometry Relations
    sizing = RCAIDE.Analyses.Sizing.Sizing()
    sizing.features.vehicle = vehicle
    analyses.append(sizing)
    
    # ------------------------------------------------------------------
    #  Weights
    weights = RCAIDE.Analyses.Weights.Weights_UAV()
    weights.settings.empty_weight_method = \
        RCAIDE.Methods.Weights.Correlations.Human_Powered.empty
    weights.vehicle = vehicle
    analyses.append(weights)
    
    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics = RCAIDE.Analyses.Aerodynamics.Fidelity_Zero() 
    aerodynamics.geometry                            = vehicle
    aerodynamics.settings.drag_coefficient_increment = 0.0000
    aerodynamics.settings.span_efficiency = 0.98
    analyses.append(aerodynamics)
    
    # ------------------------------------------------------------------
    #  Energy
    energy = RCAIDE.Analyses.Energy.Energy()
    energy.network = vehicle.networks #what is called throughout the mission (at every time step))
    analyses.append(energy)
    
    # ------------------------------------------------------------------
    #  Planet Analysis
    planet = RCAIDE.Analyses.Planets.Planet()
    analyses.append(planet)
    
    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere = RCAIDE.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   
 
    return analyses    


# ----------------------------------------------------------------------
#   Define the Mission
# ----------------------------------------------------------------------
def mission_setup(analyses,vehicle):
    
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
    base_segment.process.iterate.initials.initialize_battery = RCAIDE.Methods.Missions.Segments.Common.Energy.initialize_battery
    
    # ------------------------------------------------------------------    
    #   Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------    
    
    segment = RCAIDE.Analyses.Mission.Segments.Cruise.Constant_Mach_Constant_Altitude(base_segment)
    segment.tag = "cruise1"
    
    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise)
    
    # segment attributes     
    segment.start_time     = time.strptime("Tue, Jun 21 11:30:00  2020", "%a, %b %d %H:%M:%S %Y",)
    segment.altitude       = 15.0  * Units.km 
    segment.mach_number    = 0.1
    segment.distance       = 3050.0 * Units.km
    segment.battery_energy = vehicle.networks.solar.battery.pack.max_energy*0.3 #Charge the battery to start
    segment.latitude       = 37.4300   # this defaults to degrees (do not use Units.degrees)
    segment.longitude      = -122.1700 # this defaults to degrees
    segment = vehicle.networks.solar.add_unknowns_and_residuals_to_segment(segment,initial_rotor_power_coefficients = [0.05])    
    
    
    mission.append_segment(segment)    

    # ------------------------------------------------------------------    
    #   Mission definition complete    
    # ------------------------------------------------------------------
    
    return mission


def missions_setup(base_mission):

    # the mission container
    missions = RCAIDE.Analyses.Mission.Mission.Container()

    # ------------------------------------------------------------------
    #   Base Mission
    # ------------------------------------------------------------------
    missions.base = base_mission 
    
    # done!
    return missions  

# ----------------------------------------------------------------------
#   Plot Mission
# ----------------------------------------------------------------------

def plot_mission(results,line_style='bo-'):     
    
    # Plot Propeller Performance 
    plot_rotor_conditions(results,line_style)
    
    # Plot Power and Disc Loading
    plot_disc_power_loading(results,line_style)
    
    # Plot Solar Radiation Flux
    plot_solar_flux(results,line_style) 
    
    return 

# ----------------------------------------------------------------------        
#   Call Main
# ----------------------------------------------------------------------    

if __name__ == '__main__':
    main()
    plt.show()
