# RCAIDE/Library/Methods/Mass_Properties/Moment_of_Inertia/compute_bwb_center_of_gravity.py 
# 
# Created:  January 2026, S. Shekar, A. Molloy M. Clarke,  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import RCAIDE

# package imports 
import numpy as np  
from   copy import deepcopy
import shapely.geometry as geom
from shapely import Polygon, box 
import trimesh

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Blended Wing Body Center of Gravity
# ----------------------------------------------------------------------------------------------------------------------  
def compute_bwb_center_of_gravity(bwb_wing, vehicle): 
    ''' computes the moment of inertia tensor for a blended wing body about a given center of gravity.
    Includes the ability to model a  wing fuel tank as a condensed wing

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
    - Fuel flag (whether the wing is considered a fuel tank or not)

    Outputs:
    - wing moment of inertia tensor

    Properties Used:
    N/A
    ''' 
    # compute cabin moment of inertia 
    compute_center_body_center_of_gravity(bwb_wing)
    
    # compute aft cabin moment of inertia 
    compute_aft_center_body_center_of_gravity(bwb_wing)

    # compute wing moment of intertia 
    compute_bwb_wing_center_of_gravity(bwb_wing) 

    return bwb_wing.mass_properties.center_of_gravity 

def compute_bwb_wing_center_of_gravity(bwb_wing):

    mass = bwb_wing.mass_properties.mass  

    #populate the wing segment properties and other things 
    segment_meshes = []
    seg_keys = ['wing_section_1','wing_section_2','wing_section_3']
    for i in range(len(seg_keys)-1):
        # compute volume and assume unit density to get mass
        inner_segment = bwb_wing.segments[seg_keys[i]]
        outer_segment = bwb_wing.segments[seg_keys[i+1]]


        x_in = np.array(inner_segment.airfoil.geometry.x_coordinates)[:-1] * bwb_wing.chords.root *inner_segment.root_chord_percent + inner_segment.origin[0][0]
        y_in = np.array(inner_segment.airfoil.geometry.y_coordinates)[:-1] * bwb_wing.chords.root *inner_segment.root_chord_percent + inner_segment.origin[0][2]
        x_out = np.array(outer_segment.airfoil.geometry.x_coordinates)[:-1] * bwb_wing.chords.root *outer_segment.root_chord_percent+ outer_segment.origin[0][0]
        y_out = np.array(outer_segment.airfoil.geometry.y_coordinates)[:-1] * bwb_wing.chords.root *outer_segment.root_chord_percent+ outer_segment.origin[0][2]


        points_out = list(zip(x_out, y_out))
        poly_out = Polygon(points_out)

        points_in = list(zip(x_in, y_in))
        poly_in = Polygon(points_in) 

        # Compute segment span length
        L = (outer_segment.percent_span_location - inner_segment.percent_span_location) * bwb_wing.spans.projected/2
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
        T[2, 3] = inner_segment.percent_span_location * bwb_wing.spans.projected/2
        solid_segment.apply_transform(T)
        R = trimesh.transformations.rotation_matrix(np.deg2rad(90), [1, 0, 0], [0, 0, 0])
        solid_segment.apply_transform(R)

        segment_meshes.append(solid_segment)
    
    combinde_mesh = trimesh.util.concatenate([segment_meshes[0],segment_meshes[1]])
    # Reflect across the YZ plane (mirror X)
    Ry = np.diag([1, -1, 1])   # reflection matrix

    # 1. copy the mesh
    combined_mesh_sym = deepcopy(combinde_mesh)

    # 2. apply the mirror transform
    combined_mesh_sym.vertices = (Ry @ combined_mesh_sym.vertices.T).T

    # 3. fix face orientation (reverse winding)
    combined_mesh_sym.faces = combined_mesh_sym.faces[:, ::-1]

    # 4. concatenate original + mirrored
    combined_mesh_full = trimesh.util.concatenate([combinde_mesh, combined_mesh_sym])
    combined_mesh_full.density = mass / combined_mesh_full.volume
    I        = combined_mesh_full.moment_inertia
    centroid = combined_mesh_full.centroid 
      
    # store values 
    bwb_wing.mass_properties.center_of_gravity         =  [centroid.tolist()]
    bwb_wing.mass_properties.moments_of_inertia.tensor =  I
    return   

