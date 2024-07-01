## @ingroup Library-Methods-Energy-Sources-Battery-Ragone
# RCAIDE/Library/Methods/Energy/Sources/Battery/Ragone/compute_ragone_optimum.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from .  import compute_ragone_properties

# package imports 
import scipy as sp

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Ragone Optimium 
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Energy-Sources-Battery-Ragone
def compute_ragone_optimum(battery, energy, power):
    """ Uses Brent's Bracketing Method to find an optimum-mass battery based on the 
    specific energy and specific power of the battery determined from the battery's ragone plot.
    
    Assumptions:
    Specific power can be modeled as a curve vs. specific energy of the form c1*10**(c2*specific_energy)
    
    Args:
        battery   (dict): battery data structure[-]
        energy   (float): energy                [J]
        power    (float): power                 [W]
                
    Returns:
        None 
    """ 
    
    lb = battery.ragone.lower_bound
    ub = battery.ragone.upper_bound

    #optimize!
    specific_energy_opt = sp.optimize.fminbound(compute_ragone_properties, lb, ub, args=( battery, energy, power), xtol=1e-12)
    
    # now initialize the battery with the new optimum properties
    compute_ragone_properties(specific_energy_opt, battery, energy, power)
    
    return 