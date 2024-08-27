## @defgroup Library-Compoments-Energy-Networks-Distribution
# RCAIDE/Library/Compoments/Energy/Networks/Distribution/Coolant_Line.py 
# 
# Created:  Aug 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Library.Components                                import Component
from RCAIDE.Library.Components.Component                      import Container    

# ----------------------------------------------------------------------------------------------------------------------
#  Coolant Line
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Compoments-Energy-Networks-Distribution
class Coolant_Line(Component):
    """ Fuel line class.
    """ 
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """          
        self.tag                           = 'coolant_Line'  
        #self.reservoirs                     = Container()
        #self.heat_exchangers               = Container()
        #self.active                        = True 
        #self.efficiency                    = 1.0

                    
    def __init__ (self, distributor=None):
        
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """               
        self.active                        = True 
        self.efficiency                    = 1.0            
            
        for tag, item in  distributor.items():
            if tag == 'batteries':
                self.batteries  = Container()
                for battery in item:
                    self.batteries[battery.tag] = Container()
                
                    
        