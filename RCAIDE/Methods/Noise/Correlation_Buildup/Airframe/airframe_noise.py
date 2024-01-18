## @ingroup Methods-Noise-Correlation_Buildup-Airframe 
# RCAIDE/Methods/Noise/Correlation_Buildup/Airframe/airframe_noise.py
# 
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE Imports
from RCAIDE.Core                      import Data , Units

from .clean_wing_noise             import clean_wing_noise
from .landing_gear_noise           import landing_gear_noise
from .leading_edge_slat_noise      import leading_edge_slat_noise
from .trailing_edge_flap_noise     import trailing_edge_flap_noise 
from RCAIDE.Methods.Noise.Metrics  import PNL_noise_metric
from RCAIDE.Methods.Noise.Metrics  import EPNL_noise_metric
from RCAIDE.Methods.Noise.Metrics  import SENEL_noise_metric_single_point
from RCAIDE.Methods.Noise.Metrics  import A_weighting_metric 
from RCAIDE.Methods.Noise.Common   import noise_tone_correction
from RCAIDE.Methods.Noise.Common   import atmospheric_attenuation
from RCAIDE.Methods.Noise.Common   import SPL_arithmetic
from RCAIDE.Visualization.Noise    import print_airframe_output

# python imports 
import numpy as np

# ----------------------------------------------------------------------
#  Airframe Noise 
# ----------------------------------------------------------------------

