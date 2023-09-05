# Regression/scripts/Tests/network_all_electric/all_electric_network_test.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE
from RCAIDE.Core import Units  
from RCAIDE.Visualization                 import *      
from RCAIDE.Methods.Power.Battery.Sizing  import initialize_from_circuit_configuration

# python imports     
import numpy as np  
import sys
import matplotlib.pyplot as plt  

# local imports 
sys.path.append('../../Vehicles')
from NASA_X57    import vehicle_setup as   ECTOL_vehicle_setup
from NASA_X57    import configs_setup as   ECTOL_configs_setup 


# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------  
def main():     
    
    battery_chemistry       =  ['NMC','LFP']
    unknown_throttles       =  [[0.005,0.005,0.005],
                                [0.005,0.005,0.005]] 
    
    # ----------------------------------------------------------------------
    #  True Values  
    # ----------------------------------------------------------------------    

    # General Aviation Aircraft   

    RPM_true              = [2091.4442095019845,2091.4442092004297]
    lift_coefficient_true = [0.5405970801673611,0.5405970801669211]
     
    
        
    for i in range(len(battery_chemistry)):
        print('***********************************')
        print(battery_chemistry[i] + ' Cell Powered Aircraft')
        print('***********************************')
        
        print('\nBattery Propeller Network Analysis')
        print('--------------------------------------')
        
        configs, analyses = full_setup(battery_chemistry[i],unknown_throttles[i])  
        configs.finalize()
        analyses.finalize()   
         
        # mission analysis
        mission = analyses.missions.base
        results = mission.evaluate() 
         
        # plot the results
        plot_results(results)  
        
        # RPM of rotor check during hover
        RPM        = results.segments.climb_1_f_1_d1.conditions.propulsion.propulsor_group_0.rotor.rpm[3][0] 
        print('GA RPM: ' + str(RPM))
        diff_RPM   = np.abs(RPM - RPM_true[i])
        print('RPM difference')
        print(diff_RPM)
        assert np.abs((RPM - RPM_true[i])/RPM_true[i]) < 1e-6  
        
        # lift Coefficient Check During Cruise
        lift_coefficient        = results.segments.cruise_f_1_d1.conditions.aerodynamics.lift_coefficient[2][0] 
        print('GA CL: ' + str(lift_coefficient)) 
        diff_CL                 = np.abs(lift_coefficient  - lift_coefficient_true[i]) 
        print('CL difference')
        print(diff_CL)
        assert np.abs((lift_coefficient  - lift_coefficient_true[i])/lift_coefficient_true[i]) < 1e-6 
             
    return


# ----------------------------------------------------------------------
#   Analysis Setup
# ---------------------------------------------------------------------- 

def full_setup(battery_chemistry,unknown_throttles):

    # vehicle data
    vehicle  = ECTOL_vehicle_setup()
    
    # Modify the battery 
    net = vehicle.networks.all_electric
    net.batteries.pop((list(net.batteries.keys())[0]))
    if battery_chemistry   == 'NMC': 
        bat = RCAIDE.Energy.Storages.Batteries.Lithium_Ion_NMC()  
    elif battery_chemistry == 'LFP': 
        bat = RCAIDE.Energy.Storages.Batteries.Lithium_Ion_LFP()    

    bat.pack.electrical_configuration.series               = 140   
    bat.pack.electrical_configuration.parallel             = 100
    initialize_from_circuit_configuration(bat)  
    bat.module_config.number_of_modules                    = 14  
    bat.module.geometrtic_configuration.total              = bat.pack.electrical_configuration.total
    bat.module_config.voltage                              = bat.pack.maximum_voltage/bat.module_config.number_of_modules  
    bat.module.geometrtic_configuration.normal_count       = 24
    bat.module.geometrtic_configuration.parallel_count     = 40
    bat.thermal_management_system                          = RCAIDE.Energy.Thermal_Management.Batteries.Atmospheric_Air_Convection_Heat_Exchanger()     
    net.voltage                                            = bat.pack.maximum_voltage     
    net.batteries.append(bat) 
    
    # Set up configs
    configs  = ECTOL_configs_setup(vehicle)

    # vehicle analyses
    configs_analyses = analyses_setup(configs)

    # mission analyses
    mission  = mission_setup(configs_analyses,vehicle,unknown_throttles)
    missions_analyses = missions_setup(mission)

    analyses = RCAIDE.Analyses.Analysis.Container()
    analyses.configs  = configs_analyses
    analyses.missions = missions_analyses

    return configs, analyses

  
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
    #  Basic Geometry Relations
    sizing = RCAIDE.Analyses.Sizing.Sizing()
    sizing.features.vehicle = vehicle
    analyses.append(sizing)

    # ------------------------------------------------------------------
    #  Weights
    weights = RCAIDE.Analyses.Weights.Weights_eVTOL()
    weights.vehicle = vehicle
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics = RCAIDE.Analyses.Aerodynamics.Fidelity_Zero() 
    aerodynamics.geometry = vehicle
    aerodynamics.settings.drag_coefficient_increment = 0.0000
    analyses.append(aerodynamics)  

    # ------------------------------------------------------------------	
    #  Stability Analysis	
    stability = RCAIDE.Analyses.Stability.Fidelity_Zero()    	
    stability.geometry = vehicle	
    analyses.append(stability) 

    # ------------------------------------------------------------------
    #  Energy
    energy= RCAIDE.Analyses.Energy.Energy()
    energy.network = vehicle.networks 
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

