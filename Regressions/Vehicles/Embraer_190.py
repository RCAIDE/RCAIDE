# Regression/scripts/Vehicles/Embraer_E190.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports 
import RCAIDE
from RCAIDE.Core import Units      
from RCAIDE.Methods.Energy.Propulsion.Converters.Turbofan  import design_turbofan
from RCAIDE.Methods.Geometry.Two_Dimensional.Planform      import wing_planform, segment_properties
from RCAIDE.Visualization                 import *     

# python imports 
import numpy as np  
from copy import deepcopy

# ----------------------------------------------------------------------------------------------------------------------
#   Build the Vehicle
# ----------------------------------------------------------------------------------------------------------------------
def vehicle_setup():
    # ------------------------------------------------------------------
    #   Initialize the Vehicle
    # ------------------------------------------------------------------

    vehicle = RCAIDE.Vehicle()
    vehicle.tag = 'Embraer_E190AR'

    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------

    # mass properties (http://www.embraercommercialaviation.com/AircraftPDF/E190_Weights.pdf)
    vehicle.mass_properties.max_takeoff               = 51800.   # kg
    vehicle.mass_properties.operating_empty           = 27837.   # kg
    vehicle.mass_properties.takeoff                   = 51800.   # kg
    vehicle.mass_properties.max_zero_fuel             = 40900.   # kg
    vehicle.mass_properties.max_payload               = 13063.   # kg
    vehicle.mass_properties.max_fuel                  = 12971.   # kg
    vehicle.mass_properties.cargo                     =     0.0  # kg

    vehicle.mass_properties.center_of_gravity         = [[16.8, 0, 1.6]]
    vehicle.mass_properties.moments_of_inertia.tensor = [[10 ** 5, 0, 0],[0, 10 ** 6, 0,],[0,0, 10 ** 7]] 

    # envelope properties
    vehicle.envelope.ultimate_load = 3.5
    vehicle.envelope.limit_load    = 1.5

    # basic parameters
    vehicle.reference_area         = 92.
    vehicle.passengers             = 106
    vehicle.systems.control        = "fully powered"
    vehicle.systems.accessories    = "medium range"


    # ------------------------------------------------------------------
    #   Main Wing
    # ------------------------------------------------------------------
    wing                         = RCAIDE.Components.Wings.Main_Wing()
    wing.tag                     = 'main_wing'
    wing.areas.reference         = 92.0
    wing.aspect_ratio            = 8.4
    wing.chords.root             = 6.2
    wing.chords.tip              = 1.44
    wing.sweeps.quarter_chord    = 23.0 * Units.deg
    wing.thickness_to_chord      = 0.11
    wing.taper                   = 0.28
    wing.dihedral                = 5.00 * Units.deg
    wing.spans.projected         = 28.72
    wing.origin                  = [[13.0,0,-1.]]
    wing.vertical                = False
    wing.symmetric               = True       
    wing.high_lift               = True
    wing.areas.exposed           = 0.80 * wing.areas.wetted        
    wing.twists.root             = 2.0 * Units.degrees
    wing.twists.tip              = 0.0 * Units.degrees    
    wing.dynamic_pressure_ratio  = 1.0
    
    
    segment = RCAIDE.Components.Wings.Segment()
    segment.tag                   = 'root'
    segment.percent_span_location = 0.0
    segment.twist                 = 4. * Units.deg
    segment.root_chord_percent    = 1.
    segment.thickness_to_chord    = .11
    segment.dihedral_outboard     = 5. * Units.degrees
    segment.sweeps.quarter_chord  = 20.6 * Units.degrees
    wing.Segments.append(segment)    
    
    segment = RCAIDE.Components.Wings.Segment()
    segment.tag                   = 'yehudi'
    segment.percent_span_location = 0.348
    segment.twist                 = (4. - segment.percent_span_location*4.) * Units.deg
    segment.root_chord_percent    = 0.60
    segment.thickness_to_chord    = .11
    segment.dihedral_outboard     = 4 * Units.degrees
    segment.sweeps.quarter_chord  = 24.1 * Units.degrees
    wing.Segments.append(segment)
    
    segment = RCAIDE.Components.Wings.Segment()
    segment.tag                   = 'section_2'
    segment.percent_span_location = 0.961
    segment.twist                 = (4. - segment.percent_span_location*4.) * Units.deg
    segment.root_chord_percent    = 0.25
    segment.thickness_to_chord    = .11
    segment.dihedral_outboard     = 70. * Units.degrees
    segment.sweeps.quarter_chord  = 50. * Units.degrees
    wing.Segments.append(segment)

    segment = RCAIDE.Components.Wings.Segment() 
    segment.tag                   = 'Tip'
    segment.percent_span_location = 1.
    segment.twist                 = (4. - segment.percent_span_location*4.) * Units.deg
    segment.root_chord_percent    = 0.070
    segment.thickness_to_chord    = .11
    segment.dihedral_outboard     = 0.
    segment.sweeps.quarter_chord  = 0.
    wing.Segments.append(segment)       
    
    # Fill out more segment properties automatically
    wing = segment_properties(wing)        

    # control surfaces -------------------------------------------
    flap                       = RCAIDE.Components.Wings.Control_Surfaces.Flap() 
    flap.tag                   = 'flap' 
    flap.span_fraction_start   = 0.11
    flap.span_fraction_end     = 0.85
    flap.deflection            = 0.0 * Units.deg 
    flap.chord_fraction        = 0.28    
    flap.configuration_type    = 'double_slotted'
    wing.append_control_surface(flap)   
        
    slat                       = RCAIDE.Components.Wings.Control_Surfaces.Slat()
    slat.tag                   = 'slat' 
    slat.span_fraction_start   = 0.324 
    slat.span_fraction_end     = 0.963     
    slat.deflection            = 1.0 * Units.deg 
    slat.chord_fraction        = 0.1   
    wing.append_control_surface(slat) 
    
    wing                         = wing_planform(wing)
    
    wing.areas.exposed           = 0.80 * wing.areas.wetted
    wing.twists.root             = 2.0 * Units.degrees
    wing.twists.tip              = 0.0 * Units.degrees    
    wing.dynamic_pressure_ratio  = 1.0   

    # add to vehicle
    vehicle.append_component(wing)
    
    # ------------------------------------------------------------------
    #  Horizontal Stabilizer
    # ------------------------------------------------------------------

    wing = RCAIDE.Components.Wings.Horizontal_Tail()
    wing.tag = 'horizontal_stabilizer'
    wing.areas.reference         = 26.0
    wing.aspect_ratio            = 5.5
    wing.sweeps.quarter_chord    = 34.5 * Units.deg
    wing.thickness_to_chord      = 0.11
    wing.taper                   = 0.11
    wing.dihedral                = 8.4 * Units.degrees
    wing.origin                  = [[31,0,1.5]]
    wing.vertical                = False
    wing.symmetric               = True       
    wing.high_lift               = False  
    wing                         = wing_planform(wing)
    wing.areas.exposed           = 0.9 * wing.areas.wetted 
    wing.twists.root             = 2.0 * Units.degrees
    wing.twists.tip              = 2.0 * Units.degrees    
    wing.dynamic_pressure_ratio  = 0.90

    # add to vehicle
    vehicle.append_component(wing)

    # ------------------------------------------------------------------
    #   Vertical Stabilizer
    # ------------------------------------------------------------------

    wing = RCAIDE.Components.Wings.Vertical_Tail()
    wing.tag = 'vertical_stabilizer'
    wing.areas.reference         = 16.0
    wing.aspect_ratio            =  1.7
    wing.sweeps.quarter_chord    = 35. * Units.deg
    wing.thickness_to_chord      = 0.11
    wing.taper                   = 0.31
    wing.dihedral                = 0.00
    wing.origin                  = [[30.4,0,1.675]]
    wing.vertical                = True
    wing.symmetric               = False       
    wing.high_lift               = False
    wing                         = wing_planform(wing)
    wing.areas.exposed           = 0.9 * wing.areas.wetted
    wing.twists.root             = 0.0 * Units.degrees
    wing.twists.tip              = 0.0 * Units.degrees    
    wing.dynamic_pressure_ratio  = 1.00
    
    # add to vehicle
    vehicle.append_component(wing)
    
    # ------------------------------------------------------------------
    #  Fuselage
    # ------------------------------------------------------------------

    fuselage = RCAIDE.Components.Fuselages.Fuselage()
    fuselage.tag    = 'fuselage'
    fuselage.origin = [[0,0,0]]
    fuselage.number_coach_seats    = vehicle.passengers
    fuselage.seats_abreast         = 4
    fuselage.seat_pitch            = 30. * Units.inches

    fuselage.fineness.nose         = 1.28
    fuselage.fineness.tail         = 3.48

    fuselage.lengths.nose          = 6.0
    fuselage.lengths.tail          = 9.0
    fuselage.lengths.cabin         = 21.24
    fuselage.lengths.total         = 36.24
    fuselage.lengths.fore_space    = 0.
    fuselage.lengths.aft_space     = 0.

    fuselage.width                 = 3.01 * Units.meters

    fuselage.heights.maximum       = 3.35    
    fuselage.heights.at_quarter_length          = 3.35 
    fuselage.heights.at_three_quarters_length   = 3.35 
    fuselage.heights.at_wing_root_quarter_chord = 3.35 

    fuselage.areas.side_projected  = 239.20
    fuselage.areas.wetted          = 327.01
    fuselage.areas.front_projected = 8.0110

    fuselage.effective_diameter    = 3.18

    fuselage.differential_pressure = 10**5 * Units.pascal    # Maximum differential pressure  
    

    # Segment  
    segment                                     = RCAIDE.Components.Lofted_Body_Segment.Segment() 
    segment.tag                                 = 'segment_0'    
    segment.percent_x_location                  = 0.0000
    segment.percent_z_location                  = -0.00144 
    segment.height                              = 0.0100 
    segment.width                               = 0.0100  
    fuselage.Segments.append(segment)   
    
    # Segment  
    segment                                     = RCAIDE.Components.Lofted_Body_Segment.Segment() 
    segment.tag                                 = 'segment_1'    
    segment.percent_x_location                  = 0.00576 
    segment.percent_z_location                  = -0.00144 
    segment.height                              = 0.7500
    segment.width                               = 0.6500
    fuselage.Segments.append(segment)   
    
    # Segment                                   
    segment                                     = RCAIDE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_2'   
    segment.percent_x_location                  = 0.02017 
    segment.percent_z_location                  = 0.00000 
    segment.height                              = 1.52783 
    segment.width                               = 1.20043 
    fuselage.Segments.append(segment)      
    
    # Segment                                   
    segment                                     = RCAIDE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_3'   
    segment.percent_x_location                  = 0.03170 
    segment.percent_z_location                  = 0.00000 
    segment.height                              = 1.96435 
    segment.width                               = 1.52783 
    fuselage.Segments.append(segment)   

    # Segment                                   
    segment                                     = RCAIDE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_4'   
    segment.percent_x_location                  = 0.04899 	
    segment.percent_z_location                  = 0.00431 
    segment.height                              = 2.72826 
    segment.width                               = 1.96435 
    fuselage.Segments.append(segment)   
    
    # Segment                                   
    segment                                     = RCAIDE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_5'   
    segment.percent_x_location                  = 0.07781 
    segment.percent_z_location                  = 0.00861 
    segment.height                              = 3.49217 
    segment.width                               = 2.61913 
    fuselage.Segments.append(segment)     
    
    # Segment                                   
    segment                                     = RCAIDE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_6'   
    segment.percent_x_location                  = 0.10375 
    segment.percent_z_location                  = 0.01005 
    segment.height                              = 3.70130 
    segment.width                               = 3.05565 
    fuselage.Segments.append(segment)             
     
    # Segment                                   
    segment                                     = RCAIDE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_7'   
    segment.percent_x_location                  = 0.16427 
    segment.percent_z_location                  = 0.01148 
    segment.height                              = 3.92870 
    segment.width                               = 3.71043 
    fuselage.Segments.append(segment)    
    
    # Segment                                   
    segment                                     = RCAIDE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_8'   
    segment.percent_x_location                  = 0.22478 
    segment.percent_z_location                  = 0.01148 
    segment.height                              = 3.92870 
    segment.width                               = 3.92870 
    fuselage.Segments.append(segment)   
    
    # Segment                                   
    segment                                     = RCAIDE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_9'     
    segment.percent_x_location                  = 0.69164 
    segment.percent_z_location                  = 0.01292
    segment.height                              = 3.81957
    segment.width                               = 3.81957
    fuselage.Segments.append(segment)     
        
    # Segment                                   
    segment                                     = RCAIDE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_10'     
    segment.percent_x_location                  = 0.71758 
    segment.percent_z_location                  = 0.01292
    segment.height                              = 3.81957
    segment.width                               = 3.81957
    fuselage.Segments.append(segment)   
        
    # Segment                                   
    segment                                     = RCAIDE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_11'     
    segment.percent_x_location                  = 0.78098 
    segment.percent_z_location                  = 0.01722
    segment.height                              = 3.49217
    segment.width                               = 3.71043
    fuselage.Segments.append(segment)    
        
    # Segment                                   
    segment                                     = RCAIDE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_12'     
    segment.percent_x_location                  = 0.85303
    segment.percent_z_location                  = 0.02296
    segment.height                              = 3.05565
    segment.width                               = 3.16478
    fuselage.Segments.append(segment)             
        
    # Segment                                   
    segment                                     = RCAIDE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_13'     
    segment.percent_x_location                  = 0.91931 
    segment.percent_z_location                  = 0.03157
    segment.height                              = 2.40087
    segment.width                               = 1.96435
    fuselage.Segments.append(segment)               
        
    # Segment                                   
    segment                                     = RCAIDE.Components.Lofted_Body_Segment.Segment()
    segment.tag                                 = 'segment_14'     
    segment.percent_x_location                  = 1.00 
    segment.percent_z_location                  = 0.04593
    segment.height                              = 1.09130
    segment.width                               = 0.21826
    fuselage.Segments.append(segment)       

    # add to vehicle
    vehicle.append_component(fuselage)

    # -----------------------------------------------------------------
    # Design the Nacelle
    # ----------------------------------------------------------------- 
    nacelle                               = RCAIDE.Components.Nacelles.Nacelle()
    nacelle.diameter                      = 2.05
    nacelle.length                        = 2.71
    nacelle.tag                           = 'nacelle_1'
    nacelle.inlet_diameter                = 2.0
    nacelle.origin                        = [[12.0,4.38,-2.1]]
    Awet                                  = 1.1*np.pi*nacelle.diameter*nacelle.length # 1.1 is simple coefficient
    nacelle.areas.wetted                  = Awet   
    nacelle.Airfoil.NACA_4_series_flag    = True 
    nacelle.Airfoil.coordinate_file       = '2410'
    
    
  
    nac_segment                    = RCAIDE.Components.Lofted_Body_Segment.Segment()
    nac_segment.tag                = 'segment_1'
    nac_segment.percent_x_location = 0.0  
    nac_segment.height             = 2.05
    nac_segment.width              = 2.05
    nacelle.append_segment(nac_segment)   
    
    nac_segment                    = RCAIDE.Components.Lofted_Body_Segment.Segment()
    nac_segment.tag                = 'segment_2'
    nac_segment.percent_x_location = 0.3
    nac_segment.height             = 2.1  
    nac_segment.width              = 2.1 
    nacelle.append_segment(nac_segment)   
    
    nac_segment                    = RCAIDE.Components.Lofted_Body_Segment.Segment()
    nac_segment.tag                = 'segment_3'
    nac_segment.percent_x_location = 0.4  
    nac_segment.height             = 2.05
    nac_segment.width              = 2.05 
    nacelle.append_segment(nac_segment)  
     
    nac_segment                    = RCAIDE.Components.Lofted_Body_Segment.Segment()
    nac_segment.tag                = 'segment_4'
    nac_segment.percent_x_location = 0.75  
    nac_segment.height             = 1.9
    nac_segment.width              = 1.9
    nacelle.append_segment(nac_segment)  
    
    nac_segment                    = RCAIDE.Components.Lofted_Body_Segment.Segment()
    nac_segment.tag                = 'segment_5'
    nac_segment.percent_x_location = 1.0
    nac_segment.height             = 1.7 
    nac_segment.width              = 1.7
    nacelle.append_segment(nac_segment)    
        
    nacelle_2                             = deepcopy(nacelle)
    nacelle_2.tag                         = 'nacelle_2'
    nacelle_2.origin                      = [[12.0,-4.38,-2.1]]
    
    vehicle.append_component(nacelle)   
    vehicle.append_component(nacelle_2)    
  

    #------------------------------------------------------------------------------------------------------------------------------------  
    #  Landing Gear
    #------------------------------------------------------------------------------------------------------------------------------------  
    landing_gear                          =  RCAIDE.Components.Landing_Gear.Landing_Gear()
    landing_gear.tag                      = "main_landing_gear"
    landing_gear.main_tire_diameter       = 1.12000 * Units.m
    landing_gear.nose_tire_diameter       = 0.6858 * Units.m
    landing_gear.main_strut_length        = 1.8 * Units.m
    landing_gear.nose_strut_length        = 1.3 * Units.m
    landing_gear.main_units               = 1    #number of nose landing gear
    landing_gear.nose_units               = 1    #number of nose landing gear
    landing_gear.main_wheels              = 2    #number of wheels on the main landing gear
    landing_gear.nose_wheels              = 2    #number of wheels on the nose landing gear
    vehicle.landing_gear                  = landing_gear

  
    #------------------------------------------------------------------------------------------------------------------------------------  
    #  Turbofan Network
    #------------------------------------------------------------------------------------------------------------------------------------  
    #initialize the gas turbine network
    net                   = RCAIDE.Energy.Networks.Turbofan_Engine() 
    
    #------------------------------------------------------------------------------------------------------------------------------------  
    # Fuel Distrubition Line 
    #------------------------------------------------------------------------------------------------------------------------------------  
    fuel_line                                   = RCAIDE.Energy.Networks.Distribution.Fuel_Line() 
    
    #------------------------------------------------------------------------------------------------------------------------------------  
    #   Fuel
    #------------------------------------------------------------------------------------------------------------------------------------  
    # fuel tank
    fuel_tank                                   = RCAIDE.Energy.Sources.Fuel_Tanks.Fuel_Tank()
    fuel_tank.origin                            = wing.origin 
    
    # fuel 
    fuel                                        = RCAIDE.Attributes.Propellants.Aviation_Gasoline()   
    fuel.mass_properties.mass                   = vehicle.mass_properties.max_takeoff-vehicle.mass_properties.max_fuel
    fuel.origin                                 = vehicle.wings.main_wing.mass_properties.center_of_gravity      
    fuel.mass_properties.center_of_gravity      = vehicle.wings.main_wing.aerodynamic_center
    fuel.internal_volume                        = fuel.mass_properties.mass/fuel.density  
    fuel_tank.fuel                              = fuel  
    fuel_line.fuel_tanks.append(fuel_tank) 
    

    #------------------------------------------------------------------------------------------------------------------------------------  
    #  Propulsor
    #------------------------------------------------------------------------------------------------------------------------------------   
    starboard_propulsor                             = RCAIDE.Energy.Propulsion.Propulsor() 
       
    # Turbofan     
    turbofan                                        = RCAIDE.Energy.Propulsion.Converters.Turbofan() 
    turbofan.tag                                    = 'turbofan'
    turbofan.engine_length                          = 2.71     
    turbofan.bypass_ratio                           = 5.4   
    turbofan.design_altitude                        = 35000.0*Units.ft
    turbofan.design_mach_number                     = 0.78   
    turbofan.design_thrust                          = 37278.0* Units.N/2 
                  
    # fan                     
    fan                                             = RCAIDE.Energy.Propulsion.Converters.Fan()   
    fan.tag                                         = 'fan'
    fan.polytropic_efficiency                       = 0.93
    fan.pressure_ratio                              = 1.7   
    turbofan.fan                                    = fan        
                        
    # working fluid                        
    turbofan.working_fluid                          = RCAIDE.Attributes.Gases.Air() 
    ram                                             = RCAIDE.Energy.Propulsion.Converters.Ram()
    ram.tag                                         = 'ram' 
    turbofan.ram                                    = ram 
               
    # inlet nozzle               
    inlet_nozzle                                    = RCAIDE.Energy.Propulsion.Converters.Compression_Nozzle()
    inlet_nozzle.tag                                = 'inlet nozzle'
    inlet_nozzle.polytropic_efficiency              = 0.98
    inlet_nozzle.pressure_ratio                     = 0.98 
    turbofan.inlet_nozzle                           = inlet_nozzle


    # low pressure compressor    
    low_pressure_compressor                        = RCAIDE.Energy.Propulsion.Converters.Compressor()    
    low_pressure_compressor.tag                    = 'lpc'
    low_pressure_compressor.polytropic_efficiency  = 0.91
    low_pressure_compressor.pressure_ratio         = 1.9   
    turbofan.low_pressure_compressor               = low_pressure_compressor

    # high pressure compressor  
    high_pressure_compressor                       = RCAIDE.Energy.Propulsion.Converters.Compressor()    
    high_pressure_compressor.tag                   = 'hpc'
    high_pressure_compressor.polytropic_efficiency = 0.91
    high_pressure_compressor.pressure_ratio        = 10.0    
    turbofan.high_pressure_compressor              = high_pressure_compressor

    # low pressure turbine  
    low_pressure_turbine                           = RCAIDE.Energy.Propulsion.Converters.Turbine()   
    low_pressure_turbine.tag                       ='lpt'
    low_pressure_turbine.mechanical_efficiency     = 0.99
    low_pressure_turbine.polytropic_efficiency     = 0.93 
    turbofan.low_pressure_turbine                  = low_pressure_turbine
   
    # high pressure turbine     
    high_pressure_turbine                          = RCAIDE.Energy.Propulsion.Converters.Turbine()   
    high_pressure_turbine.tag                      ='hpt'
    high_pressure_turbine.mechanical_efficiency    = 0.99
    high_pressure_turbine.polytropic_efficiency    = 0.93 
    turbofan.high_pressure_turbine                 = high_pressure_turbine 
   
    # combustor     
    combustor                                      = RCAIDE.Energy.Propulsion.Converters.Combustor()   
    combustor.tag                                  = 'Comb'
    combustor.efficiency                           = 0.99 
    combustor.alphac                               = 1.0     
    combustor.turbine_inlet_temperature            = 1500
    combustor.pressure_ratio                       = 0.95
    combustor.fuel_data                            = RCAIDE.Attributes.Propellants.Jet_A()  
    turbofan.combustor                             = combustor
           
    # core nozzle           
    core_nozzle                                    = RCAIDE.Energy.Propulsion.Converters.Expansion_Nozzle()   
    core_nozzle.tag                                = 'core nozzle'
    core_nozzle.polytropic_efficiency              = 0.95
    core_nozzle.pressure_ratio                     = 0.99  
    core_nozzle.diameter                           = 0.92    
    turbofan.core_nozzle                           = core_nozzle
          
    # fan nozzle          
    fan_nozzle                                  = RCAIDE.Energy.Propulsion.Converters.Expansion_Nozzle()   
    fan_nozzle.tag                              = 'fan nozzle'
    fan_nozzle.polytropic_efficiency            = 0.95
    fan_nozzle.pressure_ratio                   = 0.99 
    fan_nozzle.diameter                         = 1.659
    turbofan.fan_nozzle                         = fan_nozzle 
    
    #design turbofan
    design_turbofan(turbofan) 
    
    # append turbofan to propulsor data class 
    starboard_propulsor.turbofan = turbofan 
    
    # append propulsor to distribution line 
    fuel_line.propulsors.append(starboard_propulsor)


    #------------------------------------------------------------------------------------------------------------------------------------  
    # Port Propulsor
    #------------------------------------------------------------------------------------------------------------------------------------     

    port_propulsor                         = RCAIDE.Energy.Propulsion.Propulsor() 
    
    # copy turbofan
    turbofan_2                             = deepcopy(turbofan)
    turbofan_2.tag                         = 'turbofan_2' 
    turbofan_2.origin                      = [[12.0,-4.38,-1.1]]  # change origin
    
    # append turbofan to propulsor data class 
    port_propulsor.turbofan                = turbofan_2 
    
    # append propulsor to distribution line 
    fuel_line.propulsors.append(port_propulsor)

    #------------------------------------------------------------------------------------------------------------------------------------     
    
    # Append fuel line to network      
    net.fuel_lines.append(fuel_line)        
    
    # Append energy network to aircraft 
    vehicle.append_energy_network(net)     
        
    return vehicle

