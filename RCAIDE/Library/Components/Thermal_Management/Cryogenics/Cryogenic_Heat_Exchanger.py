## @ingroup Library-Compoments-Thermal_Management-Cryogenics
# RCAIDE/Library/Compoments/Thermal_Management/Cryogenics/Cryogenic_Heat_Exchange.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
import RCAIDE 
from RCAIDE.Library.Components import Component  
from RCAIDE.Library.Methods.Thermal_Management.Cryogenics.compute_cryogen_mass_flow_rate import compute_cryogen_mass_flow_rate
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Cryogenic Heat Exchanger Component
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Compoments-Thermal_Management-Cryogenics
class Cryogenic_Heat_Exchanger(Component):
    """This provides output values for a heat exchanger used to cool cryogenic components
    """
    
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
            None

        Source:
            None
        """                 
        self.tag                            = 'Cryogenic_Heat_Exchanger' 
        self.cryogen                        = RCAIDE.Library.Attributes.Cryogens.Liquid_Hydrogen()
        self.cryogen_inlet_temperature      =    300.0      # [K]
        self.cryogen_outlet_temperature     =    300.0      # [K]
        self.cryogen_pressure               = 100000.0      # [Pa]
        self.cryogen_is_fuel                =      0.0      # Proportion of cryogen that is burned as fuel. Assumes the cryogen is the same as the fuel, e.g. that both are hydrogen.
        self.inputs.cooling_power           =      0.0      # [W]
        self.outputs.mdot                   =      0.0      #[kg/s]

    def energy_calc(self, conditions): 
        """ This calculates the mass of cryogen required to achieve the desired cooling power
        given the temperature of the cryogen supplied, and the desired temperature of the cryogenic equipment.

        Assumptions:
            Perfect thermal conduction of the cryogen to the cooled equipment.

        Source:
            None

        Args:
            self                       (dict): cryogen            [-]
            self.inputs.cooling_power (float): cooling power      [W]

        Returns: 
            mdot  (numpy.ndarray): mass flow of cryogenic heat exchanger  [kg/s] 
        
        """         
        # unpack 
        cryogen         = self.cryogen         
        temp_in         = self.cryogen_inlet_temperature 
        temp_out        = self.cryogen_outlet_temperature
        vent_pressure   = self.cryogen_pressure
        cooling_power   = self.inputs.cooling_power
        
        # calculate the cryogen mass flow
        mdot = compute_cryogen_mass_flow_rate(cryogen,temp_in,temp_out,cooling_power,vent_pressure)
        self.outputs.mdot = mdot
    
        return mdot
        
    