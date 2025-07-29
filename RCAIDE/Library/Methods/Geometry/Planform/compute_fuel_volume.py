# RCAIDE/Library/Methods/Geometry/Planform/compute_fuel_volume.py
# 
# 
# Created:  Jul 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
import RCAIDE 
from RCAIDE.Library.Methods.Geometry.Airfoil import import_airfoil_geometry,  compute_naca_4series  
from RCAIDE.Library.Methods.Geometry.Planform.convert_sweep import convert_sweep_segments 
from RCAIDE.Framework.Core import Units
import matplotlib.pyplot as plt

# python imports 
import numpy as np   
from scipy.interpolate import interp1d
from shapely.geometry import Polygon, Point
from copy import  deepcopy
import os 

# ----------------------------------------------------------------------------------------------------------------------
# compute_fuel_volume 
# ----------------------------------------------------------------------------------------------------------------------
def compute_fuel_volume(vehicle, update_max_fuel =True):
    wings     = vehicle.wings
    fuselages = vehicle.fuselages
    total_fuel_volume = 0
    total_fuel_mass   = 0
    tank_percent_span_location = 0
    for network in vehicle.networks: 
        for fuel_line in network.fuel_lines:
            for fuel_tank in fuel_line.fuel_tanks: 
                fuel_tank.internal_volume = 0
                tank_c_g    =  [[0, 0, 0]]
                tank_mass   = 0

                # fuel tanks integrated into wings 
                if fuel_tank.wing_tag != None:
                    wing = wings[fuel_tank.wing_tag]  
                    if type(fuel_tank) == RCAIDE.Library.Components.Powertrain.Sources.Fuel_Tanks.Integral_Tank: 
                        if len(wing.segments) > 1:
                            segment_tank_moment = np.array([0.0, 0.0, 0.0])
                            seg_tags = list(wing.segments.keys())
                            for i in range(len(seg_tags)-1):
                                inner_segment = wing.segments[seg_tags[i]]
                                outer_segment = wing.segments[seg_tags[i+1]]
                                if inner_segment.has_fuel_tank == True:

                                    # get orgin of fuel tank     
                                    fuel_tank.origin = wing.origin # NEED TO UPDATE

                                    # compute volume of fuel in wing
                                    volume = compute_segmented_wing_integral_tank_fuel_volume(fuel_tank,wing,inner_segment,outer_segment)
                                    fuel_tank.internal_volume += volume 
                                    total_fuel_volume     += volume
                                    total_fuel_mass       += volume * fuel_tank.fuel.density
                                    tank_mass             += volume * fuel_tank.fuel.density
                                    segment_tank_moment   += np.array(inner_segment.mass_properties.center_of_gravity)[0] * tank_mass

                            tank_c_g = list(segment_tank_moment / tank_mass)
                        else: 
                            # get orgin of fuel tank     
                            fuel_tank.origin = wing.origin 

                            # assume whole wing has fuel 
                            volume = compute_wing_integral_tank_fuel_volume(fuel_tank,wing)                         
                            fuel_tank.internal_volume += volume 
                            total_fuel_volume += volume
                            total_fuel_mass   += volume * fuel_tank.fuel.density
                            tank_mass         += volume * fuel_tank.fuel.density
                            tank_c_g          = wing.aerodynamic_center  

                    elif type(fuel_tank) == RCAIDE.Library.Components.Powertrain.Sources.Fuel_Tanks.Non_Integral_Tank: 
                        if len(wing.segments) > 1: 
                            seg_tags = list(wing.segments.keys())
                            for i in range(len(seg_tags)-1):
                                inner_segment = wing.segments[seg_tags[i]]
                                outer_segment = wing.segments[seg_tags[i+1]]
                                if inner_segment.has_fuel_tank == True:  
                                    # compute volume and update percent span location of next non-integral tank 
                                    try:
                                        volume ,  tank_percent_span_location = compute_wing_non_integral_tank_fuel_volume(fuel_tank,wing,inner_segment,outer_segment,tank_percent_span_location)
                                    except:
                                        RuntimeWarning('Fuel tank cannot be place in specified wing segment, trying next segment')
                                        outer_segment = wing.segments[seg_tags[i+2]]
                                        volume ,  tank_percent_span_location = compute_wing_non_integral_tank_fuel_volume(fuel_tank,wing,inner_segment,outer_segment,tank_percent_span_location)


                                    fuel_tank.internal_volume += volume 
                                    total_fuel_volume += volume  
                                    total_fuel_mass   += volume * fuel_tank.fuel.density 
                                    tank_mass         += volume * fuel_tank.fuel.density   
                                    tank_c_g          = [[fuel_tank.length /2, 0, fuel_tank.outer_diameter / 2]]             

                # fuel tanks integrated fuselage
                elif fuel_tank.fuselage_tag != None: 
                    fuselage = fuselages[fuel_tank.fuselage_tag]  
                    if type(fuel_tank) == RCAIDE.Library.Components.Powertrain.Sources.Fuel_Tanks.Integral_Tank:

                        if len(fuselage.segments) > 1:
                            tank_section_percent_x = 0
                            seg_tags = list(fuselage.segments.keys())
                            for i in range(len(seg_tags)-1):
                                inner_segment = fuselage.segments[seg_tags[i]]
                                outer_segment = fuselage.segments[seg_tags[i+1]]
                                if inner_segment.has_fuel_tank == True: 
                                    volume = compute_fuselage_integral_tank_fuel_volume(fuel_tank,fuselage,inner_segment,outer_segment,tank_section_percent_x)
                                    fuel_tank.internal_volume += volume 
                                    total_fuel_volume += volume  
                                    total_fuel_mass   += volume * fuel_tank.fuel.density
                                    tank_mass         += volume * fuel_tank.fuel.density  
                                    tank_c_g           = [[fuselage.lengths.total * (inner_segment.percent_x_location  + outer_segment.percent_x_location)/2 ,0,  (inner_segment.height  + outer_segment.height)/2]]

                    elif type(fuel_tank) == RCAIDE.Library.Components.Powertrain.Sources.Fuel_Tanks.Non_Integral_Tank:

                        # compute volume and update percent span location of next non-integral tank 
                        volume  = compute_fuselage_non_integral_tank_fuel_volume(fuel_tank,fuselage)
                        fuel_tank.internal_volume += volume 
                        total_fuel_volume += volume  
                        total_fuel_mass   += volume * fuel_tank.fuel.density
                        tank_c_g           = [[fuel_tank.length /2, 0, fuel_tank.outer_diameter / 2]]
                else:
                    if type(fuel_tank) == RCAIDE.Library.Components.Powertrain.Sources.Fuel_Tanks.Non_Integral_Tank: 
                        if fuel_tank.bwb_aft_tank == True: 
                            # Check if there are enough properties to accurately compute the maximum possible tank volume 
                            if any(val is None for val in [
                                fuel_tank.aft_tank_start_root_chord,
                                fuel_tank.aft_tank_end_rood_chord,
                                fuel_tank.aft_tank_end_segment_tag,
                                fuel_tank.wing_root_tag
                                ]):
                                raise ValueError("One or more required aft tank parameters are not set in 'fuel_tank'.")

                            wing = wings[fuel_tank.wing_root_tag]  

                            if len(wing.segments) > 1: 
                                seg_tags = list(wing.segments.keys())
                            index = seg_tags.index(fuel_tank.aft_tank_end_segment_tag)
                            aft_tank_seg_tags = seg_tags[:index + 1]

                            circle_coordiantes =[]
                            for i,tag in enumerate(aft_tank_seg_tags):
                                segment = wing.segments[tag]

                                #baseline dimensions  
                                chord_root = wing.chords.root
                                start = fuel_tank.aft_tank_start_root_chord * chord_root
                                end   = fuel_tank.aft_tank_end_rood_chord   * chord_root

                                # Need to get Z coordinates from airfoil data
                                af = segment.airfoil   
                                coord_file = af.get('coordinate_file', None)
                                if coord_file and os.path.isfile(coord_file):
                                    # Load and scale coordinates
                                    coords = np.loadtxt(coord_file, skiprows=1)
                                    scale = wing.chords.root * segment.root_chord_percent
                                    coords *= scale

                                # Extract and shift to segment origin
                                orig_x, orig_y, orig_z = segment.origin[0]
                                x = coords[:, 0] + orig_x
                                z = coords[:, 1] + orig_z
                                y = orig_y  

                                # Flip the first half so upper and lower surfaces line up
                                half = len(x) // 2
                                x = np.concatenate((x[:half][::-1], x[half:]))
                                z = np.concatenate((z[:half][::-1], z[half:]))

                                # Mask points within the aft‑tank region
                                mask = (x >= start) & (x <= end)
                                x_tank_possible = x[mask]
                                z_tank_possible = z[mask]

                                # separate positive and negative z
                                mask_pos = z_tank_possible >= 0
                                mask_neg = z_tank_possible <  0

                                x_pos, z_pos = x_tank_possible[mask_pos], z_tank_possible[mask_pos]
                                x_neg, z_neg = x_tank_possible[mask_neg], z_tank_possible[mask_neg]

                                # sort each pair by x
                                pos_idx = np.argsort(x_pos)
                                x_pos, z_pos = x_pos[pos_idx], z_pos[pos_idx]

                                neg_idx = np.argsort(x_neg)
                                x_neg, z_neg = x_neg[neg_idx], z_neg[neg_idx]

                                # build interpolators 
                                z_interp_pos = interp1d(x_pos, z_pos, kind='linear', fill_value="extrapolate")
                                z_interp_neg = interp1d(x_neg, z_neg, kind='linear', fill_value="extrapolate")

                                new_x = np.linspace(x_tank_possible.min(), x_tank_possible.max(), 10)
                                z_upper = z_interp_pos(new_x)
                                z_lower = z_interp_neg(new_x)

                                max_diameter,x_center,z_center = compute_largest_circle(new_x,z_upper,z_lower)
                                circle_coordiantes.append([max_diameter, x_center,y, z_center])

                            circle_coordiantes = np.array(circle_coordiantes)

                            # Now that we have x,y,z and  max circle diamteres we will start computing the volumes for all the possible cases. 
                            max_dia, x_ctr, y, z_ctr = circle_coordiantes.T
                            # define new, equispaced y
                            y_new = np.linspace(y.min(), y.max(), 100)
                            f_dia = interp1d(y, max_dia, kind='cubic', fill_value='extrapolate')
                            f_x   = interp1d(y, x_ctr,   kind='cubic', fill_value='extrapolate')
                            f_z   = interp1d(y, z_ctr,   kind='cubic', fill_value='extrapolate')

                            max_dia_cub = f_dia(y_new)
                            x_cub       = f_x(y_new)
                            z_cub       = f_z(y_new)

                            interpolated_circle_coordinates  = np.column_stack([max_dia_cub/2, x_cub, y_new, z_cub])
                                                                                # Radii,        x,     y,      z
                            d = np.hypot((interpolated_circle_coordinates[1:,1]-interpolated_circle_coordinates[0,1]),(interpolated_circle_coordinates[1:,3]-interpolated_circle_coordinates[0,3]))
                            r = (interpolated_circle_coordinates[0,0] + interpolated_circle_coordinates[1:,0] - d) / 2
                            t = (interpolated_circle_coordinates[0,0] - r) / d
                            xc = interpolated_circle_coordinates[0,1] + t * (interpolated_circle_coordinates[1:,1] - interpolated_circle_coordinates[0,1])
                            zc = interpolated_circle_coordinates[0,3] + t * (interpolated_circle_coordinates[1:,3] - interpolated_circle_coordinates[0,3])

                            maximum_circle_coordinates  = np.column_stack([r*2, xc, interpolated_circle_coordinates[1:,2], zc])
                                                                            #Dia, x,     y,      z

                           
                            r      = (maximum_circle_coordinates[:,0] -  fuel_tank.radial_offset - 2 * fuel_tank.wall_thickness) / 2
                            l      = maximum_circle_coordinates[:,2] - maximum_circle_coordinates[:,0]/2 # Length of cylinder Section of the rounded edge tank 
                            volume = (np.pi * ( r** 2) * l +  4 / 3 * np.pi * ( r** 3))*2 # multiply the volume by 2 as it is symmetric about root chord

                            max_volume_index = np.argmax(volume)    

                            fuel_tank.internal_volume += volume[max_volume_index]
                            total_fuel_volume += volume[max_volume_index]
                            total_fuel_mass   += volume[max_volume_index] * fuel_tank.fuel.density
                            # Geometric Properties for Plotting 

                            fuel_tank.outer_diameter = maximum_circle_coordinates[max_volume_index,0]  -  fuel_tank.radial_offset - 2 * fuel_tank.wall_thickness
                            fuel_tank.length         = 2*(r[max_volume_index]+l[max_volume_index]) # Length of whole tank with rounded edges
                            
                            fuel_tank.origin[0][0]   = maximum_circle_coordinates[max_volume_index,1] - fuel_tank.outer_diameter/2
                            fuel_tank.origin[0][1]   = -(r[max_volume_index]+l[max_volume_index]) # Start of roudned edge of the tank
                            fuel_tank.origin[0][2]   = maximum_circle_coordinates[max_volume_index,3]


                        else:
                            volume  = compute_non_integral_tank_fuel_volume(fuel_tank)
                            fuel_tank.internal_volume += volume 
                            total_fuel_volume += volume  
                            total_fuel_mass   += volume * fuel_tank.fuel.density
                            tank_c_g           = [[fuel_tank.length /2, 0, fuel_tank.outer_diameter / 2]]

                fuel_tank.mass_properties.center_of_gravity =  tank_c_g
                fuel_tank.mass_properties.mass = tank_mass
    vehicle.fuel_tank_volume = total_fuel_volume # temp ********** find a better place for it 
    if update_max_fuel:
        vehicle.mass_properties.max_fuel = total_fuel_mass
    return


