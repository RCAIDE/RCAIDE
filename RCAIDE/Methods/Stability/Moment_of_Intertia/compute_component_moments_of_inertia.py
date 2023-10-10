## @ingroup Methods-Stability-Moment_of_Intertia
# RCAIDE/Methods/Stability/Moment_of_Intertia/compute_compoments_moments_of_intertia.py 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Moment of Inertia of Cuboid  
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Stability-Moment_of_Intertia
def calculate_moment_of_inertia_cuboid(comp, l_x, l_y, l_z):
    
    m = comp.mass_properties.mass
    # Calculate the components of the moment of inertia tensor
    Ixx = (m / 12) * (l_y**2 + l_z**2)
    Iyy = (m / 12) * (l_x**2 + l_z**2)
    Izz = (m / 12) * (l_x**2 + l_y**2)

    # Create the moment of inertia tensor as a numpy array
    I = np.array([[Ixx, 0, 0],
                  [0, Iyy, 0],
                  [0, 0, Izz]])

    comp.mass_properties.moment_of_intertia = I
    return   

# ----------------------------------------------------------------------------------------------------------------------
#  Moment of Inertia of Hollow Cuboid  
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Stability-Moment_of_Intertia
def calculate_moment_of_inertia_hollow_cuboid(comp, l_x1, l_y1, l_z1, l_x2, l_y2, l_z2):
    
    m = comp.mass_properties.mass
    # Calculate the volumes
    V1 = l_x1 * l_y1 * l_z1
    V2 = l_x2 * l_y2 * l_z2

    # Calculate the moment of inertia tensor
    Ixx = (m / 12) * ((V2 * (l_y2**2 + l_z2**2)) - (V1 * (l_y1**2 + l_z1**2))) / (V2 - V1)
    Iyy = (m / 12) * ((V2 * (l_x2**2 + l_z2**2)) - (V1 * (l_x1**2 + l_z1**2))) / (V2 - V1)
    Izz = (m / 12) * ((V2 * (l_x2**2 + l_y2**2)) - (V1 * (l_x1**2 + l_y1**2))) / (V2 - V1)

    # Create the moment of inertia tensor as a numpy array
    I = np.array([[Ixx, 0, 0],
                  [0, Iyy, 0],
                  [0, 0, Izz]])

    comp.mass_properties.moment_of_intertia = I
    return 


# ----------------------------------------------------------------------------------------------------------------------
#  Moment of Inertia of Hollow Cylinder
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Stability-Moment_of_Intertia
def calculate_moment_of_inertia_hollow_cylinder(comp, R1, R2, h):
    
    m = comp.mass_properties.mass
    
    # Calculate the components of the moment of inertia tensor
    Ixx = (m / 2) * (R2**2 + R1**2)
    Iyy = (m / 12) * (3 * (R2**2 + R1**2) + h**2)
    Izz = (m / 12) * (3 * (R2**2 + R1**2) + h**2)

    # Create the moment of inertia tensor as a numpy array
    I = np.array([[Ixx, 0, 0],
                  [0, Iyy, 0],
                  [0, 0, Izz]])

    comp.mass_properties.moment_of_intertia = I
    return     

# ----------------------------------------------------------------------------------------------------------------------
#  Moment of Inertia of Solid Cuboid  
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Stability-Moment_of_Intertia
def calculate_moment_of_inertia_solid_cylinder(comp, R2, h):
    
    m = comp.mass_properties.mass
    # Calculate the components of the moment of inertia tensor
    Ixx = (m / 2) * R2**2
    Iyy = (m / 12) * (3 * R2**2 + h**2)
    Izz = (m / 12) * (3 * R2**2 + h**2)

    # Create the moment of inertia tensor as a numpy array
    I = np.array([[Ixx, 0, 0],
                  [0, Iyy, 0],
                  [0, 0, Izz]])

    comp.mass_properties.moment_of_intertia = I
    return 

