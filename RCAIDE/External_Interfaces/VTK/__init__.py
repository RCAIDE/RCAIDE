## @defgroup External_Interfaces-VTK VTK 
# @ingroup External_Interfaces
# RCAIDE/External_Interfaces/VTK/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

from Legacy.trunk.S.Input_Output.VTK.save_evaluation_points_vtk   import save_evaluation_points_vtk
from Legacy.trunk.S.Input_Output.VTK.save_fuselage_vtk            import save_fuselage_vtk            
from Legacy.trunk.S.Input_Output.VTK.save_prop_vtk                import save_prop_vtk          
from Legacy.trunk.S.Input_Output.VTK.save_prop_wake_vtk           import save_prop_wake_vtk          
from Legacy.trunk.S.Input_Output.VTK.save_vortex_distribution_vtk import save_vortex_distribution_vtk
from Legacy.trunk.S.Input_Output.VTK.save_wing_vtk                import save_wing_vtk               
from Legacy.trunk.S.Input_Output.VTK.store_wake_evolution_vtks    import store_wake_evolution_vtks
from Legacy.trunk.S.Input_Output.VTK.write_azimuthal_cell_values  import write_azimuthal_cell_values         
from .save_nacelle_vtk             import save_nacelle_vtk        
from .save_vehicle_vtk             import save_vehicle_vtk