# RCAIDE/Library/Methods/Mass_Properties/Center_of_Gravity/compute_wing_integral_tank_center_of_gravity.py 
# 
# Created:  Dec 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
import RCAIDE
from RCAIDE.Library.Methods.Geometry.Planform.compute_segment_volume   import compute_segment_volume
from RCAIDE.Library.Methods.Geometry.Planform.compute_segment_centroid import compute_segment_centroid
from RCAIDE.Library.Methods.Geometry.Airfoil import import_airfoil_geometry
from RCAIDE.Library.Methods.Geometry.Airfoil import compute_naca_4series 

# package imports 
import numpy as np  
from   copy import deepcopy
import shapely.geometry as geom
from shapely import Polygon, box 
import trimesh


# ----------------------------------------------------------------------------------------------------------------------
#  Compute Boom Center of Gravity
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_wing_integral_tank_center_of_gravity(fuel_tank,vehicle):   
    wing    = vehicle.wings[fuel_tank.wing_tag]
    mass    = fuel_tank.fuel.mass_properties.mass
    symm    = wing.xz_plane_symmetric
    n_points =  101
    
    if len(wing.segments) != 0:
        segment_meshes = []
        seg_keys       = fuel_tank.segments_bounding_tank
        for i in range(len(seg_keys)-1):
            # compute volume and assume unit density to get mass
            inner_segment = wing.segments[seg_keys[i]]
            outer_segment = wing.segments[seg_keys[i+1]] 
 
            # Compute segment span length
            L = (outer_segment.percent_span_location - inner_segment.percent_span_location) * wing.spans.projected/(symm + 1)
            spanwise_shift = inner_segment.percent_span_location * wing.spans.projected/2 
            
             
            airfoil_in = inner_segment.airfoil 
            if  airfoil_in !=  None:                 
                if type(airfoil_in) == RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil:
                    geometry_in = compute_naca_4series(airfoil_in.NACA_4_Series_code,n_points)
                elif type(airfoil_in) == RCAIDE.Library.Components.Airfoils.Airfoil: 
                    geometry_in     = import_airfoil_geometry(airfoil_in.coordinate_file,n_points)
            else:
                geometry_in = compute_naca_4series('0012',n_points)
    
            airfoil_out = outer_segment.airfoil 
            if  airfoil_out !=  None:                 
                if type(airfoil_out) == RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil:
                    geometry_out = compute_naca_4series(airfoil_out.NACA_4_Series_code,n_points)
                elif type(airfoil_out) == RCAIDE.Library.Components.Airfoils.Airfoil: 
                    geometry_out     = import_airfoil_geometry(airfoil_out.coordinate_file,n_points)
            else:
                geometry_out = compute_naca_4series('0012',n_points)
                                
            x_in  = np.array(geometry_in.x_coordinates)[:-1] * wing.chords.root *inner_segment.root_chord_percent + inner_segment.origin[0][0]
            y_in  = np.array(geometry_in.y_coordinates)[:-1] * wing.chords.root *inner_segment.root_chord_percent + inner_segment.origin[0][2]
            x_out = np.array(geometry_out.x_coordinates)[:-1] * wing.chords.root *outer_segment.root_chord_percent + outer_segment.origin[0][0]
            y_out = np.array(geometry_out.y_coordinates)[:-1] * wing.chords.root *outer_segment.root_chord_percent + outer_segment.origin[0][2]
    
            solid_segment =  compute_segment_meshes(x_in,y_in, x_out, y_out, L, spanwise_shift) 
            segment_meshes.append(solid_segment)
    else:

        seg_keys       = fuel_tank.segments_bounding_tank 
        # compute volume and assume unit density to get mass
        inner_segment = wing.segments[seg_keys[i]]
        outer_segment = wing.segments[seg_keys[i+1]] 

        # Compute segment span length
        L              = wing.spans.projected/(symm + 1)
        spanwise_shift = 0
 
        if wing.airfoil != None:
            airfoil = wing.airfoil
            if type(airfoil) == RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil:
                geometry = compute_naca_4series(airfoil.NACA_4_Series_code,n_points)
            elif type(airfoil) == RCAIDE.Library.Components.Airfoils.Airfoil: 
                geometry     = import_airfoil_geometry(airfoil.coordinate_file,n_points)
        else:
            geometry = compute_naca_4series('0012',n_points)
    
        dihedral   = wing.dihedral 
        sweep      = wing.sweeps.leading_edge 
        x_in  = np.array(geometry.x_coordinates)[:-1]  * wing.chords.root   + wing.origin[0][0]
        y_in  = np.array(geometry.y_coordinates)[:-1]  * wing.chords.root   + wing.origin[0][2]
        x_out = np.array(geometry.x_coordinates)[:-1]  * wing.chords.tip    + L*np.tan(sweep)
        y_out = np.array(geometry.y_coordinates)[:-1]  * wing.chords.tip    + L*np.tan(dihedral)
        
        solid_segment =  compute_segment_meshes(x_in,y_in, x_out, y_out, L, spanwise_shift) 
        segment_meshes.append(solid_segment)
            
        
    combinde_mesh = trimesh.util.concatenate(segment_meshes)
    # Reflect across the YZ plane (mirror X)
    Ry = np.diag([1, -1, 1])   # reflection matrix

    # 1. copy the mesh
    combined_mesh_sym = deepcopy(combinde_mesh)

    # 2. apply the mirror transform
    combined_mesh_sym.vertices = (Ry @ combined_mesh_sym.vertices.T).T

    # 3. fix face orientation (reverse winding)
    combined_mesh_sym.faces = combined_mesh_sym.faces[:, ::-1]

    # 4. concatenate original + mirrored
    combined_mesh_full         = trimesh.util.concatenate([combinde_mesh, combined_mesh_sym])
    combined_mesh_full.density = mass / combined_mesh_full.volume

    # axes = trimesh.creation.axis(axis_length=1.0)
    # # Add your mesh and the axes to a scene
    # scene = trimesh.Scene([combinde_mesh, combined_mesh_sym,axes])
    # scene.show()
    centroid = combined_mesh_full.centroid
    cg_x     = centroid[0]
    cg_y     = 0
    cg_z     = centroid[2]
    center_of_gravity = [[cg_x, cg_y, cg_z]]
    
    # Shift inertia tensor from origin to the requested (actual) centroid
    I = combined_mesh_full.moment_inertia 
    volume   = combined_mesh_full.volume 
    
    fuel_tank.fuel.mass_properties.center_of_gravity          = center_of_gravity
    fuel_tank.fuel.mass_properties.moments_of_inertia.tensor  = I
        
    return fuel_tank.mass_properties.center_of_gravity


