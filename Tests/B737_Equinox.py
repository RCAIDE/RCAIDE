# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------

import time
import dataclasses as dc

import jax
from jax import value_and_grad, jit

import equinox as eqx
import jax.numpy as jnp

from RCAIDE.Framework import State, System, Settings, Process, ProcessStep
from RCAIDE.Framework.Missions.Conditions import Numerics
from RCAIDE.Framework.System import Aircraft, VehicleEnvelope, AircraftMassProperties
from RCAIDE.Framework.Missions.Segments import Segment
from RCAIDE.Framework.Missions.Segments.Profiles import (ConstantAltitude, AltitudeChange,  # Position Profiles
                                                         ConstantSpeed,  # Speed Profiles
                                                         ConstantAltitudeChangeRate,  # Velocity Profiles
                                                         FixedDistance, FixedTime,)  # Duration Profiles
from RCAIDE.Framework.Missions.Conditions.Controls import DirectControlVariable
from RCAIDE.Framework.Analyses.Aerodynamics import TestAero, VLM, VLMSettings, VLMVortices, InitializeVLM
from RCAIDE.Framework.Plotting import plot_vlm_panels

from RCAIDE.Library import Units
from RCAIDE.Library.Components import ComponentAreas, Airfoil, Airfoil_Data
from RCAIDE.Library.Components.Wings import Wing, WingChords, WingControlSurface, WingDimensions, WingSegment, WingSweeps
from RCAIDE.Library.Components.Fuselages import *
from RCAIDE.Library.Components.Landing_Gear import LandingGear
from RCAIDE.Library.Components.Nacelles import Nacelle, NacelleDiameters
from RCAIDE.Library.Components.Energy.Propulsors import TurbofanEngine, DesignParameters
from RCAIDE.Library.Components.Energy.Stores import FuelTank, FuelTankMass
from RCAIDE.Library.Components.Energy.Lines.Jets import TurbofanEnergyLine

from RCAIDE.Library.Atmospheres import USStandard1976
# ----------------------------------------------------------------------------------------------------------------------
# Boeing 737 New Process
# ----------------------------------------------------------------------------------------------------------------------


