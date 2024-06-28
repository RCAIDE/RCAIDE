## @ingroup Components-Propulsors-Converters
# RCAIDE/Library/Components/Propulsors/Converters/Compressor.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Feb 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from RCAIDE.Library.Components                      import Component  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Compressor 
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Components-Propulsors-Converters 
class Compressor(Component):
    """This is a compressor component typically used in a turbofan or turbojet
    """
    
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
            None

        Source:
            None 
        """          
        #set the default values
        self.tag                             = 'Compressor'
        self.polytropic_efficiency           = 1.0
        self.pressure_ratio                  = 1.0
        self.inputs.stagnation_temperature   = 0.
        self.inputs.stagnation_pressure      = 0.
        self.outputs.stagnation_temperature  = 0.
        self.outputs.stagnation_pressure     = 0.
        self.outputs.stagnation_enthalpy     = 0.