# RCAIDE/Library/Methods/Mass_Properties/Center_of_Gravity/compute_wing_center_of_gravity.py 
# 
# Created:  Dec 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
import RCAIDE
from RCAIDE.Library.Methods.Geometry.Planform.compute_segment_volume   import compute_segment_volume
from RCAIDE.Library.Methods.Geometry.Planform.compute_segment_centroid import compute_segment_centroid

# package imports 
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Boom Center of Gravity
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_wing_center_of_gravity(component,vehicle): 
    if isinstance(component,RCAIDE.Library.Components.Powertrain.Sources.Fuel_Tanks.Integral_Tank):
        fuel_tank = component
        wing = vehicle.wings[fuel_tank.wing_tag]
        if len(wing.segments) == 0: 
            fuel_tank.fuel.mass_properties.center_of_gravity  = wing.mass_properties.center_of_gravity
        else:
            pass # already computed in RCAIDE/Methods/Powertrain/Sources/Fuel_Tanks/compute_integral_tank_volume.py
        
    else:
        wing     = component 
        sym      = wing.xz_plane_symmetric
        span     = wing.spans.projected  
        semispan = span/(1+sym) 
        vertical = wing.vertical
        if len(wing.segments) > 1:  
            seg_keys = list(wing.segments.keys())
            
            # estimate empty wing center of gravity
            total_moment = np.array([[0.0,0.0,0.0]])
            total_mass   = 0.0
            
            outer_wing_flag = False
            v_wing = 0
            for i in range(len(wing.segments)-1):
                # compute volume and assume unit density to get mass
                inner_segment = wing.segments[seg_keys[i]]
                outer_segment = wing.segments[seg_keys[i+1]]
                v_seg         = compute_segment_volume(wing,inner_segment,outer_segment)
                inner_segment.volume_properties.gross_volume = v_seg
                v_wing        += v_seg
                m_seg         = v_seg * 1
                if isinstance(wing, RCAIDE.Library.Components.Wings.Blended_Wing_Body):
                    if not isinstance(inner_segment, RCAIDE.Library.Components.Wings.Segments.Blended_Wing_Body_Fuselage_Segment):
                        outer_wing_flag = True
                    if outer_wing_flag:
                        total_moment += m_seg * np.array(inner_segment.mass_properties.center_of_gravity)
                        total_mass   += m_seg 
                else:
                    total_moment += m_seg * np.array(inner_segment.mass_properties.center_of_gravity)
                    total_mass   += m_seg 
                     
            cg_wing = total_moment / total_mass
            wing.volume_properties.gross_volume = v_wing
            
            if vertical:
                wing.mass_properties.center_of_gravity[0][0] = cg_wing[0][0]
                wing.mass_properties.center_of_gravity[0][1] = cg_wing[0][2] 
                wing.mass_properties.center_of_gravity[0][2] = 0 if sym ==True else cg_wing[0][1]
            
            else:
                wing.mass_properties.center_of_gravity[0][0] = cg_wing[0][0]
                wing.mass_properties.center_of_gravity[0][1] = 0 if sym ==True else cg_wing[0][1]
                wing.mass_properties.center_of_gravity[0][2] = cg_wing[0][2]
            
        else:  
            # update
            chord_root = wing.chords.root             
            chord_tip  = wing.chords.tip
            dihedral   = wing.dihedral
            taper      = wing.taper  
            le_sweep   = wing.sweeps.leading_edge        
    
            # estimate empty wing center of gravity        
            cg_wing   =  compute_segment_centroid(le_sweep,semispan,0,0,0,taper,dihedral,chord_root,chord_tip) 
            if vertical:
                wing.mass_properties.center_of_gravity[0][0] = cg_wing[0] 
                wing.mass_properties.center_of_gravity[0][1] = cg_wing[2]  
                wing.mass_properties.center_of_gravity[0][2] = 0 if sym ==True else cg_wing[1]
            else: 
                wing.mass_properties.center_of_gravity[0][0] = cg_wing[0] 
                wing.mass_properties.center_of_gravity[0][1] = 0 if sym ==True else cg_wing[1]
                wing.mass_properties.center_of_gravity[0][2] = cg_wing[2] 

    # # SAI& AIDAN : WE NEED TO REMOVE THE CODE BELOW
    if isinstance(wing, RCAIDE.Library.Components.Wings.Blended_Wing_Body): 
        wing.aft_center_body.origin = [[wing.chords.root - 2/3 * wing.aft_center_body.length,0,0]]    # IMPROVE HOW WE HANDLE THIS ASSUMPTION     
        wing.aft_center_body.tag    = 'aft_center_body'
        wing.center_body.origin     = [[0.5*(wing.chords.root - wing.aft_center_body.length),0,0]] # IMPROVE HOW WE HANDLE THIS ASSUMPTION    
        wing.center_body.tag        = 'center_body' 
        wing.center_body.mass_properties.mass += vehicle.mass_properties.weight_breakdown.empty.systems.furnishings +\
                                                 vehicle.mass_properties.weight_breakdown.empty.systems.air_conditioner +\
                                                  vehicle.mass_properties.weight_breakdown.operational_items.total  # NO SHOULD BE COMPONENTS   
   
       
    return wing.mass_properties.center_of_gravity