def compute_aft_center_body_center_of_gravity(bwb_wing):
    mass          = bwb_wing.aft_center_body.mass_properties.mass
    origin_x      = bwb_wing.layout_of_passenger_accommodations.object_coordinates[-1][2] + bwb_wing.layout_of_passenger_accommodations.cabin_x_offset
    cabin_length  = bwb_wing.layout_of_passenger_accommodations.object_coordinates[-1][2] - bwb_wing.layout_of_passenger_accommodations.cabin_x_offset 
 
    segment_meshes = []
    seg_keys = ['fuselage_section_1','fuselage_section_2','fuselage_section_3','cabin_wall','fuel_wall']
    for i in range(len(seg_keys)-1):
        # compute volume and assume unit density to get mass
        inner_segment = bwb_wing.segments[seg_keys[i]]
        outer_segment = bwb_wing.segments[seg_keys[i+1]]


        x_in = np.array(inner_segment.airfoil.geometry.x_coordinates)[:-1] * bwb_wing.chords.root *inner_segment.root_chord_percent + inner_segment.origin[0][0]
        y_in = np.array(inner_segment.airfoil.geometry.y_coordinates)[:-1] * bwb_wing.chords.root *inner_segment.root_chord_percent + inner_segment.origin[0][2]
        x_out = np.array(outer_segment.airfoil.geometry.x_coordinates)[:-1] * bwb_wing.chords.root *outer_segment.root_chord_percent+ outer_segment.origin[0][0]
        y_out = np.array(outer_segment.airfoil.geometry.y_coordinates)[:-1] * bwb_wing.chords.root *outer_segment.root_chord_percent+ outer_segment.origin[0][2]

        cabin_seperation = box(cabin_length, -1e9, 1e9, 1e9)
        points_out = list(zip(x_out, y_out))
        poly_out = Polygon(points_out)
        poly_out = poly_out.intersection(cabin_seperation)

        points_in = list(zip(x_in, y_in))
        poly_in = Polygon(points_in)
        poly_in = poly_in.intersection(cabin_seperation) 

        # Compute segment span length
        L = (outer_segment.percent_span_location - inner_segment.percent_span_location) * bwb_wing.spans.projected/2
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
        T[2, 3] = inner_segment.percent_span_location * bwb_wing.spans.projected/2
        solid_segment.apply_transform(T)
        R = trimesh.transformations.rotation_matrix(np.deg2rad(90), [1, 0, 0], [0, 0, 0])
        solid_segment.apply_transform(R)

        segment_meshes.append(solid_segment)
    
    combinde_mesh = trimesh.util.concatenate([segment_meshes[0],segment_meshes[1],segment_meshes[2]])
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
    I                          = combined_mesh_full.moment_inertia
    centroid                   = combined_mesh_full.centroid 
        
    # store values 
    bwb_wing.aft_center_body.mass_properties.center_of_gravity         =  [centroid.tolist()]
    bwb_wing.aft_center_body.mass_properties.moments_of_inertia.tensor =  I
    bwb_wing.aft_center_body.origin                                    = [[origin_x,0, 0]]
    
    return  

def compute_center_body_center_of_gravity(bwb_wing): 
    mass          = bwb_wing.center_body.mass_properties.mass
    origin_x      = bwb_wing.layout_of_passenger_accommodations.cabin_x_offset
    cabin_length  = bwb_wing.layout_of_passenger_accommodations.object_coordinates[-1][2] - origin_x
 
    segment_meshes = []
    seg_keys = ['fuselage_section_1','fuselage_section_2','fuselage_section_3','cabin_wall']
    for i in range(len(seg_keys)-1):
        # compute volume and assume unit density to get mass
        inner_segment = bwb_wing.segments[seg_keys[i]]
        outer_segment = bwb_wing.segments[seg_keys[i+1]]


        x_in = np.array(inner_segment.airfoil.geometry.x_coordinates)[:-1] * bwb_wing.chords.root *inner_segment.root_chord_percent + inner_segment.origin[0][0]
        y_in = np.array(inner_segment.airfoil.geometry.y_coordinates)[:-1] * bwb_wing.chords.root *inner_segment.root_chord_percent + inner_segment.origin[0][2]
        x_out = np.array(outer_segment.airfoil.geometry.x_coordinates)[:-1] * bwb_wing.chords.root *outer_segment.root_chord_percent+ outer_segment.origin[0][0]
        y_out = np.array(outer_segment.airfoil.geometry.y_coordinates)[:-1] * bwb_wing.chords.root *outer_segment.root_chord_percent+ outer_segment.origin[0][2]

        cabin_seperation = box(-1e9, -1e9, cabin_length, 1e9)
        points_out = list(zip(x_out, y_out))
        poly_out = Polygon(points_out)
        poly_out = poly_out.intersection(cabin_seperation)

        points_in = list(zip(x_in, y_in))
        poly_in = Polygon(points_in)
        poly_in = poly_in.intersection(cabin_seperation)
        
        A_1 = poly_in.area
        A_2 = poly_out.area

        # Compute segment span length
        L = (outer_segment.percent_span_location - inner_segment.percent_span_location) * bwb_wing.spans.projected/2
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
        T[2, 3] = inner_segment.percent_span_location * bwb_wing.spans.projected/2
        solid_segment.apply_transform(T)
        R = trimesh.transformations.rotation_matrix(np.deg2rad(90), [1, 0, 0], [0, 0, 0])
        solid_segment.apply_transform(R)

        segment_meshes.append(solid_segment)
    
    combinde_mesh = trimesh.util.concatenate([segment_meshes[0],segment_meshes[1],segment_meshes[2]])
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
    I                          = combined_mesh_full.moment_inertia
    centroid                   = combined_mesh_full.centroid
    
    # store values 
    bwb_wing.center_body.mass_properties.center_of_gravity         =  [centroid.tolist()]
    bwb_wing.center_body.mass_properties.moments_of_inertia.tensor =  I
    bwb_wing.center_body.origin                                    = [[origin_x,0, 0]]
    
    return   