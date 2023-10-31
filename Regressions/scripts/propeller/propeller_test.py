# propeller_test.py
# 
# Created:  Sep 2014, E. Botero
# Modified: Feb 2020, M. Clarke  
#           Sep 2020, M. Clarke 
#           Oct 2023, Racheal M. Erhard

#----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import Legacy.trunk.S as SUAVE
from Legacy.trunk.S.Core import Units
from RCAIDE.Visualization.Geometry.plot_propeller import plot_propeller
import matplotlib.pyplot as plt  
from Legacy.trunk.S.Core import (
Data, Container,
)

import numpy as np
import copy, time
from RCAIDE.Methods.Propulsion import propeller_design
from RCAIDE.Analyses.Aerodynamics.Airfoils.Airfoil import Airfoil as Airfoil_Analysis
from Legacy.trunk.S.Components.Energy.Networks.Battery_Propeller import Battery_Propeller
import os
import RCAIDE


def main():
    
    # This script could fail if either the design or analysis scripts fail,
    # in case of failure check both. The design and analysis powers will 
    # differ because of karman-tsien compressibility corrections in the 
    # analysis scripts

    # ------------------------------------------------------------------------------------------    
    # Set up a few airfoils for use in the following rotor tests
    #    Define airfoil using generated naca 4 series for geometry and polars in the indicated directory    
    airfoil_0 = RCAIDE.Components.Airfoils.Airfoil()  
    airfoil_0.airfoil_directory = os.path.abspath('../Vehicles/Airfoils/NACA_4412')
    airfoil_0.settings.NACA_4_series_flag   = True
    airfoil_0.settings.NACA_4_series_digits ='4412'
    
    #    Define airfoil using provided coordinate file and polars in the indicated directory
    airfoil_1 = RCAIDE.Components.Airfoils.Airfoil()
    airfoil_1.tag = 'NACA_4412' 
    airfoil_1.airfoil_directory = os.path.abspath('../Vehicles/Airfoils/NACA_4412')
    airfoil_1.coordinate_file = 'NACA_4412.txt'
    
    #    Define airfoil using provided coordinate file and polars in the indicated directory
    airfoil_2 = RCAIDE.Components.Airfoils.Airfoil()  
    airfoil_2.tag = 'Clark_Y' 
    airfoil_2.airfoil_directory = os.path.abspath('../Vehicles/Airfoils/Clark_y')
    airfoil_2.coordinate_file = 'Clark_y.txt'
    
    # ------------------------------------------------------------------------------------------    
    net                       = Battery_Propeller()   
    net.number_of_propeller_engines     = 2    

    # ------------------------------------------------------------------------------------------    
    # Design Gearbox 
    gearbox                   = SUAVE.Components.Energy.Converters.Gearbox()
    gearbox.gearwheel_radius1 = 1
    gearbox.gearwheel_radius2 = 1
    gearbox.efficiency        = 0.95
    gearbox.inputs.torque     = 885.550158704757
    gearbox.inputs.speed      = 207.16160479940007
    gearbox.inputs.power      = 183451.9920076409
    gearbox.compute()
    
    conditions, conditions_r = set_conditions()

    # ------------------------------------------------------------------------------------------        
    test_bad_prop(gearbox, airfoil_0, conditions)

    # ------------------------------------------------------------------------------------------    
    prop_a, F_a, Q_a, P_a, Cplast_a ,output_a , etap_a = test_prop_a(gearbox, airfoil_1, airfoil_2, conditions)

    # ------------------------------------------------------------------------------------------ 
    prop, F, Q, P, Cplast, output , etap = test_prop(gearbox, conditions)

    # ------------------------------------------------------------------------------------------
    rot_a, Fr_a, Qr_a, Pr_a, Cplastr_a ,outputr_a , etapr = test_rot_a(gearbox, airfoil_0, conditions_r)

    # ------------------------------------------------------------------------------------------    
    rot, Fr, Qr, Pr, Cplastr ,outputr , etapr = test_rot(gearbox, conditions_r)

    # ------------------------------------------------------------------------------------------    

    
    # propeller with airfoil results 
    plot_results(output_a, prop_a,'blue','-','s')
    
    # propeller without airfoil results 
    plot_results(output, prop,'red','-','o')
    
    # rotor with airfoil results 
    plot_results(outputr_a, rot_a,'green','-','^')
    
    # rotor with out airfoil results 
    plot_results(outputr, rot,'black','-','P')
    
    # Truth values for propeller with airfoil geometry defined 
    F_a_truth       = 3367.1596921441087
    Q_a_truth       = 927.6570322
    P_a_truth       = 192174.91949376
    Cplast_a_truth  = 0.09905162
    
    # Truth values for propeller without airfoil geometry defined 
    F_truth         = 3760.214425042781
    Q_truth         = 955.96244497
    P_truth         = 198038.71422859
    Cplast_truth    = 0.10207396
     
    # Truth values for rotor with airfoil geometry defined 
    Fr_a_truth      = 1499.405768350158
    Qr_a_truth      = 143.08485231
    Pr_a_truth      = 29641.68762631
    Cplastr_a_truth = 0.0466249
    
    # Truth values for rotor without airfoil geometry defined 
    Fr_truth        = 1395.052125288473
    Qr_truth        = 86.67457412
    Pr_truth        = 17955.64386962
    Cplastr_truth   = 0.02824333
    
    # Store errors 
    error = Data()
    error.Thrust_a  = np.max(np.abs(np.linalg.norm(F_a) -F_a_truth))
    error.Torque_a  = np.max(np.abs(Q_a -Q_a_truth))    
    error.Power_a   = np.max(np.abs(P_a -P_a_truth))
    error.Cp_a      = np.max(np.abs(Cplast_a -Cplast_a_truth))  
    
    error.Thrust    = np.max(np.abs(np.linalg.norm(F)-F_truth))
    error.Torque    = np.max(np.abs(Q-Q_truth))    
    error.Power     = np.max(np.abs(P-P_truth))
    error.Cp        = np.max(np.abs(Cplast-Cplast_truth))  
    
    error.Thrustr_a = np.max(np.abs(np.linalg.norm(Fr_a)-Fr_a_truth))
    error.Torquer_a = np.max(np.abs(Qr_a-Qr_a_truth))    
    error.Powerr_a  = np.max(np.abs(Pr_a-Pr_a_truth))
    error.Cpr_a     = np.max(np.abs(Cplastr_a-Cplastr_a_truth))  
    
    error.Thrustr   = np.max(np.abs(np.linalg.norm(Fr)-Fr_truth))
    error.Torquer   = np.max(np.abs(Qr-Qr_truth))    
    error.Powerr    = np.max(np.abs(Pr-Pr_truth))
    error.Cpr       = np.max(np.abs(Cplastr-Cplastr_truth))     
    
    print('Errors:')
    print(error)
    
    for k,v in list(error.items()):
        assert(np.abs(v)<1e-6)

    return


