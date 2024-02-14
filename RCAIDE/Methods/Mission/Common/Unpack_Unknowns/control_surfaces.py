## @ingroup Methods-Missions-Common-Unpack_Unknowns
# RCAIDE/Methods/Missions/Common/Unpack_Unknowns/control_surfaces.py
# 
# 
# Created:  Jul 2023, M. Clarke
import RCAIDE

# ----------------------------------------------------------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Common-Unpack_Unknowns
def control_surfaces(segment,wings):
    # Elevator Control
    if segment.elevator_deflection_control.active:
        for wing in wings:
            for control_surface in wing.control_surfaces:
                if type(control_surface == RCAIDE.Components.Wings.Control_Surfaces.Elevator()):
                    num_elev_ctrls = len(segment.elevator_deflection_control.assigned_surfaces) 
                    for i in range(num_elev_ctrls):   
                        for j in range(len(segment.elevator_deflection_control.assigned_surfaces[i])): 
                            elevator_name = segment.elevator_deflection_control.assigned_surfaces[i][j]
                            control_surface[elevator_name].deflection = segment.state.unknowns["elevator_control_" + str(i)]    
                
    # Slat Control
    if segment.slat_deflection_control.active:
        for wing in wings:
            for control_surface in wing.control_surfaces:
                if type(control_surface == RCAIDE.Components.Wings.Control_Surfaces.Slat()):
                    num_slat_ctrls = len(segment.slat_deflection_control.assigned_surfaces) 
                    for i in range(num_slat_ctrls):   
                        for j in range(len(segment.slat_deflection_control.assigned_surfaces[i])): 
                            slat_name = segment.slat_deflection_control.assigned_surfaces[i][j]
                            control_surface[slat_name].deflection = segment.state.unknowns["slat_control_" + str(i)]  
            
                        
    # Slat Control
    if segment.flap_deflection_control.active:
        for wing in wings:
            for control_surface in wing.control_surfaces:
                if type(control_surface == RCAIDE.Components.Wings.Control_Surfaces.Flap()):
                    num_flap_ctrls = len(segment.flap_deflection_control.assigned_surfaces) 
                    for i in range(num_flap_ctrls):   
                        for j in range(len(segment.flap_deflection_control.assigned_surfaces[i])): 
                            flap_name = segment.flap_deflection_control.assigned_surfaces[i][j]
                            control_surface[flap_name].deflection = segment.state.unknowns["flap_control_" + str(i)]  
                                                    
    # Aileron Control
    if segment.aileron_deflection_control.active:
        for wing in wings:
            for control_surface in wing.control_surfaces:
                if type(control_surface == RCAIDE.Components.Wings.Control_Surfaces.Aileron()):
                    num_aile_ctrls = len(segment.aileron_deflection_control.assigned_surfaces) 
                    for i in range(num_aile_ctrls):   
                        for j in range(len(segment.aileron_deflection_control.assigned_surfaces[i])): 
                            aileron_name = segment.aileron_deflection_control.assigned_surfaces[i][j]
                            control_surface[aileron_name].deflection = segment.state.unknowns["aileron_control_" + str(i)]     
    
    return