def compute_non_integral_tank_fuel_volume(fuel_tank):  

    l      = fuel_tank.length - fuel_tank.outer_diameter # assuming rounded end cylindrical tank
    r      = (fuel_tank.outer_diameter - 2 * fuel_tank.wall_thickness) / 2
    volume = np.pi * ( r** 2) * l +  4 / 3 * np.pi * ( r** 3)       

    return volume


def compute_fuselage_integral_tank_fuel_volume(fuel_tank,fuselage,fus_first_segment,fus_second_segment,tank_section_percent_x): 

    # volume of truncated  
    A_1    = np.pi * fus_first_segment.height /2  *  fus_first_segment.width/2
    A_2    = np.pi * fus_second_segment.height/2  *  fus_second_segment.width/2
    h      = fuselage.lengths.total * (fus_second_segment.percent_x_location  - fus_first_segment.percent_x_location)
    volume = (1 /3) * ( A_1 + A_2 + np.sqrt(A_1*A_2)) *h 

    return volume


def compute_fuselage_non_integral_tank_fuel_volume(fuel_tank,fuselage):  
    l      = fuel_tank.length - fuel_tank.outer_diameter # assuming rounded end cylindrical tank
    r      = (fuel_tank.outer_diameter - 2 * fuel_tank.wall_thickness) / 2
    volume = np.pi * ( r** 2) * l +  4 / 3 * np.pi * ( r** 3)       
    return volume


