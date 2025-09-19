# RCAIDE/Library/Methods/Stability/Vortex_Lattice_Method/evaluate_VLM.py
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports   
from RCAIDE.Framework.Core     import Data   
from RCAIDE.Library.Methods.Mass_Properties.Center_of_Gravity     import compute_vehicle_center_of_gravity

# package imports
import numpy   as np
from copy      import  deepcopy 

# ----------------------------------------------------------------------------------------------------------------------
#  Vortex_Lattice
# ---------------------------------------------------------------------------------------------------------------------- 
def update_center_of_gravity(vehicle, conditions):
    # --------------------------------------------------------------------------
    # unpack 
    # --------------------------------------------------------------------------
    AoA           = conditions.aerodynamics.angles.alpha  

    # --------------------------------------------------------------------------       
    # update center of gravity 
    # --------------------------------------------------------------------------
    # create aircraft copy without fuel mass 
    vehicle_no_fuel =  deepcopy(vehicle)
    for network in vehicle_no_fuel.networks: 
        for fuel_line in network.fuel_lines:   
            for fuel_tank in fuel_line.fuel_tanks: 
                fuel_tank.fuel.mass_properties.mass = 0.0
    
    # run c.g. function to get total mass  and moment without updating C.G.
    _ , Mom_0, Mass_0 = compute_vehicle_center_of_gravity(vehicle_no_fuel, update_center_of_gravity= False) 
    
    # determine original fuel mass and moment and remove it from total mass and moment
    Mom_fuel = np.array([[0.0, 0.0, 0.0]])
    M_fuel   = np.zeros_like(AoA)
    for network in vehicle.networks: 
        for fuel_line in network.fuel_lines:  
            fuel_line_results   = conditions.energy.fuel_lines[fuel_line.tag]
            for fuel_tank in fuel_line.fuel_tanks: 
                m_fuel        = fuel_line_results.fuel_tanks[fuel_tank.tag].fuel_mass 
                global_cg_loc = np.array(fuel_tank.fuel.mass_properties.center_of_gravity) + np.array(fuel_tank.fuel.origin)  
                M_fuel        += m_fuel
                Mom_fuel      += np.multiply(m_fuel[:, 0], global_cg_loc)               
    
    # recompute mass and moment of fuel
    Mom_aircraft = Mom_0 + Mom_fuel
    M_aircraft   = Mass_0 + M_fuel
        
    # compute updated C.G. 
    CG = np.atleast_2d(Mom_aircraft[:, 0]).T / M_aircraft
    
    return CG