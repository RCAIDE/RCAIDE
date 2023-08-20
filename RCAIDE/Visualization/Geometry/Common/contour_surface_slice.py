## @ingroup Visualization-Geometry-Common
# RCAIDE/Visualization/Geometry/Common/contour_surface_slices.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
import plotly.graph_objects as go   

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Visualization-Geometry-Common
def contour_surface_slice(x,y,z,values,color_scale, showscale = False , colorbar_title = None, colorbar_location = 'right', colorbar_orientation = 'v'):
    return go.Surface(x=x,y=y,z=z,surfacecolor=values,colorscale=color_scale, showscale=showscale,
                      colorbar = dict(title = colorbar_title, titleside = "right", orientation = "v")) 

   