# ----------------------------------------------------------------------------------------------------------------------
#  Moment of Inertia of Hollow Sphere 
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Stability-Moment_of_Intertia
def moment_of_inertia_solid_sphere(comp, outer_radius=0 , inner_radius=0):
    """
    Calculate the moment of inertia matrix for a solid sphere.

    Parameters:
    - mass:(in kg)
    - outer_radius: (in meters)
    - inner_radius: in meters, default is 0 for a solid sphere

    Return:
    - MOI [I]
    """
    
    mass = comp.mass_properties.mass
    # Calculate the moment of inertia components
    Ixx = (2 / 5) * mass * ((outer_radius**5 - inner_radius**5) / 3)
    Iyy = (2 / 5) * mass * ((outer_radius**5 - inner_radius**5) / 3)
    Izz = (2 / 5) * mass * ((outer_radius**5 - inner_radius**5) / 3)

    # Create the moment of inertia matrix [I]
    I = np.array([
        [Ixx, 0, 0],
        [0, Iyy, 0],
        [0, 0, Izz]
    ])
    comp.mass_properties.moment_of_intertia = I
    return 

# ----------------------------------------------------------------------------------------------------------------------
#  Moment of Inertia of Cone
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Stability-Moment_of_Intertia
def moment_of_inertia_cone_matrix(comp, radius, height):
    """
    Calculate the moment of inertia matrix for a cone.

    Parameters:
    - mass:   (in kg)
    - radius:  (in meters)
    - height: (in meters)

    Returns:
    - [Ixx, Iyy, Izz] matrix
    """
    mass = comp.mass_properties.mass
    # Calculate the moment of inertia components
    Ixx = (3 / 20) * mass * radius**2 + (3 / 5) * mass * height**2
    Iyy = (3 / 20) * mass * radius**2 + (3 / 5) * mass * height**2
    Izz = (3 / 10) * mass * radius**2

    # Create the moment of inertia matrix [Ixx, Iyy, Izz]
    I= [
        [Ixx, 0, 0],
        [0, Iyy, 0],
        [0, 0, Izz]
    ]
    comp.mass_properties.moment_of_intertia = I
    return     

#-----------------------------------------
# fuselage trial MOI
#-----------------------------------------

def moment_of_inertia_fuselage(fuselage):
    """
    Calculate the total moment of inertia matrix for a fuselage composed of three sections:
    nose cone, cylinder, and tail cone.

    Parameters:
    - mass_nose_cone: Mass of the nose cone in kg
    - mass_cylinder: Mass of the cylinder section in kg
    - mass_tail_cone: Mass of the tail cone in kg
    - radius_nose_cone: Radius of the nose cone base in meters
    - height_nose_cone: Height of the nose cone in meters
    - radius_cylinder: Radius of the cylinder base in meters
    - height_cylinder: Height of the cylinder in meters
    - radius_tail_cone: Radius of the tail cone base in meters
    - height_tail_cone: Height of the tail cone in meters

    Returns:
    - Total moment of inertia matrix 3x3 [Ixx, Iyy, Izz]
    """
    mass_nose_cone
    mass_cylinder
    mass_tail_cone
    radius_nose_cone
    height_nose_cone
    adius_cylinder
    height_cylinder
    radius_tail_cone
    height_tail_cone
                               
    # Calculate the moments of inertia for each section
    I_nose_cone = moment_of_inertia_cone(mass_nose_cone, radius_nose_cone, height_nose_cone)
    I_cylinder  = moment_of_inertia_cylinder(mass_cylinder, radius_cylinder, height_cylinder)
    I_tail_cone = moment_of_inertia_cone(mass_tail_cone, radius_tail_cone, height_tail_cone)

    # Sum the moments of inertia for all sections
    I = I_nose_cone + I_cylinder + I_tail_cone
    
    
    
    
    
    
    fuselage.mass_properties.moment_of_inertia = I

    return 







