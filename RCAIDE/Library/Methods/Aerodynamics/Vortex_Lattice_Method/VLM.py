
# VLM.py
# 
# Created: Aug 2025, M. Clarke    

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# package imports 
import RCAIDE
from RCAIDE.Framework.Core import Data 
from .compute_wing_induced_velocity      import compute_wing_induced_velocity
from .generate_vortex_distribution       import generate_vortex_distribution 
from .compute_RHS_matrix                 import compute_RHS_matrix

from scipy.integrate import trapezoid
from copy import  deepcopy
import numpy as np
# ----------------------------------------------------------------------
#  Vortex Lattice
# ----------------------------------------------------------------------

def VLM(conditions,settings,geometry):
    """Uses the vortex lattice method to compute the lift, induced drag and moment coefficients.
     
    The user should be forwarned that this will cause very slight differences in results for 0 deflection due to
    the slightly different discretization.
    
    The user has the option to use the boundary conditions and induced velocities from either RCAIDE
    or VORLAX. See build_RHS in compute_RHS_matrix.py for more details.
    
    By default in Vortex_Lattice, VLM performs calculations based on panel coordinates with float32 precision. 
    The user may also choose to use float16 or float64, but be warned that the latter can be memory intensive.
    
    The user should note that fully capitalized variables correspond to a VORLAX variable of the same name
    
    
    Assumptions:
    The user provides either global discretezation (number_spanwise/chordwise_vortices) or
    separate discretization (wing/fuselage_spanwise/chordwise_vortices) in settings, not both.
    The set of settings not being used should be set to None.
    
    The VLM requires that the user provide a non-zero velocity that matches mach number. For
    surrogate training cases at mach 0, VLM uses a velocity of 1e-6 m/s

    
    Source:
    1. Miranda, Luis R., Robert D. Elliot, and William M. Baker. "A generalized vortex 
    lattice method for subsonic and supersonic flow applications." (1977). (NASA CR)
    
    2. VORLAX Source Code

    
    Inputs:
    geometry.
       reference_area                          [m^2]
       wing.
         spans.projected                       [m]
         chords.root                           [m]
         chords.tip                            [m]
         sweeps.quarter_chord                  [radians]
         taper                                 [Unitless]
         twists.root                           [radians]
         twists.tip                            [radians]
         xz_plane_symmetric                    [Boolean]
         aspect_ratio                          [Unitless]
         areas.reference                       [m^2]
         vertical                              [Boolean]
         origin                                [m]
       fuselage.
        origin                                 [m]
        width                                  [m]
        heights.maximum                        [m]      
        lengths.nose                           [m]    
        lengths.tail                           [m]     
        lengths.total                          [m]     
        lengths.cabin                          [m]     
        fineness.nose                          [Unitless]
        fineness.tail                          [Unitless]
        
    settings.number_of_spanwise_vortices       [Unitless]  <---|
    settings.number_of_chordwise_vortices      [Unitless]  <---|
                                                               |--Either/or; see generate_vortex_distribution() for more details
    settings.wing_spanwise_vortices            [Unitless]  <---|
    settings.wing_chordwise_vortices           [Unitless]  <---|
    settings.fuselage_spanwise_vortices        [Unitless]  <---|
    settings.fuselage_chordwise_vortices       [Unitless]  <---|  
       
    settings.use_surrogate                     [Unitless]
    settings.propeller_wake_model              [Unitless] 
    settings.use_VORLAX_matrix_calculation     [boolean]
    settings.floating_point_precision          [float16/32/64]
       
    conditions.aerodynamics.angles.alpha       [radians]
    conditions.aerodynamics.angles.beta        [radians]
    conditions.freestream.mach_number          [Unitless]
    conditions.freestream.velocity             [m/s]
    conditions.static_stability.pitch_rate     [radians/s]
    conditions.static_stability.roll_rate      [radians/s]
    conditions.static_stability.yaw_rate       [radians/s]
       
    
    Outputs:    
    results.
        CL                                     [Unitless], CLTOT in VORLAX
        CDi                                    [Unitless], CDTOT in VORLAX
        CM                                     [Unitless], CMTOT in VORLAX
        CY                                     [Unitless], Total y force coeff
        CRTOT                                  [Unitless], Rolling moment coeff (unscaled)
        CL_mom                                 [Unitless], Rolling moment coeff (scaled by b_ref)
        CNTOT                                  [Unitless], Yawing  moment coeff (unscaled)
        CN                                     [Unitless], Yawing  moment coeff (scaled by b_ref)
        CL_wing                                [Unitless], CL  of each wing
        CDi_wing                               [Unitless], CDi of each wing
        cl_y                                   [Unitless], CL  of each strip
        cdi_y                                  [Unitless], CDi of each strip
        alpha_i                                [radians] , Induced angle of each strip in each wing (array of numpy arrays)
        CP                                     [Unitless], Pressure coefficient of each panel
        gamma                                  [Unitless], Vortex strengths of each panel

    
    Properties Used:
    N/A
    """
     
    S_ref = geometry.reference_area
    c_ref = geometry.reference_chord
    b_ref = geometry.reference_span  
    x_m   = geometry.mass_properties.center_of_gravity[0][0]
    z_m   = geometry.mass_properties.center_of_gravity[0][2] 

    # ---------------------------------------------------------------------------------------
    # Generate Panelization and Vortex Distribution
    # ------------------ -------------------------------------------------------------------- 
    VD                                                    = generate_vortex_distribution(conditions,settings,geometry) 
    settings.vortex_distribution.chord_lengths            = VD.chord_lengths[VD.leading_edge_indices].reshape(len(VD.n_sw),np.sum(VD.n_sw[0]))
    settings.vortex_distribution.n_sw                     = VD.n_sw 
    settings.vortex_distribution.n_cw                     = VD.n_cw 
    settings.vortex_distribution.n_w                      = VD.n_w 
    settings.vortex_distribution.chord_widths             = VD.chord_widths 
    settings.vortex_distribution.leading_edge_sweeps      = VD.leading_edge_sweeps 
    settings.vortex_distribution.XA1                      = VD.XA1
    settings.vortex_distribution.XA2                      = VD.XA2
    settings.vortex_distribution.XB1                      = VD.XB1
    settings.vortex_distribution.XB2                      = VD.XB2
    settings.vortex_distribution.YA1                      = VD.YA1
    settings.vortex_distribution.YA2                      = VD.YA2
    settings.vortex_distribution.YB1                      = VD.YB1
    settings.vortex_distribution.YB2                      = VD.YB2
    settings.vortex_distribution.ZA1                      = VD.ZA1
    settings.vortex_distribution.ZA2                      = VD.ZA2
    settings.vortex_distribution.ZB1                      = VD.ZB1
    settings.vortex_distribution.ZB2                      = VD.ZB2 
    settings.vortex_distribution.X                        = VD.X
    settings.vortex_distribution.Y                        = VD.Y
    settings.vortex_distribution.Z                        = VD.Z
    settings.vortex_distribution.XC                       = VD.XC
    settings.vortex_distribution.YC                       = VD.YC
    settings.vortex_distribution.ZC                       = VD.ZC
    settings.vortex_distribution.Y_SW                     = VD.Y_SW
     
    # unpack conditions--------------------------------------------------------------
    pwm      = settings.propeller_wake_model
    K_SPC    = settings.leading_edge_suction_multiplier 
    aoa      = conditions.aerodynamics.angles.alpha 
    mach     = conditions.freestream.mach_number 
    len_mach = len(mach)
    
    #For angular values, VORLAX uses degrees by default to radians via DTR (degrees to rads). 
    #RCAIDE uses radians and its Units system. All algular variables will be in radians or var*Units.degrees
    PSI       = conditions.aerodynamics.angles.beta    
    PITCHQ    = conditions.static_stability.pitch_rate              
    ROLLQ     = conditions.static_stability.roll_rate             
    YAWQ      = conditions.static_stability.yaw_rate 
    VINF      = conditions.freestream.velocity    
       
    #freestream 0 velocity safeguard
    if not conditions.freestream.velocity.all():
        if settings.use_surrogate:
            velocity                       = conditions.freestream.velocity
            velocity[velocity==0]          = np.ones(len(velocity[velocity==0])) * 1e-6
            conditions.freestream.velocity = velocity
        else:
            raise AssertionError("VLM requires that conditions.freestream.velocity be specified and non-zero")    

    
    # Unpack vortex distribution 
    CHORD        = VD.chord_lengths
    chord_breaks = VD.chordwise_breaks
    span_breaks  = VD.spanwise_breaks
    RNMAX        = VD.panels_per_strip    
    LE_ind       = VD.leading_edge_indices
    ZETA         = VD.tangent_incidence_angle
    RK           = VD.chordwise_panel_number
    
    exposed_leading_edge_flag = VD.exposed_leading_edge_flag
    
    YAH = VD.YAH*1.  
    YBH = VD.YBH*1. 
    XA1 = VD.XA1*1.
    XB1 = VD.XB1*1. 
    
    # Compute X and Z BAR ouside of generate_vortex_distribution to avoid requiring x_m and z_m as inputs 
    VD.XBAR = np.ones(( len_mach,sum(LE_ind[0]))) * x_m 
    VD.ZBAR = np.ones(( len_mach,sum(LE_ind[0]))) * z_m  
    
    # ---------------------------------------------------------------------------------------
    # STEP 10: Generate A and RHS matrices from VD and geometry
    # ------------------ --------------------------------------------------------------------    
    # Compute flow tangency conditions
    phi   = np.arctan((VD.ZBC - VD.ZAC)/(VD.YBC - VD.YAC)) # dihedral angle 
    delta = np.arctan((VD.ZC - VD.ZCH)/((VD.XC - VD.XCH))) # mean camber surface angle 

    # Build the RHS vector    
    rhs     = compute_RHS_matrix(VD,delta,phi,conditions,settings,geometry,pwm) 
    RHS     = rhs.RHS*1 # this matches numpy=1.26 in terms of dimension
    ONSET   = rhs.ONSET*1

    # Build induced velocity matrix, C_mn  
    C_mn, s, RFLAG, EW = compute_wing_induced_velocity(VD,mach,compute_EW=True)
    
    # Turn off sonic vortices when Mach>1
    RHS = RHS*RFLAG
    
    # To ensure compatibility for np.linalg.solve across numpy1.0 and numpy2.0
    RHS = np.atleast_3d(RHS)

    # Build Aerodynamic Influence Coefficient Matrix
    use_VORLAX_induced_velocity = settings.use_VORLAX_matrix_calculation
    if not use_VORLAX_induced_velocity:
        A =   np.multiply(C_mn[:,:,:,0],np.atleast_3d(np.sin(delta)*np.cos(phi))) \
            + np.multiply(C_mn[:,:,:,1],np.atleast_3d(np.cos(delta)*np.sin(phi))) \
            - np.multiply(C_mn[:,:,:,2],np.atleast_3d(np.cos(phi)*np.cos(delta)))   # validated from book eqn 7.42 
    else:
        A = EW

    # Compute vortex strength
    GAMMA  = np.linalg.solve(A,RHS)

    # To ensure compatibility for np.linalg.solve across numpy1.0 and numpy2.0
    RHS    = RHS.squeeze(axis=2)
    GAMMA  = GAMMA.squeeze(axis=2)

    # ---------------------------------------------------------------------------------------
    # STEP 11: Compute Pressure Coefficient
    # ------------------ --------------------------------------------------------------------   
    #VORLAX subroutine = PRESS
                  
    # spanwise strip exposure flag, always 0 for RCAIDE's infinitely thin airfoils. Needs to change if thick airfoils added
    RJTS = 0                         
    
    # COMPUTE FREE-STREAM AND ONSET FLOW PARAMETERS. Used throughout the remainder of VLM
    B2     = np.tile((mach**2 - 1),VD.n_cp[0])
    SINALF = np.sin(aoa)
    COSALF = np.cos(aoa)
    TANALF = np.tan(aoa)
    SINPSI = np.sin(PSI)
    COPSI  = np.cos(PSI)
    COSIN  = COSALF *SINPSI *2.0
    COSINP = COSALF *SINPSI
    COSCOS = COSALF *COPSI
    PITCH  = PITCHQ /VINF
    ROLL   = ROLLQ /VINF
    YAW    = YAWQ /VINF    
    
    # reshape CHORD 
    dim_1 = len(np.sum(LE_ind, axis=1))
    dim_2 = np.sum(LE_ind, axis=1)[0]
    
    # COMPUTE EFFECT OF SIDESLIP on DCP intermediate variables. needs change if cosine chorwise spacing added
    FORAXL = COSCOS
    FORLAT = COSIN 
    TAN_LEi= (VD.XB1[:,LE_ind[0]]-VD.XA1[:,LE_ind[0]])/  np.sqrt((VD.ZB1[:,LE_ind[0]]-VD.ZA1[:,LE_ind[0]])**2 +  (VD.YB1[:,LE_ind[0]]-VD.YA1[:,LE_ind[0]])**2)  
    TAN_TE = (VD.XB_TE - VD.XA_TE)/ np.sqrt((VD.ZB_TE-VD.ZA_TE)**2 + (VD.YB_TE-VD.YA_TE)**2) 
    TAN_LE = np.repeat( TAN_LEi, RNMAX[LE_ind].reshape(dim_1,dim_2)[0] , axis=1)
    
    TAN_LE = TAN_LE
    TNL    = TAN_LE * 1 # VORLAX's SIGN variable not needed, as these are taken directly from geometry
    TNT    = TAN_TE * 1
    XIA    = np.broadcast_to((RK-1)/RNMAX, np.shape(B2))
    XIB    = np.broadcast_to((RK  )/RNMAX, np.shape(B2))
    TANA   = TNL *(1. - XIA) + TNT *XIA
    TANB   = TNL *(1. - XIB) + TNT *XIB
    
    # cumsum GANT loop if KTOP > 0 (don't actually need KTOP with vectorized arrays and np.roll)
    GFX    = VD.chord_lengths
    GANT   = strip_cumsum(GFX*GAMMA, chord_breaks[0], RNMAX[LE_ind].reshape(dim_1,dim_2)[0]  )
    GANT   = np.roll(GANT,1)
    GANT[LE_ind] = 0 
    
    GLAT   = GANT *(TANA - TANB) - GFX *GAMMA *TANB
    cos_DL = (YBH-YAH)[LE_ind].reshape(dim_1,dim_2)/VD.D
    COS_DL = np.repeat( cos_DL, RNMAX[LE_ind].reshape(dim_1,dim_2)[0] , axis=1)
    DCPSID = FORLAT * COS_DL *GLAT /(XIB - XIA)
    FACTOR = FORAXL + ONSET
    
    # COMPUTE LOAD COEFFICIENT
    GNET = GAMMA*FACTOR
    GNET = GNET *RNMAX /CHORD
    DCP  = 2*GNET + DCPSID
    CP   = DCP

    # ---------------------------------------------------------------------------------------
    # STEP 12: Compute aerodynamic coefficients 
    # ------------------ --------------------------------------------------------------------  
    # Flip coordinates on the other side of the wing
    boolean = YBH<0. 
    XA1[boolean], XB1[boolean] = XB1[boolean], XA1[boolean]
    YAH[boolean], YBH[boolean] = YBH[boolean], YAH[boolean]

    # Leading edge sweep. VORLAX does it panel by panel. This will be spanwise.
    TLE   = TAN_LE[LE_ind].reshape(dim_1,dim_2)
    B2_LE = B2[LE_ind].reshape(dim_1,dim_2)
    T2    = TLE*TLE
    STB   = np.zeros_like(B2_LE)
    STB[B2_LE<T2] = np.sqrt(T2[B2_LE<T2]-B2_LE[B2_LE<T2])
    
    # DL IS THE DIHEDRAL ANGLE (WITH RESPECT TO THE X-Y PLANE) OF
    # THE IR STREAMWISE STRIP OF HORSESHOE VORTICES. 
    COD = np.cos(phi[LE_ind]).reshape(dim_1,dim_2)  # Just the LE values 
    SID = np.sin(phi[LE_ind]).reshape(dim_1,dim_2)  # Just the LE values

    # Now on to each strip
    PION = 2.0 /RNMAX
    ADC  = 0.5*PION

    # XLE = LOCATION OF FIRST VORTEX MIDPOINT IN FRACTION OF CHORD.
    XLE = 0.125 *PION
    
    GAF = 0.5 + 0.5 *RJTS**2

    # CORMED IS LENGTH OF STRIP CENTERLINE BETWEEN LOAD POINT
    # AND TRAILING EDGE THIS PARAMETER IS USED IN THE COMPUTATION
    # OF THE STRIP ROLLING COUPLE CONTRIBUTION DUE TO SIDESLIP.
    X      = VD.XCH                       #x-coord of load point (horseshoe centroid)
    XTE    = (VD.XA_TE + VD.XB_TE)/2   #Trailing edge x-coord behind the control point  
    CORMED = XTE - X   

    # SINF REFERENCES THE LOAD CONTRIBUTION OF IRT-VORTEX TO THE
    # STRIP NOMINAL AREA, I.E., AREA OF STRIP ASSUMING CONSTANT
    # (CHORDWISE) HORSESHOE SPAN.    
    SINF = ADC * DCP # The horshoe span lengths have been removed since VST/VSS == 1 always

    # Split into chordwise strengths and sum into strips    
    # SICPLE = COUPLE (ABOUT STRIP CENTERLINE) DUE TO SIDESLIP.
    CNC    = np.add.reduceat(SINF       ,chord_breaks[0],axis=1)
    SICPLE = np.add.reduceat(SINF*CORMED,chord_breaks[0],axis=1)

    # COMPUTE SLOPE (TX) WITH RESPECT TO X-AXIS AT LOAD POINTS BY INTER
    # POLATING BETWEEN CONTROL POINTS AND TAKING INTO ACCOUNT THE LOCAL
    # INCIDENCE.    
    XX   = (RK - .75) *PION /2.0
    TX    = VD.SLOPE - ZETA
    CAXL  = -SINF*TX/(1.0+TX**2) # These are the axial forces on each panel
    BMLE  = (XLE-XX)*SINF        # These are moment on each panel
    
    # Sum onto the panel
    CAXL = np.add.reduceat(CAXL,chord_breaks[0],axis=1)
    BMLE = np.add.reduceat(BMLE,chord_breaks[0],axis=1)
    
    SICPLE *= (-1) * COSIN * COD * GAF
    DCP_LE = DCP[LE_ind].reshape(dim_1,dim_2)
    
    # COMPUTE LEADING EDGE THRUST COEFF. (CSUC) BY CALCULATING
    # THE TOTAL INDUCED FLOW AT THE LEADING EDGE. THIS COMPUTATION
    # ONLY PERFORMED FOR COSINE CHORDWISE SPACING (LAX = 0).    
    # ** TO DO ** Add cosine spacing (earlier in VLM) to properly capture the magnitude of these earlier.
    # Right now, this computation still happens with linear spacing, though its effects are underestimated.
    CLE = compute_rotation_effects(VD, settings, EW, GAMMA, X, CHORD, XLE, VD.XBAR, rhs, COSINP, SINALF,COSCOS, PITCH, ROLL, YAW, STB, RNMAX)    
    
    # Leading edge suction multiplier. See documentation. This is a negative integer if used
    # Default to 1 unless specified otherwise
    SPC  = K_SPC*np.ones_like(DCP_LE)
    
    # If the vehicle is subsonic and there is vortex lift enabled then SPC changes to -1
    VL   = np.repeat(VD.vortex_lift,VD.n_sw[0], axis=1)
    m_b  = np.atleast_2d(mach[:,0]<1.)
    SPC_cond      = VL*m_b.T
    SPC[SPC_cond] = -1.
    SPC           = SPC * exposed_leading_edge_flag
    
    CLE  = CLE + 0.5* DCP_LE *np.sqrt(XLE[LE_ind].reshape(dim_1,dim_2))
    CSUC = 0.5*np.pi*np.abs(SPC)*(CLE**2)*STB 

    # TFX AND TFZ ARE THE COMPONENTS OF LEADING EDGE FORCE VECTOR ALONG
    # ALONG THE X AND Z BODY AXES.   
    
    SLE  = VD.SLOPE[LE_ind].reshape(dim_1,dim_2)
    ZETA = ZETA[LE_ind].reshape(dim_1,dim_2)
    XCOS = np.cos(SLE-ZETA) 
    XSIN = np.sin(SLE-ZETA) 
    TFX  =  1.*XCOS
    TFZ  = -1.*XSIN

    # If a negative number is used for SPC a different correction is used. See VORLAX documentation for Lan reference
    TFX[SPC<0] = XSIN[SPC<0]*np.sign(DCP_LE)[SPC<0]
    TFZ[SPC<0] = np.abs(XCOS)[SPC<0]*np.sign(DCP_LE)[SPC<0]

    CAXL = CAXL - TFX*CSUC
    
    # Add a dimension into the suction to be chordwise
    CNC   = CNC + CSUC*np.sqrt(1+T2)*TFZ
    
    # FCOS AND FSIN ARE THE COSINE AND SINE OF THE ANGLE BETWEEN
    # THE CHORDLINE OF THE IR-STRIP AND THE X-AXIS    
    FCOS = np.cos(ZETA)
    FSIN = np.sin(ZETA)
    
    # BFX, BFY, AND BFZ ARE THE COMPONENTS ALONG THE BODY AXES
    # OF THE STRIP FORCE CONTRIBUTION.
    BFX = -  CNC *FSIN + CAXL *FCOS
    BFY = - (CNC *FCOS + CAXL *FSIN) *SID
    BFZ =   (CNC *FCOS + CAXL *FSIN) *COD

    # CONVERT CNC FROM CN INTO CNC (COEFF. *CHORD).
    CHORD_strip = CHORD[LE_ind].reshape(dim_1,dim_2)   
    CNC         = CNC  * CHORD_strip
    BMLE        = BMLE * CHORD_strip

    # BMX, BMY, AND BMZ ARE THE COMPONENTS ALONG THE BODY AXES
    # OF THE STRIP MOMENT (ABOUT MOM. REF. POINT) CONTRIBUTION.
    X      = VD.XCH[LE_ind].reshape(dim_1,dim_2)  # These are all LE values
    Y      = VD.YCH[LE_ind].reshape(dim_1,dim_2)  # These are all LE values
    Z      = VD.ZCH[LE_ind].reshape(dim_1,dim_2)  # These are all LE values
    BMX    = BFZ * Y - BFY * (Z - VD.ZBAR)
    BMX    = BMX + SICPLE
    BMY    = BMLE * COD + BFX * (Z - VD.ZBAR) - BFZ * (X - VD.XBAR)
    BMZ    = BMLE * SID - BFX * Y + BFY * (X - VD.XBAR)
    CDC    = BFZ * SINALF +  (BFX *COPSI + BFY *SINPSI) * COSALF
    CDC    = CDC * CHORD_strip 

    ES     = 2*s[:,0,:][LE_ind].reshape(dim_1,dim_2)
    STRIP  = ES *CHORD_strip
    LIFT   = (BFZ *COSALF - (BFX *COPSI + BFY *SINPSI) *SINALF)*STRIP    
    MOMENT = STRIP * (BMY *COPSI - BMX *SINPSI)  
    FY     = (BFY *COPSI - BFX *SINPSI) *STRIP
    RM     = STRIP *(BMX *COSALF *COPSI + BMY *COSALF *SINPSI + BMZ *SINALF)
    YM     = STRIP *(BMZ *COSALF - (BMX *COPSI + BMY *SINPSI) *SINALF)

    # Lift coefficient
    Clift_y   = LIFT/CHORD_strip/ES  
    CL_wing   = np.add.reduceat(LIFT,span_breaks[0],axis=1)/VD.wing_areas  
    CLift     = np.atleast_2d(np.sum(LIFT,axis=1)/S_ref).T          

    # Drag coefficient
    results   = compute_trefftz_plane_induced_drag(conditions, VD,Clift_y, X, Y, Z, CHORD_strip,S_ref,b_ref)       
    
    # force coefficeints 
    CX_for   = (TANALF * CLift -  results.CDrag_induced)/(COSALF - SINALF*TANALF)
    CZ_for   = (results.CDrag_induced+ CX_for*COSALF)/SINALF  
    CY_for   = np.atleast_2d(np.sum(FY,axis=1)/S_ref).T  

    # moment coefficients 
    CM_mom   = np.atleast_2d(np.sum(MOMENT,axis=1)/S_ref).T/c_ref  
    CL_mom   = np.atleast_2d(np.sum(RM,axis=1)/S_ref).T    /b_ref*(-1)                             
    CN_mom   = np.atleast_2d(np.sum(YM,axis=1)/S_ref).T    /b_ref*(-1)                            
   
    # ---------------------------------------------------------------------------------------
    # STEP 13: Pack outputs
    # ------------------ --------------------------------------------------------------------     
    results.CLift             = CLift  
    results.CX                = CX_for 
    results.CY                = CY_for  
    results.CZ                = -CZ_for 
    results.CL                = CL_mom 
    results.CM                = CM_mom  
    results.CN                = CN_mom  
    results.spanwise_stations = Y 
    results.CLift_wing        = CL_wing   
    results.sectional_CLift   = Clift_y     
    results.CP                = np.array(CP    , dtype=settings.floating_point_precision )
    results.gamma             = np.array(GAMMA , dtype=settings.floating_point_precision ) 
    results.V_distribution    = rhs.V_distribution
    results.V_x               = rhs.Vx_ind_total
    results.V_z               = rhs.Vz_ind_total 
 
    i = 0 
    dim_wing_lifts      = results.CLift_wing * VD.wing_areas
    dim_wing_drags      = results.CDrag_induced_wing * VD.wing_areas
    Clift_wings         = Data()
    Cdrag_wings         = Data()
    # Assign the lift and drag and non-dimensionalize
    for wing in geometry.wings.values():
        ref = wing.areas.reference
        if wing.xz_plane_symmetric:
            Clift_wings[wing.tag]      = np.atleast_2d(np.sum(dim_wing_lifts[:,i:(i+2)],axis=1)).T/ref
            Cdrag_wings[wing.tag]      = np.atleast_2d(np.sum(dim_wing_drags[:,i:(i+2)],axis=1)).T/ref
            i+=1
        else:
            Clift_wings[wing.tag]      = np.atleast_2d(dim_wing_lifts[:,i]).T/ref
            Cdrag_wings[wing.tag]      = np.atleast_2d(dim_wing_drags[:,i]).T/ref
        i+=1 
    results.CLift_wings         = Clift_wings
    results.CDrag_induced_wings = Cdrag_wings
    
    return results

