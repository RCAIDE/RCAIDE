# RCAIDE/Framework/Missions/Mission.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from typing import Callable, List, Any, Tuple
from dataclasses import field

# package imports

import jax
import jax.numpy as jnp
import scipy.optimize

import chex

jax.config.update("jax_enable_x64", True)

from jax import jit, grad

import RNUMPY as rp
from scipy.optimize import minimize, NonlinearConstraint

from RNUMPY.scipy import fsolve

# RCAIDE imports

import RCAIDE.Framework as rcf
from RCAIDE.Framework import Process, ProcessStep
from RCAIDE.Framework.Process import skip
from RCAIDE.Framework.Missions.Initialize import *
from RCAIDE.Framework.Missions.Update     import *
from RCAIDE.Framework.Missions.Converge   import fsolve_results_parser, fsolve_update_kwargs
from RCAIDE.Framework.Missions.Conditions.Controls import ControlVariable

# ----------------------------------------------------------------------------------------------------------------------
# Segment Subfunctions
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class InitializeSegment(Process):

    tag: str = 'Segment Initialization'

    active_controls:   Tuple[str|ControlVariable, ...] = field(default_factory=tuple)
    active_residuals:  Tuple[str|ControlVariable, ...] = field(default_factory=tuple)

    controls_initial_guess: rp.ndarray = None

    def _activate_control(self, control: str | ControlVariable) -> None:
        if isinstance(control, str):
            control = control.replace(' ', '_').lower()  # Normalize control name to lowercase and replace spaces with underscores
            if control not in self.state.controls.keys():
                self.state.controls.add_control_variable(ControlVariable(tag=control))
            self.state.controls[control].active = True
        else:
            self.state.controls.add_control_variable(control)

    def _activate_residual(self, residual_name: str) -> None:
        residual_name = residual_name.replace(' ', '_').lower()  # Normalize residual name to lowercase and replace spaces with underscores
        self.state.dynamics[residual_name].active = True

    def __post_init__(self):

        default_steps = [
            # Step Name              Step Functions
            ("Expand State",         expand_state),
            ("Time",                 initialize_time),
            ("Mass",                 initialize_mass),
            ("Energy",               initialize_energy),
            ("Inertial Position",    initialize_inertial_position),
            ("Planetary Position",   initialize_planetary_position),
        ]

        for name, function in default_steps:
            self.append(ProcessStep(tag=name, function=function))

    def __call__(self):
        for ctrl_name in self.active_controls:
            self._activate_control(ctrl_name)
        if isinstance(self.controls_initial_guess, rp.ndarray):
            self.state.unknowns = self.controls_initial_guess
        elif isinstance(self.controls_initial_guess, tuple):
            self.state.unknowns = rp.concatenate([rp.ones(self.state.numerics.number_of_control_points) * v for v in self.controls_initial_guess])
        else:
            self.state.unknowns = rp.zeros((self.state.numerics.number_of_control_points * len(self.active_controls)))

        for res_name in self.active_residuals:
            self._activate_residual(res_name)
        self.state.residuals = rp.zeros((self.state.numerics.number_of_control_points, len(self.active_residuals)))

        assert self.state.check_controls(verbose=False), (
            f"During initialization of {self.tag} the number of active controls"
            "did not match the number of active residuals.\n"
            "Please run State.check_controls(verbose=True) to see details"
        )

        return super(InitializeSegment, self).__call__()


@chex.dataclass(kw_only=True)
class AnalyzeSegment(Process):

    tag: str = "Segment Analysis Specification"

    gravity:                Callable = lambda st, sy, se: skip(st, sy, se)
    energy:                 Callable = lambda st, sy, se: skip(st, sy, se)
    aerodynamics:           Callable = lambda st, sy, se: skip(st, sy, se)
    stability:              Callable = lambda st, sy, se: skip(st, sy, se)
    planetary_position:     Callable = lambda st, sy, se: skip(st, sy, se)

    calculate_residuals:    Callable = flight_dynamics_residuals

    def __post_init__(self):

        default_steps = [
            ("Time Differentials",   update_time_differentials),
            ("Acceleration",         update_acceleration),
            ("Angular Acceleration", update_angular_acceleration),
            ("Altitude",             update_altitude),
            ("Gravity",              update_gravity),
            ("Freestream",           update_freestream),
            ("Orientations",         update_orientations),
            ("Energy",               self.energy),
            ("Aerodynamics",         self.aerodynamics),
            ("Stability",            self.stability),
            ("Mass",                 update_mass_and_weight),
            ("Forces",               update_forces),
            ("Moments",              update_moments),
            ("Planetary Position",   self.planetary_position),
            ("Calculate Residuals",  self.calculate_residuals)
        ]

        for name, function in default_steps:
            self.append(ProcessStep(tag=name, function=function))


