# RCAIDE/Library/Methods/Geometry/Two_Dimensional/Planform/wing_segmented_planform.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports 
import RNUMPY as rp

# ----------------------------------------------------------------------------------------------------------------------
#  compute_section_coefficients
# ----------------------------------------------------------------------------------------------------------------------    
def wing_segmented_planform(wing, overwrite_reference = False):
    """Computes the high-level properties of a segmented wing. These include: 
    wing.
      spans.total                (float): [m]
      chords.tip                 (float): [m]
      chords.mean_aerodynamics   (float): [m]
      wing.chords.mean_geometric (float): [m]
      areas.reference            (float): [m^2]
      taper                      (float): [-]
      sweeps.quarter_chord       (float): [radians]
      aspect_ratio               (float): [-]
      thickness_to_chord         (float): [-]
      dihedral                   (float): [radians] 
      aerodynamic_center          (list):  x, y, and z location [m]     
    
    Assumptions:
        Multisegmented wing. There is no unexposed wetted area, ie wing area that 
        intersects inside a fuselage. Aerodynamic center is at 25% mean aerodynamic chord.
    
    Source:
        None
    
    Args:
         wing                       (dict):
         overwrite_reference     (boolean): Determines if reference area, wetted area, and aspect
                                            ratio are overwritten based on the segment values.
    wing.
      chords.root              [m]
      spans.projected          [m]
      symmetric                <boolean> Determines if wing is symmetric
    
    Returns:
        None 
    """
    
    # Unpack
    
    # Pull all the segment data into array format
    span_locs = []
    twists    = []
    sweeps    = []
    dihedrals = []
    chords    = []
    t_cs      = []
    for key in wing.Segments.keys():
        seg = wing.Segments[key]
        span_locs.append(seg.percent_span_location)
        twists.append(seg.twist)
        chords.append(seg.root_chord_percent)
        sweeps.append(seg.sweeps.quarter_chord)
        t_cs.append(seg.thickness_to_chord)
        dihedrals.append(seg.dihedral_outboard)
        
    # Convert to arrays
    chords    = rp.array(chords)
    span_locs = rp.array(span_locs)
    sweeps    = rp.array(sweeps)
    t_cs      = rp.array(t_cs)
    
    # Basic calcs:
    span         = wing.spans.projected 
    sym          = wing.symmetric
    semispan     = span/(1+sym)
    lengths_ndim = span_locs[1:]-span_locs[:-1]
    lengths_dim  = lengths_ndim*semispan
    chords_dim   = wing.chords.root*chords
    tapers       = chords[1:]/chords[:-1]
    
    # Compute the areas of each segment
    segment_areas = (lengths_dim*chords_dim[:-1]-(chords_dim[:-1]-chords_dim[1:])*(lengths_dim/2))
    
    # Compute the weighted area, this should not include any unexposed area 
    A_wets = 2*(1+0.2*t_cs[:-1])*segment_areas
    wet_area = rp.sum(A_wets)
    
    # Compute the wing area
    wing_area = rp.sum(segment_areas)*(1+sym)
    
    # Compute the Aspect Ratio
    AR = (span**2)/wing_area
    
    # Compute the total span
    lens = lengths_dim/rp.cos(dihedrals[:-1])
    total_len = rp.sum(rp.array(lens))*(1+sym)
    
    # Compute the mean geometric chord
    mgc = wing_area/span
    
    # Compute the mean aerodynamic chord
    A        = chords_dim[:-1]
    B        = (A-chords_dim[1:])/(-lengths_ndim)
    C        = span_locs[:-1]
    integral = ((A+B*(span_locs[1:]-C))**3-(A+B*(span_locs[:-1]-C))**3)/(3*B)
    
    # For the cases when the wing doesn't taper in a spot
    integral[rp.isnan(integral)] = (A[rp.isnan(integral)]**2)*((lengths_ndim)[rp.isnan(integral)])
    MAC = (semispan*(1+sym)/(wing_area))*rp.sum(integral)
    
    # Compute the taper ratio
    lamda = chords[-1]/chords[0] 
    
    # Compute an average t/c weighted by area
    t_c = rp.sum(segment_areas*t_cs[:-1])/(wing_area/2)
    
    # Compute the segment leading edge sweeps
    r_offsets = chords_dim[:-1]/4
    t_offsets = chords_dim[1:]/4
    le_sweeps = rp.arctan((r_offsets+rp.tan(sweeps[:-1])*(lengths_dim)-t_offsets)/(lengths_dim))    
    
    # Compute the effective sweeps
    c_4_sweep      = rp.arctan(rp.sum(lengths_ndim*rp.tan(sweeps[:-1])))
    le_sweep_total = rp.arctan(rp.sum(lengths_ndim*rp.tan(le_sweeps)))

    # Compute the aerodynamic center, but first the centroid
    dxs = rp.cumsum(rp.concatenate([rp.array([0]),rp.tan(le_sweeps[:-1])*lengths_dim[:-1]]))
    dys = rp.cumsum(rp.concatenate([rp.array([0]),lengths_dim[:-1]]))
    dzs = rp.cumsum(rp.concatenate([rp.array([0]),rp.tan(dihedrals[:-2])*lengths_dim[:-1]])) 
    Cxys = []
    for i in range(len(lengths_dim)):
        Cxys.append(segment_centroid(le_sweeps[i],lengths_dim[i],dxs[i],dys[i],dzs[i], tapers[i], 
                                     segment_areas[i], dihedrals[i], chords_dim[i], chords_dim[i+1]))
 
    aerodynamic_center = (rp.dot(rp.transpose(Cxys),segment_areas)/(wing_area/(1+sym))) 
    single_side_aerodynamic_center    = (rp.array(aerodynamic_center)*1.)
    single_side_aerodynamic_center[0] = single_side_aerodynamic_center[0] - MAC*.25    
    if sym== True:
        aerodynamic_center[1] = 0 
    aerodynamic_center[0]     = single_side_aerodynamic_center[0]
    
    # Compute wing length
    wing_length = rp.tan(le_sweep_total)*semispan + chords[-1]*wing.chords.root
    
    # Pack results 
    if overwrite_reference:
        wing.areas.reference         = wing_area
        wing.areas.wetted            = wet_area
        wing.aspect_ratio            = AR

    wing.spans.total                    = total_len
    wing.chords.mean_geometric          = mgc
    wing.chords.mean_aerodynamic        = MAC
    wing.chords.tip                     = chords_dim[-1]
    wing.taper                          = lamda
    wing.sweeps.quarter_chord           = c_4_sweep
    wing.sweeps.leading_edge            = le_sweep_total
    wing.thickness_to_chord             = t_c
    wing.aerodynamic_center             = aerodynamic_center
    wing.single_side_aerodynamic_center = single_side_aerodynamic_center
    wing.total_length                   =  wing_length

    # Update remainder segment properties
    wing =  segment_properties(wing)
    
    return wing
 
