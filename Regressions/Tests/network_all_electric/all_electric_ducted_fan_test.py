# battery_ducted_fan_network.py
# 
# Created:  Apr 2019, C. McMillan
#        

""" create and evaluate a battery ducted fan network
"""

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import RCAIDE
from RCAIDE.Core import Units
from RCAIDE.Core import Data
from RCAIDE.Visualization                 import *      
from RCAIDE.Energy.Networks.All_Electric_Ducted_Fan      import All_Electric_Ducted_Fan
from RCAIDE.Methods.Propulsion                           import design_ducted_fan 
from RCAIDE.Methods.Power.Battery.Sizing                 import initialize_from_mass 
from RCAIDE.Methods.Propulsion                           import  size_optimal_motor 
from RCAIDE.Methods.Power.Battery.Sizing                 import initialize_from_circuit_configuration
from RCAIDE.Methods.Weights.Correlations.Propulsion      import nasa_motor

# python imports     
import numpy as np  
import sys
import matplotlib.pyplot as plt   
from copy import deepcopy
import os

# local imports 
sys.path.append('../../Vehicles')
from NASA_X57    import vehicle_setup as   vehicle_setup 


# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------
def main():
   
    # Define internal combustion engine from Cessna Regression Aircraft 
    baseline_vehicle     = vehicle_setup()
    
    # Setup the modified constant speed version of the network
    vehicle = modify_vehicle(baseline_vehicle) 
    configs = configs_setup(vehicle)
     
    # create analyses
    analyses = analyses_setup(configs)

    # mission analyses
    mission  = mission_setup(analyses) 

    # create mission instances (for multiple types of missions)
    missions = missions_setup(mission) 

    # mission analysis 
    results = missions.base_mission.evaluate()   
     
    plot_results(results)
 
    #CL  = results.segments.cruise.conditions.aerodynamics.coefficients.lift[2][0] 
    #P   = results.segments.cruise.conditions.energy.bus.propulsor.ducted_fan.power[3][0]  
 

    ## RPM of rotor check during hover
    #CL_true = 0.35515343148759354
    #CL      = results.segments.cruise.conditions.aerodynamics.coefficients.lift[2][0] 
    #print('Lift Coefficient: ' + str(CL))
    #diff_CL   = np.abs(CL - CL_true)
    #print('CL difference')
    #print(diff_CL)
    #assert np.abs((CL - CL_true)/CL_true) < 1e-6  
    
    ## lift Coefficient Check During Cruise
    #P_true = 157734.9151012157
    #P      = results.segments.cruise.conditions.energy.bus.propulsor.ducted_fan.power[3][0]  
    #print('Power: ' + str(P )) 
    #diff_P                  = np.abs(P - P_true) 
    #print('CL difference')
    #print(diff_P )
    #assert np.abs((P  - P_true)/P_true) < 1e-6 

    return 
 

# ----------------------------------------------------------------------
#   Analysis Setup
# ---------------------------------------------------------------------- 

