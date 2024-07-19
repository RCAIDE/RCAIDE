# RCAIDE/Methods/Aerodynamics/Common/Drag/parasite_drag_total.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
import RCAIDE
import numpy as np 
 
# package imports
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------  
#  Total Parasite Drag 
# ----------------------------------------------------------------------------------------------------------------------   
def parasite_total(state,settings,geometry):
    """Sums up the parasite drags from all compoments 

    Assumptions:
        None

    Source:
        None

    Args:
        state                                                (dict): flight conditions       [-]
        settings                                             (dict): analyses settings       [-]
        geometry                                             (dict): aircraft data stucture  [-]
        conditions.aerodynamics.coefficients.drag.
          parasite[wing.tag(s)].parasite_drag       (numpy.ndarray): wing parasite drags     [Unitless]
          parasite[fuselage.tag(s)].parasite_drag   (numpy.ndarray): fuselage parasite drags [Unitless]
          parasite[boom.tag(s)].parasite_drag       (numpy.ndarray): boom parasite drags     [Unitless]
          parasite[nacelle.tag(s)].parasite_drag    (numpy.ndarray): nacelle parasite drags  [Unitless]
          parasite[pylon.tag(s)].parasite_drag      (numpy.ndarray): pylon parasite drags    [Unitless]


    Returns:
        None 
    """ 
    # unpack
    conditions             = state.conditions 
    vehicle_reference_area = geometry.reference_area
    
    #compute parasite drag total
    total_parasite_drag = 0.0
    
    # renormalize parasite drag from wings using reference area of aircraft 
    for wing in geometry.wings:
        parasite_drag = conditions.aerodynamics.coefficients.drag.parasite[wing.tag].total 
        conditions.aerodynamics.coefficients.drag.parasite[wing.tag].total  = parasite_drag * wing.areas.reference/vehicle_reference_area
        total_parasite_drag += parasite_drag * wing.areas.reference/vehicle_reference_area
 
    # renormalize parasite drag from fuselages using reference area of aircraft 
    for fuselage in geometry.fuselages:
        if type(fuselage) == RCAIDE.Library.Components.Fuselages.Blended_Wing_Body_Fuselage:
            continue
        parasite_drag = conditions.aerodynamics.coefficients.drag.parasite[fuselage.tag].total 
        conditions.aerodynamics.coefficients.drag.parasite[fuselage.tag].total = parasite_drag * fuselage.areas.front_projected/vehicle_reference_area
        total_parasite_drag += parasite_drag * fuselage.areas.front_projected/vehicle_reference_area
    
    # renormalize parasite drag from nacelles and pylons using reference area of aircraft  
    for network in  geometry.networks: 
        if 'busses' in network:  
            for bus in network.busses:
                for propulsor in bus.propulsors:  
                    if 'nacelle' in propulsor:
                        nacelle       =  propulsor.nacelle 
                        ref_area      = nacelle.diameter**2 / 4 * np.pi
                        parasite_drag = conditions.aerodynamics.coefficients.drag.parasite[nacelle.tag].total 
                        conditions.aerodynamics.coefficients.drag.parasite[nacelle.tag].total  = parasite_drag * ref_area/vehicle_reference_area
                        total_parasite_drag += parasite_drag * ref_area/vehicle_reference_area 
                            
                        if nacelle.has_pylon:
                            parasite_drag = conditions.aerodynamics.coefficients.drag.parasite[nacelle.tag + '_pylon'].total 
                            conditions.aerodynamics.coefficients.drag.parasite[nacelle.tag + '_pylon'].total = parasite_drag * fuselage.areas.front_projected/vehicle_reference_area
                            total_parasite_drag += parasite_drag * ref_area/vehicle_reference_area 
     
        if 'fuel_lines' in network:  
            for fuel_line in network.fuel_lines:
                for propulsor in fuel_line.propulsors:  
                    if 'nacelle' in propulsor: 
                        nacelle       =  propulsor.nacelle 
                        ref_area      = nacelle.diameter**2 / 4 * np.pi
                        parasite_drag = conditions.aerodynamics.coefficients.drag.parasite[nacelle.tag].total 
                        conditions.aerodynamics.coefficients.drag.parasite[nacelle.tag].total  = parasite_drag * ref_area/vehicle_reference_area
                        total_parasite_drag += parasite_drag * ref_area/vehicle_reference_area 
                            
                        if nacelle.has_pylon:
                            parasite_drag = conditions.aerodynamics.coefficients.drag.parasite[nacelle.tag + '_pylon'].total 
                            conditions.aerodynamics.coefficients.drag.parasite[nacelle.tag + '_pylon'].total = parasite_drag * fuselage.areas.front_projected/vehicle_reference_area
                            total_parasite_drag += parasite_drag * ref_area/vehicle_reference_area  
    
    state.conditions.aerodynamics.coefficients.drag.parasite.total = total_parasite_drag

    return 