def test_bad_prop(gearbox, airfoil_0, conditions):
    # ------------------------------------------------------------------------------------------
    # Design the Propeller with airfoil  geometry defined                      
    bad_prop                          = RCAIDE.Energy.Converters.Propeller() 
    bad_prop.tag                      = "Prop_W_Aifoil"
    bad_prop.number_of_blades         = 2
    bad_prop.number_of_engines        = 1
    bad_prop.freestream_velocity      = 1
    bad_prop.tip_radius               = 0.3
    bad_prop.hub_radius               = 0.21336 
    bad_prop.design_tip_mach          = 0.1
    bad_prop.angular_velocity         = gearbox.inputs.speed  
    bad_prop.design_Cl                = 0.7
    bad_prop.design_altitude          = 1. * Units.km
    bad_prop.design_thrust            = 100000
    
    bad_prop.append_airfoil_component(airfoil_0)
    bad_prop.airfoil_polar_stations   =  [0] * 20

    # Set the airfoil analysis methods
    bad_prop.finalize(Airfoil_Analysis())
    
    bad_prop = propeller_design(bad_prop)
    

    # Set condition
    bad_prop.inputs.omega     = np.array(gearbox.inputs.speed, ndmin=2)    
    
    return

def test_prop_a(gearbox, airfoil_1, airfoil_2, conditions):
    prop_a                            = RCAIDE.Energy.Converters.Propeller()
    prop_a.tag                        = "Prop_W_Aifoil"
    prop_a.number_of_blades           = 3
    prop_a.number_of_engines          = 1
    prop_a.freestream_velocity        = 49.1744
    prop_a.tip_radius                 = 1.0668
    prop_a.hub_radius                 = 0.21336
    prop_a.design_tip_mach            = 0.65
    prop_a.angular_velocity           = gearbox.inputs.speed
    prop_a.design_Cl                  = 0.7
    prop_a.design_altitude            = 1. * Units.km 
    prop_a.design_thrust             = 3054.4809132125697
    
    # Append airfoil components to this rotor
    prop_a.append_airfoil_component(airfoil_1)   # append first airfoil 
    prop_a.append_airfoil_component(airfoil_2)   # append second airfoil 
    
    
    # define polar stations on rotor 
    prop_a.airfoil_polar_stations = [0] * 13 + [1] * 7

    prop_a.finalize(Airfoil_Analysis())
    
    prop_a = propeller_design(prop_a)
    
    # plot propeller 
    plot_propeller(prop_a)    
    
    # Set conditions and spin
    prop_a.inputs.omega     = np.array(gearbox.inputs.speed, ndmin=2)      
    prop_a.inputs.pitch_command                = 0.0*Units.degree
    F_a, Q_a, P_a, Cplast_a ,output_a , etap_a = prop_a.spin(conditions) 
    
    return prop_a, F_a, Q_a, P_a, Cplast_a ,output_a , etap_a

