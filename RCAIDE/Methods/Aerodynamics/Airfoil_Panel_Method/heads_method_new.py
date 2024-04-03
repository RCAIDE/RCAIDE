## @ingroup Methods-Aerodynamics-Airfoil_Panel_Method
# RCAIDE/Methods/Aerodynamics/Airfoil_Panel_Method/heads_method.py
# 
# 
# Created:  Mar 2024, Niranjan Nanjappa

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Core import Data

# package imports  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# heads_method
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Aerodynamics-Airfoil_Panel_Method
def heads_method_new(npanel,ncases,ncpts,DEL_0,THETA_0,DELTA_STAR_0,CF_0,ShapeFactor_0,RE_L,TURBULENT_COORD,VE_I,DVE_I,TURBULENT_SURF,tol):
    """ Computes the boundary layer characteristics in turbulent
    flow pressure gradients

    Source:
    Head, M. R., and P. Bandyopadhyay. "New aspects of turbulent boundary-layer structure."
    Journal of fluid mechanics 107 (1981): 297-338.

    Assumptions:
    None  

    Inputs: 
    ncases         - number of cases                                                               [unitless]
    ncpts          - number of control points                                                      [unitless]
    DEL_0          - intital bounday layer thickness                                               [m]
    DELTA_STAR_0   - initial displacement thickness                                                [m]
    CF_0           - initial value of the skin friction coefficient                                [unitless]
    H_0            - initial value of the shape factor                                             [unitless]
    THETA_0        - initial momentum thickness                                                    [m]
    TURBULENT_SURF - normalized length of surface                                                  [unitless]
    RE_L           - Reynolds number                                                               [unitless]
    TURBULENT_COORD- x coordinate on surface of airfoil                                            [unitless] 
    VE_I           - boundary layer velocity at all panels                                         [m/s-m] 
    DVE_I          - derivative of boundary layer velocity at all panels                           [m/s^2] 
    npanel         - number of points on surface                                                   [unitless]
    tol            - boundary layer error correction tolerance                                     [unitless]

    Outputs: 
    RESULTS.
      X_H          - reshaped distance along airfoil surface                    [unitless]
      THETA_H      - momentum thickness                                         [m]
      DELTA_STAR_H - displacement thickness                                     [m] 
      H_H          - shape factor                                               [unitless]
      CF_H         - friction coefficient                                       [unitless]
      RE_THETA_H   - Reynolds number as a function of momentum thickness        [unitless]
      RE_X_H       - Reynolds number as a function of distance                  [unitless]
      DELTA_H      - boundary layer thickness                                   [m]
       
    Properties Used:
    N/A
    """   
    rho = 1.225  # air density
    # Initialize vectors 
    X_H          = np.zeros((npanel,ncases,ncpts))
    THETA_H      = np.zeros_like(X_H)
    DELTA_STAR_H = np.zeros_like(X_H)
    H_H          = np.zeros_like(X_H)
    CF_H         = np.zeros_like(X_H) 
    RE_THETA_H   = np.zeros_like(X_H)
    RE_X_H       = np.zeros_like(X_H)
    DELTA_H      = np.zeros_like(X_H) 
    H1_H         = np.zeros_like(X_H)
    VETHETAH1_H  = np.zeros_like(X_H)      
 
    H1_check = (DEL_0 - DELTA_STAR_0)/THETA_0   
    for case in range(ncases):
        for cpt in range(ncpts):  
            # length of tubulent surface  
            l = TURBULENT_SURF[case,cpt] 
            if l == 0.0:
                pass
            else: 
                def getcf(ind, H, THETA):
                    ReTheta = (Re_L/l)*Ve_i[ind]*THETA;
                    cf_var = 0.246*(10**(-0.678*H))*(ReTheta**-0.268);
                    return cf_var


                def getH(H1_var):
                    if H1_var<3.3:
                        H_var = 3.0
                    elif H1_var < 5.39142:
                        H_var = 0.6778 + 1.153793*(H1_var-3.3)**-0.32637;
                    elif H1_var >= 5.39142:
                        H_var = 1.1 + 0.8598636*(H1_var - 3.3)**-0.777;
                    return H_var
                
             
                # define RK4 slope function for Theta
                def dTheta_by_dx(index, X, THETA, VETHETAH1):
                    return 0.5*cf[index] - (THETA/Ve_i[index])*(2+H[index])*(dVe_i[index])
                
                # define RK4 slope function for VeThetaH1
                def dVeThetaH1_by_dx(index, X, THETA, VETHETAH1):
                    return Ve_i[index]*0.0306*(((VETHETAH1/(Ve_i[index]*THETA))-3)**-0.6169)
                
                x_i          = TURBULENT_COORD.data[:,case,cpt][TURBULENT_COORD.mask[:,case,cpt] ==False] 
                Ve_i         = VE_I.data[:,case,cpt][TURBULENT_COORD.mask[:,case,cpt] ==False]
                dVe_i        = DVE_I.data[:,case,cpt][TURBULENT_COORD.mask[:,case,cpt] ==False]
                Re_L         = RE_L[cpt] 
                nu           = l/Re_L 
                n            = len(x_i)
                dx           = np.diff(x_i)
                
                H            = np.zeros(n) 
                H[0]         = ShapeFactor_0[case,cpt]
                Theta        = np.zeros(n)
                Theta[0]     = THETA_0[case,cpt]
                H1           = np.zeros(n) 
                H1[0]        = (DEL_0[case,cpt] - DELTA_STAR_0[case,cpt])/THETA_0[case,cpt]
                if H1[0]<3.3:
                    H1[0] = 3.417285
                
                cf           = np.zeros(n)
                cf[0]        = CF_0[case,cpt] 
                VeThetaH1    = np.zeros(n)
                VeThetaH1[0] = Ve_i[0]*Theta[0]*H1[0]
                
                for i in range(1,n):
                    # initialise the variable values at the current grid point using previous grid points (to define the error functions)
                    H_er = H[i-1];  cf_er = cf[i-1];  H1_er = H1[i-1];  Theta_er = Theta[i-1];
                    # assign previous grid point values of H and Cf to start RK4
                    H[i] = H[i-1]; cf[i] = cf[i-1];
                    
                    #assume some error values
                    erH = 0.2; erH1 = 0.2; erTheta = 0.2; ercf = 0.2;
                    
                    # iterate to get the variables at the grid point
                    while abs(erH)>0.00001 or abs(erH1)>0.00001 or abs(erTheta)>0.00001 or abs(ercf)>0.00001:
                        
                        # get Theta and VeThetaH1
                        Theta[i], VeThetaH1[i] = RK4(i-1, dx, x_i, Theta, VeThetaH1, dTheta_by_dx, dVeThetaH1_by_dx)
                        if np.isnan(VeThetaH1[i]):
                            VeThetaH1[i] = VeThetaH1[i-1]
                       
                        # get H1
                        H1[i] = VeThetaH1[i]/(Ve_i[i]*Theta[i])
                        
                        # get H
                        H[i] = getH(H1[i])
                        
                        # get skin friction
                        cf[i] = getcf(i, H[i], Theta[i])
                        
                        # define errors
                        erH = (H[i]-H_er)/H[i];
                        erH1 = (H1[i]-H1_er)/H1[i];
                        erTheta = (Theta[i]-Theta_er)/Theta[i];
                        ercf = (cf[i]-cf_er)/cf[i];
                        
                        # assign current iteration variable values to the Var_er
                        H_er = H[i]
                        H1_er = H1[i]
                        Theta_er = Theta[i]
                        cf_er = cf[i]
                
                
                delta_star   = H*Theta
                Re_theta     = (Re_L/l)*Ve_i*Theta
                Re_x         = (Ve_i*x_i)/nu
                delta        = (Theta*H1) + delta_star
                
                indices = np.where(TURBULENT_COORD.mask[:,case,cpt] == False)
                np.put(X_H[:,case,cpt],indices,x_i )
                np.put(THETA_H[:,case,cpt],indices,Theta)
                np.put(DELTA_STAR_H[:,case,cpt],indices,delta_star)
                np.put(H_H[:,case,cpt],indices,H)
                np.put(CF_H[:,case,cpt],indices,cf)
                np.put(RE_THETA_H[:,case,cpt],indices,Re_theta)
                np.put(RE_X_H[:,case,cpt],indices,Re_x)
                np.put(DELTA_H[:,case,cpt],indices,delta)

    RESULTS = Data(
            X_H          = X_H,      
            THETA_H      = THETA_H,   
            DELTA_STAR_H = DELTA_STAR_H,
            H_H          = H_H,       
            CF_H         = CF_H,   
            RE_THETA_H   = RE_THETA_H,   
            RE_X_H       = RE_X_H,    
            DELTA_H      = DELTA_H,   
        )    

    return  RESULTS


