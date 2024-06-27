## @ingroup Library-Components-Fuselages
# RCAIDE/Library/Compoments/Fuselage/Segment.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from RCAIDE.Framework.Core import Container
from RCAIDE.Library.Components import Component  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Segment
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Components-Wings  
class Segment(Component):
    """Fuselage segment class.
    """
    def __defaults__(self): 
        """This sets the default for fuselage segments in RCAIDE.

        Assumptions:
           None

        Source:
           None
        """ 
        self.tag                     = 'segment'
        self.prev                    = None
        self.next                    = None    
        self.percent_x_location      = 0  
        self.percent_y_location      = 0
        self.percent_z_location      = 0 
        self.height                  = 0 
        self.width                   = 0 
        self.curvature               = 2
        
## @ingroup Components-Wings
class Segment_Container(Container):
    """ Container for fuselage segment.
    """     

    def get_children(self):
        """ Returns the components that can go inside
        
        Assumptions:
        None
    
        Source:
        None 
        """       
        
        return []