def test_prop(gearbox, conditions):
    # Design the Propeller with airfoil  geometry defined 
    prop                           = RCAIDE.Energy.Converters.Propeller()
    prop.tag                       = "Prop_No_Aifoil"
    prop.number_of_blades          = 3
    prop.number_of_engines         = 1
    prop.freestream_velocity       = 49.1744
    prop.tip_radius                = 1.0668
    prop.hub_radius                = 0.21336
    prop.design_tip_mach           = 0.65
    prop.angular_velocity          = gearbox.inputs.speed
    prop.design_Cl                 = 0.7
    prop.design_altitude           = 1. * Units.km
    prop.origin                    = [[16.*0.3048 , 0. ,2.02*0.3048 ]]
    prop.design_power              = gearbox.outputs.power
    

    prop.finalize(Airfoil_Analysis())
    prop                           = propeller_design(prop)
    

    # Set condition
    prop.inputs.omega     = np.array(gearbox.inputs.speed, ndmin=2)    
    prop.inputs.pitch_command           = 0.0*Units.degree
    F, Q, P, Cplast ,output , etap      = prop.spin(conditions)    
    return prop, F, Q, P, Cplast ,output , etap

def test_rot_a(gearbox, airfoil_0, conditions_r):
    # Design a Rotor with airfoil  geometry defined  
    rot_a                          = RCAIDE.Energy.Converters.Rotor() 
    rot_a.tag                      = "Rot_W_Aifoil"
    rot_a.tip_radius               = 2.8 * Units.feet
    rot_a.hub_radius               = 0.35 * Units.feet      
    rot_a.number_of_blades         = 2   
    rot_a.design_tip_mach          = 0.65
    rot_a.number_of_engines        = 12
    rot_a.disc_area                = np.pi*(rot_a.tip_radius**2)   
    rot_a.freestream_velocity      = 500. * Units['ft/min']  
    rot_a.angular_velocity         = 258.9520059992501
    rot_a.design_Cl                = 0.7
    rot_a.design_altitude          = 20 * Units.feet                            
    rot_a.design_thrust            = 2271.2220451593753  

    rot_a.append_airfoil_component(airfoil_0)   
    rot_a.airfoil_polar_stations   = [0] * 20
    rot_a.finalize(Airfoil_Analysis())
    rot_a = propeller_design(rot_a) 
    

    # Set condition
    rot_a.inputs.omega     = np.array(gearbox.inputs.speed, ndmin=2)       
    rot_a.inputs.pitch_command                     = 0.0*Units.degree
    Fr_a, Qr_a, Pr_a, Cplastr_a ,outputr_a , etapr = rot_a.spin(conditions_r) 
    return rot_a, Fr_a, Qr_a, Pr_a, Cplastr_a ,outputr_a , etapr

