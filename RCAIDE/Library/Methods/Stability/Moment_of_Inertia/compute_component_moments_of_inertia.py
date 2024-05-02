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
# compute component moments of inertia
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Stability-Moment_of_Intertia
def compute_component_moments_of_inertia(vehicle): 
    ''' Computes the moments of inertia of each compoment on an aircraft 
    
    Source:
    Simplified Mass and Inertial Estimates for Aircraft with Components of Constant Density
    Moulton, B. C., and Hunsaker, D. F., “Simplified Mass and Inertial Estimates for Aircraft with Components 
    of Constant Density,” AIAA SCITECH 2023 Forum, January 2023, AIAA-2023-2432 DOI: 10.2514/
    6.2023-2432
    
    
    Assumtions:
    Assumes simplified shapes 
    
    Inputs:
    vehicle 
    
    Outputs:
    
    '''
    # moment of interia in wings 
    for wing in vehicle.wings:     
        wing_moment_of_inertia(wing)  
        
    # moment of inertia of fuselages 
    for fuselage in vehicle.fuselages: 
        outer_radius = fuselage.width   
        cylinder_moment_of_inertia(fuselage, outer_radius )  

    # moment of intertia of largest compoments in energy network 
    for network in vehicle.networks:
        for bus in network.busses:
            for propulsor in bus.propulsors:
                if 'motor' in propulsor:
                    motor        = propulsor.motor 
                    outer_radius = motor.rotor_radius 
                    height       = 1 # needs to be mentioned 
                    cylinder_moment_of_inertia(motor, height, outer_radius)
                if 'rotor' in propulsor:
                    pass 
                 
            for battery in bus.batteries: 
                outer_length = 2   #bat.lenght intialize inside the battery f
                outer_width  = 2
                outer_height = 4
                cubuid_moment_of_inertia(battery, outer_length, outer_width, outer_height)
             
        for fuel_line in network.fuel_lines:
            for propulsor in fuel_line.propulsors:
                if 'rotor' in propulsor:
                    pass

                if 'turbofan' in propulsor:
                    pass  
                
                if 'turbojet' in propulsor:
                    pass    
    return

# ----------------------------------------------------------------------------------------------------------------------
#  Cuboid Moment of Inertia 
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Stability-Moment_of_Intertia
def cubuid_moment_of_inertia(comp,outer_length, outer_width, outer_height, inner_length= 0, inner_width = 0, inner_height = 0 ):
    ''' Computes the moment of intertia of a component assuming a simplified cuboid shape
    
    
    Assumptions:
    The compoment is of a homogeneous medium

    Source: 
    Simplified Mass and Inertial Estimates for Aircraft with Components of Constant Density
    Moulton, B. C., and Hunsaker, D. F., “Simplified Mass and Inertial Estimates for Aircraft with Components 
    of Constant Density,” AIAA SCITECH 2023 Forum, January 2023, AIAA-2023-2432 DOI: 10.2514/
    6.2023-2432
     
    Inputs:
    compoment         - data structure of cylindrical       [-]
    outer_length      - external length of object (x-axis)  [m]
    inner_length      - internal length of object (x-axis)  [m]
    outer_width       - external length of object (y-axis)  [m]
    inner_width       - internal length of object (y-axis)  [m]
    outer_height      - external length of object (z-axis)  [m]
    inner_height      - internal length of object (z-axis)  [m] 
    
    Outputs:
    I                 - mass moment of inertia matrix    [kg-m^2]
    
    '''    
    m = comp.mass_properties.mass
    # Calculate the volumes
    V1 = inner_length * inner_width * inner_height
    V2 = outer_length * outer_width * outer_height

    # Calculate the moment of inertia tensor
    Ixx = (m / 12) * ((V2 * (outer_width**2 + outer_height**2)) - (V1 * (inner_width**2 + inner_height**2))) / (V2 - V1)
    Iyy = (m / 12) * ((V2 * (outer_length**2 + outer_height**2)) - (V1 * (inner_length**2 + inner_height**2))) / (V2 - V1)
    Izz = (m / 12) * ((V2 * (outer_length**2 + outer_width**2)) - (V1 * (inner_length**2 + inner_width**2))) / (V2 - V1)

    # Create the moment of inertia tensor as a numpy array
    I = np.array([[Ixx, 0, 0],
                  [0, Iyy, 0],
                  [0, 0, Izz]])

    comp.mass_properties.moment_of_intertia = I
    return 


# ----------------------------------------------------------------------------------------------------------------------
#  Cylinder Moment of Inertia 
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Stability-Moment_of_Intertia
def cylinder_moment_of_inertia(comp, height, outer_radius, inner_radius=0): 
    """Computes the moment of intertia of a component assuming a simplified cylinder  
    
    Assumptions: 
    The compoment is assumed to be a cylinder of a homogeneous medium

    Source: 
    Simplified Mass and Inertial Estimates for Aircraft with Components of Constant Density
    Moulton, B. C., and Hunsaker, D. F., “Simplified Mass and Inertial Estimates for Aircraft with Components 
    of Constant Density,” AIAA SCITECH 2023 Forum, January 2023, AIAA-2023-2432 DOI: 10.2514/
    6.2023-2432

    Inputs: 
    compoment         - data structure of cylindrical    [-]  
    outer_radius      - outer radius of cylinder         [-] 
    inner_radius      - inner radius of cylinder         [-] 

    Outputs: 
    I                 - mass moment of inertia matrix    [kg-m^2]
    """
    
    m = comp.mass_properties.mass
    
    # Calculate the components of the moment of inertia tensor
    Ixx = (m / 2) * (outer_radius**2 + inner_radius**2)
    Iyy = (m / 12) * (3 * (outer_radius**2 + inner_radius**2) + height**2)
    Izz = (m / 12) * (3 * (outer_radius**2 + inner_radius**2) + height**2)

    # Create the moment of inertia tensor as a numpy array
    I = np.array([[Ixx, 0, 0],
                  [0, Iyy, 0],
                  [0, 0, Izz]])

    comp.mass_properties.moment_of_intertia = I
    return
 

# ----------------------------------------------------------------------------------------------------------------------
#  Sing Moment of Inertia  
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Stability-Moment_of_Intertia
def wing_moment_of_inertia(wing): 
    """Computes the moment of intertia of a wing  
    
    Assumptions: 
    The compoment is of a homogeneous medium

    Source: 
    Simplified Mass and Inertial Estimates for Aircraft with Components of Constant Density
    Moulton, B. C., and Hunsaker, D. F., “Simplified Mass and Inertial Estimates for Aircraft with Components 
    of Constant Density,” AIAA SCITECH 2023 Forum, January 2023, AIAA-2023-2432 DOI: 10.2514/
    6.2023-2432

    Inputs: 
    wing          - data structure of wing       [-]

    Return: 
    """
        
    
    return       




