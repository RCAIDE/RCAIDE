
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

sys.path.append(os.path.join( os.path.split(os.path.split(sys.path[0])[0])[0], 'Vehicles'))
from NASA_X57    import vehicle_setup, configs_setup     
 
# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main():
    # fidelity zero wakes
    print('Wake Fidelity Zero, Identical Props')    
    t0=time.time()
    Propeller_Slipstream(wake_fidelity=0,identical_props=True)
    print((time.time()-t0)/60) 
    
    return


def Propeller_Slipstream(wake_fidelity,identical_props): 

    rotor_type = 'Blade_Element_Momentum_Theory_Helmholtz_Wake'
    vehicle  = vehicle_setup(rotor_type)      

    for network in vehicle.networks: 
        network.identical_propulsors  = identical_props
        for propulsor in network.propulsors:
            propeller = propulsor.rotor 
            propeller.rotation = -1 
                
    
    configs  = configs_setup(vehicle) 
    analyses = analyses_setup(configs)  
    mission  = mission_setup(analyses)
    missions = missions_setup(mission) 
    results  = missions.base_mission.evaluate()    
       
    # Regression for Stopped Rotor Test (using Fidelity Zero wake model)
    lift_coefficient            = results.segments.cruise.conditions.aerodynamics.coefficients.lift.total[1][0]
    sectional_lift_coeff        = results.segments.cruise.conditions.aerodynamics.coefficients.lift.inviscid.spanwise[0]
    
    # lift coefficient and sectional lift coefficient check
    lift_coefficient_true       = 0.8138843131816682
    sectional_lift_coeff_true   = np.array([ 7.65787870e-01,  7.76916729e-01,  7.99378634e-01,  9.18119053e-01,
                                             7.29035970e-01,  6.40946887e-01,  6.54955932e-01,  6.41833800e-01,
                                             6.20656243e-01,  5.91983396e-01,  5.54772222e-01,  5.06943288e-01,
                                             4.38351745e-01,  9.30606888e-02,  1.05055686e-01,  7.48560347e-01,
                                             7.18180603e-01,  6.68139261e-01,  5.35673848e-01,  6.32004194e-01,
                                             6.80363288e-01,  6.36324156e-01,  6.22830306e-01,  6.04129042e-01,
                                             5.77920516e-01,  5.42820617e-01,  4.96779897e-01,  4.29888014e-01,
                                             9.11033066e-02,  1.02715098e-01,  2.35242716e-02,  2.10849937e-02,
                                             1.86284088e-02,  1.58879451e-02,  1.27526047e-02,  9.26612707e-03,
                                             5.58415010e-03,  1.96046827e-03, -1.28762850e-03, -3.84314515e-03,
                                            -5.45801916e-03, -6.01193111e-03, -5.54570839e-03, -4.26055313e-03,
                                            -2.56599057e-03,  2.60275374e-02,  2.83211639e-02,  3.04542822e-02,
                                             3.25999080e-02,  3.47284147e-02,  3.66760893e-02,  3.82181209e-02,
                                             3.90620296e-02,  3.88792800e-02,  3.73844559e-02,  3.44005642e-02,
                                             2.98995060e-02,  2.40265924e-02,  1.71236162e-02,  1.00422100e-02,
                                             8.97363824e-07,  1.97643216e-06,  2.20482584e-06,  2.99888546e-06,
                                             4.02069727e-06,  4.95471519e-06,  5.66530010e-06,  6.10526146e-06,
                                             6.26108514e-06,  6.12214969e-06,  5.66078069e-06,  4.81946345e-06,
                                             3.54208736e-06,  1.97742880e-06,  7.08249333e-07])

    diff_CL = np.abs(lift_coefficient  - lift_coefficient_true)
    print('CL difference')
    print(diff_CL)

    diff_Cl   = np.abs(sectional_lift_coeff - sectional_lift_coeff_true)
    print('Cl difference')
    print(diff_Cl)
    
    assert np.abs(lift_coefficient  - lift_coefficient_true) < 1e-2
    assert  np.max(np.abs(sectional_lift_coeff - sectional_lift_coeff_true)) < 1e-2

    # plot results, vehicle, and vortex distribution
    plot_mission(results)
    plot_3d_vehicle_vlm_panelization(vehicle,
                                     show_figure= False,
                                     save_figure=False,
                                     show_wing_control_points=True)
              
    return
 

def plot_mission(results):

    # Plot surface pressure coefficient
    plot_surface_pressures(results)

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

    # ------------------------------------------------------------------     
    #  Geometry
    geometry = RCAIDE.Framework.Analyses.Geometry.Geometry()
    geometry.vehicle = vehicle
    geometry.settings.overwrite_reference        = True
    geometry.settings.update_wing_properties     = True
    analyses.append(geometry)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics                               = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method() 
    aerodynamics.vehicle                       = vehicle
    aerodynamics.settings.use_surrogate        = False 
    aerodynamics.settings.propeller_wake_model = True
    analyses.append(aerodynamics)   
  

    # ------------------------------------------------------------------
    #  Energy
    energy          = RCAIDE.Framework.Analyses.Energy.Energy()
    energy.vehicle  = vehicle 
    analyses.append(energy)

    # ------------------------------------------------------------------
    #  Planet Analysis
    planet = RCAIDE.Framework.Analyses.Planets.Earth()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
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
