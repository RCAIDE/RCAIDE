# RCAIDE/Methods/Aerodynamics/Airfoil_Panel_Method/aero_coeff.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Dec 2023, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Reference.Core import Data

# package imports  
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
# aero_coeff
# ----------------------------------------------------------------------------------------------------------------------   
def aero_coeff(x,y,cp,al,npanel):
    """Compute airfoil force and moment coefficients about the quarter chord point          

    Assumptions:
        None

    Source:
        None                                                                    
                                                                   
    Args:                                                     
        x      (numpy.ndarray): Vector of x coordinates of the surface nodes    [unitless]  
        y      (numpy.ndarray): Vector of y coordinates of the surface nodes    [unitless]    
        cp     (numpy.ndarray): Vector of coefficients of pressure at the nodes [unitless]  
        al     (numpy.ndarray): Angle of attack in radians                      [radians]      
        npanel           (int): Number of panels on the airfoil                 [unitless]
                                                                 
    Returns:                                           
        AERO_RES.cl  (numpy.ndarray):  Airfoil lift coefficient                 [unitless]
        AERO_RES.cd  (numpy.ndarray):  Airfoil drag coefficient                 [unitless]              
        AERO_RES.cm  (numpy.ndarray):  Airfoil moment coefficient about the c/4 [unitless]
    """  
    dx      = x[1:]-x[:-1]
    dy      = y[1:]-y[:-1]
    xa      = 0.5*(x[1:] +x[:-1])-0.25
    ya      = 0.5*(y[1:] +y[:-1]) 
    dcn     = -cp*dx  
    dca     = cp*dy   
    
    # compute differential forces
    cn      = np.sum(dcn,axis=0).T
    ca      = np.sum(dca,axis=0).T
    cm      = np.sum((-dcn*xa + dca*ya),axis=0).T
    
    # orient normal and axial forces 
    cl      = cn*np.cos(al) - ca*np.sin(al) 
    cdpi    = cn*np.sin(al) + ca*np.cos(al)  
    
    # pack results
    AERO_RES = Data(
        cl   = cl, 
        cdpi = cdpi,
        cm   = cm)
    
    return AERO_RES