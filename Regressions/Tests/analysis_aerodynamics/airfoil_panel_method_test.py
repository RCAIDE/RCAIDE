# airfoil_panel_method_test.py
#
# Created: Dec 2023, M. Clarke  
 
# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
# RCAIDE Imports 
from RCAIDE.Core import Units
from RCAIDE.Methods.Aerodynamics.Airfoil_Panel_Method     import airfoil_analysis 
from RCAIDE.Methods.Geometry.Two_Dimensional.Airfoil      import  compute_naca_4series
from RCAIDE.Methods.Geometry.Two_Dimensional.Airfoil      import import_airfoil_geometry
from RCAIDE.Visualization import * 

# Python imports
import os 
import numpy as np
import matplotlib.pyplot as plt    
 

# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main():   
    single_airfoil()
    multi_airfoil()
    
    return 
    
def single_airfoil():
    # -----------------------------------------------
    # Batch analysis of single airfoil - NACA 2410 
    # -----------------------------------------------
    AoA_deg              = np.linspace(-5,10,16)
    Re_vals              = np.atleast_2d(np.ones(len(AoA_deg)))* 1E5 
    AoA_rad              = np.atleast_2d(AoA_deg*Units.degrees)   
    airfoil_file_1       = '2412'
    airfoil_geometry_1   = compute_naca_4series(airfoil_file_1,npoints = 200)
    airfoil_properties_1 = airfoil_analysis(airfoil_geometry_1,AoA_rad,Re_vals)  
    
     # Plots    
    plot_airfoil_surface_forces(airfoil_properties_1)   
    plot_airfoil_boundary_layer_properties(airfoil_properties_1,show_legend = True )   
    
    # XFOIL Validation  
    xfoil_data_cl   = 0.803793
    xfoil_data_cd   = 0.017329
    xfoil_data_cm   = -0.053745
  
    diff_CL  = np.abs(airfoil_properties_1.cl[0,10] - xfoil_data_cl)    
    print('\nCL difference')
    print(diff_CL)
    assert np.abs(airfoil_properties_1.cl[0,10]   - xfoil_data_cl)   < 1e-1
    

    diff_CD           = np.abs(airfoil_properties_1.cd_visc[0,10] - xfoil_data_cd)  
    print('\nCDpi difference')
    print(diff_CD)
    assert np.abs(airfoil_properties_1.cd_visc[0,10]  - xfoil_data_cd)  < 1e-2
     

    diff_CM           = np.abs(airfoil_properties_1.cm[0,10] - xfoil_data_cm)  
    print('\nCM difference')
    print(diff_CM)
    assert np.abs(airfoil_properties_1.cm[0,10]  - xfoil_data_cm)   < 1e-2
    

    fig = plt.figure()
    axis_1 = fig.add_subplot(2,2,1)
    axis_1.plot(AoA_deg,airfoil_properties_1.cl[0,:],'-ko')
    axis_1.plot(AoA_deg,airfoil_properties_1.cl_visc[0,:],'-k')
    axis_2 = fig.add_subplot(2,2,2)
    axis_2.plot(AoA_deg,airfoil_properties_1.cd_visc[0,:])
    axis_3 = fig.add_subplot(2,2,3)
    axis_3.plot(AoA_deg,airfoil_properties_1.cm[0,:],'-ko')
    axis_3.plot(AoA_deg,airfoil_properties_1.cm_visc[0,:],'-k') 
       
    return 
    
def multi_airfoil():
    # -----------------------------------------------
    # Single Condition Analysis of multiple airfoils  
    # ----------------------------------------------- 
    ospath                = os.path.abspath(__file__)
    separator             = os.path.sep 
    rel_path              = ospath.split('analysis_aerodynamics' + separator + 'airfoil_panel_method_test.py')[0] + '..' + separator + 'Vehicles' + separator + 'Airfoils' + separator 
    Re_vals               = np.atleast_2d(np.array([[1E5,1E5,1E5,1E5,1E5,1E5],[2E5,2E5,2E5,2E5,2E5,2E5]]))
    AoA_vals              = np.atleast_2d(np.array([[0,1,2,3,4,5],[0,1,2,3,4,5]])*Units.degrees)   
    airfoil_file_2        = rel_path + 'NACA_4412.txt'     
    airfoil_geometry_2    = import_airfoil_geometry(airfoil_file_2,npoints = 200)      
    airfoil_properties_2  = airfoil_analysis(airfoil_geometry_2,AoA_vals,Re_vals)     
       
    True_cls    = np.array([0.46727175, 0.57740125, 0.68757035, 0.79774468, 0.90788928, 1.01796863])
    True_cd     = np.array([0.01419351, 0.01569456, 0.01744239, 0.01964226, 0.02245851,0.02597575])
    True_cms    = np.array([-0.10300446, -0.10247586, -0.1019346 , -0.10138134, -0.10081674,-0.10024149])
       
    print('\nCL difference')
    print(np.sum(np.abs((airfoil_properties_2.cl[0]  - True_cls)/True_cls)))
    assert np.sum(np.abs((airfoil_properties_2.cl[0]   - True_cls)/True_cls))  < 1e-5 
    
    print('\nCD difference') 
    print(np.sum(np.abs((airfoil_properties_2.cd_visc[0]  - True_cd)/True_cd)))
    assert np.sum(np.abs((airfoil_properties_2.cd_visc[0]   - True_cd)/True_cd))  < 1e-5
    
    print('\nCM difference') 
    print(np.sum(np.abs((airfoil_properties_2.cm[0]  - True_cms)/True_cms)))
    assert np.sum(np.abs((airfoil_properties_2.cm[0]   - True_cms)/True_cms))  < 1e-5  
    return   
    

if __name__ == '__main__': 
    main() 
    plt.show()