# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/compressibility_drag_total.py
# 
# Created:  Jul 2024, RCAIDE Team 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from RCAIDE.Framework.Core                    import Data
from RCAIDE.Library.Components.Wings          import Main_Wing
from RCAIDE.Library.Methods.Utilities         import Cubic_Spline_Blender
from .drag_divergence                         import drag_divergence 
from .supersonic_wave_drag_volume_raymer      import supersonic_wave_drag_volume_raymer
from .supersonic_wave_drag_volume_sears_haack import supersonic_wave_drag_volume_sears_haack

# package imports
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Compressibility Drag Total
# ----------------------------------------------------------------------------------------------------------------------  
def compressibility_drag(state,settings,geometry):
    """Computes compressibility drag for full aircraft including volume drag

    Assumptions:
    None

    Source:
    None

    Args:   
    settings.
      begin_drag_rise_mach_number                                    [Unitless]
      end_drag_rise_mach_number                                      [Unitless]
      peak_mach_number                                               [Unitless]
      transonic_drag_multiplier                                      [Unitless]
      volume_wave_drag_scaling                                       [Unitless]
    state.conditions.freestream.mach_number                          [Unitless]
    geometry.maximum_cross_sectional_area                            [m^2] (used in subfunctions)
    geometry.total_length                                            [m]   (used in subfunctions)
    geometry.reference_area                                          [m^2]
    geometry.wings                             

    Returns:
    total_compressibility_drag                                       [Unitless]

    Properties Used:
    None
    """     

    # Unpack
    conditions       = state.conditions
    Mach             = conditions.freestream.mach_number 
    Cl               = conditions.aerodynamics.coefficients.lift.total   
    low_mach_cutoff  = settings.supersonic.begin_drag_rise_mach_number
    high_mach_cutoff = settings.supersonic.end_drag_rise_mach_number
    peak_mach        = settings.supersonic.peak_mach_number
    peak_factor      = settings.supersonic.transonic_drag_multiplier
    scaling_factor   = settings.supersonic.volume_wave_drag_scaling

    # ---------------------------------------------------------------------     
    # Compressibility volume drag
    # ---------------------------------------------------------------------
    if settings.supersonic.wave_drag_type == 'Raymer':
        wave_drag_volume = supersonic_wave_drag_volume_raymer
    elif settings.supersonic.wave_drag_type == 'Sears-Haack':
        wave_drag_volume = supersonic_wave_drag_volume_sears_haack
    else:
        raise NotImplementedError    
    
    if settings.supersonic.cross_sectional_area_calculation_type != 'Fixed':
        raise NotImplementedError
  
    low_cutoff_volume_total  = drag_divergence(low_mach_cutoff*np.ones_like(Mach), geometry,Cl) 
    high_cutoff_volume_total = wave_drag_volume(geometry,low_mach_cutoff*np.ones_like(Mach),scaling_factor) 
    peak_volume_total        = high_cutoff_volume_total*peak_factor
     
    # subsonic side smoothing function
    a1 = (low_cutoff_volume_total-peak_volume_total)/(low_mach_cutoff-peak_mach)/(low_mach_cutoff-peak_mach)
    
    # supersonic side smoothing function
    a2 = (high_cutoff_volume_total-peak_volume_total)/(high_mach_cutoff-peak_mach)/(high_mach_cutoff-peak_mach) 
    
    # Shorten cubic Hermite spline
    sub_spline = Cubic_Spline_Blender(low_mach_cutoff, peak_mach-(peak_mach-low_mach_cutoff)*3/4)
    sup_spline = Cubic_Spline_Blender(peak_mach,high_mach_cutoff)
    sub_h00    = lambda M:sub_spline.compute(M)
    sup_h00    = lambda M:sup_spline.compute(M) 
    
    low_inds = Mach[:,0]<peak_mach
    hi_inds  = Mach[:,0]>=peak_mach

    cd_compressibility_volume_base                  = np.zeros_like(Mach) 
    cd_compressibility_volume_base[low_inds]        = drag_divergence(Mach[low_inds], geometry,Cl[low_inds]) 
    cd_compressibility_volume_base[Mach>=peak_mach] = wave_drag_volume(geometry, Mach[Mach>=peak_mach], scaling_factor) 
    
    cd_compressibility_volume = np.zeros_like(Mach)
    cd_compressibility_volume[low_inds] = cd_compressibility_volume_base[low_inds]*(sub_h00(Mach[low_inds])) + transonic_compressibility_drag(Mach[low_inds],a1[low_inds], peak_mach, peak_volume_total[low_inds])*(1-sub_h00(Mach[low_inds]))
    cd_compressibility_volume[hi_inds]  = transonic_compressibility_drag(Mach[hi_inds],a2[hi_inds], peak_mach, peak_volume_total[hi_inds])*(sup_h00(Mach[hi_inds])) + cd_compressibility_volume_base[hi_inds]*(1-sup_h00(Mach[hi_inds]))
 
    # ---------------------------------------------------------------------    
    # transonic wave drag 
    # --------------------------------------------------------------------- 
    wave_drag = transonic_wave_drag(conditions, settings, geometry)

    # ---------------------------------------------------------------------        
    # wave drag due to lift at supersonic speeds 
    # ---------------------------------------------------------------------
    cd_wave_supersonic_lift  = supersonic_lift_wave_drag(conditions, settings, geometry)*(1-sup_h00(Mach))   

    # ---------------------------------------------------------------------     
    # total compressibility drag
    # ---------------------------------------------------------------------
    cd_c = cd_compressibility_volume + cd_wave_supersonic_lift + wave_drag

    # Save drag breakdown 
    conditions.aerodynamics.coefficients.drag.compressible = Data(total   = cd_c, 
                                                                  wave    = wave_drag+cd_wave_supersonic_lift)  
        
    return