def RK4(ind, dx, x, Theta_var, VeThetaH1_var, Theta_slope, VeThetaH1_slope):
    k1 = Theta_slope(ind,  x[ind],  Theta_var[ind],  VeThetaH1_var[ind])
    l1 = VeThetaH1_slope(ind,  x[ind],  Theta_var[ind],  VeThetaH1_var[ind])
    
    k2 = Theta_slope(ind,  x[ind] + (dx[ind]/2),  Theta_var[ind] + (k1*dx[ind]/2),  VeThetaH1_var[ind] + (l1*dx[ind]/2))
    l2 = VeThetaH1_slope(ind,  x[ind] + (dx[ind]/2),  Theta_var[ind] + (k1*dx[ind]/2),  VeThetaH1_var[ind] + (l1*dx[ind]/2))
    
    k3 = Theta_slope(ind,  x[ind] + (dx[ind]/2),  Theta_var[ind] + (k2*dx[ind]/2),  VeThetaH1_var[ind] + (l2*dx[ind]/2))
    l3 = VeThetaH1_slope(ind,  x[ind] + (dx[ind]/2),  Theta_var[ind] + (k2*dx[ind]/2),  VeThetaH1_var[ind] + (l2*dx[ind]/2))
    
    k4 = Theta_slope(ind,  x[ind] + dx[ind],  Theta_var[ind] + (k3*dx[ind]),  VeThetaH1_var[ind] + (l2*dx[ind]))
    l4 = VeThetaH1_slope(ind,  x[ind] + dx[ind],  Theta_var[ind] + (k3*dx[ind]),  VeThetaH1_var[ind] + (l2*dx[ind]))
    
    Theta_new = Theta_var[ind] + ((dx[ind]/6)*(k1 + 2*k2 + 2*k3 + k4))
    VeThetaH1_new = VeThetaH1_var[ind] + ((dx[ind]/6)*(l1 + 2*l2 + 2*l3 + l4))
    return Theta_new, VeThetaH1_new


                # H_0          = ShapeFactor_0[case,cpt]
                # theta_0      = THETA_0[case,cpt] 
                # H1_0         = (DEL_0[case,cpt] - DELTA_STAR_0[case,cpt])/theta_0
                # cf_0         = CF_0
                # VeThetaH1_0  = Ve_i[0]*theta_0*             
                # del_0        = DEL_0[case,cpt]
                # del_star_0   = DELTA_STAR_0[case,cpt]
                
                # H1_0         = getH1(np.atleast_1d(H_0))[0]
                # if np.isnan(H1_0):
                #     H1_0     = (del_0 - del_star_0) / theta_0 
                # y0           = [theta_0, getVe(0,x_i,Ve_i)*theta_0*H1_0]     
                # y            = odeint(odefcn,y0,x_i,args=(Re_L/l, x_i, Ve_i, dVe_i))  
                
                # Compute momentum thickness, theta 
