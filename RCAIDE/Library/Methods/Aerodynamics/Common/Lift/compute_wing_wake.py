# RCAIDE/Library/Methods/Aerodynamics/Common/Lift/compute_wing_wake.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 
# 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import RCAIDE
from RCAIDE.Framework.Core  import Data
from RCAIDE.Library.Methods.Aerodynamics.Vortex_Lattice_Method.Vortex_Lattice_Method import Vortex_Lattice_Method
from RCAIDE.Library.Methods.Aerodynamics.Vortex_Lattice_Method.Vortex_Lattice_Method import compute_wing_induced_velocity
from RCAIDE.Library.Methods.Aerodynamics.Common.Lift                                 import generate_wing_wake_grid

# python imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Compute Wing Wake 
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_wing_wake(vehicle, conditions, X_wake, grid_settings, VLM_settings,evaluation_points=None,viscous_wake=True):
    """ Computes the wing-induced velocities at a given x-plane.
    
     Assumptions:
         None
         
     Sources:
         None 
    
     Args:
          vehicle             (dict): aircraft data structure                    [Unitless]
          conditions          (dict): flight conditions                          [Unitless]
          X_wake             (float): streamwise location for evaluating wake    [m]
          viscous_wake     (boolean): flag for using viscous wake correction     [Boolean]
          grid_settings       (dict): settings of VLM analysis                   [-]
     
     Returns:
          wing_wake
            .u_velocities  (numpy.ndarray): streamwise induced velocities at control points           [m/s]
            .v_velocities  (numpy.ndarray): spanwise induced velocities at control points             [m/s]
            .w_velocities  (numpy.ndarray): induced downwash at control points                        [m/s]
            .VD            (numpy.ndarray): vortex distribution of wing and control points in wake    [Unitless]
          results                   (dict): vortex lattice method results                             [Unitless]

    """     
     
    # use main main for as reference wing else use largest wing
    s_ref   = 0
    span    = 0
    croot   = 0
    ctip    = 0
    x0_wing = 0
    for wing in  vehicle.wings:
        if type(wing) ==  RCAIDE.Library.Components.Wings.Main_Wing: 
            span      = wing.spans.projected
            croot     = wing.chords.root
            ctip      = wing.chords.tip
            x0_wing   = wing.origin[0,0] 
        else:
            if s_ref <  wing.areas.reference:
                s_ref   = wing.areas.reference
                span    = wing.spans.projected 
                croot   = wing.chords.root 
                ctip    = wing.chords.tip  
                x0_wing = wing.origin[0,0] 

    mach      = conditions.freestream.mach_number
    rho       = conditions.freestream.density[0,0]
    Vv        = conditions.freestream.velocity[0,0]
    mu        = conditions.freestream.dynamic_viscosity[0,0] 
    nu        = mu/rho 
    H         = grid_settings.height
    L         = grid_settings.length
    H_f       = grid_settings.height_fine
     
    # Run the VLM for the given vehicle and conditions  
    results = Vortex_Lattice_Method(conditions,VLM_settings, vehicle)
    gamma   = results.gamma
    VD      = vehicle.vortex_distribution  
    gammaT  = gamma.T
     
    #  Generate grid points to evaluate wing induced velocities 
    if evaluation_points == None:
        grid_points = generate_wing_wake_grid(vehicle, H, L, H_f, X_wake) 
        VD.XC = grid_points.XC
        VD.YC = grid_points.YC
        VD.ZC = grid_points.ZC 
    else:
        VD.XC = evaluation_points.X
        VD.YC = evaluation_points.Y
        VD.ZC = evaluation_points.Z
     
    # Compute wing induced velocity      
    C_mn, _, _, _ = compute_wing_induced_velocity(VD,mach)     
    u_inviscid    = (C_mn[:,:,:,0]@gammaT)[0,:,0]
    v_inviscid    = (C_mn[:,:,:,1]@gammaT)[0,:,0]
    w_inviscid    = (C_mn[:,:,:,2]@gammaT)[0,:,0]     
     
    # Impart the wake deficit from BL of wing if x is behind the wing 
    Va_deficit = np.zeros_like(VD.YC) 
    if viscous_wake and (X_wake>=x0_wing):
        
        # impart viscous wake to grid points within the span of the wing
        y_inside            = abs(VD.YC)<0.5*span
        chord_distribution  = croot - (croot-ctip)*(abs(VD.YC[y_inside])/(0.5*span))
        
        # Reynolds number developed at x-plane:
        Rex_prop_plane     = Vv*(VD.XC[y_inside]-x0_wing)/nu
        
        # boundary layer development distance
        x_dev      = np.ones_like(chord_distribution) * (VD.XC[y_inside]-x0_wing)  
        
        # For turbulent flow
        theta_turb  = 0.036*x_dev/(Rex_prop_plane**(1/5))
        x_theta     = (x_dev-chord_distribution)/theta_turb

        # axial velocity deficit due to turbulent BL from the wing (correlation from Ramaprian et al.)
        W0  = Vv/np.sqrt(4*np.pi*0.032*x_theta)
        b   = 2*theta_turb*np.sqrt(16*0.032*np.log(2)*x_theta)
        Va_deficit[y_inside] = W0*np.exp(-4*np.log(2)*(abs(VD.ZC[y_inside])/b)**2) 
  
    wing_wake = Data()
    wing_wake.u_velocities = u_inviscid - Va_deficit/Vv
    wing_wake.v_velocities = v_inviscid
    wing_wake.w_velocities = w_inviscid
    wing_wake.VD           = VD         
    
    return wing_wake, results