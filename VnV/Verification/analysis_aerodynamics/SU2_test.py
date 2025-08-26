# SU2_test.py
# 
# Created:  Aug 2025, M. Clarke

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE
from RCAIDE.Framework.Core import Units ,  Data
from RCAIDE.Library.Plots             import *       

# python imports 
import numpy as np
import pylab as plt 
import sys
import os

# local imports 
sys.path.append(os.path.join( os.path.split(os.path.split(sys.path[0])[0])[0], 'Vehicles'))
from Boeing_737    import vehicle_setup as vehicle_setup
from Boeing_737    import configs_setup as configs_setup 

# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main():
    new_regression             = True # should be false
    gmsh_installation          = False 
    vsp_installation           = False 
    SU2_installation           = False
    generate_new_training_data = False

    try: 
        import gmsh as gmsh
        gmsh_installation = True   
    except:
        pass

    try:  
        import vsp as vsp
        vsp_installation  = True 
    except:
        pass 

    try:  
        import SU2_CFD as SU2_CFD
        SU2_installation =  False
    except:
        pass
    
    
    # if new regression and all flags are true, run SU2
    if new_regression:
        if (gmsh_installation == False) or (vsp_installation  == False) or (SU2_installation  == False):
            raise AssertionError('Required packages are not installed to run regression')
        generate_new_training_data = True 
    else:
        generate_new_training_data = False
    
    # vehicle data
    vehicle  = vehicle_setup()  
    
    # Set up vehicle configs
    configs  = configs_setup(vehicle)

    # create analyses
    analyses = analyses_setup(configs,generate_new_training_data)

    # mission analyses 
    mission = mission_setup(analyses)
    
    # create mission instances (for multiple types of missions)
    missions = missions_setup(mission) 
     
    # mission analysis 
    results = missions.base_mission.evaluate()   
 
    # Extract sample values from computation   
    climb_CL        = results.segments.climb.conditions.aerodynamics.coefficients.lift.total[2][0]
    cruise_CL       = results.segments.cruise.conditions.aerodynamics.coefficients.lift.total[2][0] 
    
    #print values for resetting regression
    show_vals = True
    if show_vals:
        data = [climb_CL, cruise_CL]
        for val in data:
            print(val)
    
    # Truth values 
    climb_CL_truth        = 0 # UPDATE 
    cruise_CL_truth       = 0 # UPDATE 
    
    # Store errors 
    error = Data() 
    error.climb_CL        = np.max((np.abs(climb_CL          - climb_CL_truth ))/climb_CL_truth)
    error.cruise_1        = np.max((np.abs(cruise_CL          - cruise_CL_truth ))/cruise_CL_truth)       
     
    print('Errors:')
    print(error)
     
    for k,v in list(error.items()): 
        assert(np.abs(v)<1e-6)
        
    return 
# ----------------------------------------------------------------------
#   Define the Vehicle Analyses
# ----------------------------------------------------------------------

def analyses_setup(configs, generate_new_training_data):

    analyses = RCAIDE.Framework.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in list(configs.items()):
        analysis = base_analysis(config,generate_new_training_data)
        analyses[tag] = analysis
 
    return analyses


def base_analysis(vehicle, generate_new_training_data):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Framework.Analyses.Vehicle() 
    
    # ------------------------------------------------------------------
    #  geometry
    geometry = RCAIDE.Framework.Analyses.Geometry.Geometry()
    geometry.vehicle = vehicle 
    analyses.append(geometry)

    # ------------------------------------------------------------------
    #  Weights
    weights                                          = RCAIDE.Framework.Analyses.Weights.Conventional_Transport() 
    weights.vehicle                                  = vehicle
    analyses.append(weights)
 
    #  Aerodynamics Analysis
    aerodynamics                                        = RCAIDE.Framework.Analyses.Aerodynamics.SU2_Euler()
    aerodynamics.vehicle                                = vehicle
    # NEED TO ADD CODE TO USE OLD TRAINING DATA
    # aerodynamics.settings.generate_new_training_data (maybe a name change)
    analyses.append(aerodynamics)
  
    #  Energy
    energy                                           = RCAIDE.Framework.Analyses.Energy.Energy()
    energy.vehicle                                   = vehicle 
    analyses.append(energy)
 
    #  Planet Analysis
    planet                                           = RCAIDE.Framework.Analyses.Planets.Earth()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere                                       = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
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

    mission = RCAIDE.Framework.Mission.Sequential_Segments()
    mission.tag = 'the_mission'
  
    Segments = RCAIDE.Framework.Mission.Segments 
    base_segment = Segments.Segment()
    base_segment.state.numerics.number_of_control_points = 4  
  
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    #   Climb : Constant Speed Linear Altitude 
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    segment = Segments.Climb.Constant_Speed_Linear_Altitude(base_segment)
    segment.tag = "climb"
    segment.analyses.extend( analyses.base )  
    segment.altitude_start                                           = 3.    * Units.km   
    segment.altitude_end                                             = 7.    * Units.km   
    segment.air_speed                                                = 250.2 * Units.m / Units.s 
                 
    # define flight dynamics to model              
    segment.flight_dynamics.force_x                                  = True  
    segment.flight_dynamics.force_z                                  = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['propulsor_1','propulsor_2']] 
    segment.assigned_control_variables.body_angle.active             = True                
    mission.append_segment(segment)
    
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    #   Cruise Segment: constant Speed, constant altitude
    # ------------------------------------------------------------------------------------------------------------------------------------ 
    segment = Segments.Cruise.Constant_Mach_Constant_Altitude(base_segment)
    segment.tag = "cruise" 
    segment.analyses.extend(analyses.base) 
    segment.altitude                                                 = 36000 * Units.feet 
    segment.mach_number                                              = 0.85 * Units.feet 
    segment.distance                                                 = 500 * Units.km  
               
    # define flight dynamics to model            
    segment.flight_dynamics.force_x                                  = True  
    segment.flight_dynamics.force_z                                  = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['propulsor_1','propulsor_2']] 
    segment.assigned_control_variables.body_angle.active             = True                
    
    mission.append_segment(segment)     
     
 
    return mission


def missions_setup(mission): 
 
    missions     = RCAIDE.Framework.Mission.Missions() 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions  


if __name__ == '__main__': 
    main()    