# ----------------------------------------------------------------------
#  CLE rotation effects helper function
# ----------------------------------------------------------------------
def compute_rotation_effects(VD, settings, EW_large, GAMMA, X, CHORD, XLE, XBAR, 
                             rhs, COSINP, SINALF,COSCOS, PITCH, ROLL, YAW, STB, RNMAX):
    """ This computes the effects of the freestream and aircraft rotation rate on 
    CLE, the induced flow at the leading edge
    
    Assumptions:
    Several of the values needed in this calculation have been computed earlier and stored in VD
    
    Normally, VORLAX skips the calculation implemented in this function for linear 
    chordwise spacing (the if statement below). However, since the trends are correct, 
    albeit underestimated, this calculation is being forced here.    
    """
    LE_ind   = VD.leading_edge_indices
    RNMAX    = VD.panels_per_strip
    dim_1    = len(np.sum(LE_ind, axis=1))
    dim_2    = np.sum(LE_ind, axis=1)[0]
    dim_3    = len(LE_ind[0])
    
    # Computate rotational effects (pitch, roll, yaw rates) on LE suction
    # pick leading edge strip values for EW and reshape GAMMA -> gamma accordingly
    EW    = EW_large[LE_ind, :].reshape(dim_1, dim_2, dim_3) 
    gamma = np.array(np.split(np.repeat(GAMMA, dim_2, axis=0), dim_1))
    CLE   = (EW*gamma).sum(axis=2)
    
    # Up till EFFINC, some of the following values were computed in compute_RHS_matrix().
    #     EFFINC and ALOC are calculated the exact same way, except for the XGIRO term.
    # LOCATE VORTEX LATTICE CONTROL POINT WITH RESPECT TO THE
    # ROTATION CENTER (XBAR, 0, ZBAR). THE RELATIVE COORDINATES
    # ARE XGIRO, YGIRO, AND ZGIRO. 
    XGIRO = X - CHORD*XLE - np.repeat( XBAR, RNMAX[LE_ind].reshape(dim_1,dim_2)[0] , axis=1) 
    YGIRO = rhs.YGIRO
    ZGIRO = rhs.ZGIRO
    
    # VX, VY, VZ ARE THE FLOW ONSET VELOCITY COMPONENTS AT THE LEADING
    # EDGE (STRIP MIDPOINT). VX, VY, VZ AND THE ROTATION RATES ARE
    # REFERENCED TO THE FREE STREAM VELOCITY.     
    VX = (COSCOS - PITCH*ZGIRO + YAW  *YGIRO)  
    VY = (COSINP - YAW  *XGIRO + ROLL *ZGIRO)  
    VZ = (SINALF - ROLL *YGIRO + PITCH*XGIRO)

    # CCNTL, SCNTL, SID, and COD were computed in compute_RHS_matrix()
    
    # EFFINC = COMPONENT OF ONSET FLOW ALONG NORMAL TO CAMBERLINE AT
    #          LEADING EDGE.
    EFFINC = VX *rhs.SCNTL + VY *rhs.CCNTL *rhs.SID - VZ *rhs.CCNTL *rhs.COD 
    CLE = CLE - EFFINC[LE_ind].reshape(dim_1,dim_2) 
    CLE = np.where(STB > 0, CLE /RNMAX[LE_ind].reshape(dim_1,dim_2) /STB, CLE)
    
    return CLE

