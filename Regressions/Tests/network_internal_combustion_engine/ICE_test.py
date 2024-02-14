# Regression/scripts/Tests/network_internal_combustion_engine/internal_combustion_engine_test.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE
from RCAIDE.Core import Units ,Data 

# python imports     
import numpy as np  
import sys 

sys.path.append('../../Vehicles')
# the analysis functions 
 
from Cessna_172  import vehicle_setup ,configs_setup


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
    
    # evaluate
    results     = mission.evaluate()  
    P_truth     = 53537.3966546438
    mdot_truth  = 0.004703918236179497
    
    P    = results.segments.cruise.state.conditions.energy.fuel_line.propulsor.engine.power[-1,0]
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


# ----------------------------------------------------------------------
#   Define the Mission
# ----------------------------------------------------------------------

def mission_setup(analyses):

    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------

    mission = RCAIDE.Analyses.Mission.Sequential_Segments()
    mission.tag = 'the_mission'
 

    # unpack Segments module
    Segments = RCAIDE.Analyses.Mission.Segments

    # base segment
    base_segment = Segments.Segment()
    


    # ------------------------------------------------------------------    
    #   Cruise Segment: Constant Speed Constant Altitude
    # ------------------------------------------------------------------    

    segment     = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise" 
    segment.analyses.extend( analyses.base ) 
    segment.altitude                                = 12000. * Units.feet
    segment.air_speed                               = 119.   * Units.knots
    segment.distance                                = 10 * Units.nautical_mile  
    segment.state.numerics.number_control_points    = 4   
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                       = True  
    segment.flight_dynamics.force_z                       = True     
    
    # define flight controls 
    segment.flight_controls.RPM.active                    = True           
    segment.flight_controls.RPM.assigned_propulsors       = [['ice_propeller']]
    segment.flight_controls.RPM.initial_values            = [[2500*Units.rpm]]
    segment.flight_controls.body_angle                   
    segment.flight_controls.body_angle.active             = True               
    segment.flight_controls.body_angle.initial_values     = [[3*Units.degrees]]    
    
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


def analyses_setup(configs):

    analyses = RCAIDE.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config)
        analyses[tag] = analysis

    return analyses

def missions_setup(mission): 
 
    missions         = RCAIDE.Analyses.Mission.Missions()
    
    # base mission 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions  

# ----------------------------------------------------------------------        
#   Call Main
# ----------------------------------------------------------------------    

if __name__ == '__main__':
    main()
    