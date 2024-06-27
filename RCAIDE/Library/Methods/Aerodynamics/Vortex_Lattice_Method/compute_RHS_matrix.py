## @ingroup Library-Methods-Aerdoynamics-Vortex_Lattice_Method
# RCAIDE/Library/Methods/Aerodynamics/Vortex_Lattice_Method/compute_RHS_matrix.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
#
# Created:  Aug 2018, M. Clarke
# Modified: Apr 2020, M. Clarke
#           Jun 2021, R. Erhard
#           Jul 2021, A. Blaufox
#           Jul 2021, E. Botero
#           Jul 2021, R. Erhard
#           Feb 2022, R. Erhard
#           Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports
from RCAIDE.Framework.Core import Data 

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  compute_section_coefficients
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Library-Methods-Aerdoynamics-Vortex_Lattice_Method
def compute_RHS_matrix(delta,phi,conditions,settings,geometry,propeller_wake_model): 
    """ This computes the right hand side matrix for the VLM. In this function,
        induced velocites from propeller wake are also included when relevent and
        where specified

    Source:
        1. Low-Speed Aerodynamics, Second Edition by Joseph Katz, Allen Plotkin, Pgs. 331-338 

        2. VORLAX Source Code

    Args:
        delta                                    (numpy.ndarray) : flow tangency angles        [radians]
        phi                                      (numpy.ndarray) : flow tangency angles        [radians] 
        conditions.aerodynamics.angles.alpha     (numpy.ndarray) : angle of attack             [radians]
        conditions.aerodynamics.angles.beta      (numpy.ndarray) : sideslip angle              [radians]
        conditions.freestream.velocity           (numpy.ndarray) : velocity                    [m/s]
        conditions.static_stability.pitch_rate   (numpy.ndarray) : pitch_rat                   [radians/s]
        conditions.static_stability.roll_rate    (numpy.ndarray) : roll_rate                   [radians/s]
        conditions.static_stability.yaw_rate     (numpy.ndarray) : yaw_rate                    [radians/s]
        settings.use_VORLAX_matrix_calculation         (boolean) : vlm flag                    [unitless]
        propeller_wake_model                           (boolean) : propeller_wake_model flag   [unitless]

    Returns:
       rhs.
           RHS              (numpy.ndarray) : Right hand side matrix of VLM [unitless] 
           ONSET            (numpy.ndarray) : VLM properties                [unitless] 
           Vx_ind_total     (numpy.ndarray) : induced velocity distribution [m/s] 
           Vz_ind_total     (numpy.ndarray) : induced velocity distribution [m/s] 
           V_distribution   (numpy.ndarray) : induced velocity distribution [m/s] 
           dt               (numpy.ndarray) : VLM properties                [unitless] 
           YGIRO            (numpy.ndarray) : VLM properties                [unitless] 
           ZGIRO            (numpy.ndarray) : VLM properties                [unitless] 
           VX               (numpy.ndarray) : VLM properties                [m/s] 
           SCNTL            (numpy.ndarray) : VLM properties                [unitless] 
           CCNTL            (numpy.ndarray) : VLM properties                [unitless] 
           COD              (numpy.ndarray) : VLM properties                [unitless] 
           SID              (numpy.ndarray) : VLM properties                [unitless]    
    """

    # unpack
    VD               = geometry.vortex_distribution 
    aoa              = conditions.aerodynamics.angles.alpha
    PSI              = conditions.aerodynamics.angles.beta
    V_inf            = conditions.freestream.velocity
    num_ctrl_pts     = len(aoa)  
    num_eval_pts     = len(VD.XC)
    aoa_distribution = np.repeat(aoa, VD.n_cp, axis = 1)
    PSI_distribution = np.repeat(PSI, VD.n_cp, axis = 1)
    V_distribution   = np.repeat(V_inf , VD.n_cp, axis = 1) 
    rot_V_wake_ind   = np.zeros((len(aoa), VD.n_cp,3))
    prop_V_wake_ind  = np.zeros((len(aoa), VD.n_cp,3))
    Vx_ind_total     = np.zeros_like(V_distribution)
    Vy_ind_total     = np.zeros_like(V_distribution)
    Vz_ind_total     = np.zeros_like(V_distribution) 
    dt               = 0
    
    if propeller_wake_model:     
        prop_V_wake_ind = np.zeros((num_ctrl_pts,num_eval_pts,3)) 
        rot_V_wake_ind = np.zeros((num_ctrl_pts,num_eval_pts,3))       
        for network in geometry.networks: 
            if 'busses' in network:  
                for bus in network.busses:
                    for propulsor in bus.propulsors:  
                        if 'rotor' in propulsor:
                            r =  propulsor.rotor
                            rot_V_wake_ind += r.Wake.evaluate_slipstream(p,geometry,num_ctrl_pts) 
                        if 'propeller' in propulsor:
                            p =  propulsor.propeller
                            prop_V_wake_ind += p.Wake.evaluate_slipstream(p,geometry,num_ctrl_pts)
                             
         
            if 'fuel_lines' in network:  
                for fuel_line in network.fuel_lines:
                    for propulsor in fuel_line.propulsors: 
                        if 'rotor' in propulsor: 
                            r =  propulsor.rotor
                            rot_V_wake_ind += r.Wake.evaluate_slipstream(r,geometry,num_ctrl_pts) 
                        if 'propeller' in propulsor: 
                            p =  propulsor.propeller
                            prop_V_wake_ind += p.Wake.evaluate_slipstream(p,geometry,num_ctrl_pts)   
                     
        # update the total induced velocity distribution
        Vx_ind_total = Vx_ind_total + prop_V_wake_ind[:,:,0] + rot_V_wake_ind[:,:,0]
        Vy_ind_total = Vy_ind_total + prop_V_wake_ind[:,:,1] + rot_V_wake_ind[:,:,1]
        Vz_ind_total = Vz_ind_total + prop_V_wake_ind[:,:,2] + rot_V_wake_ind[:,:,2]

        rhs = build_RHS(VD, conditions, settings, aoa_distribution, delta, phi, PSI_distribution,
                        Vx_ind_total, Vy_ind_total, Vz_ind_total, V_distribution, dt)      
        return  rhs

    rhs = build_RHS(VD, conditions, settings, aoa_distribution, delta, phi, PSI_distribution,
                    Vx_ind_total, Vy_ind_total, Vz_ind_total, V_distribution, dt)
    
    return rhs 

