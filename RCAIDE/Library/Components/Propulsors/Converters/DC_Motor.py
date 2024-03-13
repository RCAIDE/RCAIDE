## @ingroup Components-Propulsors-Converters
# RCAIDE/Library/Components/Propulsors/Converters/DC_Motor.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Library.Components import Component
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.DC_Motor import compute_omega_and_Q_from_Cp_and_V , compute_I_from_omega_and_V


# ----------------------------------------------------------------------------------------------------------------------
#  DC_Motor  
# ----------------------------------------------------------------------------------------------------------------------           
## @ingroup Components-Propulsors-Converters 
class DC_Motor(Component):
    """This is a motor component.
    
    Assumptions:
    None

    Source:
    None
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
        self.tag                = 'motor' 
        self.resistance         = 0.0
        self.no_load_current    = 0.0
        self.speed_constant     = 0.0
        self.rotor_radius       = 0.0
        self.rotor_Cp           = 0.0
        self.efficiency         = 1.0
        self.gear_ratio         = 1.0
        self.gearbox_efficiency = 1.0
        self.expected_current   = 0.0
        self.power_split_ratio  = 0.0
        self.design_torque      = 0.0
        self.wing_mounted       = False
        self.interpolated_func  = None
        
    def compute_omega(self,conditions): 
        """Calculates the motor's rotation rate
        
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
         
        compute_omega_and_Q_from_Cp_and_V(self,conditions)    
        
        return 
    
    def compute_current_draw(self):
        """Calculates the current draw from a DC motor 
        
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
         
        compute_I_from_omega_and_V(self)        
        
        return 