## @ingroup Energy-Propulsors-Converters
# RCAIDE/Energy/Propulsors/Converters/Compression_Nozzle.py
# 
# 
# Created:  Feb 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from RCAIDE.Energy.Energy_Component                      import Energy_Component  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Compression Nozzle 
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Propulsors-Converters 
class Compression_Nozzle(Energy_Component):
    """This is a nozzle component intended for use in compression.
    Calling this class calls the compute function.

    Assumptions:
    Pressure ratio and efficiency do not change with varying conditions.
    Subsonic or choked output.

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
        #setting the default values
        self.tag = 'Nozzle'
        self.polytropic_efficiency           = 1.0
        self.pressure_ratio                  = 1.0
        self.pressure_recovery               = 1.0
        self.compressibility_effects         = False
        self.inputs.stagnation_temperature   = 0.0
        self.inputs.stagnation_pressure      = 0.0
        self.outputs.stagnation_temperature  = 0.0
        self.outputs.stagnation_pressure     = 0.0
        self.outputs.stagnation_enthalpy     = 0.0
        self.compression_levels              = 0.0
        self.theta                           = 0.0
