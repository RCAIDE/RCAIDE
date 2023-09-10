# RCAIDE/Energy/Distributors/Fuel_Line.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Energy.Energy_Component                   import Energy_Component
from RCAIDE.Components.Component                      import Container    

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Line
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Components-Energy-Distributors
class Fuel_Line(Energy_Component):
    """  This controls the flow of energy into and from a fuel-powered nework 
    
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
        self.tag                           = 'fuel_line' 
        self.rotors                        = Container() 
        self.engines                       = Container() 
        self.fuel_tanks                    = Container()  
        self.active_propulsor_groups       = None 
        self.efficiency                    = 1.0 
        
    def logic(self,conditions,numerics):
        """ Determines the fuel supply disturbution on an fuel-powered network
        
            Assumptions: 
                
            Source:
            N/A
            
            Inputs: 

            Outputs: 
        """
        # Unpack 
        return 