@chex.dataclass(kw_only=True)
class IterateSegment(Process):

    tag:            str     = 'Segment Convergence'

    analyze:        Process = None

    # Root-finder arguments and parser
    root_finder:            Callable    = fsolve
    root_finder_args:       Tuple       = None
    root_finder_kwargs:     dict        = None

    update_args:            Callable    = None
    update_kwargs:          Callable    = fsolve_update_kwargs
    results_parser:         Callable[[Any], Tuple["rcf.State", "rcf.System", "rcf.Settings"]] = fsolve_results_parser

    def _get_fsolve_residuals(self, unknowns):
        """
        Wraps the analysis step to calculate residuals for fsolve.
        """

        self.state.unknowns = unknowns
        self.state.unpack_unknowns()

        self.analyze.state          = self.state
        self.analyze.system         = self.system
        self.analyze.settings       = self.settings

        self.state, self.system, self.settings = self.analyze()

        self.state.pack_residuals()

        if self.update_args:
            self.root_finder_args = self.update_args(self.root_finder_args, self.state, self.system, self.settings)
        if self.update_kwargs:
            self.root_finder_kwargs = self.update_kwargs(self.root_finder_kwargs, self.state, self.system, self.settings)

        return self.state.residuals.ravel(order='F')


    def __call__(self):



        if self.root_finder is fsolve and self.root_finder_kwargs is None:

            self.root_finder_kwargs = {
                'func': self._get_fsolve_residuals,
                'x0': self.state.unknowns,
                # 'args': self.state.unknowns,
                'xtol': self.state.numerics.solution_tolerance,
                'maxfev': self.state.numerics.max_evaluations,
                'epsfcn': self.state.numerics.step_size,
                'full_output': True
            }

        # with jax.checking_leaks():
        results = self.root_finder(**self.root_finder_kwargs)

        self.state, self.system, self.settings = self.results_parser(results, self.state, self.system, self.settings)

        return self.state, self.system, self.settings


@chex.dataclass(kw_only=True)
class FinalizeSegment(Process):

    tag: str = 'Segment Finalization'

    @staticmethod
    def _reset_controls_and_residuals(
            state: "rcf.State",
            system: "rcf.System",
            settings: "rcf.Settings",
    ):

        for name, control_var in vars(state.controls).items():
            if hasattr(control_var, 'active') and control_var.active:
                control_var.active = False

        for name, residual_var in vars(state.dynamics).items():
            if hasattr(residual_var, 'active') and residual_var.active:
                residual_var.active = False

        return state, system, settings

    def __post_init__(self):
        self.steps.append(
            ProcessStep(tag='Reset Controls and Residuals',
                        function=self._reset_controls_and_residuals)
        )


# ----------------------------------------------------------------------------------------------------------------------
# Converged Segments
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class Segment(Process):

    tag: str = "Segment"

    active_controls:    Tuple[str, ...]   = None
    active_residuals:   Tuple[str, ...]   = None

    controls_initial_guess: tuple | rp.ndarray = None

    initialize:         InitializeSegment   = field(default_factory=InitializeSegment)
    iterate:            IterateSegment      = field(default_factory=IterateSegment)
    analyze:            AnalyzeSegment      = field(default_factory=AnalyzeSegment)
    finalize:           FinalizeSegment     = field(default_factory=FinalizeSegment)

    # Global dynamics variables
    sideslip_angle:         float = 0.0
    temperature_deviation:  float = 0.0

    def __post_init__(self):

        self.initialize.tag                     = f'Initialize {self.tag}'
        self.initialize.active_controls         = self.active_controls
        self.initialize.active_residuals        = self.active_residuals

        self.initialize.controls_initial_guess  = self.controls_initial_guess

        self.analyze.tag                        = f'Analyze {self.tag}'

        self.iterate.tag                        = f'Iterate {self.tag}'
        self.iterate.analyze                    = self.analyze

        self.finalize.tag                       = f'Finalize {self.tag}'

        self.steps = [
            self.initialize,
            self.iterate,
            self.finalize,
        ]

    def __call__(self, *args, **kwargs) -> Tuple["rcf.State", "rcf.System", "rcf.Settings"]:

        for step in self.analyze.steps:
            if isinstance(step, ProcessStep) and step.function is skip:
                print(f"Skipping step {step.tag} due to missing analysis function.")

        return super(Segment, self).__call__(*args, **kwargs)


