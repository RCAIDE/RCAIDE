# RCAIDE/Library/Missions/Common/compute_point_to_point_geospatial_data.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
import RCAIDE
from RCAIDE.Framework.Core import Units, Data
from scipy.interpolate import griddata
import RNUMPY as rp
from geopy.distance import geodesic as GD

# ----------------------------------------------------------------------------------------------------------------------  
#  Compute Point to Point Geospacial Data
# ----------------------------------------------------------------------------------------------------------------------  
def compute_point_to_point_geospatial_data(topography_file                        = None,
                                            origin_tag                         = 'origin',
                                            destination_tag                       = 'destination',
                                            origin_coord_deg                 = [0.0,0.0],
                                            destination_coord_deg               = [0.0,0.0]):
    """This computes the absolute microphone/observer locations on a defined topography
            
    Assumptions: 
        topography_file is a text file obtained from https://topex.ucsd.edu/cgi-bin/get_data.cgi
    
    Source:
        None  

    Args:   
        topography_file                        - file of lattide, longitude and elevation points     
        origin_coord_deg                  - coordinates of origin location                                              [degrees]
        destination_coord_deg                - coordinates of destimation location                                            [degrees]  
        
    Returns:                                   
        latitude_longitude_micrphone_locations - latitude-longitude and elevation coordinates of all microphones in domain          [deg,deg,m]  
        flight_range                           - gound distance between origin and destination location                          [meters]              
        true_course                            - true course angle measured clockwise from true north                               [radians]
        origin tag           
        origin_location                     - cartesial coordinates of origin location relative to computational domain       [meters]                        
        origin_coord_deg                  - cartesial coordinates of origin location relative to computational domain       [meters]                                    
        destination_xyz_location                   - cartesial coordinates of destination location relative to computational domain [meters]    
    
           
    """     
    # convert cooordinates to array 
    origin_coord_deg      = rp.asarray(origin_coord_deg)
    destination_coord_deg = rp.asarray(destination_coord_deg)
    
    # extract data from file   
    data  = rp.loadtxt(topography_file)
    Long  = data[:,0]
    Lat   = data[:,1]
    Elev  = data[:,2]
    
    # get radius of earth
    earth = RCAIDE.Library.Attributes.Planets.Earth()
    R     = earth.mean_radius      
     
    # Compute distance between origin and destimation points
    origin_coord_rad      = origin_coord_deg*Units.degrees
    destination_coord_rad = destination_coord_deg*Units.degrees  
    angle                 = rp.arccos(rp.sin(origin_coord_rad[0])*rp.sin(destination_coord_rad[0]) + 
                           rp.cos(origin_coord_rad[0])*rp.cos(destination_coord_rad[0])*rp.cos(origin_coord_rad[1] - destination_coord_rad[1])) 

    # Compute heading from origin to destination    
    gamma = rp.arcsin( rp.sin(rp.pi/2 - destination_coord_rad[0])* rp.sin(destination_coord_rad[1] - origin_coord_rad[1])/rp.sin(angle)) 
    angle_vector   = destination_coord_deg - origin_coord_deg 
    if angle_vector[0] < 0:
        gamma = rp.pi - gamma  
 
    x_min_coord = rp.min(Lat)
    y_min_coord = rp.min(Long)
    ori_lat     = origin_coord_deg[0]
    ori_long    = origin_coord_deg[1]
    des_lat     = destination_coord_deg[0]
    des_long    = destination_coord_deg[1]
    if ori_long>180: 
        ori_long = ori_long-360
    if des_long>180:
        des_long = des_long-360  
    
    # compute location of origin and destimation 
    bottom_left_map_coords           = rp.array([x_min_coord,y_min_coord])  
    x0_coord                         = rp.array([ori_lat,y_min_coord])
    y0_coord                         = rp.array([x_min_coord,ori_long])
    x1_coord                         = rp.array([des_lat,y_min_coord])
    y1_coord                         = rp.array([x_min_coord,des_long])
    
    # get bounds of computational domain 
    x0                               = GD(x0_coord,bottom_left_map_coords).m 
    y0                               = GD(y0_coord,bottom_left_map_coords).m  
    x1                               = GD(x1_coord,bottom_left_map_coords).m 
    y1                               = GD(y1_coord,bottom_left_map_coords).m
    
    # compute topography data 
    lat_flag                         = rp.where(origin_coord_deg<0)[0]
    origin_coord_deg[lat_flag]       = origin_coord_deg[lat_flag] + 360 
    long_flag                        = rp.where(destination_coord_deg<0)[0]
    destination_coord_deg[long_flag] = destination_coord_deg[long_flag] + 360   
    z0                               = griddata((Lat,Long), Elev, (rp.array([origin_coord_deg[0]]),rp.array([origin_coord_deg[1]])), method='linear')[0]
    z1                               = griddata((Lat,Long), Elev, (rp.array([destination_coord_deg[0]]),rp.array([destination_coord_deg[1]])), method='linear')[0] 
    ori_location                     = rp.array([x0,y0,z0])
    des_location                     = rp.array([x1,y1,z1])
    
    # pack data 
    geospacial_data = Data( 
        flight_range            = R*angle,
        true_course             = gamma,
        origin_tag              = origin_tag,
        origin_coord_deg        = origin_coord_deg,
        origin_location         = ori_location,
        destination_tag         = destination_tag,
        destination_coord_deg   = destination_coord_deg ,
        destination_location    = des_location)
    
    return geospacial_data
