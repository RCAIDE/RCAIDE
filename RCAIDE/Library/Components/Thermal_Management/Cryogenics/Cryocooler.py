## @ingroup Library-Compoments-Thermal_Management-Cryogenics
# RCAIDE/Library/Compoments/Thermal_Management/Cryogenics/Cryocooler.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Library.Components import Component  
from RCAIDE.Library.Methods.Thermal_Management.Cryogenics.cryocooler_model import cryocooler_model

# ---------------------------------------------------------------------------------------------------------------------- 
#  Cryocooler
# ----------------------------------------------------------------------------------------------------------------------     
## @ingroup Library-Compoments-Thermal_Management-Cryogenics
class Cryocooler(Component):    
    """
    Cryocooler provides cooling power to cryogenic components.
    Energy is used by this component to provide the cooling, despite the cooling power provided also being an energy inflow.
    """
    def __defaults__(self):
        """This sets the default.

        Assumptions:
            None

        Source:
            None 
        """                
        
        # Initialise cryocooler properties as null values
        self.cooler_type                    = None
        self.rated_power                    = 0.0
        self.min_cryo_temp                  = 0.0 
        self.ambient_temp                   = 300.0
        self.inputs.cooling_power           = 0.0
        self.inputs.cryo_temp               = 0.0
        self.mass_properties.mass           = 0.0
        self.rated_power                    = 0.0
        self.outputs.input_power            = 0.0

    def energy_calc(self, conditions): 
        """Calculate the instantaneous required energy input

        Assumptions:
            None

        Source:
            None

        Inputs:
            self (dict): cryocooler data structure [-]

        Outputs:
            self.outputs.input_power (numpy.ndarray): power of cryocooler    [W] 

    """ 
        output = cryocooler_model(self)
        self.outputs.input_power = output[0]

        return output[0]

    

