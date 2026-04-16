# RCAIDE/Library/Methods/Aerodynamics/Vortex_Lattice_Method/generate_wing_vortex_distribution.py
# 
# Created:  May 2018, M. Clarke
# Modified: Apr 2020, M. Clarke
#           Jun 2021, A. Blaufox

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import RCAIDE
from RCAIDE.Framework.Core                                  import  Data , Units
from RCAIDE.Library.Methods.Geometry.Airfoil                import compute_naca_4series, import_airfoil_geometry
from RCAIDE.Library.Methods.Geometry.Planform.convert_sweep import convert_sweep_segments
  
# package imports 
import numpy as np


# ----------------------------------------------------------------------
#  Discretize Wings
# ----------------------------------------------------------------------
def generate_wing_vortex_distribution_new(VD,wing,n_cw,n_sw,spc,precision):
    """ This generates vortex distribution points for the given wing 

    Assumptions: 
    The wing is segmented and was made or modified by make_VLM_wings()
    
    For control surfaces, "positve" deflection corresponds to the RH rule where the axis of rotation is the OUTBOARD-pointing hinge vector
    symmetry: the LH rule is applied to the reflected surface for non-ailerons. Ailerons follow a RH rule for both sides
    
    The hinge_vector will only ever be calcualted on the first strip of any control/all-moving surface. It is assumed that all control
    surfaces are trapezoids, thus needing only one hinge, and that all all-moving surfaces have exactly one point of rotation.

    Source:   
    None
    
    Inputs:   
    VD                   - vortex distribution
    wing                 - a Data object made or modified by make_VLM_wings() to mimick a Wing object
    
    Properties Used:
    N/A
    """  
    # get geometry of wing  
    span          = wing.spans.projected
    xz_sym        = wing.xz_plane_symmetric 
    xy_sym        = wing.xy_plane_symmetric 
    yz_sym        = wing.yz_plane_symmetric  
    wing_origin   = wing.origin[0]
    VD.vortex_lift.append(wing.vortex_lift)

    # determine if vehicle has symmetry 
    if xz_sym is True :
        span = span/2
        VD.vortex_lift.append(wing.vortex_lift)
        
    VD.counter  +=1
    wing.surface_ID = VD.counter*1

    # ---------------------------------------------------------------------------------------
    # STEP 3: Get discretization control variables  
    # --------------------------------------------------------------------------------------- 
    # get y_coordinates (y-locations of the edges of each strip in wing-local coords)
    if spc == True: # discretize wing using cosine spacing     
        n               = np.linspace(n_sw+1,0,n_sw+1)         # vectorize
        thetan          = n*(np.pi/2)/(n_sw+1)                 # angular stations 
        y_coordinates   = span*np.cos(thetan)   # y locations based on the angular spacing           
    else:    
        y_coordinates  = np.linspace(0,span,n_sw+1)  # y locations based on the angular spacing
 
    # ---------------------------------------------------------------------------------------
    # STEP 4: Setup span_break and section arrays. A 'section' is the trapezoid between two
    #         span_breaks. A 'span_break' is described in the file make_VLM_wings.py
    # ---------------------------------------------------------------------------------------  
    del_y = y_coordinates[1:] - y_coordinates[:-1]   
    
    # -------------------------------------------------------------------------------------------------------------
    # Run the strip contruction loop again if wing is symmetric. 
    # Reflection plane = x-y plane for vertical wings. Otherwise, reflection plane = x-z plane 
    symmetry_mask = np.array([[0,0,0],[yz_sym,xz_sym,xy_sym]])
    signs         = np.array([1, -1])  
    side_idx = 0
    for _ in signs[[True,xz_sym]]:

        yz_sym_sign   = 1 if symmetry_mask[side_idx,0] == 0 else -1
        xz_sym_sign   = 1 if symmetry_mask[side_idx,1] == 0 else -1
        xy_sym_sign   = 1 if symmetry_mask[side_idx,2] == 0 else -1
        
        # create empty vectors for coordinates 
        xah_w  = np.zeros((n_sw,n_cw))
        yah_w  = np.zeros((n_sw,n_cw))
        zah_w  = np.zeros((n_sw,n_cw))
        xbh_w  = np.zeros((n_sw,n_cw))
        ybh_w  = np.zeros((n_sw,n_cw))
        zbh_w  = np.zeros((n_sw,n_cw))   
        xch_w  = np.zeros((n_sw,n_cw))
        ych_w  = np.zeros((n_sw,n_cw))
        zch_w  = np.zeros((n_sw,n_cw))   
        xa1_w  = np.zeros((n_sw,n_cw))
        ya1_w  = np.zeros((n_sw,n_cw))
        za1_w  = np.zeros((n_sw,n_cw))
        xa2_w  = np.zeros((n_sw,n_cw))
        ya2_w  = np.zeros((n_sw,n_cw))
        za2_w  = np.zeros((n_sw,n_cw))   
        xb1_w  = np.zeros((n_sw,n_cw))
        yb1_w  = np.zeros((n_sw,n_cw))
        zb1_w  = np.zeros((n_sw,n_cw))
        xb2_w  = np.zeros((n_sw,n_cw))
        yb2_w  = np.zeros((n_sw,n_cw))
        zb2_w  = np.zeros((n_sw,n_cw))   
        xac_w  = np.zeros((n_sw,n_cw))
        yac_w  = np.zeros((n_sw,n_cw))
        zac_w  = np.zeros((n_sw,n_cw))   
        xbc_w  = np.zeros((n_sw,n_cw))
        ybc_w  = np.zeros((n_sw,n_cw))
        zbc_w  = np.zeros((n_sw,n_cw)) 
        xc_w   = np.zeros((n_sw,n_cw))
        yc_w   = np.zeros((n_sw,n_cw))
        zc_w   = np.zeros((n_sw,n_cw))
        x_w    = np.zeros((n_sw+1,n_cw+1)) # may have to change to make space for split if control surfaces are allowed to have more than two Segments
        y_w    = np.zeros((n_sw+1,n_cw+1)) 
        z_w    = np.zeros((n_sw+1,n_cw+1))         
        cs_ws  = np.zeros(n_sw+1) 
        
        # adjust origin for symmetry with special case for vertical symmetry 
        wing_origin_x = wing_origin[0] * yz_sym_sign
        wing_origin_y = wing_origin[1] * xz_sym_sign
        wing_origin_z = wing_origin[2] * xy_sym_sign
             
        seg_idx       = 0
        wing_seg_tags = list(wing.segments.keys())
        for y_i in range(len(y_coordinates)):
            delta_y = y_coordinates[y_i]
            eta_y   = delta_y / span
            
            # Step 1. check to see if y-location of horseshoe vortex is within current wing segment  
            inboard_segment  = wing.segments[wing_seg_tags[seg_idx]]
            outboard_segment = wing.segments[wing_seg_tags[seg_idx+1]]
            
            if delta_y == outboard_segment.percent_span_location * span:
                pass 
            elif delta_y >= outboard_segment.percent_span_location * span: 
                seg_idx += 1
                inboard_segment = wing.segments[wing_seg_tags[seg_idx]]
                outboard_segment = wing.segments[wing_seg_tags[seg_idx+1]]              
                
            # Step 2. get segment properties  
            segment_root_chord    = wing.chords.root*inboard_segment.root_chord_percent
            segment_tip_chord     = wing.chords.root*outboard_segment.root_chord_percent 
            segment_root_twist    = inboard_segment.twist
            segment_tip_twist     = outboard_segment.twist 
            inboard_segment_y     = inboard_segment.percent_span_location * span   
            outboard_segment_y    = outboard_segment.percent_span_location * span 
            segment_span          = outboard_segment_y -  inboard_segment_y   
            local_y_val           = delta_y - inboard_segment_y
            local_percent_y_val   = local_y_val /segment_span 
            local_chord           = segment_root_chord -  (segment_root_chord - segment_tip_chord) *  local_y_val / segment_span
            local_twist           = segment_root_twist -  (segment_root_twist - segment_tip_twist) *  local_y_val / segment_span
            
            # Step 3. get global shift 
            # guarantee that all segments have leading edge sweep
            if inboard_segment.sweeps.leading_edge is None:
                old_sweep                 = inboard_segment.sweeps.quarter_chord
                new_sweep                 = convert_sweep_segments(old_sweep, inboard_segment, outboard_segment, wing, old_ref_chord_fraction=0.25, new_ref_chord_fraction=0.0)
                inboard_segment.sweeps.leading_edge = new_sweep 
                
            dihedral = inboard_segment.dihedral_outboard
            LE_sweep = inboard_segment.sweeps.leading_edge
            delta_z  = inboard_segment.origin[0][2] +  np.tan(dihedral) * local_y_val
            delta_x  = inboard_segment.origin[0][0] +  np.tan(LE_sweep) * local_y_val 
             
            # Step 4. get points of airfoil
            airfoil_x_pts_0 , airfoil_z_pts_0 = generate_interplated_airfoil_points(inboard_segment, outboard_segment,n_cw+1,local_percent_y_val) 
            
            airfoil_x_pts_1 = np.linspace(0.,1.,n_cw+1)
            airfoil_z_pts_1 = np.interp(airfoil_x_pts_1, airfoil_x_pts_0, airfoil_z_pts_0)
            
            # Step 5 scale airfoil by local chord 
            airfoil_x_pts_2 = airfoil_x_pts_1*local_chord
            airfoil_z_pts_2 = airfoil_z_pts_1*local_chord
             
            # Step 6. get control surface deflection and modify airfoil 
            LE_angle          = 0.0
            LE_chord_fraction = 0.0
            TE_angle          = 0.0 
            TE_chord_fraction = 0.0
            
            for cs in wing.control_surfaces: 
                if eta_y >= cs.span_fraction_start and  eta_y <= cs.span_fraction_end:  
                    if type(cs) == RCAIDE.Library.Components.Wings.Control_Surfaces.Slat: 
                        LE_angle          = cs.deflection  
                        LE_chord_fraction = cs.chord_fraction
                    if type(cs) == RCAIDE.Library.Components.Wings.Control_Surfaces.Aileron: 
                        TE_angle          = cs.deflection * xz_sym_sign 
                        TE_chord_fraction = cs.chord_fraction
                    else:
                        TE_angle          = cs.deflection * xz_sym_sign 
                        TE_chord_fraction = cs.chord_fraction 
            
            airfoil_x_pts_3, airfoil_z_pts_3 = apply_control_surface_deflections(airfoil_x_pts_2, airfoil_z_pts_2,LE_angle, LE_chord_fraction, TE_angle, TE_chord_fraction)
           
            # rotate airfoil by twist
            airfoil_x_pts_4 = np.cos(local_twist)*airfoil_x_pts_3 + np.sin(local_twist)*airfoil_z_pts_3
            airfoil_z_pts_4 = - np.sin(local_twist)*airfoil_x_pts_3 + np.cos(local_twist)*airfoil_z_pts_3
            
            # shift points from origin [0,0,0] to relative wing origin
            airfoil_x_pts_5 = airfoil_x_pts_4 + delta_x
            airfoil_z_pts_5 = airfoil_z_pts_4 + delta_z
            
            # store points
            x_wing_pts = airfoil_x_pts_5
            y_wing_pts = np.ones(len(x_wing_pts))*delta_y 
            z_wing_pts = airfoil_z_pts_5 
             
            #wing.inverted_wing = -np.sign(break_dihedral[i_break] - np.pi/2)  
             
            # store coordinates of panels, horseshoeces vortices and control points relative to wing root----------
            if wing.vertical:
                x_w[y_i,:] = x_wing_pts
                y_w[y_i,:] = z_wing_pts
                z_w[y_i,:] = y_wing_pts 
            else:
                x_w[y_i,:] = x_wing_pts
                y_w[y_i,:] = y_wing_pts
                z_w[y_i,:] = z_wing_pts 

            # handle flips for symmetric wings 
            if side_idx == 1:
                x_w[y_i,:] = x_w[y_i,:] * yz_sym_sign
                y_w[y_i,:] = y_w[y_i,:] * xz_sym_sign
                z_w[y_i,:] = z_w[y_i,:] * xy_sym_sign  
            
            cs_ws[y_i] = local_chord
            
        cs_w  = (cs_ws[:1] +  cs_ws[1:]) / 2
        xa1_w = x_w[:-1,:-1]
        ya1_w = y_w[:-1,:-1]
        za1_w = z_w[:-1,:-1]
        xa2_w = x_w[:-1,1:]
        ya2_w = y_w[:-1,1:]
        za2_w = z_w[:-1,1:]
        xb1_w = x_w[1:,:-1]
        yb1_w = y_w[1:,:-1]
        zb1_w = z_w[1:,:-1]
        xb2_w = x_w[1:,1:]
        yb2_w = y_w[1:,1:]
        zb2_w = z_w[1:,1:]

        xac_w = xa1_w + 0.75*(xa2_w - xa1_w)
        yac_w = ya1_w
        zac_w = za1_w + 0.75*(za2_w - za1_w)
        xbc_w = xb1_w + 0.75*(xb2_w - xb1_w)
        ybc_w = yb1_w
        zbc_w = zb1_w + 0.75*(zb2_w - zb1_w)

        xah_w = xa1_w + 0.25*(xa2_w - xa1_w)
        yah_w = ya1_w
        zah_w = za1_w + 0.25*(za2_w - za1_w)
        xbh_w = xb1_w + 0.25*(xb2_w - xb1_w)
        ybh_w = yb1_w
        zbh_w = zb1_w + 0.25*(zb2_w - zb1_w)
 
        xch_w = (xah_w + xbh_w)/2
        ych_w = (yah_w + ybh_w)/2
        zch_w = (zah_w + zbh_w)/2
        xc_w  = (xac_w + xbc_w)/2
        yc_w  = (yac_w + ybc_w)/2
        zc_w  = (zac_w + zbc_w)/2

        # store this strip's discretization information--------------------------------------------------------
        LE_inds        = np.full(n_cw, False)
        TE_inds        = np.full(n_cw, False)
        LE_inds[0]     = True
        TE_inds[-1]    = True
        
        RNMAX          = np.ones(n_cw, np.int16)*n_cw
        panel_numbers  = np.linspace(1,n_cw,n_cw, dtype=np.int16)            
                    
        VD.panels_per_strip          = np.append(VD.panels_per_strip         , RNMAX                    )
        VD.chordwise_panel_number    = np.append(VD.chordwise_panel_number   , panel_numbers            )   
        
        # adjusting coordinate axis so reference point is at the nose of the aircraft------------------------------
        xah = xah_w + wing_origin_x # x coordinate of left corner of bound vortex 
        yah = yah_w + wing_origin_y # y coordinate of left corner of bound vortex 
        zah = zah_w + wing_origin_z # z coordinate of left corner of bound vortex 
        xbh = xbh_w + wing_origin_x # x coordinate of right corner of bound vortex 
        ybh = ybh_w + wing_origin_y # y coordinate of right corner of bound vortex 
        zbh = zbh_w + wing_origin_z # z coordinate of right corner of bound vortex 
        xch = xch_w + wing_origin_x # x coordinate of center of bound vortex on panel
        ych = ych_w + wing_origin_y # y coordinate of center of bound vortex on panel
        zch = zch_w + wing_origin_z # z coordinate of center of bound vortex on panel  
    
        xa1 = xa1_w + wing_origin_x # x coordinate of top left corner of panel
        ya1 = ya1_w + wing_origin_y # y coordinate of bottom left corner of panel
        za1 = za1_w + wing_origin_z # z coordinate of top left corner of panel
        xa2 = xa2_w + wing_origin_x # x coordinate of bottom left corner of panel
        ya2 = ya2_w + wing_origin_y # y coordinate of bottom left corner of panel
        za2 = za2_w + wing_origin_z # z coordinate of bottom left corner of panel  
    
        xb1 = xb1_w + wing_origin_x # x coordinate of top right corner of panel  
        yb1 = yb1_w + wing_origin_y # y coordinate of top right corner of panel 
        zb1 = zb1_w + wing_origin_z # z coordinate of top right corner of panel 
        xb2 = xb2_w + wing_origin_x # x coordinate of bottom rightcorner of panel 
        yb2 = yb2_w + wing_origin_y # y coordinate of bottom rightcorner of panel 
        zb2 = zb2_w + wing_origin_z # z coordinate of bottom right corner of panel                   
    
        xac = xac_w + wing_origin_x  # x coordinate of control points on panel
        yac = yac_w + wing_origin_y  # y coordinate of control points on panel
        zac = zac_w + wing_origin_z  # z coordinate of control points on panel
        xbc = xbc_w + wing_origin_x  # x coordinate of control points on panel
        ybc = ybc_w + wing_origin_y  # y coordinate of control points on panel
        zbc = zbc_w + wing_origin_z  # z coordinate of control points on panel
    
        xc  = xc_w  + wing_origin_x  # x coordinate of control points on panel
        yc  = yc_w  + wing_origin_y  # y coordinate of control points on panel
        zc  = zc_w  + wing_origin_z  # y coordinate of control points on panel
        x   =  x_w   + wing_origin_x  # x coordinate of control points on panel
        y   =  y_w   + wing_origin_y  # y coordinate of control points on panel
        z   =  z_w   + wing_origin_z  # y coordinate of control points on panel
        
        # VD discretization information----------------------------------------------------------------------------
        
        # increment number of wings and panels
        n_panels = len(xch)
        VD.n_w  += 1             
        VD.n_cp += n_panels 
        
        # store this wing's discretization information  
        first_panel_ind  = VD.XAH.size
        first_strip_ind  = VD.chordwise_breaks.size
        chordwise_breaks = first_panel_ind + np.arange(n_panels)[0::n_cw]
        ID               = VD.counter*1
        
        VD.chordwise_breaks = np.append(VD.chordwise_breaks, np.int32(chordwise_breaks))
        VD.spanwise_breaks  = np.append(VD.spanwise_breaks , np.int32(first_strip_ind ))            
        VD.n_sw             = np.append(VD.n_sw            , np.int16(n_sw)            )
        VD.n_cw             = np.append(VD.n_cw            , np.int16(n_cw)            )
        VD.surface_ID       = np.append(VD.surface_ID      , np.ones(n_cw*n_sw)*ID*xz_sym_sign) # Update me when the loop is gone
        VD.surface_ID_full  = np.append(VD.surface_ID_full , np.ones((n_cw+1)*(n_sw+1))*ID*xz_sym_sign) # Update me when the loop is gone    
                
        # ---------------------------------------------------------------------------------------
        # STEP 7: Store wing in vehicle vector
        # --------------------------------------------------------------------------------------- 
        VD.XAH    = np.append(VD.XAH  , np.array(xah  , dtype=precision))
        VD.YAH    = np.append(VD.YAH  , np.array(yah  , dtype=precision))
        VD.ZAH    = np.append(VD.ZAH  , np.array(zah  , dtype=precision))
        VD.XBH    = np.append(VD.XBH  , np.array(xbh  , dtype=precision))
        VD.YBH    = np.append(VD.YBH  , np.array(ybh  , dtype=precision))
        VD.ZBH    = np.append(VD.ZBH  , np.array(zbh  , dtype=precision))
        VD.XCH    = np.append(VD.XCH  , np.array(xch  , dtype=precision))
        VD.YCH    = np.append(VD.YCH  , np.array(ych  , dtype=precision))
        VD.ZCH    = np.append(VD.ZCH  , np.array(zch  , dtype=precision))            
        VD.XA1    = np.append(VD.XA1  , np.array(xa1  , dtype=precision))
        VD.YA1    = np.append(VD.YA1  , np.array(ya1  , dtype=precision))
        VD.ZA1    = np.append(VD.ZA1  , np.array(za1  , dtype=precision))
        VD.XA2    = np.append(VD.XA2  , np.array(xa2  , dtype=precision))
        VD.YA2    = np.append(VD.YA2  , np.array(ya2  , dtype=precision))
        VD.ZA2    = np.append(VD.ZA2  , np.array(za2  , dtype=precision))        
        VD.XB1    = np.append(VD.XB1  , np.array(xb1  , dtype=precision))
        VD.YB1    = np.append(VD.YB1  , np.array(yb1  , dtype=precision))
        VD.ZB1    = np.append(VD.ZB1  , np.array(zb1  , dtype=precision))
        VD.XB2    = np.append(VD.XB2  , np.array(xb2  , dtype=precision))                
        VD.YB2    = np.append(VD.YB2  , np.array(yb2  , dtype=precision))        
        VD.ZB2    = np.append(VD.ZB2  , np.array(zb2  , dtype=precision)) 
        VD.XAC    = np.append(VD.XAC  , np.array(xac  , dtype=precision))
        VD.YAC    = np.append(VD.YAC  , np.array(yac  , dtype=precision)) 
        VD.ZAC    = np.append(VD.ZAC  , np.array(zac  , dtype=precision)) 
        VD.XBC    = np.append(VD.XBC  , np.array(xbc  , dtype=precision))
        VD.YBC    = np.append(VD.YBC  , np.array(ybc  , dtype=precision)) 
        VD.ZBC    = np.append(VD.ZBC  , np.array(zbc  , dtype=precision))  
        VD.XC     = np.append(VD.XC   , np.array(xc   , dtype=precision))
        VD.YC     = np.append(VD.YC   , np.array(yc   , dtype=precision))
        VD.ZC     = np.append(VD.ZC   , np.array(zc   , dtype=precision))  
        VD.X      = np.append(VD.X    , np.array(x    , dtype=precision))
        VD.Y      = np.append(VD.Y    , np.array(y    , dtype=precision))
        VD.Z      = np.append(VD.Z    , np.array(z    , dtype=precision))         
        VD.CS     = np.append(VD.CS   , np.array(cs_w , dtype=precision)) 
        VD.DY     = np.append(VD.DY   , np.array(del_y, dtype=precision))
        
        side_idx += 1
        
    VD.symmetric_wings = np.append(VD.symmetric_wings, int(xz_sym))
    
    # Pack wing data
    wing.n_sw = n_sw
    wing.n_cw = n_cw    
    
    return VD