#                 theta            = y[:,0]  
#                 ind              = np.where(~np.isnan(theta))[0]
#                 first, last      = ind[0], ind[-1]
#                 theta[:first]    = theta[first]
#                 dtheta_dx        = (theta[last]-theta[last-1])/(x_i[last]-x_i[last-1])
#                 theta[last + 1:] = theta[last] + dtheta_dx*(x_i[last + 1:]-x_i[last])
                
#                 Ve_theta_H1            = y[:,1]  
#                 ind                    = np.where(~np.isnan(Ve_theta_H1))[0]
#                 first, last            = ind[0], ind[-1]
#                 Ve_theta_H1[:first]    = Ve_theta_H1[first]
#                 dVe_theta_H1_dx        = (Ve_theta_H1[last]-Ve_theta_H1[last-1])/(x_i[last]-x_i[last-1])
#                 Ve_theta_H1[last + 1:] = Ve_theta_H1[last] + dVe_theta_H1_dx*(x_i[last + 1:]-x_i[last])
                
#                 # find theta values that do not converge and replace them with neighbor
#                 idx1         = np.where(abs((theta[1:] - theta[:-1])/theta[:-1]) > tol )[0]
#                 if len(idx1)> 1: 
#                     np.put(theta,idx1 + 1, theta[idx1])    
#                 idx1         = np.where(abs((Ve_theta_H1[1:] - Ve_theta_H1[:-1])/Ve_theta_H1[:-1]) >tol)[0]
#                 if len(idx1)> 1: 
#                     np.put(Ve_theta_H1,idx1 + 1, Ve_theta_H1[idx1])    
                  
