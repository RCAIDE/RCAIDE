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
    # Batch analysis of single airfoil - NACA 4412 
    # -----------------------------------------------
    AoA_deg              = np.linspace(-5,10,16)
    Re_vals              = np.atleast_1d(np.ones(1))*1E5 
    AoA_rad              = np.atleast_2d(AoA_deg*Units.degrees)   
    airfoil_file_1       = '4412'
    airfoil_geometry_1   = compute_naca_4series(airfoil_file_1,npoints = 200)
    airfoil_properties_1 = airfoil_analysis(airfoil_geometry_1,AoA_rad,Re_vals)  
    
     # Plots    
    # plot_airfoil_surface_forces(airfoil_properties_1)   
    # plot_airfoil_polars(airfoil_properties_1)
    # plot_airfoil_boundary_layer_properties(airfoil_properties_1,show_legend = True )   
    
    # Verification  
    Cl_true        = 1.07589901
    Cd_visc_true   = 0.0311218958
    Cdpi_true      = 0.00754285574
    Cm_true        = -0.114993524
  
    diff_CL = np.abs((airfoil_properties_1.cl[0,10] - Cl_true)/Cl_true)    
    print('\nCL difference')
    print(diff_CL)
    assert diff_CL < 1e-6
    
    diff_CD = np.abs((airfoil_properties_1.cd_visc[0,10] - Cd_visc_true)/Cd_visc_true)  
    print('\nCD difference')
    print(diff_CD)
    assert diff_CD < 1e-6
    
    diff_CDpi = np.abs((airfoil_properties_1.cdpi[0,10] - Cdpi_true)/Cdpi_true)  
    print('\nCDpi difference')
    print(diff_CDpi)
    assert diff_CDpi < 1e-6     

    diff_CM = np.abs((airfoil_properties_1.cm[0,10] - Cm_true)/Cm_true) 
    print('\nCM difference')
    print(diff_CM)
    assert diff_CM < 1e-6
    
    
    # Abbot Validation
    Cl_abbot = 0.906
    Cd_abbot = 0.0064
    Cm_abbot = -0.0885
    
    CL_val_diff = np.abs((airfoil_properties_1.cl[0,10] - Cl_abbot)/Cl_abbot)
    CD_val_diff = np.abs((airfoil_properties_1.cd_visc[0,10] - Cd_abbot)/Cd_abbot)
    CDpi_val_diff = np.abs((airfoil_properties_1.cdpi[0,10] - Cd_abbot)/Cd_abbot)
    CM_val_diff = np.abs((airfoil_properties_1.cm[0,10] - Cm_abbot)/Cm_abbot)
    print('\nValidation against Abbot data')
    print('Cl-Cl_abbot/Cl_abbot',CL_val_diff*100,'%\n')
    print('Cd-Cd_abbot/Cd_abbot',CD_val_diff*100,'%\n')
    print('Cdpi-Cd_abbot/Cd_abbot',CDpi_val_diff*100,'%\n')
    print('Cm-Cm_abbot/Cm_abbot',CM_val_diff*100,'%\n')
    
    
    # CFD Validation
    Cl_CFD = 1.086832
    Cd_CFD = 0.013989972
    Cm_CFD = -0.64460867
    
    CL_CFD_diff = np.abs((airfoil_properties_1.cl[0,10] - Cl_CFD)/Cl_CFD)
    CD_CFD_diff = np.abs((airfoil_properties_1.cd_visc[0,10] - Cd_CFD)/Cd_CFD)
    CDpi_CFD_diff = np.abs((airfoil_properties_1.cdpi[0,10] - Cd_CFD)/Cd_CFD)
    CM_CFD_diff = np.abs((airfoil_properties_1.cm[0,10] - Cm_CFD)/Cm_CFD)
    print('\nValidation against CFD data')
    print('Cl-Cl_CFD/Cl_CFD',CL_CFD_diff*100,'%\n')
    print('Cd-Cd_CFD/Cd_CFD',CD_CFD_diff*100,'%\n')
    print('Cdpi-Cd_CFD/Cd_CFD',CDpi_CFD_diff*100,'%\n')
    print('Cm-Cm_CFD/Cm_CFD',CM_CFD_diff*100,'%\n')

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
    Re_vals               = np.atleast_1d(np.array([1E5,2E5]))
    AoA_vals              = np.atleast_2d(np.array([[0,1,2,3,4,5],[0,1,2,3,4,5]])*Units.degrees)   
    airfoil_file_2        = rel_path + 'NACA_4412.txt'     
    airfoil_geometry_2    = import_airfoil_geometry(airfoil_file_2,npoints = 200)      
    airfoil_properties_2  = airfoil_analysis(airfoil_geometry_2,AoA_vals,Re_vals)     
       
    True_cl     = np.array([0.46727175,	0.577401252, 0.687570351, 0.797744681, 0.907889284, 1.01796863])
    True_cd     = np.array([0.012447118, 0.0138151301, 0.0158378745, 0.0172326865, 0.0197543403, 0.024218885])
    True_cm     = np.array([-0.103004455, -0.102475862, -0.101934602, -0.101381336, -0.100816737, -0.100241493])
       
    print('\nCL difference')
    print(np.sum(np.abs((airfoil_properties_2.cl[0]  - True_cl)/True_cl)))
    assert np.sum(np.abs((airfoil_properties_2.cl[0]   - True_cl)/True_cl))  < 1e-5 
    
    print('\nCD difference') 
    print(np.sum(np.abs((airfoil_properties_2.cd_visc[0]  - True_cd)/True_cd)))
    assert np.sum(np.abs((airfoil_properties_2.cd_visc[0]   - True_cd)/True_cd))  < 1e-5
    
    print('\nCM difference') 
    print(np.sum(np.abs((airfoil_properties_2.cm[0]  - True_cm)/True_cm)))
    assert np.sum(np.abs((airfoil_properties_2.cm[0]   - True_cm)/True_cm))  < 1e-5  
    return   
    

if __name__ == '__main__': 
    main() 
    plt.show()