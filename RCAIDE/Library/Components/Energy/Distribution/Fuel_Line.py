## @defgroup Energy-Networks-Distribution
# RCAIDE/Energy/Networks/Distribution/Fuel_Line.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Components                                import Component
from RCAIDE.Components.Component                      import Container    

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Line
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Networks-Distribution
class Fuel_Line(Component):
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