# ---------------------------------------------------------------------------------------------------------------------- 
#  transonic_wave_drag
# ----------------------------------------------------------------------------------------------------------------------
def transonic_wave_drag(conditions, settings, geometry): 
    
    Mach        = conditions.freestream.mach_number 
    alpha       = conditions.aerodynamics.angles.alpha
    Re          = conditions.freestream.reynolds_number 
    n           = settings.number_of_spanwise_vortices
    
    CD_wave_transonic = np.zeros_like(Mach)
    for wing in geometry.wings:
        if wing.vertical == False:
            if len(wing.segments) > 0: 
                for seg_i in range(len(wing.segments)-1):
                    segs = list(wing.segments.keys())
                    if wing.segments[segs[seg_i]].airfoil_2D_polars: 
                        inboard_segment        = wing.segments[segs[seg_i]]
                        outboard_segment       = wing.segments[segs[seg_i+1]]
                        inboard_airfoil_polar  = inboard_segment.airfoil.polars
                        outboard_airfoil_polar = outboard_segment.airfoil.polars 
                        aspect_ratio = wing.segments[segs[seg_i]]
                        root_chord   = wing.chords.root * wing.segments[segs[seg_i]].percent_root_chord
                        tip_chord    = wing.chords.root * wing.segments[segs[seg_i+1]].percent_root_chord
                        root_twist   = wing.segments[seg_i].twist
                        tip_twist    = wing.segments[segs[seg_i+1]].twist
                        sweep_le     = wing.segments[segs[seg_i]].sweeps.leading_edge 
                        CD_wave_seg  = compute_wing_wave_drag(Re,alpha,inboard_airfoil_polar, outboard_airfoil_polar,aspect_ratio, root_chord,tip_chord,root_twist,tip_twist,sweep_le,n) 
                        CD_wave_seg[Mach<0.7] = 0.0
                        CD_wave_transonic += CD_wave_seg* (wing.segments[segs[seg_i]].areas.reference/ geometry.reference_area)                        
                    else:
                        Cl                   = conditions.aerodynamics.coefficients.lift.inviscid.wings[wing.tag] 
                        CD_wave_seg          = np.array([-0.417184699337467, 0.0, 0.417184699337467, 0.45862155954167055, 0.5013290492186359, 0.5384919739235497, 0.5871622608441653, 0.6285553062389633, 0.6587038782744932, 0.8, 1.0])
                        CLs                  = np.array([1.1480189359872706, 0.0, 1.1480189359872706, 5.775673779192156, 12.836939011494024, 20.414496506330114, 34.447683899469276, 49.59172983603965, 65.49874978998449, 160, 240]) *10**-4
                        CD_wave_seg          = np.interp(Cl, CD_wave_seg, CLs)    
                        CD_wave_seg[Mach<0.7] = 0.0
                        CD_wave_transonic    += CD_wave_seg * (wing.segments[segs[seg_i]].areas.reference/ geometry.reference_area) 
            else:
                if wing.airfoil_2D_polars:
                    inboard_airfoil_polar  = wing.airfoil.polars
                    outboard_airfoil_polar = wing.airfoil.polars 
                    aspect_ratio           = wing.aspect_ratio
                    root_chord             = wing.chords.root 
                    tip_chord              = wing.chords.root * wing.taper
                    root_twist             = wing.twists.root
                    tip_twist              = wing.twists.tip
                    sweep_le               = wing.sweeps.leading_edge 
                    CD_wave_wing           = compute_wing_wave_drag(Re,alpha,inboard_airfoil_polar, outboard_airfoil_polar,aspect_ratio, root_chord,tip_chord,root_twist,tip_twist,sweep_le,n)     
                    CD_wave_wing[Mach<0.7] = 0.0 
                    CD_wave_transonic     += CD_wave_wing * (wing.areas.reference / geometry.reference_area)                                            
                else:
                    Cl                   = conditions.aerodynamics.coefficients.lift.inviscid.wings[wing.tag] 
                    CD_wave_wing         = np.array([-0.417184699337467, 0.0, 0.417184699337467, 0.45862155954167055, 0.5013290492186359, 0.5384919739235497, 0.5871622608441653, 0.6285553062389633, 0.6587038782744932, 0.8, 1.0])
                    CLs                  = np.array([1.1480189359872706, 0.0, 1.1480189359872706, 5.775673779192156, 12.836939011494024, 20.414496506330114, 34.447683899469276, 49.59172983603965, 65.49874978998449, 160, 240]) *10**-4
                    CD_wave_wing         = np.interp(Cl, CD_wave_wing, CLs)  
                    CD_wave_wing[Mach<0.7] = 0.0 
                    CD_wave_transonic    += CD_wave_wing * (wing.segments[segs[seg_i]].areas.reference/ geometry.reference_area) 
             
    return CD_wave_transonic


