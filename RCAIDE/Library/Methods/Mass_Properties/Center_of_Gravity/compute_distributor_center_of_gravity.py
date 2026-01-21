# RCAIDE/Library/Methods/Mass_Properties/Center_of_Gravity/compute_distributor_center_of_gravity.py 
# 
# Created:  Dec 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE
from RCAIDE.Library.Components   import Component

# # package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Distributor Center of Gravity
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_distributor_center_of_gravity(component,vehicle, length=0):
    """
    Compute the center of gravity of a distributor
    
    Assumptions
    ___________
         - Lines line on y-z plane (i.e. C.G.z is 0)
         - Interates through all compoments on the distribution lines and computes the manhattan distance
         - Redundancy accounted from the fact that each component is routed to all compoments (i.e. bi-directional)
         
       .-------------.
       | compoment i |---<-- line 1 ->----|
       '-------------'                    |
                                          ^
                                          |
                                       line 3
                                          |
                                          V
              .------------.              |      
              | compoment j|-<- line 2 ->-|
              '------------'              |
                                          
                                          
     """
     
    insulation_rm_density = component.insulation.rigid_material.density
    insulation_fm_density = component.insulation.flexible_material.density
    insulation_fm_ratio   = component.insulation.flexible_material_ratio  
    pipe_rm_density       = component.pipe.rigid_material.density        
    pipe_fm_density       = component.pipe.flexible_material.density   
    pipe_fm_ratio         = component.pipe.flexible_material_ratio  
    
    insulation_cross_sectional_area = (np.pi / 4) *  (component.insulation.diameters.external ** 2 -   component.insulation.diameters.internal** 2)
    pipe_cross_sectional_area       = (np.pi / 4) *  (component.pipe.diameters.external ** 2 -   component.pipe.diameters.internal** 2)
    
    c_list  =  []
    c_symm  =  []
    c_locs  = np.empty((0,3)) 

    length        = 0
    total_mass    = 0
    total_moment  = 0  
    
    for network in  vehicle.networks: 
        for propulsor in network.propulsors:
            c_list.append(propulsor.tag)
            c_symm.append(propulsor.xz_plane_symmetric) 
            c_loc  = np.array(propulsor.origin) + np.array(propulsor.mass_properties.center_of_gravity)
            c_locs =  np.concatenate((c_locs,c_loc), axis=0)
        
        for fuel_line in network.fuel_lines: 
            for tag, item in fuel_line.items():
                if isinstance(item,RCAIDE.Library.Components.Component): 
                    c_list.append(item.tag)
                    c_symm.append(item.xz_plane_symmetric)
                    c_loc  = np.array(item.origin) + np.array(item.mass_properties.center_of_gravity)
                    c_locs =  np.concatenate((c_locs,c_loc), axis=0) 
                if isinstance(item,Component.Container): 
                    for key in item.keys():
                        sub_item = item[key] 
                        if isinstance(sub_item,RCAIDE.Library.Components.Component): 
                            c_list.append(sub_item.tag)
                            c_symm.append(sub_item.xz_plane_symmetric)
                            c_loc  = np.array(sub_item.origin) + np.array(sub_item.mass_properties.center_of_gravity)
                            c_locs = np.concatenate((c_locs,c_loc), axis=0)                         
    
    num_c= len(c_list) 
    for i in range (num_c):
        for j in range(num_c): 
            if i == j:
                pass
            else: 
                # distributor distances 
                line_1_length             = abs(c_locs[i][1]) 
                line_1_centroid           = c_locs[i][0]
                line_2_length             = abs(c_locs[j][1])
                line_2_centroid           = c_locs[j][0]
                line_3_length             = abs(c_locs[i][0] - c_locs[j][0] )
                line_3_centroid           = (c_locs[j][0] + c_locs[i][0] )/2
                
                if insulation_cross_sectional_area == 0:
                    insulation_mass = 0
                    insulation_moment = 0
                else:
                    line_1_insulation_volume  = line_1_length *  insulation_cross_sectional_area
                    line_1_insulation_mass    = insulation_fm_ratio * (insulation_rm_density * line_1_insulation_volume) +  (1 - insulation_fm_ratio) * (insulation_fm_density * line_1_insulation_volume)
                    
                    line_2_insulation_volume  = line_2_length *  insulation_cross_sectional_area
                    line_2_insulation_mass    = insulation_fm_ratio * (insulation_rm_density * line_2_insulation_volume) +  (1 - insulation_fm_ratio) * (insulation_fm_density * line_2_insulation_volume)
                    
                    line_3_insulation_volume  = line_3_length *  insulation_cross_sectional_area
                    line_3_insulation_mass    = insulation_fm_ratio * (insulation_rm_density * line_3_insulation_volume) +  (1 - insulation_fm_ratio) * (insulation_fm_density * line_3_insulation_volume)
                    
                    insulation_mass = line_1_insulation_mass +  line_2_insulation_mass +  line_3_insulation_mass
                    
                    line_1_insulation_moment       = line_1_insulation_mass *line_1_centroid  
                    line_2_insulation_moment       = line_2_insulation_mass *line_2_centroid    
                    line_3_insulation_moment       = line_3_insulation_mass *line_3_centroid
                    
                    insulation_moment  = line_1_insulation_moment + line_2_insulation_moment +  line_3_insulation_moment 
                    
                
                if pipe_cross_sectional_area == 0:
                    pipe_mass = 0
                    pipe_moment = 0
                else:
                    line_1_pipe_volume        = line_1_length *  pipe_cross_sectional_area
                    line_1_pipe_mass          = pipe_fm_ratio * (pipe_rm_density * line_1_pipe_volume) +  (1 - pipe_fm_ratio) * (pipe_fm_density * line_1_pipe_volume)
                    
                    line_2_pipe_volume        = line_2_length *  pipe_cross_sectional_area
                    line_2_pipe_mass          = pipe_fm_ratio * (pipe_rm_density * line_2_pipe_volume) +  (1 - pipe_fm_ratio) * (pipe_fm_density * line_2_pipe_volume)
                    
                    line_3_pipe_volume        = line_3_length *  pipe_cross_sectional_area
                    line_3_pipe_mass          = pipe_fm_ratio * (pipe_rm_density * line_3_pipe_volume) +  (1 - pipe_fm_ratio) * (pipe_fm_density * line_3_pipe_volume)
                    
                    pipe_mass = line_1_pipe_mass +  line_2_pipe_mass +  line_3_pipe_mass
     
                    line_1_pipe_moment             = line_1_pipe_mass *line_1_centroid 
                    line_2_pipe_moment             = line_2_pipe_mass *line_2_centroid 
                    line_3_pipe_moment             = line_3_pipe_mass *line_3_centroid 
                    pipe_moment  = line_1_pipe_moment + line_2_pipe_moment +  line_3_pipe_moment 
                                         
                # assumulate all masses and  moments 
                length       += line_3_length +  line_2_length +  line_1_length
                total_mass   += insulation_mass + pipe_mass
                total_moment += pipe_moment + insulation_moment
    
    line_mass = total_mass * component.connector_weight_factor 
    if line_mass != 0.0: 
        c_g_line =  [[total_moment / total_mass, 0, 0]]
        component.mass_properties.center_of_gravity = c_g_line 
        component.mass_properties.mass              = line_mass
    
    return component.mass_properties.center_of_gravity