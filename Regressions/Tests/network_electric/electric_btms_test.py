# Regression/scripts/Tests/network_all_electric/electric_btms_test.py
# 
# 
# Created:  Sep 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE
from RCAIDE.Framework.Core import Units  
from RCAIDE.Library.Plots  import *
from RCAIDE.Library.Methods.Performance.estimate_stall_speed        import estimate_stall_speed 

# python imports     
import sys
import matplotlib.pyplot as  plt


# local imports 
sys.path.append('../../Vehicles')
from Electric_Twin_Otter    import vehicle_setup, configs_setup 


# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------  
def main():           
         
    battery_types = ['lithium_ion_lfp', 'lithium_ion_nmc']
    btms_types   =  ['Liquid_Cooled_Wavy_Channel', 'Air_Cooled', None]
    # vehicle data
    for battery_type in  battery_types:
        for btms_type in  btms_types:
            vehicle  = vehicle_setup(battery_type, btms_type)

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
            plot_mission(results)

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
    weights = RCAIDE.Framework.Analyses.Weights.Weights_eVTOL()
    weights.vehicle = vehicle
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    
    # Calculate extra drag from landing gear: 
    main_wheel_width  = 4. * Units.inches
    main_wheel_height = 12. * Units.inches
    nose_gear_height  = 10. * Units.inches
    nose_gear_width   = 4. * Units.inches 
    total_wheel       = 2*main_wheel_width*main_wheel_height + nose_gear_width*nose_gear_height 
    main_gear_strut_height = 2. * Units.inches
    main_gear_strut_length = 24. * Units.inches
    nose_gear_strut_height = 12. * Units.inches
    nose_gear_strut_width  = 2. * Units.inches 
    total_strut = 2*main_gear_strut_height*main_gear_strut_length + nose_gear_strut_height*nose_gear_strut_width 
    drag_area = 1.4*( total_wheel + total_strut)
    
    
    aerodynamics = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method() 
    aerodynamics.geometry                            = vehicle
    aerodynamics.settings.drag_coefficient_increment = drag_area/vehicle.reference_area
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
    base_segment = Segments.Segment()
    base_segment.temperature_deviation  = 15
    # VSTALL Calculation  
    vehicle        = analyses.base.aerodynamics.geometry
    vehicle_mass   = vehicle.mass_properties.max_takeoff
    reference_area = vehicle.reference_area 
    Vstall         = estimate_stall_speed(vehicle_mass,reference_area,altitude = 0.0,maximum_lift_coefficient = 1.2)
    

    # ------------------------------------------------------------------
    #   Cruise Segment: constant Speed, constant altitude
    # ------------------------------------------------------------------ 
    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "Cruise" 
    segment.analyses.extend( analyses.base )  
    segment.altitude                                      = 5000   * Units.feet 
    segment.air_speed                                     = 130 * Units.kts
    segment.distance                                      = 20.   * Units.nautical_mile
    segment.initial_battery_state_of_charge               = 1.0  
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.body_angle.active             = True                  
          
    mission.append_segment(segment)    


   
    # ------------------------------------------------------------------
    #   Mission definition complete    
    # ------------------------------------------------------------------ 
    return mission


def missions_setup(mission): 
 
    missions         = RCAIDE.Framework.Mission.Missions()
    
    # base mission 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions

def plot_mission(results):
    
    
    plot_battery_cell_conditions(results)
    
    plot_thermal_management_component(results)

    plot_battery_degradation(results)
    
    return


if __name__ == '__main__': 
    main()    
    plt.show()
