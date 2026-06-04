import pandas as pd
import json
import os
import pysu2
import numpy as np

from su2_config_class import SU2Config
from mpi4py import MPI



CACHE_FILE = "su2_run_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_cache(cache_dict):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache_dict, f, indent=4)


def run_su2_primal_raw(alpha_val):
    cache = load_cache()
    key = f"primal_alpha_{float(alpha_val):.4f}"

    # If we already ran this, return the cached value immediately!
    if key in cache:
        print(f"Loading Primal from cache for Alpha = {alpha_val}")
        return np.float64(cache[key])

    print(f"Running SU2 Primal for Alpha = {alpha_val}...")

    # 1. Setup the Config for the Primal Run
    config = SU2Config()
    config.MESH_FILENAME = os.path.abspath('mesh_ONERAM6_inv_ffd.su2')
    config.AOA = float(alpha_val)

    config.MACH_NUMBER = 0.3
    config.LOW_MACH_PREC = True
    config.CFL_NUMBER = 1.0  # Start conservative
    config.CFL_ADAPT = True  # Let SU2 ramp it up automatically
    config.CFL_ADAPT_PARAM = (0.1, 2.0, 10.0, 1e10, 0.001, 0)

    config.MATH_PROBLEM = 'DIRECT'
    # config.SCREEN_OUTPUT = ('INNER_ITER', 'RMS_DENSITY', 'RMS_ENERGY', 'LIFT', 'DRAG')

    # Set up the boundaries for the ONERA M6 mesh
    surface_markers = ('LOWER_SIDE', 'UPPER_SIDE', 'TIP')
    sym_markers = ('SYMMETRY_FACE',)

    # Boundary Conditions
    config.MARKER_EULER = surface_markers
    config.MARKER_SYM = sym_markers
    config.MARKER_FAR = ('XNORMAL_FACES', 'ZNORMAL_FACES', 'YNORMAL_FACE')

    # Output and Monitoring
    config.MARKER_PLOTTING = surface_markers
    config.MARKER_MONITORING = surface_markers
    config.MARKER_ANALYZE = surface_markers

    # Geometry and Design Variables
    config.MARKER_DESIGNING = surface_markers
    config.GEO_MARKER = surface_markers
    config.DV_MARKER = surface_markers

    # Mesh Deformation & Smoothing
    config.MARKER_DEFORM_MESH = surface_markers
    config.MARKER_SOBOLEVBC = surface_markers
    config.MARKER_DEFORM_MESH_SYM_PLANE = sym_markers

    config.DEFORM_MESH = False
    config.MARKER_DEFORM_MESH = surface_markers
    config.MARKER_SOBOLEVBC = surface_markers
    config.MARKER_DEFORM_MESH_SYM_PLANE = sym_markers

    # 2. Write to a temporary run file
    run_cfg_file = os.path.abspath(f"run_primal_{alpha_val:.2f}.cfg")
    config.write_to_file(run_cfg_file)

    if not os.path.exists(run_cfg_file):
        raise FileNotFoundError(f"Python failed to write: {run_cfg_file}")

    print(f"Config successfully written to: {run_cfg_file}")

    # 3. Run SU2
    driver = pysu2.CSinglezoneDriver(run_cfg_file, 1, MPI.COMM_WORLD)
    driver.StartSolver()
    driver.Postprocessing()

    # 4. Extract CL
    cl = driver.getOutputValue('LIFT')

    # Save the result before returning
    cache[key] = float(cl)
    save_cache(cache)

    return np.float64(cl)


