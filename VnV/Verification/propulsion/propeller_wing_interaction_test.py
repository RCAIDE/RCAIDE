
""" setup file for a cruise segment of the NASA X-57 Maxwell (Twin Engine Variant) Electric Aircraft
"""
# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
# RCAIDE Imports 
import RCAIDE
from RCAIDE.Framework.Core import Units , Data  
from RCAIDE.Library.Plots import *

# Python imports
import matplotlib.pyplot as plt  
import sys 
import os
import numpy as np     
import time

base_dir = os.path.dirname(os.path.abspath(__file__))

vehicles_path = os.path.abspath(
    os.path.join(base_dir, "..", "..", "Vehicles")
)

if vehicles_path not in sys.path:
    sys.path.insert(0, vehicles_path)
from NASA_X57    import vehicle_setup, configs_setup     
 
# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main():
    # fidelity zero wakes
    print('Wake Fidelity Zero, Identical Props')     
    Propeller_Slipstream(wake_fidelity=0,identical_props=False) 
    
    return


def Propeller_Slipstream(wake_fidelity,identical_props): 

    rotor_type = 'Blade_Element_Momentum_Theory_Helmholtz_Wake'
    vehicle  = vehicle_setup(rotor_type)      
 
    vehicle.networks.electric.propulsors.starboard_propulsor.rotor.clockwise_rotation = True
    vehicle.networks.electric.propulsors.port_propulsor.rotor.clockwise_rotation = False
     
    configs  = configs_setup(vehicle) 
    analyses = analyses_setup(configs)  
    mission  = mission_setup(analyses)
    missions = missions_setup(mission) 
    results  = missions.base_mission.evaluate()    
       
    # Regression for Stopped Rotor Test (using Fidelity Zero wake model)
    lift_coefficient            = results.segments.cruise.conditions.aerodynamics.coefficients.lift.total[1][0]
    sectional_lift_coeff        = results.segments.cruise.conditions.aerodynamics.coefficients.lift.spanwise[0]
    
    # lift coefficient and sectional lift coefficient check
    lift_coefficient_true       = 0.8475619380134876
    sectional_lift_coeff_true   = np.array([ 7.79540235e-01,  7.74635390e-01,  7.65789877e-01,  7.52705272e-01,
        7.33976652e-01,  7.05094945e-01,  6.32623240e-01,  6.14291408e-01,
        6.96260165e-01,  7.35342618e-01,  8.21564133e-01,  7.98283987e-01,
        7.38415844e-01,  7.16394134e-01,  7.00416325e-01,  6.86025539e-01,
        6.71607933e-01,  6.56340610e-01,  6.39712846e-01,  6.21379417e-01,
        6.01107239e-01,  5.78752533e-01,  5.54201625e-01,  5.27134407e-01,
        4.96243690e-01,  4.55730620e-01,  1.25276141e-01,  1.02169181e-01,
        1.03457870e-01,  9.07322071e-02,  7.79540379e-01,  7.74635819e-01,
        7.65790579e-01,  7.52705752e-01,  7.33976574e-01,  7.05094813e-01,
        6.32623440e-01,  6.14292255e-01,  6.96261710e-01,  7.35343747e-01,
        8.21563743e-01,  7.98281246e-01,  7.38409725e-01,  7.16384805e-01,
        7.00402940e-01,  6.86006803e-01,  6.71585075e-01,  6.56316589e-01,
        6.39688641e-01,  6.21353920e-01,  6.01081476e-01,  5.78731150e-01,
        5.54186369e-01,  5.27123227e-01,  4.96236471e-01,  4.55725595e-01,
        1.25274525e-01,  1.02167460e-01,  1.03455966e-01,  9.07304058e-02,
        1.82603047e-02,  1.83940965e-02,  1.86580686e-02,  1.90452143e-02,
        1.95452646e-02,  2.01449658e-02,  2.08281606e-02,  2.15759743e-02,
        2.23668863e-02,  2.31765500e-02,  2.39778766e-02,  2.47410961e-02,
        2.54339715e-02,  2.60223011e-02,  2.64706057e-02,  2.67432638e-02,
        2.68058871e-02,  2.66269296e-02,  2.61795539e-02,  2.54430965e-02,
        2.44044321e-02,  2.30591862e-02,  2.14120414e-02,  1.94767052e-02,
        1.72753831e-02,  1.48380916e-02,  1.22024208e-02,  9.41481558e-03,
        6.54149069e-03,  3.79947103e-03,  1.82602481e-02,  1.83939275e-02,
        1.86577836e-02,  1.90448236e-02,  1.95447912e-02,  2.01444133e-02,
        2.08275437e-02,  2.15753426e-02,  2.23662312e-02,  2.31758468e-02,
        2.39771441e-02,  2.47403764e-02,  2.54333030e-02,  2.60217068e-02,
        2.64700803e-02,  2.67428167e-02,  2.68055333e-02,  2.66267155e-02,
        2.61794635e-02,  2.54430048e-02,  2.44043075e-02,  2.30590810e-02,
        2.14119831e-02,  1.94767208e-02,  1.72755090e-02,  1.48384075e-02,
        1.22029763e-02,  9.41542896e-03,  6.54181162e-03,  3.79925462e-03,
       -7.19200652e-15, -1.05601771e-14, -1.30709575e-14, -1.63913110e-14,
       -4.51076845e-17,  1.92452888e-15,  3.38627842e-15,  3.82315055e-15,
        3.76654883e-15,  3.36121663e-15,  2.53218680e-15,  1.46912278e-15,
        3.06192923e-16, -8.32204767e-16, -1.65468515e-15, -2.53526160e-15,
       -3.24401472e-15, -3.93806838e-15, -4.59454251e-15, -5.00058046e-15,
       -5.23691742e-15, -5.33593173e-15, -5.23249389e-15, -4.93938833e-15,
       -4.58643850e-15, -4.13884827e-15, -3.50707671e-15, -2.74586205e-15,
       -1.94400215e-15, -1.14256969e-15])

    diff_CL = np.abs(lift_coefficient  - lift_coefficient_true) / lift_coefficient_true
    print('CL difference')
    print(diff_CL)

    diff_Cl_y   = max(np.abs(sectional_lift_coeff - sectional_lift_coeff_true) / sectional_lift_coeff_true)
    print('Cl difference')
    print(diff_Cl_y)
    
    assert diff_CL< 1e-6
    assert diff_Cl_y < 1e-6

    # plot results, vehicle, and vortex distribution
    plot_mission(results) 
              
    return
 

