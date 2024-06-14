## @ingroup Library-Components-Nacelles
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
## @ingroup Library-Components-Nacelles  
class Segment(Component):
    def __defaults__(self): 
        """This sets the default for fuselage segments in RCAIDE.

        Assumptions:
        Cross-section of nacelle is a super ellipse defined
        |x/a|^n + |x/b|^n = 1 where n is the curvature.
        n = 2 defaulted to give rounded concave edges

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """ 
        self.tag                      = 'segment' 
        self.orientation_euler_angles = [0.,0.,0.]  
        self.percent_x_location       = 0  
        self.percent_y_location       = 0
        self.percent_z_location       = 0 
        self.height                   = 0 
        self.width                    = 0 
        self.curvature                = 2  
        
## @ingroup Components-Nacelles
class Segment_Container(Container):
    """ Container for fuselage segment
    
    Assumptions:
    None

    Source:
    N/A

    Inputs:
    None

    Outputs:
    None

    Properties Used:
    N/A
    """     

    def get_children(self):
        """ Returns the components that can go inside
        
        Assumptions:
        None
    
        Source:
        N/A
    
        Inputs:
        None
    
        Outputs:
        None
    
        Properties Used:
        N/A
        """       
        
        return []