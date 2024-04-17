## @ingroup Methods-Aerodynamics-Airfoil_Panel_Method
# RCAIDE/Methods/Aerodynamics/Airfoil_Panel_Method/aero_coeff_new.py
# 
# 
# Created:  Apr 2024, Niranjan Nanjappa

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Core import Data

# pacakge imports  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# aero_coeff
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Methods-Aerodynamics-Airfoil_Panel_Method

def aero_coeff_new(x,y,cp,al,npanel,cf_top,cf_bot):
    """Compute airfoil force and moment coefficients about 
                    the quarter chord point          

    Assumptions:
    None

    Source:
    None                                                                    
                                                                   
    Inputs:                                                     
    x       -  Vector of x coordinates of the surface nodes      
    y       -  Vector of y coordinates of the surface nodes       
    cp      -  Vector of coefficients of pressure at the nodes  
    al      -  Angle of attack in radians                             
    npanel  -  Number of panels on the airfoil               
                                                                 
    Outputs:                                           
    cl      -  Airfoil lift coefficient                
    cd      -  Airfoil drag coefficient                                 
    cm      -  Airfoil moment coefficient about the c/4     
     
   Properties Used:
    N/A
    """
    dx       = x[1:]-x[:-1]
    dy       = y[1:]-y[:-1]
    xa       = 0.5*(x[1:] +x[:-1])-0.25
    ya       = 0.5*(y[1:] +y[:-1])
    dcn1     = -cp*dx
    dcn2     = cf_top*dy
    dcn3     = -cf_bot*dy
    dca1     = cp*dy
    dca2     = cf_top*dx 
    dca3     = -cf_bot*dx
    cn       = (np.sum(dcn1,axis=0) + np.sum(dcn2,axis=0) + np.sum(dcn3,axis=0)).T
    ca       = (np.sum(dca1,axis=0) + np.sum(dca2,axis=0) + np.sum(dca3,axis=0)).T
    cm_qc1   = np.sum(-dcn1*xa,axis=0) + np.sum(-dcn2*xa,axis=0) + np.sum(-dcn3*xa,axis=0)
    cm_qc2   = np.sum(dca1*ya,axis=0) + np.sum(dca2*ya,axis=0) + np.sum(dca3*ya,axis=0)
    cm_qc    = (cm_qc1 + cm_qc2).T
    # compute differential forces
    
    # cm      = np.sum((-dcn*xa + dca*ya),axis=0).T
    
    # orient normal and axial forces 
    cl      = cn*np.cos(al) - ca*np.sin(al) 
    cdpi    = cn*np.sin(al) + ca*np.cos(al)  
    
    # pack results
    AERO_RES = Data(
        cl   = cl, 
        cdpi = cdpi,
        cm   = cm_qc)
    
    return AERO_RES
    
    
    
    
    
    
    
    
    
    