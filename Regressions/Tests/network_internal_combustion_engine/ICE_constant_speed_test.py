# ICE_Test.py
# 
# Created: Feb 2020, M. Clarke 
 
""" setup file for a mission with a Cessna 172 with an internal combustion engine network
"""

# ----------------------------------------------------------------------
#   Imports
# ---------------------------------------------------------------------- 
import RCAIDE
from RCAIDE.Core import Data, Units 

# python imports 
import numpy as np   

# local imports 
import sys 
sys.path.append('../../Vehicles') 
from Cessna_172                       import vehicle_setup  
from RCAIDE.Methods.Energy.Propulsion.Converters.Rotor import design_propeller

# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main():   
     
    # Define internal combustion engine from Cessna Regression Aircraft 
    vehicle    = vehicle_setup()
    
    # Setup the modified constant speed version of the network
    vehicle = ICE_CS(vehicle) 
    configs = configs_setup(vehicle)
     
    # create analyses
    analyses = analyses_setup(configs)

    # mission analyses
    mission  = mission_setup(analyses) 

    # create mission instances (for multiple types of missions)
    missions = missions_setup(mission) 

    # mission analysis 
    results = missions.base_mission.evaluate()   
    
    P_truth     = 53595.133552791885
    mdot_truth  = 0.004708991132231039
    
    P    = results.segments.cruise.state.conditions.energy.fuel_line.ice_constant_speed_propeller.engine.power[-1,0]
    mdot = results.segments.cruise.state.conditions.weights.vehicle_mass_rate[-1,0]     

    # Check the errors
    error = Data()
    error.P      = np.max(np.abs((P     - P_truth)/P_truth))
    error.mdot   = np.max(np.abs((mdot - mdot_truth)/mdot_truth))


    print('Errors:')
    print(error)

    for k,v in list(error.items()):
        assert(np.abs(v)<1e-6)

    return


def ICE_CS(vehicle):
    
    # Replace the C172 engine and propeller with a constant speed propeller  
    vehicle.networks.pop('internal_combustion_engine')

    # ########################################################  Energy Network  #########################################################  
    net                                         = RCAIDE.Energy.Networks.Internal_Combustion_Engine_Constant_Speed()  

    #------------------------------------------------------------------------------------------------------------------------------------  
    # Bus
    #------------------------------------------------------------------------------------------------------------------------------------  
    fuel_line                                   = RCAIDE.Energy.Networks.Distribution.Fuel_Line() 
    
    #------------------------------------------------------------------------------------------------------------------------------------  
    # uel Tank and Fuel
    #------------------------------------------------------------------------------------------------------------------------------------   
    fuel_tank                                   = RCAIDE.Energy.Sources.Fuel_Tanks.Fuel_Tank()
    fuel_tank.origin                            = vehicle.wings.main_wing.origin  
    fuel                                        = RCAIDE.Attributes.Propellants.Aviation_Gasoline() 
    fuel.mass_properties.mass                   = 319 *Units.lbs 
    fuel.mass_properties.center_of_gravity      =  vehicle.wings.main_wing.mass_properties.center_of_gravity
    fuel.internal_volume                        = fuel.mass_properties.mass/fuel.density  
    fuel_tank.fuel                              = fuel  
    fuel_line.fuel_tanks.append(fuel_tank)


    #------------------------------------------------------------------------------------------------------------------------------------  
    # Propulsor
    #------------------------------------------------------------------------------------------------------------------------------------   
    propulsor                                  = RCAIDE.Energy.Propulsion.ICE_Constant_Speed_Propeller()
    propulsor.tag                              = 'ice_constant_speed_propeller'
    propulsor.active_fuel_tanks                = ['fuel_tank']
                                                   
    # Engine                     
    engine                                     = RCAIDE.Energy.Propulsion.Converters.Engine()
    engine.sea_level_power                     = 180. * Units.horsepower
    engine.flat_rate_altitude                  = 0.0
    engine.rated_speed                         = 2700. * Units.rpm
    engine.rated_power                         = 180.  * Units.hp   
    engine.power_specific_fuel_consumption     = 0.52 
    propulsor.engine                           = engine 
    
    # Prop  
    prop                                   = RCAIDE.Energy.Propulsion.Converters.Propeller()
    prop.number_of_blades                  = 2.0
    prop.variable_pitch                    = True 
    prop.tip_radius                        = 76./2. * Units.inches
    prop.hub_radius                        = 8.     * Units.inches
    prop.cruise.design_freestream_velocity = 119.   * Units.knots
    prop.cruise.design_angular_velocity    = 2650.  * Units.rpm
    prop.cruise.design_Cl                  = 0.8
    prop.cruise.design_altitude            = 12000. * Units.feet
    prop.cruise.design_power               = .64 * 180. * Units.horsepower 
    airfoil                                = RCAIDE.Components.Airfoils.Airfoil()   
    airfoil.coordinate_file                = '../../Vehicles/Airfoils/NACA_4412.txt'
    airfoil.polar_files                    = ['../../Vehicles/Airfoils/Polars/NACA_4412_polar_Re_50000.txt' ,
                                           '../../Vehicles/Airfoils/Polars/NACA_4412_polar_Re_100000.txt' ,
                                           '../../Vehicles/Airfoils/Polars/NACA_4412_polar_Re_200000.txt' ,
                                           '../../Vehicles/Airfoils/Polars/NACA_4412_polar_Re_500000.txt' ,
                                           '../../Vehicles/Airfoils/Polars/NACA_4412_polar_Re_1000000.txt' ] 
    prop.append_airfoil(airfoil)  
    prop.airfoil_polar_stations            = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    prop                                   = design_propeller(prop)   
    propulsor.propeller                    = prop
    
    fuel_line.propulsors.append(propulsor)
    net.fuel_lines.append(fuel_line) 
    
    # add the network to the vehicle
    vehicle.append_energy_network(net)
    
    
    return vehicle


