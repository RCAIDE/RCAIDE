# RCAIDE/Library/Compoments/Energy/Networks/Distribution/Fuel_Line.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Library.Components                                import Component
from RCAIDE.Library.Components.Component                      import Container    

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Line
# ----------------------------------------------------------------------------------------------------------------------  
class Fuel_Line(Component):
    """ Fuel line component class.
    """  
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """          
        self.tag                           = 'fuel_line'  
        self.fuel_tanks                    = Container()
        self.propulsors                    = Container()
        self.identical_propulsors          = True 
        self.active                        = True 
        self.efficiency                    = 1.0 