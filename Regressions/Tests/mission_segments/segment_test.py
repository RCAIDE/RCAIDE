# segment_test.py
# 
# Created:  Dec 2023, M. Clarke 

""" setup file for segment test regression with a Boeing 737"""

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE
from RCAIDE.Core import Units ,  Data

# python imports 
import numpy as np
import pylab as plt 
import sys

# local imports 
sys.path.append('../../Vehicles')
from Boeing_737    import vehicle_setup as vehicle_setup
from Boeing_737    import configs_setup as configs_setup 

# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main(): 
    # -----------------------------------------
    # Multi-Point Mission Setup 
    # -----------------------------------------

    # vehicle data
    vehicle  = vehicle_setup() 
    
    # Set up vehicle configs
    configs  = configs_setup(vehicle)

    # create analyses
    analyses = analyses_setup(configs)

    # mission analyses 
    mission = mission_setup(analyses)
    
    # create mission instances (for multiple types of missions)
    missions = missions_setup(mission) 
     
    # mission analysis 
    results = missions.base_mission.evaluate()   
 
    # Extract sample values from computation  
    climb_throttle_1   = results.segments.climb_1.conditions.energy['fuel_line'].throttle[3][0]
    climb_throttle_2   = results.segments.climb_2.conditions.energy['fuel_line'].throttle[3][0]
    climb_throttle_3   = results.segments.climb_3.conditions.energy['fuel_line'].throttle[3][0]
    climb_throttle_4   = results.segments.climb_4.conditions.energy['fuel_line'].throttle[3][0]
    climb_throttle_5   = results.segments.climb_5.conditions.energy['fuel_line'].throttle[3][0]
    climb_throttle_6   = results.segments.climb_6.conditions.energy['fuel_line'].throttle[3][0]
    climb_throttle_7   = results.segments.climb_7.conditions.energy['fuel_line'].throttle[3][0] 
    climb_throttle_8   = results.segments.climb_8.conditions.energy['fuel_line'].throttle[3][0] 
    climb_throttle_9   = results.segments.climb_9.conditions.energy['fuel_line'].throttle[3][0] 
    #climb_throttle_10  = results.segments.climb_10.conditions.energy['fuel_line'].throttle[2][0] 
    cruise_CL_1        = results.segments.cruise_1.conditions.aerodynamics.coefficients.lift[2][0]
    #cruise_CL_2        = results.segments.cruise_2.conditions.aerodynamics.coefficients.lift[2][0]
    cruise_CL_3        = results.segments.cruise_3.conditions.aerodynamics.coefficients.lift[2][0] 
    descent_throttle_1 = results.segments.descent_1.conditions.energy['fuel_line'].throttle[3][0]
    descent_throttle_2 = results.segments.descent_2.conditions.energy['fuel_line'].throttle[3][0]
    single_pt_CL_1     = results.segments.single_point_1.conditions.aerodynamics.coefficients.lift[0][0]
    single_pt_CL_2     = results.segments.single_point_2.conditions.aerodynamics.coefficients.lift[0][0]     
    loiter_CL          = results.segments.loiter.conditions.aerodynamics.coefficients.lift[2][0]
    descent_throttle_3 = results.segments.descent_3.conditions.energy['fuel_line'].throttle[3][0]
    
    #print values for resetting regression
    show_vals = True
    if show_vals:
        data = [climb_throttle_1,   climb_throttle_2,   climb_throttle_3,   climb_throttle_4,   climb_throttle_5,  
                climb_throttle_6,   climb_throttle_7,   climb_throttle_8,   climb_throttle_9,     
                cruise_CL_1,            cruise_CL_3,        descent_throttle_1, descent_throttle_2,
                single_pt_CL_1,     single_pt_CL_2,     loiter_CL,          descent_throttle_3]
        for val in data:
            print(val)
    
    # Truth values
    climb_throttle_1_truth   = 0.7265077784727384
    climb_throttle_2_truth   = 0.6118143914441121
    climb_throttle_3_truth   = 0.3723788152034738
    climb_throttle_4_truth   = 0.6270973388656428
    climb_throttle_5_truth   = 0.7280160121482968
    climb_throttle_6_truth   = 1.1415131477663158
    climb_throttle_7_truth   = 1.3631793896219946
    climb_throttle_8_truth   = 0.6572467174770464
    climb_throttle_9_truth   = 0.729398886526951
    #climb_throttle_10_truth  = 
    cruise_CL_1_truth        = 0.7041944077903105
    #cruise_CL_2_truth        = 
    cruise_CL_3_truth        = 0.6693474728737692
    descent_throttle_1_truth = 0.23745730142466245
    descent_throttle_2_truth = 0.2652993270758505
    single_pt_CL_1_truth     = 0.0005628898058955994
    single_pt_CL_2_truth     = 0.0010056426448532005
    loiter_CL_truth          = 0.5080105756207646
    descent_throttle_3_truth = 0.1274222549112285
    
    # Store errors 
    error = Data()
    error.climb_throttle_1   = np.max(np.abs(climb_throttle_1     - climb_throttle_1_truth))  
    error.climb_throttle_2   = np.max(np.abs(climb_throttle_2     - climb_throttle_2_truth))   
    error.climb_throttle_3   = np.max(np.abs(climb_throttle_3     - climb_throttle_3_truth))   
    error.climb_throttle_4   = np.max(np.abs(climb_throttle_4     - climb_throttle_4_truth))   
    error.climb_throttle_5   = np.max(np.abs(climb_throttle_5     - climb_throttle_5_truth))   
    error.climb_throttle_6   = np.max(np.abs(climb_throttle_6     - climb_throttle_6_truth))   
    error.climb_throttle_7   = np.max(np.abs(climb_throttle_7     - climb_throttle_7_truth))   
    error.climb_throttle_8   = np.max(np.abs(climb_throttle_8     - climb_throttle_8_truth))  
    error.climb_throttle_9   = np.max(np.abs(climb_throttle_9     - climb_throttle_9_truth)) 
    #error.climb_throttle_10  = np.max(np.abs(climb_throttle_10    - climb_throttle_10_truth))  
    error.cruise_CL_1        = np.max(np.abs(cruise_CL_1          - cruise_CL_1_truth ))     
    #error.cruise_CL_2        = np.max(np.abs(cruise_CL_2          - cruise_CL_2_truth ))      
    error.cruise_CL_3        = np.max(np.abs(cruise_CL_3          - cruise_CL_3_truth ))     
    error.descent_throttle_1 = np.max(np.abs(descent_throttle_1   - descent_throttle_1_truth)) 
    error.descent_throttle_2 = np.max(np.abs(descent_throttle_2   - descent_throttle_2_truth))
    error.single_pt_CL_1     = np.max(np.abs(single_pt_CL_1       - single_pt_CL_1_truth ))     
    error.single_pt_CL_2     = np.max(np.abs(single_pt_CL_2       - single_pt_CL_2_truth ))  
    error.loiter_CL          = np.max(np.abs(loiter_CL            - loiter_CL_truth ))         
    error.descent_throttle_3 = np.max(np.abs(descent_throttle_3   - descent_throttle_3_truth))  
     
    print('Errors:')
    print(error)
     
    for k,v in list(error.items()):
        assert(np.abs(v)<1e-6)  
    
    plt.show()    
    return 