def vehicle_setup():

    # ------------------------------------------------------------------------------------------------------------------
    # Vehicle Level Parameters
    # ------------------------------------------------------------------------------------------------------------------

    mass_props = AircraftMassProperties(
        total=79015.8 * Units.kg,
        max_takeoff=79015.8 * Units.kg,
        takeoff=79015.8 * Units.kg,
        operating_empty=62746.4 * Units.kg,
        max_zero_fuel=62732.0 * Units.kg,
        cargo=10000.0 * Units.kg,
        center_of_gravity=jnp.array([[15.30987849,   0.,             -0.48023939]]),  # Estimated
        moments_of_inertia=jnp.array([[3173074.17,    0.,             28752.77565],
                                      [0.,             3019041.443,    0],
                                      [0.,             0.,             5730017.433]])
    )

    vehicle = Aircraft(
        tag='Boeing 737',
        passengers=170,
        mass_properties=mass_props,
        areas=ComponentAreas(reference=124.862),
        envelope=VehicleEnvelope(ultimate_load_factor=3.75, limit_load_factor=1.5),
        design_mach_number=0.78,
        design_range=3582,
        design_cruise_alt=35000.0,
    )

    # ------------------------------------------------------------------------------------------------------------------
    # Main Wing
    # ------------------------------------------------------------------------------------------------------------------

    # Segments ---------------------------------------------------------------------------------------------------------

    # Root Segment
    root_segment = WingSegment(
        tag='Main Wing Root Segment',
        percent_span_location   =0.0,
        twist                   =4. * Units.deg,
        root_chord_percent      =1.,
        thickness_to_chord      =0.1,
        dihedral_outboard       =2.5 * Units.deg,
        sweeps                  =WingSweeps(quarter_chord=28.225 * Units.deg),
        airfoil                 =Airfoil.from_file(Airfoil_Data/'B737a.txt'))

    yehudi_segment = WingSegment(
        tag='Main Wing Yehudi Segment',
        percent_span_location=0.324,
        twist=0.047193 * Units.deg,
        root_chord_percent=0.5,
        thickness_to_chord=0.1,
        dihedral_outboard=5.5 * Units.deg,
        sweeps=WingSweeps(quarter_chord=25. * Units.deg),
        airfoil=Airfoil.from_file(Airfoil_Data/'B737b.txt'))

    mid_segment = WingSegment(
        tag='Main Wing Mid Segment',
        percent_span_location=0.963,
        twist=0.00258 * Units.deg,
        root_chord_percent=0.220,
        thickness_to_chord=0.1,
        dihedral_outboard=5.5 * Units.deg,
        sweeps=WingSweeps(quarter_chord=56.75 * Units.deg),
        airfoil=Airfoil.from_file(Airfoil_Data/'B737c.txt'))

    tip_segment = WingSegment(
        tag='Main Wing Tip Segment',
        percent_span_location=1.,
        root_chord_percent=0.10077,
        thickness_to_chord=0.1,
        airfoil=Airfoil.from_file(Airfoil_Data/'B737d.txt'))

    # Control Surfaces -------------------------------------------------------------------------------------------------

    slat = WingControlSurface(
        tag='Slat',
        span_fraction_start=0.2,
        span_fraction_end=0.963,
        deflection=0.0,
        root_chord_percent=0.075,
        hinge_fraction=1.0)

    flap = WingControlSurface(
        tag='Flap',
        span_fraction_start=0.2,
        span_fraction_end=0.7,
        deflection=0.0,
        configuration_type='double_slotted',
        root_chord_percent=0.30)

    aileron = WingControlSurface(
        tag='Aileron',
        span_fraction_start=0.7,
        span_fraction_end=0.963,
        deflection=0.0,
        root_chord_percent=0.16,
        sign_duplicate=-1.0)

    # Wing Properties --------------------------------------------------------------------------------------------------
    main_wing = Wing(
        tag='Main Wing',
        aspect_ratio=10.18,
        thickness_to_chord=0.1,
        origin=jnp.array([[13.61, 0., -0.93]]),
        aerodynamic_center=jnp.array([0, 0, 0]),
        vertical=False,
        symmetric=True,
        high_lift=True,
        dynamic_pressure_ratio=1.0,
        sweeps=WingSweeps(quarter_chord=25. * Units.deg),
        spans=WingDimensions(projected=34.32),
        chords=WingChords(root=7.760, tip=0.782, mean_aerodynamic=4.235),
        areas=ComponentAreas(reference=124.862, wetted=225.08),
        twists=WingDimensions(root=4.0 * Units.deg, tip=0.0 * Units.deg),
        segments=(root_segment, yehudi_segment, mid_segment, tip_segment),
        control_surfaces=Component(
            tag="Main Wing Control Surfaces",
            subcomponents=(slat, flap, aileron))
    ).update_geometry()
    
    vehicle = vehicle.add_subcomponent(main_wing)

    # ------------------------------------------------------------------------------------------------------------------
    # Horizontal Stabilizer
    # ------------------------------------------------------------------------------------------------------------------

    # H-Stab Segments --------------------------------------------------------------------------------------------------
    h_root_segment = WingSegment(
        tag="Main Wing Root Segment",
        thickness_to_chord=0.1,
        percent_span_location=0.0,
        root_chord_percent=1.0,
        dihedral_outboard=8.63 * Units.deg,
        sweeps=WingSweeps(quarter_chord=28.2250 * Units.deg))

    h_tip_segment = WingSegment(
        tag='Horizontal Stabilizer Tip Segment',
        percent_span_location =1.,
        root_chord_percent=0.3333,
        thickness_to_chord=.1)

    # H-Stab Controls  -------------------------------------------------------------------------------------------------

    elevator = WingControlSurface(
        tag='Elevator',
        span_fraction_start=0.09,
        span_fraction_end=0.92,
        deflection=0.0,
        root_chord_percent=0.3)

    # H-Stab Properties  -----------------------------------------------------------------------------------------------
    h_stab = Wing(
        tag='Horizontal Stabilizer',
        aspect_ratio            =4.99,
        thickness_to_chord      =0.08,
        taper                   =0.3333,
        dynamic_pressure_ratio  =0.9,
        origin                  =jnp.array([[33.02, 0, 1.466]]),
        aerodynamic_center      =jnp.array([0, 0, 0]),
        vertical                =False,
        symmetric               =True,
        sweeps                  =WingSweeps(quarter_chord=28.2250 * Units.deg),
        spans                   =WingDimensions(projected=14.4),
        chords                  =WingChords(root=4.2731, tip=1.4243, mean_aerodynamic=8.0),
        areas                   =ComponentAreas(reference=41.49, exposed=59.354, wetted=71.81),
        twists                  =WingDimensions(root=3.0 * Units.deg, tip=3.0 * Units.deg),
        # control_surfaces        =Component("Horizontal Stabilizer Controls", subcomponents=(elevator,)),
        segments                =(h_root_segment, h_tip_segment)).update_geometry()

    vehicle = vehicle.add_subcomponent(h_stab)

    # ------------------------------------------------------------------------------------------------------------------
    # Vertical Stabilizer
    # ------------------------------------------------------------------------------------------------------------------
    
    # V-Stab Segments --------------------------------------------------------------------------------------------------

    root_segment = WingSegment(
        tag='Vertical Stabilizer Root Segment',
        percent_span_location=0.0,
        root_chord_percent=1.,
        thickness_to_chord=.1,
        sweeps=WingSweeps(quarter_chord=61.485 * Units.deg))

    mid_segment = WingSegment(
        tag='Vertical Stabilizer Mid Segment',
        percent_span_location=0.2962,
        root_chord_percent=0.45,
        sweeps=WingSweeps(quarter_chord=31.2 * Units.deg),
        thickness_to_chord=.1,)

    tip_segment = WingSegment(
        tag='Vertical Stabilizer Tip Segment',
        percent_span_location=1.0,
        root_chord_percent=0.1183,
        thickness_to_chord=.1,)

    # V-Stab Properties ------------------------------------------------------------------------------------------------
    v_stab = Wing(
        tag='Vertical Stabilizer',
        aspect_ratio            =1.98865,
        thickness_to_chord      =0.08,
        taper                   =0.1183,
        origin                  =jnp.array([[26.944, 0, 1.54]]),
        aerodynamic_center      =jnp.array([0, 0, 0]),
        vertical                =True,
        symmetric               =False,
        t_tail                  =False,
        dynamic_pressure_ratio  =1.0,
        sweeps                  =WingSweeps(quarter_chord=32.2 * Units.deg),
        spans                   =WingDimensions(projected=8.33),
        chords                  =WingChords(root=10.1, tip=1.20, mean_aerodynamic=4.0),
        areas                   =ComponentAreas(reference=34.89, wetted=57.25),
        segments=(root_segment, mid_segment, tip_segment)).update_geometry()

    vehicle = vehicle.add_subcomponent(v_stab)
    
    # ------------------------------------------------------------------------------------------------------------------
    # Fuselage
    # ------------------------------------------------------------------------------------------------------------------

    # Fuselage Segments ------------------------------------------------------------------------------------------------

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

    f_segments = []
    for idx, (x, z, h, w) in enumerate(segment_specs):
        f_segments.append(FuselageSegment(
            tag=f'Fuselage Segment {idx}',
            percent_x_location=x,
            percent_z_location=z,
            heights=ComponentDimensions(maximum=h),
            widths=ComponentDimensions(maximum=w)))

    # Fuselage Properties ----------------------------------------------------------------------------------------------
    fuse = Fuselage(
        tag='Fuselage',
        number_of_seats=170,
        seats_abreast=6,
        seat_pitch=0.7874,
        differential_pressure=5.0e4,
        diameters=ComponentDimensions(effective=3.74),
        fineness=ComponentFineness(nose=1.6, tail=2.),
        lengths=FuselageLengths(nose=6.4, tail=8.0, cabin=28.85, total=38.02, fore_space=6., aft_space=5.),
        widths=ComponentDimensions(maximum=3.74),
        heights=FuselageHeights(maximum=3.74,
                                quarter_length=3.74,
                                three_quarters_length=3.65,
                                wing_root_quarter_chord=3.74),
        areas=ComponentAreas(side_projected=142.1948, wetted=385.51, front_projected=12.57),
        segments=tuple(f_segments)
    )

    vehicle = vehicle.add_subcomponent(fuse)

    # ------------------------------------------------------------------------------------------------------------------
    # Landing Gear
    # ------------------------------------------------------------------------------------------------------------------

    mlg = LandingGear(tag='Main Landing Gear', number_of_wheels=2, tire_diameter=1.12, strut_length=1.8)
    nlg = LandingGear(tag='Nose Landing Gear', number_of_wheels=2, tire_diameter=1.12, strut_length=1.3)

    vehicle.add_subcomponent(mlg)
    vehicle.add_subcomponent(nlg)

    # ------------------------------------------------------------------------------------------------------------------
    # Nacelles
    # ------------------------------------------------------------------------------------------------------------------
    nacelle = Nacelle(
        tag='Engine Nacelle 1',
        flow_through= True,
        airfoil=Airfoil.NACA_4_Series('2410'),
        origin= jnp.array([[13.72, -4.86, -1.9]]),
        lengths=ComponentDimensions(total=2.71),
        diameters=NacelleDiameters(maximum=2.05, inlet=1.90),
        areas=ComponentAreas(wetted=1.1 * jnp.pi * 2.05 * 2.71)
    )

    nacelle_2 = dc.replace(nacelle, tag="Engine Nacelle 2", origin=jnp.array([[13.72, 4.86, -1.9]]))

    vehicle = vehicle.add_subcomponent(nacelle)
    vehicle = vehicle.add_subcomponent(nacelle_2)

    # ------------------------------------------------------------------------------------------------------------------
    # Turbofan Engines
    # ------------------------------------------------------------------------------------------------------------------

    # Energy Line ------------------------------------------------------------------------------------------------------
    vehicle = eqx.tree_at(lambda v: v.energy.lines, vehicle, vehicle.energy.lines.add_subcomponent(TurbofanEnergyLine()))

    # Engine -----------------------------------------------------------------------------------------------------------
    tf = TurbofanEngine(
        tag="Engine 1",
        origin=jnp.array([[13.72, -4.86, -1.9]]),
        bypass_ratio=5.4,
        plug_diameter=0.1,
        lengths=ComponentDimensions(total=2.71),
        design_thrust_parameters=DesignParameters(total_thrust=24000., altitude=10668., mach_number=0.78),
    )

    # Converters -------------------------------------------------------------------------------------------------------
    
    cons        = tf.converters

    # Direct Replacement
    cons = eqx.tree_at(
        lambda c: (
                c.inlet_nozzle.polytropic_efficiency, c.inlet_nozzle.pressure_ratio,
                c.fan.polytropic_efficiency, c.fan.pressure_ratio,
                c.compressors.low_pressure_compressor.polytropic_efficiency, c.compressors.low_pressure_compressor.pressure_ratio,
                c.compressors.high_pressure_compressor.polytropic_efficiency, c.compressors.high_pressure_compressor.pressure_ratio,
                c.turbines.high_pressure_turbine.polytropic_efficiency, c.turbines.high_pressure_turbine.mechanical_efficiency,
                c.turbines.low_pressure_turbine.polytropic_efficiency, c.turbines.low_pressure_turbine.mechanical_efficiency,
                c.core_nozzle.polytropic_efficiency, c.core_nozzle.pressure_ratio, c.core_nozzle.diameters.reference,
                c.fan_nozzle.polytropic_efficiency, c.fan_nozzle.pressure_ratio, c.fan_nozzle.diameters.reference,
            ),
            cons,
            (
                0.98, 0.98,
                0.93, 1.7,
                0.91, 1.14,
                0.91, 13.415,
                0.93, 0.91,
                0.99, 0.93,
                0.95, 0.99, 0.92,
                0.95, 0.99, 1.659
             )
        )

    # Engine & Line Rebuild --------------------------------------------------------------------------------------------

    tf = dc.replace(tf, converters=cons)
    tf2 = dc.replace(tf, tag="Engine 2", origin=jnp.array([[13.72, 4.86, -1.9]]))

    line_cons = vehicle.energy.lines[0].converters
    line_cons = line_cons.add_subcomponent(tf)
    line_cons = line_cons.add_subcomponent(tf2)

    vehicle = eqx.tree_at(lambda v: v.energy.lines[0].converters, vehicle, line_cons)

    # ------------------------------------------------------------------------------------------------------------------
    # Fuel Tanks
    # ------------------------------------------------------------------------------------------------------------------

    fuel_mass = FuelTankMass(full_fuel_mass=79015.8-62732.0, center_of_gravity=jnp.array([[13.61, 0., -0.93]]))
    fuel = FuelTank(origin=jnp.array([[13.61, 0., -0.93]]),mass_properties=fuel_mass)

    line_stores = vehicle.energy.lines[0].stores
    line_stores = line_stores.add_subcomponent(fuel)

    vehicle = eqx.tree_at(lambda v: v.energy.lines[0].stores, vehicle, line_stores)

    # ------------------------------------------------------------------------------------------------------------------
    # Configurations
    # ------------------------------------------------------------------------------------------------------------------

    # Takeoff Configuration

    # takeoff_config = deepcopy(vehicle)
    # takeoff_config.tag = "Takeoff"
    # takeoff_config.wings.main_wing.control_surfaces.flap.deflection    = jnp.deg2rad(20)
    # takeoff_config.wings.main_wing.control_surfaces.slat.deflection    = jnp.deg2rad(25)

    # for tf in takeoff_config.energy.lines[0].converters:

    #     tf: rcl.Components.Energy.Propulsors.TurbofanEngine
    #     tf.converters.fan.rotation_speed        = 2780.
    #     tf.converters.fan_nozzle.noise_speed    = 315.
    #     tf.converters.core_nozzle.noise_speed   = 415.

    # vehicle.configurations.add_subcomponent(takeoff_config)

    # # Cutback Configuration

    # cutback_config = deepcopy(vehicle)
    # cutback_config.tag = "Cutback"
    # cutback_config.wings.main_wing.control_surfaces.flap.deflection    = jnp.deg2rad(20)
    # cutback_config.wings.main_wing.control_surfaces.slat.deflection    = jnp.deg2rad(20)

    # for tf in cutback_config.energy.lines[0].converters:

    #     tf: rcl.Components.Energy.Propulsors.TurbofanEngine
    #     tf.converters.fan.rotation_speed        = 2780.
    #     tf.converters.fan_nozzle.noise_speed    = 210.
    #     tf.converters.core_nozzle.noise_speed   = 360.

    # vehicle.configurations.add_subcomponent(cutback_config)

    # # Landing Configuration

    # landing_config = deepcopy(vehicle)
    # landing_config.tag = "Landing"
    # landing_config.wings.main_wing.control_surfaces.flap.deflection    = jnp.deg2rad(30)
    # landing_config.wings.main_wing.control_surfaces.slat.deflection    = jnp.deg2rad(25)

    # landing_config.landing_gear.main_landing_gear.deployed = True
    # landing_config.landing_gear.main_landing_gear.deployed = True

    # for tf in landing_config.energy.lines[0].converters:

    #     tf: rcl.Components.Energy.Converters.TurbofanEngine
    #     tf.converters.fan.rotation_speed        = 2030.
    #     tf.converters.fan_nozzle.noise_speed    = 109.3
    #     tf.converters.core_nozzle.noise_speed   = 92.

    # vehicle.configurations.add_subcomponent(landing_config)

    return vehicle


