# RCAIDE/Methods/Performance/aircraft_aerodynamic_analysis.py
# 
# 
# Created:  Dec 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
import RCAIDE
from RCAIDE.Framework.Core import  Data
from RCAIDE.Library.Plots.Common import set_axes, plot_style    

# Pacakge imports 
import numpy as np  
import os, sys
from copy import deepcopy
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
# aircraft_loading_diagram
#------------------------------------------------------------------------------  
def aircraft_loading_diagram(mission = None, query_segment_tag = 'cruise', plot_diagram=True):
    """
    Computes the loading dragram of an aircraft 
 
 
    Parameters
    --------
    vehicle : Vehicle
        The vehicle instance to be analyzed
    angle_of_attacks : ndarray
        Array of angle of attack values to evaluate [radians]
    mach_numbers : ndarray
        Array of Mach numbers to evaluate 
    altitude : float, optional
        Altitude for atmospheric properties [m], default 0 
 
    Returns
    --------
    results : Data
        Container of analysis results including:
            * Mach : ndarray
                Evaluated Mach numbers
            * alpha : ndarray
                Evaluated angles of attack [rad]
            * lift_coefficient : ndarray
                Computed lift coefficients
            * drag_coefficient : ndarray
                Computed drag coefficients
            * moment_coefficient : ndarray
                Computed Y-moment coefficients
 
    Notes
    -----
    The function uses the US Standard Atmosphere 1976 model for atmospheric properties
    and evaluates aerodynamic coefficients using vortex lattice methods. Can use a surrogate model
    for faster evaluation or just direct evaluation of the aerodynamics. 
 
    **Major Assumptions**
        * Flow is steady and inviscid
        * Small angle approximations apply
        * Linear aerodynamics
        * Atmospheric properties follow US Standard Atmosphere 1976
 
    See Also
    --------
    RCAIDE.Library.Methods.Aerodynamics.Vortex_Lattice_Method
    RCAIDE.Library.Attributes.Atmospheres.Earth.US_Standard_1976
    """
     
    #------------------------------------------------------------------------  
    # Compute Loading Points 
    #------------------------------------------------------------------------
    percent_payload =  np.linspace(0, 1, 3)
    percent_fuel    =  np.linspace(0, 1, 3)
    CG_variation    =  np.linspace(0.5, 1.5, 10)
    
    # create empty data structures 
    lift_coefficient     = np.zeros((len(percent_payload),len(percent_fuel)))
    drag_coefficient     = np.zeros((len(percent_payload),len(percent_fuel)))
    moment_coefficient   = np.zeros((len(percent_payload),len(percent_fuel)))
    neutral_point        = np.zeros((len(percent_payload),len(percent_fuel)))
    static_margin        = np.zeros((len(percent_payload),len(percent_fuel)))
    aerodynamic_moment   = np.zeros((len(percent_payload),len(percent_fuel)))
    weight               = np.zeros((len(percent_payload),len(percent_fuel)))
    
    # store original vehicle 
    vehicle_0 =  deepcopy( mission.segments[0].analyses.weights.vehicle) 
    
    PLD  =  vehicle_0.mass_properties.payload
    FUEL =  vehicle_0.mass_properties.fuel
    OEW  =  vehicle_0.mass_properties.operating_empty
    MTOW =  vehicle_0.mass_properties.max_takeoff
    for i in range(len(percent_payload)):
        for j in range(len(percent_fuel)): 
            # -------------------------------------------------------------------------
            # Fuel and Payload 
            # -------------------------------------------------------------------------
            # Define takeoff weight
            mission.segments[0].analyses.weights.vehicle.mass_properties.takeoff  = OEW +  (percent_payload[i] * PLD)  +( percent_fuel[i] * FUEL)
            mission.segments[0].analyses.weights.vehicle.mass_properties.payload  = percent_payload[i] *PLD
            mission.segments[0].analyses.weights.vehicle.mass_properties.fuel     = percent_fuel[j] * FUEL
    
            # Evaluate mission with current TOW
            results = mission.evaluate()
            segment = results.segments[query_segment_tag] 
         
            lift_coefficient[i,j]    = segment.state.conditions.aerodynamics.coefficients.lift.total  
            drag_coefficient[i,j]    = segment.state.conditions.aerodynamics.coefficients.drag.total  
            aerodynamic_moment[i,j]  = segment.state.conditions.static_stability.coefficients.M         
            moment_coefficient[i,j]  = segment.state.conditions.static_stability.moments.M         
            neutral_point[i,j]       = segment.state.conditions.static_stability.neutral_point  
            static_margin[i,j]       = segment.state.conditions.static_stability.static_margin
            weight[i,j]              = mission.segments[0].analyses.weights.vehicle.mass_properties.takeoff 

            ## -------------------------------------------------------------------------
            ## 5% Static Margin Aft of CG
            ## -------------------------------------------------------------------------            
            
            ## Extract CG
            #CG_0_x = mission.segments[0].analyses.aerodynamics.vehicle.mass_properties.center_of_gravity[0][0]
            
            ## update analyses such that we do not update the CG location
            
            #results = mission.evaluate()
            #segment = results.segments[query_segment_tag]
 
        
    if plot_diagram: 
        # get plotting style 
        ps      = plot_style()  
    
        parameters = {'axes.labelsize': ps.axis_font_size,
                      'xtick.labelsize': ps.axis_font_size,
                      'ytick.labelsize': ps.axis_font_size,
                      'axes.titlesize': ps.title_font_size}
        plt.rcParams.update(parameters)

        fig  = plt.figure('Aircraft Loading Dragram')
        axis = fig.add_subplot(1,1,1)
        
        
        # fuel loading line
        y_pts_1  = OEW +  (percent_fuel * FUEL)
        y_pts_2  = OEW +  percent_fuel[-1] +  (percent_fuel* FUEL)
        axis.plot( aerodynamic_moment[:,0], y_pts_1, 'go-')
        axis.plot( aerodynamic_moment[:,0], y_pts_2, 'go-')
        
        # payload loading line
        y_pts_3  = OEW +  (percent_payload * PLD)
        y_pts_4  = OEW +  percent_payload[-1] +  (percent_payload * PLD)
        axis.plot( aerodynamic_moment[0, :], y_pts_3, 'bo-')
        axis.plot( aerodynamic_moment[0, :], y_pts_4, 'bo-')
        
        
        # total loading region 
        
        
        # MTOW line
        x_pts_MTOW = np.linspace(0, 1E8)
        y_pts_MTOW = np.ones_like(x_pts_MTOW)  *MTOW
        axis.plot(x_pts_MTOW, y_pts_MTOW, 'bo-') 
        
        
        # MLW line
        x_pts_MLW = np.linspace(0, 1E8)
        y_pts_MLW = np.ones_like(x_pts_MLW)  # TO COMPLETE 
        axis.plot(x_pts_MLW, y_pts_MLW, 'bo-') 
        
        
        # Neutral Point Line 
        
    
        axis.set_xlabel('Moment')
        axis.set_ylabel('Weight') 
        set_axes(axis) 
        fig.tight_layout()              
  
    return fig 
 