def compute_wing_non_integral_tank_fuel_volume(fuel_tank,wing,inner_segment_0,outer_segment,tank_percent_span_location):

    semi_span      = wing.spans.projected / 2
    inner_segment  = deepcopy(inner_segment_0) 
    spar_sweep     = convert_sweep_segments(inner_segment_0.sweeps.quarter_chord, inner_segment_0, outer_segment, wing, old_ref_chord_fraction=0.25, new_ref_chord_fraction=inner_segment_0.fuel_tank.percent_chord_start_location)     
    if tank_percent_span_location > inner_segment_0.percent_span_location: 
        inner_segment.percent_span_location = tank_percent_span_location
        m        =  (outer_segment.root_chord_percent -  inner_segment_0.root_chord_percent) / (outer_segment.percent_span_location - inner_segment_0.percent_span_location)
        delta_y_percent  =  (tank_percent_span_location - inner_segment_0.percent_span_location)
        inner_segment.root_chord_percent = inner_segment_0.root_chord_percent + m*delta_y_percent

        # update segment origin
        delta_y                    = delta_y_percent * semi_span
        inner_segment.origin[0][0] = inner_segment_0.origin[0][0] + delta_y * np.tan( np.pi/2 -inner_segment_0.sweeps.leading_edge) 
        inner_segment.origin[0][1] = inner_segment.percent_span_location * semi_span
        inner_segment.origin[0][2] = inner_segment_0.origin[0][2] +  delta_y *np.tan(inner_segment.dihedral_outboard)

    inner_front_rib_yu,inner_rear_rib_yu,inner_front_rib_yl,inner_rear_rib_yl = compute_non_dimensional_rib_coordinates(inner_segment)
    inner_segment_chord     = wing.chords.root * inner_segment.root_chord_percent
    inner_front_rib_length  = inner_segment_chord * (abs(inner_front_rib_yu) + abs(inner_front_rib_yl)) 
    inner_rear_rib_length   = inner_segment_chord * (abs(inner_rear_rib_yu) + abs(inner_rear_rib_yl) )
    inner_wingbox_length    = inner_segment_chord * (inner_segment.fuel_tank.percent_chord_end_location -inner_segment.fuel_tank.percent_chord_start_location)

    clearance  = fuel_tank.wall_clearance
    delta_span = (outer_segment.percent_span_location - inner_segment.percent_span_location) * semi_span

    outer_front_rib_yu,outer_rear_rib_yu,outer_front_rib_yl,outer_rear_rib_yl = compute_non_dimensional_rib_coordinates(outer_segment)
    outer_segment_chord     = wing.chords.root * outer_segment.root_chord_percent
    outer_front_rib_length  = outer_segment_chord * (abs(outer_front_rib_yu) + abs(outer_front_rib_yl)) 
    outer_rear_rib_length   = outer_segment_chord * (abs(outer_rear_rib_yu) + abs(outer_rear_rib_yl))
    outer_wingbox_length    = outer_segment_chord * (outer_segment.fuel_tank.percent_chord_end_location -outer_segment.fuel_tank.percent_chord_start_location)   

    # inner segment coordinate  
    inner_segment_thickness =  np.minimum(inner_front_rib_length,inner_rear_rib_length)
    z_inner_upper  = inner_segment.origin[0][2] + (inner_segment_thickness / 2) - clearance
    z_inner_lower  = inner_segment.origin[0][2] - (inner_segment_thickness / 2) + clearance
    y_inner_upper  = inner_segment.percent_span_location * wing.spans.projected
    y_inner_lower  = y_inner_upper

    # outer segment coordinates  
    outer_segment_thickness =  np.minimum(outer_front_rib_length,outer_rear_rib_length)
    z_outer_upper  = inner_segment.origin[0][2] + delta_span *np.tan(inner_segment.dihedral_outboard) + outer_segment_thickness / 2 - clearance
    z_outer_lower  = inner_segment.origin[0][2] + delta_span *np.tan(inner_segment.dihedral_outboard) - outer_segment_thickness / 2 + clearance
    y_outer_upper  = outer_segment.percent_span_location * wing.spans.projected
    y_outer_lower  = y_outer_upper  

    dz_upper   = z_outer_upper - z_inner_upper
    dy_upper   = y_outer_upper - y_inner_upper
    dz_lower   = z_outer_lower - z_inner_lower
    dy_lower   = y_outer_lower - y_inner_lower

    # determine slopes 
    upper_slope = np.arctan(dz_upper/dy_upper) # might need to make negative
    lower_slope = np.arctan(dz_lower/dy_lower) 

    # determine tank diameter and location of next spar 
    D         = 0.1
    epsilon_D = 10 


    while abs(epsilon_D) > 0.001:
        AD =  D / np.cos(upper_slope)
        BC =  D / np.cos(lower_slope)

        # get equation of upper line
        f_upper = interp1d(np.array([y_inner_upper ,y_outer_upper  ]), np.array([z_inner_upper ,z_outer_upper  ]))

        # get equation of lower line
        f_lower = interp1d(np.array([y_inner_lower ,y_outer_lower ]), np.array([z_inner_lower ,z_outer_lower ]))

        AB = f_upper(y_inner_upper)  - f_lower(y_inner_upper)
        DC = f_upper(y_inner_upper+D)  - f_lower(y_inner_upper+D)

        epsilon_D  =  AB + DC - AD - BC

        delta_AD   = epsilon_D / (1 +  np.cos(upper_slope) /np.cos(lower_slope) )

        detla_D    = delta_AD *  np.cos(upper_slope)

        D += detla_D 

    # store tank diamter (this will set the location of the next segment)
    fuel_tank.outer_diameter = D 

    # update tank percent span location
    tank_percent_span_location = inner_segment.percent_span_location +  D / semi_span 

    # get orgin of fuel tank 
    origin_x         = inner_segment.origin[0][0] + (inner_segment.fuel_tank.percent_chord_start_location * inner_segment_chord) + (np.tan( np.pi/2 - spar_sweep) * D / 2) -D/2
    origin_y         = inner_segment.origin[0][1] + D / 2
    origin_z         = inner_segment.origin[0][2] + (D / 2) *np.tan(inner_segment.dihedral_outboard)
    fuel_tank.origin = [[origin_x,origin_y,origin_z]] 

    # get length of tank 
    m_2 =  (outer_wingbox_length -  inner_wingbox_length) / (outer_segment.percent_span_location - inner_segment_0.percent_span_location)  
    l_1 =  inner_wingbox_length +  m_2 * (tank_percent_span_location - inner_segment_0.percent_span_location)
    l_2 =  inner_wingbox_length -  (D / np.tan( np.pi/2 -spar_sweep)) 
    l   =  np.minimum(l_1, l_2) + D

    # internal radius of tank 
    r   = (D -  2 * fuel_tank.wall_thickness ) / 2
    volume = np.pi * ( r** 2) * (l - D)  +  4 / 3 * np.pi * ( r** 3) 
    if fuel_tank.symmetric:
        volume *= 2

    fuel_tank.length = l
    fuel_tank.height = D

    return volume ,  tank_percent_span_location