# ----------------------------------------------------------------------
#  Vectorized cumsum from indices
# ----------------------------------------------------------------------
def strip_cumsum(arr, chord_breaks, strip_lengths):
    """ Uses numpy to to compute a cumsum that resets along
    the leading edge of every strip.
    
    Assumptions:
    chordwise_breaks always starts at 0
    """    
    cumsum  = np.cumsum(arr, axis=1)
    offsets = cumsum[:,chord_breaks-1]
    offsets[:,0]  = 0
    offsets = np.repeat(offsets, strip_lengths, axis=1)
    return cumsum - offsets
    
    
def compute_trefftz_plane_induced_drag(conditions, VD, cl, x_dist, y_dist, z_dist, chord_dist,SREF,b_ref, v_inf=1):
    """
    Compute far-field induced drag using the Trefftz-plane method.

    The Trefftz plane is a cross-sectional plane located infinitely far downstream of
    the wing.  In this plane, the horseshoe trailing vortices appear as semi-infinite
    2-D line vortices that induce a crossflow velocity field (VY, VZ).  The induced
    drag follows from the kinetic energy of that crossflow:

        dCDi_strip = Γ_strip * (DZT * VY - DYT * VZ) / S_ref

    where DYT and DZT are the projected strip widths in the Trefftz plane, and
    VY, VZ are the induced velocities at the strip center.

    Approach
    --------
    Rather than summing with total strip circulations (as AVL does), this routine
    uses the equivalent shed-vortex representation:

      1. The strip circulation Γ is derived from the sectional lift coefficient via
         the Kutta-Joukowski theorem, with an arc-length correction for dihedral.
      2. Shed vortex strengths are the spanwise differences of Γ, placed at the
         vortex lattice spanwise stations.  Each shed vortex is a semi-infinite
         2-D point vortex in the Trefftz plane.
      3. The induced downwash at each strip centre is obtained by summing the
         contributions of all shed vortices, projected onto the local strip normal.
      4. The sectional induced drag coefficient is alpha_i * cl, and the total CDi
         is obtained by integrating chord * cdi / S_ref along the arc-length span.

    Geometry note — why body-axis Z is used in the Trefftz plane
    -------------------------------------------------------------
    The trailing vortices extend from the bound-vortex trailing edge rearward in
    the body-x direction (flat-wake assumption).  Their position in the Trefftz
    plane (x → ∞) is therefore simply their body-axis (y, z) coordinates — no
    alpha rotation is needed.  AVL's TPFORC confirms this: it calls PGMAT with
    ALFAT = 0, making the transformation an identity on Y and Z.

    Circulation arc-length correction
    ----------------------------------
    RCAIDE's Clift_y is normalised by the actual arc-length panel area
    (chord × DS, DS = sqrt(DY² + DZ²)), not the projected area (chord × DY).
    From the Kutta-Joukowski theorem applied to a dihedraled strip:
        Lift = rho * V * Γ * DY  (lift acts on projected span DY)
        Clift_y = Lift / (0.5 * rho * V² * chord * DS)
               = 2 * Γ * DY / (V * chord * DS)
        → Γ = 0.5 * V * chord * cl * (DS / DY)
    For a flat wing DS = DY, the correction factor is 1 and the formula reduces
    to the standard expression.

    Strip-normal projection
    -----------------------
    The induced downwash that contributes to drag is the velocity component
    perpendicular to the strip and in the plane of the Trefftz cross-section
    (i.e., the outward normal to the strip in the Y-Z plane).  For a flat wing
    this normal is simply [0, 1] (vertical), which is what the original formula
    assumed.  For a dihedraled strip oriented at angle δ the normal rotates to
    [-sin δ, cos δ].  A sign(DY) multiplier is applied so the normal consistently
    points "upward" (positive Z component) for both the left and right wing halves.

    Parameters
    ----------
    conditions  : flight conditions object, supplies alpha
    VD          : vortex distribution object (panel geometry, n_sw, n_cw, etc.)
    cl          : sectional lift coefficient, shape (n_cases, n_panels)
    x_dist      : x coordinates of strip load-points (unused, kept for API compat.)
    y_dist      : y coordinates of strip load-points (unused, kept for API compat.)
    z_dist      : z coordinates of strip load-points (unused, kept for API compat.)
    chord_dist  : chord at each strip, shape (n_cases, n_strips)
    SREF        : reference area
    b_ref       : reference span (unused, kept for API compat.)
    v_inf       : freestream speed (default 1, since cl is already normalised)

    Returns
    -------
    results.CDrag_induced           : total induced drag coefficient, (n_cases, 1)
    results.sectional_CDrag_induced : strip cdi distribution
    results.CDrag_induced_wing      : induced drag per surface
    results.alpha_induced           : induced angle of attack distribution
    """

    # ------------------------------------------------------------------
    # Allocate output arrays for all flight cases
    # ------------------------------------------------------------------
    alpha   = conditions.aerodynamics.angles.alpha
    n_cases = len(alpha)
    CDi_total         = np.zeros(n_cases)                        # scalar CDi per case
    CDi_wing          = np.zeros((n_cases, len(VD.n_sw[0])))    # CDi per lifting surface
    Cd_i_distribution = np.zeros_like(cl)                        # strip cdi
    alpha_i           = np.zeros_like(cl)                        # strip induced AoA

    for k in range(n_cases):

        alpha   = conditions.aerodynamics.angles.alpha[k]        # flight alpha for this case
        n_wings = len(VD.n_sw[k])                                 # number of lifting surfaces

        # cumulative split indices: spanwise control-point stations have n_sw+1 nodes per surface
        divisions_control_point = np.cumsum(VD.n_sw[k]+1)[:-1]
        # cumulative split indices for strip-level (n_sw strips per surface)
        divisions               = np.cumsum(VD.n_sw[k])[:-1]

        # sectional lift coefficient and chord, split per surface.
        # np.empty(n_wings, dtype=object) + manual assignment guarantees a 1-D object
        # array of length n_wings regardless of whether sub-arrays share the same length.
        cl_split    = np.empty(n_wings, dtype=object)
        chord_split = np.empty(n_wings, dtype=object)
        for w, (c, ch) in enumerate(zip(np.split(cl[k], divisions),
                                        np.split(chord_dist[k], divisions))):
            cl_split[w]    = c
            chord_split[w] = ch

        # ------------------------------------------------------------------
        # Trefftz-plane geometry
        # ------------------------------------------------------------------
        # Each element of VD.Y[k] / VD.Z[k] is already a per-wing node array.
        # Stride every (n_cw+1) entries to extract the leading spanwise node per strip.
        # Body-axis Z is used directly (no alpha rotation); see docstring for details.
        y_nodes_list = []
        z_nodes_list = []

        n_sw = VD.n_sw[k]
        n_cw = VD.n_cw[k]
        discretization = np.insert(np.cumsum((n_sw+1)*(n_cw+1)), 0, 0)

        for index in range(len(discretization) - 1):
            y_nodes_list.append(np.asarray(VD.Y[k][discretization[index]:discretization[index+1]][::(VD.n_cw[k][index] + 1)]))
            z_nodes_list.append(np.asarray(VD.Z[k][discretization[index]:discretization[index+1]][::(VD.n_cw[k][index] + 1)]))

        y_nodes = np.empty(len(y_nodes_list), dtype=object)
        z_nodes = np.empty(len(z_nodes_list), dtype=object)

        for i in range(len(y_nodes_list)):
            y_nodes[i] = y_nodes_list[i]
            z_nodes[i] = z_nodes_list[i]
        
        y_control_points = np.empty(n_wings, dtype=object)
        z_control_points = np.empty(n_wings, dtype=object)
        y_centerpoints   = np.empty(n_wings, dtype=object)
        z_centerpoints   = np.empty(n_wings, dtype=object)
        for w in range(n_wings):
            y_control_points[w] = y_nodes[w]                               # body-axis Y corner nodes
            z_control_points[w] = z_nodes[w]                               # body-axis Z corner nodes
            y_centerpoints[w]   = (y_nodes[w][:-1] + y_nodes[w][1:]) / 2  # mid-Y per strip
            z_centerpoints[w]   = (z_nodes[w][:-1] + z_nodes[w][1:]) / 2  # mid-Z per strip

        # ------------------------------------------------------------------
        # Strip arc-length and Kutta-Joukowski circulation with dihedral correction
        # ------------------------------------------------------------------
        # Spanwise increments between adjacent corner nodes in body axes.
        # np.diff with axis=1 does not work on jagged object arrays, so loop per surface.
        dy_strips = np.empty(n_wings, dtype=object)
        dz_strips = np.empty(n_wings, dtype=object)
        DS_strips = np.empty(n_wings, dtype=object)
        for w in range(n_wings):
            d = np.diff(y_control_points[w])             # projected spanwise width DY per strip
            d[d == 0] = 1e-6                             # guard against root-plane symmetry node
            dy_strips[w] = d
            dz_strips[w] = np.diff(z_control_points[w]) # body-axis Z increment per strip (dihedral)
            DS_strips[w] = np.sqrt(dy_strips[w]**2 + dz_strips[w]**2)  # arc-length strip width DS

        # Strip circulation from Kutta-Joukowski with arc-length correction.
        # Because RCAIDE normalises Clift_y by chord × DS (arc-length area), the
        # correct circulation is Γ = 0.5 * V * chord * cl * (DS / |DY|).
        # For a flat wing DS = |DY|, so the correction factor equals 1.
        circulation_dist = np.empty(n_wings, dtype=object)
        for w in range(n_wings):
            circulation_dist[w] = 0.5 * chord_split[w] * v_inf * cl_split[w] * (DS_strips[w] / np.abs(dy_strips[w]))

        # ------------------------------------------------------------------
        # Shed-vortex strengths at spanwise stations
        # ------------------------------------------------------------------
        # Each trailing vortex filament has strength equal to the spanwise change in
        # bound circulation (by Helmholtz's theorem).  The sign convention follows the
        # spanwise traversal direction: sign(DY) > 0 for the right half-wing and
        # sign(DY) < 0 for the left half-wing.
        #
        # For a symmetric surface the root vortex (station 0) cancels with the mirror
        # image and is therefore set to zero.  For a non-symmetric surface (e.g. a
        # vertical tail) both root and tip vortices are non-zero.
        symmetric_wing_flags = np.concatenate([
            np.repeat(np.array(VD.symmetric_wings[0], dtype=bool), 2),
            np.zeros(np.count_nonzero(~np.array(VD.symmetric_wings[0], dtype=bool)), dtype=bool)
        ])[:n_wings]

        # Each sub-array has n_sw+1 nodes (one per spanwise station); initialise per surface.
        # np.zeros_like on an object array does not produce sub-arrays of the right size,
        # so allocate explicitly with a loop.
        shed_vortices = np.empty(n_wings, dtype=object)
        for wing_number in range(n_wings):
            shed_vortices[wing_number] = np.zeros(len(y_control_points[wing_number]))
            # spanwise traversal direction (+1 right, -1 left)
            # Use [1] / [0] sub-indexing — 2D comma indexing fails on object arrays.
            span_sign = np.sign(y_control_points[wing_number][1] - y_control_points[wing_number][0])
            if symmetric_wing_flags[wing_number]:
                # interior nodes: Δ circulation between adjacent strips
                shed_vortices[wing_number][1:-1] = span_sign * np.diff(circulation_dist[wing_number])
                # root node: zero because the mirror half cancels
                shed_vortices[wing_number][0]    = 0
                # tip node: full tip circulation closes the vortex sheet
                shed_vortices[wing_number][-1]   = -span_sign * circulation_dist[wing_number][-1]
            else:
                # interior nodes: Δ circulation
                shed_vortices[wing_number][1:-1] = span_sign * np.diff(circulation_dist[wing_number])
                # root node: full root circulation (no cancelling mirror)
                shed_vortices[wing_number][0]    = -span_sign * circulation_dist[wing_number][0]
                # tip node: full tip circulation
                shed_vortices[wing_number][-1]   = -span_sign * circulation_dist[wing_number][-1]

        # ------------------------------------------------------------------
        # Induced velocity at each strip centre (Trefftz-plane summation)
        # ------------------------------------------------------------------
        # Each shed vortex at station (y_vort, z_vort) with strength Γ_shed induces a
        # 2-D velocity at field point (y_ctr, z_ctr).  The velocity direction is
        # perpendicular to the radius vector and has magnitude Γ / (4π × distance).
        # Summing over all shed vortices on all surfaces gives the total Trefftz-plane
        # crossflow at each strip centre.
        # Same reasoning as shed_vortices — initialise per-surface arrays explicitly.
        induced_velocity = np.empty(n_wings, dtype=object)
        for i in range(n_wings):
            induced_velocity[i] = np.zeros(len(y_centerpoints[i]))
        for i in range(n_wings):
            for j in range(len(y_centerpoints[i])):
                for l in range(n_wings):
                    for m in range(len(y_control_points[l])):

                        # radial distance from shed vortex to strip centre
                        distance = np.sqrt(
                            (y_centerpoints[i][j] - y_control_points[l][m])**2 +
                            (z_centerpoints[i][j] - z_control_points[l][m])**2)

                        # unit vector in the direction of the 2-D induced velocity from
                        # a positive (CCW) point vortex: perpendicular to the radius,
                        # rotated 90° CCW → [-DZ, DY] / distance
                        vortex_direction = (1.0/distance) * np.array([
                            -(z_centerpoints[i][j] - z_control_points[l][m]),
                             (y_centerpoints[i][j] - y_control_points[l][m])])

                        # Outward strip normal in the Trefftz plane: perpendicular to the
                        # strip vector (strip_dy, strip_dz) and pointing away from the wing
                        # surface (upward for a normal wing).  The 90° CCW rotation of the
                        # strip direction gives (-strip_dz, strip_dy) / strip_ds.
                        # Multiplying by sign(strip_dy) ensures the normal points consistently
                        # "upward" (positive Z component) for both the left and right halves:
                        #   right half: strip_dy > 0 → normal = (-sin δ,  cos δ)
                        #   left  half: strip_dy < 0 → sign flips → normal = (+sin δ, cos δ)
                        # For a flat wing strip_dz = 0, so the normal reduces to [0, 1],
                        # which matches the original flat-wing formula.
                        strip_dy = y_control_points[i][j+1] - y_control_points[i][j]
                        strip_dz = z_control_points[i][j+1] - z_control_points[i][j]
                        strip_ds = np.sqrt(strip_dy**2 + strip_dz**2)
                        strip_normal = np.sign(strip_dy) * np.array([-strip_dz/strip_ds,
                                                                       strip_dy/strip_ds])

                        # scalar projection of the induced velocity onto the strip normal
                        v_hat = np.dot(strip_normal, vortex_direction)

                        # velocity magnitude from a semi-infinite 2-D point vortex
                        velocity_contribution = shed_vortices[l][m] / (4.0 * np.pi * distance)

                        # accumulate normal-velocity contribution at strip centre i,j
                        induced_velocity[i][j] += velocity_contribution * v_hat

        # ------------------------------------------------------------------
        # Sectional induced angle of attack and drag coefficient
        # ------------------------------------------------------------------
        # The induced angle of attack is the downwash angle: α_i = arctan(w / V_inf).
        # The sectional induced drag coefficient is then cdi = α_i × cl (small-angle form).
        alpha_induced_dist = np.empty(n_wings, dtype=object)
        cd_induced_dist    = np.empty(n_wings, dtype=object)
        for i in range(n_wings):
            alpha_induced_dist[i] = np.arctan(induced_velocity[i] / v_inf)  # downwash angle per strip
            cd_induced_dist[i]    = alpha_induced_dist[i] * cl_split[i]     # sectional cdi = α_i × cl

        # ------------------------------------------------------------------
        # Integrate CDi along the arc-length span
        # ------------------------------------------------------------------
        # The cumulative arc-length from root to each strip centre, computed in body
        # axes.  Using arc-length (not projected span) is correct for dihedraled wings.
        # np.cumsum with axis=1 does not work on jagged object arrays; loop per surface.
        line_distance = np.empty(n_wings, dtype=object)
        for w in range(n_wings):
            line_distance[w] = np.cumsum(np.sqrt(np.diff(y_control_points[w])**2 +
                                                 np.diff(z_control_points[w])**2))

        CDi = 0
        for i in range(n_wings):
            CDi_wing_sum = 0
            # Traversal direction: if the shed vortex at the tip is negative relative
            # to the root, the strips run from root to tip → integrate directly.
            # Otherwise flip so the integrand is ordered root-to-tip.
            if np.sign(shed_vortices[i][-1] - shed_vortices[i][0]) < 0:
                CDi         += trapezoid(cd_induced_dist[i] * chord_split[i] / SREF,
                                         line_distance[i])
                CDi_wing_sum += trapezoid(cd_induced_dist[i] * chord_split[i] / SREF,
                                          line_distance[i])
            else:
                CDi         += trapezoid(np.flip(cd_induced_dist[i]) * np.flip(chord_split[i]) / SREF,
                                         np.flip(-line_distance[i]))
                CDi_wing_sum += trapezoid(np.flip(cd_induced_dist[i]) * np.flip(chord_split[i]) / SREF,
                                          np.flip(-line_distance[i]))
            CDi_wing[k][i] = CDi_wing_sum

        CDi_total[k]          = CDi
        # .ravel() on an object array of sub-arrays does not concatenate them;
        # use np.concatenate to flatten the per-surface arrays into one flat array.
        Cd_i_distribution[k]  = np.concatenate([cd_induced_dist[i]    for i in range(n_wings)])
        alpha_i[k]            = np.concatenate([alpha_induced_dist[i]  for i in range(n_wings)])

    # ------------------------------------------------------------------
    # Pack and return results
    # ------------------------------------------------------------------
    results                         = Data()
    results.CDrag_induced           = CDi_total[:,np.newaxis]
    results.sectional_CDrag_induced = Cd_i_distribution
    results.CDrag_induced_wing      = CDi_wing
    results.alpha_induced           = alpha_i

    return results