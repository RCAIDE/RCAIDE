# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/compressibility_drag_total.py
# 
# Created:  Jul 2024, RCAIDE Team 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from RCAIDE.Framework.Core                    import Data
from RCAIDE.Library.Components.Wings          import Main_Wing
from RCAIDE.Library.Methods.Utilities         import Cubic_Spline_Blender

# package imports
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Compressibility Drag Total
# ----------------------------------------------------------------------------------------------------------------------  
def wave_drag(state,settings,geometry):
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
    high_mach_cutoff = settings.supersonic.end_drag_rise_mach_number
    peak_mach        = settings.supersonic.peak_mach_number

    # supersonic smoothing 
    sup_spline = Cubic_Spline_Blender(peak_mach,high_mach_cutoff) 
    sup_h00    = lambda M:sup_spline.compute(M)

    sup_spline2 = Cubic_Spline_Blender(peak_mach,1.5) 
    sup_h002    = lambda M:sup_spline2.compute(M)     
    
    # Wave drag due to volume  
    CD_wave_volume = supersonic_volume_wave_drag(conditions, settings, geometry) *(1-sup_h00(Mach))
    
    # wave drag due to lift  
    transonic_CDw_lift           = transonic_lift_wave_drag(conditions, settings, geometry) *sup_h00(Mach)
    transonic_CDw_lift[Mach<0.7] = 0
    transonic_CDw_lift[Mach>0.95]= 0
    supersonic_CDw_lift          = supersonic_lift_wave_drag(conditions, settings, geometry) *(1-sup_h002(Mach))
    supersonic_CDw_lift[Mach<1]  = 0   
   
    # total wave drag  
    CD_wave_lift   = supersonic_CDw_lift + transonic_CDw_lift
    CD_wave        = CD_wave_lift + CD_wave_volume 

    # Save drag breakdown 
    conditions.aerodynamics.coefficients.drag.wave = Data(total  = CD_wave, 
                                                          lift   = CD_wave_lift,
                                                          volume = CD_wave_volume,)  
        
    return

