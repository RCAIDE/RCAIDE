## @ingroup Energy-Distribution
# RCAIDE/Energy/Distribution/Bus_Power_Control_Unit.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
import RCAIDE 
from RCAIDE.Energy.Energy_Component                   import Energy_Component
from RCAIDE.Components.Component                      import Container    

# ----------------------------------------------------------------------------------------------------------------------
#  Bus_Power_Control_Unit
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Distribution
class Bus_Power_Control_Unit(Energy_Component):
    """  This controls the flow of energy into and from a battery-powered nework 
    
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
        self.batteries                     = Container()
        self.propulsors                    = Container() 
        self.avionics                      = RCAIDE.Energy.Peripherals.Avionics()
        self.payload                       = RCAIDE.Energy.Peripherals.Payload()        
        self.identical_propulsors          = True  
        self.active                        = True
        self.efficiency                    = 1.0
        self.voltage                       = 0.0
        self.outputs.avionics_power        = 0.0
        self.outputs.payload_power         = 0.0
        self.outputs.total_esc_power       = 0.0    
        self.inputs.secondary_power        = 0.0
        
    def logic(self,conditions,numerics):
        """ Determines the power disturbution on a bus
        
            Assumptions: 
            N/A
                
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
        # Outputs of bus
        pavionics   = self.outputs.avionics_power
        ppayload    = self.outputs.payload_power
        pesc        = self.outputs.total_esc_power 
        voltage     = self.outputs.voltage
        
        # Secondary energy source to battery
        pin         = self.inputs.secondary_power
        
        # inputs form battery     
        self.inputs.power     = ((pavionics + ppayload + pesc) - pin)/self.efficiency
        self.inputs.current   = self.inputs.power/voltage
        return 
    