def analyses_setup(configs):

    analyses = RCAIDE.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config)
        analyses[tag] = analysis

    return analyses

def missions_setup(mission):  
    missions         = RCAIDE.Analyses.Mission.Missions() 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions  

def configs_setup(vehicle):
     # ------------------------------------------------------------------
    #   Initialize Configurations
    # ------------------------------------------------------------------ 
    configs                                                    = RCAIDE.Components.Configs.Config.Container() 
    base_config                                                = RCAIDE.Components.Configs.Config(vehicle) 
    base_config.tag                                            = 'base'
    configs.append(base_config)
    
    # ------------------------------------------------------------------
    #   Cruise Configuration
    # ------------------------------------------------------------------ 
    cruise_config                                                     = RCAIDE.Components.Configs.Config(base_config)
    cruise_config.tag                                                 = 'cruise' 
    configs.append(cruise_config) 
    
    # done!
    return configs

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
    base_segment.state.numerics.number_control_points    = 3


    # ------------------------------------------------------------------    
    #   Cruise Segment: Constant Speed Constant Altitude
    # ------------------------------------------------------------------    

    segment        = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag    = "cruise"
    segment.analyses.extend( analyses.cruise) 
    segment.altitude                                      = 12000. * Units.feet
    segment.air_speed                                     = 119.   * Units.knots
    segment.distance                                      = 10 * Units.nautical_mile
    segment.state.conditions.energy.rpm                   = 2650. *  ones_row(1)
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.flight_controls.throttle.active               = True           
    segment.flight_controls.throttle.assigned_propulsors  = [['ice_constant_speed_propeller']] 
    segment.flight_controls.body_angle                   
    segment.flight_controls.body_angle.active             = True                
                
    mission.append_segment(segment)


    return mission



def base_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Analyses.Vehicle()
 
    # ------------------------------------------------------------------
    #  Weights
    weights = RCAIDE.Analyses.Weights.Weights_Transport()
    weights.vehicle = vehicle
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics = RCAIDE.Analyses.Aerodynamics.Subsonic_VLM() 
    aerodynamics.geometry                            = vehicle
    aerodynamics.settings.drag_coefficient_increment = 0.0000
    analyses.append(aerodynamics)

    # ------------------------------------------------------------------
    #  Energy
    energy= RCAIDE.Analyses.Energy.Energy()
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
#   Call Main
# ----------------------------------------------------------------------    

if __name__ == '__main__':
    main()
    