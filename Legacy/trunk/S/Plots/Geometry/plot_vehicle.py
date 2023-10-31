## @ingroup Plots-Geometry
# plot_vehicle.py
#
# Created : Mar 2020, M. Clarke
# Modified: Apr 2020, M. Clarke
# Modified: Jul 2020, M. Clarke
# Modified: Jul 2021, E. Botero
# Modified: Oct 2021, M. Clarke
# Modified: Dec 2021, M. Clarke
# Modified: Feb 2022, R. Erhard
# Modified: Mar 2022, R. Erhard
# Modified: Sep 2022, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
from Legacy.trunk.S.Core import Data
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Cross_Section.Airfoil.compute_naca_4series    import compute_naca_4series
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.generate_vortex_distribution    import generate_vortex_distribution 
from Legacy.trunk.S.Analyses.Aerodynamics import Vortex_Lattice


def plot_wing(axes,VD,face_color,edge_color,alpha_val):
    """ This plots the wings of a vehicle

    Assumptions:
    None

    Source:
    None

    Inputs:
    VD.
       XA1...ZB2         - coordinates of wing vortex distribution
    face_color           - color of panel
    edge_color           - color of panel edge
    alpha_color          - translucency:  1 = opaque , 0 = transparent

    Properties Used:
    N/A
    """

    n_cp = VD.n_cp
    for i in range(n_cp):

        X = [VD.XA1[i],VD.XB1[i],VD.XB2[i],VD.XA2[i]]
        Y = [VD.YA1[i],VD.YB1[i],VD.YB2[i],VD.YA2[i]]
        Z = [VD.ZA1[i],VD.ZB1[i],VD.ZB2[i],VD.ZA2[i]]

        verts = [list(zip(X, Y, Z))]

        collection = Poly3DCollection(verts)
        collection.set_facecolor(face_color)
        collection.set_edgecolor(edge_color)
        collection.set_alpha(alpha_val)

        axes.add_collection3d(collection)

    return

def plot_propeller_wake(axes, prop,face_color,edge_color,alpha,ctrl_pt=0):
    """ This plots a helical wake of a propeller or rotor

    Assumptions:
    None

    Source:
    None

    Inputs:
    VD.Wake.
       XA1...ZB2         - coordinates of wake vortex distribution
    face_color           - color of panel
    edge_color           - color of panel edge
    alpha_color          - translucency:  1 = opaque , 0 = transparent

    Properties Used:
    N/A
    """
    wVD      = prop.Wake.vortex_distribution.reshaped_wake 
    num_B    = len(wVD.XA1[0,0,:,0,0])
    dim_R    = len(wVD.XA1[0,0,0,:,0])
    nts      = len(wVD.XA1[0,0,0,0,:])
    
    for t_idx in range(nts):
        for B_idx in range(num_B):
            for loc in range(dim_R):
                X = [wVD.XA1[0,ctrl_pt,B_idx,loc,t_idx],
                     wVD.XB1[0,ctrl_pt,B_idx,loc,t_idx],
                     wVD.XB2[0,ctrl_pt,B_idx,loc,t_idx],
                     wVD.XA2[0,ctrl_pt,B_idx,loc,t_idx]]
                Y = [wVD.YA1[0,ctrl_pt,B_idx,loc,t_idx],
                     wVD.YB1[0,ctrl_pt,B_idx,loc,t_idx],
                     wVD.YB2[0,ctrl_pt,B_idx,loc,t_idx],
                     wVD.YA2[0,ctrl_pt,B_idx,loc,t_idx]]
                Z = [wVD.ZA1[0,ctrl_pt,B_idx,loc,t_idx],
                     wVD.ZB1[0,ctrl_pt,B_idx,loc,t_idx],
                     wVD.ZB2[0,ctrl_pt,B_idx,loc,t_idx],
                     wVD.ZA2[0,ctrl_pt,B_idx,loc,t_idx]]
                verts = [list(zip(X, Y, Z))]
                collection = Poly3DCollection(verts)
                collection.set_facecolor(face_color)
                collection.set_edgecolor(edge_color)
                collection.set_alpha(alpha)
                axes.add_collection3d(collection)
    return


