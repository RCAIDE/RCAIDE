# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------    

import RCAIDE
from RCAIDE.Framework.Core import Units,  Data
from RCAIDE.Framework.Optimization.Common import Nexus 
from RCAIDE.Framework.Optimization.Packages.additive import Additive_Solver
import RCAIDE.Framework.Optimization.Packages.trmm.Trust_Region_Optimization as tro
from RCAIDE.Framework.Optimization.Packages.trmm.Trust_Region import Trust_Region

import vehicle_multifidelity
import procedure_multifidelity

import numpy as np 
import os

# ----------------------------------------------------------------------        
#   Run the whole thing
# ----------------------------------------------------------------------  
def main():
    np.random.seed(0)
    
    problem = setup() 
    tolerance = 5e-2
    
    def set_add_solver():
        solver = Additive_Solver()
        solver.local_optimizer = 'SLSQP'
        solver.global_optimizer = 'SHGO'
        return solver
    
    ################### Basic Additive ##################################################

    # ------------------------------------------------------------------
    #   Inactive constraints
    # ------------------------------------------------------------------

    solver = set_add_solver()

    problem.optimization_problem.constraints = np.array([
        [ 'x1' , '>', -10., 1., 1*Units.less],
        [ 'x2' , '>', -50., 1., 1*Units.less],
    ],dtype=object)

    print('\n\n Checking basic additive with no active constraints...')
    outputs = solver.Additive_Solve(problem,max_iterations=500,num_samples=200,tolerance=1e-8,print_output=False)
    print(outputs)
    obj,x1,x2 = get_results(outputs)

    # ------------------------------------------------------------------
    #   Check Results
    # ------------------------------------------------------------------

    # print results
    print(f"Objective: {obj}")
    print(f"x1: {x1}")
    print(f"x2: {x2}")
    #   Check Results
    assert abs(0.0  - obj)        < tolerance    # truth is zero; absolute error used
    assert abs(-0.1 - x1 ) / 0.1 < tolerance
    assert abs(0.0  - x2 )        < tolerance    # truth is zero; absolute error used

    # ------------------------------------------------------------------
    #   Active constraint
    # ------------------------------------------------------------------

    solver = set_add_solver()

    problem.optimization_problem.constraints = np.array([
        [ 'x1' , '>', -10., 1., 1*Units.less],
        [ 'x2' , '>',   1., 1., 1*Units.less],
    ],dtype=object)

    print('\n\n Checking basic additive with one active constraint...')
    outputs = solver.Additive_Solve(problem,max_iterations=1000,num_samples=200,tolerance=1e-8,print_output=False)
    print(outputs)
    obj,x1,x2 = get_results(outputs)

    # ------------------------------------------------------------------
    #   Check Results
    # ------------------------------------------------------------------

    # print results
    print(f"Objective: {obj}")
    print(f"x1: {x1}")
    print(f"x2: {x2}")
    #   Check Results
    assert abs(1.0  - obj) / 1.0 < tolerance
    assert abs(-0.1 - x1 ) / 0.1 < tolerance
    assert abs(1.0  - x2 ) / 1.0 < tolerance

    # ------------------------------------------------------------------
    #   Other active constraints
    # ------------------------------------------------------------------

    solver = set_add_solver()

    problem.optimization_problem.constraints = np.array([
        [ 'x1' , '=',   2., 1., 1*Units.less],
        [ 'x2' , '<',  -1., 1., 1*Units.less],
    ],dtype=object)

    print('\n\n Checking basic additive with two active constraints...')
    outputs = solver.Additive_Solve(problem,max_iterations=1000,num_samples=200,tolerance=1e-8,print_output=False)
    print(outputs)
    obj,x1,x2 = get_results(outputs)

    # ------------------------------------------------------------------
    #   Check Results
    # ------------------------------------------------------------------

    # print results
    print(f"Objective: {obj}")
    print(f"x1: {x1}")
    print(f"x2: {x2}")
    #   Check Results
    assert abs(5.41 - obj) / 5.41 < tolerance
    assert abs(2.0  - x1 ) / 2.0  < tolerance
    assert abs(-1.0 - x2 ) / 1.0  < tolerance

    ################# Additive MEI ##################################################

    # ------------------------------------------------------------------
    #   Inactive constraints
    # ------------------------------------------------------------------

    solver = set_add_solver()

    problem.optimization_problem.constraints = np.array([
        [ 'x1' , '>', -10., 1., 1*Units.less],
        [ 'x2' , '>', -50., 1., 1*Units.less],
    ],dtype=object)

    print('\n\n Checking MEI additive with no active constraint...')
    outputs = solver.Additive_Solve(problem,max_iterations=1000,num_samples=200,tolerance=1e-8,print_output=False,opt_type='MEI')
    print(outputs)
    obj,x1,x2 = get_results(outputs)

    # ------------------------------------------------------------------
    #   Check Results
    # ------------------------------------------------------------------

    # print results
    print(f"Objective: {obj}")
    print(f"x1: {x1}")
    print(f"x2: {x2}")
    #   Check Results
    assert abs(0.0  - obj)        < tolerance    # truth is zero; absolute error used
    assert abs(-0.1 - x1 ) / 0.1 < tolerance
    assert abs(0.0  - x2 )        < tolerance    # truth is zero; absolute error used

    # ------------------------------------------------------------------
    #   Active constraint
    # ------------------------------------------------------------------

    solver = set_add_solver()

    problem.optimization_problem.constraints = np.array([
        [ 'x1' , '>', -10., 1., 1*Units.less],
        [ 'x2' , '>',   1., 1., 1*Units.less],
    ],dtype=object)

    print('\n\n Checking MEI additive with one active constraint...')
    outputs = solver.Additive_Solve(problem,max_iterations=1000,num_samples=200,tolerance=1e-8,print_output=False,opt_type='MEI')
    print(outputs)
    obj,x1,x2 = get_results(outputs)

    # ------------------------------------------------------------------
    #   Check Results
    # ------------------------------------------------------------------

    # print results
    print(f"Objective: {obj}")
    print(f"x1: {x1}")
    print(f"x2: {x2}")
    #   Check Results
    assert abs(1.0  - obj) / 1.0 < tolerance
    assert abs(-0.1 - x1 ) / 0.1 < tolerance
    assert abs(1.0  - x2 ) / 1.0 < tolerance

    # ------------------------------------------------------------------
    #   Other active constraints
    # ------------------------------------------------------------------

    solver = set_add_solver()

    problem.optimization_problem.constraints = np.array([
        [ 'x1' , '=',   2., 1., 1*Units.less],
        [ 'x2' , '<',  -1., 1., 1*Units.less],
    ],dtype=object)

    print('\n\n Checking MEI additive with two active constraints...')
    outputs = solver.Additive_Solve(problem,max_iterations=1000,num_samples=200,tolerance=1e-8,print_output=False,opt_type='MEI')
    print(outputs)
    obj,x1,x2 = get_results(outputs)

    # ------------------------------------------------------------------
    #   Check Results
    # ------------------------------------------------------------------

    # print results
    print(f"Objective: {obj}")
    print(f"x1: {x1}")
    print(f"x2: {x2}")
    #   Check Results
    assert abs(5.41 - obj) / 5.41 < tolerance
    assert abs(2.0  - x1 ) / 2.0  < tolerance
    assert abs(-1.0 - x2 ) / 1.0  < tolerance

    ################# TRMM ##################################################

    tr_optimizer = 'SLSQP'

    # ------------------------------------------------------------------
    #   Inactive constraints
    # ------------------------------------------------------------------

    problem.optimization_problem.constraints = np.array([
        [ 'x1' , '>', -10., 1., 1*Units.less],
        [ 'x2' , '>', -50., 1., 1*Units.less],
    ],dtype=object)

    tr = Trust_Region()
    problem.trust_region = tr
    TRM_opt = tro.Trust_Region_Optimization()
    TRM_opt.trust_region_max_iterations           = 100
    TRM_opt.optimizer  = tr_optimizer
    print('\n\n Checking TRMM with no active constraints...')
    outputs = TRM_opt.optimize(problem,print_output=False)
    print(outputs)
    obj,x1,x2 = get_results(outputs)

    # ------------------------------------------------------------------
    #   Check Results
    # ------------------------------------------------------------------

    # print results
    print(f"Objective: {obj}")
    print(f"x1: {x1}")
    print(f"x2: {x2}")
    #   Check Results
    assert abs(0.0  - obj)        < tolerance    # truth is zero; absolute error used
    assert abs(-0.1 - x1 ) / 0.1 < tolerance
    assert abs(0.0  - x2 )        < tolerance    # truth is zero; absolute error used

    # ------------------------------------------------------------------
    #   Active constraint
    # ------------------------------------------------------------------

    problem.optimization_problem.constraints = np.array([
        [ 'x1' , '>', -10., 1., 1*Units.less],
        [ 'x2' , '>',   1., 1., 1*Units.less],
    ],dtype=object)

    tr = Trust_Region()
    problem.trust_region = tr
    TRM_opt = tro.Trust_Region_Optimization()
    TRM_opt.trust_region_max_iterations           = 100
    TRM_opt.optimizer  = tr_optimizer
    print('\n\n Checking TRMM with one active constraint...')
    outputs = TRM_opt.optimize(problem,print_output=False)
    print(outputs)
    obj,x1,x2 = get_results(outputs)

    # ------------------------------------------------------------------
    #   Check Results
    # ------------------------------------------------------------------

    # print results
    print(f"Objective: {obj}")
    print(f"x1: {x1}")
    print(f"x2: {x2}")
    #   Check Results
    assert abs(1.0  - obj) / 1.0 < tolerance
    assert abs(-0.1 - x1 ) / 0.1 < tolerance
    assert abs(1.0  - x2 ) / 1.0 < tolerance

    # ------------------------------------------------------------------
    #   Other constraints
    # ------------------------------------------------------------------

    problem.optimization_problem.constraints = np.array([
        [ 'x1' , '=',   2., 1., 1*Units.less],
        [ 'x2' , '<',  -1., 1., 1*Units.less],
    ],dtype=object)

    tr = Trust_Region()
    problem.trust_region = tr
    TRM_opt = tro.Trust_Region_Optimization()
    TRM_opt.trust_region_max_iterations           = 100
    TRM_opt.optimizer  = tr_optimizer
    print('\n\n Checking TRMM with active constraints...')
    outputs = TRM_opt.optimize(problem,print_output=False)
    print(outputs)
    obj,x1,x2 = get_results(outputs)

    # removes files from folder after regression is completed
    os.remove("add_hist.txt")
    os.remove("TRM_hist.txt")

    # ------------------------------------------------------------------
    #   Check Results
    # ------------------------------------------------------------------

    # print results
    print(f"Objective: {obj}")
    print(f"x1: {x1}")
    print(f"x2: {x2}")
    #   Check Results
    assert abs(5.41 - obj) / 5.41 < tolerance
    assert abs(2.0  - x1 ) / 2.0  < tolerance
    assert abs(-1.0 - x2 ) / 1.0  < tolerance

    return

