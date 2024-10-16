# RCAIDE/Library/Missions/Common/Update/Aerodynamics.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
import RNUMPY as rp 
    
# ----------------------------------------------------------------------------------------------------------------------
#  Update Freestream
# ----------------------------------------------------------------------------------------------------------------------
def freestream(segment):
    """ Updates the freestream conditions 
        
        Assumptions:
            None
        
        Args:
            segment.state.conditions.:
                 frames.inertial.velocity_vector   [m/s]
                 freestream.density                [kg/m^3]
                 freestream.speed_of_sound         [m/s]
                 freestream.dynamic_viscosity      [Pa-s]
        Returns:
            segment.conditions.freestream
                 velocity                          [m/s]
                 mach_number                       [-]
                 reynolds_number                   [-]
                 dynamic_pressure                  [Pa]  
    """   
    
    # unpack
    conditions = segment.state.conditions
    V          = conditions.frames.inertial.velocity_vector
    rho        = conditions.freestream.density
    a          = conditions.freestream.speed_of_sound
    mu         = conditions.freestream.dynamic_viscosity

    # velocity magnitude
    Vmag2 = rp.sum( V**2, axis=1)[:,None]  
    Vmag  = rp.sqrt(Vmag2)

    # dynamic pressure
    q = 0.5 * rho * Vmag2 # Pa

    # Mach number
    M = Vmag / a

    # Reynolds number
    Re = rho * Vmag / mu  # per m

    # pack
    conditions.freestream.velocity         = Vmag
    conditions.freestream.mach_number      = M
    conditions.freestream.reynolds_number  = Re
    conditions.freestream.dynamic_pressure = q

    return