#-----------------------------------------------------------------------------------------------------------------------
# Optimal Segments
#-----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class OptimalSegment(Process):

    tag:                    str    = 'Optimize Segment'
    optimization_method:    str    = 'SLSQP'
    display_optimization:   bool   = False

    initialize:             InitializeSegment   = field(default_factory=InitializeSegment)
    analyze:                AnalyzeSegment      = field(default_factory=AnalyzeSegment)

    calculate_objective:    Callable    = None
    bounds:                 List[Any]   = None
    constraints:            dict        = None

    function: Callable = scipy.optimize.minimize

    def _results_parser(self, res):

        self.state.unknowns.unpack_array(res.x)
        self.state.objective.unpack_array(res.fun)

        self.last_result = res

        return self.state, self.settings, self.system

    def __call__(self, *args, **kwargs) -> Tuple["rcf.State", "rcf.System", "rcf.Settings"]:

        # Fix Bounds
        NCP = self.state.numerics.number_of_control_points
        new_bounds = []
        for b in self.bounds:
            new_bounds.extend([b for _ in range(NCP)])
        self.bounds = new_bounds

        # self.state, self.system, self.settings = args[0]
        self.state.initials = self.state
        self.update_details()

        self.initialize.state = self.state
        self.initialize.system = self.system
        self.initialize.settings = self.settings

        self.state, self.system, self.settings = self.initialize((self.state, self.system, self.settings))

        def _obj(U):
            self.state.unknowns.unpack_array(U)
            self.analyze.state = self.state
            self.analyze.system = self.system
            self.analyze.settings = self.settings
            self.state, self.system, self.settings = self.analyze()
            return self.calculate_objective(self.state, self.system, self.settings)

        _obj_fcn    = jit(_obj)
        _obj_grad   = jit(grad(_obj_fcn))

        res = minimize(
            fun=_obj_fcn,
            jac=_obj_grad,
            x0=self.state.unknowns.pack_array(),
            method=self.optimization_method,
            bounds=self.bounds,
            constraints=self.constraints,
            options={'disp': self.display_optimization,
                     'maxiter': self.state.numerics.max_evaluations},
            tol=self.state.numerics.solution_tolerance,
        )

        self.state, self.system, self.settings = self._results_parser(res)

        self.state, self.system, self.settings = self.finalize(self.state, self.system, self.settings)

        return self.state, self.system, self.settings


#-----------------------------------------------------------------------------------------------------------------------
# Energy Optimal Segments

def energy_use(
        state: "rcf.State",
        system: "rcf.System",
        settings: "rcf.Settings"
):

    energy_start    = state.energy.total_energy[0]
    energy_end      = state.energy.total_energy[-1]
    energy_used     = energy_end - energy_start

    return energy_used[0]


@chex.dataclass(kw_only=True)
class EnergyOptimalCruise(OptimalSegment):

    tag: str = 'Energy Optimal Cruise'

    altitude: float = 0.0
    distance: float = 0.0

    calculate_objective: Callable = energy_use

    def __post_init__(self):
        distance_check = lambda x: self.state.frames.inertial.position_vector[-1, 0]
        self.bounds = [(-rp.pi/12, rp.pi/12), (0., 1.)]
        self.constraints = [NonlinearConstraint(distance_check, lb=self.distance, ub=self.distance)]


@chex.dataclass(kw_only=True)
class EnergyOptimalAltitudeChange(OptimalSegment):

    tag: str = 'Energy Optimal Altitude Change'

    altitude_start: float = 0.0
    altitude_end:   float = 0.0

    calculate_objective: Callable = energy_use

    def __post_init__(self):
        start_check = lambda x: self.state.frames.inertial.position_vector[0, 2]
        end_check = lambda x: self.state.frames.inertial.position_vector[-1, 2]
        self.bounds = [(-rp.pi/4, rp.pi/4), (0., 1.)]
        self.constraints = [NonlinearConstraint(start_check, lb=self.altitude_start, ub=self.altitude_start),
                            NonlinearConstraint(end_check, lb=self.altitude_end, ub=self.altitude_end)]