def plot_mission(results):
    
    # Plot lift distribution
    plot_lift_distribution(results) 
    return 
 
# ----------------------------------------------------------------------
#   Define the Vehicle Analyses
# ---------------------------------------------------------------------- 
def analyses_setup(configs):

    analyses = RCAIDE.Framework.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis      = base_analysis(config) 
        analyses[tag] = analysis

    return analyses  


def base_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Framework.Analyses.Vehicle()
    analyses.vehicle =  vehicle

    # ------------------------------------------------------------------     
    #  Weights
    weights = RCAIDE.Framework.Analyses.Weights.Electric_General_Aviation()
    analyses.append(weights)  

    # ------------------------------------------------------------------     
    #  Geometry
    geometry = RCAIDE.Framework.Analyses.Geometry.Geometry()
    analyses.append(geometry)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics                               = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method()  
    aerodynamics.settings.use_surrogate        = False 
    aerodynamics.settings.propeller_wake_model = True
    analyses.append(aerodynamics)   
  

    # ------------------------------------------------------------------
    #  Energy
    energy          = RCAIDE.Framework.Analyses.Energy.Energy() 
    analyses.append(energy)

    # ------------------------------------------------------------------
    #  Planet Analysis
    planet = RCAIDE.Framework.Analyses.Planets.Earth()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    analyses.append(atmosphere)   

    # done!
    return analyses    

# ----------------------------------------------------------------------
#  Set Up Mission 
# ---------------------------------------------------------------------- 
def mission_setup(analyses):
    

    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------ 
 
    mission = RCAIDE.Framework.Mission.Sequential_Segments()
    mission.tag = 'mission'
  
    # unpack Segments module
    Segments = RCAIDE.Framework.Mission.Segments

    #   Cruise Segment: constant Speed, constant altitude 
    segment                           = Segments.Untrimmed.Untrimmed()
    segment.analyses.extend( analyses.base ) 
    segment.tag = "cruise"    
    segment.initial_battery_state_of_charge              = 1.0       
    segment.altitude                                     = 30
    segment.air_speed                                    = 100
    segment.distance                                     = 1 * Units.miles
    segment.angle_of_attack                              = 3 *  Units.degrees
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.body_angle.active             = True                
       
    mission.append_segment(segment)      
     
    return mission

# ----------------------------------------------------------------------
#  Set Up Missions 
# ---------------------------------------------------------------------- 
def missions_setup(mission): 
 
    missions     = RCAIDE.Framework.Mission.Missions() 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions  
 

if __name__ == '__main__':
    main()
    plt.show()
