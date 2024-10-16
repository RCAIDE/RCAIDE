# RCAIDE/Methods/Aerodynamics/Airfoil_Panel_Method/hess_smith.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Dec 2023, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports   
from .panel_geometry import panel_geometry
from .infl_coeff  import infl_coeff
from .velocity_distribution import velocity_distribution

# package imports  
import RNUMPY as rp  
 
# ----------------------------------------------------------------------------------------------------------------------
# hess_smith
# ---------------------------------------------------------------------------------------------------------------------- 
def hess_smith(x_coord,y_coord,alpha,Re,npanel):
    """Computes the incompressible, inviscid flow over an airfoil of  arbitrary shape using the Hess-Smith panel method.  

    Assumptions:
       None

    Source:  An introduction to theoretical and computational aerodynamics", J. Moran, Wiley, 1984  
 
                                                     
    Inputs          
        x_coord  (numpy.ndarray):  Vector of x coordinates of the surface  [unitess]     
        y_coord  (numpy.ndarray):  Vector of y coordinates of the surface  [unitess]  
        alpha    (numpy.ndarray):  Angle of attack                         [radians] 
        Re       (numpy.ndarray):  Reynold's number                        [radians] 
        npanel             (int):  Number of panels on the airfoil.        [unitess]  
                                                                           
    Outputs                                                                   
        xbar    (numpy.ndarray):  Vector of x coordinates of the surface nodes    [unitless]           
        ybar    (numpy.ndarray):  Vector of y coordinates of the surface nodes    [unitless]          
        vt      (numpy.ndarray):  Tangential velocity on surface of airfoil       [unitless]            
        norm    (numpy.ndarray):  Normal vectors on surface of airfoil            [unitless]  
    """       
    ncases    = len(alpha[0,:])
    ncpts     = len(Re) 
    alpha_2d  = rp.repeat(alpha.T[rp.newaxis,:, :], npanel, axis=0) 
    
    # generate panel geometry data for later use   
    l,st,ct,xbar,ybar,norm = panel_geometry(x_coord,y_coord,npanel,ncases,ncpts) 
    
    # compute matrix of aerodynamic influence coefficients
    ainfl         = infl_coeff(x_coord,y_coord,xbar,ybar,st,ct,npanel,ncases,ncpts) # ncases x ncpts x npanel+1 x npanel+1 
    
    # compute right hand side vector for the specified angle of attack 
    b_2d          = rp.zeros((npanel+1,ncases, ncpts))
    b_2d[:-1,:,:] = st*rp.cos(alpha_2d) - rp.sin(alpha_2d)*ct
    b_2d[-1,:,:]  = -(ct[0,:,:]*rp.cos(alpha_2d[-1,:,:]) + st[0,:,:]*rp.sin(alpha_2d[-1,:,:]))-(ct[-1,:,:]*rp.cos(alpha_2d[-1,:,:]) +st[-1,:,:]*rp.sin(alpha_2d[-1,:,:]))
      
    # solve matrix system for vector of q_i and gamma  
    qg_T          = rp.linalg.solve(ainfl,rp.swapaxes(b_2d.T,0,1))
    qg            = rp.swapaxes(qg_T.T,1,2) 
    
    # compute the tangential velocity distribution at the midpoint of panels 
    vt            = velocity_distribution(qg,x_coord,y_coord,xbar,ybar,st,ct,alpha_2d,npanel,ncases,ncpts)
    
    return  xbar,ybar,vt,norm 