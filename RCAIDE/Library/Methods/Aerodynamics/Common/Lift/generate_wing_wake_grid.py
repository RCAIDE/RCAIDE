# RCAIDE/Library/Methods/Aerodynamics/Common/Lift/generate_wing_wake_grid.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# 
# Created:  Jul 2024, RCAIDE Team 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports
from RCAIDE.Framework.Core import Data
import numpy as np 


# ----------------------------------------------------------------------------------------------------------------------
#  Generate Wing Wake Grid
# ---------------------------------------------------------------------------------------------------------------------- 
def generate_wing_wake_grid(vehicle, H, L, H_f, x_plane, N_z_coarse=20, N_z_fine=35, N_y_coarse=20):
    """ Generates the grid points for evaluating the viscous wing wake in a downstream plane.
    Uses smaller grid near the wing to better capture boundary layer.
    
    Assumptions
        Main wing is symmetric
        
    Source
        None 

    Args: 
        vehicle       (dict) : vehicle data object                                   [-] 
        H             (float): Height of full grid, normalized by wing span          [m] 
        L             (float): Length of grid, normalized by wing span               [m] 
        H_f           (float): Height of finer grid portion                          [m] 
        x_plane       (float): Spanwise location of grid plane                       [m]  
        N_z_coarse      (int): Number of vertical grid points outside finer region   [unitless]
        N_z_fine        (int): Number of vertical grid points inside finer region    [unitless]
        N_y_coarse      (int): Number of horizontal grid points outside of wing span [unitless]
        
    Returns:
        grid_points   (dict): data struture of grid points                           [-]
    """ 
    # unpack
    span      = vehicle.wings.main_wing.spans.projected 
    half_span = span/2
    VD        = vehicle.vortex_distribution
    breaks    = VD.chordwise_breaks
    
    # Define bounds of grid 
    z_bot     = -H*half_span
    z_top     = H*half_span
    Nzo_half  = int(N_z_coarse/2)
    Nyo_half  = int(N_y_coarse/2)
       
    # generate vertical grid point locations
    z_outer_bot   = np.linspace(z_bot, -H_f, Nzo_half)
    z_outer_top   = np.linspace(H_f, z_top, Nzo_half)
    
    # Use finer concentration of grid points near the wing
    z_inner_bot   = -H_f*(np.flipud((1-np.cos(np.linspace(1e-6,1,N_z_fine)*np.pi/2))))
    z_inner_top   = H_f*(1-np.cos(np.linspace(0,1,N_z_fine)*np.pi/2))
    zlocs         = np.concatenate([z_outer_bot,z_inner_bot, z_inner_top, z_outer_top])

    # Generate spanwise grid point locations: placed between vortex lines to avoid discontinuities
    ypts        = VD.YC[breaks]
    y_semispan  = ypts[0:int(len(ypts)/2)]
    
    if L < 1.:
        # trim spanwise points to region of interest
        y_in       = y_semispan<(L*half_span)
        y_semispan = y_semispan[y_in]
    else: 
        # add grid points outside wingtip
        y_outerspan = np.linspace(1.01,L,Nyo_half)*half_span
        y_semispan  = np.append(y_semispan, y_outerspan)
        
    ylocs = np.concatenate([np.flipud(-y_semispan),y_semispan])
    
    # declare new control points
    cp_YC = np.repeat(ylocs,len(zlocs)) 
    cp_ZC = np.tile(zlocs,len(ylocs))
    cp_XC = np.ones_like(cp_YC)*x_plane 
    
    grid_points       = Data()
    grid_points.XC    = cp_XC
    grid_points.YC    = cp_YC
    grid_points.ZC    = cp_ZC
    grid_points.yline = ylocs
    grid_points.zline = zlocs
    
    return grid_points