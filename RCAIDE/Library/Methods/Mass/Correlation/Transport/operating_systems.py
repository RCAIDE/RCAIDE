# RCAIDE/Library/Methods/Mass/Correlation/Transport/operating_systems.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created:  May 2024, J. Smart
# Modified:

# ----------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------- 

# TODO: ADD IMPORTS

# -----------------------------------------------------------------------
# Functional/Library Version
# -----------------------------------------------------------------------

def func_operating_systems(aircraft_type : str = 'medium-range'
                           , *args, **kwargs):



    ac_types = ['short-range',
                'medium-range',
                'long-range',
                'business-jet',
                'cargo',
                'commuter',
                'sst']



    operitems

    return results


# -----------------------------------------------------------------------
# Stateful/Framework Version
# -----------------------------------------------------------------------

def operating_systems(State, Settings, System):
    # TODO: Unpack State, Settings, System to the functional arguments

    results = func_operating_systems(*args, **kwargs)
    # TODO: [Replace 'results' with the output of the functional version]

    # TODO: Pack 'results' into State, Settings, System

    return State, Settings, System
