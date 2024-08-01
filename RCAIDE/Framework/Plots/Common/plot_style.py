# RCAIDE/Library/Plots/Performance/Common/plot_style.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Framework.Core import Data 
 
# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------    
def plot_style():
    """Helper function for automatically setting the style of plots to the
    RCAIDE standard style.

    Use immediately before showing the figure to ensure all necessary
    information is available and to avoid over-writing style when
    constructing the figure. 

    Assumptions:
    None

    Source:
    None

    Args:
       None 

    Returns: 
       Plotting style parameters 

	
    """

    # Universal Plot Settings  
    plot_parameters                  = Data()
    plot_parameters.line_width       = 2 
    plot_parameters.line_style       = '-'
    plot_parameters.marker_size      = 10 
    plot_parameters.legend_font_size = 12
    plot_parameters.axis_font_size   = 14
    plot_parameters.title_font_size  = 18   
    plot_parameters.markers          = ['s','X','o','v','P','p','^','D','*']
    plot_parameters.color            = 'black'
    
    return plot_parameters