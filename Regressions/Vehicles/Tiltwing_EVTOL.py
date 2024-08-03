''' 
# Tiltwing_EVTOL.py
# 
# Created: May 2019, M Clarke
#          Sep 2020, M. Clarke 

'''
#----------------------------------------------------------------------
#   Imports
# ---------------------------------------------------------------------
import RCAIDE
from RCAIDE.Framework.Core import Units, Data    
from RCAIDE.Library.Methods.Performance.estimate_cruise_drag                   import estimate_cruise_drag 
from RCAIDE.Library.Methods.Energy.Sources.Battery.Common                      import initialize_from_circuit_configuration 
from RCAIDE.Library.Methods.Weights.Correlation_Buildups.Propulsion            import nasa_motor
from RCAIDE.Library.Methods.Propulsors.Converters.DC_Motor                     import design_motor
from RCAIDE.Library.Methods.Propulsors.Converters.Rotor                        import design_prop_rotor ,design_prop_rotor 
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Electric            import compute_weight , converge_weight 
from RCAIDE.Library.Plots                                                      import *       
 
import os
import numpy as np 
from copy import deepcopy
import pickle  
 

def vehicle_setup():

    # ------------------------------------------------------------------
    #   Initialize the Vehicle
    # ------------------------------------------------------------------     
    vehicle                                     = RCAIDE.Vehicle()
    vehicle.tag                                 = 'Vahana'
    vehicle.configuration                       = 'eVTOL'
    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------    
    # mass properties
    vehicle.mass_properties.takeoff             = 735. 
    vehicle.mass_properties.operating_empty     = 735.
    vehicle.mass_properties.max_takeoff         = 735.
    vehicle.mass_properties.center_of_gravity   = [[ 2.0144,   0.  ,  0.]] 
    vehicle.passengers                          = 0
    vehicle.envelope.ultimate_load              = 5.7
    vehicle.envelope.limit_load                 = 3.     

    # ------------------------------------------------------    
    # WINGS    
    # ------------------------------------------------------  
    wing                                        = RCAIDE.Library.Components.Wings.Main_Wing()
    wing.tag                                    = 'canard_wing'  
    wing.aspect_ratio                           = 11.37706641  
    wing.sweeps.quarter_chord                   = 0.0
    wing.thickness_to_chord                     = 0.18  
    wing.taper                                  = 1.  
    wing.spans.projected                        = 6.65 
    wing.chords.root                            = 0.95 
    wing.total_length                           = 0.95   
    wing.chords.tip                             = 0.95 
    wing.chords.mean_aerodynamic                = 0.95   
    wing.dihedral                               = 0.0  
    wing.areas.reference                        = wing.chords.root*wing.spans.projected 
    wing.areas.wetted                           = 2*wing.chords.root*wing.spans.projected*0.95  
    wing.areas.exposed                          = 2*wing.chords.root*wing.spans.projected*0.95 
    wing.twists.root                            = 0.  
    wing.twists.tip                             = 0.  
    wing.origin                                 = [[0.1,  0.0 , 0.0]]  
    wing.aerodynamic_center                     = [0., 0., 0.]     
    wing.winglet_fraction                       = 0.0 
    wing.symmetric                              = True

    
    ospath                                      = os.path.abspath(__file__) 
    separator                                   = os.path.sep
    rel_path                                    = os.path.dirname(ospath) + separator  
    airfoil                                     = RCAIDE.Library.Components.Airfoils.Airfoil()
    airfoil.coordinate_file                     = rel_path + 'Airfoils' + separator + 'NACA_63_412.txt'
    
    wing.append_airfoil(airfoil)
                                                
    # add to vehicle                                          
    vehicle.append_component(wing)                            
                                                
    wing                                        = RCAIDE.Library.Components.Wings.Main_Wing()
    wing.tag                                    = 'main_wing'  
    wing.aspect_ratio                           = 11.37706641  
    wing.sweeps.quarter_chord                   = 0.0
    wing.thickness_to_chord                     = 0.18  
    wing.taper                                  = 1.  
    wing.spans.projected                        = 6.65 
    wing.chords.root                            = 0.95 
    wing.total_length                           = 0.95   
    wing.chords.tip                             = 0.95 
    wing.chords.mean_aerodynamic                = 0.95   
    wing.dihedral                               = 0.0  
    wing.areas.reference                        = wing.chords.root*wing.spans.projected 
    wing.areas.wetted                           = 2*wing.chords.root*wing.spans.projected*0.95  
    wing.areas.exposed                          = 2*wing.chords.root*wing.spans.projected*0.95 
    wing.twists.root                            = 0.  
    wing.twists.tip                             = 0.  
    wing.origin                                 = [[ 5.138, 0.0  ,  1.323 ]]  # for images 1.54
    wing.aerodynamic_center                     = [0., 0., 0.]     
    wing.winglet_fraction                       = 0.0  
    wing.symmetric                              = True  
    vehicle.reference_area                      = 2*wing.areas.reference 
    wing.append_airfoil(airfoil)

    # add to vehicle 
    vehicle.append_component(wing)   


    # ------------------------------------------------------    
    # FUSELAGE    
    # ------------------------------------------------------    
    # FUSELAGE PROPERTIES                       
    fuselage                                    = RCAIDE.Library.Components.Fuselages.Fuselage()
    fuselage.tag                                = 'fuselage' 
    fuselage.seats_abreast                      = 0.  
    fuselage.seat_pitch                         = 1.  
    fuselage.fineness.nose                      = 1.5 
    fuselage.fineness.tail                      = 4.0 
    fuselage.lengths.nose                       = 1.7   
    fuselage.lengths.tail                       = 2.7 
    fuselage.lengths.cabin                      = 1.7  
    fuselage.lengths.total                      = 6.1  
    fuselage.width                              = 1.15  
    fuselage.heights.maximum                    = 1.7 
    fuselage.heights.at_quarter_length          = 1.2  
    fuselage.heights.at_wing_root_quarter_chord = 1.7  
    fuselage.heights.at_three_quarters_length   = 0.75 
    fuselage.areas.wetted                       = 12.97989862  
    fuselage.areas.front_projected              = 1.365211404  
    fuselage.effective_diameter                 = 1.318423736  
    fuselage.differential_pressure              = 0.  

    # Segment  
    segment                                     = RCAIDE.Library.Components.Fuselages.Segment() 
    segment.tag                                 = 'segment_0'   
    segment.percent_x_location                  = 0.  
    segment.percent_z_location                  = 0.  
    segment.height                              = 0.09  
    segment.width                               = 0.23473  
    segment.length                              = 0.  
    segment.effective_diameter                  = 0. 
    fuselage.Segments.append(segment)             

    # Segment                                   
    segment                                     = RCAIDE.Library.Components.Fuselages.Segment()
    segment.tag                                 = 'segment_1'   
    segment.percent_x_location                  = 0.97675/6.1 
    segment.percent_z_location                  = 0.21977/6.1
    segment.height                              = 0.9027  
    segment.width                               = 1.01709  
    fuselage.Segments.append(segment)             


    # Segment                                   
    segment                                     = RCAIDE.Library.Components.Fuselages.Segment()
    segment.tag                                 = 'segment_2'    
    segment.percent_x_location                  = 1.93556/6.1 
    segment.percent_z_location                  = 0.39371/6.1
    segment.height                              = 1.30558   
    segment.width                               = 1.38871  
    fuselage.Segments.append(segment)             


    # Segment                                   
    segment                                     = RCAIDE.Library.Components.Fuselages.Segment()
    segment.tag                                 = 'segment_3'    
    segment.percent_x_location                  = 3.44137/6.1 
    segment.percent_z_location                  = 0.57143/6.1
    segment.height                              = 1.52588 
    segment.width                               = 1.47074 
    fuselage.Segments.append(segment)             

    # Segment                                   
    segment                                     = RCAIDE.Library.Components.Fuselages.Segment()
    segment.tag                                 = 'segment_4'   
    segment.percent_x_location                  = 4.61031/6.1
    segment.percent_z_location                  = 0.10893
    segment.height                              = 1.3906
    segment.width                               = 1.11463  
    fuselage.Segments.append(segment)              

    # Segment                                   
    segment                                     = RCAIDE.Library.Components.Fuselages.Segment()
    segment.tag                                 = 'segment_5'   
    segment.percent_x_location                  = 0.9827
    segment.percent_z_location                  = 0.180
    segment.height                              = 0.6145
    segment.width                               = 0.3838
    fuselage.Segments.append(segment)            
    
    
    # Segment                                   
    segment                                     = RCAIDE.Library.Components.Fuselages.Segment()
    segment.tag                                 = 'segment_6'   
    segment.percent_x_location                  = 1. 
    segment.percent_z_location                  = 0.2058
    segment.height                              = 0.4
    segment.width                               = 0.25
    fuselage.Segments.append(segment)        

    # add to vehicle
    vehicle.append_component(fuselage)    

    #------------------------------------------------------------------------------------------------------------------------------------
    # ##################################   Determine Vehicle Mass Properties Using Physic Based Methods  ################################ 
    #------------------------------------------------------------------------------------------------------------------------------------     
    sys                            = RCAIDE.Library.Components.Systems.System()
    sys.mass_properties.mass       = 5 # kg   
    vehicle.append_component(sys)    

    #------------------------------------------------------------------------------------------------------------------------------------
    # ########################################################  Energy Network  ######################################################### 
    #------------------------------------------------------------------------------------------------------------------------------------
    # define network
    network                                                = RCAIDE.Framework.Networks.Electric()
 
 
     
    #==================================================================================================================================== 
    # Lift Bus 
    #====================================================================================================================================          
    bus                                                    = RCAIDE.Library.Components.Energy.Distribution.Electrical_Bus()
    bus.tag                                                = 'bus' 

    #------------------------------------------------------------------------------------------------------------------------------------  
    # Bus Battery
    #------------------------------------------------------------------------------------------------------------------------------------ 
    bat                                                    = RCAIDE.Library.Components.Energy.Sources.Batteries.Lithium_Ion_NMC() 
    bat.tag                                                = 'bus_battery'
    bat.pack.electrical_configuration.series               = 80 
    bat.pack.electrical_configuration.parallel             = 60
    initialize_from_circuit_configuration(bat)  
    bat.module.number_of_modules                           = 10 
    bat.module.geometrtic_configuration.total              = bat.pack.electrical_configuration.total
    bat.module.voltage                                     = bat.pack.maximum_voltage/bat.module.number_of_modules 
    bat.module.geometrtic_configuration.normal_count       = 20
    bat.module.geometrtic_configuration.parallel_count     = 24  
    bus.voltage                                            =  bat.pack.maximum_voltage  
    bus.batteries.append(bat)      
     
    
    #------------------------------------------------------------------------------------------------------------------------------------  
    # Lift Propulsors 
    #------------------------------------------------------------------------------------------------------------------------------------    
     
    # Define Lift Propulsor Container 
    lift_propulsor                                = RCAIDE.Library.Components.Propulsors.Electric_Rotor()
    lift_propulsor.tag                            = 'lift_propulsor'     
    lift_propulsor.active_batteries               = ['bus_battery']          
              
    # Electronic Speed Controller           
    prop_rotor_esc                                = RCAIDE.Library.Components.Propulsors.Modulators.Electronic_Speed_Controller()
    prop_rotor_esc.efficiency                     = 0.95    
    prop_rotor_esc.tag                            = 'prop_rotor_esc_1'  
    lift_propulsor.electronic_speed_controller    = prop_rotor_esc  
    
    # Lift Rotor Design
    g                                             = 9.81                                   # gravitational acceleration  
    Drag                                          = estimate_cruise_drag(vehicle,altitude = 1500. * Units.ft,speed= 130.* Units['mph'] ,lift_coefficient = 0.5 ,profile_drag = 0.06)
    Hover_Load                                    = vehicle.mass_properties.takeoff*g *1.2      # hover load   
    
    prop_rotor                                    = RCAIDE.Library.Components.Propulsors.Converters.Prop_Rotor()   
    prop_rotor.tag                                = 'prop_rotor'   
    prop_rotor.tip_radius                         = 0.8875
    prop_rotor.hub_radius                         = 0.15 * prop_rotor.tip_radius
    prop_rotor.number_of_blades                   = 3
    
    prop_rotor.hover.design_altitude              = 40 * Units.feet   
    prop_rotor.hover.design_thrust                = Hover_Load/8 
    prop_rotor.hover.design_freestream_velocity   = np.sqrt(prop_rotor.hover.design_thrust/(2*1.2*np.pi*(prop_rotor.tip_radius**2)))  
    prop_rotor.oei.design_altitude                = 40 * Units.feet  
    prop_rotor.oei.design_thrust                  = Hover_Load/7  
    prop_rotor.oei.design_freestream_velocity     = np.sqrt(prop_rotor.oei.design_thrust/(2*1.2*np.pi*(prop_rotor.tip_radius**2)))   
    prop_rotor.cruise.design_altitude             = 1500 * Units.feet
    prop_rotor.cruise.design_thrust               = Drag /8     
    prop_rotor.cruise.design_freestream_velocity  = 130.* Units['mph']  
    
    airfoil                                       = RCAIDE.Library.Components.Airfoils.Airfoil()   
    airfoil.coordinate_file                       = rel_path + 'Airfoils' + separator + 'NACA_4412.txt'
    airfoil.polar_files                           = [rel_path + 'Airfoils' + separator + 'Polars' + separator + 'NACA_4412_polar_Re_50000.txt' ,
                                                    rel_path + 'Airfoils' + separator + 'Polars' + separator + 'NACA_4412_polar_Re_100000.txt' ,
                                                     rel_path + 'Airfoils' + separator + 'Polars' + separator + 'NACA_4412_polar_Re_200000.txt' ,
                                                     rel_path + 'Airfoils' + separator + 'Polars' + separator + 'NACA_4412_polar_Re_500000.txt' ,
                                                     rel_path + 'Airfoils' + separator + 'Polars' + separator + 'NACA_4412_polar_Re_1000000.txt',
                                                     rel_path + 'Airfoils' + separator + 'Polars' + separator + 'NACA_4412_polar_Re_3500000.txt',
                                                     rel_path + 'Airfoils' + separator + 'Polars' + separator + 'NACA_4412_polar_Re_5000000.txt',
                                                     rel_path + 'Airfoils' + separator + 'Polars' + separator + 'NACA_4412_polar_Re_7500000.txt' ]
    prop_rotor.append_airfoil(airfoil)                
    prop_rotor.airfoil_polar_stations             = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]   
    design_prop_rotor(prop_rotor)     
     
    
    #------------------------------------------------------------------------------------------------------------------------------------               
    # Lift Rotor Motor  
    #------------------------------------------------------------------------------------------------------------------------------------    
    prop_rotor_motor                         = RCAIDE.Library.Components.Propulsors.Converters.DC_Motor()
    prop_rotor_motor.efficiency              = 0.95
    prop_rotor_motor.nominal_voltage         = bat.pack.maximum_voltage*3/4   
    prop_rotor_motor.prop_rotor_radius       = prop_rotor.tip_radius 
    prop_rotor_motor.no_load_current         = 0.1  
    prop_rotor_motor.wing_mounted            = True 
    prop_rotor_motor.rotor_radius            = prop_rotor.tip_radius
    prop_rotor_motor.design_torque           = prop_rotor.hover.design_torque
    prop_rotor_motor.angular_velocity        = prop_rotor.hover.design_angular_velocity/prop_rotor_motor.gear_ratio  
    design_motor(prop_rotor_motor)
    prop_rotor_motor.mass_properties.mass    = nasa_motor(prop_rotor_motor.design_torque)     
    lift_propulsor.motor                     = prop_rotor_motor
     

    #------------------------------------------------------------------------------------------------------------------------------------               
    # Lift Rotor Nacelle
    #------------------------------------------------------------------------------------------------------------------------------------     
    nacelle                           = RCAIDE.Library.Components.Nacelles.Nacelle() 
    nacelle.length                    = 0.45
    nacelle.diameter                  = 0.3 
    nacelle.flow_through              = False    
    lift_propulsor.nacelle            =  nacelle  

    # Front Rotors Locations 
    origins = [[-0.2, 1.347, 0.0], [-0.2, 3.2969999999999997, 0.0], [-0.2, -1.347, 0.0], [-0.2, -3.2969999999999997, 0.0],\
               [4.938, 1.347, 1.54], [4.938, 3.2969999999999997, 1.54],[4.938, -1.347, 1.54], [4.938, -3.2969999999999997, 1.54]] 
    
    for i in range(8): 
        lift_propulsor_i                                       = deepcopy(lift_propulsor)
        lift_propulsor_i.tag                                   = 'lift_rotor_propulsor_' + str(i + 1)
        lift_propulsor_i.rotor.tag                             = 'prop_rotor_' + str(i + 1) 
        lift_propulsor_i.rotor.origin                          = [origins[i]]  
        lift_propulsor_i.motor.tag                             = 'prop_rotor_motor_' + str(i + 1)  
        if i < 4: 
            lift_propulsor_i.motor.wing_tag                = 'canard_wing'
        else:
            lift_propulsor_i.motor.wing_tag                = 'main_wing'
        lift_propulsor_i.motor.origin                          = [origins[i]]  
        lift_propulsor_i.electronic_speed_controller.tag       = 'prop_rotor_esc_' + str(i + 1)  
        lift_propulsor_i.electronic_speed_controller.origin    = [origins[i]]  
        lift_propulsor_i.nacelle.tag                           = 'prop_rotor_nacelle_' + str(i + 1)  
        lift_propulsor_i.nacelle.origin                        = [origins[i]]   
        bus.propulsors.append(lift_propulsor_i)  

    #------------------------------------------------------------------------------------------------------------------------------------  
    # Additional Bus Loads
    #------------------------------------------------------------------------------------------------------------------------------------            
    # Payload   
    payload                         = RCAIDE.Library.Components.Systems.Avionics()
    payload.power_draw              = 10. # Watts 
    payload.mass_properties.mass    = 1.0 * Units.kg
    bus.payload                     = payload 
                             
    # Avionics                            
    avionics                        = RCAIDE.Library.Components.Systems.Avionics()
    avionics.power_draw             = 10. # Watts  
    avionics.mass_properties.mass   = 1.0 * Units.kg
    bus.avionics                    = avionics    

   
    network.busses.append(bus)
    
    # append motor origin spanwise locations onto wing data structure
    motor_origins_front                                   = np.array(origins[:4])
    motor_origins_rear                                    = np.array(origins[5:])
    vehicle.wings['canard_wing'].motor_spanwise_locations = motor_origins_front[:,1]/ vehicle.wings['canard_wing'].spans.projected
    vehicle.wings['canard_wing'].motor_spanwise_locations = motor_origins_front[:,1]/ vehicle.wings['canard_wing'].spans.projected
    vehicle.wings['main_wing'].motor_spanwise_locations   = motor_origins_rear[:,1]/ vehicle.wings['main_wing'].spans.projected
      
        
    # append energy network 
    vehicle.append_energy_network(network)  
 
    #------------------------------------------------------------------------------------------------------------------------------------
    # ##################################   Determine Vehicle Mass Properties Using Physic Based Methods  ################################ 
    #------------------------------------------------------------------------------------------------------------------------------------   
    converge_weight(vehicle) 
    breakdown = compute_weight(vehicle)
    print(breakdown) 

    return vehicle

