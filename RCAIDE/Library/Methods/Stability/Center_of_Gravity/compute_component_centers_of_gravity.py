# RCAIDE/Methods/Stability/Center_of_Gravity/compute_component_centers_of_gravity.py
# Copyright 2023 Aerospace Research Community LLC
# 
# Created: Dec 2023, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
import RCAIDE
from RCAIDE.Library.Methods.Geometry.Planform import compute_span_location_from_chord_length
from RCAIDE.Library.Methods.Geometry.Planform import compute_chord_length_from_span_location
from RCAIDE.Library.Methods.Geometry.Planform import convert_sweep
from RCAIDE.Framework.Components import  Component

# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Computer Aircraft Center of Gravity
# ----------------------------------------------------------------------------------------------------------------------  
def compute_component_centers_of_gravity(vehicle, nose_load = 0.06):
    """ computes the center of gravity of all of the vehicle components based on correlations. 

    Assumptions:
        None

    Source:
        Stanford University AA241 Lecture Notes 

    Args:
        vehicle    (dict): aircraft data structure [-]
        nose_load (float): aircraft nose load factor 

    Returns:
        None 
    """  
    
    Comp =  RCAIDE.Library.Components
    
    # Wings 
    for wing in vehicle.wings: 
        if wing.sweeps.leading_edge == None:
            wing.sweeps.leading_edge = convert_sweep(wing,old_ref_chord_fraction = 0.25 ,new_ref_chord_fraction = 0.0) 
        if isinstance(wing,Comp.Wings.Main_Wing):
                wing.mass_properties.center_of_gravity[0][0] = .05*wing.chords.mean_aerodynamic +wing.aerodynamic_center[0]   
        elif isinstance(wing,Comp.Wings.Horizontal_Tail):
            chord_length_h_tail_35_percent_semi_span  = compute_chord_length_from_span_location(wing,.35*wing.spans.projected*.5)
            h_tail_35_percent_semi_span_offset        = np.tan(wing.sweeps.quarter_chord)*.35*.5*wing.spans.projected   
            wing.mass_properties.center_of_gravity[0][0] = .3*chord_length_h_tail_35_percent_semi_span + \
                                                                          h_tail_35_percent_semi_span_offset             
        elif isinstance(wing,Comp.Wings.Vertical_Tail):
            chord_length_v_tail_35_percent_semi_span  = compute_chord_length_from_span_location(wing,.35*wing.spans.projected)
            v_tail_35_percent_semi_span_offset        = np.tan(wing.sweeps.quarter_chord)*.35*.5*wing.spans.projected
            wing.mass_properties.center_of_gravity[0][0] = .3*chord_length_v_tail_35_percent_semi_span + \
                                                                        v_tail_35_percent_semi_span_offset
        else:
            span_location_mac = compute_span_location_from_chord_length(wing, wing.chords.mean_aerodynamic)
            mac_le_offset     = np.tan(wing.sweeps.leading_edge)*span_location_mac 
            wing.mass_properties.center_of_gravity[0][0] = .3*wing.chords.mean_aerodynamic + mac_le_offset
             
        
    # Fuselages 
    for fuselage in vehicle.fuselages:
        fuselage.mass_properties.center_of_gravity[0][0]   = .45*fuselage.lengths.total
        
    # Energy Networks 
    network_mass   = 0.
    network_moment = 0.
    for net in vehicle.networks:  
        for key,Comp in net.items():
            if isinstance(Comp,Component):
                network_moment += net[key].mass_properties.total * (np.sum(np.array(net[key].origin), axis=0) +
                                                                    net[key].mass_properties.center_of_gravity)
                network_mass   += net[key].mass_properties.total * len(net[key].origin)

    if network_mass!= 0.:
        propulsion_cg = network_moment/network_mass
    else:
        propulsion_cg = np.array([[0.,0.,0.]])
    
    
    # All remaining compoments 
    # First, select a length scale based on aircraft 
    length_scale = 1.
    nose_length  = 0. 
    if len(vehicle.fuselages) == 0.:
        for wing in vehicle.wings:
            if isinstance(wing,Comp.Wings.Main_Wing):
                b = wing.chords.root
                if b>length_scale:
                    nose_length  = 0.25*b
                    length_scale = b
    else:
        for fuselage in vehicle.fuselages:
            nose   = fuselage.lengths.nose
            length = fuselage.lengths.total
            if length > length_scale:
                nose_length  = nose
                length_scale = length
            
    # Passengers 
    try:  
        passengers                                                 = vehicle.payload.passengers
        passengers.origin[0][0]                                    = 0.51 * length_scale  
        passengers.mass_properties.center_of_gravity[0][0]         = 0.0
    except:
        pass 
    
    # Main Landing Gear 
    try:  
        main_gear                                                  = vehicle.landing_gear.main  
        moment_sans_main                                           = vehicle.center_of_gravity()[0][0]*(vehicle.sum_mass() - main_gear.mass_properties.total)
        main_gear_location                                         = moment_sans_main / (vehicle.mass_properties.takeoff - main_gear.mass_properties.total) / (1 - nose_load)
        main_gear.origin[0][0]                                     = main_gear_location
        main_gear.mass_properties.center_of_gravity                = 0.0 
    except:
        pass  

    # Nose Landing Gear 
    try:  
        nose_gear                                                  = vehicle.landing_gear.nose  
        nose_gear.origin[0][0]                                     = 0.25*nose_length
        nose_gear.mass_properties.center_of_gravity[0][0]          = 0.0   
    except:
        pass
    
    # Baggage 
    try:  
        baggage                                                    = vehicle.payload.baggage
        baggage.origin[0][0]                                       = 0.51 * length_scale  
        baggage.mass_properties.center_of_gravity[0][0]            = 0.0 
    except:
        pass         
    
    # Cargo
    try:  
        cargo                                                      = vehicle.payload.cargo
        cargo.origin[0][0]                                         = 0.51 * length_scale  
        cargo.mass_properties.center_of_gravity[0][0]              = 0.0    
        
    except:
        pass       
    
    # Avionics              
    try: 
        avionics                                                   = vehicle.systems.avionics
        avionics.origin[0][0]                                      = 0.4 * nose_length
        avionics.mass_properties.center_of_gravity[0][0]           = 0.0 
    except:
        pass
    
    # Furnishings 
    try:  
        furnishings                                                = vehicle.systems.furnishings
        furnishings.origin[0][0]                                   = 0.51 * length_scale
        furnishings.mass_properties.center_of_gravity[0][0]        = 0.0 
    except:
        pass     
    
    # APU
    try:   
        apu                                                        = vehicle.systems.apu 
        apu.origin[0][0]                                           = 0.9 * length_scale   
        apu.mass_properties.center_of_gravity[0][0]                = 0.0
    except:
        pass         
      
    # Air Conditioning 
    try:  
        air_conditioner                                            = vehicle.systems.air_conditioner
        air_conditioner.origin[0][0]                               = nose_length
        air_conditioner.mass_properties.center_of_gravity[0][0]    = 0.0 
    except:
        pass         
    
    # System
    try:  
        optionals                                                  = vehicle.systems.optionals 
        optionals.origin[0][0]                                     = 0.51 * length_scale  
        optionals.mass_properties.center_of_gravity[0][0]          = 0.0    
    except:
        pass         
    
    # Control Systems 
    try:  
        control_systems                                            = vehicle.systems.control_systems
        control_systems.origin[0][0]                               = vehicle.wings.main_wing.origin[0][0] 
        control_systems.mass_properties.center_of_gravity[0][0]    = vehicle.wings.main_wing.mass_properties.center_of_gravity[0][0] + \
            .1*vehicle.wings.main_wing.chords.mean_aerodynamic 
    except:
        pass         
    
    # Electrical Systems 
    try:   
        electrical_systems                                         = vehicle.systems.electrical_systems
        electrical_systems.origin[0][0]                            = .75*(.5*length_scale) + propulsion_cg[0][0]*.25
        electrical_systems.mass_properties.center_of_gravity[0][0] = 0.0 
    except:
        pass         
    
    # Hydraulics 
    try:  
        hydraulics                                                 = vehicle.systems.hydraulics
        hydraulics.origin[0][0]                                    = .75*(vehicle.wings.main_wing.origin[0][0] + wing.mass_properties.center_of_gravity[0][0]) + 0.25* length_scale*.95
        hydraulics.mass_properties.center_of_gravity[0][0]         = 0.0       
    except:
        pass     
    
    return 
    