def modify_vehicle(vehicle):  
 
    # Replace the  all electric engine and propeller with a constant speed propeller  
    vehicle.networks.pop('all_electric')     

    net                      =  All_Electric_Ducted_Fan()  

    #------------------------------------------------------------------------------------------------------------------------------------  
    # Bus
    #------------------------------------------------------------------------------------------------------------------------------------  
    bus                              = RCAIDE.Energy.Distributors.Bus_Power_Control_Unit()
    bus.fixed_voltage                = True 

    #------------------------------------------------------------------------------------------------------------------------------------  
    # Electronic Speed Controller    
    #------------------------------------------------------------------------------------------------------------------------------------     
    esc_1            = RCAIDE.Energy.Distributors.Electronic_Speed_Controller()
    esc_1.tag        = 'esc_1'
    esc_1.efficiency = 0.95 
    bus.electronic_speed_controllers.append(esc_1)  
 
    esc_2            = RCAIDE.Energy.Distributors.Electronic_Speed_Controller()
    esc_2.tag        = 'esc_2'
    esc_2.efficiency = 0.95 
    bus.electronic_speed_controllers.append(esc_2)     


    #------------------------------------------------------------------------------------------------------------------------------------  
    # Ducted Fan
    #------------------------------------------------------------------------------------------------------------------------------------     

    #instantiate the ducted fan network
    ducted_fan                      = RCAIDE.Energy.Converters.Ducted_Fan()  
    ducted_fan.engine_length        = 1.038 * Units.meter
    ducted_fan.nacelle_diameter     = 1  
    ducted_fan.areas.wetted         = 1.1*np.pi*ducted_fan.nacelle_diameter*ducted_fan.engine_length
    ducted_fan.design_thrust        = 5000   # 2500
    ducted_fan.design_altitude      = 25000. * Units.feet # 2500
    ducted_fan.design_mach_number   = 0.01     
    ducted_fan.origin               = [[2.,  2.5, 0.95]]  

    # working fluid
    ducted_fan.working_fluid = RCAIDE.Attributes.Gases.Air()

    # Ram 
    ram                                               = RCAIDE.Energy.Converters.Ram()
    ram.tag                                           = 'ram' 
    ducted_fan.ram                                    = ram 

    #  Inlet Nozzle 
    inlet_nozzle                                      = RCAIDE.Energy.Converters.Compression_Nozzle()
    inlet_nozzle.tag                                  = 'inlet_nozzle' 
    inlet_nozzle.polytropic_efficiency                = 0.98
    inlet_nozzle.pressure_ratio                       = 0.98 
    ducted_fan.inlet_nozzle                           = inlet_nozzle

    # Fan                
    fan                                               = RCAIDE.Energy.Converters.Fan()   
    fan.tag                                           = 'fan' 
    fan.polytropic_efficiency                         = 0.93
    fan.pressure_ratio                                = 1.7     
    ducted_fan.fan                                    = fan

    # Fan Nozzle                
    fan_nozzle                                        = RCAIDE.Energy.Converters.Expansion_Nozzle()   
    fan_nozzle.tag                                    = 'fan_nozzle' 
    fan_nozzle.polytropic_efficiency                  = 0.95
    fan_nozzle.pressure_ratio                         = 0.99  
    ducted_fan.fan_nozzle                             = fan_nozzle   

    ducted_fan                                        = design_ducted_fan(ducted_fan)
    ducted_fan_2                                      = deepcopy(ducted_fan)
    ducted_fan_2.tag                                  = 'ducted_fan_2' 
    ducted_fan_2.origin                               = [[2., -2.5, 0.95]] 
    bus.ducted_fans.append(ducted_fan)  
    bus.ducted_fans.append(ducted_fan_2)  

    #------------------------------------------------------------------------------------------------------------------------------------           
    # Battery
    #------------------------------------------------------------------------------------------------------------------------------------  
    bat                                                    = RCAIDE.Energy.Storages.Batteries.Lithium_Ion_NMC() 
    bat.pack.electrical_configuration.series               = 140   
    bat.pack.electrical_configuration.parallel             = 100
    initialize_from_circuit_configuration(bat)  
    bat.module_config.number_of_modules                    = 14  
    bat.module.geometrtic_configuration.total              = bat.pack.electrical_configuration.total
    bat.module_config.voltage                              = bat.pack.maximum_voltage/bat.module_config.number_of_modules # assumes modules are connected in parallel, must be less than max_module_voltage (~50) /safety_factor (~ 1.5)  
    bat.module.geometrtic_configuration.normal_count       = 24
    bat.module.geometrtic_configuration.parallel_count     = 40
    bat.thermal_management_system                          = RCAIDE.Energy.Thermal_Management.Batteries.Atmospheric_Air_Convection_Heat_Exchanger()      
    bus.voltage                                            = bat.pack.maximum_voltage  
    bus.batteries.append(bat)                                

 
    #------------------------------------------------------------------------------------------------------------------------------------           
    # Payload 
    #------------------------------------------------------------------------------------------------------------------------------------  
    payload                      = RCAIDE.Energy.Peripherals.Payload()
    payload.power_draw           =  0.
    payload.mass_properties.mass = 0. * Units.kg 
    net.payload                  = payload

    #------------------------------------------------------------------------------------------------------------------------------------  
    # Avionics
    #------------------------------------------------------------------------------------------------------------------------------------  
    avionics                     = RCAIDE.Energy.Peripherals.Avionics()
    avionics.power_draw          = 200. * Units.watts 
    net.avionics                 = avionics 
     
    net.busses.append(bus)
    vehicle.append_energy_network(net)    
                         
    
    return vehicle

  
def analyses_setup(configs):

    analyses = RCAIDE.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config)
        analyses[tag] = analysis

    return analyses

