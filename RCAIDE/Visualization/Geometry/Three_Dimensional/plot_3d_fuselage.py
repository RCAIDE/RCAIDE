## @ingroup Visualization-Geometry-Three_Dimensional 
# RCAIDE/Visualization/Geometry/Three_Dimensional/plot_3d_fuselage.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Core import Data
from RCAIDE.Visualization.Geometry.Common.contour_surface_slice import contour_surface_slice
import numpy as np  
import plotly.graph_objects as go 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Visualization-Geometry-Three_Dimensional 
def plot_3d_fuselage(plot_data,fuselage, tessellation = 24 ,color_map = 'teal'):
    """ This plots the fuselage surface

    Assumptions:
    None

    Source:
    None

    Inputs:
    fuselage             - fuselage data structure
    fuselage_points      - coordinates of fuselage points
    color_map            - color of panel 


    Properties Used:
    N/A
    """
    fuselage_points      = generate_3d_fuselage_points(fuselage,tessellation = 24 )
    num_fus_segs = len(fuselage_points[:,0,0])
    if num_fus_segs > 0:
        tesselation  = len(fuselage_points[0,:,0])
        for i_seg in range(num_fus_segs-1):
            for i_tes in range(tesselation-1):
                X = np.array([[fuselage_points[i_seg  ,i_tes,0],fuselage_points[i_seg+1,i_tes  ,0]],
                              [fuselage_points[i_seg  ,i_tes+1,0],fuselage_points[i_seg+1,i_tes+1,0]]])
                Y = np.array([[fuselage_points[i_seg  ,i_tes  ,1],fuselage_points[i_seg+1,i_tes  ,1]],
                              [fuselage_points[i_seg  ,i_tes+1,1],fuselage_points[i_seg+1,i_tes+1,1]]])
                Z = np.array([[fuselage_points[i_seg  ,i_tes  ,2],fuselage_points[i_seg+1,i_tes  ,2]],
                              [fuselage_points[i_seg  ,i_tes+1,2],fuselage_points[i_seg+1,i_tes+1,2]]])  
                 
                values = np.ones_like(X) 
                verts  = contour_surface_slice(X, Y, Z,values,color_map )
                plot_data.append(verts)          

    return plot_data 

def generate_3d_fuselage_points(fuselage ,tessellation = 24 ):
    """ This generates the coordinate points on the surface of the fuselage

    Assumptions:
    None

    Source:
    None

    Inputs:
    fuselage                  - fuselage data structure

    Properties Used:
    N/A
    """
    num_fus_segs = len(fuselage.Segments.keys())
    fuselage_points      = np.zeros((num_fus_segs,tessellation ,3))

    if num_fus_segs > 0:
        for i_seg in range(num_fus_segs):
            theta    = np.linspace(0,2*np.pi,tessellation)
            a        = fuselage.Segments[i_seg].width/2
            b        = fuselage.Segments[i_seg].height/2
            r        = np.sqrt((b*np.sin(theta))**2  + (a*np.cos(theta))**2)
            fus_ypts = r*np.cos(theta)
            fus_zpts = r*np.sin(theta)
            fuselage_points[i_seg,:,0] = fuselage.Segments[i_seg].percent_x_location*fuselage.lengths.total + fuselage.origin[0][0]
            fuselage_points[i_seg,:,1] = fus_ypts + fuselage.Segments[i_seg].percent_y_location*fuselage.lengths.total + fuselage.origin[0][1]
            fuselage_points[i_seg,:,2] = fus_zpts + fuselage.Segments[i_seg].percent_z_location*fuselage.lengths.total + fuselage.origin[0][2]

    return fuselage_points