# ---------------------------------------------------------------------------------------------------------------------- 
#  transonic_lift_wave_drag
# ----------------------------------------------------------------------------------------------------------------------
def transonic_lift_wave_drag(conditions, settings, geometry): 
    """
    Theory comes from: "The Prediciton of the Drag of Aerofoils and Wings at High Subsonic Speeds" by R.C. Lock, 1986, Aeronautical journal 
    
    CL vs the CP value before the shock wave comes from the same source as well as NASA TP 2969, NASA Supercritical Airfoils by Charles D. Harris
    """
    Mach              = conditions.freestream.mach_number  
    S_ref             = geometry.reference_area 
    CD_wave_transonic = np.zeros_like(Mach)
    
    if settings.use_surrogate or (settings.vortex_distribution == None): 
        Cl                   = conditions.aerodynamics.coefficients.lift.total
        CD_wave_transonic    = np.array([1.1480189359872706, 0.0, 1.1480189359872706, 5.775673779192156, 12.836939011494024, 20.414496506330114, 34.447683899469276, 49.59172983603965, 65.49874978998449, 160, 240]) *10**-4
        CLs                  = np.array([-0.417184699337467, 0.0, 0.417184699337467, 0.45862155954167055, 0.5013290492186359, 0.5384919739235497, 0.5871622608441653, 0.6285553062389633, 0.6587038782744932, 0.8, 1.0])
        CD_wave_transonic    = np.interp(Cl, CLs, CD_wave_transonic) *( 12.5 * Mach - 8.75 ) 
    else: 
        chords   = settings.vortex_distribution.chord_lengths
        delta    = settings.vortex_distribution.leading_edge_sweeps 
        dy       = settings.vortex_distribution.chord_widths
        
        CD_wave_total = np.zeros_like(Mach)
        CL_y          = conditions.aerodynamics.coefficients.lift.inviscid.spanwise
             
        c_kappa       = 0.23 # normalized curvature of the airfoil. This can eventually be calcualted using airfoil shape data. 
    
        # ------------------------------------------------------------------
        # Cp Data (as function of CL) from "The Prediciton of the Drag of Aerofoils and Wings at High Subsonic Speeds" by R.C. Lock, 1986, Aeronautical journal and NASA TP 2969, NASA Supercritical Airfoils by Charles D. Harris
        # ------------------------------------------------------------------
        # Data was for M = 0.78, but appears to be valid for similar Mach numbers. Composite data ebtween RAE 5225 and NASA supercritical airfoil. ADD FULL REFERENCE HERE
                   
        Cp_shock =  0.9825 *(CL_y**2)  - 2.5132 *(CL_y) + 0.0279 # Cp vlaue right before the shock wave 
        # ------------------------------------------------------------------
        # Wave Drag Calculation
        # ------------------------------------------------------------------

        # Calculate the local mach number right before the shock wave
        M1_0_star = np.sqrt((5+Mach**2*np.cos(delta[0])**2)/(1+0.7*Mach**2*Cp_shock)**(2/7) - 5)
        
        # Calculate the wave drag coefficient
        constant = (np.cos(delta[0])**4)/c_kappa * 0.243*((1+0.2*Mach*np.cos(delta[0]))/(Mach*np.cos(delta[0])))**3 # note, delta is assumed to remain constant across all conditions. 
        CD_wave_segment = constant*(M1_0_star - 1)**4*(2-M1_0_star)/(M1_0_star*(1+0.2*M1_0_star**2)) * 0.5
        
        # Set the wave drag coefficient to 0 if there is no shock wave
        CD_wave_segment[Cp_shock > -0.6] = 0.0 # If the Cp > -0.6 then there is likely no shock wave

        S_segment = chords[0]*dy[0]
        CD_wave_total = np.sum(CD_wave_segment*S_segment/S_ref, axis=1, keepdims=True)

        CD_wave_transonic = CD_wave_total
        
    return CD_wave_transonic 
 
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
    Mach         = conditions.freestream.mach_number
    cd_lift_wave = np.zeros_like(Mach)
    
    for wing in  geometry.wings:
        if isinstance(wing, Main_Wing):   
            # Lift coefficient  
            CL = conditions.aerodynamics.coefficients.lift.total 
            l  = wing.chords.root  
        
            # JAXA method
            s    = wing.spans.projected / 2
            AR   = wing.aspect_ratio
            p    = 2/AR*s/l
            beta = np.sqrt(Mach**2-1) 
            x    =  beta*s/l
        
            ret = np.zeros_like(x) 
            ret[x > 0.178] = 0.4935 - 0.2382*x[x > 0.178] + 1.6306*x[x > 0.178]**2 - 0.86*x[x > 0.178]**3 + 0.2232*x[x > 0.178]**4 - 0.0365*x[x > 0.178]**5 - 0.5            
            
            Kw           = (1+1/p)*ret/(2*beta**2*(s/l)**2) 
            cd_lift_wave = CL**2 * (beta**2/np.pi*p*(s/l)*Kw) 

    return cd_lift_wave

def supersonic_volume_wave_drag(conditions, settings, vehicle):
    """Computes the volume drag
    
    Assumptions:
    Basic fit
    
    Source:
    Sieron, Thomas R., et al. Procedures and design data for the formulation of aircraft 
    configurations. WRIGHT LAB WRIGHT-PATTERSON AFB OH, 1993. Page B-3
    
    Args:
    vehicle.
      total_length                        [m]
      maximum_cross_sectional_area        [m^2]
      reference_area                      [m^2]
      
    Returns:
    vehicle_wave_drag                     [Unitless] 
    """
   
    S_ref = vehicle.reference_area
    L     = vehicle.length
    Amax  = vehicle.maximum_cross_sectional_area
     
    # compute volume drag referenced to frontal area
    Rmax = 0
    for fuselage in vehicle.fuselages:
        Rmax =  np.maximum(Rmax, fuselage.width)
    volume      =  (3 / 16) * (np.pi ** 2) * (Rmax ** 2)  *  L 
    CD_wave_vol_frontal = 24 *volume /(L **3)
    
    CD_wave_vol =  CD_wave_vol_frontal * ( Amax / S_ref) *  np.ones_like(conditions.freestream.mach_number) 
    return CD_wave_vol 