#                 # Compute mass flow shape factor, H1
#                 H1           = Ve_theta_H1/(theta*Ve_i)
                
#                 # Compute H 
#                 H            = getH(np.atleast_1d(H1)) 
#                 H[H<0]       = 1E-6    # H cannot be negative 
#                 # find H values that do not converge and replace them with neighbor
#                 idx1               = np.where(abs((H[1:] - H[:-1])/H[:-1]) >tol)[0]
#                 if len(idx1)> 1: 
#                     np.put(H,idx1 + 1, H[idx1])     
                
#                 # Compute Reynolds numbers based on momentum thickness  
#                 Re_theta     = Re_L/l * Ve_i*theta 
                
#                 # Compute Reynolds numbers based on distance along airfoil
#                 Re_x         = Ve_i* x_i / nu
                
#                 # Compute skin friction 
#                 cf           = abs( getcf(np.atleast_1d(Re_theta),np.atleast_1d(H))) 
                
#                 # Compute displacement thickness
#                 del_star     = H*theta   
                
#                 # Compute boundary layer thickness 
#                 delta        = theta*H1 + del_star 
                
#                 # Reynolds number at x=0 cannot be negative (give nans)
#                 Re_x[0]      = 1E-5                
    
#                 # Find where matrices are not masked 
#                 indices = np.where(TURBULENT_COORD.mask[:,case,cpt] == False)
                
#                 # Store results 
#                 np.put(X_H[:,case,cpt],indices,x_i )
#                 np.put(THETA_H[:,case,cpt],indices,theta)
#                 np.put(DELTA_STAR_H[:,case,cpt],indices,del_star)
#                 np.put(H_H[:,case,cpt],indices,H)
#                 np.put(CF_H[:,case,cpt],indices ,cf)
#                 np.put(RE_THETA_H[:,case,cpt],indices,Re_theta)
#                 np.put(RE_X_H[:,case,cpt],indices,Re_x)
#                 np.put(DELTA_H[:,case,cpt],indices,delta) 

#     RESULTS = Data(
#         X_H          = X_H,      
#         THETA_H      = THETA_H,   
#         DELTA_STAR_H = DELTA_STAR_H,
#         H_H          = H_H,       
#         CF_H         = CF_H,   
#         RE_THETA_H   = RE_THETA_H,   
#         RE_X_H       = RE_X_H,    
#         DELTA_H      = DELTA_H,   
#     )    

#     return  RESULTS

# def getH(H1):
#     """ Computes the shape factor, H
#     Assumptions:
#     None
#     Source:
#     None
#     Inputs: 
#     H1       - mass flow shape factor [unitless]
#     Outputs:  
#     H        - shape factor [unitless]
#     Properties Used:
#     N/A
#     """         
#     H       = 0.6778 + 1.1536*(H1-3.3)**-0.326
#     idx1    = (H1 < 3.3)
#     H[idx1] = 3.0
#     idx2    = (H1 > 5.3)
#     H[idx2] = 1.1 + 0.86*(H1[idx2] - 3.3)**-0.777 
#     return H 

