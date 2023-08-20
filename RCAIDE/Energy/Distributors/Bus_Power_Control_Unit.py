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

# package imports
import numpy as np

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
        self.tag                          = 'bus'
        self.motors                       = Container()
        self.rotors                       = Container()
        self.electronic_speed_controllers = Container()
        self.batteries                    = Container()
        self.fixed_voltage                = True
        self.battery_power_split_ratios   = [1.0]
        self.voltage                      = 0.0
        self.active_propulsor_groups      = [True] 

    def logic(self,conditions,numerics,voltage,efficiency = 1.0):
        """ The power being sent to the battery
        
            Assumptions:
                the system voltage is constant
                the maximum power point is at a constant voltage
                
            Source:
            N/A
            
            Inputs:
                self.inputs:
                    powerin
                    avionics_power
                    payload_power
                    esc_current
                numerics.time.integrate

            Outputs:
                self.outputs:
                    current
                    power_in
                    energy_transfer
                    
            Properties Used:
                self.MPPT_efficiency

        """
        #Unpack
        #pin         = self.inputs.secondary_source_power
        pavionics   = self.inputs.avionics_power
        ppayload    = self.inputs.payload_power
        esccurrent  = self.inputs.esc_current 
        #I           = numerics.time.integrate
        
        #pavail      = pin*efficiency
        #plevel      = pavail -pavionics -ppayload - voltage*esccurrent
        plevel      =  -pavionics -ppayload - voltage*esccurrent
        
        # Integrate the plevel over time to assess the energy consumption
        # or energy storage
        #e = np.dot(I,plevel)
        
        # Send or take power out of the battery, Pack up
        self.outputs.current         = (plevel/voltage)
        self.outputs.power           = plevel
        #self.outputs.energy_transfer = e 
        
        return 