def compute_wing_integral_tank_fuel_volume(fuel_tank,wing):     

    inner_front_rib_yu,inner_rear_rib_yu,inner_front_rib_yl,inner_rear_rib_yl = compute_non_dimensional_rib_coordinates(wing) 
    inner_front_rib_length  = wing.chords.root * (abs(inner_front_rib_yu) + abs(inner_front_rib_yl))
    inner_rear_rib_length   = wing.chords.root * (abs(inner_rear_rib_yu) + abs(inner_rear_rib_yl))
    inner_wingbox_length    = wing.chords.root * (wing.fuel_tank.percent_chord_end_location -wing.fuel_tank.percent_chord_start_location)  

    outer_front_rib_yu,outer_rear_rib_yu,outer_front_rib_yl,outer_rear_rib_yl = compute_non_dimensional_rib_coordinates(wing) 
    outer_front_rib_length  = wing.chords.tip * (abs(outer_front_rib_yu) + abs(outer_front_rib_yl))
    outer_rear_rib_length   = wing.chords.tip * (abs(outer_rear_rib_yu) + abs(outer_rear_rib_yl))
    outer_wingbox_length    = wing.chords.tip * (wing.fuel_tank.percent_chord_end_location -wing.fuel_tank.percent_chord_start_location)   

    # volume of truncated prism
    A_1 = inner_wingbox_length * (inner_front_rib_length + inner_rear_rib_length) / 2 
    A_2 = outer_wingbox_length * (outer_front_rib_length + outer_rear_rib_length) / 2
    h =  wing.spans.projected
    volume = (1 /3) * ( A_1 + A_2 + np.sqrt(A_1*A_2)) *h   

    return volume

