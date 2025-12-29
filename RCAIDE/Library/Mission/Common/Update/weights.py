# RCAIDE/Library/Missions/Common/Update/weights.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 
import RCAIDE

# package imports 
import numpy as np  
    
# ----------------------------------------------------------------------------------------------------------------------
# Update Weights
# ----------------------------------------------------------------------------------------------------------------------  
def weights(segment): 
    """ Updates the weight of the vehicle 
        
        Assumptions:
        N/A
        
        Inputs:
             segment.state.
                 numerics.time.integrate               [-]
                 conditions.weights.vehicle.mass         [kg]
                 conditions.weights.vehicle.mass_rate  [kg/s]
                 conditions.freestream.gravity         [m/s^2]

                 
        Outputs: 
            segment.state.conditions.
                 weights.vehicle.mass
                 frames.inertial.gravity_force_vector
      
        Properties Used:
        N/A
                    
    """ 
    
    # unpack
    conditions     = segment.state.conditions
    I              = segment.state.numerics.time.integrate
    N              = segment.state.numerics.number_of_control_points 
    m_0_vehicle    = conditions.weights.vehicle.mass[0,0]
    m_dot_vehicle  = conditions.weights.vehicle.mass_rate
    g              = conditions.freestream.gravity
    vehicle        = segment.analyses.vehicle

 
    # --------------------------------------------------------------------------       
    # update mass 
    # --------------------------------------------------------------------------       
    if (type(segment) == RCAIDE.Framework.Mission.Segments.Single_Point.Set_Speed_Set_Altitude) or\
                    (type(segment) == RCAIDE.Framework.Mission.Segments.Single_Point.Set_Speed_Set_Altitude_AVL_Trimmed) or \
                    (type(segment) == RCAIDE.Framework.Mission.Segments.Single_Point.Set_Speed_Set_Altitude_No_Propulsion) or \
                    (type(segment) == RCAIDE.Framework.Mission.Segments.Single_Point.Set_Speed_Set_Throttle): 
        
        W = m_0_vehicle*g 
        conditions.frames.inertial.gravity_force_vector[:,2] = W[:,0]
        
    else:
        
        m = m_0_vehicle + np.dot(I, -m_dot_vehicle)
    
        # weight
        W = m*g
        
        # pack
        conditions.weights.vehicle.mass[1:,0]                = m[1:,0]  
        conditions.frames.inertial.gravity_force_vector[:,2] = W[:,0]
        
        # --------------------------------------------------------------------------       
        # update center of gravity
        # -------------------------------------------------------------------------- 
        Mom_tot   = np.zeros((N,3))
        Mass_tot  = np.zeros((N,1))
        for item in segment.conditions.weights.components.mass.keys():
            Mass_tot += segment.conditions.weights.components.mass[item]
            Mom_tot  += segment.conditions.weights.components.global_center_of_gravity[item] * segment.conditions.weights.components.mass[item]
            
        # update vehicle CG 
        segment.conditions.weights.vehicle.center_of_gravity = Mom_tot / Mass_tot

        # --------------------------------------------------------------------------       
        # update moment of gravity
        # --------------------------------------------------------------------------
        # update fuel MOI 
        for network in vehicle.networks:
            for fuel_line in network.fuel_lines:
                for fuel_tank in fuel_line.fuel_tanks: 
                    m_fuel_loss      = np.dot(I, -m_dot_vehicle) * fuel_tank.fuel_selector_ratio
                    fuel_tag         = fuel_tank.fuel.tag                     
                    M_fuel           = segment.conditions.weights.components.mass[fuel_tag][0,0]  +  m_fuel_loss
                    fuel_origin      = fuel_tank.fuel.origin
                    MOI_fuel_non_dim = fuel_tank.fuel.mass_properties.moments_of_inertia.non_dimensional_tensor
                                        
                    # compute moment of intertia of fuel in fuel tank
                    s                = segment.conditions.weights.vehicle.center_of_gravity - np.array(fuel_origin) # Vector for the parallel axis theorem
                    I_fuel           = M_fuel[:,:,None] * np.array(MOI_fuel_non_dim)[None,:,:]  # SAI AND AIDAN NEED TO FIX THIS LAST PART + M_fuel[:,:,None] * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - np.outer(s, s))                    
                    
                    
                    # update data strutures where masses and MOIs are stored 
                    segment.conditions.weights.components.mass[fuel_tag]                        = M_fuel
                    segment.conditions.weights.components.moments_of_inertia_Ixx[fuel_tag][:,0] = I_fuel[:,0,0]
                    segment.conditions.weights.components.moments_of_inertia_Ixy[fuel_tag][:,0] = I_fuel[:,0,1]
                    segment.conditions.weights.components.moments_of_inertia_Ixz[fuel_tag][:,0] = I_fuel[:,0,2]
                    segment.conditions.weights.components.moments_of_inertia_Iyx[fuel_tag][:,0] = I_fuel[:,1,0]
                    segment.conditions.weights.components.moments_of_inertia_Iyy[fuel_tag][:,0] = I_fuel[:,1,1]
                    segment.conditions.weights.components.moments_of_inertia_Iyz[fuel_tag][:,0] = I_fuel[:,1,2]
                    segment.conditions.weights.components.moments_of_inertia_Izx[fuel_tag][:,0] = I_fuel[:,2,0]
                    segment.conditions.weights.components.moments_of_inertia_Izy[fuel_tag][:,0] = I_fuel[:,2,1]
                    segment.conditions.weights.components.moments_of_inertia_Izz[fuel_tag][:,0] = I_fuel[:,2,2]    
        
      
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
        for item in segment.conditions.weights.components.mass.keys():
            Mass_tot += segment.conditions.weights.components.mass[item] 
            MOI_Ixx  += segment.conditions.weights.components.moments_of_inertia_Ixx[item]
            MOI_Ixy  += segment.conditions.weights.components.moments_of_inertia_Ixy[item]
            MOI_Ixz  += segment.conditions.weights.components.moments_of_inertia_Ixz[item]
            MOI_Iyx  += segment.conditions.weights.components.moments_of_inertia_Iyx[item]
            MOI_Iyy  += segment.conditions.weights.components.moments_of_inertia_Iyy[item]
            MOI_Iyz  += segment.conditions.weights.components.moments_of_inertia_Iyz[item]
            MOI_Izx  += segment.conditions.weights.components.moments_of_inertia_Izx[item]
            MOI_Izy  += segment.conditions.weights.components.moments_of_inertia_Izy[item]
            MOI_Izz  += segment.conditions.weights.components.moments_of_inertia_Izz[item] 
            
             
        # update vehicle MOI
        segment.conditions.weights.vehicle.moments_of_inertia_Ixx = MOI_Ixx
        segment.conditions.weights.vehicle.moments_of_inertia_Ixy = MOI_Ixy
        segment.conditions.weights.vehicle.moments_of_inertia_Ixz = MOI_Ixz
        segment.conditions.weights.vehicle.moments_of_inertia_Iyx = MOI_Iyx
        segment.conditions.weights.vehicle.moments_of_inertia_Iyy = MOI_Iyy
        segment.conditions.weights.vehicle.moments_of_inertia_Iyz = MOI_Iyz
        segment.conditions.weights.vehicle.moments_of_inertia_Izx = MOI_Izx
        segment.conditions.weights.vehicle.moments_of_inertia_Izy = MOI_Izy
        segment.conditions.weights.vehicle.moments_of_inertia_Izz = MOI_Izz 
                
    return
 