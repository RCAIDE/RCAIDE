# Regression/scripts/Tests/network_all_electric/all_electric_network_test.py
# 
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
from NASA_X57    import vehicle_setup, configs_setup 


# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------  
def main():     
    
    battery_chemistry       =  ['NMC','LFP']
    
    # ----------------------------------------------------------------------
    #  True Values  
    # ----------------------------------------------------------------------    

    # General Aviation Aircraft   

    RPM_true              = [1597.730347228566,1597.7303471313394]
    lift_coefficient_true = [0.3519728024171797,0.35197280241717954]  
        
    for i in range(len(battery_chemistry)): 
        print(battery_chemistry[i] + ' Battery Electric Aircraft') 
         
        # vehicle data
        baseline_vehicle  = vehicle_setup()
        vehicle           = modify_vehicle(baseline_vehicle,battery_chemistry[i])
    
        # Set up configs
        configs  = configs_setup(vehicle)
    
        # vehicle analyses
        analyses = analyses_setup(configs)
    
        # mission analyses
        mission  = mission_setup(analyses)
        missions = missions_setup(mission) 
         
        results = missions.base_mission.evaluate() 
         
        # plot the results
        if i == 0: 
            plot_results(results)  
        
        # RPM of rotor check during hover
        RPM        = results.segments.climb_flight_no_1_day_1.conditions.energy.bus.propulsor.rotor.rpm[3][0] 
        print('RPM: ' + str(RPM))
        diff_RPM   = np.abs(RPM - RPM_true[i])
        print('RPM difference: ' +  str(diff_RPM))
        assert np.abs((RPM - RPM_true[i])/RPM_true[i]) < 1e-6  
        
        # lift Coefficient Check During Cruise
        lift_coefficient        = results.segments.cruise_flight_no_1_day_1.conditions.aerodynamics.coefficients.lift[2][0] 
        print('CL: ' + str(lift_coefficient)) 
        diff_CL                 = np.abs(lift_coefficient  - lift_coefficient_true[i]) 
        print('CL difference: ' +  str(diff_CL)) 
        assert np.abs((lift_coefficient  - lift_coefficient_true[i])/lift_coefficient_true[i]) < 1e-6 
             
    return


# ----------------------------------------------------------------------
#   Analysis Setup
# ---------------------------------------------------------------------- 