def compute_segmented_wing_integral_tank_fuel_volume(fuel_tank,wing,inner_segment,outer_segment):   

    inner_front_rib_yu,inner_rear_rib_yu,inner_front_rib_yl,inner_rear_rib_yl = compute_non_dimensional_rib_coordinates(inner_segment)
    inner_segment_chord     = wing.chords.root * inner_segment.root_chord_percent
    inner_front_rib_length  = inner_segment_chord * (abs(inner_front_rib_yu) + abs(inner_front_rib_yl))
    inner_rear_rib_length   = inner_segment_chord * (abs(inner_rear_rib_yu) + abs(inner_rear_rib_yl) )
    inner_wingbox_length    = inner_segment_chord * (inner_segment.fuel_tank.percent_chord_end_location -inner_segment.fuel_tank.percent_chord_start_location)  

    outer_front_rib_yu,outer_rear_rib_yu,outer_front_rib_yl,outer_rear_rib_yl = compute_non_dimensional_rib_coordinates(outer_segment)
    outer_segment_chord     = wing.chords.root * outer_segment.root_chord_percent
    outer_front_rib_length  = outer_segment_chord * (abs(outer_front_rib_yu) + abs(outer_front_rib_yl) )
    outer_rear_rib_length   = outer_segment_chord * (abs(outer_rear_rib_yu) + abs(outer_rear_rib_yl) )
    outer_wingbox_length    = outer_segment_chord * (outer_segment.fuel_tank.percent_chord_end_location -outer_segment.fuel_tank.percent_chord_start_location)  

    # volume of truncated prism
    A_1 = inner_wingbox_length * (inner_front_rib_length + inner_rear_rib_length) / 2 
    A_2 = outer_wingbox_length * (outer_front_rib_length + outer_rear_rib_length) / 2
    h   =  (outer_segment.percent_span_location -  inner_segment.percent_span_location) *  wing.spans.projected /2    # assumes wing is symmetric
    volume = (1 /3) * ( A_1 + A_2 + np.sqrt(A_1*A_2)) *h

    if wing.symmetric:
        volume *= 2    

    return volume

