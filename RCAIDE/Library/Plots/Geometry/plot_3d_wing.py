## @ingroup Library-Plots-Geometry
# RCAIDE/Library/Plots/Geometry/plot_3d_wing.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import RCAIDE
from RCAIDE.Framework.Core import Data
from RCAIDE.Library.Plots.Geometry.Common.contour_surface_slice import contour_surface_slice
from RCAIDE.Library.Methods.Geometry.Airfoil import import_airfoil_geometry
from RCAIDE.Library.Methods.Geometry.Airfoil import compute_naca_4series 
import numpy as np     

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Plots-Geometry
def plot_3d_wing(plot_data,wing,number_of_airfoil_points = 21, color_map='greys',alpha=1):
    """ This plots the wings of a vehicle

    Assumptions:
    None

    Source:
    None

    Inputs:
    VD.
       XA1...ZB2    - coordinates of wing vortex distribution
    color_map       - color of panel 

    Properties Used:
    N/A
    """
     
    af_pts    = number_of_airfoil_points-1 
    n_segments = len(wing.Segments)  
    if n_segments>0:
        dim =  n_segments
    else:
        dim = 2 
 
    G = generate_3d_wing_points(wing,number_of_airfoil_points,dim)
    # ------------------------------------------------------------------------
    # Plot Rotor Blade
    # ------------------------------------------------------------------------
    for sec in range(dim-1):
        for loc in range(af_pts):
            X = np.array([[G.XA1[sec,loc],G.XA2[sec,loc]],
                 [G.XB1[sec,loc],G.XB2[sec,loc]]])
            Y = np.array([[G.YA1[sec,loc],G.YA2[sec,loc]],
                 [G.YB1[sec,loc],G.YB2[sec,loc]]])
            Z = np.array([[G.ZA1[sec,loc],G.ZA2[sec,loc]],
                 [G.ZB1[sec,loc],G.ZB2[sec,loc]]]) 
             
            values      = np.ones_like(X) 
            verts       = contour_surface_slice(X, Y, Z ,values,color_map)
            plot_data.append(verts)
    if wing.symmetric:
        if wing.vertical: 
            for sec in range(dim-1):
                for loc in range(af_pts):
                    X = np.array([[G.XA1[sec,loc],G.XA2[sec,loc]],[G.XB1[sec,loc],G.XB2[sec,loc]]])
                    Y = np.array([[G.YA1[sec,loc],G.YA2[sec,loc]],[G.YB1[sec,loc],G.YB2[sec,loc]]])
                    Z = np.array([[-G.ZA1[sec,loc], -G.ZA2[sec,loc]],[-G.ZB1[sec,loc], -G.ZB2[sec,loc]]]) 
                     
                    values      = np.ones_like(X) 
                    verts       = contour_surface_slice(X, Y, Z ,values,color_map)
                    plot_data.append(verts)
        else:
            for sec in range(dim-1):
                for loc in range(af_pts):
                    X = np.array([[G.XA1[sec,loc],G.XA2[sec,loc]],[G.XB1[sec,loc],G.XB2[sec,loc]]])
                    Y = np.array([[-G.YA1[sec,loc], -G.YA2[sec,loc]], [-G.YB1[sec,loc], -G.YB2[sec,loc]]])
                    Z = np.array([[G.ZA1[sec,loc],G.ZA2[sec,loc]], [G.ZB1[sec,loc],G.ZB2[sec,loc]]]) 
                     
                    values      = np.ones_like(X) 
                    verts       = contour_surface_slice(X, Y, Z ,values,color_map)
                    plot_data.append(verts)
            
             
    return plot_data

