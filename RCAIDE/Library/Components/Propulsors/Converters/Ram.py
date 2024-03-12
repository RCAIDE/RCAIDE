## @ingroup Components-Propulsors-Converters
# RCAIDE/Components/Propulsors/Converters/Ram.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Feb 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from RCAIDE.Components                      import Component  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Fan Component
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Components-Propulsors-Converters
class Ram(Component):
    """This represent the compression of incoming air flow.
    Calling this class calls the compute function.

    Assumptions:
    None

    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/
    """

    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """
        #set the deafult values
        self.tag = 'Ram'
        self.outputs.stagnation_temperature  = 1.0
        self.outputs.stagnation_pressure     = 1.0
        self.inputs.working_fluid = Data()
 