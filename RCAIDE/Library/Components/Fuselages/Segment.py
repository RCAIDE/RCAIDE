# RCAIDE/Library/Compoments/Fuselage/Segment.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from RCAIDE.Reference.Core import Container
from RCAIDE.Library.Components import Component  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Segment
# ----------------------------------------------------------------------------------------------------------------------   
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
        self.percent_x_location      = 0  
        self.percent_y_location      = 0
        self.percent_z_location      = 0 
        self.height                  = 0 
        self.width                   = 0 
        
Segment.Container = Container