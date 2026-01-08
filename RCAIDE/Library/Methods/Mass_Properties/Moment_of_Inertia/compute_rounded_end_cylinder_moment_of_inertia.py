# RCAIDE/Library/Methods/Mass_Properties/Moment_of_Inertia/compute_rounded_end_cylinder_moment_of_inertia.py 
# 
# Created:  Aug. 2025, M. Clarke  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Rounded-End Cylinder Moment of Inertia
# ----------------------------------------------------------------------------------------------------------------------   
def compute_rounded_end_cylinder_moment_of_inertia(component,outer_length,outer_radius,inner_length = 0,inner_radius = 0,center_of_gravity = np.array([[0,0,0]])):  
    """
    Computes the moment of inertia tensor for a hollow rounded-end cylinder.

    Parameters
    ----------
    origin : numpy.ndarray
        Origin coordinates of the component [m]
    mass : float
        Total mass of the cylinder [kg]
    outer_length : float
        Length of the outer cylinder [m]
    outer_radius : float
        Radius of the outer cylinder [m]
    inner_length : float, optional
        Length of the inner cylinder (for hollow cylinder) [m], default is 0
    inner_radius : float, optional
        Radius of the inner cylinder (for hollow cylinder) [m], default is 0
    center_of_gravity : numpy.ndarray, optional
        Global center of gravity coordinates [m], default is [0,0,0]

    Returns
    -------
    I_global : numpy.ndarray
        Moment of inertia tensor in global coordinate system [kg⋅m²]
        Shape: (3, 3) matrix
    mass : float
        Mass of the cylinder [kg]

    Notes
    -----
    This function computes the moment of inertia tensor for a hollow rounded-end
    cylinder using the parallel axis theorem to transform from local to global
    coordinate systems. The cylinder consists of a cylindrical section with
    hemispherical end caps.
    
    **Major Assumptions**
        * Cylinder has constant density throughout
        * Cylinder axis is aligned with the x-axis
        * Rounded ends are perfect hemispheres
        * Parallel axis theorem is valid for the transformation
        * Point mass approximation for zero radius/length cases
    
    **Theory**

    The volume of a rounded-end cylinder is:
    :math:`V = V_{cylinder} + V_{hemispheres} = \\pi r^2 L + \\frac{4}{3}\\pi r^3`

    For a hollow cylinder:
    :math:`V_{total} = V_{outer} - V_{inner}`

    The density is calculated as:
    :math:`\\rho = \\frac{m}{V}`

    The parallel axis theorem transforms the moment of inertia:
    :math:`I_{global} = I_{local} + m(\\|\\vec{s}\\|^2 \\mathbf{I} - \\vec{s} \\vec{s}^T)`

    where :math:`\\vec{s}` is the vector from the component origin to the global center of gravity.
    """

    # ----------------------------------------------------------------------------------------------------------------------
    # unpack 
    # ----------------------------------------------------------------------------------------------------------------------
    origin = component.origin
    mass   = component.mass_properties.mass
        
    # ----------------------------------------------------------------------------------------------------------------------    
    # Setup
    # ----------------------------------------------------------------------------------------------------------------------           
    I =  np.zeros((3, 3))
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # Moment of inertia in local system 
    # ----------------------------------------------------------------------------------------------------------------------
    #I_cylinder_ax_1      = # AIDAN
    #I_sperical_caps_ax_1 = # AIDAN
    #I_tot_ax_1           = I_cylinder_ax_1 + I_sperical_caps_ax_1 + #parallel axis theoem compoment of caps

    #I_cylinder_ax_2      = # AIDAN
    #I_sperical_caps_ax_2 = # AIDAN
    #I_tot_ax_2           = I_cylinder_ax_2 + I_sperical_caps_ax_2 + #parallel axis theoem compoment of caps     
     
    ## depending on orientation of cylindrical tank
    #if:
        #I[0][0]
        #I[1][1]
        #I[2][2]
    #else:
        #I[0][0]
        #I[1][1]
        #I[2][2] 
    
    # ----------------------------------------------------------------------------------------------------------------------    
    # transform moment of inertia to the global system
    # ----------------------------------------------------------------------------------------------------------------------
    s        = np.array(center_of_gravity) - np.array(origin) # Vector between component and the CG    
    I_global = np.array(I) + mass * (np.array(np.dot(s[0], s[0])) * np.array(np.identity(3)) - np.outer(s,s))

    # Store moment of inertia tensor on component 
    component.mass_properties.moments_of_inertia.tensor = I_global   
    component.mass_properties.moments_of_inertia.non_dimensional_tensor = I / mass 
        
    return I_global,  mass