# ---------------------------------------------------------------------
#   Define the Configurations
# ---------------------------------------------------------------------

def configs_setup(vehicle):
 
    
    # ------------------------------------------------------------------
    #   Initialize Configurations
    # ------------------------------------------------------------------

    configs     = RCAIDE.Components.Configs.Config.Container() 
    base_config = RCAIDE.Components.Configs.Config(vehicle)
    base_config.tag = 'base' 
    base_config.landing_gear.gear_condition                      = 'up'
    configs.append(base_config)

    # ------------------------------------------------------------------
    #   Cruise Configuration
    # ------------------------------------------------------------------

    config = RCAIDE.Components.Configs.Config(base_config)
    config.tag = 'cruise'
    configs.append(config)


    # ------------------------------------------------------------------
    #   Takeoff Configuration
    # ------------------------------------------------------------------

    config = RCAIDE.Components.Configs.Config(base_config)
    config.tag = 'takeoff'
    config.wings['main_wing'].control_surfaces.flap.deflection  = 20. * Units.deg
    config.wings['main_wing'].control_surfaces.slat.deflection  = 25. * Units.deg
    config.landing_gear.gear_condition                          = 'up'       
    config.V2_VS_ratio = 1.21
    configs.append(config)
    
    # ------------------------------------------------------------------
    #   Landing Configuration
    # ------------------------------------------------------------------

    config = RCAIDE.Components.Configs.Config(base_config)
    config.tag = 'landing'
    config.wings['main_wing'].control_surfaces.flap.deflection  = 30. * Units.deg
    config.wings['main_wing'].control_surfaces.slat.deflection  = 25. * Units.deg
    config.landing_gear.gear_condition                          = 'down'   
    config.Vref_VS_ratio = 1.23
    configs.append(config)   
     
    # ------------------------------------------------------------------
    #   Short Field Takeoff Configuration
    # ------------------------------------------------------------------ 

    config = RCAIDE.Components.Configs.Config(base_config)
    config.tag = 'short_field_takeoff'    
    config.wings['main_wing'].control_surfaces.flap.deflection  = 20. * Units.deg
    config.wings['main_wing'].control_surfaces.slat.deflection  = 25. * Units.deg
    config.landing_gear.gear_condition                          = 'down'   
    config.V2_VS_ratio = 1.21
    
    # payload?
    
    configs.append(config)    

    # done!
    return configs

 