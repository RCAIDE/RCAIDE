# RCAIDE/Library/Methods/Mass_Properties/Moment_of_Inertia/compute_wing_moment_of_inertia.py 
# 
# Created:  September 2023, A. Molloy  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import RCAIDE
from RCAIDE.Library.Methods.Mass_Properties.Moment_of_Inertia.compute_wing_moment_of_inertia import compute_wing_section_moment_of_intertia

# package imports 
import numpy as np  
# ----------------------------------------------------------------------------------------------------------------------
#  Compute Wing Moment of Inertia
# ----------------------------------------------------------------------------------------------------------------------  
def compute_wing_integral_tank_moment_of_inertia(fuel_tank,wing, center_of_gravity = [[0, 0, 0]]):
    ''' computes the moment of inertia tensor for a wing about a given center of gravity. 

    Assumptions:
    - Wing is solid
    - Wing has a constant density

    Source:
    [1] Moulton, B. C., and Hunsaker, D. F., “Simplified Mass and Inertial Estimates for Aircraft with Components
    of Constant Density,” AIAA SCITECH 2023 Forum, January 2023, AIAA-2023-2432 DOI: 10.2514/
    6.2023-2432
    
    [2] Fuel tank references: These were used to estimate the length percentages. 
    - https://assets.publishing.service.gov.uk/media/5422fa1aed915d13710007a1/2-2007_G-YMME.pdf
    - https://oat.aero/2023/03/17/airbus-a380-general-familiarisation-fuel-storage/
    - http://www.b737.org.uk/fuel.htm
    - https://slideplayer.com/slide/3854059/
    
    Inputs:
    - Wing
    - Wing mass
    - Center of gravity 

    Outputs:
    - wing moment of inertia tensor

    Properties Used:
    N/A
    '''  
    xz_symm     = wing.xz_plane_symmetric
    mass        = wing.mass_properties.mass
    vertical    = wing.vertical
    span        = wing.spans.projected
    if xz_symm:  
        m_wing = mass * 0.5
    else:
        m_wing = mass 
    
    I_global        = np.zeros((3, 3))
    I_local_non_dim = np.zeros((3, 3))
    if len(wing.segments) > 1:
        # Collect all segment tags between start and end (inclusive)
        collect = False
        seg_tags = []
        seg_bounds =  fuel_tank.segments_bounding_tank  
        for segment in wing.segments:
            if segment.tag == seg_bounds[0]:
                collect = True
            if collect:
                seg_tags.append(segment.tag)
            if segment.tag == seg_bounds[1]:
                break
    
        for i in range(len(seg_tags)-1):   
            inner_segment = wing.segments[seg_tags[i]]
            outer_segment = wing.segments[seg_tags[i+1]]
            if isinstance(wing, RCAIDE.Library.Components.Wings.Blended_Wing_Body):
                if not isinstance(inner_segment, RCAIDE.Library.Components.Wings.Segments.Blended_Wing_Body_Fuselage_Segment):
                    outer_wing_flag = True
                if outer_wing_flag:
                    inner_start     = fuel_tank.segments_percent_chord_start[i]
                    outer_start     = fuel_tank.segments_percent_chord_start[i+1]
                    inner_end       = fuel_tank.segments_percent_chord_end[i]
                    outer_end       = fuel_tank.segments_percent_chord_end[i+1]
                    tr              = inner_segment.thickness_to_chord                             
                    tt              = outer_segment.thickness_to_chord                             
                    ct              = wing.chords.root * outer_segment.root_chord_percent * (outer_start - outer_end)
                    cr              = wing.chords.root * inner_segment.root_chord_percent * (inner_start - inner_end)      
                    b               = span * (outer_segment.percent_span_location - inner_segment.percent_span_location)/(1+xz_symm)
                    A               = inner_segment.sweeps.quarter_chord                             
                    dihedral        = inner_segment.dihedral_outboard                                
                    origin_wing     = inner_segment.origin + np.array([[cr / 4, 0, 0]])     
                    m_wing          = fuel_tank.fuel.mass_properties.mass * (inner_segment.volume_properties.fuel /fuel_tank.volume_properties.gross_volume)   
                    I_section ,I_section_local_non_dim  = compute_wing_section_moment_of_intertia(m_wing,tr,tt,ct,cr, b, A,dihedral,origin_wing,xz_symm,vertical,center_of_gravity)
                    I_global        += I_section
                    I_local_non_dim += I_section_local_non_dim
                     
            else:    
                inner_start = fuel_tank.segments_percent_chord_start[i]
                outer_start = fuel_tank.segments_percent_chord_start[i+1]
                inner_end   = fuel_tank.segments_percent_chord_end[i]
                outer_end   = fuel_tank.segments_percent_chord_end[i+1] 
                tr          = inner_segment.thickness_to_chord   # root thickness as percent of chord
                tt          = outer_segment.thickness_to_chord   #tip thickness as a percent of chord
                ct          = wing.chords.root * outer_segment.root_chord_percent * (outer_start - outer_end)  # tip chord 
                cr          = wing.chords.root * inner_segment.root_chord_percent * (inner_start - inner_end)  # root chord
                b           = span * (outer_segment.percent_span_location - inner_segment.percent_span_location)/(1+xz_symm)   # half-span of the wing
                A           = inner_segment.sweeps.quarter_chord                            # sweep angle (located at quarter chord)
                dihedral    = inner_segment.dihedral_outboard                               # Wing dihedral
                origin_wing = inner_segment.origin + np.array([[cr / 4, 0, 0]]) # moves the origin of the wing to the quarter chord of the root airfoil.  
                m_wing      = fuel_tank.fuel.mass_properties.mass * (inner_segment.volume_properties.fuel /fuel_tank.volume_properties.gross_volume)  
                 
                I_section , I_section_local_non_dim  = compute_wing_section_moment_of_intertia(m_wing,tr,tt,ct,cr, b, A,dihedral,origin_wing,xz_symm,vertical,center_of_gravity)
                I_global        += I_section
                I_local_non_dim += I_section_local_non_dim
        
    else: 
        inner_start = fuel_tank.segments_percent_chord_start[i]
        outer_start = fuel_tank.segments_percent_chord_start[i+1]
        inner_end   = fuel_tank.segments_percent_chord_end[i]
        outer_end   = fuel_tank.segments_percent_chord_end[i+1]
        
        tr          = wing.thickness_to_chord # root thickness as percent of chord
        tt          = wing.thickness_to_chord #tip thickness as a percent of chord
        ct          = wing.chords.tip  * (outer_start - outer_end)# tip chord 
        cr          = wing.chords.root * (inner_start - inner_end)# root chord
        b           = span/(1+xz_symm)           # half-span of the wing
        A           = wing.sweeps.quarter_chord  # sweep angle (located at quarter chord)
        dihedral    = wing.dihedral              # Wing dihedral
        origin_wing = wing.origin + np.array([[cr / 4, 0, 0]]) # moves the origin of the wing to the quarter chord of the root airfoil.
        
   
        I_global,I_local_non_dim   = compute_wing_section_moment_of_intertia(m_wing,tr,tt,ct,cr, b, A,dihedral,origin_wing,xz_symm,vertical,center_of_gravity)
        
    # Store moment of inertia tensor on component 
    fuel_tank.fuel.mass_properties.moments_of_inertia.tensor                 = I_global
    fuel_tank.fuel.mass_properties.moments_of_inertia.non_dimensional_tensor = I_local_non_dim
    
    return I_global,  mass
    