def segment_properties(wing,update_wet_areas=False,update_ref_areas=False):
    """Computes detailed segment properties. These are currently used for parasite drag calculations.

    Assumptions:
        Segments are trapezoids

    Source:
        Stanford AA241 A/B Course Notes : http://aerodesign.stanford.edu/aircraftdesigNoneircraftdesign.html  

    Args:
        wing.
          percent_span_root_offset           (float): [m]
          symmetric                          (float): [-]
          spans.projected                    (float): [m]
          thickness_to_chord                 (float): [-]
          areas.wetted                       (float): [m^2]
          chords.root                        (float): [m]
          Segments.[].percent_span_location  (float): [-]
          Segments.[].root_chord_percent     (float): [-]

    Returns:
        None 

    """  
        
    # Unpack wing properties 
    percent_span_root_offset  = wing.percent_span_root_offset
    symm                      = wing.symmetric
    semispan                  = wing.spans.projected*0.5 * (2 - symm)
    t_c_w                     = wing.thickness_to_chord
    segments                  = wing.Segments
    segment_names             = list(segments.keys())
    num_segments              = len(segment_names)       
    total_wetted_area         = 0.
    total_reference_area      = 0.
    root_chord                = wing.chords.root      
    
    for i_segs in range(num_segments):
        if i_segs == num_segments-1:
            continue 
        else:  
            span_seg  = semispan*(segments[segment_names[i_segs+1]].percent_span_location - \
                                  segments[segment_names[i_segs]].percent_span_location ) 
            segment   = segments[segment_names[i_segs]]         
            
            if i_segs == 0:
                chord_root    = root_chord*segments[segment_names[i_segs]].root_chord_percent
                chord_tip     = root_chord*segments[segment_names[i_segs+1]].root_chord_percent   
                wing_root     = chord_root + percent_span_root_offset*((chord_tip - chord_root)/span_seg)
                taper         = chord_tip/wing_root  
                mac_seg       = wing_root  * 2/3 * (( 1 + taper  + taper**2 )/( 1 + taper))  
                Sref_seg      = span_seg*(chord_root+chord_tip)*0.5 
                S_exposed_seg = (span_seg-percent_span_root_offset)*(wing_root+chord_tip)*0.5                    
            
            else: 
                chord_root    = root_chord*segments[segment_names[i_segs]].root_chord_percent
                chord_tip     = root_chord*segments[segment_names[i_segs+1]].root_chord_percent
                taper         = chord_tip/chord_root   
                mac_seg       = chord_root * 2/3 * (( 1 + taper  + taper**2 )/( 1 + taper))
                Sref_seg      = span_seg*(chord_root+chord_tip)*0.5
                S_exposed_seg = Sref_seg

            if wing.symmetric:
                Sref_seg = Sref_seg*2
                S_exposed_seg = S_exposed_seg*2
            
            # compute wetted area of segment
            if t_c_w < 0.05:
                Swet_seg = 2.003* S_exposed_seg
            else:
                Swet_seg = (1.977 + 0.52*t_c_w) * S_exposed_seg
                
            segment.taper                   = taper 
            segment.chords.mean_aerodynamic = mac_seg 
            segment.areas.reference         = Sref_seg
            segment.areas.exposed           = S_exposed_seg
            segment.areas.wetted            = Swet_seg 
            total_wetted_area               += Swet_seg
            total_reference_area            += Sref_seg 
    
    if wing.areas.reference==0. or update_ref_areas:
        wing.areas.reference = total_reference_area
        
    if wing.areas.wetted==0. or update_wet_areas:
        wing.areas.wetted    = total_wetted_area
        
    return wing 

# Segment centroid
def segment_centroid(le_sweep,seg_span,dx,dy,dz,taper,A,dihedral,root_chord,tip_chord):
    """Computes the centroid of a trapezoidal segment
    
    Assumptions:
        None 
    
    Source:
        None
    
    Args:
        le_sweep    (float):  [rad]
        seg_span    (float):  [m]
        dx          (float):  [m]
        dy          (float):  [m]
        taper       (float):  [dimensionless]
        A           (float):  [m**2]
        dihedral    (float):  [radians]
        root_chord  (float):  [m]
        tip_chord   (float):  [m]

    Returns:
        centroid    (numpy.ndarray): [m,m,m]


    """    
    
    a        = tip_chord
    b        = root_chord
    c        = rp.tan(le_sweep)*seg_span
    cx       = (2*a*c + a**2 + c*b + a*b + b**2) / (3*(a+b))
    cy       = seg_span / 3. * (( 1. + 2. * taper ) / (1. + taper))
    cz       = cy * rp.tan(dihedral)     
    centroid =  rp.array([cx+dx,cy+dy,cz+dz])
    
    return centroid