def generate_fuselage_points(fus ,tessellation = 24 ):
    """ This generates the coordinate points on the surface of the fuselage

    Assumptions:
    None

    Source:
    None

    Inputs:
    fus                  - fuselage data structure

    Properties Used:
    N/A
    """
    num_fus_segs = len(fus.Segments.keys())
    fus_pts      = np.zeros((num_fus_segs,tessellation ,3))

    if num_fus_segs > 0:
        for i_seg in range(num_fus_segs):
            theta    = np.linspace(0,2*np.pi,tessellation)
            a        = fus.Segments[i_seg].width/2
            b        = fus.Segments[i_seg].height/2
            r        = np.sqrt((b*np.sin(theta))**2  + (a*np.cos(theta))**2)
            fus_ypts = r*np.cos(theta)
            fus_zpts = r*np.sin(theta)
            fus_pts[i_seg,:,0] = fus.Segments[i_seg].percent_x_location*fus.lengths.total + fus.origin[0][0]
            fus_pts[i_seg,:,1] = fus_ypts + fus.Segments[i_seg].percent_y_location*fus.lengths.total + fus.origin[0][1]
            fus_pts[i_seg,:,2] = fus_zpts + fus.Segments[i_seg].percent_z_location*fus.lengths.total + fus.origin[0][2]

    return fus_pts


def plot_fuselage_geometry(axes,fus_pts, face_color,edge_color,alpha):
    """ This plots the 3D surface of the fuselage

    Assumptions:
    None

    Source:
    None

    Inputs:
    fus_pts              - coordinates of fuselage points
    face_color           - color of panel
    edge_color           - color of panel edge
    alpha_color          - translucency:  1 = opaque , 0 = transparent


    Properties Used:
    N/A
    """

    num_fus_segs = len(fus_pts[:,0,0])
    if num_fus_segs > 0:
        tesselation  = len(fus_pts[0,:,0])
        for i_seg in range(num_fus_segs-1):
            for i_tes in range(tesselation-1):
                X = [fus_pts[i_seg  ,i_tes  ,0],
                     fus_pts[i_seg  ,i_tes+1,0],
                     fus_pts[i_seg+1,i_tes+1,0],
                     fus_pts[i_seg+1,i_tes  ,0]]
                Y = [fus_pts[i_seg  ,i_tes  ,1],
                     fus_pts[i_seg  ,i_tes+1,1],
                     fus_pts[i_seg+1,i_tes+1,1],
                     fus_pts[i_seg+1,i_tes  ,1]]
                Z = [fus_pts[i_seg  ,i_tes  ,2],
                     fus_pts[i_seg  ,i_tes+1,2],
                     fus_pts[i_seg+1,i_tes+1,2],
                     fus_pts[i_seg+1,i_tes  ,2]]
                verts = [list(zip(X, Y, Z))]
                collection = Poly3DCollection(verts)
                collection.set_facecolor(face_color)
                collection.set_edgecolor(edge_color)
                collection.set_alpha(alpha)
                axes.add_collection3d(collection)

    return




def plot_nacelle_geometry(axes,NAC_SURF_PTS,face_color,edge_color,alpha):
    """ This plots a 3D surface of a nacelle  

    Assumptions:
    None

    Source:
    None 
    
    Inputs:
    axes          - plotting axes
    NAC_SURF_PTS  - nacelle surface points 
    face_color    - face color of nacelle 
    edge_color    - edge color of nacelle 
    alpha         - transparency factor 

    Properties Used:
    N/A
    """

    num_nac_segs = len(NAC_SURF_PTS[:,0,0])
    tesselation  = len(NAC_SURF_PTS[0,:,0]) 
    for i_seg in range(num_nac_segs-1):
        for i_tes in range(tesselation-1):
            X = [NAC_SURF_PTS[i_seg  ,i_tes  ,0],
                 NAC_SURF_PTS[i_seg  ,i_tes+1,0],
                 NAC_SURF_PTS[i_seg+1,i_tes+1,0],
                 NAC_SURF_PTS[i_seg+1,i_tes  ,0]]
            Y = [NAC_SURF_PTS[i_seg  ,i_tes  ,1],
                 NAC_SURF_PTS[i_seg  ,i_tes+1,1],
                 NAC_SURF_PTS[i_seg+1,i_tes+1,1],
                 NAC_SURF_PTS[i_seg+1,i_tes  ,1]]
            Z = [NAC_SURF_PTS[i_seg  ,i_tes  ,2],
                 NAC_SURF_PTS[i_seg  ,i_tes+1,2],
                 NAC_SURF_PTS[i_seg+1,i_tes+1,2],
                 NAC_SURF_PTS[i_seg+1,i_tes  ,2]]
            verts = [list(zip(X, Y, Z))]
            collection = Poly3DCollection(verts)
            collection.set_facecolor(face_color)
            collection.set_edgecolor(edge_color)
            collection.set_alpha(alpha)
            axes.add_collection3d(collection)

    return