def modify_vehicle(vehicle,battery_chemistry): 
    
    # Modify the battery 
    bus = vehicle.networks.all_electric.busses.bus
    bus.batteries.pop((list(bus.batteries.keys())[0]))
    if battery_chemistry   == 'NMC': 
        bat = RCAIDE.Energy.Storages.Batteries.Lithium_Ion_NMC()  
        bat.thermal_management_system  = RCAIDE.Energy.Thermal_Management.Batteries.No_Heat_Exchanger()  
    elif battery_chemistry == 'LFP':  
        bat = RCAIDE.Energy.Storages.Batteries.Lithium_Ion_LFP()    
        bat.thermal_management_system  = RCAIDE.Energy.Thermal_Management.Batteries.Atmospheric_Air_Convection_Heat_Exchanger()  

    bat.pack.electrical_configuration.series               = 140   
    bat.pack.electrical_configuration.parallel             = 100
    initialize_from_circuit_configuration(bat)  
    bat.module.number_of_modules                           = 14  
    bat.module.geometrtic_configuration.total              = bat.pack.electrical_configuration.total
    bat.module.voltage                                     = bat.pack.maximum_voltage/bat.module.number_of_modules  
    bat.module.geometrtic_configuration.normal_count       = 24
    bat.module.geometrtic_configuration.parallel_count     = 40 
    bus.voltage                                            = bat.pack.maximum_voltage  
    bus.batteries.append(bat)                                     
    
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
    aerodynamics          = RCAIDE.Analyses.Aerodynamics.Subsonic_VLM() 
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
    
    flights_per_day = 1 
    simulated_days  = 1
    for day in range(simulated_days): 
         
        atmosphere         = RCAIDE.Analyses.Atmospheric.US_Standard_1976() 
        atmo_data          = atmosphere.compute_values(altitude = 0,temperature_deviation= 1.)   

        # compute daily temperature in san francisco: link: https://www.usclimatedata.com/climate/san-francisco/california/united-states/usca0987/2019/1
        daily_temp = (13.5 + (day)*(-0.00882) + (day**2)*(0.00221) + (day**3)*(-0.0000314) + (day**4)*(0.000000185)  + \
                      (day**5)*(-0.000000000483)  + (day**6)*(4.57E-13)) + 273.2
        base_segment.temperature_deviation = daily_temp - atmo_data.temperature[0][0]
        
        for flight_no in range(flights_per_day): 
    
            # ------------------------------------------------------------------
            #   Climb 1 : constant Speed, constant rate segment 
            # ------------------------------------------------------------------  

            segment = Segments.Climb.Linear_Speed_Constant_Rate(base_segment) 
            segment.tag = "climb"  + "_flight_no_" + str(flight_no+ 1) + "_day_" + str (day+1) 
            segment.analyses.extend( analyses.base ) 
            segment.altitude_start                                   = 2500.0  * Units.feet
            segment.altitude_end                                     = 8012    * Units.feet  
            segment.air_speed_start                                  = 100.     * Units['mph']  
            segment.air_speed_end                                    = 150     * Units['mph']   
            segment.climb_rate                                       = 500.    * Units['ft/min']     
            segment.battery_cell_temperature                         = atmo_data.temperature[0,0]
            if (day == 0) and (flight_no == 0):        
                segment.initial_battery_state_of_charge              = 0.89 
                segment.initial_battery_resistance_growth_factor     = 1
                segment.initial_battery_capacity_fade_factor         = 1 
            mission.append_segment(segment) 
            
        
            # ------------------------------------------------------------------
            #   Cruise Segment: constant Speed, constant altitude
            # ------------------------------------------------------------------ 
            segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
            segment.tag = "cruise"  + "_flight_no_" + str(flight_no+ 1) + "_day_" + str (day+ 1) 
            segment.analyses.extend(analyses.base) 
            segment.altitude                  = 8012   * Units.feet
            segment.air_speed                 = 150.    * Units['mph'] 
            segment.distance                  = 50.   * Units.nautical_mile    
            mission.append_segment(segment)    
        
        
            # ------------------------------------------------------------------
            #   Descent Segment Flight 1   
            # ------------------------------------------------------------------ 
            segment = Segments.Descent.Linear_Speed_Constant_Rate(base_segment) 
            segment.tag = "decent"   + "_flight_no_" + str(flight_no+ 1) + "_day_" + str (day+ 1) 
            segment.analyses.extend( analyses.base )       
            segment.altitude_start                                   = 8012 * Units.feet  
            segment.altitude_end                                     = 2500.0 * Units.feet
            segment.air_speed_start                                  = 150.* Units['mph']  
            segment.air_speed_end                                    = 90 * Units['mph']   
            segment.descent_rate                                     = 200 * Units['ft/min']      
            mission.append_segment(segment)
            
            # ------------------------------------------------------------------
            #  Charge Segment: 
            # ------------------------------------------------------------------     
            # Charge Model 
            segment                                                 = Segments.Ground.Battery_Recharge(base_segment)     
            segment.tag                                             = 'Recharge'  + "_F_" + str(flight_no+ 1) + "_D" + str (day+ 1) 
            segment.current                                         = 100
            segment.analyses.extend(analyses.base)                       
            segment.time                                            = 1.5 * Units.hr
            if flight_no  == flights_per_day:  
                segment.increment_battery_age_by_one_day            =True                            
            mission.append_segment(segment)        

    return mission

def missions_setup(mission): 
 
    missions         = RCAIDE.Analyses.Mission.Missions()
    
    # base mission 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions  
def plot_results(results):

    # Plots fligh conditions 
    plot_flight_conditions(results) 
    
    # Plot arcraft trajectory
    plot_flight_trajectory(results)   
    
    # Plot Aircraft Electronics
    plot_battery_pack_conditions(results) 
    plot_battery_temperature(results)
    plot_battery_cell_conditions(results) 
    plot_battery_pack_C_rates(results)
    plot_battery_degradation(results) 
    
    # Plot Propeller Conditions 
    plot_rotor_conditions(results) 
    plot_disc_and_power_loading(results)
    
    # Plot Electric Motor and Propeller Efficiencies 
    plot_electric_efficiencies(results)  
      
    return 

if __name__ == '__main__': 
    main()    
    plt.show()