def mission_setup(analyses,vehicle,unknown_throttles): 
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------
    mission = RCAIDE.Analyses.Mission.Sequential_Segments()
    mission.tag = 'mission'

    # airport
    airport            = RCAIDE.Attributes.Airports.Airport()
    airport.altitude   =  0. * Units.ft
    airport.delta_isa  =  0.0
    airport.atmosphere = RCAIDE.Attributes.Atmospheres.Earth.US_Standard_1976() 
    mission.airport    = airport  
    atmosphere         = RCAIDE.Analyses.Atmospheric.US_Standard_1976() 
    atmo_data          = atmosphere.compute_values(altitude = airport.altitude,temperature_deviation= 1.)  
    

    # unpack Segments module
    Segments = RCAIDE.Analyses.Mission.Segments 
    
    # base segment
    base_segment = Segments.Segment()
    ones_row     = base_segment.state.ones_row
    base_segment.process.initialize.initialize_battery                        = RCAIDE.Methods.Missions.Segments.Common.Energy.initialize_battery
    base_segment.process.finalize.post_process.update_battery_state_of_health = RCAIDE.Methods.Missions.Segments.Common.Energy.update_battery_state_of_health  
    base_segment.state.numerics.number_control_points                         = 4       
    
    flights_per_day = 2 
    simulated_days  = 2
    for day in range(simulated_days): 

        # compute daily temperature in san francisco: link: https://www.usclimatedata.com/climate/san-francisco/california/united-states/usca0987/2019/1
        daily_temp = (13.5 + (day)*(-0.00882) + (day**2)*(0.00221) + (day**3)*(-0.0000314) + (day**4)*(0.000000185)  + \
                      (day**5)*(-0.000000000483)  + (day**6)*(4.57E-13)) + 273.2
        
        base_segment.temperature_deviation = daily_temp - atmo_data.temperature[0][0]
        
                
        print(' ***********  Day ' + str(day+1) + ' ***********  ')
        for flight_no in range(flights_per_day): 
    
            # ------------------------------------------------------------------
            #   Climb 1 : constant Speed, constant rate segment 
            # ------------------------------------------------------------------  

            segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
            segment.tag = "Climb_1"  + "_F_" + str(flight_no+ 1) + "_D" + str (day+1) 
            segment.analyses.extend( analyses.base ) 
            segment.battery_energies                                 = [vehicle.networks.all_electric.batteries.lithium_ion_nmc.pack.maximum_energy * 0.89]
            segment.altitude_start                                   = 2500.0  * Units.feet
            segment.altitude_end                                     = 8012    * Units.feet 
            segment.air_speed                                        = 96.4260 * Units['mph'] 
            segment.climb_rate                                       = 700.034 * Units['ft/min']     
            segment.battery_pack_temperatures                        = [atmo_data.temperature[0,0]]
            if (day == 0) and (flight_no == 0):        
                segment.battery_energies                             = [vehicle.networks.all_electric.batteries.lithium_ion_nmc.pack.maximum_energy]   
                segment.initial_battery_resistance_growth_factor     = 1
                segment.initial_battery_capacity_fade_factor         = 1
            segment = vehicle.networks.all_electric.add_unknowns_and_residuals_to_segment(segment)          
            # add to misison
            mission.append_segment(segment) 
            
        
            # ------------------------------------------------------------------
            #   Cruise Segment: constant Speed, constant altitude
            # ------------------------------------------------------------------ 
            segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
            segment.tag = "Cruise"  + "_F_" + str(flight_no+ 1) + "_D" + str (day+ 1) 
            segment.analyses.extend(analyses.base) 
            segment.altitude                  = 8012   * Units.feet
            segment.air_speed                 = 120.91 * Units['mph'] 
            segment.distance                  =  20.   * Units.nautical_mile   
            segment = vehicle.networks.all_electric.add_unknowns_and_residuals_to_segment(segment,  initial_rotor_power_coefficients = [unknown_throttles[1]])   
        
            # add to misison
            mission.append_segment(segment)    
        
        
            # ------------------------------------------------------------------
            #   Descent Segment Flight 1   
            # ------------------------------------------------------------------ 
            segment = Segments.Climb.Linear_Speed_Constant_Rate(base_segment) 
            segment.tag = "Decent"   + "_F_" + str(flight_no+ 1) + "_D" + str (day+ 1) 
            segment.analyses.extend( analyses.base )       
            segment.altitude_start                                   = 8012 * Units.feet  
            segment.altitude_end                                     = 2500.0 * Units.feet
            segment.air_speed_start                                  = 175.* Units['mph']  
            segment.air_speed_end                                    = 110 * Units['mph']   
            segment.climb_rate                                       = -200 * Units['ft/min']  
            segment.state.unknowns.throttle                          = 0.8 * ones_row(1)  
            segment = vehicle.networks.all_electric.add_unknowns_and_residuals_to_segment(segment,  initial_rotor_power_coefficients = [unknown_throttles[2]])   
            
            # add to misison
            mission.append_segment(segment)
            
            # ------------------------------------------------------------------
            #  Charge Segment: 
            # ------------------------------------------------------------------     
            # Charge Model 
            segment                                                 = Segments.Ground.Battery_Recharge(base_segment)     
            segment.tag                                             = 'Recharge'  + "_F_" + str(flight_no+ 1) + "_D" + str (day+ 1) 
            segment.analyses.extend(analyses.base)                       
            if flight_no  == flights_per_day:  
                segment.increment_battery_age_by_one_day            =True                        
            segment = vehicle.networks.all_electric.add_unknowns_and_residuals_to_segment(segment)    
            
            # add to misison
            mission.append_segment(segment)        

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


def plot_results(results):  
     
    return

if __name__ == '__main__': 
    main()    
    plt.show()
