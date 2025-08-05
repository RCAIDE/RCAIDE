# RCAIDE/Methods/Powertrain/Sources/Fuel_Tanks/compute_integral_tank_volume.py
# 
# 
# Created:  Jul 2023, M. Clarke
# Modified: Aug 2025, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports
import  RCAIDE
from RCAIDE.Framework.Mission.Common     import   Conditions
from RCAIDE.Library.Methods.Geometry.Airfoil import import_airfoil_geometry,  compute_naca_4series 

#Python Imports 
import numpy as np
from scipy.interpolate import interp1d

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ----------------------------------------------------------------------------------------------------------------------  


def compute_fuselage_integral_tank_fuel_volume(fuel_tank,fuselage):
    if len(fuselage.segments) > 1:
        seg_tags = list(fuselage.segments.keys())
        for i in range(len(seg_tags)-1):
            inner_segment = fuselage.segments[seg_tags[i]]
            outer_segment = fuselage.segments[seg_tags[i+1]]
            if inner_segment.has_fuel_tank == True: 
                # volume of truncated  
                A_1    = np.pi * inner_segment.height /2  *  inner_segment.width/2
                A_2    = np.pi * outer_segment.height/2  *  outer_segment.width/2
                h      = fuselage.lengths.total * (outer_segment.percent_x_location  - inner_segment.percent_x_location)
                volume = (1 /3) * ( A_1 + A_2 + np.sqrt(A_1*A_2)) *h
                fuel_tank.internal_volume = volume 
                fuel_tank.mass_properties.fuel                  = volume * fuel_tank.fuel.density  
                fuel_tank.mass_properties.center_of_gravity     = [[fuselage.lengths.total * (inner_segment.percent_x_location  + outer_segment.percent_x_location)/2 ,0,  (inner_segment.height  + outer_segment.height)/2]]
       
    return volume

def compute_wing_integral_tank_volume(fuel_tank,wing):

    if len(wing.segments) > 1:
        segment_tank_moment = np.array([0.0, 0.0, 0.0])
        seg_tags = list(wing.segments.keys())
        for i in range(len(seg_tags)-1):
            inner_segment = wing.segments[seg_tags[i]]
            outer_segment = wing.segments[seg_tags[i+1]]
            if inner_segment.has_fuel_tank == True:

                # get orgin of fuel tank     
                fuel_tank.origin = wing.origin 

                # compute volume of fuel in wing
                volume = compute_segmented_wing_integral_tank_fuel_volume(fuel_tank,wing,inner_segment,outer_segment)
                fuel_tank.internal_volume = volume 
                fuel_tank.mass_properties.fuel = volume * fuel_tank.fuel.density  

                fuel_tank.mass_properties.moments_of_inertia.tensor  += np.array(inner_segment.mass_properties.center_of_gravity)[0] * fuel_tank.mass_properties.fuel
                fuel_tank.mass_properties.center_of_gravity           = list(segment_tank_moment / fuel_tank.mass_properties.fuel)
    else: 
        # get orgin of fuel tank     
        fuel_tank.origin = wing.origin 

        # assume whole wing has fuel 
        volume = compute_wing_integral_tank_fuel_volume(fuel_tank,wing)                         
        fuel_tank.internal_volume = volume
        
        fuel_tank.mass_properties.fuel                  = volume * fuel_tank.fuel.density  
        fuel_tank.mass_properties.center_of_gravity     = wing.aerodynamic_center  
    
    return volume



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