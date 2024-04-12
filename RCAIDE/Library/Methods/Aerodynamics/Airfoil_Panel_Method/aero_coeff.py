## @ingroup Methods-Aerodynamics-Airfoil_Panel_Method
# aero_coeff.py

# Created:  Mar 2021, M. Clarke
# Modified: Sep 2022, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------- 
from Legacy.trunk.S.Core import Data
import numpy as np

# ----------------------------------------------------------------------
# panel_geometry.py
# ----------------------------------------------------------------------   

## @ingroup Methods-Aerodynamics-Airfoil_Panel_Method
def func_aero_coeff(x,y,cp,al,npanel):
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
     
    dx      = x[1:]-x[:-1]
    dy      = y[1:]-y[:-1]
    xa      = 0.5*(x[1:] +x[:-1])-0.25
    ya      = 0.5*(y[1:] +y[:-1])
    dcn     = -cp[:-1]*dx
    dca     = cp[:-1]*dy
    
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


def aero_coeff(State, Settings, System):
	#TODO: x      = [Replace With State, Settings, or System Attribute]
	#TODO: y      = [Replace With State, Settings, or System Attribute]
	#TODO: cp     = [Replace With State, Settings, or System Attribute]
	#TODO: al     = [Replace With State, Settings, or System Attribute]
	#TODO: npanel = [Replace With State, Settings, or System Attribute]

	results = func_aero_coeff('x', 'y', 'cp', 'al', 'npanel')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System