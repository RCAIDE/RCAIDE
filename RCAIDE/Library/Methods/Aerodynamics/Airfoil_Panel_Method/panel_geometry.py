# RCAIDE/Methods/Aerodynamics/Airfoil_Panel_Method/panel_geometry.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Dec 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
# panel_geometry
# ----------------------------------------------------------------------------------------------------------------------
def panel_geometry(x,y,npanel,ncases,ncpts):
    """Computes airfoil surface panelization parameters for later use in 
    the computation of the matrix of influence coefficients.        

    Assumptions:
        None

    Source:
        None 
                                                                       
    Args:                                                         
    x       (numpy.ndarray): Vector of x coordinates of the surface nodes  [unitless]         
    y       (numpy.ndarray): Vector of y coordinates of the surface nodes  [unitless]      
    npanel            (int): Number of panels on the airfoil               [unitless]              
    ncases            (int): Number of cases                               [unitless]                
    ncpts             (int): Number of control points                      [unitless]             
                                                                     
    Returns:                                             
    l       (numpy.ndarray): Panel lengths                              [unitless]
    st      (numpy.ndarray): np.sin(theta) for each panel               [radians]
    ct      (numpy.ndarray): np.cos(theta) for each panel               [radians]
    xbar    (numpy.ndarray): x-coordinate of the midpoint of each panel [unitless]              
    ybar    (numpy.ndarray): y-coordinate of the midpoint of each panel [unitless]              
    norm    (numpy.ndarray): normal vectors                             [unitless]       
    """     
     
    l              = np.sqrt((x[1:] -x[:-1])**2 +(y[1:] -y[:-1])**2)
    st             = (y[1:] -y[:-1])/l 
    ct             = (x[1:] -x[:-1])/l 
    xbar           = (x[1:] +x[:-1])/2
    ybar           = (y[1:] +y[:-1])/2  
    norm           = np.zeros((npanel,2,ncases,ncpts))
    norm[:,0,:,:]  = -st
    norm[:,1,:,:]  = ct 
    
    return l,st,ct,xbar,ybar,norm 