## @ingroup Methods-Noise-Correlation_Buildup-Airframe
def airframe_noise(segment,analyses,config,settings,ioprint = 0, filename=0):  
    """ This computes the noise from different sources of the airframe for a given vehicle for a constant altitude flight. 

    Assumptions:
        Correlation based 
 
    Source:
        Fink, Martin R. Airframe noise prediction method. No. UTRC/R77-912607-11. UNITED 
        TECHNOLOGIES RESEARCH CENTER EAST HARTFORD CT, 1977.  
               
    Inputs:
        vehicle	 - RCAIDE type vehicle

        includes these fields:
            S                          - Wing Area
            bw                         - Wing Span
            Sht                        - Horizontal tail area
            bht                        - Horizontal tail span
            Svt                        - Vertical tail area
            bvt                        - Vertical tail span
            deltaf                     - Flap deflection
            Sf                         - Flap area
            cf                         - Flap chord
            slots                      - Number of slots (Flap type)
            Dp                         - Main landing gear tyre diameter
            Hp                         - Main lading gear strut length
            Dn                         - Nose landing gear tyre diameter
            Hn                         - Nose landing gear strut length
            wheels                     - Number of wheels 
            
        noise segment - flight path data, containing:
            distance_vector             - distance from the source location to observer
            angle                       - polar angle from the source to the observer
            phi                         - azimuthal angle from the source to the observer


    Outputs: One Third Octave Band SPL [dB]
        SPL_wing                        - Sound Pressure Level of the clean wing
        SPLht                           - Sound Pressure Level of the horizontal tail
        SPLvt                           - Sound Pressure Level of the vertical tail
        SPL_flap                        - Sound Pressure Level of the flaps trailing edge
        SPL_slat                        - Sound Pressure Level of the slat leading edge
        SPL_main_landing_gear           - Sound Pressure Level og the main landing gear
        SPL_nose_landing_gear           - Sound Pressure Level of the nose landing gear

    Properties Used:
        N/A      
        
    """  
    # Unpack 
    wing     = config.wings
    flap     = wing.main_wing.control_surfaces.flap 
    Sw       = wing.main_wing.areas.reference  / (Units.ft)**2              # wing area, sq.ft
    bw       = wing.main_wing.spans.projected / Units.ft                    # wing span, ft
    Sht      = wing.horizontal_stabilizer.areas.reference / (Units.ft)**2   # horizontal tail area, sq.ft
    bht      = wing.horizontal_stabilizer.spans.projected / Units.ft        # horizontal tail span, ft
    Svt      = wing.vertical_stabilizer.areas.reference / (Units.ft)**2     # vertical tail area, sq.ft
    bvt      = wing.vertical_stabilizer.spans.projected  / Units.ft         # vertical tail span, ft
    deltaf   = flap.deflection                                              # flap delection, rad
    Sf       = flap.area  / (Units.ft)**2                                   # flap area, sq.ft        
    cf       = flap.chord_dimensional  / Units.ft                           # flap chord, ft
    Dp       = config.landing_gear.main_tire_diameter  / Units.ft           # MLG tyre diameter, ft
    Hp       = config.landing_gear.nose_tire_diameter  / Units.ft           # MLG strut length, ft
    Dn       = config.landing_gear.main_strut_length   / Units.ft           # NLG tyre diameter, ft
    Hn       = config.landing_gear.nose_strut_length   / Units.ft           # NLG strut length, ft
    gear     = config.landing_gear.gear_condition                           # Gear up or gear down
    
    nose_wheels  = config.landing_gear.nose_wheels                          # Number of wheels   
    main_wheels  = config.landing_gear.main_wheels                          # Number of wheels   
    main_units   = config.landing_gear.main_units                           # Number of main units   
    velocity     = np.float(segment.conditions.freestream.velocity[0,0])    # aircraft velocity 
    altitude     = segment.conditions.freestream.altitude[:,0]              # aircraft altitude
    noise_time   = segment.conditions.frames.inertial.time[:,0]             # time discretization 

    # determining flap slot number
    if wing.main_wing.control_surfaces.flap.configuration_type   == 'single_slotted':
        slots = 1
    elif wing.main_wing.control_surfaces.flap.configuration_type == 'double_slotted':
        slots = 2
    elif wing.main_wing.control_surfaces.flap.configuration_type == 'triple_slotted':
        slots = 3  

    # Geometric information from the source to observer position 
    RML                 = segment.conditions.noise.relative_microphone_locations  
    distance_vector     = np.linalg.norm(RML,axis = 2)
    thetas              = np.arccos(RML[:,:,0]/distance_vector) 
    phis                = np.arccos(RML[:,:,1]/distance_vector)   
    viscosity           = segment.conditions.freestream.dynamic_viscosity[:,0]*Units.ft*Units.ft # units converstion - m2 to ft2 
    M                   = segment.conditions.freestream.mach_number
    
    # Generate array with the One Third Octave Band Center Frequencies
    frequency = settings.center_frequencies[5:]  
    num_f     = len(frequency) 
    n_cpts    = len(thetas)  
    n_mic     = len(RML[0,:,0]) 

    SPL_wing_history              = np.zeros((n_cpts,n_mic,num_f))
    SPLht_history                 = np.zeros((n_cpts,n_mic,num_f))
    SPLvt_history                 = np.zeros((n_cpts,n_mic,num_f))
    SPL_flap_history              = np.zeros((n_cpts,n_mic,num_f))
    SPL_slat_history              = np.zeros((n_cpts,n_mic,num_f))
    SPL_main_landing_gear_history = np.zeros((n_cpts,n_mic,num_f))
    SPL_nose_landing_gear_history = np.zeros((n_cpts,n_mic,num_f))
    SPL_total_history             = np.zeros((n_cpts,n_mic,num_f)) 
    SPLt_dBA_history              = np.zeros((n_cpts,n_mic,num_f))  
    SPLt_dBA_max                  = np.zeros((n_cpts,n_mic))    
    
    # START LOOP FOR EACH POSITION OF AIRCRAFT   
    for i in range(n_cpts):
        for j in range(n_mic): 
            
            # Emission angle
            theta = thetas[i,j]
            phi   = phis[i,j]
            
            # Distance from airplane to observer, evaluated at retarded time
            distance = distance_vector[i,j]    
           
            # Atmospheric attenuation
            delta_atmo=atmospheric_attenuation(np.array([distance]),frequency)[:,0]
    
            # Call each noise source model
            SPL_wing = clean_wing_noise(Sw,bw,0,1,velocity,viscosity[i],M[i],phi,theta,distance,frequency) - delta_atmo    #Wing Noise
            SPLht    = clean_wing_noise(Sht,bht,0,1,velocity,viscosity[i],M[i],phi,theta,distance,frequency)  -delta_atmo    #Horizontal Tail Noise
            SPLvt    = clean_wing_noise(Svt,bvt,0,0,velocity,viscosity[i],M[i],phi,theta,distance,frequency)  -delta_atmo    #Vertical Tail Noise
     
            SPL_slat = leading_edge_slat_noise(SPL_wing,Sw,bw,velocity,viscosity[i],M[i],phi,theta,distance,frequency) -delta_atmo        #Slat leading edge
     
            if (deltaf==0):
                SPL_flap = np.zeros(num_f)
            else:
                SPL_flap = trailing_edge_flap_noise(Sf,cf,deltaf,slots,velocity,M[i],phi,theta,distance,frequency) - delta_atmo #Trailing Edge Flaps Noise
     
            if gear=='up': #0
                SPL_main_landing_gear = np.zeros(num_f)
                SPL_nose_landing_gear = np.zeros(num_f)
            else:
                SPL_main_landing_gear = landing_gear_noise(Dp,Hp,main_wheels,M[i],velocity,phi,theta,distance,frequency)  - delta_atmo     #Main Landing Gear Noise
                SPL_nose_landing_gear = landing_gear_noise(Dn,Hn,nose_wheels,M[i],velocity,phi,theta,distance,frequency)  - delta_atmo     #Nose Landing Gear Noise
            if main_units>1: # Incoherent summation of each main landing gear unit
                SPL_main_landing_gear = SPL_main_landing_gear+3*(main_units-1) 
     
            # Total Airframe Noise
            SPL_total = 10.*np.log10(10.0**(0.1*SPL_wing)+10.0**(0.1*SPLht)+10**(0.1*SPL_flap)+ \
                 10.0**(0.1*SPL_slat)+10.0**(0.1*SPL_main_landing_gear)+10.0**(0.1*SPL_nose_landing_gear))
                
            SPL_total_history[i,j,:]             = SPL_total 
            SPL_wing_history[i,j,:]              = SPL_wing 
            SPLvt_history[i,j,:]                 = SPLvt 
            SPLht_history[i,j,:]                 = SPLht 
            SPL_flap_history[i,j,:]              = SPL_flap 
            SPL_slat_history[i,j,:]              = SPL_slat 
            SPL_nose_landing_gear_history[i,j,:] = SPL_nose_landing_gear 
            SPL_main_landing_gear_history[i,j,:] = SPL_main_landing_gear  
            
            # Calculation of dBA based on the sound pressure time history 
            SPLt_dBA_history[i,j,:] = A_weighting_metric(SPL_total,frequency)
            SPLt_dBA_max[i,j]       = np.max(A_weighting_metric(SPL_total,frequency))    
              
    # Calculation of the Perceived Noise Level EPNL based on the sound time history 
    PNL_total             = PNL_noise_metric(SPL_total_history)
    PNL_wing              = PNL_noise_metric(SPL_wing_history)
    PNL_ht                = PNL_noise_metric(SPLht_history)
    PNL_vt                = PNL_noise_metric(SPLvt_history)
    PNL_nose_landing_gear = PNL_noise_metric(SPL_nose_landing_gear_history)
    PNL_main_landing_gear = PNL_noise_metric(SPL_main_landing_gear_history)
    PNL_slat              = PNL_noise_metric(SPL_slat_history)
    PNL_flap              = PNL_noise_metric(SPL_flap_history)
     
    # Calculation of the tones corrections on the SPL for each component and total
    tone_correction_total             = noise_tone_correction(SPL_total_history) 
    tone_correction_wing              = noise_tone_correction(SPL_wing_history)
    tone_correction_ht                = noise_tone_correction(SPLht_history)
    tone_correction_vt                = noise_tone_correction(SPLvt_history)
    tone_correction_flap              = noise_tone_correction(SPL_flap_history)
    tone_correction_slat              = noise_tone_correction(SPL_slat_history)
    tone_correction_nose_landing_gear = noise_tone_correction(SPL_nose_landing_gear_history)
    tone_correction_main_landing_gear = noise_tone_correction(SPL_main_landing_gear_history)
    
    # Calculation of the PLNT for each component and total
    PNLT_total             = PNL_total+tone_correction_total
    PNLT_wing              = PNL_wing+tone_correction_wing
    PNLT_ht                = PNL_ht+tone_correction_ht
    PNLT_vt                = PNL_vt+tone_correction_vt
    PNLT_nose_landing_gear = PNL_nose_landing_gear+tone_correction_nose_landing_gear
    PNLT_main_landing_gear = PNL_main_landing_gear+tone_correction_main_landing_gear
    PNLT_slat              = PNL_slat+tone_correction_slat
    PNLT_flap              = PNL_flap+tone_correction_flap
    
    #Calculation of the EPNL for each component and total
    EPNL_total             = EPNL_noise_metric(PNLT_total)
    EPNL_wing              = EPNL_noise_metric(PNLT_wing)
    EPNL_ht                = EPNL_noise_metric(PNLT_ht)
    EPNL_vt                = EPNL_noise_metric(PNLT_vt)    
    EPNL_nose_landing_gear = EPNL_noise_metric(PNLT_nose_landing_gear)
    EPNL_main_landing_gear = EPNL_noise_metric(PNLT_main_landing_gear)
    EPNL_slat              = EPNL_noise_metric(PNLT_slat)
    EPNL_flap              = EPNL_noise_metric(PNLT_flap)
    
    # Calculation of the SENEL total
    SENEL_total = SENEL_noise_metric_single_point(SPLt_dBA_max) 
    
    SAE_Airframe_Noise_Outputs = Data(
        tag                       = config.tag,
        filename                  = filename,
        velocity                  = velocity,
        n_cpts                    = n_cpts,
        time                      = noise_time,
        altitude                  = altitude,
        M                         = M,
        angle                     = thetas,
        distance_vector           = distance_vector,
        PNLT_wing                 = PNLT_wing,
        phi                       = phi,
        PNLT_ht                   = PNLT_ht,
        PNLT_vt                   = PNLT_vt,
        PNLT_flap                 = PNLT_flap,
        PNLT_slat                 = PNLT_slat,
        PNLT_nose_landing_gear    = PNLT_nose_landing_gear,
        PNLT_main_landing_gear    = PNLT_main_landing_gear,
        PNLT_total                = PNLT_total,
        SPLt_dBA_max              = SPLt_dBA_max,
        frequency                 = frequency,
        EPNL_wing                 = EPNL_wing,
        EPNL_ht                   = EPNL_ht,
        EPNL_vt                   = EPNL_vt,
        EPNL_flap                 = EPNL_flap,
        EPNL_slat                 = EPNL_slat,
        EPNL_nose_landing_gear    = EPNL_nose_landing_gear,
        EPNL_main_landing_gear    = EPNL_main_landing_gear,
        EPNL_total                = EPNL_total,
        SENEL_total               = SENEL_total,
        SPL_total_history         = SPL_total_history,
        SPLt_dBA_history          = SPLt_dBA_history)  
    
    if ioprint:
        print_airframe_output(SAE_Airframe_Noise_Outputs) 
    
    # Pack Airframe Noise 
    airframe_noise                   = Data()
    airframe_noise.EPNL_total        = EPNL_total
    airframe_noise.SPL               = SPL_arithmetic(SPL_total_history, sum_axis= 2)
    airframe_noise.SPL_1_3_spectrum  = SPL_total_history
    airframe_noise.SPL_dBA           = SPL_arithmetic(np.atleast_2d(SPLt_dBA_history), sum_axis= 2)
    airframe_noise.SENEL_total       = SENEL_total 
    airframe_noise.noise_time        = noise_time 
    return airframe_noise
