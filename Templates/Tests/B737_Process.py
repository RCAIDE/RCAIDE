import RCAIDE.Framework as rcf
import RCAIDE.Library as rcl

from RCAIDE.Framework.System import VehicleEnvelope

from copy import deepcopy

import numpy as np


def vehicle_setup():

    # ------------------------------------------------------------------------------------------------------------------
    # Vehicle Level Parameters
    # ------------------------------------------------------------------------------------------------------------------

    vehicle = rcf.Aircraft(tag='Boeing 737')

    vehicle.areas.reference                     = 124.862 # m^2
    vehicle.passengers                          = 170

    vehicle.mass_properties.total               = 79015.8   # kg
    vehicle.mass_properties.max_takeoff         = 79015.8   # kg
    vehicle.mass_properties.takeoff             = 79015.8   # kg
    vehicle.mass_properties.operating_empty     = 62746.4   # kg
    vehicle.mass_properties.takeoff             = 79015.8   # kg
    vehicle.mass_properties.max_zero_fuel       = 62732.0   # kg
    vehicle.mass_properties.cargo               = 10000.0   # kg
    vehicle.mass_properties.center_of_gravity   = np.array(
                                                   [[15.30987849,   0.,             -0.48023939]])  # Estimated
    vehicle.mass_properties.moments_of_inertia  = np.array(
                                                   [[3173074.17,    0.,             28752.77565],
                                                   [0.,             3019041.443,    0],
                                                   [0.,             0.,             5730017.433]])

    vehicle.design_mach_number                  = 0.78
    vehicle.design_range                        = 3582
    vehicle.design_cruise_alt                   = 35000.0

    vehicle.envelope = VehicleEnvelope()
    vehicle.envelope.ultimate_load              = 3.75
    vehicle.envelope.limit_load                 = 1.5

    # ------------------------------------------------------------------------------------------------------------------
    # Main Wing
    # ------------------------------------------------------------------------------------------------------------------

    main_wing = rcl.Components.Wings.Wing(tag='Main Wing')

    main_wing.aspect_ratio            = 10.18
    main_wing.sweeps.quarter_chord    = np.deg2rad(25.)
    main_wing.thickness_to_chord      = 0.1
    main_wing.taper                   = 0.1

    main_wing.spans.projected         = 34.32

    main_wing.chords.root             = 7.760
    main_wing.chords.tip              = 0.782
    main_wing.chords.mean_aerodynamic = 4.235

    main_wing.areas.reference         = 124.862
    main_wing.areas.wetted            = 225.08

    main_wing.twists.root             = np.deg2rad(4.0)
    main_wing.twists.tip              = np.deg2rad(0.0)

    main_wing.origin                  = np.array([[13.61, 0., -0.93]])
    main_wing.aerodynamic_center      = np.array([0, 0, 0])

    main_wing.vertical                = False
    main_wing.symmetric               = True
    main_wing.high_lift               = True

    main_wing.dynamic_pressure_ratio  = 1.0

    # Root Segment

    root_segment = rcl.Components.Wings.WingSegment(tag='Main Wing Root Segment')

    root_segment.percent_span_location      = 0.0
    root_segment.twist                      = np.deg2rad(4.)
    root_segment.root_chord_percent         = 1.
    root_segment.thickness_to_chord         = 0.1
    root_segment.dihedral_outboard          = np.deg2rad(2.5)
    root_segment.sweeps.quarter_chord       = np.deg2rad(28.225)
    root_segment.thickness_to_chord         = .1

    # root_segment.airfoil = rcl.Components.Airfoil.from_file(rcl.Components.Airfoil_Data/'B737a.txt')

    main_wing.add_segment(root_segment)

    # Yehudi Segment

    yehudi_segment = rcl.Components.Wings.WingSegment(tag='Main Wing Yehudi Segment')

    yehudi_segment.percent_span_location    = 0.324
    yehudi_segment.twist                    = np.deg2rad(0.047193)
    yehudi_segment.root_chord_percent       = 0.5
    yehudi_segment.thickness_to_chord       = 0.1
    yehudi_segment.dihedral_outboard        = np.deg2rad(5.5)
    yehudi_segment.sweeps.quarter_chord     = np.deg2rad(25.)
    yehudi_segment.thickness_to_chord       = .1

    # yehudi_segment.airfoil = rcl.Components.Airfoil.from_file(rcl.Components.Airfoil_Data/'B737b.txt')

    main_wing.add_segment(yehudi_segment)

    # Mid Segment

    mid_segment = rcl.Components.Wings.WingSegment(tag='Main Wing Mid Segment')

    mid_segment.percent_span_location       = 0.963
    mid_segment.twist                       = np.deg2rad(0.00258)
    mid_segment.root_chord_percent          = 0.220
    mid_segment.thickness_to_chord          = 0.1
    mid_segment.dihedral_outboard           = np.deg2rad(5.5)
    mid_segment.sweeps.quarter_chord        = np.deg2rad(56.75)
    mid_segment.thickness_to_chord          = .1

    # mid_segment.airfoil = rcl.Components.Airfoil.from_file(rcl.Components.Airfoil_Data/'B737c.txt')

    main_wing.add_segment(mid_segment)

    # Tip Segment

    tip_segment = rcl.Components.Wings.WingSegment(tag='Main Wing Tip Segment')

    tip_segment.percent_span_location         = 1.
    tip_segment.twist                         = np.deg2rad(0.)
    tip_segment.root_chord_percent            = 0.10077
    tip_segment.thickness_to_chord            = 0.1
    tip_segment.dihedral_outboard             = 0.
    tip_segment.sweeps.quarter_chord          = 0.
    tip_segment.thickness_to_chord            = .1

    # tip_segment.airfoil = rcl.Components.Airfoil.from_file(rcl.Components.Airfoil_Data/'B737d.txt')

    main_wing.add_segment(tip_segment)

    # Control Surfaces

    slat = rcl.Components.Wings.WingControlSurface(tag='Slat')

    slat.span_fraction_start    = 0.2
    slat.span_fraction_end      = 0.963
    slat.deflection             = 0.0
    slat.chord_fraction         = 0.075
    slat.hinge_fraction         = 1.0

    main_wing.control_surfaces.add_subcomponent(slat)

    flap = rcl.Components.Wings.WingControlSurface(tag='Flap')

    flap.span_fraction_start    = 0.2
    flap.span_fraction_end      = 0.7
    flap.deflection             = 0.0
    flap.configuration_type     = 'double_slotted'
    flap.chord_fraction         = 0.30

    main_wing.control_surfaces.add_subcomponent(flap)

    aileron = rcl.Components.Wings.WingControlSurface(tag='Aileron')

    aileron.span_fraction_start = 0.7
    aileron.span_fraction_end   = 0.963
    aileron.deflection          = 0.0
    aileron.chord_fraction      = 0.16
    aileron.sign_duplicate      = -1.0

    main_wing.control_surfaces.add_subcomponent(aileron)

    vehicle.add_subcomponent(main_wing)

    # ------------------------------------------------------------------------------------------------------------------
    # Horizontal Stabilizer
    # ------------------------------------------------------------------------------------------------------------------

    h_stab = rcl.Components.Wings.Wing(tag='Horizontal Stabilizer')

    h_stab.aspect_ratio            = 4.99
    h_stab.sweeps.quarter_chord    = np.deg2rad(28.2250)
    h_stab.thickness_to_chord      = 0.08
    h_stab.taper                   = 0.3333

    h_stab.spans.projected         = 14.4

    h_stab.chords.root             = 4.2731
    h_stab.chords.tip              = 1.4243
    h_stab.chords.mean_aerodynamic = 8.0

    h_stab.areas.reference         = 41.49
    h_stab.areas.exposed           = 59.354    # Exposed area of the horizontal tail
    h_stab.areas.wetted            = 71.81     # Wetted area of the horizontal tail
    h_stab.twists.root             = np.deg2rad(3.0)
    h_stab.twists.tip              = np.deg2rad(3.0)

    h_stab.origin                  = np.array([[33.02, 0, 1.466]])
    h_stab.aerodynamic_center      = np.array([0, 0, 0])

    h_stab.vertical                = False
    h_stab.symmetric               = True

    h_stab.dynamic_pressure_ratio  = 0.9

    # H-Stab Segments

    root_segment = rcl.Components.Wings.WingSegment(tag='Horizontal Stabilizer Root Segment')

    root_segment.percent_span_location  = 0.0
    root_segment.twist                  = 0.
    root_segment.root_chord_percent     = 1.0
    root_segment.dihedral_outboard      = np.deg2rad(8.63)
    root_segment.sweeps.quarter_chord   = np.deg2rad(28.2250 )
    root_segment.thickness_to_chord     = .1
    h_stab.add_segment(root_segment)

    tip_segment = rcl.Components.Wings.WingSegment(tag='Horizontal Stabilizer Tip Segment')

    tip_segment.percent_span_location  = 1.
    tip_segment.twist                  = 0.
    tip_segment.root_chord_percent     = 0.3333
    tip_segment.dihedral_outboard      = 0.
    tip_segment.sweeps.quarter_chord   = 0.
    tip_segment.thickness_to_chord     = .1
    h_stab.add_segment(tip_segment)

    # H-Stab Elevator

    elevator                       = rcl.Components.Wings.WingControlSurface(tag='Elevator')

    elevator.span_fraction_start   = 0.09
    elevator.span_fraction_end     = 0.92
    elevator.deflection            = 0.0
    elevator.chord_fraction        = 0.3
    h_stab.control_surfaces.add_subcomponent(elevator)

    # Add H-Stab to vehicle
    h_stab.make_segmented_planform()
    vehicle.add_subcomponent(h_stab)

    # ------------------------------------------------------------------------------------------------------------------
    # Vertical Stabilizer
    # ------------------------------------------------------------------------------------------------------------------

    v_stab = rcl.Components.Wings.Wing(tag='Vertical Stabilizer')

    v_stab.aspect_ratio            = 1.98865
    v_stab.sweeps.quarter_chord    = 31.2
    v_stab.thickness_to_chord      = 0.08
    v_stab.taper                   = 0.1183

    v_stab.spans.projected         = 8.33
    v_stab.total_length            = v_stab.spans.projected

    v_stab.chords.root             = 10.1
    v_stab.chords.tip              = 1.20
    v_stab.chords.mean_aerodynamic = 4.0

    v_stab.areas.reference         = 34.89
    v_stab.areas.wetted            = 57.25

    v_stab.twists.root             = 0.0
    v_stab.twists.tip              = 0.0

    v_stab.origin                  = np.array([[26.944, 0, 1.54]])
    v_stab.aerodynamic_center      = np.array([0, 0, 0])

    v_stab.vertical                = True
    v_stab.symmetric               = False
    v_stab.t_tail                  = False

    v_stab.dynamic_pressure_ratio  = 1.0

    # V-Stab Segments
    root_segment = rcl.Components.Wings.WingSegment(tag='Vertical Stabilizer Root Segment')

    root_segment.percent_span_location   = 0.0
    root_segment.twist                   = 0.
    root_segment.root_chord_percent      = 1.
    root_segment.dihedral_outboard       = 0.
    root_segment.sweeps.quarter_chord    = 61.485
    root_segment.thickness_to_chord      = .1
    v_stab.add_segment(root_segment)

    mid_segment = rcl.Components.Wings.WingSegment(tag='Vertical Stabilizer Mid Segment')

    mid_segment.percent_span_location   = 0.2962
    mid_segment.twist                   = 0.
    mid_segment.root_chord_percent      = 0.45
    mid_segment.dihedral_outboard       = 0.
    mid_segment.sweeps.quarter_chord    = np.deg2rad(31.2)
    mid_segment.thickness_to_chord      = .1
    v_stab.add_segment(mid_segment)

    tip_segment = rcl.Components.Wings.WingSegment(tag='Vertical Stabilizer Tip Segment')

    tip_segment.percent_span_location   = 1.0
    tip_segment.twist                   = 0.
    tip_segment.root_chord_percent      = 0.1183
    tip_segment.dihedral_outboard       = 0.0
    tip_segment.sweeps.quarter_chord    = 0.0
    tip_segment.thickness_to_chord      = .1
    v_stab.add_segment(tip_segment)

    # Add V-Stab to vehicle
    v_stab.make_segmented_planform()
    vehicle.add_subcomponent(v_stab)

    # ------------------------------------------------------------------------------------------------------------------
    # Fuselage
    # ------------------------------------------------------------------------------------------------------------------

    fuse = rcl.Components.Fuselage(tag='Fuselage')

    fuse.seats          = vehicle.passengers
    fuse.seats_abreast  = 6
    fuse.seat_pitch     = 0.7874

    fuse.fineness.nose = 1.6
    fuse.fineness.tail = 2.

    fuse.lengths.nose       = 6.4
    fuse.lengths.tail       = 8.0
    fuse.lengths.cabin      = 28.85
    fuse.lengths.total      = 38.02
    fuse.lengths.fore_space = 6.
    fuse.lengths.aft_space  = 5.

    fuse.widths.maximum = 3.74

    fuse.diameters.effective = 3.74

    fuse.heights.maximum = 3.74
    fuse.heights.at_quarter_length = 3.74
    fuse.heights.at_three_quarters_length = 3.65
    fuse.heights.at_wing_root_quarter_chord = 3.74

    fuse.areas.side_projected = 142.1948
    fuse.areas.wetted = 385.51
    fuse.areas.front_projected = 12.57

    fuse.effective_diameter = 3.74

    fuse.differential_pressure = 5.0e4

    # Fuselage Segments

    segment_specs = [
        # %X      %Z        Height   Width
        (0.00000, -0.00144, 0.01000, 0.01000),
        (0.00576, -0.00144, 0.75000, 0.65000),
        (0.02017,  0.00000, 1.52783, 1.20043),
        (0.03170,  0.00000, 1.96435, 1.52783),
        (0.04899,  0.00431, 2.72826, 1.96435),
        (0.07781,  0.00861, 3.49217, 2.61913),
        (0.10375,  0.01005, 3.70130, 3.05565),
        (0.16427,  0.01148, 3.92870, 3.92870),
        (0.69164,  0.01292, 3.81957, 3.81957),
        (0.71758,  0.01292, 3.81957, 3.81957),
        (0.78098,  0.01722, 3.49217, 3.71043),
        (0.85303,  0.02296, 3.05565, 3.16478),
        (0.91931,  0.03157, 2.40087, 1.96435),
        (1.00000,  0.04593, 1.09130, 0.21826)
    ]

    for idx, (x, z, h, w) in enumerate(segment_specs):
        segment = rcl.Components.Fuselages.FuselageSegment(tag=f'Fuselage Segment {idx}')
        segment.percent_x_location  = x
        segment.percent_z_location  = z
        segment.heights.maximum     = h
        segment.widths.maximum      = w

    vehicle.add_subcomponent(fuse)

    # ------------------------------------------------------------------------------------------------------------------
    # Landing Gear
    # ------------------------------------------------------------------------------------------------------------------

    mlg = rcl.Components.LandingGear(tag='Main Landing Gear')
    mlg.number_of_wheels    = 2
    mlg.tire_diameter       = 1.12
    mlg.strut_length        = 1.8

    vehicle.add_subcomponent(mlg)

    nlg = rcl.Components.LandingGear(tag='Nose Landing Gear')
    nlg.number_of_wheels    = 2
    nlg.tire_diameter       = 1.12
    nlg.strut_length        = 1.3

    vehicle.add_subcomponent(nlg)

    # ------------------------------------------------------------------------------------------------------------------
    # Nacelles
    # ------------------------------------------------------------------------------------------------------------------

    nacelle = rcl.Components.Nacelle(tag='Engine Nacelle 1')
    nacelle.flow_through = True
    # nacelle.airfoil = rcl.Components.Airfoils.Airfoil.NACA_4_Series('2410')

    nacelle.origin = np.array([[13.72, -4.86, -1.9]])

    nacelle.lengths.total = 2.71

    nacelle.diameters.maximum   = 2.05
    nacelle.diameters.inlet     = 1.90

    nacelle.areas.wetted = 1.1 * np.pi * nacelle.diameters.maximum * nacelle.lengths.total

    nacelle_2 = deepcopy(nacelle)
    nacelle_2.name = 'Engine Nacelle 2'
    nacelle_2.origin = np.array([[13.72, 4.86, -1.9]])

    vehicle.add_subcomponent(nacelle)
    vehicle.add_subcomponent(nacelle_2)

    # ------------------------------------------------------------------------------------------------------------------
    # Turbofan Engines
    # ------------------------------------------------------------------------------------------------------------------

    vehicle.energy.lines.add_subcomponent(rcl.Components.Energy.Lines.Jets.TurbofanEnergyLine())

    tf          = rcl.Components.Energy.Propulsors.TurbofanEngine()
    tf.name     = 'Engine 1'
    tf.origin   = nacelle.origin

    tf.bypass_ratio                                     = 5.4
    tf.engine_length                                    = nacelle.lengths.total
    tf.plug_diameter                                    = 0.1

    tf.heights.above_ground                             = 0.5

    tf.design_thrust_parameters.total_thrust            = 24000.
    tf.design_thrust_parameters.altitude                = 10668.
    tf.design_thrust_parameters.mach_number             = 0.78

    # Inlet Nozzle
    tf.converters.inlet_nozzle.polytropic_efficiency    = 0.98
    tf.converters.inlet_nozzle.pressure_ratio           = 0.98

    # Fan
    tf.converters.fan.polytropic_efficiency             = 0.93
    tf.converters.fan.pressure_ratio                    = 1.7

    # Low Pressure Compressor
    tf.converters.compressors[0].polytropic_efficiency  = 0.91
    tf.converters.compressors[0].pressure_ratio         = 1.14

    # High Pressure Compressor
    tf.converters.compressors[1].polytropic_efficiency  = 0.91
    tf.converters.compressors[1].pressure_ratio         = 13.415

    # Combustor
    tf.converters.combustor.efficiency                  = 0.99
    tf.converters.combustor.pressure_ratio              = 0.95

    # Low Pressure Turbine

    tf.converters.turbines[0].mechanical_efficiency     = 0.91
    tf.converters.turbines[0].polytropic_efficiency     = 0.93

    # High Pressure Turbine
    tf.converters.turbines[1].mechanical_efficiency     = 0.99
    tf.converters.turbines[1].polytropic_efficiency     = 0.93

    # Core Nozzle
    tf.converters.core_nozzle.polytropic_efficiency     = 0.95
    tf.converters.core_nozzle.pressure_ratio            = 0.99
    tf.converters.core_nozzle.diameters.reference       = 0.92

    # Fan Nozzle
    tf.converters.fan_nozzle.polytropic_efficiency      = 0.95
    tf.converters.fan_nozzle.pressure_ratio             = 0.99
    tf.converters.fan_nozzle.diameters.reference        = 1.659

    tf2 = deepcopy(tf)
    tf2.name    = 'Engine 2'
    tf2.origin  = nacelle_2.origin

    vehicle.energy.lines[0].converters.add_subcomponent(tf)
    vehicle.energy.lines[0].converters.add_subcomponent(tf2)

    # ------------------------------------------------------------------------------------------------------------------
    # Fuel Tanks
    # ------------------------------------------------------------------------------------------------------------------

    fuel = rcl.Components.Energy.Stores.FuelTank()
    fuel.origin = main_wing.mass_properties.center_of_gravity

    fuel.mass_properties.full_fuel_mass = vehicle.mass_properties.max_takeoff - vehicle.mass_properties.max_zero_fuel
    fuel.mass_properties.center_of_gravity = main_wing.aerodynamic_center

    vehicle.energy.lines[0].stores.add_subcomponent(fuel)

    # ------------------------------------------------------------------------------------------------------------------
    # Configurations
    # ------------------------------------------------------------------------------------------------------------------

    # Takeoff Configuration

    takeoff_config = deepcopy(vehicle)
    takeoff_config.tag = "Takeoff"
    takeoff_config.wings.main_wing.control_surfaces.flap.deflection    = np.deg2rad(20)
    takeoff_config.wings.main_wing.control_surfaces.slat.deflection    = np.deg2rad(25)

    for tf in takeoff_config.energy.lines[0].converters:

        tf: rcl.Components.Energy.Propulsors.TurbofanEngine
        tf.converters.fan.rotation_speed        = 2780.
        tf.converters.fan_nozzle.noise_speed    = 315.
        tf.converters.core_nozzle.noise_speed   = 415.

    vehicle.configurations.add_subcomponent(takeoff_config)

    # Cutback Configuration

    cutback_config = deepcopy(vehicle)
    cutback_config.tag = "Cutback"
    cutback_config.wings.main_wing.control_surfaces.flap.deflection    = np.deg2rad(20)
    cutback_config.wings.main_wing.control_surfaces.slat.deflection    = np.deg2rad(20)

    for tf in cutback_config.energy.lines[0].converters:

        tf: rcl.Components.Energy.Propulsors.TurbofanEngine
        tf.converters.fan.rotation_speed        = 2780.
        tf.converters.fan_nozzle.noise_speed    = 210.
        tf.converters.core_nozzle.noise_speed   = 360.

    vehicle.configurations.add_subcomponent(cutback_config)

    # Landing Configuration

    landing_config = deepcopy(vehicle)
    landing_config.tag = "Landing"
    landing_config.wings.main_wing.control_surfaces.flap.deflection    = np.deg2rad(30)
    landing_config.wings.main_wing.control_surfaces.slat.deflection    = np.deg2rad(25)

    landing_config.landing_gear.main_landing_gear.deployed = True
    landing_config.landing_gear.main_landing_gear.deployed = True

    for tf in landing_config.energy.lines[0].converters:

        tf: rcl.Components.Energy.Converters.TurbofanEngine
        tf.converters.fan.rotation_speed        = 2030.
        tf.converters.fan_nozzle.noise_speed    = 109.3
        tf.converters.core_nozzle.noise_speed   = 92.

    vehicle.configurations.add_subcomponent(landing_config)

    return vehicle


def mission_setup(settings: "rcf.Settings"):

    mission  = rcf.Process(
        tag='Boeing 737 Mission',

        steps=[
            rcf.Missions.Segments.TestCSACruise(
                altitude=10000.0,
                air_speed=230.0,
                distance=(5500. * 1000.),
            )
        ]
    )

    for segment in mission.steps:

        segment: rcf.Missions.Segment
        analysis = segment.analyze

        analysis['Aerodynamics']    = rcf.Analyses.Aerodynamics.TestAero(settings=settings)

    return mission


def state_setup():

    state = rcf.State()

    state.freestream.atmosphere = rcl.Atmospheres.USStandard1976()

    state.initials = state

    return state


def mission_b737():

    # Initialize State

    state = state_setup()

    # Initialize System from Vehicle Setup
    system      = vehicle_setup()

    # Initialize Settings
    settings    = rcf.Settings()

    mission             = mission_setup(settings)
    mission.state       = state
    mission.system      = system
    mission.settings    = settings

    final_state, final_system, final_settings = mission.run()

    return final_state, final_system, final_settings


if __name__ == '__main__':
    st, sy, se = mission_b737()