# RCAIDE/Library/Missions/Segments/Climb/Constant_CAS_Constant_Rate.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE 
from RCAIDE.Framework.Mission.Functions.Common.Update.atmosphere import atmosphere
from RCAIDE.Framework.Core import Units

# Package imports  
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.
     Computed flight kinematics include: 
        conditions.frames.inertial.velocity_vector  [meters/second]
        conditions.frames.inertial.position_vector  [meters]
        conditions.freestream.altitude              [meters] 
    
    Assumptions:
       Constant CAS airspeed with a constant rate of climb

    Source:
       None

    Args:
       segment.climb_rate                                  [meters/second]
       segment.calibrated_air_speed                        [meters/second]
       segment.altitude_start                              [meters]
       segment.altitude_end                                [meters]
       segment.state.numerics.dimensionless.control_points [unitless]
       conditions.freestream.density                       [kilograms/meter^3]

    Returns:
       None

    """         
    
    # unpack
    climb_rate = segment.climb_rate
    CAS        = segment.calibrated_air_speed   
    alt0       = segment.altitude_start 
    altf       = segment.altitude_end
    beta       = segment.sideslip_angle
    t_nondim   = segment.state.numerics.dimensionless.control_points
    conditions = segment.state.conditions  

    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 * segment.state.initials.conditions.frames.inertial.position_vector[-1,2]

    # discretize on altitude
    alt = t_nondim * (altf-alt0) + alt0 

    if CAS is None:
        if not segment.state.initials: raise AttributeError('initial equivalent airspeed not set')
        v_mag =  np.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1,:])    
    else:  
        # determine airspeed from calibrated airspeed
        atmosphere(segment) # get density for airspeed
        density   = conditions.freestream.density[:,0]  
        pressure  = conditions.freestream.pressure[:,0]
        
        # compute sea level properties 
        MSL_data  = segment.analyses.atmosphere.compute_values(0.0,0.0) 
        pressure0 = MSL_data.pressure[0] 
        kCAS      = CAS / Units.knots
        delta     = pressure / pressure0  
        mach      = 2.236*((((1+4.575e-7*kCAS**2)**3.5-1)/delta + 1)**0.2857 - 1)**0.5 
        qc        = pressure * ((1+0.2*mach**2)**3.5 - 1)
        EAS       = CAS * (pressure/pressure0)**0.5*(((qc/pressure+1)**0.286-1)/((qc/pressure0+1)**0.286-1))**0.5 
        v_mag     = EAS/np.sqrt(density/MSL_data.density[0])    
    
    # process velocity vector 
    v_z   = -climb_rate  
    v_xy  = np.sqrt( v_mag**2 - v_z**2 )
    v_x   = np.cos(beta)*v_xy 
    v_y   = np.sin(beta)*v_xy 
    
    # pack conditions    
    conditions.frames.inertial.velocity_vector[:,0] = v_x
    conditions.frames.inertial.velocity_vector[:,1] = v_y
    conditions.frames.inertial.velocity_vector[:,2] = v_z
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0]  
    conditions.freestream.altitude[:,0]             = alt[:,0]  
    
    return 