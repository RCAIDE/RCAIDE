# RCAIDE/Energy/Distributors/Bus_Power_Control_Unit.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Energy.Energy_Component import Energy_Component
from RCAIDE.Components.Component    import Container   

# ----------------------------------------------------------------------------------------------------------------------
#  Bus_Power_Control_Unit
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Components-Energy-Distributors
class Bus_Power_Control_Unit(Energy_Component):
    """  This controls the flow of energy in to and from a battery-powered nework
        This includes the basic logic of the maximum power point tracker that modifies the voltage of the panels to
        extract maximum power.
    
        Assumptions:
        None
        
        Source:
        None
    """
    
    
    def __defaults__(self):
        """ This sets the default values.
    
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
        self.tag                           = 'bus'
        self.motors                        = Container()
        self.rotors                        = Container()
        self.electronic_speed_controllers  = Container()
        self.batteries                     = Container()
        self.fixed_voltage                 = True
        self.active_propulsor_groups       = None 
        self.efficiency                    = 1.0
        self.voltage                       = 0.0
        self.outputs.avionics_power        = 0.0
        self.outputs.payload_power         = 0.0
        self.outputs.total_esc_power       = 0.0    
        self.inputs.secondary_source_power = 0.0
        
    def logic(self,conditions,numerics):
        """ The power being sent to the battery
        
            Assumptions:
                the system voltage is constant
                the maximum power point is at a constant voltage
                
            Source:
            N/A
            
            Inputs:
            self.inputs:
                    secondary_source_power           [Watts]
                .outputs
                    avionics_power                   [Watts]
                    payload_power                    [Watts]
                    total_esc_power                  [Watts]

            Outputs:
            self.outputs.power                       [Watts]
                inputs.power                         [Watts]

        """
        # Unpack
        pin         = self.inputs.secondary_source_power
        pavionics   = self.outputs.avionics_power
        ppayload    = self.outputs.payload_power
        pesc        = self.outputs.total_esc_power   
        
        # outputs from bus    
        self.outputs.power    = pavionics + ppayload + pesc - pin
        
        # inputs to bus
        self.inputs.power     = self.outputs.power/self.efficiency
        return 