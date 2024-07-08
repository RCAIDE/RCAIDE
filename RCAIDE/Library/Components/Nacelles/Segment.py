# RCAIDE/Library/Compoments/Nacelles/Segment.py
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
class Segment(Component):
    def __defaults__(self): 
        """This sets the default for fuselage segments in RCAIDE.

        Assumptions:
            Cross-section of nacelle is a super ellipse defined
            |x/a|^n + |x/b|^n = 1 where n is the curvature.
            n = 2 defaulted to give rounded concave edges

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
        self.curvature                = 2  
         
class Segment_Container(Container):
    """ Container for nacelle segment. 
    """     

    def get_children(self):
        """ Returns the components that can go inside
        
        Assumptions:
            None
    
        Source:
            None
    
        Args:
            None
    
        Returns:
            None 
        """      
        return []