def run_su2_adjoint_raw(alpha_val):
    cache = load_cache()
    key = f"adjoint_alpha_{float(alpha_val):.4f}"

    if key in cache:
        print(f"Loading Adjoint from cache for Alpha = {alpha_val}")
        return np.float64(cache[key])

    print(f"Running SU2 Adjoint for Alpha = {alpha_val}...")

    # 1. Setup the Config for the Adjoint Run
    config = SU2Config()
    config.MESH_FILENAME = os.path.abspath('mesh_ONERAM6_inv_ffd.su2')
    config.AOA = float(alpha_val)

    config.MACH_NUMBER = 0.3
    config.LOW_MACH_PREC = True
    config.CFL_NUMBER = 1.0  # Start conservative
    config.CFL_ADAPT = True  # Let SU2 ramp it up automatically
    config.CFL_ADAPT_PARAM = (0.1, 2.0, 10.0, 1e10, 0.001, 0)

    config.MATH_PROBLEM = 'DISCRETE_ADJOINT'
    config.OBJECTIVE_FUNCTION = 'LIFT'
    # config.SCREEN_OUTPUT = ('INNER_ITER', 'RMS_DENSITY', 'RMS_ENERGY', 'LIFT', 'DRAG')

    # Set up the boundaries for the ONERA M6 mesh
    surface_markers = ('LOWER_SIDE', 'UPPER_SIDE', 'TIP')
    sym_markers = ('SYMMETRY_FACE',)

    # Boundary Conditions
    config.MARKER_EULER = surface_markers
    config.MARKER_SYM = sym_markers
    config.MARKER_FAR = ('XNORMAL_FACES', 'ZNORMAL_FACES', 'YNORMAL_FACE')

    # Output and Monitoring
    config.MARKER_PLOTTING = surface_markers
    config.MARKER_MONITORING = surface_markers
    config.MARKER_ANALYZE = surface_markers

    # Geometry and Design Variables
    config.MARKER_DESIGNING = surface_markers
    config.GEO_MARKER = surface_markers
    config.DV_MARKER = surface_markers

    # Mesh Deformation & Smoothing
    config.MARKER_DEFORM_MESH = surface_markers
    config.MARKER_SOBOLEVBC = surface_markers
    config.MARKER_DEFORM_MESH_SYM_PLANE = sym_markers

    config.DEFORM_MESH = False
    config.MARKER_DEFORM_MESH = surface_markers
    config.MARKER_SOBOLEVBC = surface_markers
    config.MARKER_DEFORM_MESH_SYM_PLANE = sym_markers

    # Secure the escape hatch: Use raw string for the complex DV definition
    config.DEFINITION_DV = "( 1.0, 1.0 | ANGLE_OF_ATTACK | 1.0 )"

    # 2. Write to a temporary run file
    run_cfg_file = os.path.abspath(f"run_adjoint_{alpha_val:.2f}.cfg")
    config.write_to_file(run_cfg_file)

    # 3. Run SU2 Adjoint
    driver = pysu2.CDiscAdjSinglezoneDriver(run_cfg_file, 1, MPI.COMM_WORLD)
    driver.StartSolver()
    driver.Postprocessing()

    # 4. Extract dCL/dAlpha
    # The adjoint solver creates 'of_grad.csv' containing the gradients
    try:
        # Read the CSV generated by SU2 v8.4.0
        grad_df = pd.read_csv('of_grad.csv', skipinitialspace=True)

        # The column name usually matches your DEFINITION_DV tag
        # e.g., 'ANGLE_OF_ATTACK'
        dcl_dalpha = grad_df['ANGLE_OF_ATTACK'].iloc[0]

    except FileNotFoundError:
        # Fallback for older .dat formats if v8.4 defaults to legacy output
        with open('of_grad.dat', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'ANGLE_OF_ATTACK' in line:
                    dcl_dalpha = float(line.split()[1])
                    break

    cache[key] = float(dcl_dalpha)
    save_cache(cache)

    return np.float64(dcl_dalpha)


if __name__ == '__main__':
    cl = run_su2_primal_raw(2.0)
    print(f"Primal Lift Coefficient at Alpha = 2.0: {cl:.4f}")

    dcl_dalpha = run_su2_adjoint_raw(2.0)
    print(f"Adjoint dCL/dAlpha at Alpha = 2.0: {dcl_dalpha:.4f}")
