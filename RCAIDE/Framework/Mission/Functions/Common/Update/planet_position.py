# RCAIDE/Library/Missions/Common/Update/planet_position.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core  import Units 

# package imports 
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Update Planet Position
# ----------------------------------------------------------------------------------------------------------------------
def planet_position(segment):
    """ Updates the location of the vehicle relative to the Planet throughout the mission
    
        Assumptions:
        This is valid for small movements and times as it does not account for the rotation of the Planet beneath the vehicle
        
        Args:
        segment.state.conditions:
            freestream.velocity                      [meters/second]
            freestream.altitude                      [meters]
            frames.body.inertial_rotations           [Radians]
        segment.analyses.planet.features.mean_radius [meters]
        segment.state.numerics.time.integrate        [float]
            
        Returns:
            segment.state.conditions:           
                frames.planet.latitude  [Radians]
                frames.planet.longitude [Radians] 
    """        
    
    # unpack
    conditions = segment.state.conditions
    
    # unpack orientations and velocities
    V          = conditions.freestream.velocity[:,0]
    altitude   = conditions.freestream.altitude[:,0] 
    theta      = conditions.frames.body.inertial_rotations[:,1]
    psi        = segment.true_course        # sign convetion is clockwise positive
    alpha      = conditions.aerodynamics.angles.alpha[:,0]
    I          = segment.state.numerics.time.integrate
    Re         = segment.analyses.planet.features.mean_radius  
         
    # The flight path and radius
    gamma     = theta - alpha
    R         = altitude + Re

    # Find the velocities and integrate the positions
    lamdadot  = (V/R)*np.cos(gamma)*np.cos(psi)
    lamda     = np.dot(I,lamdadot) / Units.deg # Latitude
    mudot     = (V/R)*np.cos(gamma)*np.sin(psi)/np.cos(lamda)
    mu        = np.dot(I,mudot) / Units.deg # Longitude

    # Reshape the size of the vectorss
    shape     = np.shape(conditions.freestream.velocity)
    mu        = np.reshape(mu,shape)
    lamda     = np.reshape(lamda,shape)
    phi       = np.array([[np.cos(psi),-np.sin(psi),0],[np.sin(psi),np.cos(psi),0],[0,0,1]])

    # Pack 
    lat                                           = conditions.frames.planet.latitude[0,0]
    lon                                           = conditions.frames.planet.longitude[0,0]
    conditions.frames.planet.latitude             = lat + lamda
    conditions.frames.planet.longitude            = lon + mu 
    conditions.frames.planet.true_course          = np.tile(phi[None,:,:],(len(V),1,1))    

    return 