def base_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Analyses.Vehicle() 
    
    # ------------------------------------------------------------------
    #  Weights
    weights         = RCAIDE.Analyses.Weights.Weights_eVTOL()
    weights.vehicle = vehicle
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics          = RCAIDE.Analyses.Aerodynamics.Fidelity_Zero() 
    aerodynamics.geometry = vehicle
    aerodynamics.settings.drag_coefficient_increment = 0.0000
    analyses.append(aerodynamics)   

    # ------------------------------------------------------------------
    #  Energy
    energy          = RCAIDE.Analyses.Energy.Energy()
    energy.networks = vehicle.networks 
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

    # done!
    return analyses    

# ----------------------------------------------------------------------
#   Define the Mission
# ----------------------------------------------------------------------

def mission_setup(analyses): 
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------
    mission = RCAIDE.Analyses.Mission.Sequential_Segments()
    mission.tag = 'mission'
 

    # unpack Segments module
    Segments = RCAIDE.Analyses.Mission.Segments 
    
    # base segment
    base_segment = Segments.Segment()
    ones_row     = base_segment.state.ones_row
    base_segment.state.numerics.number_control_points  = 4     


    # ------------------------------------------------------------------
    #   Climb 1 : constant Speed, constant rate segment 
    # ------------------------------------------------------------------  

    segment = Segments.Climb.Linear_Speed_Constant_Rate(base_segment) 
    segment.tag = "Climb" 
    segment.analyses.extend( analyses.base ) 
    segment.altitude_start                                   = 5000   * Units.feet
    segment.altitude_end                                     = 25000    * Units.feet  
    segment.air_speed_start                                  = 300.     * Units['mph']  
    segment.air_speed_end                                    = 400     * Units['mph']   
    segment.climb_rate                                       = 500.    * Units['ft/min']     
    segment.initial_battery_state_of_charge                  = 1.0 
    segment.initial_battery_resistance_growth_factor         = 1
    segment.initial_battery_capacity_fade_factor             = 1
    segment = analyses.base.energy.networks.battery_ducted_fan.add_unknowns_and_residuals_to_segment(segment)          
    # add to misison
    mission.append_segment(segment) 
    

    ## ------------------------------------------------------------------
    ##   Cruise Segment: constant Speed, constant altitude
    ## ------------------------------------------------------------------ 
    #segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    #segment.tag = "Cruise"  
    #segment.analyses.extend(analyses.base) 
    #segment.altitude                  = 25000  * Units.feet
    #segment.air_speed                 = 400.    * Units['mph'] 
    #segment.distance                  = 50.   * Units.nautical_mile   
    #segment = analyses.base.energy.networks.battery_ducted_fan.add_unknowns_and_residuals_to_segment(segment)   

    ## add to misison
    #mission.append_segment(segment)    


    ## ------------------------------------------------------------------
    ##   Descent Segment Flight 1   
    ## ------------------------------------------------------------------ 
    #segment = Segments.Descent.Linear_Speed_Constant_Rate(base_segment) 
    #segment.tag = "Decent"  
    #segment.analyses.extend( analyses.base )       
    #segment.altitude_start                                   = 5000 * Units.feet  
    #segment.altitude_end                                     = 25000.0 * Units.feet
    #segment.air_speed_start                                  = 400.* Units['mph']  
    #segment.air_speed_end                                    = 300 * Units['mph']   
    #segment.descent_rate                                     = 200 * Units['ft/min']   
    #segment = analyses.base.energy.networks.battery_ducted_fan.add_unknowns_and_residuals_to_segment(segment)   
    
    ## add to misison
    #mission.append_segment(segment)    
    

    return mission

def missions_setup(mission): 
 
    missions         = RCAIDE.Analyses.Mission.Missions()
    
    # base mission 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions  
def plot_results(results):

    # Plot Flight Conditions 
    plot_flight_conditions(results) 
    
    # Plot Aerodynamic Coefficients
    plot_aerodynamic_coefficients(results)  
    
    # Plot Aircraft Flight Speed
    plot_aircraft_velocities(results)
    
    # Plot Aircraft Electronics
    plot_battery_pack_conditions(results) 
      
    return 
 
# ---------------------------------------------------------------------
#   Define the Configurations
# ---------------------------------------------------------------------

def configs_setup(vehicle):

    # ------------------------------------------------------------------
    #   Initialize Configurations
    # ------------------------------------------------------------------

    configs     = RCAIDE.Components.Configs.Config.Container() 
    base_config = RCAIDE.Components.Configs.Config(vehicle)
    base_config.tag = 'base' 
    base_config.networks.battery_ducted_fan.busses.bus.active_propulsor_groups = ['propulsor']  # default in network 
    configs.append(base_config) 

    # done!
    return configs

if __name__ == '__main__':
    
    main()
    plt.show()