## @ingroup Library-Plots-Geometry
# RCAIDE/Library/Plots/Geometry/plot_3d_vehicle_vlm_panelization.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
import RCAIDE
from RCAIDE.Library.Methods.Aerodynamics.Vortex_Lattice_Method  import generate_vortex_distribution
from RCAIDE.Library.Plots.Geometry.Common.contour_surface_slice import contour_surface_slice

import numpy as np  
import plotly.graph_objects as go 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Plots-Geometry
def plot_3d_vehicle_vlm_panelization(vehicle,
                                     alpha = 1.0,
                                     plot_axis = False,
                                     save_figure = False,
                                     show_wing_control_points = True,
                                     save_filename = "VLM_Panelization",
                                     min_x_axis_limit            =  -5,
                                     max_x_axis_limit            =  40,
                                     min_y_axis_limit            =  -20,
                                     max_y_axis_limit            =  20,
                                     min_z_axis_limit            =  -20,
                                     max_z_axis_limit            =  20, 
                                     show_figure = True):
                                  
    """This plots vortex lattice panels created when Fidelity Zero  Aerodynamics 
    Routine is initialized

    Assumptions:
    None

    Source:
    None

    Inputs:
    vehicle.vortex_distribution

    Outputs: 
    Plots

    Properties Used:
    N/A	
    """

    # unpack vortex distribution
    try:
        VD = vehicle.vortex_distribution
    except:
        VL = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method()  
        VL.settings.number_of_spanwise_vortices  = 25
        VL.settings.number_of_chordwise_vortices = 5
        VL.settings.spanwise_cosine_spacing      = False
        VL.settings.model_fuselage               = False
        VL.settings.model_nacelle                = False
        VD = generate_vortex_distribution(vehicle,VL.settings) 

    camera        = dict(up=dict(x=0.5, y=0.5, z=1), center=dict(x=0, y=0, z=-.75), eye=dict(x=-1.5, y=-1.5, z=.8))
    plot_data     = []      

    # -------------------------------------------------------------------------
    # PLOT VORTEX LATTICE
    # -------------------------------------------------------------------------        
    n_cp      = VD.n_cp 
    color_map = 'greys'
    for i in range(n_cp):  
        X = np.array([[VD.XA1[i],VD.XA2[i]],[VD.XB1[i],VD.XB2[i]]])
        Y = np.array([[VD.YA1[i],VD.YA2[i]],[VD.YB1[i],VD.YB2[i]]])
        Z = np.array([[VD.ZA1[i],VD.ZA2[i]],[VD.ZB1[i],VD.ZB2[i]]])           
        
        values      = np.ones_like(X) 
        verts       = contour_surface_slice(X, Y, Z ,values,color_map)
        plot_data.append(verts)                 
  
  
    if  show_wing_control_points: 
        ctrl_pts = go.Scatter3d(x=VD.XC, y=VD.YC, z=VD.ZC,
                                    mode  = 'markers',
                                    marker= dict(size=6,color='red',opacity=0.8),
                                    line  = dict(color='red',width=2))
        plot_data.append(ctrl_pts)         
 
 
 
    fig = go.Figure(data=plot_data)
    fig.update_scenes(aspectmode   = 'auto',
                      xaxis_visible=plot_axis,
                      yaxis_visible=plot_axis,
                      zaxis_visible=plot_axis
                      )
    fig.update_layout( 
             width     = 1500,
             height    = 1500, 
             scene = dict(
                        xaxis = dict(backgroundcolor="grey", gridcolor="white", showbackground=plot_axis,
                                     zerolinecolor="white", range=[min_x_axis_limit,max_x_axis_limit]),
                        yaxis = dict(backgroundcolor="grey", gridcolor="white", showbackground=plot_axis, 
                                     zerolinecolor="white", range=[min_y_axis_limit,max_y_axis_limit]),
                        zaxis = dict(backgroundcolor="grey",gridcolor="white",showbackground=plot_axis,
                                     zerolinecolor="white", range=[min_z_axis_limit,max_z_axis_limit])),             
             scene_camera=camera) 
    fig.update_coloraxes(showscale=False)
    fig.update_traces(opacity = alpha)
    if save_figure:
        fig.write_image(save_filename + ".png")
        
    if show_figure:
        fig.write_html( save_filename + '.html', auto_open=True)
    return fig
