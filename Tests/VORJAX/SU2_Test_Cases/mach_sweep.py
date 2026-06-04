import os
import re
import json
import numpy as np
from mpi4py import MPI
import pysu2ad as pysu2

# MPI Setup
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
num_cores = comm.Get_size()

CACHE_FILE = "su2_run_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache_dict):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache_dict, f, indent=4)


def update_mach_in_config(template_filename, temp_filename, new_mach):
    """ Reads the template .cfg, updates MACH_NUMBER, and saves a temporary copy. """
    with open(template_filename, 'r') as file:
        config_text = file.read()
    
    # The lambda safely grabs Group 1 and slaps the new Mach number on the end
    updated_text = re.sub(
        r'(?i)(MACH_NUMBER\s*=\s*)([0-9]*\.?[0-9]+)', 
        lambda match: match.group(1) + str(new_mach), 
        config_text
    )
    
    with open(temp_filename, 'w') as file:
        file.write(updated_text)


def prep_configs_for_sweep(template_filename, mach_number):
    """ Generates separate Primal and Adjoint configs for the current Mach step. """
    with open(template_filename, 'r') as file:
        base_config = file.read()
    
    m_str = str(mach_number).replace('.', '_')

    # 1. Update the Mach Number for both
    base_config = re.sub(
        r'(?i)(MACH_NUMBER\s*=\s*)([0-9]*\.?[0-9]+)', 
        lambda m: m.group(1) + str(mach_number), 
        base_config
    )

    base_config = re.sub(
        r'(?i)(RESTART_SOL\s*=\s*)([A-Za-z]+)', 
        lambda m: m.group(1) + 'NO', 
        base_config
    )

    base_config = re.sub(
        r'(?i)(CONV_FILENAME\s*=\s*)([A-Za-z0-9_.]+)', 
        lambda m: m.group(1) + f'history_M{m_str}.csv', 
        base_config
    )
    base_config = re.sub(
        r'(?i)(VOLUME_FILENAME\s*=\s*)([A-Za-z0-9_.]+)', 
        lambda m: m.group(1) + f'flow_M{m_str}.vtu', 
        base_config
    )
    base_config = re.sub(
        r'(?i)(SURFACE_FILENAME\s*=\s*)([A-Za-z0-9_.]+)', 
        lambda m: m.group(1) + f'surface_flow_M{m_str}.vtu', 
        base_config
    )
    
    # Rename Primal Output State (CRITICAL)
    base_config = re.sub(
        r'(?i)(RESTART_FILENAME\s*=\s*)([A-Za-z0-9_.]+)', 
        lambda m: m.group(1) + f'restart_flow_M{m_str}.dat', 
        base_config
    )

    base_config = re.sub(
        r'(?i)(LIMITER_ITER\s*=\s*)([0-9]+)', 
        lambda m: m.group(1) + '500', 
        base_config
    )
    
    # 2. Save the Primal Config
    primal_filename = f"temp_primal_M{m_str}.cfg"
    with open(primal_filename, 'w+') as file:
        file.write(base_config)
        
    # 3. Modify settings for the Adjoint Config
    adj_config = base_config
    
    # Switch the math problem
    adj_config = re.sub(
        r'(?i)(MATH_PROBLEM\s*=\s*)([A-Za-z_]+)', 
        lambda m: m.group(1) + 'DISCRETE_ADJOINT', 
        adj_config
    )

    adj_config = re.sub(
        r'(?i)(SCREEN_OUTPUT\s*=\s*)\((.*)\)', 
        lambda m: m.group(1) + '(INNER_ITER, AVG_RMS_RES, SENS_AOA, LINSOL_RESIDUAL)', 
        adj_config
    )
    
    # Change the history filename to prevent wiping the Primal data
    adj_config = re.sub(
        r'(?i)(CONV_FILENAME\s*=\s*)([A-Za-z0-9_.]+)', 
        lambda m: m.group(1) + f'history_adj_M{m_str}.csv', 
        adj_config
    )

    adj_config = re.sub(
        r'(?i)(VOLUME_FILENAME\s*=\s*)([A-Za-z0-9_.]+)', 
        lambda m: m.group(1) + f'adjoint_M{m_str}.vtu', 
        adj_config
    )

    adj_config = re.sub(
        r'(?i)(SURFACE_FILENAME\s*=\s*)([A-Za-z0-9_.]+)', 
        lambda m: m.group(1) + f'surface_adjoint_M{m_str}.vtu', 
        adj_config
    )

    adj_config = re.sub(
        r'(?i)(CONV_FIELD\s*=\s*)([A-Za-z_]+)', 
        lambda m: m.group(1) + 'AVG_RMS_RES', 
        adj_config
    )
    
    adj_config = re.sub(
        r'(?i)(CONV_RESIDUAL_MINVAL\s*=\s*)([-0-9.]+)', 
        lambda m: m.group(1) + '-8', 
        adj_config
    )

    # Force the Adjoint to calculate sensitivities for LIFT
    adj_config = re.sub(
        r'(?i)(OBJECTIVE_FUNCTION\s*=\s*)([A-Za-z_]+)', 
        lambda m: m.group(1) + 'LIFT', 
        adj_config
    )

    adj_config = re.sub(
        r'(?i)(SOLUTION_FILENAME\s*=\s*)([A-Za-z0-9_.]+)', 
        lambda m: m.group(1) + f'restart_flow_M{m_str}.dat', 
        adj_config
    )

    adj_config = re.sub(
        r'(?i)(HISTORY_OUTPUT\s*=\s*)\((.*)\)', 
        lambda m: m.group(1) + '(ITER, RMS_RES, SENS_AOA)', 
        adj_config
    )

    adj_config = re.sub(
        r'(?i)(CFL_NUMBER\s*=\s*)([0-9]*\.?[0-9]+)', 
        lambda m: m.group(1) + '2.0', 
        adj_config
    )
    adj_config = re.sub(
        r'(?i)(CFL_ADAPT\s*=\s*)([A-Za-z]+)', 
        lambda m: m.group(1) + 'NO', 
        adj_config
    )

    adj_config += "\nDEFINITION_DV= ( AOA, 1.0 | NONE )\n"

    # 4. Save the Adjoint Config
    adjoint_filename = f"temp_adjoint_M{m_str}.cfg"
    with open(adjoint_filename, 'w') as file:
        file.write(adj_config)
        
    return primal_filename, adjoint_filename