def compute_non_dimensional_rib_coordinates(compoment): 
    if compoment.airfoil != None: 
        if type(compoment.airfoil) == RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil:
            geometry = compute_naca_4series(compoment.airfoil.NACA_4_Series_code)
        elif type(compoment.airfoil) == RCAIDE.Library.Components.Airfoils.Airfoil: 
            geometry = import_airfoil_geometry(compoment.airfoil.coordinate_file)
    else:
        geometry = compute_naca_4series('0012')

    clearance = 1.5E-2
    front_rib_nondim_x       = compoment.fuel_tank.percent_chord_start_location   
    rear_rib_nondim_x        = compoment.fuel_tank.percent_chord_end_location 
    f_upper = interp1d(geometry.x_upper_surface  ,geometry.y_upper_surface, kind='linear')
    f_lower = interp1d(geometry.x_lower_surface  , geometry.y_lower_surface, kind='linear')

    # non-wing box dimension coordinates 
    front_rib_nondim_y_upper = f_upper([front_rib_nondim_x])[0] - clearance
    rear_rib_nondim_y_upper  = f_upper([rear_rib_nondim_x])[0]  - clearance   
    front_rib_nondim_y_lower = f_lower([front_rib_nondim_x])[0] + clearance   
    rear_rib_nondim_y_lower  = f_lower([rear_rib_nondim_x])[0]  + clearance   

    return front_rib_nondim_y_upper,rear_rib_nondim_y_upper, front_rib_nondim_y_lower, rear_rib_nondim_y_lower 

