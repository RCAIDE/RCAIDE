## @defgroup Energy-Networks-Distribution
# RCAIDE/Energy/Networks/Distribution/Fuel_Line.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Energy.Energy_Component                   import Energy_Component

from Legacy.trunk.S.Components.Physical_Component     import Container 

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Line
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Networks-Distribution
class Fuel_Line(Energy_Component):
    """  This controls the flow of energy into and from a fuel-Energy-Sourcesed nework 
    
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
        self.fuel_tanks                    = Container()
        self.propulsors                    = Container()
        self.identical_propulsors          = True 
        self.active                        = True 
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
