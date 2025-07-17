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
    # wave drag due to lift at supersonic speeds 
    # ---------------------------------------------------------------------
    cd_wave_supersonic_lift  = supersonic_lift_wave_drag(conditions, settings, geometry)*(1-sup_h00(Mach))   
    
    # ---------------------------------------------------------------------    
    # transonic wave drag 
    # --------------------------------------------------------------------- 
    wave_drag = transonic_wave_drag(conditions, settings, geometry)  

    # ---------------------------------------------------------------------     
    # total compressibility drag
    # ---------------------------------------------------------------------
    cd_c = cd_compressibility_volume + cd_wave_supersonic_lift + wave_drag

    # Save drag breakdown 
    conditions.aerodynamics.coefficients.drag.compressible = Data(total   = cd_c, 
                                                                  wave    = wave_drag)  
        
    return

# ---------------------------------------------------------------------------------------------------------------------- 
#  transonic_wave_drag
# ----------------------------------------------------------------------------------------------------------------------
def transonic_wave_drag(conditions, settings, geometry): 
    Cl         = conditions.aerodynamics.coefficients.lift.total  
    Mach       = conditions.freestream.mach_number   
    CD_wave    = np.array([-0.417184699337467, 0.0, 0.417184699337467, 0.45862155954167055, 0.5013290492186359, 0.5384919739235497, 0.5871622608441653, 0.6285553062389633, 0.6587038782744932, 0.8, 1.0])
    CLs        = np.array([1.1480189359872706, 0.0, 1.1480189359872706, 5.775673779192156, 12.836939011494024, 20.414496506330114, 34.447683899469276, 49.59172983603965, 65.49874978998449, 160, 240]) *10**-4
    wave_drag  = np.interp(Cl, CD_wave, CLs)
    
    wave_drag[Mach<0.7] = 0.0 
    
    return wave_drag


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
