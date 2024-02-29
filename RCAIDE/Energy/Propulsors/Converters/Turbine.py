## @ingroup Energy-Propulsors-Converters
# RCAIDE/Energy/Propulsors/Converters/Turbine.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports  
from RCAIDE.Energy.Energy_Component                      import Energy_Component   

# ---------------------------------------------------------------------------------------------------------------------- 
#  Turbine
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Energy-Propulsors-Converters
class Turbine(Energy_Component):
    """This is a turbine component typically used in a turbofan.
    Calling this class calls the compute function.
    
    Assumptions:
    Efficiencies do not change with varying conditions.

    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/
    """
    
    def __defaults__(self):
        """ This sets the default values for the component to function.

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
        #set the default values
        self.tag                               ='Turbine'
        self.mechanical_efficiency             = 1.0
        self.polytropic_efficiency             = 1.0
        self.inputs.stagnation_temperature     = 1.0
        self.inputs.stagnation_pressure        = 1.0
        self.inputs.fuel_to_air_ratio          = 1.0
        self.outputs.stagnation_temperature    = 1.0
        self.outputs.stagnation_pressure       = 1.0
        self.outputs.stagnation_enthalpy       = 1.0 
        self.inputs.shaft_power_off_take       = None
    