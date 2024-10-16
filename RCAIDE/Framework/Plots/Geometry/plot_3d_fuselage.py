# RCAIDE/Library/Plots/Geometry/plot_3d_fuselage.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Framework.Plots.Geometry.Common.contour_surface_slice import contour_surface_slice
import RNUMPY as rp   

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------   
def plot_3d_fuselage(plot_data,fuselage, tessellation = 24 ,color_map = 'teal'):
    """ This plots the fuselage surface

    Assumptions:
    None

    Source:
    None

    Args:
    fuselage             - fuselage data structure
    fuselage_points      - coordinates of fuselage points
    color_map            - color of panel  
    """
    fuselage_points      = generate_3d_fuselage_points(fuselage,tessellation = 24 )
    num_fus_segs = len(fuselage_points[:,0,0])
    if num_fus_segs > 0:
        tesselation  = len(fuselage_points[0,:,0])
        for i_seg in range(num_fus_segs-1):
            for i_tes in range(tesselation-1):
                X = rp.array([[fuselage_points[i_seg  ,i_tes,0],fuselage_points[i_seg+1,i_tes  ,0]],
                              [fuselage_points[i_seg  ,i_tes+1,0],fuselage_points[i_seg+1,i_tes+1,0]]])
                Y = rp.array([[fuselage_points[i_seg  ,i_tes  ,1],fuselage_points[i_seg+1,i_tes  ,1]],
                              [fuselage_points[i_seg  ,i_tes+1,1],fuselage_points[i_seg+1,i_tes+1,1]]])
                Z = rp.array([[fuselage_points[i_seg  ,i_tes  ,2],fuselage_points[i_seg+1,i_tes  ,2]],
                              [fuselage_points[i_seg  ,i_tes+1,2],fuselage_points[i_seg+1,i_tes+1,2]]])  
                 
                values = rp.ones_like(X) 
                verts  = contour_surface_slice(X, Y, Z,values,color_map )
                plot_data.append(verts)          

    return plot_data 

def generate_3d_fuselage_points(fuselage ,tessellation = 24 ):
    """ This generates the coordinate points on the surface of the fuselage

    Assumptions:
    None

    Source:
    None

    Args:
    fuselage                  - fuselage data structure 
    """
    num_fus_segs = len(fuselage.Segments.keys())
    fuselage_points      = rp.zeros((num_fus_segs,tessellation ,3))

    if num_fus_segs > 0:
        for i_seg, segment in enumerate(fuselage.Segments): 
            a = segment.width/2
            b = segment.height/2
            theta    = rp.linspace(0,2*rp.pi,tessellation) 
            fus_ypts =  (abs((rp.cos(theta))))*a * ((rp.cos(theta)>0)*1 - (rp.cos(theta)<0)*1) 
            fus_zpts =  (abs((rp.sin(theta))))*b * ((rp.sin(theta)>0)*1 - (rp.sin(theta)<0)*1)  
            fuselage_points[i_seg,:,0] = segment.percent_x_location*fuselage.lengths.total + fuselage.origin[0][0]
            fuselage_points[i_seg,:,1] = fus_ypts + segment.percent_y_location*fuselage.lengths.total + fuselage.origin[0][1]
            fuselage_points[i_seg,:,2] = fus_zpts + segment.percent_z_location*fuselage.lengths.total + fuselage.origin[0][2]

    return fuselage_points
