# RCAIDE/Library/Compoments/Nacelles/Segment.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from RCAIDE.Framework.Core import Container
from RCAIDE.Library.Components import Component  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Segment
# ----------------------------------------------------------------------------------------------------------------------  
class Segment(Component):
    def __defaults__(self): 
        """This sets the default for fuselage segments in RCAIDE.

        Assumptions:
            Cross-section of nacelle is an ellipse defined
            |x/a| + |x/b| = 1.

        Source:
            None

        Args:
            None

        Returns:
            None 
        """ 
        self.tag                      = 'segment' 
        self.orientation_euler_angles = [0.,0.,0.]  
        self.percent_x_location       = 0  
        self.percent_y_location       = 0
        self.percent_z_location       = 0 
        self.height                   = 0 
        self.width                    = 0 
        
Segment.Container = Container