# RCAIDE/Library/Components/Propulsors/Converters/Combustor.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Feb 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from RCAIDE.Library.Components                      import Component
from RCAIDE.Library.Methods.Propulsors.Converters.Combustor.append_combustor_conditions import  append_combustor_conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  Combustor
# ---------------------------------------------------------------------------------------------------------------------- 
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
        self.area_ratio                      = 1.0
        self.axial_fuel_velocity_ratio       = 0.0
        self.fuel_velocity_ratio             = 0.0
        self.burner_drag_coefficient         = 0.0
        self.absolute_sensible_enthalpy      = 0.0
        self.fuel_equivalency_ratio          = 1.0        
    
    def append_operating_conditions(self,segment,fuel_line,propulsor):
        propulsor_conditions =  segment.state.conditions.energy[fuel_line.tag][propulsor.tag]
        append_combustor_conditions(self,segment,propulsor_conditions)
        return
