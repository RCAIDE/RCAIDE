# RCAIDE/Library/Methods/Propulsors/Converters/compression_nozzle.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: Mar 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from __future__ import annotations
from typing import TYPE_CHECKING

# package imports
import jax.numpy as np

# RCAIDE imports
if TYPE_CHECKING:
    import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
#  Compression Nozzle Functional Methods
# ----------------------------------------------------------------------------------------------------------------------


def func_isentropic_nozzle_performance(
    T_t,
    P_t,
    P0,
    g,
    PR,
    n_r,
    n_p
):

    # Isentropic Outputs

    P_t_out = np.maximum(P_t * PR * n_r, P0)              # Output stagnation pressure, minimum is freestream pressure
    T_t_out = T_t * (PR * n_r) ** ((g - 1.) / (g * n_p))  # Output stagnation temperature

    M_out   = np.sqrt((((P_t_out / P0) ** ((g - 1.) / g)) - 1.) * 2. / (g - 1.))  # Output Mach number
    T_out   = T_t_out / (1. + (g - 1.) / 2. * M_out ** 2)                         # Output static temperature

    return P_t_out, T_t_out, T_out, M_out


def func_compression_nozzle_performance(
    T_t,
    P_t,
    P0,
    M0,
    Cp,
    g,
    PR,
    n_r,
    n_p
):

    P_t_out, T_t_out, T_out, M_out = func_isentropic_nozzle_performance(T_t, P_t, P0, g, PR, n_r, n_p)

    # Normal Shock Outputs

    ns_M    = np.sqrt((1. + (g - 1.) / 2. * M0 ** 2.) / (g * M0 ** 2 - (g - 1.) / 2.))
    ns_T    = T_t_out / (1. + (g - 1.) / 2 * ns_M ** 2)
    ns_P_t  = (PR *
               P_t *
               ((((g + 1.) * (M0 ** 2.)) / ((g - 1.) * M0 ** 2. + 2.)) ** (g / (g - 1.))) *
               ((g + 1.) / (2. * g * M0 ** 2.-(g - 1.))) ** (1./(g - 1.))
               )

    # Combine Outputs

    P_t_out[M0[:, 0] > 1.0] = ns_P_t[M0[:, 0] > 1.0]
    T_out[M0[:, 0] > 1.0] = ns_T[M0[:, 0] > 1.0]
    M_out[M0[:, 0] > 1.0] = ns_M[M0[:, 0] > 1.0]

    h_out   = Cp * T_out                        # Output static enthalpy
    h_t_out = Cp * T_t_out                      # Output stagnation enthalpy
    u_out   = np.sqrt(2. * (h_t_out - h_out))   # Output velocity

    return M_out, u_out, P_t_out, T_t_out, T_out, h_t_out, h_out


def func_expansion_nozzle_performance(
    T_t,
    T_t0,
    P_t,
    P_t0,
    P0,
    M0,
    Cp,
    g,
    R,
    PR,
    n_p
):

    P_t_out, T_t_out, T_out, M_isn = func_isentropic_nozzle_performance(T_t, P_t, P0, g, PR, 1., n_p)

    # Supersonic Expansion
    sup = M_isn > 1
    M = np.maximum(np.minimum(M_isn, 1.0), 0.001)  # Bound Mach number to [0.001, 1]
    P   = P_t_out / (1. + (g - 1.) / 2. * M ** 2) ** (g / (g - 1.))
    P_out = P0.at(sup).set(P)

    T_out   = T_t_out / (1. + (g - 1.) / 2. * M ** 2)

    h_t_out = Cp * T_t_out
    h_out   = Cp * T_out
    u_out   = np.sqrt(2. * (h_t_out - h_out))
    r_out   = P_out/(R * T_out)

    def fm(M, g):

        m0 = (g + 1.) / (2. * (g - 1.))
        m1 = ((g + 1.) / 2.) ** m0
        m2 = (1. + (g - 1.) / 2. * M * M) ** m0

        return m1 * M / m2

    AR      = (fm(M0, g) / fm(M, g) * (1 / (P_t_out / P_t0)) * (np.sqrt(T_t_out / T_t0)))

    return AR, M, r_out, u_out, P_out, P_t_out, T_out, T_t_out, h_out, h_t_out


