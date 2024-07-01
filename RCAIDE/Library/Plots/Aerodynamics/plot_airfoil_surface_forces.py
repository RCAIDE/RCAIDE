## @ingroup Library-Plots-Performance-Aerodynamics  
# RCAIDE/Library/Plots/Performance/Aerodynamics/plot_airfoil_surface_forces.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
 
from RCAIDE.Framework.Core import Units  
import matplotlib.pyplot as plt    

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------     

## @ingroup Library-Plots-Performance-Aerodynamics   
def plot_airfoil_surface_forces(polars, save_figure = False , arrow_color = 'red',save_filename = 'Airfoil_Cp_Distribution', show_figure = True, file_type = ".png"):  
    """ This plots the forces on an airfoil surface
    
        Assumptions:
           None
        
        Args: 
            polars    (dict) data stucture of airfoil boundary layer properties and polars 
         
        Returns: 
            fig
        
        """        
    
    # determine dimension of angle of attack and reynolds number 
    n_cpts   = len(polars.AoA)
    nAoA     = len(polars.AoA[0])
    n_pts    = len(polars.x[0,0,:])- 1 
     

    for i in range(n_cpts):     
        for j in range(nAoA): 
            label =  '_AoA_' + str(round(polars.AoA[i][j]/Units.degrees,2)) + '_deg_Re_' + str(round(polars.Re[i][j]/1000000,2)) + 'E6'
            fig   = plt.figure('Airfoil_Pressure_Normals' + label )
            axis = fig.add_subplot(1,1,1) 
            axis.plot(polars.x[0,0,:], polars.y[0,0,:],'k-')   
            for k in range(n_pts):
                dx_val = polars.normals[i,j,k,0]*abs(polars.cp[i,j,k])*0.1
                dy_val = polars.normals[i,j,k,1]*abs(polars.cp[i,j,k])*0.1
                if polars.cp[i,j,k] < 0:
                    plt.arrow(x= polars.x[i,j,k], y=polars.y[i,j,k] , dx= dx_val , dy = dy_val , 
                              fc=arrow_color, ec=arrow_color,head_width=0.005, head_length=0.01 )   
                else:
                    plt.arrow(x= polars.x[i,j,k]+dx_val , y= polars.y[i,j,k]+dy_val , dx= -dx_val , dy = -dy_val , 
                              fc=arrow_color, ec=arrow_color,head_width=0.005, head_length=0.01 )   
    
    
    return fig 

