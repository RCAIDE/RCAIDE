''' 
# transition_segment_test.py
# 
# Created: May 2019, M Clarke
#          Sep 2020, M. Clarke 

'''
#----------------------------------------------------------------------
#   Imports
# ---------------------------------------------------------------------
import RCAIDE
from RCAIDE.Framework.Core import Units, Data     
from RCAIDE.Library.Plots  import *       
  
# python imports     
import numpy as np  
import sys
import matplotlib.pyplot as plt  
 

# local imports 
sys.path.append('../../Vehicles')
from Tiltwing_EVTOL    import vehicle_setup, configs_setup

# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------
def main():  
    vehicle  = vehicle_setup() 

    plot_3d_vehicle(vehicle, show_figure  = False)    
        
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
    
    # Extract sample values from computation   
    vertical_climb_throttle                      = results.segments.vertical_climb.conditions.energy['bus']['lift_rotor_propulsor_1'].throttle[3][0]
    hover_throttle                               = results.segments.hover.conditions.energy['bus']['lift_rotor_propulsor_1'].throttle[3][0]
    vertical_climb_2_throttle                    = results.segments.vertical_climb_2.conditions.energy['bus']['lift_rotor_propulsor_1'].throttle[3][0]
    vertical_transition_throttle                 = results.segments.vertical_transition.conditions.energy['bus']['lift_rotor_propulsor_1'].throttle[3][0]
    low_speed_climb_transition_throttle          = results.segments.low_speed_climb_transition.conditions.energy['bus']['lift_rotor_propulsor_1'].throttle[3][0]
    high_speed_climb_transition_throttle         = results.segments.high_speed_climb_transition.conditions.energy['bus']['lift_rotor_propulsor_1'].throttle[3][0]
    cruise_throttle                              = results.segments.cruise.conditions.energy['bus']['lift_rotor_propulsor_1'].throttle[3][0] 
    descent_throttle                             = results.segments.descent.conditions.energy['bus']['lift_rotor_propulsor_1'].throttle[3][0] 
    reserve_climb_throttle                       = results.segments.reserve_climb.conditions.energy['bus']['lift_rotor_propulsor_1'].throttle[3][0]  
    reserve_cruise_throttle                      = results.segments.reserve_cruise.conditions.energy['bus']['lift_rotor_propulsor_1'].throttle[3][0]
    reserve_descent_throttle                     = results.segments.reserve_descent.conditions.energy['bus']['lift_rotor_propulsor_1'].throttle[3][0] 
    
    #print values for resetting regression
    show_vals = True
    if show_vals:
        data = [vertical_climb_throttle,  hover_throttle,  vertical_climb_2_throttle ,  vertical_transition_throttle ,              
                low_speed_climb_transition_throttle,   high_speed_climb_transition_throttle, cruise_throttle,                            
                descent_throttle,    reserve_climb_throttle,  reserve_cruise_throttle,  reserve_descent_throttle,   ]
        for val in data:
            print(val)
    
    # Truth values
    vertical_climb_throttle_truth                       = 0.6076504419441053
    hover_throttle_truth                                = 0.6044572977444364
    vertical_climb_2_throttle_truth                     = 0.6079718628008569
    vertical_transition_throttle_truth                  = 0.6043028366156381
    low_speed_climb_transition_throttle_truth           = 0.5411198887621672
    high_speed_climb_transition_throttle_truth          = 0.3163340311366646
    cruise_throttle_truth                               = 0.33153148526487025
    descent_throttle_truth                              = 0.3123412690545646
    reserve_climb_throttle_truth                        = 0.2923889200977024
    reserve_cruise_throttle_truth                       = 0.30689740485385486
    reserve_descent_throttle_truth                      = 0.28269327552102963
    
    # Store errors 
    error = Data()
    error.vertical_climb_throttle                     = np.max(np.abs( vertical_climb_throttle_truth                        - vertical_climb_throttle                     )/ vertical_climb_throttle_truth                    )
    error.hover_throttle                              = np.max(np.abs( hover_throttle_truth                                 - hover_throttle                              )/ hover_throttle_truth                             )
    error.vertical_climb_2_throttle                   = np.max(np.abs( vertical_climb_2_throttle_truth                      - vertical_climb_2_throttle                   )/ vertical_climb_2_throttle_truth                  )
    error.vertical_transition_throttle                = np.max(np.abs( vertical_transition_throttle_truth                   - vertical_transition_throttle                )/ vertical_transition_throttle_truth               )
    error.low_speed_climb_transition_throttle         = np.max(np.abs( low_speed_climb_transition_throttle_truth            - low_speed_climb_transition_throttle         )/ low_speed_climb_transition_throttle_truth        )
    error.high_speed_climb_transition_throttle        = np.max(np.abs( high_speed_climb_transition_throttle_truth           - high_speed_climb_transition_throttle        )/ high_speed_climb_transition_throttle_truth       )
    error.cruise_throttle                             = np.max(np.abs( cruise_throttle_truth                                - cruise_throttle                             )/ cruise_throttle_truth                            )
    error.descent_throttle                            = np.max(np.abs( descent_throttle_truth                               - descent_throttle                            )/ descent_throttle_truth                           )
    error.reserve_climb_throttle                      = np.max(np.abs( reserve_climb_throttle_truth                         - reserve_climb_throttle                      )/ reserve_climb_throttle_truth                     )
    error.reserve_cruise_throttle                     = np.max(np.abs( reserve_cruise_throttle_truth                        - reserve_cruise_throttle                     )/ reserve_cruise_throttle_truth                    )
    error.reserve_descent_throttle                    = np.max(np.abs( reserve_descent_throttle_truth                       - reserve_descent_throttle                     )/ reserve_descent_throttle_truth               )
 
    print('Errors:')
    print(error)
     
    for k,v in list(error.items()):
        assert(np.abs(v)<1e-1)   # lower tolerance due to lose bounds on prop-rotor blade design 
    return     
 
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
 