def mission_setup(state: "State", system: "System", settings: "Settings"):

    # Set Controls & Analysis Settings

    controls = (
        "body_angle",
        DirectControlVariable(tag='Thrust', path=("frames", "body", "thrust_force_vector",), active=True)
    )

    residuals = ("force_x", "force_z")

    vortex_settings = VLMVortices(spanwise_vortices=20, chordwise_vortices=12)
    aero_settings = VLMSettings(vortices=vortex_settings)

    updated_settings = eqx.tree_at(lambda s: s.analysis.aerodynamics, settings, aero_settings)

    # Create Segments

    climb_segment = Segment(
        tag="Climb Segment",
        position_profile=AltitudeChange(initial_altitude=0.0 * Units.m, final_altitude=10000.0 * Units.m),
        speed_profile=ConstantSpeed(speed=125 * Units.m/Units.s),
        velocity_profile=ConstantAltitudeChangeRate(change_rate=6.0 * Units.m/Units.s),
        duration_profile=FixedTime(time = 10000.0 / 6.0 * Units.s),
        active_controls=controls,
        active_residuals=residuals,
        controls_initial_guess=(0.03, 50000.0 * Units.N),
    )
    
    cruise_segment = Segment(
        tag="Cruise Segment",
        position_profile=ConstantAltitude(altitude=10000.0 * Units.m),
        speed_profile=ConstantSpeed(speed=230 * Units.m/Units.s),
        duration_profile=FixedDistance(distance=5500. * Units.km),
        active_controls=controls,
        active_residuals=residuals,
        controls_initial_guess=(0.03, 50000.0 * Units.N),
    )

    descent_segment = Segment(
        tag="Descent Segment",
        position_profile=AltitudeChange(initial_altitude=10000.0 * Units.m, final_altitude=0.0 * Units.m),
        speed_profile=ConstantSpeed(speed=145 * Units.m/Units.s),
        velocity_profile=ConstantAltitudeChangeRate(change_rate=5.0 * Units.m/Units.s),
        duration_profile=FixedTime(time = 10000.0 / 5.0 * Units.s),
        active_controls=controls,
        active_residuals=residuals,
    )

    # test_cruise_segment = TestCSACruise(altitude=10000.0, speed)

    mission = Process(
        tag='Boeing 737 Mission',
        steps=(
            # climb_segment,
            cruise_segment,
            # descent_segment,
            ), #type: ignore
        initial_state=state,
        initial_system=system,
        initial_settings=settings
    )

    final_segments = []
    
    for segment in mission.steps:
        aero_analysis = VLM()
        seg_w_analysis = eqx.tree_at(lambda s: s.analyze.aerodynamics, segment, aero_analysis)
        
        aero_init = InitializeVLM()
        updated_init_steps = segment.initialize.steps + (aero_init,)
        final_seg = eqx.tree_at(lambda s: s.initialize.steps, seg_w_analysis, updated_init_steps)
        
        final_segments.append(final_seg)

    return eqx.tree_at(lambda m: m.steps, mission, tuple(final_segments)), updated_settings