def generate_interplated_airfoil_points(inboard_segment,outboard_segment,n_cw,local_percent_y_val,npts=100): 
        """ Takes in two airfoils, interpolates between their coordinates to generate new
        airfoil geometries and saves new airfoil files.
        
        Assumptions: Linear geometric transition between airfoils
        
        Source: None
        
        Inputs:
        a1                 first airfoil                                [ airfoil ]
        a2                 second airfoil                               [ airfoil ]
        nairfoils          number of airfoils                           [ unitless ]
        
        """
        
        # Get points of inboard segment airfoil 
        if inboard_segment.airfoil: 
            if type(inboard_segment.airfoil) == RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil: 
                a_geo_1 = compute_naca_4series(inboard_segment.airfoil.NACA_4_Series_code,npts*2+1)
            else:
                a_geo_1 = import_airfoil_geometry(inboard_segment.airfoil.coordinate_file,npts*2+1)   
        else:
            a_geo_1 =  Data()
            a_geo_1.camber_coordinates = np.zeros(npts)              
            a_geo_1.x_upper_surface    = np.linspace(0,1,npts)
    
    
        # Get points of outboard segment airfoil     
        if outboard_segment.airfoil: 
            if type(outboard_segment.airfoil) == RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil: 
                a_geo_2 = compute_naca_4series(outboard_segment.airfoil.NACA_4_Series_code,npts*2+1)
            else:
                a_geo_2 = import_airfoil_geometry(outboard_segment.airfoil.coordinate_file,npts*2+1)   
        else:
            a_geo_2 =  Data()
            a_geo_2.camber_coordinates = np.zeros(npts)              
            a_geo_2.x_upper_surface    = np.linspace(0,1,npts)
                
        
        # for each point around the airfoil, interpolate between the two given airfoil coordinates
        z = np.linspace(0,1,npts)
        
        y_u_lb = a_geo_1.camber_coordinates 
        y_u_ub = a_geo_2.camber_coordinates  
        x_u_lb = a_geo_1.x_upper_surface 
        x_u_ub = a_geo_2.x_upper_surface    
        
        # broadcasting interpolation
        cambers = (z[None,...] * (y_u_ub[...,None] - y_u_lb[...,None]) + (y_u_lb[...,None])).T 
        x_vals  = (z[None,...] * (x_u_ub[...,None] - x_u_lb[...,None]) + (x_u_lb[...,None])).T  
           
        idx = int(local_percent_y_val *npts)
        
        if idx == len(cambers):
            idx -= 1
        airfoil_z_coords = cambers[idx]
        airfoil_x_coords = x_vals[idx]
         
        return airfoil_x_coords, airfoil_z_coords
    
    
