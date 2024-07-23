# RCAIDE/Library/Methods/Geometry/Two_Dimensional/Airfoil/convert_airfoil_to_meshgrid.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# convert_airfoil_to_meshgrid
# ----------------------------------------------------------------------------------------------------------------------   
def convert_airfoil_to_meshgrid(airfoil_geometry, *args, **kwargs):
    """Converts an airfoil geometry representation to a numpy meshgrid array mask of boolean values.

    Assumptions:
        None

    Source:
        None

    Args:
        airfoil_geometry               (dict): [-]   
            .x_lower_surf     (numpy.ndarray): [unitless]
            .y_lower_surf     (numpy.ndarray): [unitless]
            .y_upper_surface  (numpy.ndarray): [unitless]

    Returns:  
        airfoil_mask          (numpy.ndarray,bool):

	
    """

    # Unpack Values 
    x_lower_surf = airfoil_geometry.x_lower_surf
    y_lower_surf = airfoil_geometry.y_lower_surf
    y_upper_surface = airfoil_geometry.y_upper_surface

    # Determine necessary resolution of the meshgrid. We do this by dividing the
    # x-length of the lower surface by the minimum separation between
    # any two x-coordinates of the geometry (ceil-rounded to an int). Later
    # we'll instantiate the meshgrid with this number of x-indices, so that the
    # separation between any two points in the meshgrid is equal to the minimum
    # separation between any two x-coordinates.

    x_length = (np.max(x_lower_surf)) 
    Nx       = int(np.ceil(x_length / np.abs(np.min(np.diff(x_lower_surf)))))

    # We determine the necessary number of y-coordinate points by taking the
    # maximum separation between the highest point of the upper surface and the
    # lowest point of the lower surface and multiplying that by the number of
    # x-points in order to re-normalize to our future meshgrid coordinates,
    # then ciel-rounding to an int.

    Ny = int(np.ceil(Nx * ( np.max(y_upper_surface) - np.min(y_lower_surf) )))

    # Instantiate the meshgrid, using ij-indexing so that X[i,j] returns i
    # for all points, and Y[i,j] returns j for all coordinates. 
    X, Y = np.meshgrid(np.arange(Nx), np.arange(Ny), indexing="ij")

    # Create the indexing arrays for the meshgrid. These convert the airfoil
    # geometry coordinates into meshgrid array indices. The x_indices are found
    # just by multplying/stretching the x_lower_surface coordinates across the
    # number of x-coodinates in the meshgrid. 
    x_indices = int(np.ceil(Nx / x_length * x_lower_surf))

    # The Y_INDICES are similarly stretched, but first are offset by the
    # minimum of the lower surface to bring them to a relative zero 
    y_lower_indices = int(np.floor( Nx / x_length * ( y_lower_surf - np.min(y_lower_surf)))) 
    y_upper_indices = int(np.ceil( Nx /x_length * ( y_upper_surface - np.min(y_lower_surf))))

    # We then repeat the elements of the Y_INDICES by the number of gridpoints
    # between each x-coordinate, essentially treating the y-surface as flat
    # between those points. We trim the final point by telling it to repeat 0
    # times 
    num_reps = np.append(np.diff(x_indices), 0 )

    # Need to hand the case where the x_indices aren't sorted, and swap
    # some elements around to allow the masks to be created

    if np.any(num_reps<0): 
        reg_reps = np.where(num_reps<0)[0]

        if np.any(np.diff(reg_reps) == 1):
            print("Airfoil geometry contains sequential negative x-steps. Meshing Failed.")
            return None

        (x_indices[reg_reps],x_indices[reg_reps + 1]) = (x_indices[reg_reps + 1], x_indices[reg_reps])

        (y_lower_indices[reg_reps],  y_lower_indices[reg_reps + 1]) = (y_lower_indices[reg_reps + 1], y_lower_indices[reg_reps])

        (y_upper_indices[reg_reps], y_upper_indices[reg_reps + 1]) = (y_upper_indices[reg_reps + 1], y_upper_indices[reg_reps])

        num_reps = np.append( np.diff(x_indices), 0 )

        Nx = np.sum(num_reps) 
        Ny = int(np.ceil( Nx * (np.max(y_upper_surface) - np.min(y_lower_surf))))

        X, Y = np.meshgrid(np.arange(Nx), np.arange(Ny), indexing="ij")

    y_lower_indices = np.repeat(y_lower_indices, num_reps)
    y_upper_indices = np.repeat(y_upper_indices, num_reps)

    # We then create masks for the upper and lower surfaces by tiling the
    # indices over the meshgrid (taking a transpose to comport with our earlier
    # indexing style).

    y_lower_grid = np.tile(y_lower_indices, (Ny,1)).T
    y_upper_grid = np.tile(y_upper_indices, (Ny,1)).T

    # We then create our airfoil meshgrid mask by comparing our Y coordinates
    # from the meshgrid to our upper and lower grids, intermediately treating
    # them as ints to simplify the multi-condition comparison

    y_lower = (Y > y_lower_grid).astype(int)
    y_upper = (Y < y_upper_grid).astype(int)

    airfoil_mask = (y_lower + y_upper) > 1

    return airfoil_mask
