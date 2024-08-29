# RCAIDE/Library/Methods/Mass/Correlation/Transport/landing_gear.py
# (c) Copyright 2024 Aerospace Research Community LLC#
# Created:  May 2024, J. Smart
# Modified: 
# -------------------------------------------------------------------------------
#  Imports
# -------------------------------------------------------------------------------

# TODO: ADD IMPORTS

# -------------------------------------------------------------------------------
#  Functional/Library Version
# -------------------------------------------------------------------------------

def func_landing_gear(*args,
                      **kwargs
                      ):
    """
    Library version of landing_gear.
    
    Parameters
    ----------
    
    args : type
        Description of arguments
    
    kwargs : type
        Description of keyword arguments
                
    Returns
    -------
    output : type
        Description of outputs
       
    See Also
    --------
    code :
        Description of related functions
    
    Notes
    -----
    Details/explanation of what this function implements. [1]
    
    References
    ----------
    [1] Reference to works cited in the Notes section
    
    Examples
    --------
    func_landing_gear():
        Example output
    
    Description of example.  
    
    """

    # TODO: Implement functional version of landing_gear

    return results


# -------------------------------------------------------------------------------
#  Stateful/Framework Version
# -------------------------------------------------------------------------------

def landing_gear(State, Settings, System):
    """
    Framework version of landing_gear
    
    See Also
    --------
    func_landing_gear: 
        Functional implementation which this method calls.
    """

    # TODO: Unpack functional arguments

    results = func_landing_gear(*args,
                                **kwargs
                                )

    # TODO: Unpack results

    return State, Settings, System