# def getH1(H) :    
#     """ Computes the mass flow shape factor, H1
#     Assumptions:
#     None
#     Source:
#     None
#     Inputs: 
#     H        - shape factor [unitless]
#     Outputs:  
#     H1       - mass flow shape factor [unitless]
#     Properties Used:
#     N/A 
#     """
#     H1       = 3.3 + 0.8234*(H - 1.1)**-1.287  
#     idx1     = (H > 1.6) 
#     H1[idx1] = 3.3 + 1.5501*(H[idx1] - 0.6778)**-3.064
#     return H1 

# def odefcn(y,x,ReL_div_L, x_i, Ve_i, dVe_i): 
#     """ Computes boundary layer functions using SciPy ODE solver 
#     Assumptions:
#     None
#     Source:
#     None
#     Inputs:  
#     y           - initial conditions of functions               [unitless]
#     x           - new x values at which to solve ODE            [unitless]
#     ReL_div_L   - ratio of Reynolds number to length of surface [unitless]
#     x_i         - intial array of x values                      [unitless]
#     Ve_i        - intial boundary layer velocity                [m/s]
#     dVe_i       - initial derivative of bounday layer velocity  [m/s-m]

#     Outputs:  
#     f           - 2D function of momentum thickness and the product of 
#                   the velocity,momentum thickness and the mass flow shape factor
#     Properties Used:
#     N/A 
#     """    
#     theta       = y[0]
#     Ve_theta_H1 = y[1]  

#     if theta == 0:
#         H1 = Ve_theta_H1 / (theta + 1e-6) / getVe(x,x_i,Ve_i)
#     else:
#         H1 = Ve_theta_H1 / theta / getVe(x,x_i,Ve_i)

#     H           = getH(np.atleast_1d(H1))
#     Re_theta    = ReL_div_L * theta
#     cf          = getcf(np.atleast_1d(Re_theta),np.atleast_1d(H))
#     dydx_1      = 0.5*cf-(theta/getVe(x,x_i,Ve_i))*(2+H)*getdVe(x, x_i, dVe_i)
#     dydx_2      = getVe(x,x_i,Ve_i)*0.0306*(H1 - 3)**-0.6169 
#     f           = [dydx_1,dydx_2] 
#     return f 

# def getVe(x,x_i,Ve_i):
#     """ Interpolates the bounday layer velocity over a new dimension of x 
#     Assumptions:
#     None
#     Source:
#     None
#     Inputs: 
#     x         - new x dimension                    [unitless]
#     x_i       - old x dimension                    [unitless]
#     Ve_i      - old boundary layer velocity values [m/s] 

#     Outputs:  
#     Ve        - new boundary layer velocity values [m/s]
#     Properties Used:
#     N/A 
#     """    
#     Ve_func = interp1d(x_i,Ve_i,fill_value = "extrapolate")
#     Ve      = Ve_func(x)
#     return Ve 

# def getdVe(x,x_i,dVe_i):
#     """ Interpolates the derivatives of the bounday layer velocity over a new dimension of x

#     Assumptions:
#     None
#     Source:
#     None
#     Inputs: 
#     x         - new x dimension                                  [unitless]
#     x_i       - old x dimension                                  [unitless]
#     dVe_i     - old derivative of boundary layer velocity values [m/s-m] 

#     Outputs:  
#     dVe       - new derivative of boundary layer velocity values [m/s-m]
#     Properties Used:
#     N/A 
#     """        
#     dVe_func = interp1d(x_i,dVe_i,fill_value = "extrapolate")
#     dVe      = dVe_func(x)
#     return dVe  

# def getcf(Re_theta,H): 
#     """ Computes the skin friction coefficient, cf
#     Assumptions:
#     None
#     Source:
#     None
#     Inputs: 
#     Re_theta - Reynolds Number as a function of momentum thickness [m]
#     H        - shape factor                                        [unitless]
#     Outputs:  
#     cf       - skin friction coefficient  [unitless]
#     Properties Used:
#     N/A 
#     """    
#     cf       = 0.246*10**(-0.678*H)*(Re_theta)**-0.268 
#     idx1     = (Re_theta == 0) 
#     cf[idx1] = 0.246*10**(-0.678*H[idx1])*(1e-3)**-0.268 
#     return cf 