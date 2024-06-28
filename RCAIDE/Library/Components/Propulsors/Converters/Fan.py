## @ingroup Components-Propulsors-Converters
# RCAIDE/Library/Components/Propulsors/Converters/Fan.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Feb 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from RCAIDE.Library.Components                      import Component  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Fan  
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Components-Propulsors-Converters
class Fan(Component):
    """This is a fan component typically used in a turbofan. 
    """
    
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
            Pressure ratio and efficiency do not change with varying conditions.

        Source:
            https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/ 
        """         
        #set the default values
        self.tag                            = 'Fan'
        self.polytropic_efficiency          = 1.0
        self.pressure_ratio                 = 1.0
        self.angular_velocity               = 0   
        self.inputs.stagnation_temperature  = 0.
        self.inputs.stagnation_pressure     = 0.
        self.outputs.stagnation_temperature = 0.
        self.outputs.stagnation_pressure    = 0.
        self.outputs.stagnation_enthalpy    = 0.