def evaluate_su2_parallel(mach_number):
    """
    Runs the Primal and Adjoint solvers in parallel with caching.
    """
    # Have Rank 0 check the cache first
    cache = load_cache() if rank == 0 else None
    
    # Broadcast the cache to all cores so everyone knows if we are skipping
    cache = comm.bcast(cache, root=0)
    key = f"mach_{float(mach_number):.3f}"
    
    if key in cache:
        if rank == 0:
            print(f"Loading results for Mach {mach_number} from cache.")
        return np.float64(cache[key]['cl']), np.float64(cache[key]['dcl_dalpha'])

    if rank == 0:
        print(f"\n--- Running SU2 on {num_cores} cores for Mach {mach_number} ---")
    
    primal_cfg, adjoint_cfg = prep_configs_for_sweep("inv_ONERAM6.cfg", mach_number)
    
    # 1. Run Primal
    primal_driver = pysu2.CSinglezoneDriver(primal_cfg, 1, comm)
    primal_driver.StartSolver()
    primal_driver.Postprocess()
    
    # 2. Run Adjoint (Automatically uses the converged Primal state)
    adjoint_driver = pysu2.CDiscAdjSinglezoneDriver(adjoint_cfg, 1, comm)
    adjoint_driver.StartSolver()
    adjoint_driver.Postprocess()
    
    # 3. Extract Results
    cl = primal_driver.GetOutputValue("LIFT")
    dcl_dalpha = adjoint_driver.GetOutputValue("SENS_AOA")

    
    # 4. Rank 0 saves to the cache so we never have to run this Mach number again
    if rank == 0:
        cache[key] = {'cl': float(cl), 'dcl_dalpha': float(dcl_dalpha)}
        save_cache(cache)
        print(f"--- Mach {mach_number} Complete ---")

    return np.float64(cl) , np.float64(dcl_dalpha)

if __name__ == "__main__":

    cl = 0.0
    dcl_dalpha = 0.0
    for M in [1.6, 1.7, 1.8, 1.9, 2.0]:
        cl, dcl_dalpha = evaluate_su2_parallel(M)
    
    if rank == 0:
        print(f"\nFinal Results -> CL: {cl: .5f}, dCL_dA: {dcl_dalpha: .5f}")