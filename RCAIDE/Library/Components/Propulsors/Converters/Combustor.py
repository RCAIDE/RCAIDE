## @ingroup Components-Propulsors-Combustor
# RCAIDE/Library/Components/Propulsors/Converters/Combustor.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Feb 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from RCAIDE.Library.Components                      import Component  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Combustor
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Components-Propulsors-Converters 
class Combustor(Component):
    """This is a combustor compoment class.
    """
    
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
        None

        Source:
        None 
        """         
        
        self.tag                             = 'Combustor' 
        self.alphac                          = 0.0
        self.turbine_inlet_temperature       = 1.0
        self.inputs.stagnation_temperature   = 1.0
        self.inputs.stagnation_pressure      = 1.0
        self.inputs.static_pressure          = 1.0
        self.inputs.mach_number              = 0.1
        self.outputs.stagnation_temperature  = 1.0
        self.outputs.stagnation_pressure     = 1.0
        self.outputs.static_pressure         = 1.0
        self.outputs.stagnation_enthalpy     = 1.0
        self.outputs.fuel_to_air_ratio       = 1.0 
        self.area_ratio                      = 1.0
        self.axial_fuel_velocity_ratio       = 0.0
        self.fuel_velocity_ratio             = 0.0
        self.burner_drag_coefficient         = 0.0
        self.absolute_sensible_enthalpy      = 0.0
        self.fuel_equivalency_ratio          = 1.0        
        self.inputs.nondim_mass_ratio        = 1.0 # allows fuel already burned to be added to the flow 
    
