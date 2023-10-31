## @ingroup External_Interfaces-VTK
# save_nacelle_vtk.py
#
# Created:    Oct 2023, Racheal M. Erhard
# Modified:
#

#------------------------------
# Imports
#------------------------------

from Legacy.trunk.S.Input_Output.VTK.save_nacelle_vtk import write_nacelle_data
from RCAIDE.Visualization.Geometry.plot_vehicle import generate_nacelle_points
import numpy as np

#------------------------------
# Nacelle VTK generation
#------------------------------
## @ingroup Input_Output-VTK
def save_nacelle_vtk(nacelle, filename, Results, origin_offset):
    """
    Saves a SUAVE nacelle object as a VTK in legacy format.

    Inputs:
       nacelle        Data structure of SUAVE nacelle                [Unitless]
       filename       Name of vtk file to save                       [String]
       Results        Data structure of wing and propeller results   [Unitless]

    Outputs:
       N/A

    Properties Used:
       N/A

    Assumptions:
       N/A

    Source:
       None

    """

    nac_pts = generate_nacelle_points(nacelle)
    num_nac_segs = np.shape(nac_pts)[0]
    if num_nac_segs == 0:
        print("No nacelle segments found!")
    else:
        write_nacelle_data(nac_pts,filename,origin_offset)

    return