def compute_segment_meshes(x_in,y_in, x_out, y_out, L, spanwise_shift):

    points_out = list(zip(x_out, y_out))
    poly_out = Polygon(points_out)

    points_in = list(zip(x_in, y_in))
    poly_in = Polygon(points_in) 
    
    # STEP 1: Build 3D point clouds for both sections
    x1, y1 = poly_in.exterior.xy
    x2, y2 = poly_out.exterior.xy

    pts1 = np.column_stack((x1[:-1], y1[:-1], np.zeros(len(x1)-1)))   # z = 0
    pts2 = np.column_stack((x2[:-1], y2[:-1], np.full(len(x2)-1, L))) # z = L

    # STEP 2: Combine all points
    all_pts = np.vstack([pts1, pts2])

    # STEP 3: Convex hull → watertight volume mesh
    solid_segment = trimesh.convex.convex_hull(all_pts)

    # Apply spanwise translation AFTER orientation fix
    T = np.eye(4)
    T[0, 3] = 0.0
    T[1, 3] = 0.0
    T[2, 3] = spanwise_shift
    solid_segment.apply_transform(T)
    R = trimesh.transformations.rotation_matrix(np.deg2rad(90), [1, 0, 0], [0, 0, 0])
    solid_segment.apply_transform(R)
    
    return solid_segment