def build_RHS(VD, conditions, settings, aoa_distribution, delta, phi, PSI_distribution,
              Vx_ind_total, Vy_ind_total, Vz_ind_total, V_distribution, dt):
    """ This uses freestream conditions, induced wake velocities, and rotation
        rates (pitch, roll, yaw) to find the boundary conditions (RHS) needed to
        compute gamma. The function defaults to a classical boundary condition
        equation, RHS = V dot N, where V is the unit velocity vector only the panel
        and N is the panel unit normal. However, the user may also define
        settings.use_VORLAX_matrix_calculation to use the boundary condition equation
        from VORLAX, the code on which this VLM is based. This is useful for future
        developers who need to compare numbers 1:1 with VORLAX.
        
    Assumtions   
        Note if using VORLAX boundary conditions:
        VORLAX does not take induced wake velocity into account. Additionally,
        VORLAX uses the camber, twist, and dihedral values of a strip's leading
        edge panel for every panel in that strip when calculating panel normals.

    Source:
        1. Low-Speed Aerodynamics, Second Edition by Joseph Katz, Allen Plotkin Pgs. 331-338
     
        2. VORLAX Source Code

    Args:
        settings.use_VORLAX_matrix_calculation  (numpy.ndarray) RHS equation switch               [boolean]
        conditions.static_stability.pitch_rate  (numpy.ndarray)                                   [radians/s]
        conditions.static_stability.roll_rate   (numpy.ndarray)                                   [radians/s]
        conditions.static_stability.yaw_rate    (numpy.ndarray)                                   [radians/s]
        aoa_distribution                        (numpy.ndarray) angle of attack                   [radians]
        PSI_distribution                        (numpy.ndarray) sideslip angle                    [radians]
        V[]_ind_total                           (numpy.ndarray) component induced wake velocities [m/s]
        V_distribution                          (numpy.ndarray) freestream velocity magnitude     [m/s]
        delta, phi                              (numpy.ndarray) flow tangency angles              [radians]

    Returns:
        rhs  (dict):  a Data object used to hold several values including RHS [-]
    """
    LE_ind      = VD.leading_edge_indices
    RNMAX       = VD.panels_per_strip


    # VORLAX frame RHS calculation---------------------------------------------------------
    #VORLAX subroutine = BOUNDY
    #unpack conditions
    ALFA   = aoa_distribution
    PSIRAD = PSI_distribution
    PITCHQ = conditions.static_stability.pitch_rate
    ROLLQ  = conditions.static_stability.roll_rate
    YAWQ   = conditions.static_stability.yaw_rate
    VINF   = conditions.freestream.velocity

    SINALF = np.sin(ALFA)
    COSIN  = np.cos(ALFA) * np.sin(PSIRAD)
    COSCOS = np.cos(ALFA) * np.cos(PSIRAD)
    PITCH  = PITCHQ / VINF
    ROLL   = ROLLQ  / VINF
    YAW    = YAWQ   / VINF

    #unpack/rename variables from VD
    X      = VD.XCH
    YY     = VD.YCH
    ZZ     = VD.ZCH
    XBAR   = VD.XBAR
    ZBAR   = VD.ZBAR

    CHORD  = VD.chord_lengths[0,:]
    DELTAX = 0.5/RNMAX

    # LOCATE VORTEX LATTICE CONTROL POINT WITH RESPECT TO THE
    # ROTATION CENTER (XBAR, 0, ZBAR). THE RELATIVE COORDINATES
    # ARE XGIRO, YGIRO, AND ZGIRO.
    XGIRO = X + CHORD*DELTAX - np.repeat(XBAR, RNMAX[LE_ind])
    YGIRO = YY
    ZGIRO = ZZ - np.repeat(ZBAR, RNMAX[LE_ind])

    # VX, VY, VZ ARE THE FLOW ONSET VELOCITY COMPONENTS AT THE LEADING
    # EDGE (STRIP MIDPOINT). VX, VY, VZ AND THE ROTATION RATES ARE
    # REFERENCED TO THE FREE STREAM VELOCITY.
    VX = (COSCOS - PITCH*ZGIRO + YAW  *YGIRO)
    VY = (COSIN  - YAW  *XGIRO + ROLL *ZGIRO)
    VZ = (SINALF - ROLL *YGIRO + PITCH*XGIRO)
    
    #COMPUTE DIRECTION COSINES.
    SCNTL  = VD.SLOPE/np.sqrt(1. + VD.SLOPE **2)
    CCNTL  = 1. / np.sqrt(1.0 + SCNTL**2)
    phi_LE = np.repeat(phi[:,LE_ind]  , RNMAX[LE_ind], axis=1)
    COD    = np.cos(phi_LE)
    SID    = np.sin(phi_LE)

    # COMPUTE ONSET FLOW COMPONENT ALONG THE OUTWARD NORMAL TO
    # THE SURFACE AT THE CONTROL POINT, ALOC.
    ALOC  = VX *SCNTL + VY *CCNTL *SID - VZ *CCNTL *COD

    # COMPUTE VELOCITY COMPONENT ALONG X-AXIS INDUCED BY THE RIGID
    # BODY ROTATION, ONSET.
    ONSET = - PITCH *ZGIRO + YAW *YGIRO

    # Body-Frame RHS calculation----------------------------------------------------------
    # Add wake and rotation effects to the freestream
    Vx_rotation       = -PITCHQ*ZGIRO + YAWQ  *YGIRO
    Vy_rotation       = -YAWQ  *XGIRO + ROLLQ *ZGIRO
    Vz_rotation       = -ROLLQ *YGIRO + PITCHQ*XGIRO

    Vx                = V_distribution*np.cos(aoa_distribution)*np.cos(PSI_distribution) + Vx_rotation + Vx_ind_total
    Vy                = V_distribution*np.cos(aoa_distribution)*np.sin(PSI_distribution) + Vy_rotation + Vy_ind_total
    Vz                = V_distribution*np.sin(aoa_distribution)                          + Vz_rotation + Vz_ind_total    
    
    aoa_distribution  = np.arctan(Vz/ np.sqrt(Vx**2 + Vy**2) )
    PSI_distribution  = np.arctan(Vy / Vx)

    # compute RHS: dot(v, panel_normals)
    V_unit_vector    = (np.array([Vx,Vy,Vz])/V_distribution).T
    panel_normals    = VD.normals[:,np.newaxis,:]
    RHS_from_normals = np.sum(V_unit_vector*panel_normals, axis=2).T    

    #pack values--------------------------------------------------------------------------
    use_VORLAX_RHS = settings.use_VORLAX_matrix_calculation

    rhs = Data()
    rhs.RHS            = RHS_from_normals if not use_VORLAX_RHS else ALOC
    rhs.ONSET          = ONSET
    rhs.Vx_ind_total   = Vx_ind_total
    rhs.Vz_ind_total   = Vz_ind_total
    rhs.V_distribution = V_distribution
    rhs.dt             = dt 
    rhs.YGIRO          = YGIRO
    rhs.ZGIRO          = ZGIRO
    rhs.VX             = VX
    rhs.SCNTL          = SCNTL
    rhs.CCNTL          = CCNTL
    rhs.COD            = COD
    rhs.SID            = SID

    return rhs
