## @ingroup Plots
# Airfoil_Plots.py
#
# Created:  Mar 2021, M. Clarke
# Modified: Feb 2022, M. Clarke
#           Aug 2022, R. Erhard
#           Sep 2022, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------- 
from SUAVE.Core.Utilities import interp2d
from SUAVE.Core import Units 
import numpy as np 
import matplotlib.pyplot as plt  
import matplotlib.cm as cm
import os
 
## @ingroup Plots-Performance
def plot_airfoil_boundary_layer_properties(ap,show_legend = False ):
    """Plots viscous distributions
    
    Assumptions:
    None
    
    Source: 
    None
                                                     
    Inputs:
        ap     : data stucture of airfoil boundary layer properties  
                                                                           
    Outputs:
        Figures of quantity distributions
    
    Properties Used:
    N/A
    """            
    
    plot_quantity(ap, ap.Ue_Vinf, r'$U_{e}/U_{inv}}$'  ,'inviscid edge velocity',show_legend) 
    plot_quantity(ap, ap.H,  r'$H$'  ,'kinematic shape parameter',show_legend)
    plot_quantity(ap, ap.delta_star, r'$\delta*$' ,'displacement thickness',show_legend)
    plot_quantity(ap, ap.delta   , r'$\delta$' ,'boundary layer thickness',show_legend)
    plot_quantity(ap, ap.theta, r'$\theta$' ,'momentum thickness',show_legend)
    plot_quantity(ap, ap.cf, r'$c_f $'  ,   'skin friction coefficient',show_legend)
    plot_quantity(ap, ap.Re_theta,  r'$Re_{\theta}$'  ,'theta Reynolds number',show_legend) 
    

    fig      = plt.figure()
    axis     = fig.add_subplot(1,1,1)       
    n_cpts   = len(ap.AoA[:,0])
    n_cases  = len(ap.AoA[0,:]) 

    # create array of colors for difference reynolds numbers     
    blues  = cm.winter(np.linspace(0, 0.75,n_cases))    
    reds   = cm.autumn(np.linspace(0, 0.75,n_cases)) 
    
    for i in range(n_cpts):   
        for j in range(n_cases): 
            case_label = 'AoA: ' + str(round(ap.AoA[i,j]/Units.degrees, 2)) + ', Re: ' + str(ap.Re[i,j]) 
            axis.plot(ap.x[i,j], ap.y[i,j], color = blues[j] , linewidth = 2, label = case_label ) 
            axis.plot(ap.x_bl[i,j], ap.y_bl[i,j], color = reds[j] , marker = 'o', linewidth = 2, label = case_label ) 
            
    axis.set_title('Airfoil with Boundary Layers')            
    axis.set_ylabel(r'$y$') 
    axis.set_xlabel(r'$x$') 
    if show_legend:
        axis.legend(loc='upper left', ncol=1)    
    
    
    return    
 

## @ingroup Plots-Performance
def plot_quantity(ap, q, qaxis, qname,show_legend):
    """Plots a quantity q over lower/upper/wake surfaces
    
    Assumptions:
    None
    
    Source: 
    None
                                                     
    Inputs:
       ap        : data stucture of airfoil boundary layer properties  
       q         : vector of values to plot, on all points (wake too if present)
       qaxis     : name of quantity, for axis labeling
       qname     : name of quantity, for title labeling
                                                                           
    Outputs:
       Figure showing q versus x
    
    Properties Used:
    N/A
    """          

    fig      = plt.figure()
    axis     = fig.add_subplot(1,1,1)       
    n_cpts   = len(ap.AoA[:,0])
    n_cases  = len(ap.AoA[0,:]) 

    # create array of colors for difference reynolds numbers     
    blues  = cm.winter(np.linspace(0, 0.75,n_cases)) 
    
    for i in range(n_cpts):   
        for j in range(n_cases): 
            case_label = 'AoA: ' + str(round(ap.AoA[i,j]/Units.degrees, 2)) + ', Re: ' + str(ap.Re[i,j]) 
            axis.plot(ap.x[i,j], q[i,j], color = blues[j] , marker = 'o', linewidth = 2, label = case_label ) 
            
    axis.set_title(qname)            
    axis.set_ylabel(qaxis) 
    axis.set_xlabel(r'$x$') 
    if show_legend:
        axis.legend(loc='upper left', ncol=1)
    return  
 
