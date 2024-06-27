## @ingroup Library-Methods-Performance
# RCAIDE/Library/Methods/Performance/estimate_stall_speed.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
import RCAIDE
 
# Pacakge imports 
import numpy as np  

#------------------------------------------------------------------------------
# Stall Speed Estimation
#------------------------------------------------------------------------------

## @ingroup Library-Methods-Performance
def estimate_stall_speed(vehicle_mass,reference_area,altitude,maximum_lift_coefficient):

    """Calculates the stall speed of an aircraft at a given altitude and a maximum lift coefficient.

        Sources:
        None

        Assumptions:
        None 

        Args:
            vehicle_mass                    vehicle mass             [kg]
            reference_area                  vehicle reference area   [m^2] 
            altitude                        cruise altitude          [m]
            maximum_lift_coefficient        maximum lift coefficient [unitless] 
            
        Returns: 
            V_stall                         stall speed              [m/s]
    """ 
      
    g       = 9.81 
    atmo    = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    rho     = atmo.compute_values(altitude,0.).density 
    V_stall = float(np.sqrt(2.*vehicle_mass*g/(rho*reference_area*maximum_lift_coefficient)))  
    
    return V_stall