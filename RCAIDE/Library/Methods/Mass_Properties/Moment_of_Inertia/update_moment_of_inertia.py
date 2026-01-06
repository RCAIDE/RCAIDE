# RCAIDE/Library/Methods/Stability/Common/update_moment_of_inertia.py
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports     

# package imports
import numpy   as np 

# ----------------------------------------------------------------------------------------------------------------------
#  update_moment_of_inertia
# ---------------------------------------------------------------------------------------------------------------------- 
def update_moment_of_inertia(state,vehicle):
    """
    Updates the vehicle center of gravity accounting for fuel consumption during flight.

    Parameters
    ----------
    vehicle : RCAIDE.Library.Components.Vehicle
        Vehicle object containing all components and fuel systems
            - networks : list
                List of propulsion networks
            - fuel_lines : list
                List of fuel lines within each network
            - fuel_tanks : list
                List of fuel tanks within each fuel line
                    - fuel : RCAIDE.Library.Components.Energy.Storages.Fuel
                        Fuel component with mass properties
                            - mass_properties : Data
                                - mass : float
                                    Current fuel mass [kg]
                                - center_of_gravity : list
                                    Fuel tank center of gravity [m]
                            - origin : list
                                Fuel tank origin location [m]
    conditions : RCAIDE.Framework.Core.Data
        Flight conditions and state data
            - aerodynamics : Data
                - angles : Data
                    - alpha : float
                        Angle of attack [radians]
            - energy : Data
                - fuel_lines : dict
                    Dictionary of fuel line results
                        - fuel_tanks : dict
                            Dictionary of fuel tank results
                                - fuel_mass : float
                                    Current fuel mass [kg]

    Returns
    -------
    CG : numpy.ndarray
        Updated moment of intertia tensor variables
        Shape: (1, N) where N is the number of flight conditions

    Notes
    -----
    This function calculates the moment of inertia of the vehicle by
    accounting for fuel consumption during flight.  
    
    **Major Assumptions**
        * Fuel tank locations and orientations remain constant
        * No fuel sloshing or redistribution effects
        * Vehicle structure mass remains constant
        * Fuel density is constant 
 
    """
    
    # unoack
    conditions     = state.conditions
    N              = state.numerics.number_of_control_points  
    I              = state.numerics.time.integrate
    m_dot_vehicle  = conditions.weights.vehicle.mass_rate 

    # --------------------------------------------------------------------------       
    # update moment of gravity
    # --------------------------------------------------------------------------
    # update fuel MOI 
    for network in vehicle.networks:
        for fuel_line in network.fuel_lines:
            for fuel_tank in fuel_line.fuel_tanks: 
                m_fuel_loss      = np.dot(I, -m_dot_vehicle) * fuel_tank.fuel_selector_ratio
                fuel_tag         = fuel_tank.fuel.tag                     
                M_fuel           = conditions.weights.components.mass[fuel_tag][0,0]  +  m_fuel_loss
                fuel_origin      = fuel_tank.fuel.origin
                MOI_fuel_non_dim = fuel_tank.fuel.mass_properties.moments_of_inertia.non_dimensional_tensor
                I_fuel = np.zeros([len(conditions.weights.vehicle.center_of_gravity), 3, 3])             
                # compute moment of intertia of fuel in fuel tank
                for i in range(len(conditions.weights.vehicle.center_of_gravity)):  
                    s                = conditions.weights.vehicle.center_of_gravity[i] - np.array(fuel_origin) # Vector for the parallel axis theorem
                    I_fuel[i]           = M_fuel[i] * np.array(MOI_fuel_non_dim)[None,:,:]  
                    I_fuel[i]           = I_fuel[i] + M_fuel[i] * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - np.outer(s, s))             
                
                
                # update data strutures where masses and MOIs are stored 
                conditions.weights.components.mass[fuel_tag]                        = M_fuel
                conditions.weights.components.moments_of_inertia_Ixx[fuel_tag][:,0] = I_fuel[:,0,0]
                conditions.weights.components.moments_of_inertia_Ixy[fuel_tag][:,0] = I_fuel[:,0,1]
                conditions.weights.components.moments_of_inertia_Ixz[fuel_tag][:,0] = I_fuel[:,0,2]
                conditions.weights.components.moments_of_inertia_Iyx[fuel_tag][:,0] = I_fuel[:,1,0]
                conditions.weights.components.moments_of_inertia_Iyy[fuel_tag][:,0] = I_fuel[:,1,1]
                conditions.weights.components.moments_of_inertia_Iyz[fuel_tag][:,0] = I_fuel[:,1,2]
                conditions.weights.components.moments_of_inertia_Izx[fuel_tag][:,0] = I_fuel[:,2,0]
                conditions.weights.components.moments_of_inertia_Izy[fuel_tag][:,0] = I_fuel[:,2,1]
                conditions.weights.components.moments_of_inertia_Izz[fuel_tag][:,0] = I_fuel[:,2,2]    
    
  
    # update aircraft MOI
    MOI_Ixx   = np.zeros((N,1))
    MOI_Ixy   = np.zeros((N,1))
    MOI_Ixz   = np.zeros((N,1))
    MOI_Iyx   = np.zeros((N,1))
    MOI_Iyy   = np.zeros((N,1))
    MOI_Iyz   = np.zeros((N,1))
    MOI_Izx   = np.zeros((N,1))
    MOI_Izy   = np.zeros((N,1))
    MOI_Izz   = np.zeros((N,1))
    for item in conditions.weights.components.mass.keys():
        MOI_Ixx  += conditions.weights.components.moments_of_inertia_Ixx[item]
        MOI_Ixy  += conditions.weights.components.moments_of_inertia_Ixy[item]
        MOI_Ixz  += conditions.weights.components.moments_of_inertia_Ixz[item]
        MOI_Iyx  += conditions.weights.components.moments_of_inertia_Iyx[item]
        MOI_Iyy  += conditions.weights.components.moments_of_inertia_Iyy[item]
        MOI_Iyz  += conditions.weights.components.moments_of_inertia_Iyz[item]
        MOI_Izx  += conditions.weights.components.moments_of_inertia_Izx[item]
        MOI_Izy  += conditions.weights.components.moments_of_inertia_Izy[item]
        MOI_Izz  += conditions.weights.components.moments_of_inertia_Izz[item] 
        
         
    # update vehicle MOI
    conditions.weights.vehicle.moments_of_inertia_Ixx = MOI_Ixx
    conditions.weights.vehicle.moments_of_inertia_Ixy = MOI_Ixy
    conditions.weights.vehicle.moments_of_inertia_Ixz = MOI_Ixz
    conditions.weights.vehicle.moments_of_inertia_Iyx = MOI_Iyx
    conditions.weights.vehicle.moments_of_inertia_Iyy = MOI_Iyy
    conditions.weights.vehicle.moments_of_inertia_Iyz = MOI_Iyz
    conditions.weights.vehicle.moments_of_inertia_Izx = MOI_Izx
    conditions.weights.vehicle.moments_of_inertia_Izy = MOI_Izy
    conditions.weights.vehicle.moments_of_inertia_Izz = MOI_Izz
    
    return 
    
    
    ## --------------------------------------------------------------------------
    ## unpack 
    ## --------------------------------------------------------------------------
    #AoA           = conditions.aerodynamics.angles.alpha  

    ## --------------------------------------------------------------------------       
    ## update center of gravity 
    ## --------------------------------------------------------------------------
    ## create aircraft copy without fuel mass 
    #vehicle_no_fuel =  deepcopy(vehicle)
    #for network in vehicle_no_fuel.networks: 
        #for fuel_line in network.fuel_lines:   
            #for fuel_tank in fuel_line.fuel_tanks: 
                #fuel_tank.fuel.mass_properties.mass = 0.0
    
    ## run c.g. function to get total mass  and moment without updating C.G.
    #_ , Mom_0, Mass_0 = compute_vehicle_center_of_gravity(vehicle_no_fuel, update_center_of_gravity= False) 
    
    ## determine original fuel mass and moment and remove it from total mass and moment
    #Mom_fuel = np.array([[0.0, 0.0, 0.0]])
    #M_fuel   = np.zeros_like(AoA)
    #for network in vehicle.networks: 
        #for fuel_line in network.fuel_lines:  
            #fuel_line_results   = conditions.energy.fuel_lines[fuel_line.tag]
            #for fuel_tank in fuel_line.fuel_tanks: 
                #m_fuel        = fuel_line_results.fuel_tanks[fuel_tank.tag].fuel_mass[0] 
                #global_cg_loc = np.array(fuel_tank.fuel.mass_properties.center_of_gravity) + np.array(fuel_tank.fuel.origin)  
                #M_fuel        += m_fuel
                #Mom_fuel      += np.multiply(m_fuel, global_cg_loc)               
    
    ## recompute mass and moment of fuel
    #Mom_aircraft = Mom_0 + Mom_fuel
    #M_aircraft   = Mass_0 + M_fuel
        
    ## compute updated C.G. 
    #CG = np.atleast_2d(Mom_aircraft[:, 0]).T / M_aircraft
    
    #return CG