def mission_setup(analyses ):
    

    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------
    mission = RCAIDE.Framework.Mission.Sequential_Segments()
    mission.tag = 'mission'

    # unpack Segments module
    Segments = RCAIDE.Framework.Mission.Segments  
    base_segment = Segments.Segment() 
     
  
 
    # ------------------------------------------------------------------
    #   First Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------ 
    segment                                            = Segments.Vertical_Flight.Climb(base_segment)
    segment.tag                                        = "Vertical_Climb"   
    segment.analyses.extend(analyses.vertical_climb) 
    segment.altitude_start                             = 0.0  * Units.ft  
    segment.altitude_end                               = 40.  * Units.ft  
    segment.initial_battery_state_of_charge            = 1.0 
    segment.climb_rate                                 = 100. * Units['ft/min'] 

    # define flight dynamics to model  
    segment.flight_dynamics.force_z                        = True 

    # define flight controls  
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['lift_rotor_propulsor_1','lift_rotor_propulsor_2','lift_rotor_propulsor_3','lift_rotor_propulsor_4',
                                                            'lift_rotor_propulsor_5','lift_rotor_propulsor_6','lift_rotor_propulsor_7','lift_rotor_propulsor_8']]
    
    mission.append_segment(segment)  
     

    # ------------------------------------------------------------------
    #   First Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------ 
    segment                                               = Segments.Vertical_Flight.Hover(base_segment)
    segment.tag                                           = "Hover"   
    segment.analyses.extend(analyses.vertical_climb)   
            
    # define flight dynamics to model  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['lift_rotor_propulsor_1','lift_rotor_propulsor_2','lift_rotor_propulsor_3','lift_rotor_propulsor_4',
                                                            'lift_rotor_propulsor_5','lift_rotor_propulsor_6','lift_rotor_propulsor_7','lift_rotor_propulsor_8']]
      
    mission.append_segment(segment)
 
 

    # ------------------------------------------------------------------
    #   First Climb Segment: Constant Speed, Constant Rate
    # ------------------------------------------------------------------ 
    segment                                            = Segments.Vertical_Flight.Climb(base_segment)
    segment.tag                                        = "Vertical_Climb_2"   
    segment.analyses.extend(analyses.vertical_climb)  
    segment.altitude_end                               = 60.  * Units.ft  
    segment.initial_battery_state_of_charge            = 1.0 
    segment.climb_rate                                 = 100. * Units['ft/min'] 

    # define flight dynamics to model  
    segment.flight_dynamics.force_z                        = True 

    # define flight controls  
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['lift_rotor_propulsor_1','lift_rotor_propulsor_2','lift_rotor_propulsor_3','lift_rotor_propulsor_4',
                                                            'lift_rotor_propulsor_5','lift_rotor_propulsor_6','lift_rotor_propulsor_7','lift_rotor_propulsor_8']]
    
    mission.append_segment(segment)  
     
          
    # ------------------------------------------------------------------
    #  First Transition Segment
    # ------------------------------------------------------------------ 
    segment                                               = Segments.Cruise.Constant_Acceleration_Constant_Altitude(base_segment)
    segment.tag                                           = "Vertical_Transition"  
    segment.analyses.extend( analyses.vertical_transition)   
    segment.air_speed_end                                 = 35 * Units['mph']     
    segment.acceleration                                  = 0.5

    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['lift_rotor_propulsor_1','lift_rotor_propulsor_2','lift_rotor_propulsor_3','lift_rotor_propulsor_4',
                                                                             'lift_rotor_propulsor_5','lift_rotor_propulsor_6','lift_rotor_propulsor_7','lift_rotor_propulsor_8']]
    segment.assigned_control_variables.body_angle.active             = True 
    
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   First Cruise Segment: Constant Acceleration, Constant Altitude
    # ------------------------------------------------------------------ 
    segment                          = Segments.Climb.Linear_Speed_Constant_Rate(base_segment)
    segment.tag                      = "low_speed_climb_transition" 
    segment.analyses.extend(analyses.climb_transition) 
    segment.climb_rate               = 500. * Units['ft/min'] 
    segment.air_speed_end            = 85.   * Units['mph'] 
    segment.altitude_start           = 40.0 * Units.ft    
    segment.altitude_end             = 100.0 * Units.ft

    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['lift_rotor_propulsor_1','lift_rotor_propulsor_2','lift_rotor_propulsor_3','lift_rotor_propulsor_4',
                                                                             'lift_rotor_propulsor_5','lift_rotor_propulsor_6','lift_rotor_propulsor_7','lift_rotor_propulsor_8']]
    segment.assigned_control_variables.body_angle.active             = True 
                                                                             
    mission.append_segment(segment)   
    
     
    # ------------------------------------------------------------------
    #  Second Transition Segment
    # ------------------------------------------------------------------ 
    segment                           = Segments.Cruise.Constant_Acceleration_Constant_Altitude(base_segment)
    segment.tag                       = "high_speed_climb_transition"  
    segment.analyses.extend( analyses.climb_transition)   
    segment.air_speed_end             = 125.  * Units['mph']  
    segment.acceleration              = 9.81/5 

    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['lift_rotor_propulsor_1','lift_rotor_propulsor_2','lift_rotor_propulsor_3','lift_rotor_propulsor_4',
                                                                             'lift_rotor_propulsor_5','lift_rotor_propulsor_6','lift_rotor_propulsor_7','lift_rotor_propulsor_8']]
    segment.assigned_control_variables.body_angle.active             = True
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   First Cruise Segment: Constant Acceleration, Constant Altitude
    # ------------------------------------------------------------------ 
    segment                           = Segments.Climb.Linear_Speed_Constant_Rate(base_segment)
    segment.tag                       = "Climb"  
    segment.analyses.extend(analyses.cruise) 
    segment.climb_rate                = 500. * Units['ft/min']
    segment.air_speed_start           = 125.   * Units['mph']
    segment.air_speed_end             = 130.  * Units['mph']  
    segment.altitude_start            = 100.0 * Units.ft   
    segment.altitude_end              = 2500.0 * Units.ft 
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['lift_rotor_propulsor_1','lift_rotor_propulsor_2','lift_rotor_propulsor_3','lift_rotor_propulsor_4',
                                                                             'lift_rotor_propulsor_5','lift_rotor_propulsor_6','lift_rotor_propulsor_7','lift_rotor_propulsor_8']]  
        
    segment.assigned_control_variables.body_angle.active             = True
    
    mission.append_segment(segment)
    
    

    # ------------------------------------------------------------------
    #   First Cruise Segment: Constant Acceleration, Constant Altitude
    # ------------------------------------------------------------------ 
    segment                          = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag                      = "Cruise"  
    segment.analyses.extend(analyses.cruise) 
    segment.altitude                 = 2500.0 * Units.ft
    segment.air_speed                = 130.  * Units['mph']   
    segment.distance                 = 30*Units.nmi
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['lift_rotor_propulsor_1','lift_rotor_propulsor_2','lift_rotor_propulsor_3','lift_rotor_propulsor_4',
                                                                             'lift_rotor_propulsor_5','lift_rotor_propulsor_6','lift_rotor_propulsor_7','lift_rotor_propulsor_8']]
    segment.assigned_control_variables.body_angle.active             = True
    mission.append_segment(segment)     
    
    # ------------------------------------------------------------------
    #    Descent Segment: Constant Acceleration, Constant Altitude
    # ------------------------------------------------------------------ 
    segment                          = Segments.Climb.Linear_Speed_Constant_Rate(base_segment)
    segment.tag                      = "Descent"  
    segment.analyses.extend(analyses.cruise)
    segment.climb_rate               = -300. * Units['ft/min']
    segment.air_speed_start          = 130.  * Units['mph'] 
    segment.air_speed_end            = 100.   * Units['mph'] 
    segment.altitude_start           = 2500.0 * Units.ft
    segment.altitude_end             = 100.0 * Units.ft

    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['lift_rotor_propulsor_1','lift_rotor_propulsor_2','lift_rotor_propulsor_3','lift_rotor_propulsor_4',
                                                                             'lift_rotor_propulsor_5','lift_rotor_propulsor_6','lift_rotor_propulsor_7','lift_rotor_propulsor_8']]
    segment.assigned_control_variables.body_angle.active             = True
    
        
    mission.append_segment(segment)     

    # ------------------------------------------------------------------
    #   Reserve Climb Segment 
    # ------------------------------------------------------------------ 
    segment                          = Segments.Climb.Linear_Speed_Constant_Rate(base_segment)
    segment.tag                      = "Reserve_Climb"   
    segment.analyses.extend(analyses.cruise) 
    segment.climb_rate               = 500. * Units['ft/min']
    segment.air_speed_start          = 100.   * Units['mph'] 
    segment.air_speed_end            = 120.  * Units['mph']  
    segment.altitude_start           = 100.0 * Units.ft 
    segment.altitude_end             = 1000.0 * Units.ft
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['lift_rotor_propulsor_1','lift_rotor_propulsor_2','lift_rotor_propulsor_3','lift_rotor_propulsor_4',
                                                                             'lift_rotor_propulsor_5','lift_rotor_propulsor_6','lift_rotor_propulsor_7','lift_rotor_propulsor_8']]
    segment.assigned_control_variables.body_angle.active             = True
             
    mission.append_segment(segment)      
 
    # ------------------------------------------------------------------
    #   First Cruise Segment: Constant Acceleration, Constant Altitude
    # ------------------------------------------------------------------ 
    segment                          = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment) 
    segment.tag                      = "Reserve_Cruise"  
    segment.analyses.extend(analyses.cruise)  
    segment.air_speed                = 120.  * Units['mph']  
    segment.distance                 = 10.*Units.nmi

    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['lift_rotor_propulsor_1','lift_rotor_propulsor_2','lift_rotor_propulsor_3','lift_rotor_propulsor_4',
                                                                             'lift_rotor_propulsor_5','lift_rotor_propulsor_6','lift_rotor_propulsor_7','lift_rotor_propulsor_8']]
    segment.assigned_control_variables.body_angle.active             = True
    
        
    mission.append_segment(segment)     
 
    # ------------------------------------------------------------------
    #   Reserve Descent Segment: Constant Acceleration, Constant Altitude
    # ------------------------------------------------------------------ 
    segment                          = Segments.Descent.Linear_Speed_Constant_Rate(base_segment)
    segment.tag                      = "Reserve_Descent" 
    segment.analyses.extend(analyses.cruise)
    segment.descent_rate             = 300. * Units['ft/min']
    segment.air_speed_start          = 120.  * Units['mph'] 
    segment.air_speed_end            = 85.   * Units['mph']
    segment.altitude_start           = 1000.0 * Units.ft
    segment.altitude_end             = 100.0 * Units.ft

    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['lift_rotor_propulsor_1','lift_rotor_propulsor_2','lift_rotor_propulsor_3','lift_rotor_propulsor_4',
                                                                             'lift_rotor_propulsor_5','lift_rotor_propulsor_6','lift_rotor_propulsor_7','lift_rotor_propulsor_8']]
    segment.assigned_control_variables.body_angle.active             = True 
        
    mission.append_segment(segment)        
     
    return mission

def missions_setup(mission): 
 
    missions         = RCAIDE.Framework.Mission.Missions()
    
    # base mission 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions  

# ----------------------------------------------------------------------
#   Plot Results
# ----------------------------------------------------------------------

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