## @ingroup Plots-Performance
def plot_airfoil_surface_forces(ap,show_legend= True,arrow_color = 'r'):  
    """ This plots the forces on an airfoil surface
    
        Assumptions:
        None
        
        Inputs: 
        ap       - data stucture of airfoil boundary layer properties and polars 
         
        Outputs: 
        None 
        
        Properties Used:
        N/A
        """        
    
    # determine dimension of angle of attack and reynolds number 
    n_cpts   = len(ap.AoA[:,0])
    n_cases  = len(ap.AoA[0,:])
    n_pts    = len(ap.x[0,0,:])-1
    

    for i in range(n_cpts):     
        for j in range(n_cases): 
            label =  '_AoA_' + str(round(ap.AoA[i,j]/Units.degrees,2)) + '_deg_Re_' + str(round(ap.Re[i,j]/1000000,2)) + 'E6'
            fig   = plt.figure('Airfoil_Pressure_Normals' + label )
            axis = fig.add_subplot(1,1,1) 
            axis.plot(ap.x[0,0,:], ap.y[0,0,:],'k-')   
            for k in range(n_pts):
                dx_val = ap.normals[i,j,k,0]*abs(ap.cp[i,j,k])*0.1
                dy_val = ap.normals[i,j,k,1]*abs(ap.cp[i,j,k])*0.1
                if ap.cp[i,j,k] < 0:
                    plt.arrow(x= ap.x[i,j,k], y=ap.y[i,j,k] , dx= dx_val , dy = dy_val , 
                              fc=arrow_color, ec=arrow_color,head_width=0.005, head_length=0.01 )   
                else:
                    plt.arrow(x= ap.x[i,j,k]+dx_val , y= ap.y[i,j,k]+dy_val , dx= -dx_val , dy = -dy_val , 
                              fc=arrow_color, ec=arrow_color,head_width=0.005, head_length=0.01 )   
    
    return   

## @ingroup Plots-Performance
def plot_airfoil_polar_files(polar_data, line_color = 'k-', save_figure = False, save_filename = "Airfoil_Polars", file_type = ".png"):
    """This plots all airfoil polars in the list "airfoil_polar_paths" 

    Assumptions:
    None

    Source:
    None

    Inputs:
    airfoil_polar_paths   [list of strings]

    Outputs: 
    Plots

    Properties Used:
    N/A	
    """ 
 
    # Get raw data polars
    CL           = polar_data.lift_coefficients
    CD           = polar_data.drag_coefficients
    alpha        = polar_data.angle_of_attacks
    Re_raw       = polar_data.reynolds_numbers
    n_Re         = len(polar_data.re_from_polar)
    cols         = cm.winter(np.linspace(0, 0.75,n_Re))   
        
    # plot all Reynolds number polars for ith airfoil 
    fig      = plt.figure(save_filename, figsize=(8,2*n_Re))
      
    for j in range(n_Re):
        ax1    = fig.add_subplot(n_Re,2,1+2*j)
        ax2    = fig.add_subplot(n_Re,2,2+2*j)   
        Re_val = str(round(Re_raw[j])/1e6)+'e6'
        
        ax1.plot(alpha/Units.degrees, CL[j,:], color= cols[j], linestyle = '--', label='Re='+Re_val)
        ax2.plot(alpha/Units.degrees, CD[j,:], color= cols[j], linestyle = '--', label='Re='+Re_val)
         
        ax1.set_ylabel('$C_l$')   
        ax2.set_ylabel('$C_d$')  
        ax1.legend(loc='best')
        
    ax1.set_xlabel('AoA [deg]') 
    ax2.set_xlabel('AoA [deg]') 
    fig.tight_layout()
    
    if save_figure:
        plt.savefig(save_filename.replace("_", " ") + file_type) 
    return

## @ingroup Plots-Performance
def plot_airfoil_polars(polar_data, save_figure = False,save_filename = "Airfoil_Polars", file_type = ".png"):
    """This plots all airfoil polars stored in the polar_data data_structure after AERODAS and smoothing corrections.
    
    Assumptions:
    None
    Source:
    None
    Inputs:
    polar_data     - airfoil polar data 
    aoa_sweep      - angles over which to plot the polars                [rad]
    Re_sweep       - Reynolds numbers over which to plot the polars      [-]
    
    Outputs: 
    Plots
    Properties Used:
    N/A	
    """ 
    #----------------------------------------------------------------------------
    # plot airfoil polar surrogates
    #----------------------------------------------------------------------------  
    num_polars = len(polar_data.reynolds_numbers)
    Re_sweep   = polar_data.reynolds_numbers 
    aoa_sweep  = polar_data.angle_of_attacks
    CL         = polar_data.lift_coefficients
    CD         = polar_data.drag_coefficients
    
    fig, ((ax,ax2),(ax3,ax4))  = plt.subplots(2,2)
    fig.set_figheight(8)
    fig.set_figwidth(12)
     
    fig.suptitle(save_filename + " (Raw Polar Data)")
    col_raw     = cm.jet(np.linspace(0, 1.0,num_polars))   
    for ii in range(len(Re_sweep[:num_polars])):
        
        ax.plot(aoa_sweep,CL[ii], color = col_raw[ii], label='Re='+str(Re_sweep[ii]))
        ax.set_xlabel("Alpha (deg)")
        ax.set_ylabel("Cl")
        ax.legend()
        ax.grid()
        
        ax2.plot(aoa_sweep, CD[ii], color = col_raw[ii])
        ax2.set_xlabel("Alpha (deg)")
        ax2.set_ylabel("Cd")
        ax2.grid()    
        
        ax3.plot(CD[ii], CL[ii], color = col_raw[ii])
        ax3.set_xlabel("Cd")
        ax3.set_ylabel("Cl")
        ax3.grid() 

        ax4.plot(aoa_sweep, CD[ii]/CL[ii], color = col_raw[ii])
        ax4.set_xlabel("Alpha (deg)")
        ax4.set_ylabel("Cd/Cl")
        ax4.grid()             
        
    plt.tight_layout()

    if save_figure:
        plt.savefig(save_filename +'_'  + file_type)  
    return