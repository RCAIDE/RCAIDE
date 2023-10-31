## @ingroup Input_Output-VTK
# save_vehicle_vtks.py
#
# Created:    Jun 2021, R. Erhard
# Modified:   Jul 2022, R. Erhard
#

#----------------------------
# Imports
#----------------------------

from Legacy.trunk.S.Input_Output.VTK.save_vehicle_vtk import save_vehicle_vtk as save_vehicle_vtk_legacy
from .save_nacelle_vtk import save_nacelle_vtk

from Legacy.trunk.S.Core import Data
import numpy as np

## @ingroup Input_Output-VTK
def save_vehicle_vtk(vehicle, conditions=None, Results=Data(),
                      time_step=0,origin_offset=np.array([0.,0.,0.]),VLM_settings=None, aircraftReferenceFrame=True,
                      prop_filename="propeller.vtk", rot_filename="rotor.vtk",
                      wake_filename="prop_wake.vtk", wing_vlm_filename="wing_vlm_horseshoes.vtk",wing_filename="wing_vlm.vtk",
                      fuselage_filename="fuselage.vtk", nacelle_filename="nacelle.vtk", save_loc=None):
    """
    Saves SUAVE vehicle components as VTK files in legacy format.

    Inputs:
       vehicle                Data structure of SUAVE vehicle                    [Unitless]
       settings               Settings for aerodynamic analysis                  [Unitless]
       Results                Data structure of wing and propeller results       [Unitless]
       time_step              Simulation time step                               [Unitless]
       prop_filename          Name of vtk file to save                           [String]
       rot_filename           Name of vtk file to save                           [String]
       wake_filename          Name of vtk file to save                           [String]
       wing_filename          Name of vtk file to save                           [String]
       fuselage_filename      Name of vtk file to save                           [String]
       save_loc               Location at which to save vtk files                [String]

    Outputs:
       N/A

    Properties Used:
       N/A

    Assumptions:
       Quad cell structures for mesh

    Source:
       None

    """

    save_vehicle_vtk_legacy(vehicle, conditions, Results,
                      time_step,origin_offset,VLM_settings, aircraftReferenceFrame,
                      prop_filename, rot_filename,
                      wake_filename, wing_vlm_filename,wing_filename,
                      fuselage_filename, nacelle_filename, save_loc)
    
    #------------------------------
    # Save nacelles to vtk
    #------------------------------
    nacelles = vehicle.nacelles
    for i, nacelle in enumerate(nacelles):
        if save_loc is None:
            filename = nacelle_filename
        else:
            filename = f"{save_loc}{nacelle_filename}"
        sep  = filename.rfind('.')
        file = f"{filename[0:sep]}{i}_t{time_step}{filename[sep:]}"

        save_nacelle_vtk(nacelle, file, Results, origin_offset)
    return