# ---------------------------------------------------------------------------------------------------------------------- 
#  transonic wave drag
# ----------------------------------------------------------------------------------------------------------------------
def compute_wing_wave_drag(non_dim_Re,alpha,inboard_airfoil_polar, outboard_airfoil_polar,aspect_ratio, root_chord,tip_chord,root_twist,tip_twist,sweep_le,n):
    
    n_cases =  len(alpha)
    
    # get dimensional reynolds number                     
    segment_chords         = np.linspace(root_chord,tip_chord,n)
    chord_Res              = segment_chords * non_dim_Re 

    linear_smoothing       = np.tile(np.linspace(0,1,n)[None,:],(n_cases , 1)) 
    twist_distribution     = np.tile(np.linspace(root_twist,tip_twist,n)[None,:] ,(n_cases,1)) 
    AoA_eff                = alpha + twist_distribution 


    # AIDAN TO UPDATE 
    ## function for converting 2D polars into 3D polars considering the effect of sweep and boundary layer growth 
    #eta                    =  np.linspace(0,1,n) 
    #kappa_tip              = aspect_ratio * (eta)
    #kappa_root             = aspect_ratio * (eta - 1)
    #kappa                  = 1 +  kappa_root  +  kappa_tip  
    #sweep_eff              = sweep_le * kappa
    #F_sweep                = np.cos(sweep_eff)
 
    #inboard_pts            = np.hstack((chord_Res.reshape(n_cases * n , 1),inboard_AoA_2_5_D.reshape(n_cases * n , 1))) 
    #outboard_pts           = np.hstack((chord_Res.reshape(n_cases * n, 1),outboard_AoA_2_5_D.reshape(n_cases * n , 1))) 
    #inboard_Cdrag_eff_i    = np.atleast_2d(inboard_Cdrag_func(inboard_pts)).reshape(n_cases, n  )
    #outboard_Cdrag_eff_i   = np.atleast_2d(outboard_Cdrag_func(outboard_pts)).reshape(n_cases, n ) 
    #CD_wave_wing            = inboard_Cdrag_eff_i* (1- linear_smoothing)  + outboard_Cdrag_eff_i*linear_smoothing
    
    #CD_wave_y              = inboard_Cdrag_eff_i* (1- eta)  + outboard_Cdrag_eff_i*eta 
    #spacing                = np.linspace(0,1,n+1)  
    #delta_y                = np.diff(spacing * span)
    #D_wave_wing            = np.atleast_2d(np.sum(CD_form_y  * segment_chords * delta_y, axis=1)).T 
    #CD_wave_wing           = D_wave_wing /(S_ref)
    
        
    CD_wave_wing = alpha * 0
    return CD_wave_wing