def test_rot(gearbox, conditions_r):
    # Design a Rotor without airfoil geometry defined 
    rot                            = RCAIDE.Energy.Converters.Rotor()
    rot.tag                        = "Rot_No_Aifoil"
    rot.tip_radius                 = 2.8 * Units.feet
    rot.hub_radius                 = 0.35 * Units.feet
    rot.number_of_blades           = 2
    rot.design_tip_mach            = 0.65
    rot.number_of_engines          = 12
    rot.disc_area                  = np.pi*(rot.tip_radius**2)
    rot.freestream_velocity        = 500. * Units['ft/min']
    rot.angular_velocity           = 258.9520059992501
    rot.design_Cl                  = 0.7
    rot.design_altitude            = 20 * Units.feet
    rot.design_thrust              = 2271.2220451593753
    rot.finalize(Airfoil_Analysis())
    rot                            = propeller_design(rot)
    

    # Set condition
    rot.inputs.omega     = np.array(gearbox.inputs.speed, ndmin=2)  
    rot.inputs.pitch_command              = 0.0*Units.degree
    Fr, Qr, Pr, Cplastr ,outputr , etapr  = rot.spin(conditions_r)      
    return rot, Fr, Qr, Pr, Cplastr ,outputr , etapr


def set_conditions():
    # Set the operating conditions
    atmosphere                     = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    atmosphere_conditions          = atmosphere.compute_values(20 * Units.feet)
    
    V = 49.1744
    Vr = 500. * Units['ft/min']
    
    conditions                                          = SUAVE.Analyses.Mission.Segments.Conditions.Aerodynamics()
    conditions._size                                    = 1
    #conditions.freestream                               = Data()
    #conditions.propulsion                               = Data()
    #conditions.frames                                   = Data()
    #conditions.frames.body                              = Data()
    #conditions.frames.inertial                          = Data()
    conditions.freestream.update(atmosphere_conditions)
    conditions.freestream.dynamic_viscosity             = atmosphere_conditions.dynamic_viscosity
    conditions.frames.inertial.velocity_vector          = np.array([[V,0,0]])
    conditions.propulsion.throttle                      = np.array([[1.0]])
    conditions.frames.body.transform_to_inertial        = np.array([np.eye(3)])
    
    conditions_r = copy.deepcopy(conditions)
    conditions.frames.inertial.velocity_vector   = np.array([[V,0,0]])
    conditions_r.frames.inertial.velocity_vector = np.array([[0,Vr,0]])
    
    return conditions, conditions_r


def plot_results(results,prop,c,ls,m):
    
    tag                = prop.tag
    va_ind             = results.blade_axial_induced_velocity[0]  
    vt_ind             = results.blade_tangential_induced_velocity[0]  
    r                  = prop.radius_distribution
    T_distribution     = results.blade_thrust_distribution[0] 
    vt                 = results.blade_tangential_velocity[0]  
    va                 = results.blade_axial_velocity[0] 
    Q_distribution     = results.blade_torque_distribution[0] 
        
    # ----------------------------------------------------------------------------
    # 2D - Plots  Plots    
    # ---------------------------------------------------------------------------- 
    # perpendicular velocity, up Plot 
    fig = plt.figure('va_ind')         
    plt.plot(r  , va_ind ,color = c  , marker = m, linestyle = ls , label =  tag)          
    plt.xlabel('Radial Location')
    plt.ylabel('Induced Axial Velocity') 
    plt.legend(loc='lower right') 
    
    fig = plt.figure('vt_ind')          
    plt.plot(r  , vt_ind ,color = c ,marker = m, linestyle = ls , label =  tag )       
    plt.xlabel('Radial Location')
    plt.ylabel('Induced Tangential Velocity') 
    plt.legend(loc='lower right')  
        
    fig = plt.figure('T')     
    plt.plot(r , T_distribution ,color = c ,marker = m, linestyle = ls, label =  tag  )    
    plt.xlabel('Radial Location')
    plt.ylabel('Thrust, N')
    plt.legend(loc='lower right')
    
    fig = plt.figure('Q')
    plt.plot(r , Q_distribution ,color = c ,marker = m, linestyle = ls, label =  tag)            
    plt.xlabel('Radial Location')
    plt.ylabel('Torque, N-m')
    plt.legend(loc='lower right')
    
    fig = plt.figure('Va')     
    plt.plot(r , va ,color = c  ,marker =m, linestyle = ls, label =  tag + 'axial vel')          
    plt.xlabel('Radial Location')
    plt.ylabel('Axial Velocity') 
    plt.legend(loc='lower right') 
    
    fig = plt.figure('Vt')       
    plt.plot(r , vt ,color = c ,marker = m, linestyle = ls, label =  tag )         
    plt.xlabel('Radial Location')
    plt.ylabel('Tangential Velocity') 
    plt.legend(loc='lower right')  
    
    return 

# ----------------------------------------------------------------------        
#   Call Main
# ----------------------------------------------------------------------    

if __name__ == '__main__':
    main()
    plt.show()