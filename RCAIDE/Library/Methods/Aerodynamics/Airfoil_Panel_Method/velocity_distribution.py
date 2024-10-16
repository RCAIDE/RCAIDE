# RCAIDE/Methods/Aerodynamics/Airfoil_Panel_Method/velocity_distribution.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Dec 2023, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# Python imports  
import RNUMPY as rp  

# ---------------------------------------------------------------------------------------------------------------------- 
# velocity_distribution
# ---------------------------------------------------------------------------------------------------------------------- 
def velocity_distribution(qg,x,y,xbar,ybar,st,ct,alpha_2d,npanel,ncases,ncpts):
    """Compute the tangential velocity distribution at the midpoint of each panel   
    
    Source:
        None

    Assumptions:
        None  
    
    Args:  
        qg          (numpy.ndarray): Vector of source/sink and vortex strengths    [unitless]          
        x           (numpy.ndarray): Vector of x coordinates of the surface nodes  [unitless]         
        y           (numpy.ndarray): Vector of y coordinates of the surface nodes  [unitless]            
        xbar        (numpy.ndarray): x-coordinate of the midpoint of each panel    [unitless]           
        ybar        (numpy.ndarray): y-coordinate of the midpoint of each panel    [unitless]           
        st          (numpy.ndarray): rp.sin(theta) for each panel                  [radians]                
        ct          (numpy.ndarray): rp.cos(theta) for each panel                  [radians]             
        al          (numpy.ndarray): Angle of attack in radians                    [radians]             
        npanel                (int): Number of panels on the airfoil               [unitless]  

     Returns:        
        vt_2d       (numpy.ndarray): Vector of tangential velocities               [unitless]
    """   
    # flow tangency boundary condition - source distribution  
    vt_2d = ct *rp.cos(alpha_2d) + st*rp.sin(alpha_2d)
    gamma = rp.repeat(qg[-1,:,:][rp.newaxis,:,:],npanel, axis = 0)  
    
    # convert 1d matrices to 2d 
    qg_2d                = rp.repeat(qg[:-1,:,:][rp.newaxis,:,:,:],npanel, axis = 0) 
    x_2d                 = rp.repeat(rp.swapaxes(rp.swapaxes(x,0, 2),0,1)[:,:,rp.newaxis,:],npanel, axis = 2)
    y_2d                 = rp.repeat(rp.swapaxes(rp.swapaxes(y,0, 2),0,1)[:,:,rp.newaxis,:],npanel, axis = 2)
    xbar_2d              = rp.repeat(rp.swapaxes(rp.swapaxes(xbar,0, 2),0,1)[:,:,:,rp.newaxis],npanel, axis = 3)
    ybar_2d              = rp.repeat(rp.swapaxes(rp.swapaxes(ybar,0, 2),0,1)[:,:,:,rp.newaxis],npanel, axis = 3) 
    st_2d                = rp.repeat(rp.swapaxes(rp.swapaxes(st,0, 2),0,1)[:,:,:,rp.newaxis],npanel, axis = 3) 
    ct_2d                = rp.repeat(rp.swapaxes(rp.swapaxes(ct,0, 2),0,1)[:,:,:,rp.newaxis],npanel, axis = 3) 
    st_2d_T              = rp.swapaxes(st_2d,2,3)
    ct_2d_T              = rp.swapaxes(ct_2d,2,3)  
    
    # Fill the elements of the matrix of aero influence coefficients
    sti_minus_j          = ct_2d_T*st_2d - st_2d_T*ct_2d 
    cti_minus_j          = ct_2d_T*ct_2d + st_2d_T*st_2d 
    rij                  = rp.sqrt((xbar_2d-x_2d[:,:,:,:-1])**2 + (ybar_2d-y_2d[:,:,:,:-1])**2)
    rij_plus_1           = rp.sqrt((xbar_2d-x_2d[:,:,:,1:])**2 +  (ybar_2d-y_2d[:,:,:,1:])**2)
    rij_dot_rij_plus_1   = (xbar_2d-x_2d[:,:,:,:-1])*(xbar_2d-x_2d[:,:,:,1:]) + (ybar_2d-y_2d[:,:,:,:-1])*(ybar_2d-y_2d[:,:,:,1:])  
    anglesign            = rp.sign((xbar_2d-x_2d[:,:,:,:-1])*(ybar_2d-y_2d[:,:,:,1:]) - (xbar_2d-x_2d[:,:,:,1:])*(ybar_2d-y_2d[:,:,:,:-1]))
    r_ratio              = rij_dot_rij_plus_1/rij/rij_plus_1
    r_ratio[r_ratio>1.0] = 1.0 # attenuate numerical noise     
    betaij               = rp.real(anglesign*rp.arccos(r_ratio)) 
    for i in range(ncases):
        for j in range(ncpts):
            rp.fill_diagonal(betaij[i,j,:,:], rp.pi)   
    
    # swap axes 
    sti_minus_j_2d  = rp.swapaxes(rp.swapaxes(sti_minus_j,0,2),1,3) 
    betaij_2d       = rp.swapaxes(rp.swapaxes(betaij,0,2),1,3) 
    cti_minus_j_2d  = rp.swapaxes(rp.swapaxes(cti_minus_j,0,2),1,3) 
    rij_2d          = rp.swapaxes(rp.swapaxes(rij,0,2),1,3) 
    rij_plus_1_2d   = rp.swapaxes(rp.swapaxes(rij_plus_1,0,2),1,3) 
     
    vt_2d += rp.sum(qg_2d/2/rp.pi*(sti_minus_j_2d*betaij_2d - cti_minus_j_2d*rp.log(rij_plus_1_2d/rij_2d)),1)  + \
             rp.sum(gamma/2/rp.pi*(sti_minus_j_2d*rp.log(rij_plus_1_2d/rij_2d) + cti_minus_j_2d*betaij_2d),1)
    
    return  vt_2d