# ---------------------------------------------------------------------------------------------------------------------- 
#  transonic_compressibility_drag
# ---------------------------------------------------------------------------------------------------------------------- 
def transonic_compressibility_drag(Mach,a_vertex, peak_mach, peak_volume_total):
    """  parabolic approximation of drag rise in the transonic region
    
    Assumptions:
    Basic fit

    Source:
    None 

    Args:
    Mach
    a_vertex
    peak_mach
    peak_volume_total

    Returns:
    transonic_drag
    """ 
    transonic_drag = a_vertex*(Mach-peak_mach)*(Mach-peak_mach)+peak_volume_total
    transonic_drag = transonic_drag.reshape(np.shape(Mach))
    return transonic_drag

# ---------------------------------------------------------------------------------------------------------------------- 
# supersonic_lift_wave_drag
# ---------------------------------------------------------------------------------------------------------------------- 
def supersonic_lift_wave_drag(conditions,configuration,geometry):
    """Determine lift wave drag for supersonic speeds

    Assumptions:
    Basic fit

    Source:
    Yoshida, Kenji. "Supersonic drag reduction technology in the scaled supersonic 
    experimental airplane project by JAXA."

    Args:
    conditions.freestream.mach_number [-]
    configuration                     (passed to another function)
    wing.areas.reference              [m^2]
    Sref_main                         [m^2] Main reference area

    Returns:
    cd_wave_supersonic_lift                            [-] Wave drag CD due to lift 
    """

    # Initalize cd arrays 
    Mach        = conditions.freestream.mach_number  
    cd_wave_supersonic_lift = np.zeros_like(Mach)
    
    for wing in  geometry.wings:
        if isinstance(wing, Main_Wing):   
            # Lift coefficient  
            CL = conditions.aerodynamics.coefficients.lift.total 
            l  = np.maximum(wing.total_length,wing.chords.root)     
        
            # JAXA method
            s    = wing.spans.projected / 2
            AR   = wing.aspect_ratio
            p    = 2/AR*s/l
            beta = np.sqrt(Mach[Mach >= 1.01]**2-1)
            
            x    =  beta*s/l
        
            ret = np.zeros_like(x)
            
            ret[x > 0.178] = 0.4935 - 0.2382*x[x > 0.178] + 1.6306*x[x > 0.178]**2 - \
                0.86*x[x > 0.178]**3 + 0.2232*x[x > 0.178]**4 - 0.0365*x[x > 0.178]**5 - 0.5            
            
            Kw           = (1+1/p)*ret/(2*beta**2*(s/l)**2) 
            CDwl         = CL[Mach >= 1.01]**2 * (beta**2/np.pi*p*(s/l)*Kw)
            cd_lift_wave = np.zeros_like(Mach)
            cd_lift_wave[Mach >= 1.01] = CDwl
             
            # Pack supersonic results into correct elements
            cd_wave_supersonic_lift[Mach >= 1.01] = cd_lift_wave[0:len(Mach[Mach >= 1.01]),0] 

    return cd_wave_supersonic_lift
