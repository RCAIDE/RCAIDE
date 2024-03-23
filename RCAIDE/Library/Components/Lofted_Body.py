## @ingroup Library-Compoments
# RCAIDE/Library/Compoments/Lofted_Body.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

from .Component                    import Component 
from RCAIDE.Framework.Core         import DataOrdered


# ----------------------------------------------------------------------------------------------------------------------
#  Lofted Body
# ----------------------------------------------------------------------------------------------------------------------        
## @ingroup Library-Components 
class Lofted_Body(Component):
    def __defaults__(self):
        """This sets the default values.
    
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
        self.tag      = 'Lofted_Body'
        self.Segments = DataOrdered() # think edges
    
   
# ------------------------------------------------------------
#  Segment
# ------------------------------------------------------------

## @ingroup Components
class Segment(Component):
    """ A class that stubs out what a segment is
    
    Assumptions:
    None
    
    Source:
    None
    """      
    def __defaults__(self):
        """This sets the default values.
    
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
        self.tag = 'Segment'
        
        self.prev = None
        self.next = None # for connectivity

# ------------------------------------------------------------
#  Section
# ------------------------------------------------------------

## @ingroup Components
class Section(Component):
    """ A class that stubs out what a section is
    
    Assumptions:
    None
    
    Source:
    None
    """     
    def __defaults__(self):
        """This sets the default values.
    
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
        self.tag = 'Section'
                
        self.prev = None
        self.next = None
        
        
# ------------------------------------------------------------
#  Containers
# ------------------------------------------------------------

## @ingroup Components
class Section_Container(Component.Container):
    """ This does nothing
    
    Assumptions:
    None
    
    Source:
    None
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


# ------------------------------------------------------------
#  Handle Linking
# ------------------------------------------------------------

Section.Container   = Section_Container
Lofted_Body.Section = Section
Lofted_Body.Segment = Segment