def compute_largest_circle(x_points,z_upper,z_lower):

    coords = list(zip(x_points, z_upper)) + list(zip(x_points[::-1], z_lower[::-1]))
    poly   = Polygon(coords)

    #scan a fine grid inside the polygon’s bounding box to find the best center
    minx, minz, maxx, maxz = poly.bounds
    nx, nz = 200, 200  
    xs = np.linspace(minx, maxx, nx)
    zs = np.linspace(minz, maxz, nz)

    best_r = 0.0
    best_pt = None

    for x in xs:
        for z in zs:
            p = Point(x, z)
            if not poly.contains(p):
                continue
            # the radius is limited by the closest polygon edge
            r = p.distance(poly.exterior)
            if r > best_r:
                best_r = r
                best_pt = (x, z)

    # 3) report the result
    max_diameter = 2 * best_r

    circle_center = (best_pt[0], best_pt[1])
    circle_radius = max_diameter / 2
    # Delete Later
    print(f"Largest inscribed circle diameter ≈ {max_diameter:.4f}")
    print(f" Center at x={best_pt[0]:.3f}, z={best_pt[1]:.3f}")
    # # Plotting
    # fig, ax = plt.subplots()
    # ax.plot(x_points, z_upper, label='Upper Surface')
    # ax.plot(x_points, z_lower, label='Lower Surface')

    # # Draw the inscribed circle
    # circle = plt.Circle(circle_center, circle_radius, fill=False)
    # ax.add_patch(circle)

    # ax.set_aspect('equal', 'box')
    # ax.set_xlabel("x")
    # ax.set_ylabel("z")
    # ax.legend()
    # plt.show()

    return max_diameter , best_pt[0],best_pt[1]


