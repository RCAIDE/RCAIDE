## @ingroup Components-Propulsors-Converters
# RCAIDE/Library/Components/Propulsors/Converters/DC_Motor.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Library.Components import Component
from RCAIDE.Library.Methods.Propulsors.Converters.DC_Motor.append_motor_conditions import  append_motor_conditions
from RCAIDE.Library.Methods.Propulsors.Converters.DC_Motor import compute_RPM_and_torque_from_power_coefficent_and_voltage , compute_current_from_RPM_and_voltage


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
        
    def compute_omega(self,motor_conditions,freestream): 
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
         
        compute_RPM_and_torque_from_power_coefficent_and_voltage(self,motor_conditions,freestream)    
        
        return 
    
    def compute_current_draw(self,motor_conditions,freestream):
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
         
        compute_current_from_RPM_and_voltage(self,motor_conditions,freestream)        
        
        return

    def append_operating_conditions(self,segment,bus,propulsor):
        propulsor_conditions =  segment.state.conditions.energy[bus.tag][propulsor.tag]
        append_motor_conditions(self,segment,propulsor_conditions)
        return
    