# ----------------------------------------------------------------------        
#   Inputs, Objective, & Constraints
# ----------------------------------------------------------------------  

def setup():

    nexus = Nexus()
    problem = Data()
    nexus.optimization_problem = problem

    # -------------------------------------------------------------------
    # Inputs
    # -------------------------------------------------------------------

    #   [ tag                            , initial, (lb,ub)             , scaling , units ]
    problem.inputs = np.array([
        [ 'x1'  ,  1.  , (   -2.   ,   2.   )  ,   1.   , 1*Units.less],
        [ 'x2'  ,  1.  , (   -2.   ,   2.   )  ,   1.   , 1*Units.less],
    ],dtype=object)
    
    # -------------------------------------------------------------------
    # Objective
    # -------------------------------------------------------------------

    # throw an error if the user isn't specific about wildcards
    # [ tag, scaling, units ]
    problem.objective = np.array([
        ['y',1.,1*Units.less]
    ],dtype=object)
    
    # -------------------------------------------------------------------
    # Constraints
    # -------------------------------------------------------------------
    
    # [ tag, sense, edge, scaling, units ]
    problem.constraints = np.array([
        [ 'x1' , '>', -10., 1., 1*Units.less],
        [ 'x2' , '>', -50., 1., 1*Units.less],
    ],dtype=object)
    
    # -------------------------------------------------------------------
    #  Aliases
    # -------------------------------------------------------------------
    
    # [ 'alias' , ['data.path1.name','data.path2.name'] ]

    # don't set wing_area for initial configuration so that values can be used later
    problem.aliases = [
        [ 'x1'                        ,    'vehicle_configurations.base.x1'       ],
        [ 'x2'                        ,    'vehicle_configurations.base.x2'       ],
        [ 'y'                         ,    'obj'                            ],
    ]    
    
    # -------------------------------------------------------------------
    #  Vehicles
    # -------------------------------------------------------------------
    nexus.vehicle_configurations = vehicle_multifidelity.setup()
    
    
    # -------------------------------------------------------------------
    #  Analyses
    # -------------------------------------------------------------------
    nexus.analyses = None
    
    
    # -------------------------------------------------------------------
    #  Missions
    # -------------------------------------------------------------------
    nexus.missions = None
    
    
    # -------------------------------------------------------------------
    #  Procedure
    # -------------------------------------------------------------------    
    nexus.procedure = procedure_multifidelity.setup()
    
    # -------------------------------------------------------------------
    #  Summary
    # -------------------------------------------------------------------    
    nexus.summary = Data()    
    nexus.total_number_of_iterations = 0
    return nexus

def get_results(outputs):
    obj = outputs[0]   
    x1  = outputs[1][0] 
    x2  = outputs[1][1] 
    return obj, x1, x2

if __name__ == '__main__':
    main()
    
    
