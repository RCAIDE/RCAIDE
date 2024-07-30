# RCAIDE/Library/Methods/Aerodynamics/Common/Lift/compute_airfoil_section_coefficients.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports 
from RCAIDE.Framework.Core import interp2d

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  compute_section_coefficients
# ----------------------------------------------------------------------------------------------------------------------   
def compute_section_coefficients(beta,c,r,R,B,Wa,Wt,a,nu,airfoils,a_loc,ctrl_pts,Nr,Na,t_c,use_2d_analysis):
    """ Computes the aerodynamic properties at sectional blade locations for the blade element theory analysis. 

    Assumptions:
        If airfoil geometry and locations are specified, the forces are computed using the airfoil polar lift
        and drag surrogates, accounting for the local Reynolds number and local angle of attack.
        If the airfoils are not specified, an approximation of DAE51 data at RE=50k for Cdis used

    Source:
        None

    Args:
       beta             (numpy.ndaray) :  blade twist distribution                        [unitless]
       c                (numpy.ndaray) :  chord distribution                              [unitless]
       r                (numpy.ndaray) :  radius distribution                             [unitless]
       R                       (float) :  tip radius                                      [unitless]
       B                         (int) :  number of rotor blades                          [unitless] 
       Wa               (numpy.ndaray) :  axial velocity                                  [rad/s]
       Wt               (numpy.ndaray) :  tangential velocity                             [m/s]
       a                (numpy.ndaray) :  speed of sound                                  [m/s]
       nu               (numpy.ndaray) :  viscosity                                       [Pa-s]
       airfoil_data             (dict) :  Data structure of airfoil polar information     [-]
       ctrl_pts                  (int) :  Number of control points                        [unitless]
       Nr                        (int) :  Number of radial blade sections                 [unitless]
       Na                        (int) :  Number of azimuthal blade stations              [unitless]
       t_c              (numpy.ndaray) :  Thickness to chord                              [unitless]
       use_2d_analysis       (boolean) :  Specifies 2d disc vs. 1d single angle analysis  [Boolean]

    Returns:
       Cl               (numpy.ndaray) :  Lift Coefficients                         [unitless]
       Cdval            (numpy.ndaray) :  Drag Coefficients  (before scaling)       [unitless]
       AoA              (numpy.ndaray) :  section local angle of attack             [rad]
       Ma               (numpy.ndaray) :  Mach Numner                               [unitless]
       W                (numpy.ndaray) :  Sectional velocitty                       [m/s]
       Re               (numpy.ndaray) :  Reynolds Number                           [unitless] 
    """ 
    AoA      = beta - np.arctan2(Wa,Wt)
    W        = (Wa*Wa + Wt*Wt)**0.5
    Ma       = W/a
    Re       = (W*c)/nu

    # If propeller airfoils are not defined, use empirical fit 
    if a_loc == None:    
        # Estimate Cl max
        t_c_1      = t_c*100
        Cl_max_ref = -0.0009*t_c_1**3 + 0.0217*t_c_1**2 - 0.0442*t_c_1 + 0.7005
        Cl_max_ref[Cl_max_ref<0.7] = 0.7
        Re_ref     = 9.*10**6
        Cl1maxp    = Cl_max_ref * ( Re / Re_ref ) **0.1

        # If not airfoil polar provided, use 2*pi as lift curve slope
        Cl                 = 2.*np.pi*AoA 
        Cl[Cl>Cl1maxp]     = Cl1maxp[Cl>Cl1maxp] # use Cl max value 
        Cl[AoA>=np.pi/2] = 0. # stall if blade angle is greater than 90 degrees 

        # Apply Karmen_Tsien Mach scaling 
        KT_cond         = np.logical_and((Ma[:,:]<1.),(Cl>0))
        Cl[KT_cond]     = Cl[KT_cond]/((1-Ma[KT_cond]*Ma[KT_cond])**0.5+((Ma[KT_cond]*Ma[KT_cond])/(1+(1-Ma[KT_cond]*Ma[KT_cond])**0.5))*Cl[KT_cond]/2) 
        Cl[Ma[:,:]>=1.] = Cl[Ma[:,:]>=1.] # If the blade segments are supersonic, don't scale

        # DAE51 data Approximation
        Cdval = (0.108*(Cl**4)-0.2612*(Cl**3)+0.181*(Cl**2)-0.0139*Cl+0.0278)*((50000./Re)**0.2)
        Cdval[AoA>=np.pi/2] = 2. # limit if blade angle is greater than 90 degrees
        
    else: 
        # Compute blade Cl and Cd distribution from the airfoil data 
        if use_2d_analysis:# return the 2D Cl and CDval of shape (ctrl_pts, Nr, Na)
            Cl      = np.zeros((ctrl_pts,Nr,Na))
            Cdval   = np.zeros((ctrl_pts,Nr,Na))
            for jj,airfoil in enumerate(airfoils):
                pd              = airfoil.polars
                Cl_af           = interp2d(Re,AoA,pd.reynolds_numbers, pd.angle_of_attacks, pd.lift_coefficients) 
                Cdval_af        = interp2d(Re,AoA,pd.reynolds_numbers, pd.angle_of_attacks, pd.drag_coefficients)
                locs            = np.where(np.array(a_loc) == jj )
                Cl[:,locs,:]    = Cl_af[:,locs,:]
                Cdval[:,locs,:] = Cdval_af[:,locs,:]
        else: # return the 1D Cl and CDval of shape (ctrl_pts, Nr)
            Cl      = np.zeros((ctrl_pts,Nr))
            Cdval   = np.zeros((ctrl_pts,Nr)) 
            for jj,airfoil in enumerate(airfoils):
                pd            = airfoil.polars
                Cl_af         = interp2d(Re,AoA,pd.reynolds_numbers, pd.angle_of_attacks, pd.lift_coefficients)
                Cdval_af      = interp2d(Re,AoA,pd.reynolds_numbers, pd.angle_of_attacks, pd.drag_coefficients)
                locs          = np.where(np.array(a_loc) == jj )
                Cl[:,locs]    = Cl_af[:,locs]
                Cdval[:,locs] = Cdval_af[:,locs]        
        
    # prevent zero Cl to keep Cd/Cl from breaking in BET
    Cl[Cl==0] = 1e-12

    return Cl, Cdval, AoA, Ma, W, Re  

