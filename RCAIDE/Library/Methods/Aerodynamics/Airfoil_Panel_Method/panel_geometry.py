## @ingroup Methods-Aerodynamics-Airfoil_Panel_Method
# panel_geometry.py 

# Created:  Mar 2021, M. Clarke
# Modified: Sep 2022, M. Clarke

# ---------------------------------------
#-------------------------------
#  Imports
# ----------------------------------------------------------------------
import Legacy.trunk.S as SUAVE
from Legacy.trunk.S.Core import Units
import numpy as np

# ----------------------------------------------------------------------
# panel_geometry.py
# ----------------------------------------------------------------------  
## @ingroup Methods-Aerodynamics-Airfoil_Panel_Method
def func_panel_geometry(x,y,npanel,ncases,ncpts):
    """Computes airfoil surface panelization parameters for later use in 
    the computation of the matrix of influence coefficients.        

    Assumptions:
    None

    Source:
    None 
                                                                       
    Inputs:                                                         
    x       -  Vector of x coordinates of the surface nodes  [unitless]         
    y       -  Vector of y coordinates of the surface nodes  [unitless]      
    npanel  -  Number of panels on the airfoil               [unitless]         
                                                                     
    Outputs:                                             
    l       -  Panel lengths                              [unitless]
    st      -  np.sin(theta) for each panel               [radians]
    ct      -  np.cos(theta) for each panel               [radians]
    xbar    -  x-coordinate of the midpoint of each panel [unitless]              
    ybar    -  y-coordinate of the midpoint of each panel [unitless]               
    
    
    Properties Used:
    N/A
    """     
    # compute various geometrical quantities    
    l    = np.sqrt((x[1:] -x[:-1])**2 +(y[1:] -y[:-1])**2)
    st   = (y[1:] -y[:-1])/l 
    ct   = (x[1:] -x[:-1])/l 
    xbar = (x[1:] +x[:-1])/2
    ybar = (y[1:] +y[:-1])/2 
    
    norm  = np.zeros((npanel,2,ncases,ncpts))
    norm[:,0,:,:]  =  -st
    norm[:,1,:,:]  =  ct 
    
    return l,st,ct,xbar,ybar,norm 
     


panel_geometry(State, Settings, System):
	#TODO: x      = [Replace With State, Settings, or System Attribute]
	#TODO: y      = [Replace With State, Settings, or System Attribute]
	#TODO: npanel = [Replace With State, Settings, or System Attribute]
	#TODO: ncases = [Replace With State, Settings, or System Attribute]
	#TODO: ncpts  = [Replace With State, Settings, or System Attribute]

	results = func_panel_geometry('x', 'y', 'npanel', 'ncases', 'ncpts')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System