def state_setup():

    numerics = Numerics(number_of_control_points=4)
    
    state = State(numerics=numerics)
    state = eqx.tree_at(lambda s: s.freestream.atmosphere, state, USStandard1976(), is_leaf=lambda x: x is None)
    frozen_initials = eqx.tree_at(lambda s: s.initials, state, None, is_leaf=lambda x: x is None)
    state = eqx.tree_at(lambda s: s.initials, state, frozen_initials, is_leaf=lambda x: x is None)

    return state


def mission_b737(state, system, settings):

    mission, updated_settings = mission_setup(state, system, settings)

    final_state, final_system, final_settings = mission.run(state, system, updated_settings)

    VLM_data = final_system.analysis_data
    fig = plot_vlm_panels(VLM_data['vortex_distribution'], VLM_data['pressure_coefficients'][0])
    fig.show()

    return final_state, final_system, final_settings


if __name__ == '__main__':

    print("Setting up mission ...")

    state = state_setup()
    system = vehicle_setup()
    settings = Settings(DEBUG_MODE=False)

    print("Setup complete, starting mission ...")

    final_state, _, _ = mission_b737(state, system, settings)
    
    print("Controls:")
    print(f"  AoA: {final_state.aerodynamics.angles.alpha}")
    print(f"  Thrust: {final_state.frames.body.thrust_force_vector[:, 0]}")
    print(f"\nAerodynamics:")
    print(f"  CL: {final_state.aerodynamics.coefficients.lift.total}")
    print(f"  CD: {final_state.aerodynamics.coefficients.drag.total}")
    print(f"    CDi: {final_state.aerodynamics.coefficients.drag.induced.total}")
    print(f"      Inv.: {final_state.aerodynamics.coefficients.drag.induced.inviscid.total}")
    print(f"      Visc.: {final_state.aerodynamics.coefficients.drag.induced.viscous.total}")
    print(f"    CDp: {final_state.aerodynamics.coefficients.drag.parasite.total}")
    

    # def CL_M(total_mass, state, system, settings):
    #     # Setup Phase (Pure Python, executes every time)

    #     # Update the mass dynamically
    #     system = eqx.tree_at(lambda s: s.mass_properties.total, system, total_mass)

    #     # Execution Phase (JIT compiled solver)
    #     final_state, _, _ = mission_b737(state, system, settings)
        
    #     return final_state.aerodynamics.coefficients.lift.total[0][0]
    
    # # Create our value-and-gradient function
    # dCL_M = value_and_grad(CL_M)
    
    # # ---------------------------------------------------------
    # # 1. THE COMPILATION RUN (The "Cold Start")
    # # ---------------------------------------------------------
    # print("Initiating XLA Compilation and First Run...")
    # t0 = time.perf_counter()
    
    # val = CL_M(79015.8, state, system, settings)
    
    # val.block_until_ready()
    # # grad.block_until_ready()
    
    # t1 = time.perf_counter()
    # print(f"Compilation + First Execution: {t1 - t0:.4f} seconds")
    # print(f"Initial Lift: {val:.4f}")# | dCL/dMass: {grad:.8f}\n")

    # # ---------------------------------------------------------
    # # 2. THE EXECUTION BENCHMARK (The "Hot Runs")
    # # ---------------------------------------------------------
    # print("Benchmarking Compiled Execution Graph...")
    # iterations = 10
    
    # t2 = time.perf_counter()
    
    # for _ in range(iterations):
    #     val = CL_M(79015.8, state, system, settings)
    #     val.block_until_ready()
    #     # grad.block_until_ready()
        
    # t3 = time.perf_counter()
    
    # avg_time = (t3 - t2) / iterations
    # print(f"Average Total Time (Setup + Execution): {avg_time:.6f} seconds per run")
    # print(f"Equivalent to {1 / avg_time:.2f} full mission evaluations per second")