## @ingroup Energy-Distributors
# RCAIDE/Energy/Distributors/Electronic_Speed_Controller.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Energy.Energy_Component import Energy_Component
 
# ----------------------------------------------------------------------------------------------------------------------
#  Electronic Speed Controller Class
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Distributors
class Electronic_Speed_Controller(Energy_Component):
    
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

        self.tag              = 'electronic_speed_controller'  
        self.efficiency       = 0.0       
    
    def calculate_voltage_out_from_throttle(self,eta):
        """ The voltage out of the electronic speed controller
        
            Assumptions:
            The ESC's output voltage is linearly related to throttle setting
    
            Source:
            N/A
    
            Inputs:
            conditions.energy.throttle     [0-1] 
            self.inputs.voltage            [volts]
    
            Outputs:
            voltsout                       [volts]
            self.outputs.voltageout        [volts]
    
            Properties Used:
            None
           
        """ 
        # Negative throttle is bad
        eta[eta<=0.0] = 0.0
        
        # Cap the throttle
        eta[eta>=1.0] = 1.0
        voltsout = eta*self.inputs.voltage
        
        # Pack the output
        self.outputs.voltage  = voltsout
        
        return

    def calculate_voltage_in_from_throttle(self,eta):
        """ The voltage out of the electronic speed controller

            Assumptions:
            The ESC's output voltage is linearly related to throttle setting

            Source:
            N/A

            Inputs:
            conditions.energy.throttle     [0-1]
            self.inputs.voltage            [volts]

            Outputs:
            voltsout                       [volts]
            self.outputs.voltageout        [volts]

            Properties Used:
            None

        """
        # Negative throttle is bad
        eta[eta<=0.0] = 0.0

        # Cap the throttle
        eta[eta>=1.0] = 1.0
        voltsin = self.outputs.voltage/eta

        # Pack the output
        self.inputs.throttle = eta
        self.inputs.voltage  = voltsin

        return

    def calculate_throttle_from_voltages(self):

        """ The voltage out of the electronic speed controller

            Assumptions:
            The ESC's output voltage is linearly related to throttle setting

            Source:
            N/A

            Inputs:
            conditions.energy.throttle     [0-1]
            self.inputs.voltage            [volts]

            Outputs:
            voltsout                       [volts]
            self.outputs.voltageout        [volts]
    
            Properties Used:
            None

        """
        eta  = self.outputs.voltage/self.inputs.voltage

        # Negative throttle is bad
        eta[eta<=0.0] = 0.0

        # Cap the throttle
        eta[eta>=1.0] = 1.0
        self.inputs.throttle = eta
        return

    def calculate_current_in_from_throttle(self,eta):
        """ The current going into the speed controller
        
            Assumptions:
                The ESC draws current.
            
            Inputs:
                self.inputs.currentout [amps]
               
            Outputs:
                outputs.currentin      [amps]
            
            Properties Used:
                self.efficiency - [0-1] efficiency of the ESC
               
        """
        
        # Unpack, don't modify the throttle   
        eff        = self.efficiency
        currentout = self.outputs.current 
        currentin  = currentout*eta/eff # The inclusion of eta satisfies a power balance: p_in = p_out/eff
        
        # Pack 
        self.inputs.current   = currentin
        self.inputs.power     = self.inputs.voltage *currentin
        
        return