# ----------------------------------------------------------------------
#   Define the Vehicle Analyses
# ----------------------------------------------------------------------

def analyses_setup(configs):

    analyses = RCAIDE.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in list(configs.items()):
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
    weights                                          = RCAIDE.Analyses.Weights.Weights_Transport()
    weights.vehicle                                  = vehicle
    analyses.append(weights)
 
    #  Aerodynamics Analysis
    aerodynamics                                     = RCAIDE.Analyses.Aerodynamics.Subsonic_VLM()
    aerodynamics.geometry                            = vehicle
    aerodynamics.settings.number_spanwise_vortices   = 5
    aerodynamics.settings.number_chordwise_vortices  = 2       
    aerodynamics.settings.drag_coefficient_increment = 0.0000
    analyses.append(aerodynamics)
 
    ##  Stability Analysis
    #stability                                        = RCAIDE.Analyses.Stability.Fidelity_Zero()
    #stability.geometry                               = vehicle
    #analyses.append(stability)
 
    #  Energy
    energy                                           = RCAIDE.Analyses.Energy.Energy()
    energy.networks                                  = vehicle.networks  
    analyses.append(energy)
 
    #  Planet Analysis
    planet                                           = RCAIDE.Analyses.Planets.Planet()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere                                       = RCAIDE.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet                       = planet.features
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
    mission.tag = 'the_mission'
  
    Segments = RCAIDE.Analyses.Mission.Segments 
    base_segment = Segments.Segment()
    base_segment.state.numerics.number_control_points = 4  
 
    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    ##   Takeoff Roll
    ## ------------------------------------------------------------------------------------------------------------------------------------ 

    #segment = Segments.Ground.Takeoff(base_segment)
    #segment.tag = "Takeoff" 
    #segment.analyses.extend( analyses.takeoff )
    #segment.velocity_start           = 100.* Units.knots
    #segment.velocity_end             = 150 * Units.knots
    #segment.friction_coefficient     = 0.04
    #segment.altitude                 = 0.0   
    #mission.append_segment(segment)
    

    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    ##    Climb 1 : Constant Speed Constant Rate  
    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    #segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    #segment.tag = "climb_1" 
    #segment.analyses.extend( analyses.takeoff )  
    #segment.altitude_end                                  = 1.0  * Units.km
    #segment.air_speed                                     = 150   * Units.knots
    #segment.climb_rate                                    = 10.0  * Units['m/s'] 
    
    ## define flight dynamics to model 
    #segment.flight_dynamics.force_x                       = True  
    #segment.flight_dynamics.force_z                       = True     
    
    ## define flight controls 
    #segment.flight_controls.throttle.active               = True           
    #segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]
    #segment.flight_controls.throttle.initial_values       = [[0.5]] 
    #segment.flight_controls.body_angle.active             = True               
    #segment.flight_controls.body_angle.initial_values     = [[3*Units.degrees]]
    
    #mission.append_segment(segment)

   
    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    ##   Climb 2 : Constant Dynamic Pressure Constant Angle 
    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    #segment = Segments.Climb.Constant_Dynamic_Pressure_Constant_Angle(base_segment)
    #segment.tag = "climb_2"
    #segment.analyses.extend( analyses.base )  
    #segment.altitude_end                                  = 2.    * Units.km
    #segment.climb_angle                                   = 5.   * Units.degrees 
    #segment.dynamic_pressure                              = 3800 * Units.pascals  
    
    ## define flight dynamics to model 
    #segment.flight_dynamics.force_x                       = True  
    #segment.flight_dynamics.force_z                       = True     
    
    ## define flight controls 
    #segment.flight_controls.throttle.active               = True           
    #segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]
    #segment.flight_controls.throttle.initial_values       = [[0.5]] 
    #segment.flight_controls.body_angle.active             = True               
    #segment.flight_controls.body_angle.initial_values     = [[3*Units.degrees]]
    #segment.flight_controls.altitude.active               = True 
      
    #mission.append_segment(segment)

    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    ##   Climb 3 : Constant Dynamic Pressure Constant Rate 
    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    #segment = Segments.Climb.Constant_Dynamic_Pressure_Constant_Rate(base_segment)
    #segment.tag = "climb_3"
    #segment.analyses.extend( analyses.base )  
    #segment.altitude_end                                  = 3.   * Units.km
    #segment.climb_rate                                    = 730. * Units['ft/min']    
    #segment.dynamic_pressure                              = 12000 * Units.pascals
    
    ## define flight dynamics to model 
    #segment.flight_dynamics.force_x                       = True  
    #segment.flight_dynamics.force_z                       = True     
    
    ## define flight controls 
    #segment.flight_controls.throttle.active               = True           
    #segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]
    #segment.flight_controls.throttle.initial_values       = [[0.5]] 
    #segment.flight_controls.body_angle.active             = True               
    #segment.flight_controls.body_angle.initial_values     = [[3*Units.degrees]]
      
    #mission.append_segment(segment)
    
    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    ##   Climb 4 : Constant Mach Constant Angle 
    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    #segment = Segments.Climb.Constant_Mach_Constant_Angle(base_segment)
    #segment.tag = "climb_4"
    #segment.analyses.extend( analyses.base )  
    #segment.altitude_end                                   = 4.   * Units.km
    #segment.mach_number                                    = 0.5
    #segment.climb_angle                                    = 3.5 * Units.degrees  
    
    ## define flight dynamics to model 
    #segment.flight_dynamics.force_x                       = True  
    #segment.flight_dynamics.force_z                       = True     
    
    ## define flight controls 
    #segment.flight_controls.throttle.active               = True           
    #segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]
    #segment.flight_controls.throttle.initial_values       = [[0.5]] 
    #segment.flight_controls.body_angle.active             = True               
    #segment.flight_controls.body_angle.initial_values     = [[3*Units.degrees]]
      
    #mission.append_segment(segment)

    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    ##   Climb 5 : 
    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    #segment = Segments.Climb.Constant_Speed_Constant_Angle(base_segment)
    #segment.tag = "climb_5"
    #segment.analyses.extend( analyses.base )  
    #segment.altitude_end                                  = 5.    * Units.km
    #segment.air_speed                                     = 180   * Units.m / Units.s
    #segment.climb_angle                                   = 3.    * Units.degrees 
    
    ## define flight dynamics to model 
    #segment.flight_dynamics.force_x                       = True  
    #segment.flight_dynamics.force_z                       = True     
    
    ## define flight controls 
    #segment.flight_controls.throttle.active               = True           
    #segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]
    #segment.flight_controls.throttle.initial_values       = [[0.5]] 
    #segment.flight_controls.body_angle.active             = True               
    #segment.flight_controls.body_angle.initial_values     = [[3*Units.degrees]]
       
    #mission.append_segment(segment)
    
    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    ##   Climb 6 : 
    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    #segment = Segments.Climb.Constant_Mach_Linear_Altitude(base_segment)
    #segment.tag = "climb_6"
    #segment.analyses.extend( analyses.base )  
    #segment.altitude_end                                  = 6. * Units.km   
    #segment.mach_number                                   = 0.75   
    
    ## define flight dynamics to model 
    #segment.flight_dynamics.force_x                       = True  
    #segment.flight_dynamics.force_z                       = True     
    
    ## define flight controls 
    #segment.flight_controls.throttle.active               = True           
    #segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]
    #segment.flight_controls.throttle.initial_values       = [[0.5]] 
    #segment.flight_controls.body_angle.active             = True               
    #segment.flight_controls.body_angle.initial_values     = [[3*Units.degrees]]
    
    #mission.append_segment(segment)

    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    ##   Climb 7 : Constant Speed Linear Altitude 
    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    #segment = Segments.Climb.Constant_Speed_Linear_Altitude(base_segment)
    #segment.tag = "climb_7"
    #segment.analyses.extend( analyses.base ) 
    #segment.altitude_start                                = 7.    * Units.km
    #segment.altitude_end                                  = 9.    * Units.km   
    #segment.air_speed                                     = 250.2 * Units.m / Units.s 
    
    ## define flight dynamics to model 
    #segment.flight_dynamics.force_x                       = True  
    #segment.flight_dynamics.force_z                       = True     
    
    ## define flight controls 
    #segment.flight_controls.throttle.active               = True           
    #segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]
    #segment.flight_controls.throttle.initial_values       = [[0.5]] 
    #segment.flight_controls.body_angle.active             = True               
    #segment.flight_controls.body_angle.initial_values     = [[3*Units.degrees]] 
    #mission.append_segment(segment)
 
    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    ##   Climb 8 : Constant EAS Constant Rate 
    ## ------------------------------------------------------------------------------------------------------------------------------------  
    #segment = Segments.Climb.Constant_EAS_Constant_Rate(base_segment)
    #segment.tag = "climb_8"
    #segment.analyses.extend( analyses.base )  
    #segment.altitude_end                                 = 8.   * Units.km    
    #segment.equivalent_air_speed                         = 150. * Units.m / Units.s
    #segment.climb_rate                                   = 1.   
    
    ## define flight dynamics to model 
    #segment.flight_dynamics.force_x                      = True  
    #segment.flight_dynamics.force_z                      = True     
    
    ## define flight controls 
    #segment.flight_controls.throttle.active              = True           
    #segment.flight_controls.throttle.assigned_propulsors = [['starboard_propulsor','port_propulsor']]
    #segment.flight_controls.throttle.initial_values      = [[0.5]] 
    #segment.flight_controls.body_angle.active            = True               
    #segment.flight_controls.body_angle.initial_values    = [[3*Units.degrees]]
    
    #mission.append_segment(segment)

    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    ##   Climb 9 : Constant EAS Constant Rate 
    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    #segment = Segments.Climb.Constant_CAS_Constant_Rate(base_segment)
    #segment.tag = "climb_9"
    #segment.analyses.extend( analyses.base )  
    #segment.altitude_end                                 = 9. * Units.km    
    #segment.calibrated_air_speed                         = 150. * Units.m / Units.s
    #segment.climb_rate                                   = 1.  
    
    ## define flight dynamics to model 
    #segment.flight_dynamics.force_x                      = True  
    #segment.flight_dynamics.force_z                      = True     
    
    ## define flight controls 
    #segment.flight_controls.throttle.active              = True           
    #segment.flight_controls.throttle.assigned_propulsors = [['starboard_propulsor','port_propulsor']]
    #segment.flight_controls.throttle.initial_values      = [[0.5]] 
    #segment.flight_controls.body_angle.active            = True               
    #segment.flight_controls.body_angle.initial_values    = [[3*Units.degrees]]
     
    #mission.append_segment(segment)
    


    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    ##   Climb 10 : Constant EAS Constant Rate 
    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    #segment = Segments.Climb.Constant_Throttle_Constant_Speed(base_segment)
    #segment.tag = "climb_10"
    #segment.analyses.extend( analyses.base )  
    #segment.altitude_end                                 = 11.   * Units.km    
    #segment.air_speed                                    = 150. * Units.m / Units.s
    #segment.throttle                                     = 0.5 
    
    ## define flight dynamics to model 
    #segment.flight_dynamics.force_x                      = True  
    #segment.flight_dynamics.force_z                      = True     
    
    ## define flight controls 
    #segment.flight_controls.wind_angle.active           = True            
    #segment.flight_controls.wind_angle.initial_values   = [[ 1.0 * Units.deg]] 
    #segment.flight_controls.body_angle.active           = True               
    #segment.flight_controls.body_angle.initial_values   = [[ 5.0 * Units.deg]]
     
    #mission.append_segment(segment)
    
    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    ###   Climb 10 : Optimized
    ## ------------------------------------------------------------------------------------------------------------------------------------ 
    ##segment = Segments.Climb.Optimized(base_segment)
    ##segment.tag = "climb_11"
    ##segment.analyses.extend( analyses.base )  
    ##segment.altitude_start         = 10.9   * Units.km   
    ##segment.altitude_end           = 11.0   * Units.km   
    ##segment.air_speed_start        = 160. * Units.m / Units.s
    ##segment.air_speed_end          = None
    ##segment.objective              = 'conditions.frames.inertial.time[-1,0]*1000'
    ##segment.minimize               = True
    ##segment.state.numerics.number_control_points = 3 
    ##mission.append_segment(segment)
        
    
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    #   Cruise Segment 1: constant Speed, constant altitude
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    segment = Segments.Cruise.Constant_Dynamic_Pressure_Constant_Altitude(base_segment)
    segment.tag = "cruise_1" 
    segment.analyses.extend(analyses.base) 
    segment.altitude                                      = 11. * Units.km    
    segment.dynamic_pressure                              = 28000 * Units.pascals   
    segment.distance                                      = 500 * Units.km  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]
    segment.flight_controls.throttle.initial_values       = [[0.5]] 
    segment.flight_controls.body_angle.active             = True               
    segment.flight_controls.body_angle.initial_values     = [[3*Units.degrees]]
    
    mission.append_segment(segment)    

    # ------------------------------------------------------------------------------------------------------------------------------------ 
    ##   Cruise Segment 2: Constant Throttle Constant Altltude
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    #segment = Segments.Cruise.Constant_Throttle_Constant_Altitude(base_segment)
    #segment.tag = "cruise_2" 
    #segment.analyses.extend(analyses.base)  
    #segment.air_speed_start                      = 200 * Units.m / Units.s 
    #segment.air_speed_end                        = 210 * Units.m / Units.s 
    #segment.throttle                             = 0.5
    #segment.distance                             = 500 * Units.km 
    #segment.state.numerics.number_control_points = 32
    #segment.state.unknowns.accel_x               = 0.1 * ones_row(1)
    #segment.state.unknowns.time                  = 100.  
    #mission.append_segment(segment)   
    
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    #   Cruise Segment 3 : Constant Pitch Rate Constant Altltude
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    segment = Segments.Cruise.Constant_Pitch_Rate_Constant_Altitude(base_segment)
    segment.tag = "cruise_3" 
    segment.analyses.extend(analyses.base) 
    segment.altitude                                     = 10. * Units.km    
    segment.pitch_rate                                   = 0.0001  * Units['rad/s/s']
    segment.pitch_final                                  = 4.  * Units.degrees 
    segment.distance                                     = 500 * Units.km   
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active              = True           
    segment.flight_controls.throttle.assigned_propulsors = [['starboard_propulsor','port_propulsor']]
    segment.flight_controls.throttle.initial_values      = [[0.9]] 
    segment.flight_controls.velocity.active              = True               
    segment.flight_controls.velocity.initial_values      = [[ 200]] 
        
    mission.append_segment(segment)   
    
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    #   Descent Segment 1: Constant Speed Constant Angle 
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    segment = Segments.Descent.Constant_Speed_Constant_Angle(base_segment)
    segment.tag = "descent_1" 
    segment.analyses.extend( analyses.base ) 
    segment.altitude_start                                = 10. * Units.km    
    segment.air_speed                                     = 150 * Units.m / Units.s 
    segment.altitude_end                                  = 5  * Units.km  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]
    segment.flight_controls.throttle.initial_values       = [[0.5]] 
    segment.flight_controls.body_angle.active             = True               
    segment.flight_controls.body_angle.initial_values     = [[3*Units.degrees]]
    
    mission.append_segment(segment) 

    # ------------------------------------------------------------------------------------------------------------------------------------ 
    #   Descent Segment 2: Constant CAS Constant Angle 
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    segment = Segments.Descent.Constant_CAS_Constant_Rate(base_segment)
    segment.tag = "descent_2" 
    segment.analyses.extend( analyses.base ) 
    segment.altitude_end                                  = 2500. * Units.feet
    segment.descent_rate                                  = 2.  * Units.m / Units.s
    segment.calibrated_air_speed                          = 100 * Units.m / Units.s
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]
    segment.flight_controls.throttle.initial_values       = [[0.5]] 
    segment.flight_controls.body_angle.active             = True               
    segment.flight_controls.body_angle.initial_values     = [[3*Units.degrees]]
     
    mission.append_segment(segment) 

    # ------------------------------------------------------------------------------------------------------------------------------------ 
    #  Single Point Segment 1: constant Speed, constant altitude
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    segment = Segments.Single_Point.Set_Speed_Set_Altitude(base_segment)
    segment.tag = "single_point_1" 
    segment.analyses.extend(analyses.base) 
    segment.altitude                                      =  2500. * Units.feet
    segment.air_speed                                     =  200. * Units['m/s']  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]
    segment.flight_controls.throttle.initial_values       = [[0.5]] 
    segment.flight_controls.body_angle.active             = True               
    segment.flight_controls.body_angle.initial_values     = [[3*Units.degrees]]
     
    mission.append_segment(segment)    
    
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    #  Single Point Segment 1: constant Speed, constant altitude
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    segment = Segments.Single_Point.Set_Speed_Set_Throttle(base_segment)
    segment.tag = "single_point_2" 
    segment.analyses.extend(analyses.base) 
    segment.altitude                                      =  2500. * Units.feet
    segment.air_speed                                     =  200. * Units['m/s']   
    segment.throttle                                      =  0.5 
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls   
    segment.flight_controls.body_angle.active             = True               
    segment.flight_controls.body_angle.initial_values     = [[3*Units.degrees]]
    
    mission.append_segment(segment)    
    
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    #   Loiter Segment: Constant Dynamic Pressure Constant Altitude Loiter
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    segment = Segments.Cruise.Constant_Dynamic_Pressure_Constant_Altitude_Loiter(base_segment)
    segment.tag = "loiter" 
    segment.analyses.extend(analyses.base) 
    segment.altitude                  = 2500  * Units.feet
    segment.dynamic_pressure          = 12000 * Units.pascals  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]
    segment.flight_controls.throttle.initial_values       = [[0.5]] 
    segment.flight_controls.body_angle.active             = True               
    segment.flight_controls.body_angle.initial_values     = [[3*Units.degrees]]
    
    mission.append_segment(segment)   
       
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    #   Descent Segment: Constant EAS Constant Rate
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    segment = Segments.Descent.Constant_EAS_Constant_Rate(base_segment)
    segment.tag = "descent_3" 
    segment.analyses.extend( analyses.base ) 
    segment.altitude_start                                = 2500  * Units.feet
    segment.altitude_end                                  = 0  * Units.feet 
    segment.descent_rate                                  = 3.  * Units.m / Units.s
    segment.equivalent_air_speed                          = 100 * Units.m / Units.s 
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]
    segment.flight_controls.throttle.initial_values       = [[0.5]] 
    segment.flight_controls.body_angle.active             = True               
    segment.flight_controls.body_angle.initial_values     = [[3*Units.degrees]]
    
    mission.append_segment(segment)   

    # ------------------------------------------------------------------------------------------------------------------------------------ 
    #   Landing Roll
    # ------------------------------------------------------------------------------------------------------------------------------------ 

    segment = Segments.Ground.Landing(base_segment)
    segment.tag = "Landing"

    segment.analyses.extend( analyses.landing )
    segment.velocity_start                                = 150 * Units.knots
    segment.velocity_end                                  = 100 * Units.knots
    segment.state.unknowns.time                           = 30.
    segment.friction_coefficient                          = 0.4
    segment.altitude                                      = 0.0 
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True       
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]
    segment.flight_controls.throttle.initial_values       = [[0.5]] 
    
    mission.append_segment(segment)     


    # ------------------------------------------------------------------------------------------------------------------------------------ 
    #   Non Converged Segment : Constant Throttle Constant Altltude
    # ------------------------------------------------------------------------------------------------------------------------------------  
    segment = Segments.Cruise.Constant_Throttle_Constant_Altitude(base_segment)
    segment.tag = "cruise_non_converged" 
    segment.analyses.extend(analyses.base)    
    segment.air_speed_end                                  = 150 * Units.knots
    segment.throttle                                       = 0
    segment.distance                                       = 10 * Units.km 
    segment.state.numerics.number_control_points           = 2
    segment.state.numerics.max_evaluations                 = 10 
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                        = True  
    segment.flight_dynamics.force_z                        = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]
    segment.flight_controls.throttle.initial_values       = [[0.5]] 
    segment.flight_controls.body_angle.active             = True               
    segment.flight_controls.body_angle.initial_values     = [[3*Units.degrees]]
    
    mission.append_segment(segment)     

        
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    #   Mission definition complete    
    # ------------------------------------------------------------------------------------------------------------------------------------  
    
    return mission


def missions_setup(mission): 
 
    missions     = RCAIDE.Analyses.Mission.Missions() 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions  


if __name__ == '__main__': 
    main()    
