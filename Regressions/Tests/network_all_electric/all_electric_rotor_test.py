# Regression/scripts/Tests/network_all_electric/all_electric_network_test.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE
from RCAIDE.Framework.Core import Units  
from RCAIDE.Library.Plots  import *       

# python imports     
import numpy as np  
import sys
import matplotlib.pyplot as plt  

# local imports 
sys.path.append('../../Vehicles')
from Stopped_Rotor_EVTOL    import vehicle_setup, configs_setup 


# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------  
def main():           
         
    # vehicle data
    vehicle  = vehicle_setup()

    # plot vehicle 
    plot_3d_vehicle(vehicle, 
                    min_x_axis_limit            = -5,
                    max_x_axis_limit            = 15,
                    min_y_axis_limit            = -10,
                    max_y_axis_limit            = 10,
                    min_z_axis_limit            = -10,
                    max_z_axis_limit            = 10,
                    show_figure                 = False 
                    )           

    # Set up configs
    configs  = configs_setup(vehicle)

    # vehicle analyses
    analyses = analyses_setup(configs)

    # mission analyses
    mission  = mission_setup(analyses)
    missions = missions_setup(mission) 
     
    results = missions.base_mission.evaluate() 
     
    # plot the results 
    plot_results(results)    
    
    # lift Coefficient Check During Cruise
    lift_coefficient_true   = 0.7180063809031857
    lift_coefficient        = results.segments.high_speed_climbing_transition.conditions.aerodynamics.coefficients.lift.total[2][0] 
    print('CL: ' + str(lift_coefficient)) 
    diff_CL                 = np.abs(lift_coefficient  - lift_coefficient_true) 
    print('CL difference: ' +  str(diff_CL)) 
    assert np.abs((lift_coefficient  - lift_coefficient_true)/lift_coefficient_true) < 1e-6 
             
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
    #  Energy
    energy          = RCAIDE.Framework.Analyses.Energy.Energy()
    energy.vehicle  = vehicle 
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
    mission.tag = 'mission'

    # unpack Segments module
    Segments = RCAIDE.Framework.Mission.Segments 
    
    # base segment
    base_segment = Segments.Segment()
    base_segment.state.numerics.number_control_points  = 4       
    
    flights_per_day = 1 
    simulated_days  = 1
    for day in range(simulated_days): 
         
        atmosphere         = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976() 
        atmo_data          = atmosphere.compute_values(altitude = 0,temperature_deviation= 1.)   

        # compute daily temperature in san francisco: link: https://www.usclimatedata.com/climate/san-francisco/california/united-states/usca0987/2019/1
        daily_temp = (13.5 + (day)*(-0.00882) + (day**2)*(0.00221) + (day**3)*(-0.0000314) + (day**4)*(0.000000185)  + \
                      (day**5)*(-0.000000000483)  + (day**6)*(4.57E-13)) + 273.2
        base_segment.temperature_deviation = daily_temp - atmo_data.temperature[0][0]
        
        for flight_no in range(flights_per_day):  
            # ------------------------------------------------------------------
            #   Initialize the Mission
            # ------------------------------------------------------------------
        
            mission     = RCAIDE.Framework.Mission.Sequential_Segments()
            mission.tag = 'baseline_mission' 
            
            # unpack Segments module
            Segments = RCAIDE.Framework.Mission.Segments
        
            # base segment           
            base_segment  = Segments.Segment()   
            
            # VSTALL Calculation   
            Vstall         = 48.3144   
             
            #------------------------------------------------------------------------------------------------------------------------------------  
            # Vertical Climb 
            #------------------------------------------------------------------------------------------------------------------------------------  
            segment     = Segments.Vertical_Flight.Climb(base_segment)
            segment.tag = "Vertical_Climb"   
            segment.analyses.extend( analyses.vertical_flight )  
            segment.altitude_start                                = 0.0  * Units.ft  
            segment.altitude_end                                  = 200.  * Units.ft   
            segment.initial_battery_state_of_charge               = 1.0 
            segment.climb_rate                                    = 500. * Units['ft/min'] 
            segment.battery_cell_temperature                      = atmo_data.temperature[0,0]   
                    
            # define flight dynamics to model  
            segment.flight_dynamics.force_z                       = True     
            
            # define flight controls 
            segment.assigned_control_variables.throttle.active               = True           
            segment.assigned_control_variables.throttle.assigned_propulsors  = [['lift_propulsor_1','lift_propulsor_2','lift_propulsor_3','lift_propulsor_4',
                                                                      'lift_propulsor_5','lift_propulsor_6','lift_propulsor_7','lift_propulsor_8']] 
             
            if (day == 0) and (flight_no == 0):        
                segment.initial_battery_state_of_charge              = 0.89 
                segment.initial_battery_resistance_growth_factor     = 1
                segment.initial_battery_capacity_fade_factor         = 1             
               
            mission.append_segment(segment)
            
            #------------------------------------------------------------------------------------------------------------------------------------  
            # Low-Speed Transition
            #------------------------------------------------------------------------------------------------------------------------------------  
         
            segment                                               = Segments.Transition.Constant_Acceleration_Constant_Pitchrate_Constant_Altitude(base_segment)
            segment.tag                                           = "Low_Speed_Transition"  
            segment.analyses.extend( analyses.transition_flight )   
            segment.altitude                                      = 200.  * Units.ft           
            segment.air_speed_start                               = 500. * Units['ft/min']
            segment.air_speed_end                                 = 0.75 * Vstall
            segment.acceleration                                  = 1.5
            segment.pitch_initial                                 = 0.0 * Units.degrees
            segment.pitch_final                                   = 2.  * Units.degrees    
        
            # define flight dynamics to model 
            segment.flight_dynamics.force_x                       = True  
            segment.flight_dynamics.force_z                       = True     
            
            # define flight controls 
            segment.assigned_control_variables.throttle.active               = True           
            segment.assigned_control_variables.throttle.assigned_propulsors  = [['cruise_propulsor_1','cruise_propulsor_2'],
                                                                     ['lift_propulsor_1','lift_propulsor_2','lift_propulsor_3','lift_propulsor_4',
                                                                    'lift_propulsor_5','lift_propulsor_6','lift_propulsor_7','lift_propulsor_8']]
            mission.append_segment(segment) 
            
            #------------------------------------------------------------------------------------------------------------------------------------  
            # High-Speed Climbing Transition 
            #------------------------------------------------------------------------------------------------------------------------------------  
            segment                                               = Segments.Transition.Constant_Acceleration_Constant_Angle_Linear_Climb(base_segment)
            segment.tag                                           = "High_Speed_Climbing_Transition" 
            segment.analyses.extend( analyses.transition_flight)    
            segment.altitude_start                                = 200.0 * Units.ft   
            segment.altitude_end                                  = 500.0 * Units.ft   
            segment.air_speed_start                               = 0.75   * Vstall
            segment.climb_angle                                   = 3     * Units.degrees   
            segment.acceleration                                  = 0.25  * Units['m/s/s'] 
            segment.pitch_initial                                 = 2.    * Units.degrees 
            segment.pitch_final                                   = 7.    * Units.degrees   
        
            # define flight dynamics to model 
            segment.flight_dynamics.force_x                       = True  
            segment.flight_dynamics.force_z                       = True     
            
            # define flight controls 
            segment.assigned_control_variables.throttle.active               = True           
            segment.assigned_control_variables.throttle.assigned_propulsors  = [['cruise_propulsor_1','cruise_propulsor_2'],
                                                                     ['lift_propulsor_1','lift_propulsor_2','lift_propulsor_3','lift_propulsor_4',
                                                                    'lift_propulsor_5','lift_propulsor_6','lift_propulsor_7','lift_propulsor_8']]
            mission.append_segment(segment) 
           
            #------------------------------------------------------------------------------------------------------------------------------------ 
            # Vertical Descent 
            #------------------------------------------------------------------------------------------------------------------------------------ 
            segment                                               = Segments.Vertical_Flight.Descent(base_segment)
            segment.tag                                           = "Vertical_Descent" 
            segment.analyses.extend( analyses.vertical_flight)     
            segment.altitude_start                                = 300.0 * Units.ft   
            segment.altitude_end                                  = 0.   * Units.ft  
            segment.descent_rate                                  = 300. * Units['ft/min']  
            
            # define flight dynamics to model  
            segment.flight_dynamics.force_z                       = True     
            
            # define flight controls 
            segment.assigned_control_variables.throttle.active               = True           
            segment.assigned_control_variables.throttle.assigned_propulsors  = [['lift_propulsor_1','lift_propulsor_2','lift_propulsor_3','lift_propulsor_4',
                                                                      'lift_propulsor_5','lift_propulsor_6','lift_propulsor_7','lift_propulsor_8']] 
                    
            mission.append_segment(segment)  
          
        
            # ------------------------------------------------------------------
            #  Charge Segment: 
            # ------------------------------------------------------------------  
            # Charge Model 
            segment                                         = Segments.Ground.Battery_Recharge(base_segment)     
            segment.analyses.extend(analyses.base)              
            segment.tag                                     = 'Recharge' 
            segment.time                                    = 1 * Units.hr
            segment.current                                 = 100 
            if flight_no  == flights_per_day:  
                segment.increment_battery_age_by_one_day    =True     
            mission.append_segment(segment)                

    return mission


def missions_setup(mission): 
 
    missions         = RCAIDE.Framework.Mission.Missions()
    
    # base mission 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions

def plot_results(results):

    # Plots fligh conditions 
    plot_flight_conditions(results) 
    
    # Plot arcraft trajectory
    plot_flight_trajectory(results)   

    plot_propulsor_throttles(results)
    
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
    plot_electric_propulsor_efficiencies(results)  
      
    return 

if __name__ == '__main__': 
    main()    
    plt.show()