# ----------------------------------------------------------------------
#   Define the Configurations
# ---------------------------------------------------------------------

def configs_setup(vehicle):
    '''
    The configration set up below the scheduling of the nacelle angle and vehicle speed.
    Since one prop_rotor operates at varying flight conditions, one must perscribe  the 
    pitch command of the prop_rotor which us used in the variable pitch model in the analyses
    Note: low pitch at take off & low speeds, high pitch at cruise
    '''
    # ------------------------------------------------------------------
    #   Initialize Configurations
    # ------------------------------------------------------------------ 
    configs = RCAIDE.Library.Components.Configs.Config.Container() 
    base_config                                                       = RCAIDE.Library.Components.Configs.Config(vehicle)
    base_config.tag                                                   = 'base'     
    configs.append(base_config) 
 
    # ------------------------------------------------------------------
    #   Hover Climb Configuration
    # ------------------------------------------------------------------
    config                                                 = RCAIDE.Library.Components.Configs.Config(vehicle)
    config.tag                                             = 'vertical_climb'
    vector_angle                                           = 90.0 * Units.degrees
    config.wings.main_wing.twists.root                     = vector_angle
    config.wings.main_wing.twists.tip                      = vector_angle
    config.wings.canard_wing.twists.root                   = vector_angle
    config.wings.canard_wing.twists.tip                    = vector_angle    
    for network in  config.networks: 
        for bus in network.busses: 
            for propulsor in  bus.propulsors:
                propulsor.rotor.inputs.y_axis_rotation =  vector_angle 
    configs.append(config)

    # ------------------------------------------------------------------
    #    
    # ------------------------------------------------------------------
    config                                            = RCAIDE.Library.Components.Configs.Config(vehicle)
    vector_angle                                      = 45.0  * Units.degrees 
    config.tag                                        = 'vertical_transition'
    config.wings.main_wing.twists.root                = vector_angle
    config.wings.main_wing.twists.tip                 = vector_angle
    config.wings.canard_wing.twists.root              = vector_angle
    config.wings.canard_wing.twists.tip               = vector_angle
    for network in  config.networks: 
        for bus in network.busses: 
            for propulsor in  bus.propulsors:
                propulsor.rotor.inputs.y_axis_rotation = vector_angle
                propulsor.rotor.inputs.pitch_command   = propulsor.rotor.cruise.design_collective_pitch  
    configs.append(config)
    

    # ------------------------------------------------------------------
    #   Hover-to-Cruise Configuration
    # ------------------------------------------------------------------
    config                                            = RCAIDE.Library.Components.Configs.Config(vehicle)
    config.tag                                        = 'climb_transition'
    vector_angle                                      = 5.0  * Units.degrees  
    config.wings.main_wing.twists.root                = vector_angle
    config.wings.main_wing.twists.tip                 = vector_angle
    config.wings.canard_wing.twists.root              = vector_angle
    config.wings.canard_wing.twists.tip               = vector_angle 
    for network in  config.networks: 
        for bus in network.busses: 
            for propulsor in  bus.propulsors:
                propulsor.rotor.inputs.y_axis_rotation = vector_angle
                propulsor.rotor.inputs.pitch_command   = propulsor.rotor.cruise.design_collective_pitch  
    configs.append(config) 

    # ------------------------------------------------------------------
    #   Cruise Configuration
    # ------------------------------------------------------------------
    config                                            = RCAIDE.Library.Components.Configs.Config(vehicle)
    config.tag                                        = 'cruise'   
    vector_angle                                      = 0.0 * Units.degrees 
    config.wings.main_wing.twists.root                = vector_angle
    config.wings.main_wing.twists.tip                 = vector_angle
    config.wings.canard_wing.twists.root              = vector_angle
    config.wings.canard_wing.twists.tip               = vector_angle  
    for network in  config.networks: 
        for bus in network.busses: 
            for propulsor in  bus.propulsors:
                propulsor.rotor.inputs.y_axis_rotation = vector_angle
                propulsor.rotor.inputs.pitch_command   = propulsor.rotor.cruise.design_collective_pitch  
    configs.append(config)    
    
  

    # ------------------------------------------------------------------
    #   Approach Configuration
    # ------------------------------------------------------------------
    config                                            = RCAIDE.Library.Components.Configs.Config(vehicle)
    config.tag                                        = 'approach'   
    vector_angle                                      = 5.0 * Units.degrees 
    config.wings.main_wing.twists.root                = vector_angle
    config.wings.main_wing.twists.tip                 = vector_angle
    config.wings.canard_wing.twists.root              = vector_angle
    config.wings.canard_wing.twists.tip               = vector_angle 
    for network in  config.networks: 
        for bus in network.busses: 
            for propulsor in  bus.propulsors:
                propulsor.rotor.inputs.y_axis_rotation = vector_angle
                propulsor.rotor.inputs.pitch_command   = propulsor.rotor.cruise.design_collective_pitch    
    configs.append(config)     
    
    # ------------------------------------------------------------------
    #   
    # ------------------------------------------------------------------ 
    config                                                 = RCAIDE.Library.Components.Configs.Config(vehicle)
    vector_angle                                           = 75.0  * Units.degrees   
    config.tag                                             = 'descent_transition'   
    config.wings.main_wing.twists.root                     = vector_angle
    config.wings.main_wing.twists.tip                      = vector_angle
    config.wings.canard_wing.twists.root                   = vector_angle
    config.wings.canard_wing.twists.tip                    = vector_angle
    for network in  config.networks: 
        for bus in network.busses: 
            for propulsor in  bus.propulsors:
                propulsor.rotor.inputs.y_axis_rotation = vector_angle
                propulsor.rotor.inputs.pitch_command   = propulsor.rotor.cruise.design_collective_pitch * 0.5
    configs.append(config) 
    

    # ------------------------------------------------------------------
    #   Hover Configuration
    # ------------------------------------------------------------------
    config                                            = RCAIDE.Library.Components.Configs.Config(vehicle)
    config.tag                                        = 'vertical_descent'
    vector_angle                                      = 90.0  * Units.degrees   
    config.wings.main_wing.twists.root                = vector_angle
    config.wings.main_wing.twists.tip                 = vector_angle
    config.wings.canard_wing.twists.root              = vector_angle
    config.wings.canard_wing.twists.tip               = vector_angle     
    for network in  config.networks: 
        for bus in network.busses: 
            for propulsor in  bus.propulsors:
                propulsor.rotor.inputs.y_axis_rotation = vector_angle 
    configs.append(config)

    return configs 

 