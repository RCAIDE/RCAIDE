# RCAIDE/Library/Missions/Segments/converge_root.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# Package imports 
import scipy.optimize
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# converge root
# ---------------------------------------------------------------------------------------------------------------------- 
def converge_root(segment):
    """Interfaces the mission to a numerical solver. The solver may be changed by using root_finder.

    Assumptions:
    None

    Source:
    None

    Args:
    segment                            [Data]
    segment.settings.root_finder       [Data]
    state.numerics.tolerance_solution  [unitless]

    Returns:
    state.unknowns                     [Any]
    segment.state.numerics.converged   [unitless]


    """       
    
    unknowns = segment.state.unknowns.pack_array()
    
    try:
        root_finder = segment.settings.root_finder
    except AttributeError:
        root_finder = scipy.optimize.fsolve 
    
    unknowns,infodict,ier,msg = root_finder( iterate,
                                         unknowns,
                                         args = segment,
                                         xtol = segment.state.numerics.tolerance_solution,
                                         maxfev = segment.state.numerics.max_evaluations,
                                         epsfcn = segment.state.numerics.step_size,
                                         full_output = 1)
    
    if ier!=1:
        print("Segment did not converge. Segment Tag: " + segment.tag)
        print("Error Message:\n" + msg)
        segment.state.numerics.converged = False
        segment.converged = False
    else:
        segment.state.numerics.converged = True
        segment.converged = True
                            
    return
    
# ---------------------------------------------------------------------------------------------------------------------- 
#  Helper Functions
# ----------------------------------------------------------------------------------------------------------------------  
def iterate(unknowns, segment):
    
    """Runs one iteration of of all analyses for the mission.

    Assumptions:
    None

    Source:
    None

    Args:
    state.unknowns                [Data]
    segment.process.iterate       [Data]

    Returns:
    residuals                     [unitless]


    """       
    if isinstance(unknowns,np.ndarray):
        segment.state.unknowns.unpack_array(unknowns)
    else:
        segment.state.unknowns = unknowns
        
    segment.process.iterate.evaluate(segment)
    
    residuals = segment.state.residuals.pack_array()
        
    return residuals 