## @ingroup Library-Plots-Geometry 
def generate_3d_wing_points(wing,n_points,dim):
    """ This generates the coordinates of the blade surface for plotting in the aircraft frame (x-back, z-up)

    Assumptions:
    None

    Source:
    None

    Inputs:
    rotor            - RCAIDE rotor
    n_points         - number of points around airfoils of each blade section
    dim              - number for radial dimension
    i                - blade number
    aircraftRefFrame - boolean to convert the coordinates from rotor frame to aircraft frame 

    Properties Used:
    N/A
    """    
    # unpack  
    # obtain the geometry for each segment in a loop                                            
    symm                 = wing.symmetric
    semispan             = wing.spans.projected*0.5 * (2 - symm) 
    root_chord           = wing.chords.root
    segments             = wing.Segments
    n_segments           = len(segments.keys()) 
    origin               = wing.origin   
        
    if n_segments > 0: 
        pts              = np.zeros((dim,n_points, 3,1))  
        section_twist    = np.zeros((dim,n_points, 3,3))
        section_twist[:, :, 0, 0] = 1        
        section_twist[:, :, 1, 1] = 1
        section_twist[:, :, 2, 2] = 1 
        translation        = np.zeros((dim,n_points, 3,1)) 
        translation[0, :, 0,:] = origin[0][0]  
        translation[0, :, 1,:] = origin[0][1]  
        translation[0, :, 2,:] = origin[0][2]  
        
        for i in range(n_segments):
            current_seg = list(segments.keys())[i]
            airfoil = wing.Segments[current_seg].Airfoil 
            if len(list(airfoil.keys())) > 0:
                af_tag =  list(airfoil.keys())[0]
                
                if type(airfoil[af_tag]) == RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil:
                    geometry = compute_naca_4series(airfoil[af_tag].NACA_4_Series_code,n_points)
                elif type(airfoil[af_tag]) == RCAIDE.Library.Components.Airfoils.Airfoil: 
                    geometry     = import_airfoil_geometry(airfoil[af_tag].coordinate_file,n_points)
            else:
                geometry = compute_naca_4series('0012',n_points)  
            
            if (i == n_segments-1):
                sweep = 0                                 
            else: 
                next_seg = list(segments.keys())[i+1]                
                if wing.Segments[current_seg].sweeps.leading_edge is not None: 
                    # If leading edge sweep is defined 
                    sweep       = wing.Segments[current_seg].sweeps.leading_edge  
                else:   
                    # If quarter chord sweep is defined, convert it to leading edge sweep
                    sweep_quarter_chord = wing.Segments[current_seg].sweeps.quarter_chord 
                    chord_fraction      = 0.25                          
                    segment_root_chord  = root_chord*wing.Segments[current_seg].root_chord_percent
                    segment_tip_chord   = root_chord*wing.Segments[next_seg].root_chord_percent
                    segment_span        = semispan*(wing.Segments[next_seg].percent_span_location - wing.Segments[current_seg].percent_span_location )
                    sweep               = np.arctan(((segment_root_chord*chord_fraction) + (np.tan(sweep_quarter_chord )*segment_span - chord_fraction*segment_tip_chord)) /segment_span) 
            dihedral = wing.Segments[current_seg].dihedral_outboard    
            twist    = wing.Segments[current_seg].twist
            
            if wing.vertical: 
                pts[i,:,0,0]   = geometry.x_coordinates * wing.Segments[current_seg].root_chord_percent * wing.chords.root 
                pts[i,:,1,0]   = geometry.y_coordinates * wing.Segments[current_seg].root_chord_percent * wing.chords.root 
                pts[i,:,2,0]   = np.zeros_like(geometry.y_coordinates) 
              
                section_twist[i,:,0,0] = np.cos(twist) 
                section_twist[i,:,0,1] = -np.sin(twist)  
                section_twist[i,:,1,0] = np.sin(twist) 
                section_twist[i,:,1,1] = np.cos(twist) 
            
            else: 
                pts[i,:,0,0]   = geometry.x_coordinates * wing.Segments[current_seg].root_chord_percent * wing.chords.root
                pts[i,:,1,0]   = np.zeros_like(geometry.y_coordinates) 
                pts[i,:,2,0]   = geometry.y_coordinates * wing.Segments[current_seg].root_chord_percent * wing.chords.root  
                                 

                section_twist[i,:,0,0] = np.cos(twist) 
                section_twist[i,:,0,2] = np.sin(twist)  
                section_twist[i,:,2,0] = -np.sin(twist) 
                section_twist[i,:,2,2] =  np.cos(twist)  
             
            if (i != n_segments-1):
                # update origin for next segment 
                segment_percent_span =    wing.Segments[next_seg].percent_span_location - wing.Segments[current_seg].percent_span_location     
                if wing.vertical:
                    inverted_wing = -np.sign(abs(dihedral) - np.pi/2)
                    if inverted_wing  == 0:
                        inverted_wing  = 1
                    dz = inverted_wing*semispan*segment_percent_span
                    dy = dz*np.tan(dihedral)
                    l  = dz/np.cos(dihedral)
                    dx = l*np.tan(sweep)
                else:
                    inverted_wing = np.sign(dihedral)
                    if inverted_wing  == 0:
                        inverted_wing  = 1
                    dy = inverted_wing*semispan*segment_percent_span
                    dz = dy*np.tan(dihedral)
                    l  = dy/np.cos(dihedral)
                    dx = l*np.tan(sweep)
                translation[i+1,:,0,:] = translation[i,:,0,:] + dx
                translation[i+1,:,1,:] = translation[i,:,1,:] + dy
                translation[i+1,:,2,:] = translation[i,:,2,:] + dz  
    else:

        pts              = np.zeros((dim,n_points, 3,1))  
        section_twist    = np.zeros((dim,n_points, 3,3))
        section_twist[:, :, 0, 0] = 1        
        section_twist[:, :, 1, 1] = 1
        section_twist[:, :, 2, 2] = 1
        translation      = np.zeros((dim,n_points, 3,1))
        
        airfoil = wing.Airfoil 
        if len(list(airfoil.keys())) > 0:
            af_tag =  list(airfoil.keys())[0]
            
            if type(airfoil[af_tag]) == RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil:
                geometry = compute_naca_4series(airfoil[af_tag].NACA_4_Series_code,n_points)
            elif type(airfoil[af_tag]) == RCAIDE.Library.Components.Airfoils.Airfoil: 
                geometry     = import_airfoil_geometry(airfoil[af_tag].coordinate_file,n_points)
        else:
            geometry = compute_naca_4series('0012',n_points)
            
        dihedral              = wing.dihedral
        if wing.sweeps.leading_edge  is not None: 
            sweep      = wing.sweeps.leading_edge
        else:  
            sweep_quarter_chord = wing.sweeps.quarter_chord 
            chord_fraction      = 0.25                          
            segment_root_chord  = wing.chords.root
            segment_tip_chord   = wing.chords.tip
            segment_span        = semispan 
            sweep       = np.arctan(((segment_root_chord*chord_fraction) + (np.tan(sweep_quarter_chord )*segment_span - chord_fraction*segment_tip_chord)) /segment_span)  
           
        # append root section     
        translation[:, :, 0,:] = origin[0][0]  
        translation[:, :, 1,:] = origin[0][1]  
        translation[:, :, 2,:] = origin[0][2] 
       
        if wing.vertical: 
            pts[0,:,0,0]   = geometry.x_coordinates *  wing.chords.root
            pts[0,:,1,0]   = geometry.y_coordinates *  wing.chords.root
            pts[0,:,2,0]   = np.zeros_like(geometry.y_coordinates)
            
            pts[1,:,0,0]   = geometry.x_coordinates *  wing.chords.tip  
            pts[1,:,1,0]   = geometry.y_coordinates *  wing.chords.tip  
            pts[1,:,2,0]   = np.zeros_like(geometry.y_coordinates)   
            
            translation[1, :, 0,:] += semispan*np.tan(sweep)
            translation[1, :, 1,:] += semispan*np.tan(dihedral) 
            translation[1, :, 2,:] += semispan 

            section_twist[0,:,0,0] = np.cos(wing.twists.root) 
            section_twist[0,:,0,1] = -np.sin(wing.twists.root)  
            section_twist[0,:,1,0] = np.sin(wing.twists.root) 
            section_twist[0,:,1,1] = np.cos(wing.twists.root)
             
            section_twist[1,:,0,0] = np.cos(wing.twists.tip) 
            section_twist[1,:,0,1] = -np.sin(wing.twists.tip)  
            section_twist[1,:,1,0] = np.sin(wing.twists.tip) 
            section_twist[1,:,1,1] = np.cos(wing.twists.tip)
            
            
        else:
            pts[0,:,0,0]   = geometry.x_coordinates *  wing.chords.root
            pts[0,:,1,0]   = np.zeros_like(geometry.y_coordinates) 
            pts[0,:,2,0]   = geometry.y_coordinates *  wing.chords.root
            
            pts[1,:,0,0]   = geometry.x_coordinates *  wing.chords.tip  
            pts[1,:,1,0]   = np.zeros_like(geometry.y_coordinates)  
            pts[1,:,2,0]   = geometry.y_coordinates *  wing.chords.tip  
            
    
            translation[1, :, 0,:] +=  semispan*np.tan(sweep)
            translation[1, :, 1,:] += semispan 
            translation[1, :, 2,:] += semispan*np.tan(dihedral)     

            section_twist[0,:,0,0] = np.cos(wing.twists.root) 
            section_twist[0,:,0,2] = np.sin(wing.twists.root)  
            section_twist[0,:,2,0] = -np.sin(wing.twists.root) 
            section_twist[0,:,2,2] =  np.cos(wing.twists.root)
             
            section_twist[1,:,0,0] = np.cos(wing.twists.tip) 
            section_twist[1,:,0,2] = np.sin(wing.twists.tip)  
            section_twist[1,:,2,0] = -np.sin(wing.twists.tip) 
            section_twist[1,:,2,2] =  np.cos(wing.twists.tip) 
 
    mat     = translation + np.matmul(section_twist ,pts)
    
    # ---------------------------------------------------------------------------------------------
    # create empty data structure for storing geometry
    G = Data()

    # store node points
    G.X    = mat[:,:,0,0]  
    G.Y    = mat[:,:,1,0]  
    G.Z    = mat[:,:,2,0]
    G.PTS  = mat[:,:,:,0]

    # store points
    G.XA1  = mat[:-1,:-1,0,0] 
    G.YA1  = mat[:-1,:-1,1,0] 
    G.ZA1  = mat[:-1,:-1,2,0] 
    G.XA2  = mat[:-1,1:,0,0]  
    G.YA2  = mat[:-1,1:,1,0]  
    G.ZA2  = mat[:-1,1:,2,0]  
    G.XB1  = mat[1:,:-1,0,0]  
    G.YB1  = mat[1:,:-1,1,0]  
    G.ZB1  = mat[1:,:-1,2,0]  
    G.XB2  = mat[1:,1:,0,0]   
    G.YB2  = mat[1:,1:,1,0]   
    G.ZB2  = mat[1:,1:,2,0]      
    
    return G
     