def apply_control_surface_deflections(airfoil_x_pts_2, airfoil_z_pts_2,LE_angle, LE_chord_fraction, TE_angle, TE_chord_fraction):

    chord = airfoil_x_pts_2[-1]
    LE_chord_loc = chord*LE_chord_fraction
    TE_chord_loc = chord*(1-TE_chord_fraction)
 
    LE_hinge_distance = LE_chord_loc - airfoil_x_pts_2
    LE_hinge_distance[airfoil_x_pts_2>LE_chord_loc] = 0

    TE_hinge_distance = airfoil_x_pts_2 - TE_chord_loc 
    TE_hinge_distance[airfoil_x_pts_2<TE_chord_loc] = 0

    LE_deflection = np.tan(LE_angle)*LE_hinge_distance
    TE_deflection = np.tan(TE_angle)*TE_hinge_distance
    Total_CS_deflection = LE_deflection + TE_deflection

    # shift points of airfoil by control surface deflection 
    airfoil_x_pts_3 = airfoil_x_pts_2
    airfoil_z_pts_3 = airfoil_z_pts_2 + Total_CS_deflection        

    return airfoil_x_pts_3, airfoil_z_pts_3

# ----------------------------------------------------------------------
#  Discretize Wings
# ----------------------------------------------------------------------
def generate_wing_vortex_distribution(VD,wing,n_cw,n_sw,spc,precision):
    """ This generates vortex distribution points for the given wing 

    Assumptions: 
    The wing is segmented and was made or modified by make_VLM_wings()
    
    For control surfaces, "positve" deflection corresponds to the RH rule where the axis of rotation is the OUTBOARD-pointing hinge vector
    symmetry: the LH rule is applied to the reflected surface for non-ailerons. Ailerons follow a RH rule for both sides
    
    The hinge_vector will only ever be calcualted on the first strip of any control/all-moving surface. It is assumed that all control
    surfaces are trapezoids, thus needing only one hinge, and that all all-moving surfaces have exactly one point of rotation.

    Source:   
    None
    
    Inputs:   
    VD                   - vortex distribution
    wing                 - a Data object made or modified by make_VLM_wings() to mimick a Wing object
    
    Properties Used:
    N/A
    """ 
    wings = VD.VLM_wings
    
    # get geometry of wing  
    span          = wing.spans.projected
    xz_sym        = wing.xz_plane_symmetric 
    xy_sym        = wing.xy_plane_symmetric 
    yz_sym        = wing.yz_plane_symmetric  
    wing_origin   = wing.origin[0]
    VD.vortex_lift.append(wing.vortex_lift)

    # determine if vehicle has symmetry 
    if xz_sym is True :
        span = span/2
        VD.vortex_lift.append(wing.vortex_lift)
        
    VD.counter  +=1
    wing.surface_ID = VD.counter*1

    # ---------------------------------------------------------------------------------------
    # STEP 3: Get discretization control variables  
    # ---------------------------------------------------------------------------------------
    # get number of spanwise and chordwise panels for this wing
    n_sw = n_sw  if (not wing.is_a_control_surface) else max(len(wing.y_coords_required)-1,2) 
    n_cw = n_cw  if (not wing.is_a_control_surface) else max(int(np.ceil(wing.chord_fraction*n_cw)),2)  
    
    # get y_coordinates (y-locations of the edges of each strip in wing-local coords)
    if spc == True: # discretize wing using cosine spacing     
        n               = np.linspace(n_sw+1,0,n_sw+1)         # vectorize
        thetan          = n*(np.pi/2)/(n_sw+1)                 # angular stations
        if wing.vertical:
            z_coordinates   =  span*np.cos(thetan) # z locations based on the angular spacing
        else: 
            y_coordinates   = span*np.cos(thetan)   # y locations based on the angular spacing           
    else:  # discretize wing using linear spacing   
        if wing.vertical:    
            z_coordinates = np.linspace(0,span,n_sw+1)   # z locations based on the angular spacing
        else:  
            y_coordinates  = np.linspace(0,span,n_sw+1)  # y locations based on the angular spacing

    # get span_breaks object
    span_breaks   = wing.span_breaks
    n_breaks      = len(span_breaks)

    # ---------------------------------------------------------------------------------------
    # STEP 4: Setup span_break and section arrays. A 'section' is the trapezoid between two
    #         span_breaks. A 'span_break' is described in the file make_VLM_wings.py
    # ---------------------------------------------------------------------------------------
    break_chord       = np.zeros(n_breaks)
    break_twist       = np.zeros(n_breaks)
    break_sweep       = np.zeros(n_breaks)
    break_dihedral    = np.zeros(n_breaks)
    break_camber_xs   = [] 
    break_camber_zs   = []
    break_camber_ys   = []
    break_x_offset    = np.zeros(n_breaks)
    break_z_offset    = np.zeros(n_breaks)
    break_y_offset    = np.zeros(n_breaks)
    break_spans       = np.zeros(n_breaks) 
    section_span      = np.zeros(n_breaks)
    section_area      = np.zeros(n_breaks)
    section_LE_cut    = np.zeros(n_breaks)
    section_TE_cut    = np.ones(n_breaks)

    # ---------------------------------------------------------------------------------------
    # STEP 5:  Obtain sweep, chord, dihedral and twist at the beginning/end of each break.
    #          If applicable, append airfoil section VD and flap/aileron deflection angles.
    # --------------------------------------------------------------------------------------- 
    for i_break in range(n_breaks):
        break_spans[i_break]    = span_breaks[i_break].span_fraction*span  
        break_chord[i_break]    = span_breaks[i_break].local_chord
        break_twist[i_break]    = span_breaks[i_break].twist
        break_dihedral[i_break] = span_breaks[i_break].dihedral_outboard                    

        # get leading edge sweep. make_VLM wings should have precomputed this for all span_breaks
        is_not_last_break    = (i_break != n_breaks-1)
        break_sweep[i_break] = span_breaks[i_break].sweep_outboard_LE if is_not_last_break else 0
    
        if wing.vertical:
            # find span and area. All span_break offsets should be calculated in make_VLM_wings
            if i_break == 0:
                section_span[i_break]   = 0.0
                break_x_offset[i_break] = 0.0  
                break_y_offset[i_break] = 0.0       
            else:
                section_span[i_break]   = break_spans[i_break] - break_spans[i_break-1]
                section_area[i_break]   = 0.5*(break_chord[i_break-1] + break_chord[i_break])*section_span[i_break]
                break_x_offset[i_break] = span_breaks[i_break].x_offset
                break_y_offset[i_break] = span_breaks[i_break].dih_offset
    
            # Get airfoil section VD  
            if span_breaks[i_break].airfoil: 
                if type(span_breaks[i_break].airfoil) == RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil: # check if naca 4 series of airfoil from datafile
                    airfoil_geo_data = compute_naca_4series(span_breaks[i_break].airfoil.NACA_4_Series_code,span_breaks[i_break].airfoil.number_of_points-2)
                else:
                    airfoil_geo_data = import_airfoil_geometry(span_breaks[i_break].airfoil.coordinate_file)  
                break_camber_ys.append(airfoil_geo_data.camber_coordinates)
                break_camber_xs.append(airfoil_geo_data.x_lower_surface) 
            else:
                break_camber_ys.append(np.zeros(30))              
                break_camber_xs.append(np.linspace(0,1,30)) 
     
        else: 
        
            # find span and area. All span_break offsets should be calculated in make_VLM_wings
            if i_break == 0:
                section_span[i_break]   = 0.0
                break_x_offset[i_break] = 0.0  
                break_z_offset[i_break] = 0.0       
            else:
                section_span[i_break]   = break_spans[i_break] - break_spans[i_break-1]
                section_area[i_break]   = 0.5*(break_chord[i_break-1] + break_chord[i_break])*section_span[i_break]
                break_x_offset[i_break] = span_breaks[i_break].x_offset
                break_z_offset[i_break] = span_breaks[i_break].dih_offset
        
            # Get airfoil section VD  
            if span_breaks[i_break].airfoil: 
                if type(span_breaks[i_break].airfoil) == RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil: # check if naca 4 series of airfoil from datafile
                    airfoil_geo_data = compute_naca_4series(span_breaks[i_break].airfoil.NACA_4_Series_code,span_breaks[i_break].airfoil.number_of_points-2)
                else:
                    airfoil_geo_data = import_airfoil_geometry(span_breaks[i_break].airfoil.coordinate_file)  
                break_camber_zs.append(airfoil_geo_data.camber_coordinates)
                break_camber_xs.append(airfoil_geo_data.x_lower_surface) 
            else:
                break_camber_zs.append(np.zeros(30))              
                break_camber_xs.append(np.linspace(0,1,30)) 
        
        # Get control surface leading and trailing edge cute cuts: section__cuts[-1] should never be used in the following code
        section_LE_cut[i_break] = span_breaks[i_break].cuts[0,1]
        section_TE_cut[i_break] = span_breaks[i_break].cuts[1,1]      


    VD.wing_areas.append(np.sum(section_area[:], dtype=precision))
    if xz_sym is True :
        VD.wing_areas.append(np.sum(section_area[:], dtype=precision))
        
    # Shift spanwise vortices onto section breaks 
    if wing.vertical: 
        if len(z_coordinates) < n_breaks:
            raise ValueError('Not enough spanwise VLM stations for segment breaks') 
        z_coords_required = break_spans if (not wing.is_a_control_surface) else np.array(sorted(wing.y_coords_required))  #control surfaces have additional required y_coords  
        shifted_idxs = np.zeros(len(z_coordinates))
        for z_req in z_coords_required:
            idx = (np.abs(z_coordinates - z_req) + shifted_idxs).argmin() #index of y-coord nearest to the span break
            shifted_idxs[idx]  = np.inf 
            z_coordinates[idx] = z_req 
        z_coordinates = np.array(sorted(z_coordinates)) 
        for z_req in z_coords_required:
            if z_req not in z_coordinates:
                raise ValueError('VLM did not capture all section breaks') 

        # ---------------------------------------------------------------------------------------
        # STEP 6: Define coordinates of panels horseshoe vortices and control points 
        # --------------------------------------------------------------------------------------- 
        z_a   = z_coordinates[:-1] 
        z_b   = z_coordinates[1:]             
        del_z = z_coordinates[1:] - z_coordinates[:-1] 

        # Let relevant control surfaces know which y-coords they are required to have----------------------------------
        if not wing.is_a_control_surface:
            i_break = 0
            for idx_z in range(n_sw):
                span_break = span_breaks[i_break]
                cs_IDs     = span_break.cs_IDs[:,1] #only the outboard control surfaces
                z_coord    = z_coordinates[idx_z]
                
                for cs_ID in cs_IDs[cs_IDs >= 0]:
                    cs_tag     = wing.tag + '__cs_id_{}'.format(cs_ID)
                    cs_wing    = wings[cs_tag]
                    rel_offset = cs_wing.origin[0,2] - wing.origin[0][2]  
                    cs_wing.y_coords_required.append(z_coord - rel_offset)
                
                if z_coordinates[idx_z+1] == break_spans[i_break+1]: 
                    i_break += 1
                    
    else:
        if len(y_coordinates) < n_breaks:
            raise ValueError('Not enough spanwise VLM stations for segment breaks')

        y_coords_required = break_spans if (not wing.is_a_control_surface) else np.array(sorted(wing.y_coords_required))  #control surfaces have additional required y_coords  
        shifted_idxs = np.zeros(len(y_coordinates))
        for y_req in y_coords_required:
            idx = (np.abs(y_coordinates - y_req) + shifted_idxs).argmin() #index of y-coord nearest to the span break
            shifted_idxs[idx]  = np.inf 
            y_coordinates[idx] = y_req 
        y_coordinates = np.array(sorted(y_coordinates)) 
        for y_req in y_coords_required:
            if y_req not in y_coordinates:
                raise ValueError('VLM did not capture all section breaks')  
    
        # ---------------------------------------------------------------------------------------
        # STEP 6: Define coordinates of panels horseshoe vortices and control points 
        # --------------------------------------------------------------------------------------- 
        y_a   = y_coordinates[:-1] 
        y_b   = y_coordinates[1:]             
        del_y = y_coordinates[1:] - y_coordinates[:-1] 

        # Let relevant control surfaces know which y-coords they are required to have----------------------------------
        if not wing.is_a_control_surface:
            i_break = 0
            for idx_y in range(n_sw):
                span_break = span_breaks[i_break]
                cs_IDs     = span_break.cs_IDs[:,1] #only the outboard control surfaces
                y_coord    = y_coordinates[idx_y]
                
                for cs_ID in cs_IDs[cs_IDs >= 0]:
                    cs_tag     = wing.tag + '__cs_id_{}'.format(cs_ID)
                    cs_wing    = wings[cs_tag]
                    rel_offset = cs_wing.origin[0,1] - wing.origin[0][1]  
                    cs_wing.y_coords_required.append(y_coord - rel_offset)
                
                if y_coordinates[idx_y+1] == break_spans[i_break+1]: 
                    i_break += 1
    
    # -------------------------------------------------------------------------------------------------------------
    # Run the strip contruction loop again if wing is symmetric. 
    # Reflection plane = x-y plane for vertical wings. Otherwise, reflection plane = x-z plane 
    symmetry_mask = np.array([[0,0,0],[yz_sym,xz_sym,xy_sym]])
    signs         = np.array([1, -1])  
    side_idx = 0
    for _ in signs[[True,xz_sym]]:
        # create empty vectors for coordinates 
        xah   = np.zeros(n_cw*n_sw)
        yah   = np.zeros(n_cw*n_sw)
        zah   = np.zeros(n_cw*n_sw)
        xbh   = np.zeros(n_cw*n_sw)
        ybh   = np.zeros(n_cw*n_sw)
        zbh   = np.zeros(n_cw*n_sw)    
        xch   = np.zeros(n_cw*n_sw)
        ych   = np.zeros(n_cw*n_sw)
        zch   = np.zeros(n_cw*n_sw)    
        xa1   = np.zeros(n_cw*n_sw)
        ya1   = np.zeros(n_cw*n_sw)
        za1   = np.zeros(n_cw*n_sw)
        xa2   = np.zeros(n_cw*n_sw)
        ya2   = np.zeros(n_cw*n_sw)
        za2   = np.zeros(n_cw*n_sw)    
        xb1   = np.zeros(n_cw*n_sw)
        yb1   = np.zeros(n_cw*n_sw)
        zb1   = np.zeros(n_cw*n_sw)
        xb2   = np.zeros(n_cw*n_sw) 
        yb2   = np.zeros(n_cw*n_sw) 
        zb2   = np.zeros(n_cw*n_sw)    
        xac   = np.zeros(n_cw*n_sw)
        yac   = np.zeros(n_cw*n_sw)
        zac   = np.zeros(n_cw*n_sw)    
        xbc   = np.zeros(n_cw*n_sw)
        ybc   = np.zeros(n_cw*n_sw)
        zbc   = np.zeros(n_cw*n_sw)  
        xc    = np.zeros(n_cw*n_sw) 
        yc    = np.zeros(n_cw*n_sw) 
        zc    = np.zeros(n_cw*n_sw) 
        x     = np.zeros((n_cw+1)*(n_sw+1)) # may have to change to make space for split if control surfaces are allowed to have more than two Segments
        y     = np.zeros((n_cw+1)*(n_sw+1)) 
        z     = np.zeros((n_cw+1)*(n_sw+1))         
        cs_w  = np.zeros(n_sw)        
        
        # adjust origin for symmetry with special case for vertical symmetry
        yz_sym_sign   = 1 if symmetry_mask[side_idx,0] == 0 else -1
        xz_sym_sign   = 1 if symmetry_mask[side_idx,1] == 0 else -1
        xy_sym_sign   = 1 if symmetry_mask[side_idx,2] == 0 else -1
        wing_origin_x = wing_origin[0] * yz_sym_sign
        wing_origin_y = wing_origin[1] * xz_sym_sign
        wing_origin_z = wing_origin[2] * xy_sym_sign
            
        # ---------------------------------------------------------------------------------------------------------
        # Loop over each strip of panels in the wing
        i_break = 0           
        for idx_y in range(n_sw):
            
            if wing.vertical:
                
                
                # define basic geometric values------------------------------------------------------------------------
                # inboard, outboard, and central panel values
                eta_a = (z_a[idx_y] - break_spans[i_break])  
                eta_b = (z_b[idx_y] - break_spans[i_break]) 
                eta   = (z_b[idx_y] - del_z[idx_y]/2 - break_spans[i_break])  
                
                segment_chord_ratio = (break_chord[i_break+1] - break_chord[i_break])/section_span[i_break+1]
                segment_twist_ratio = (break_twist[i_break+1] - break_twist[i_break])/section_span[i_break+1]
                
                wing_chord_section_a  = break_chord[i_break] + (eta_a*segment_chord_ratio) 
                wing_chord_section_b  = break_chord[i_break] + (eta_b*segment_chord_ratio)
                wing_chord_section    = break_chord[i_break] + (eta*segment_chord_ratio)
                
                # x-positions based on whether the wing needs 'cuts' for its control sufaces
                nondim_x_stations = np.interp(np.linspace(0.,1.,num=n_cw+1), [0.,1.], [section_LE_cut[i_break], section_TE_cut[i_break]])
                x_stations_a      = nondim_x_stations * wing_chord_section_a  #x positions accounting for control surface cuts, relative to leading
                x_stations_b      = nondim_x_stations * wing_chord_section_b
                x_stations        = nondim_x_stations * wing_chord_section
                
                delta_x_a = (x_stations_a[-1] - x_stations_a[0])/n_cw  
                delta_x_b = (x_stations_b[-1] - x_stations_b[0])/n_cw      
                delta_x   = (x_stations[-1]   - x_stations[0]  )/n_cw             
                
                # define coordinates of horseshoe vortices and control points------------------------------------------
                xi_a1 = break_x_offset[i_break] + eta_a*np.tan(break_sweep[i_break]) + x_stations_a[:-1]                  # x coordinate of top left corner of panel
                xi_ah = break_x_offset[i_break] + eta_a*np.tan(break_sweep[i_break]) + x_stations_a[:-1] + delta_x_a*0.25 # x coordinate of left corner of panel
                xi_ac = break_x_offset[i_break] + eta_a*np.tan(break_sweep[i_break]) + x_stations_a[:-1] + delta_x_a*0.75 # x coordinate of bottom left corner of control point vortex  
                xi_a2 = break_x_offset[i_break] + eta_a*np.tan(break_sweep[i_break]) + x_stations_a[1:]                   # x coordinate of bottom left corner of bound vortex 
                xi_b1 = break_x_offset[i_break] + eta_b*np.tan(break_sweep[i_break]) + x_stations_b[:-1]                  # x coordinate of top right corner of panel      
                xi_bh = break_x_offset[i_break] + eta_b*np.tan(break_sweep[i_break]) + x_stations_b[:-1] + delta_x_b*0.25 # x coordinate of right corner of bound vortex         
                xi_bc = break_x_offset[i_break] + eta_b*np.tan(break_sweep[i_break]) + x_stations_b[:-1] + delta_x_b*0.75 # x coordinate of bottom right corner of control point vortex         
                xi_b2 = break_x_offset[i_break] + eta_b*np.tan(break_sweep[i_break]) + x_stations_b[1:]                   # x coordinate of bottom right corner of panel
                xi_ch = break_x_offset[i_break] + eta  *np.tan(break_sweep[i_break]) + x_stations[:-1]   + delta_x  *0.25 # x coordinate center of bound vortex of each panel 
                xi_c  = break_x_offset[i_break] + eta  *np.tan(break_sweep[i_break]) + x_stations[:-1]   + delta_x  *0.75 # x coordinate three-quarter chord control point for each panel
                
                #adjust for camber-------------------------------------------------------------------------------------    
                #format camber vars for wings vs control surface wings
                nondim_camber_x_coords = break_camber_xs[i_break] *1
                nondim_camber          = break_camber_ys[i_break] *1
                if wing.is_a_control_surface: #rescale so that airfoils get cut properly
                    if not wing.is_slat:
                        nondim_camber_x_coords -= 1 - wing.chord_fraction
                    nondim_camber_x_coords /= wing.chord_fraction
                    nondim_camber          /= wing.chord_fraction
                
                # adjustment of coordinates for camber
                section_camber_a  = nondim_camber*wing_chord_section_a  
                section_camber_b  = nondim_camber*wing_chord_section_b  
                section_camber_c  = nondim_camber*wing_chord_section             
                
                section_x_coord_a = nondim_camber_x_coords*wing_chord_section_a
                section_x_coord_b = nondim_camber_x_coords*wing_chord_section_b
                section_x_coord   = nondim_camber_x_coords*wing_chord_section
                
                y_c_a1 = np.interp((x_stations_a[:-1]                 ) ,section_x_coord_a, section_camber_a) 
                y_c_ah = np.interp((x_stations_a[:-1] + delta_x_a*0.25) ,section_x_coord_a, section_camber_a)
                y_c_ac = np.interp((x_stations_a[:-1] + delta_x_a*0.75) ,section_x_coord_a, section_camber_a) 
                y_c_a2 = np.interp((x_stations_a[1:]                  ) ,section_x_coord_a, section_camber_a) 
                y_c_b1 = np.interp((x_stations_b[:-1]                 ) ,section_x_coord_b, section_camber_b)   
                y_c_bh = np.interp((x_stations_b[:-1] + delta_x_b*0.25) ,section_x_coord_b, section_camber_b) 
                y_c_bc = np.interp((x_stations_b[:-1] + delta_x_b*0.75) ,section_x_coord_b, section_camber_b) 
                y_c_b2 = np.interp((x_stations_b[1:]                  ) ,section_x_coord_b, section_camber_b) 
                y_c_ch = np.interp((x_stations[:-1]   + delta_x  *0.25) ,section_x_coord  , section_camber_c) 
                y_c    = np.interp((x_stations[:-1]   + delta_x  *0.75) ,section_x_coord  , section_camber_c) 
                
                # adjust for dihedral and add to camber----------------------------------------------------------------    
                zeta_a1 = break_y_offset[i_break] + eta_a*np.tan(break_dihedral[i_break])  + y_c_a1  # y coordinate of top left corner of panel
                zeta_ah = break_y_offset[i_break] + eta_a*np.tan(break_dihedral[i_break])  + y_c_ah  # y coordinate of left corner of bound vortex  
                zeta_a2 = break_y_offset[i_break] + eta_a*np.tan(break_dihedral[i_break])  + y_c_a2  # y coordinate of bottom left corner of panel
                zeta_ac = break_y_offset[i_break] + eta_a*np.tan(break_dihedral[i_break])  + y_c_ac  # y coordinate of bottom left corner of panel of control point
                zeta_bc = break_y_offset[i_break] + eta_b*np.tan(break_dihedral[i_break])  + y_c_bc  # y coordinate of top right corner of panel of control point                          
                zeta_b1 = break_y_offset[i_break] + eta_b*np.tan(break_dihedral[i_break])  + y_c_b1  # y coordinate of top right corner of panel  
                zeta_bh = break_y_offset[i_break] + eta_b*np.tan(break_dihedral[i_break])  + y_c_bh  # y coordinate of right corner of bound vortex        
                zeta_b2 = break_y_offset[i_break] + eta_b*np.tan(break_dihedral[i_break])  + y_c_b2  # y coordinate of bottom right corner of panel                 
                zeta_ch = break_y_offset[i_break] + eta  *np.tan(break_dihedral[i_break])  + y_c_ch  # y coordinate center of bound vortex on each panel
                zeta    = break_y_offset[i_break] + eta  *np.tan(break_dihedral[i_break])  + y_c     # y coordinate three-quarter chord control point for each panel
                
                # adjust for twist-------------------------------------------------------------------------------------
                # pivot point is the leading edge before camber  
                pivot_x_a = break_x_offset[i_break] + eta_a*np.tan(break_sweep[i_break])             # x location of leading edge left corner of wing
                pivot_x_b = break_x_offset[i_break] + eta_b*np.tan(break_sweep[i_break])             # x location of leading edge right of wing
                pivot_x   = break_x_offset[i_break] + eta  *np.tan(break_sweep[i_break])             # x location of leading edge center of wing
                
                pivot_y_a = break_y_offset[i_break] + eta_a*np.tan(break_dihedral[i_break])          # z location of leading edge left corner of wing
                pivot_y_b = break_y_offset[i_break] + eta_b*np.tan(break_dihedral[i_break])          # z location of leading edge right of wing
                pivot_z   = break_y_offset[i_break] + eta  *np.tan(break_dihedral[i_break])          # z location of leading edge center of wing
                
                # adjust twist pivot line for control surface wings: offset leading edge to match that of the owning wing            
                if wing.is_a_control_surface and not wing.is_slat: #correction only leading for non-leading edge control surfaces since the LE is the pivot by default
                    nondim_cs_LE = (1 - wing.chord_fraction)
                    pivot_x_a   -= nondim_cs_LE *(wing_chord_section_a /wing.chord_fraction) 
                    pivot_x_b   -= nondim_cs_LE *(wing_chord_section_b /wing.chord_fraction) 
                    pivot_x     -= nondim_cs_LE *(wing_chord_section   /wing.chord_fraction) 
                
                # adjust coordinates for twist
                section_twist_a = break_twist[i_break] + (eta_a * segment_twist_ratio)               # twist at left side of panel
                section_twist_b = break_twist[i_break] + (eta_b * segment_twist_ratio)               # twist at right side of panel
                section_twist   = break_twist[i_break] + (eta   * segment_twist_ratio)               # twist at center local chord 
                
                xi_prime_a1    = pivot_x_a + np.cos(section_twist_a)*(xi_a1-pivot_x_a) + np.sin(section_twist_a)*(zeta_a1-pivot_y_a) # x coordinate transformation of top left corner
                xi_prime_ah    = pivot_x_a + np.cos(section_twist_a)*(xi_ah-pivot_x_a) + np.sin(section_twist_a)*(zeta_ah-pivot_y_a) # x coordinate transformation of bottom left corner
                xi_prime_ac    = pivot_x_a + np.cos(section_twist_a)*(xi_ac-pivot_x_a) + np.sin(section_twist_a)*(zeta_a2-pivot_y_a) # x coordinate transformation of bottom left corner of control point
                xi_prime_a2    = pivot_x_a + np.cos(section_twist_a)*(xi_a2-pivot_x_a) + np.sin(section_twist_a)*(zeta_a2-pivot_y_a) # x coordinate transformation of bottom left corner
                xi_prime_b1    = pivot_x_b + np.cos(section_twist_b)*(xi_b1-pivot_x_b) + np.sin(section_twist_b)*(zeta_b1-pivot_y_b) # x coordinate transformation of top right corner 
                xi_prime_bh    = pivot_x_b + np.cos(section_twist_b)*(xi_bh-pivot_x_b) + np.sin(section_twist_b)*(zeta_bh-pivot_y_b) # x coordinate transformation of top right corner 
                xi_prime_bc    = pivot_x_b + np.cos(section_twist_b)*(xi_bc-pivot_x_b) + np.sin(section_twist_b)*(zeta_b1-pivot_y_b) # x coordinate transformation of top right corner of control point                         
                xi_prime_b2    = pivot_x_b + np.cos(section_twist_b)*(xi_b2-pivot_x_b) + np.sin(section_twist_b)*(zeta_b2-pivot_y_b) # x coordinate transformation of botton right corner 
                xi_prime_ch    = pivot_x   + np.cos(section_twist)  *(xi_ch-pivot_x)   + np.sin(section_twist)  *(zeta_ch-pivot_z)   # x coordinate transformation of center of horeshoe vortex 
                xi_prime       = pivot_x   + np.cos(section_twist)  *(xi_c -pivot_x)   + np.sin(section_twist)  *(zeta   -pivot_z)   # x coordinate transformation of control point
                
                zeta_prime_a1  = pivot_y_a - np.sin(section_twist_a)*(xi_a1-pivot_x_a) + np.cos(section_twist_a)*(zeta_a1-pivot_y_a) # y coordinate transformation of top left corner
                zeta_prime_ah  = pivot_y_a - np.sin(section_twist_a)*(xi_ah-pivot_x_a) + np.cos(section_twist_a)*(zeta_ah-pivot_y_a) # y coordinate transformation of bottom left corner
                zeta_prime_ac  = pivot_y_a - np.sin(section_twist_a)*(xi_ac-pivot_x_a) + np.cos(section_twist_a)*(zeta_ac-pivot_y_a) # y coordinate transformation of bottom left corner
                zeta_prime_a2  = pivot_y_a - np.sin(section_twist_a)*(xi_a2-pivot_x_a) + np.cos(section_twist_a)*(zeta_a2-pivot_y_a) # y coordinate transformation of bottom left corner
                zeta_prime_b1  = pivot_y_b - np.sin(section_twist_b)*(xi_b1-pivot_x_b) + np.cos(section_twist_b)*(zeta_b1-pivot_y_b) # y coordinate transformation of top right corner 
                zeta_prime_bh  = pivot_y_b - np.sin(section_twist_b)*(xi_bh-pivot_x_b) + np.cos(section_twist_b)*(zeta_bh-pivot_y_b) # y coordinate transformation of top right corner 
                zeta_prime_bc  = pivot_y_b - np.sin(section_twist_b)*(xi_bc-pivot_x_b) + np.cos(section_twist_b)*(zeta_bc-pivot_y_b) # y coordinate transformation of top right corner                         
                zeta_prime_b2  = pivot_y_b - np.sin(section_twist_b)*(xi_b2-pivot_x_b) + np.cos(section_twist_b)*(zeta_b2-pivot_y_b) # y coordinate transformation of botton right corner 
                zeta_prime_ch  = pivot_z   - np.sin(section_twist)  *(xi_ch-pivot_x)   + np.cos(-section_twist) *(zeta_ch-pivot_z)   # y coordinate transformation of center of horseshoe
                zeta_prime     = pivot_z   - np.sin(section_twist)  *(xi_c -pivot_x)   + np.cos(-section_twist) *(zeta   -pivot_z)   # y coordinate transformation of control point
                
                # Define z-coordinate and other arrays-----------------------------------------------------------------
                # take normal value for first wing, then reflect over xz plane for a symmetric wing
                z_prime_as = (np.ones(n_cw+1)*z_a[idx_y]                 ) *1          
                z_prime_a1 = (z_prime_as[:-1]                            ) *1       
                z_prime_ah = (z_prime_as[:-1]                            ) *1       
                z_prime_ac = (z_prime_as[:-1]                            ) *1          
                z_prime_a2 = (z_prime_as[:-1]                            ) *1        
                z_prime_bs = (np.ones(n_cw+1)*z_b[idx_y]                 ) *1
                z_prime_b1 = (z_prime_bs[:-1]                            ) *1         
                z_prime_bh = (z_prime_bs[:-1]                            ) *1         
                z_prime_bc = (z_prime_bs[:-1]                            ) *1         
                z_prime_b2 = (z_prime_bs[:-1]                            ) *1   
                z_prime_ch = (np.ones(n_cw)*(z_b[idx_y] - del_z[idx_y]/2)) *1
                z_prime    = (z_prime_ch                                 ) *1    
                
                # populate all corners of all panels. Right side only populated for last strip wing the wing
                xi_prime_as   = np.concatenate([xi_prime_a1,  np.array([xi_prime_a2  [-1]])])*1
                xi_prime_bs   = np.concatenate([xi_prime_b1,  np.array([xi_prime_b2  [-1]])])*1
                zeta_prime_as = np.concatenate([zeta_prime_a1,np.array([zeta_prime_a2[-1]])])*1            
                zeta_prime_bs = np.concatenate([zeta_prime_b1,np.array([zeta_prime_b2[-1]])])*1  
                 
                wing.inverted_wing = -np.sign(break_dihedral[i_break] - np.pi/2)
                
                # store coordinates of panels, horseshoeces vortices and control points relative to wing root----------
                xa1[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_a1     # top left corner of panel
                ya1[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_a1*xz_sym_sign    
                za1[idx_y*n_cw:(idx_y+1)*n_cw] = z_prime_a1
                
                xah[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_ah     # left coord of horseshoe
                yah[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_ah*xz_sym_sign  
                zah[idx_y*n_cw:(idx_y+1)*n_cw] = z_prime_ah
                
                xac[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_ac     # left coord of control point
                yac[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_ac*xz_sym_sign  
                zac[idx_y*n_cw:(idx_y+1)*n_cw] = z_prime_ac
                
                xa2[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_a2     # bottom left corner of panel
                ya2[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_a2*xz_sym_sign  
                za2[idx_y*n_cw:(idx_y+1)*n_cw] = z_prime_a2
            
                xb1[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_b1     # top right corner of panel
                yb1[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_b1*xz_sym_sign            
                zb1[idx_y*n_cw:(idx_y+1)*n_cw] = z_prime_b1
                
                xbh[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_bh     # right coord of horseshoe
                ybh[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_bh*xz_sym_sign            
                zbh[idx_y*n_cw:(idx_y+1)*n_cw] = z_prime_bh
                
                xbc[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_bc     # right coord of control point
                ybc[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_bc*xz_sym_sign                             
                zbc[idx_y*n_cw:(idx_y+1)*n_cw] = z_prime_bc
                
                xb2[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_b2     # bottom right corner of panel
                yb2[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_b2*xz_sym_sign                          
                zb2[idx_y*n_cw:(idx_y+1)*n_cw] = z_prime_b2 
            
                xch[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_ch     # center coord of horseshoe
                ych[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_ch*xz_sym_sign                                
                zch[idx_y*n_cw:(idx_y+1)*n_cw] = z_prime_ch
                
                xc [idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime        # center (true) coord of control point
                yc [idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime*xz_sym_sign  
                zc [idx_y*n_cw:(idx_y+1)*n_cw] = z_prime 
            
                x[idx_y*(n_cw+1):(idx_y+1)*(n_cw+1)] = xi_prime_as                      # x, y, z represent all all points of the corners of the panels, LE and TE inclusive
                y[idx_y*(n_cw+1):(idx_y+1)*(n_cw+1)] = zeta_prime_as*xz_sym_sign        # the final right corners get appended at last strip in wing, later
                z[idx_y*(n_cw+1):(idx_y+1)*(n_cw+1)] = z_prime_as       
                
            else:
                # define basic geometric values------------------------------------------------------------------------
                # inboard, outboard, and central panel values
                eta_a = (y_a[idx_y] - break_spans[i_break])  
                eta_b = (y_b[idx_y] - break_spans[i_break]) 
                eta   = (y_b[idx_y] - del_y[idx_y]/2 - break_spans[i_break])  
        
                segment_chord_ratio = (break_chord[i_break+1] - break_chord[i_break])/section_span[i_break+1]
                segment_twist_ratio = (break_twist[i_break+1] - break_twist[i_break])/section_span[i_break+1]
        
                wing_chord_section_a  = break_chord[i_break] + (eta_a*segment_chord_ratio) 
                wing_chord_section_b  = break_chord[i_break] + (eta_b*segment_chord_ratio)
                wing_chord_section    = break_chord[i_break] + (eta*segment_chord_ratio)
        
                # x-positions based on whether the wing needs 'cuts' for its control sufaces
                nondim_x_stations = np.interp(np.linspace(0.,1.,num=n_cw+1), [0.,1.], [section_LE_cut[i_break], section_TE_cut[i_break]])
                x_stations_a      = nondim_x_stations * wing_chord_section_a  #x positions accounting for control surface cuts, relative to leading
                x_stations_b      = nondim_x_stations * wing_chord_section_b
                x_stations        = nondim_x_stations * wing_chord_section
                
                delta_x_a = (x_stations_a[-1] - x_stations_a[0])/n_cw  
                delta_x_b = (x_stations_b[-1] - x_stations_b[0])/n_cw      
                delta_x   = (x_stations[-1]   - x_stations[0]  )/n_cw             
        
                # define coordinates of horseshoe vortices and control points------------------------------------------
                xi_a1 = break_x_offset[i_break] + eta_a*np.tan(break_sweep[i_break]) + x_stations_a[:-1]                  # x coordinate of top left corner of panel
                xi_ah = break_x_offset[i_break] + eta_a*np.tan(break_sweep[i_break]) + x_stations_a[:-1] + delta_x_a*0.25 # x coordinate of left corner of panel
                xi_ac = break_x_offset[i_break] + eta_a*np.tan(break_sweep[i_break]) + x_stations_a[:-1] + delta_x_a*0.75 # x coordinate of bottom left corner of control point vortex  
                xi_a2 = break_x_offset[i_break] + eta_a*np.tan(break_sweep[i_break]) + x_stations_a[1:]                   # x coordinate of bottom left corner of bound vortex 
                xi_b1 = break_x_offset[i_break] + eta_b*np.tan(break_sweep[i_break]) + x_stations_b[:-1]                  # x coordinate of top right corner of panel      
                xi_bh = break_x_offset[i_break] + eta_b*np.tan(break_sweep[i_break]) + x_stations_b[:-1] + delta_x_b*0.25 # x coordinate of right corner of bound vortex         
                xi_bc = break_x_offset[i_break] + eta_b*np.tan(break_sweep[i_break]) + x_stations_b[:-1] + delta_x_b*0.75 # x coordinate of bottom right corner of control point vortex         
                xi_b2 = break_x_offset[i_break] + eta_b*np.tan(break_sweep[i_break]) + x_stations_b[1:]                   # x coordinate of bottom right corner of panel
                xi_ch = break_x_offset[i_break] + eta  *np.tan(break_sweep[i_break]) + x_stations[:-1]   + delta_x  *0.25 # x coordinate center of bound vortex of each panel 
                xi_c  = break_x_offset[i_break] + eta  *np.tan(break_sweep[i_break]) + x_stations[:-1]   + delta_x  *0.75 # x coordinate three-quarter chord control point for each panel
        
                #adjust for camber-------------------------------------------------------------------------------------    
                #format camber vars for wings vs control surface wings
                nondim_camber_x_coords = break_camber_xs[i_break] *1
                nondim_camber          = break_camber_zs[i_break] *1
                if wing.is_a_control_surface: #rescale so that airfoils get cut properly
                    if not wing.is_slat:
                        nondim_camber_x_coords -= 1 - wing.chord_fraction
                    nondim_camber_x_coords /= wing.chord_fraction
                    nondim_camber          /= wing.chord_fraction
        
                # adjustment of coordinates for camber
                section_camber_a  = nondim_camber*wing_chord_section_a  
                section_camber_b  = nondim_camber*wing_chord_section_b  
                section_camber_c  = nondim_camber*wing_chord_section             
                
                section_x_coord_a = nondim_camber_x_coords*wing_chord_section_a
                section_x_coord_b = nondim_camber_x_coords*wing_chord_section_b
                section_x_coord   = nondim_camber_x_coords*wing_chord_section
        
                z_c_a1 = np.interp((x_stations_a[:-1]                 ) ,section_x_coord_a, section_camber_a) 
                z_c_ah = np.interp((x_stations_a[:-1] + delta_x_a*0.25) ,section_x_coord_a, section_camber_a)
                z_c_ac = np.interp((x_stations_a[:-1] + delta_x_a*0.75) ,section_x_coord_a, section_camber_a) 
                z_c_a2 = np.interp((x_stations_a[1:]                  ) ,section_x_coord_a, section_camber_a) 
                z_c_b1 = np.interp((x_stations_b[:-1]                 ) ,section_x_coord_b, section_camber_b)   
                z_c_bh = np.interp((x_stations_b[:-1] + delta_x_b*0.25) ,section_x_coord_b, section_camber_b) 
                z_c_bc = np.interp((x_stations_b[:-1] + delta_x_b*0.75) ,section_x_coord_b, section_camber_b) 
                z_c_b2 = np.interp((x_stations_b[1:]                  ) ,section_x_coord_b, section_camber_b) 
                z_c_ch = np.interp((x_stations[:-1]   + delta_x  *0.25) ,section_x_coord  , section_camber_c) 
                z_c    = np.interp((x_stations[:-1]   + delta_x  *0.75) ,section_x_coord  , section_camber_c) 
        
                # adjust for dihedral and add to camber----------------------------------------------------------------    
                zeta_a1 = break_z_offset[i_break] + eta_a*np.tan(break_dihedral[i_break])  + z_c_a1  # z coordinate of top left corner of panel
                zeta_ah = break_z_offset[i_break] + eta_a*np.tan(break_dihedral[i_break])  + z_c_ah  # z coordinate of left corner of bound vortex  
                zeta_a2 = break_z_offset[i_break] + eta_a*np.tan(break_dihedral[i_break])  + z_c_a2  # z coordinate of bottom left corner of panel
                zeta_ac = break_z_offset[i_break] + eta_a*np.tan(break_dihedral[i_break])  + z_c_ac  # z coordinate of bottom left corner of panel of control point
                zeta_bc = break_z_offset[i_break] + eta_b*np.tan(break_dihedral[i_break])  + z_c_bc  # z coordinate of top right corner of panel of control point                          
                zeta_b1 = break_z_offset[i_break] + eta_b*np.tan(break_dihedral[i_break])  + z_c_b1  # z coordinate of top right corner of panel  
                zeta_bh = break_z_offset[i_break] + eta_b*np.tan(break_dihedral[i_break])  + z_c_bh  # z coordinate of right corner of bound vortex        
                zeta_b2 = break_z_offset[i_break] + eta_b*np.tan(break_dihedral[i_break])  + z_c_b2  # z coordinate of bottom right corner of panel                 
                zeta_ch = break_z_offset[i_break] + eta  *np.tan(break_dihedral[i_break])  + z_c_ch  # z coordinate center of bound vortex on each panel
                zeta    = break_z_offset[i_break] + eta  *np.tan(break_dihedral[i_break])  + z_c     # z coordinate three-quarter chord control point for each panel
        
                # adjust for twist-------------------------------------------------------------------------------------
                # pivot point is the leading edge before camber  
                pivot_x_a = break_x_offset[i_break] + eta_a*np.tan(break_sweep[i_break])             # x location of leading edge left corner of wing
                pivot_x_b = break_x_offset[i_break] + eta_b*np.tan(break_sweep[i_break])             # x location of leading edge right of wing
                pivot_x   = break_x_offset[i_break] + eta  *np.tan(break_sweep[i_break])             # x location of leading edge center of wing
                
                pivot_z_a = break_z_offset[i_break] + eta_a*np.tan(break_dihedral[i_break])          # z location of leading edge left corner of wing
                pivot_z_b = break_z_offset[i_break] + eta_b*np.tan(break_dihedral[i_break])          # z location of leading edge right of wing
                pivot_z   = break_z_offset[i_break] + eta  *np.tan(break_dihedral[i_break])          # z location of leading edge center of wing
        
                # adjust twist pivot line for control surface wings: offset leading edge to match that of the owning wing            
                if wing.is_a_control_surface and not wing.is_slat: #correction only leading for non-leading edge control surfaces since the LE is the pivot by default
                    nondim_cs_LE = (1 - wing.chord_fraction)
                    pivot_x_a   -= nondim_cs_LE *(wing_chord_section_a /wing.chord_fraction) 
                    pivot_x_b   -= nondim_cs_LE *(wing_chord_section_b /wing.chord_fraction) 
                    pivot_x     -= nondim_cs_LE *(wing_chord_section   /wing.chord_fraction) 
        
                # adjust coordinates for twist
                section_twist_a = break_twist[i_break] + (eta_a * segment_twist_ratio)               # twist at left side of panel
                section_twist_b = break_twist[i_break] + (eta_b * segment_twist_ratio)               # twist at right side of panel
                section_twist   = break_twist[i_break] + (eta   * segment_twist_ratio)               # twist at center local chord 
        
                xi_prime_a1    = pivot_x_a + np.cos(section_twist_a)*(xi_a1-pivot_x_a) + np.sin(section_twist_a)*(zeta_a1-pivot_z_a) # x coordinate transformation of top left corner
                xi_prime_ah    = pivot_x_a + np.cos(section_twist_a)*(xi_ah-pivot_x_a) + np.sin(section_twist_a)*(zeta_ah-pivot_z_a) # x coordinate transformation of bottom left corner
                xi_prime_ac    = pivot_x_a + np.cos(section_twist_a)*(xi_ac-pivot_x_a) + np.sin(section_twist_a)*(zeta_a2-pivot_z_a) # x coordinate transformation of bottom left corner of control point
                xi_prime_a2    = pivot_x_a + np.cos(section_twist_a)*(xi_a2-pivot_x_a) + np.sin(section_twist_a)*(zeta_a2-pivot_z_a) # x coordinate transformation of bottom left corner
                xi_prime_b1    = pivot_x_b + np.cos(section_twist_b)*(xi_b1-pivot_x_b) + np.sin(section_twist_b)*(zeta_b1-pivot_z_b) # x coordinate transformation of top right corner 
                xi_prime_bh    = pivot_x_b + np.cos(section_twist_b)*(xi_bh-pivot_x_b) + np.sin(section_twist_b)*(zeta_bh-pivot_z_b) # x coordinate transformation of top right corner 
                xi_prime_bc    = pivot_x_b + np.cos(section_twist_b)*(xi_bc-pivot_x_b) + np.sin(section_twist_b)*(zeta_b1-pivot_z_b) # x coordinate transformation of top right corner of control point                         
                xi_prime_b2    = pivot_x_b + np.cos(section_twist_b)*(xi_b2-pivot_x_b) + np.sin(section_twist_b)*(zeta_b2-pivot_z_b) # x coordinate transformation of botton right corner 
                xi_prime_ch    = pivot_x   + np.cos(section_twist)  *(xi_ch-pivot_x)   + np.sin(section_twist)  *(zeta_ch-pivot_z)   # x coordinate transformation of center of horeshoe vortex 
                xi_prime       = pivot_x   + np.cos(section_twist)  *(xi_c -pivot_x)   + np.sin(section_twist)  *(zeta   -pivot_z)   # x coordinate transformation of control point
        
                zeta_prime_a1  = pivot_z_a - np.sin(section_twist_a)*(xi_a1-pivot_x_a) + np.cos(section_twist_a)*(zeta_a1-pivot_z_a) # z coordinate transformation of top left corner
                zeta_prime_ah  = pivot_z_a - np.sin(section_twist_a)*(xi_ah-pivot_x_a) + np.cos(section_twist_a)*(zeta_ah-pivot_z_a) # z coordinate transformation of bottom left corner
                zeta_prime_ac  = pivot_z_a - np.sin(section_twist_a)*(xi_ac-pivot_x_a) + np.cos(section_twist_a)*(zeta_ac-pivot_z_a) # z coordinate transformation of bottom left corner
                zeta_prime_a2  = pivot_z_a - np.sin(section_twist_a)*(xi_a2-pivot_x_a) + np.cos(section_twist_a)*(zeta_a2-pivot_z_a) # z coordinate transformation of bottom left corner
                zeta_prime_b1  = pivot_z_b - np.sin(section_twist_b)*(xi_b1-pivot_x_b) + np.cos(section_twist_b)*(zeta_b1-pivot_z_b) # z coordinate transformation of top right corner 
                zeta_prime_bh  = pivot_z_b - np.sin(section_twist_b)*(xi_bh-pivot_x_b) + np.cos(section_twist_b)*(zeta_bh-pivot_z_b) # z coordinate transformation of top right corner 
                zeta_prime_bc  = pivot_z_b - np.sin(section_twist_b)*(xi_bc-pivot_x_b) + np.cos(section_twist_b)*(zeta_bc-pivot_z_b) # z coordinate transformation of top right corner                         
                zeta_prime_b2  = pivot_z_b - np.sin(section_twist_b)*(xi_b2-pivot_x_b) + np.cos(section_twist_b)*(zeta_b2-pivot_z_b) # z coordinate transformation of botton right corner 
                zeta_prime_ch  = pivot_z   - np.sin(section_twist)  *(xi_ch-pivot_x)   + np.cos(-section_twist) *(zeta_ch-pivot_z)   # z coordinate transformation of center of horseshoe
                zeta_prime     = pivot_z   - np.sin(section_twist)  *(xi_c -pivot_x)   + np.cos(-section_twist) *(zeta   -pivot_z)   # z coordinate transformation of control point
                
                # Define y-coordinate and other arrays-----------------------------------------------------------------
                # take normal value for first wing, then reflect over xz plane for a symmetric wing
                y_prime_as = (np.ones(n_cw+1)*y_a[idx_y]                 ) *xz_sym_sign          
                y_prime_a1 = (y_prime_as[:-1]                            ) *1       
                y_prime_ah = (y_prime_as[:-1]                            ) *1       
                y_prime_ac = (y_prime_as[:-1]                            ) *1          
                y_prime_a2 = (y_prime_as[:-1]                            ) *1        
                y_prime_bs = (np.ones(n_cw+1)*y_b[idx_y]                 ) *xz_sym_sign            
                y_prime_b1 = (y_prime_bs[:-1]                            ) *1         
                y_prime_bh = (y_prime_bs[:-1]                            ) *1         
                y_prime_bc = (y_prime_bs[:-1]                            ) *1         
                y_prime_b2 = (y_prime_bs[:-1]                            ) *1   
                y_prime_ch = (np.ones(n_cw)*(y_b[idx_y] - del_y[idx_y]/2)) *xz_sym_sign
                y_prime    = (y_prime_ch                                 ) *1    
                
                # populate all corners of all panels. Right side only populated for last strip wing the wing
                xi_prime_as   = np.concatenate([xi_prime_a1,  np.array([xi_prime_a2  [-1]])])*1
                xi_prime_bs   = np.concatenate([xi_prime_b1,  np.array([xi_prime_b2  [-1]])])*1
                zeta_prime_as = np.concatenate([zeta_prime_a1,np.array([zeta_prime_a2[-1]])])*1            
                zeta_prime_bs = np.concatenate([zeta_prime_b1,np.array([zeta_prime_b2[-1]])])*1  
                 
                wing.inverted_wing = -np.sign(break_dihedral[i_break] - np.pi/2)  
                 
                # store coordinates of panels, horseshoeces vortices and control points relative to wing root----------
                xa1[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_a1     # top left corner of panel
                ya1[idx_y*n_cw:(idx_y+1)*n_cw] = y_prime_a1
                za1[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_a1
                xah[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_ah     # left coord of horseshoe
                yah[idx_y*n_cw:(idx_y+1)*n_cw] = y_prime_ah
                zah[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_ah                    
                xac[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_ac     # left coord of control point
                yac[idx_y*n_cw:(idx_y+1)*n_cw] = y_prime_ac
                zac[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_ac
                xa2[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_a2     # bottom left corner of panel
                ya2[idx_y*n_cw:(idx_y+1)*n_cw] = y_prime_a2
                za2[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_a2
                                                 
                xb1[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_b1     # top right corner of panel
                yb1[idx_y*n_cw:(idx_y+1)*n_cw] = y_prime_b1          
                zb1[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_b1   
                xbh[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_bh     # right coord of horseshoe
                ybh[idx_y*n_cw:(idx_y+1)*n_cw] = y_prime_bh          
                zbh[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_bh                    
                xbc[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_bc     # right coord of control point
                ybc[idx_y*n_cw:(idx_y+1)*n_cw] = y_prime_bc                           
                zbc[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_bc   
                xb2[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_b2     # bottom right corner of panel
                yb2[idx_y*n_cw:(idx_y+1)*n_cw] = y_prime_b2                        
                zb2[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_b2 
                                                 
                xch[idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime_ch     # center coord of horseshoe
                ych[idx_y*n_cw:(idx_y+1)*n_cw] = y_prime_ch                              
                zch[idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime_ch
                xc [idx_y*n_cw:(idx_y+1)*n_cw] = xi_prime        # center (true) coord of control point
                yc [idx_y*n_cw:(idx_y+1)*n_cw] = y_prime
                zc [idx_y*n_cw:(idx_y+1)*n_cw] = zeta_prime 
               
                x[idx_y*(n_cw+1):(idx_y+1)*(n_cw+1)] = xi_prime_as     # x, y, z represent all all points of the corners of the panels, LE and TE inclusive
                y[idx_y*(n_cw+1):(idx_y+1)*(n_cw+1)] = y_prime_as      # the final right corners get appended at last strip in wing, later
                z[idx_y*(n_cw+1):(idx_y+1)*(n_cw+1)] = zeta_prime_as              

            cs_w[idx_y] = wing_chord_section       
                   
            # store this strip's discretization information--------------------------------------------------------
            LE_inds        = np.full(n_cw, False)
            TE_inds        = np.full(n_cw, False)
            LE_inds[0]     = True
            TE_inds[-1]    = True
            
            RNMAX          = np.ones(n_cw, np.int16)*n_cw
            panel_numbers  = np.linspace(1,n_cw,n_cw, dtype=np.int16)           
                        
            is_a_slat                  = wing.is_a_control_surface and wing.is_slat
            strip_has_no_slat          = (not wing.is_a_control_surface) and (span_breaks[i_break].cs_IDs[0,1] == -1) # wing's le, outboard control surface ID
            exposed_leading_edge_flag  = np.int16(1) if is_a_slat or strip_has_no_slat else np.int16(0)   
            
            VD.leading_edge_indices      = np.append(VD.leading_edge_indices     , LE_inds                  ) 
            VD.trailing_edge_indices     = np.append(VD.trailing_edge_indices    , TE_inds                  )            
            VD.panels_per_strip          = np.append(VD.panels_per_strip         , RNMAX                    )
            VD.chordwise_panel_number    = np.append(VD.chordwise_panel_number   , panel_numbers            )  
            VD.exposed_leading_edge_flag = np.append(VD.exposed_leading_edge_flag, exposed_leading_edge_flag)
            
            #increment i_break if needed; check for end of wing----------------------------------------------------
            if wing.vertical:
                if z_b[idx_y] == break_spans[i_break+1]: 
                    i_break += 1 
            else:
                if y_b[idx_y] == break_spans[i_break+1]: 
                    i_break += 1
                
                
        #End 'for each strip' loop    
        
        # store outboardmost edge
        x[-(n_cw+1):] = xi_prime_bs

   
        if wing.vertical:
            y[-(n_cw+1):] = zeta_prime_bs
            z[-(n_cw+1):] = z_prime_bs  
        else: 
            y[-(n_cw+1):] = y_prime_bs
            z[-(n_cw+1):] = zeta_prime_bs              
        
        # adjusting coordinate axis so reference point is at the nose of the aircraft------------------------------
        xah = xah + wing_origin_x # x coordinate of left corner of bound vortex 
        yah = yah + wing_origin_y # y coordinate of left corner of bound vortex 
        zah = zah + wing_origin_z # z coordinate of left corner of bound vortex 
        xbh = xbh + wing_origin_x # x coordinate of right corner of bound vortex 
        ybh = ybh + wing_origin_y # y coordinate of right corner of bound vortex 
        zbh = zbh + wing_origin_z # z coordinate of right corner of bound vortex 
        xch = xch + wing_origin_x # x coordinate of center of bound vortex on panel
        ych = ych + wing_origin_y # y coordinate of center of bound vortex on panel
        zch = zch + wing_origin_z # z coordinate of center of bound vortex on panel  
    
        xa1 = xa1 + wing_origin_x # x coordinate of top left corner of panel
        ya1 = ya1 + wing_origin_y # y coordinate of bottom left corner of panel
        za1 = za1 + wing_origin_z # z coordinate of top left corner of panel
        xa2 = xa2 + wing_origin_x # x coordinate of bottom left corner of panel
        ya2 = ya2 + wing_origin_y # x coordinate of bottom left corner of panel
        za2 = za2 + wing_origin_z # z coordinate of bottom left corner of panel  
    
        xb1 = xb1 + wing_origin_x # x coordinate of top right corner of panel  
        yb1 = yb1 + wing_origin_y # y coordinate of top right corner of panel 
        zb1 = zb1 + wing_origin_z # z coordinate of top right corner of panel 
        xb2 = xb2 + wing_origin_x # x coordinate of bottom rightcorner of panel 
        yb2 = yb2 + wing_origin_y # y coordinate of bottom rightcorner of panel 
        zb2 = zb2 + wing_origin_z # z coordinate of bottom right corner of panel                   
    
        xac = xac + wing_origin_x  # x coordinate of control points on panel
        yac = yac + wing_origin_y  # y coordinate of control points on panel
        zac = zac + wing_origin_z  # z coordinate of control points on panel
        xbc = xbc + wing_origin_x  # x coordinate of control points on panel
        ybc = ybc + wing_origin_y  # y coordinate of control points on panel
        zbc = zbc + wing_origin_z  # z coordinate of control points on panel
    
        xc  = xc  + wing_origin_x  # x coordinate of control points on panel
        yc  = yc  + wing_origin_y  # y coordinate of control points on panel
        zc  = zc  + wing_origin_z  # y coordinate of control points on panel
        x   = x   + wing_origin_x  # x coordinate of control points on panel
        y   = y   + wing_origin_y  # y coordinate of control points on panel
        z   = z   + wing_origin_z  # y coordinate of control points on panel
        
        # VD discretization information----------------------------------------------------------------------------
        
        # increment number of wings and panels
        n_panels = len(xch)
        VD.n_w  += 1             
        VD.n_cp += n_panels 
        
        # store this wing's discretization information  
        first_panel_ind  = VD.XAH.size
        first_strip_ind  = VD.chordwise_breaks.size
        chordwise_breaks = first_panel_ind + np.arange(n_panels)[0::n_cw]
        ID               = VD.counter*1
        
        VD.chordwise_breaks = np.append(VD.chordwise_breaks, np.int32(chordwise_breaks))
        VD.spanwise_breaks  = np.append(VD.spanwise_breaks , np.int32(first_strip_ind ))            
        VD.n_sw             = np.append(VD.n_sw            , np.int16(n_sw)            )
        VD.n_cw             = np.append(VD.n_cw            , np.int16(n_cw)            )
        VD.surface_ID       = np.append(VD.surface_ID      , np.ones(n_cw*n_sw)*ID*xz_sym_sign) # Update me when the loop is gone
        VD.surface_ID_full  = np.append(VD.surface_ID_full , np.ones((n_cw+1)*(n_sw+1))*ID*xz_sym_sign) # Update me when the loop is gone    
                
        # ---------------------------------------------------------------------------------------
        # STEP 7: Store wing in vehicle vector
        # --------------------------------------------------------------------------------------- 
        VD.XAH    = np.append(VD.XAH  , np.array(xah  , dtype=precision))
        VD.YAH    = np.append(VD.YAH  , np.array(yah  , dtype=precision))
        VD.ZAH    = np.append(VD.ZAH  , np.array(zah  , dtype=precision))
        VD.XBH    = np.append(VD.XBH  , np.array(xbh  , dtype=precision))
        VD.YBH    = np.append(VD.YBH  , np.array(ybh  , dtype=precision))
        VD.ZBH    = np.append(VD.ZBH  , np.array(zbh  , dtype=precision))
        VD.XCH    = np.append(VD.XCH  , np.array(xch  , dtype=precision))
        VD.YCH    = np.append(VD.YCH  , np.array(ych  , dtype=precision))
        VD.ZCH    = np.append(VD.ZCH  , np.array(zch  , dtype=precision))            
        VD.XA1    = np.append(VD.XA1  , np.array(xa1  , dtype=precision))
        VD.YA1    = np.append(VD.YA1  , np.array(ya1  , dtype=precision))
        VD.ZA1    = np.append(VD.ZA1  , np.array(za1  , dtype=precision))
        VD.XA2    = np.append(VD.XA2  , np.array(xa2  , dtype=precision))
        VD.YA2    = np.append(VD.YA2  , np.array(ya2  , dtype=precision))
        VD.ZA2    = np.append(VD.ZA2  , np.array(za2  , dtype=precision))        
        VD.XB1    = np.append(VD.XB1  , np.array(xb1  , dtype=precision))
        VD.YB1    = np.append(VD.YB1  , np.array(yb1  , dtype=precision))
        VD.ZB1    = np.append(VD.ZB1  , np.array(zb1  , dtype=precision))
        VD.XB2    = np.append(VD.XB2  , np.array(xb2  , dtype=precision))                
        VD.YB2    = np.append(VD.YB2  , np.array(yb2  , dtype=precision))        
        VD.ZB2    = np.append(VD.ZB2  , np.array(zb2  , dtype=precision)) 
        VD.XAC    = np.append(VD.XAC  , np.array(xac  , dtype=precision))
        VD.YAC    = np.append(VD.YAC  , np.array(yac  , dtype=precision)) 
        VD.ZAC    = np.append(VD.ZAC  , np.array(zac  , dtype=precision)) 
        VD.XBC    = np.append(VD.XBC  , np.array(xbc  , dtype=precision))
        VD.YBC    = np.append(VD.YBC  , np.array(ybc  , dtype=precision)) 
        VD.ZBC    = np.append(VD.ZBC  , np.array(zbc  , dtype=precision))  
        VD.XC     = np.append(VD.XC   , np.array(xc   , dtype=precision))
        VD.YC     = np.append(VD.YC   , np.array(yc   , dtype=precision))
        VD.ZC     = np.append(VD.ZC   , np.array(zc   , dtype=precision))  
        VD.X      = np.append(VD.X    , np.array(x    , dtype=precision))
        VD.Y      = np.append(VD.Y    , np.array(y    , dtype=precision))
        VD.Z      = np.append(VD.Z    , np.array(z    , dtype=precision))         
        VD.CS     = np.append(VD.CS   , np.array(cs_w , dtype=precision))
        
        if wing.vertical:
            VD.DY     = np.append(VD.DY   , np.array(del_z, dtype=precision))
        else:
            VD.DY     = np.append(VD.DY   , np.array(del_y, dtype=precision))
        
        side_idx += 1
        
    VD.symmetric_wings = np.append(VD.symmetric_wings, int(xz_sym))
    
    # Pack wing data
    wing.n_sw = n_sw
    wing.n_cw = n_cw    
    
    return VD, wing
