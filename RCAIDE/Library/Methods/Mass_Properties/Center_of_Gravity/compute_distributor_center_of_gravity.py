# RCAIDE/Library/Methods/Mass_Properties/Center_of_Gravity/compute_distributor_center_of_gravity.py 
# 
# Created:  Dec 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE 

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
     

    valve_unit_mass       = component.valve_unit_mass                      
    fuel_probe_unit_mass  = component.fuel_probe_unit_mass
    boost_pump_unit_mass  = component.boost_pump_unit_mass 
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

    total_line_length    = 0
    total_line_mass      = 0
    total_line_moment    = 0
    transfer_system_mass = 0 
     
    for network in  vehicle.networks: 
        for propulsor in network.propulsors:
            c_list.append(propulsor.tag)
            c_symm.append(propulsor.xz_plane_symmetric) 
            c_loc  = np.array(propulsor.origin) + np.array(propulsor.mass_properties.center_of_gravity)
            c_locs =  np.concatenate((c_locs,c_loc), axis=0)
        
        wing_tank_included = False
        aft_tank_included  = False
        for fuel_line in network.fuel_lines:
            for fuel_tank in fuel_line.fuel_tanks:
                if wing_tank_included == False:
                    c_list.append(fuel_tank.tag)
                    c_symm.append(fuel_tank.xz_plane_symmetric)
                    c_loc  = np.array(fuel_tank.origin) + np.array(fuel_tank.mass_properties.center_of_gravity)
                    c_locs =  np.concatenate((c_locs,c_loc), axis=0) 
                    wing_tank_included = True
                     
                if aft_tank_included == False and fuel_tank.bwb_aft_tank == True:
                    c_list.append(fuel_tank.tag)
                    c_symm.append(fuel_tank.xz_plane_symmetric)
                    c_loc  = np.array(fuel_tank.origin) + np.array(fuel_tank.mass_properties.center_of_gravity)
                    c_locs =  np.concatenate((c_locs,c_loc), axis=0)
                    aft_tank_included = True                    
    
    num_c= len(c_list) 
    for i in range(num_c):
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
                total_line_length      += line_3_length +  line_2_length +  line_1_length
                total_line_mass        += insulation_mass + pipe_mass
                transfer_system_mass   += insulation_mass + pipe_mass +  valve_unit_mass +  fuel_probe_unit_mass  +  boost_pump_unit_mass
                total_line_moment      += pipe_moment + insulation_moment
     
    transfer_system_mass += component.venting_system_mass 
    if total_line_mass != 0.0: 
        c_g_line =  [[total_line_moment / total_line_mass, 0, 0]]
        component.mass_properties.center_of_gravity = c_g_line 
        component.mass_properties.mass              = transfer_system_mass
    
    return component.mass_properties.center_of_gravity