def inlet_nozzle_performance(
    state: "rcf.State",
    system: "rcf.Aircraft",
    settings: "rcf.Settings"
):

    # Get inputs

    fs = state.freestream
    T_t = fs.stagnation_temperature
    P_t = fs.stagnation_pressure
    P0  = fs.pressure
    M0  = fs.mach_number
    Cp  = fs.Cp
    g   = fs.gamma

    for l_idx, line in enumerate(system.energy.lines):
        for p_idx, propulsor in enumerate(line.propulsors):

            nozzle = propulsor.converters.inlet_nozzle
            PR  = nozzle.pressure_ratio
            n_r = nozzle.pressure_recovery
            n_p = nozzle.polytropic_efficiency

            # Call function
            M_out, u_out, P_t_out, T_t_out, T_out, h_t_out, h_out = func_compression_nozzle_performance(T_t,
                                                                                                        P_t,
                                                                                                        P0,
                                                                                                        M0,
                                                                                                        Cp,
                                                                                                        g,
                                                                                                        PR,
                                                                                                        n_r,
                                                                                                        n_p)

            # Set Input State
            nozzle_state = state.energy.lines[l_idx].propulsors[p_idx].converters.inlet_nozzle

            inputs = nozzle_state.inputs

            inputs.stagnation_temperature = T_t
            inputs.stagnation_pressure    = P_t
            inputs.freestream_pressure    = P0
            inputs.freestream_mach_number = M0
            inputs.freestream_Cp          = Cp
            inputs.freestream_gamma       = g

            # Set Output State
            outputs = nozzle_state.outputs

            outputs.mach_number             = M_out
            outputs.velocity                = u_out

            outputs.stagnation_pressure     = P_t_out

            outputs.stagnation_temperature  = T_t_out
            outputs.static_temperature      = T_out

            outputs.stagnation_enthalpy     = h_t_out
            outputs.static_enthalpy         = h_out

    return state, system, settings


def _expansion_nozzle_performance(
    state: "rcf.State",
    system: "rcf.System",
    settings: "rcf.Settings",
    input_converter_state,
    output_converter_state,
    PR,
    n_p
):

    # Get Inputs
    T_t = input_converter_state.outputs.stagnation_temperature
    P_t = input_converter_state.stagnation_pressure

    fs      = state.freestream
    P0      = fs.pressure
    M0      = fs.mach_number
    Cp      = fs.Cp
    g       = fs.gamma
    R       = fs.R
    P_t0    = fs.stagnation_pressure
    T_t0    = fs.stagnation_temperature
    # Call function

    AR, M, r_out, u_out, P_out, P_t_out, T_out, T_t_out, h_out, h_t_out = func_expansion_nozzle_performance(T_t,
                                                                                                            T_t0,
                                                                                                            P_t,
                                                                                                            P_t0,
                                                                                                            P0,
                                                                                                            M0,
                                                                                                            Cp,
                                                                                                            g,
                                                                                                            R,
                                                                                                            PR,
                                                                                                            n_p)

    # Set Input State
    inputs = input_converter_state

    inputs.stagnation_temperature               = T_t
    inputs.stagnation_pressure                  = P_t

    inputs.freestream_stagnation_temperature    = T_t0
    inputs.freestream_stagnation_pressure       = P_t0
    inputs.freestream_pressure                  = P0
    inputs.freestream_mach_number               = M0
    inputs.freestream_Cp                        = Cp
    inputs.freestream_gamma                     = g
    inputs.freestream_R                         = R

    # Set Output State
    outputs = output_converter_state

    outputs.area_ratio                          = AR
    outputs.mach_number                         = M

    outputs.density                             = r_out
    outputs.velocity                            = u_out

    outputs.pressure                            = P_out
    outputs.stagnation_pressure                 = P_t_out

    outputs.temperature                         = T_out
    outputs.stagnation_temperature              = T_t_out

    outputs.enthalpy                            = h_out
    outputs.stagnation_enthalpy                 = h_t_out

    return state, system, settings


def fan_nozzle_performance(
    state: "rcf.State",
    system: "rcf.Aircraft",
    settings: "rcf.Settings"
):
    # Get Inputs

    for l_idx, line in enumerate(system.energy.lines):
        for p_idx, prop in enumerate(line.propulsors):

            nozzle = prop.converters.fan_nozzle
            PR  = nozzle.pressure_ratio
            n_p = nozzle.polytropic_efficiency

            state, system, settings = _expansion_nozzle_performance(state, system, settings,
                                                                    prop.converters.fan,
                                                                    prop.converters.fan_nozzle,
                                                                    PR, n_p)

    return state, system, settings


def core_nozzle_performance(
    state: "rcf.State",
    system: "rcf.Aircraft",
    settings: "rcf.Settings"
):
    # Get Inputs

    for l_idx, line in enumerate(system.energy.lines):
        for p_idx, prop in enumerate(line.propulsors):

            nozzle = prop.converters.core_nozzle
            PR = nozzle.pressure_ratio
            n_p = nozzle.polytropic_efficiency

            state, system, settings = _expansion_nozzle_performance(state, system, settings,
                                                                    prop.converters.turbines[-1],
                                                                    prop.converters.core_nozzle,
                                                                    PR, n_p)

    return state, system, settings