# ----------------------------------------------------------------------------------------------------------------------
#  compute_inflow_and_tip_loss
# ----------------------------------------------------------------------------------------------------------------------   
def compute_inflow_and_tip_loss(r,R,Wa,Wt,B,et1=1.0,et2=1.0,et3=1.0):
    """ Computes the inflow, lamdaw, and the tip loss factor, F.

    Assumptions:
        None

    Source:
        None

    Args:
       r       (numpy.ndarray) : radius distribution                     [m]
       R       (numpy.ndarray) : tip radius                              [m]
       Wa      (numpy.ndarray) : axial velocity                          [m/s]
       Wt      (numpy.ndarray) : tangential velocity                     [m/s]
       B                 (int) :  number of rotor blades                 [unitless]
       et1             (float) : tuning parameter for tip loss function  [unitless]
       et2             (float) : tuning parameter for tip loss function  [unitless]
       et3             (float) : tuning parameter for tip loss function  [unitless]
       
    Returns:               
       lamdaw   (numpy.ndarray) :  inflow ratio                                                     [unitless]
       F        (numpy.ndarray) :  tip loss factor                                                  [unitless]
       piece    (numpy.ndarray) :  output of a step in tip loss calculation (needed for residual)   [unitless]
    """
    lamdaw             = r*Wa/(R*Wt)
    lamdaw[lamdaw<=0.] = 1e-12 
    tipfactor          = B/2.0*(  (R/r)**et1 - 1  )**et2/lamdaw**et3  
    piece              = np.exp(-tipfactor)
    Ftip               = 2.*np.arccos(piece)/np.pi   

    return lamdaw, Ftip, piece