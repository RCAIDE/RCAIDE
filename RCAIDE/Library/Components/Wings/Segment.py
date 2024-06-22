## @ingroup Library-Components-Wings
# RCAIDE/Compoments/Wings/Segment.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from RCAIDE.Framework.Core import Data, Container
from RCAIDE.Library.Components import Component  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Segment
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Components-Wings  
class Segment(Component):
    def __defaults__(self):
        """This sets the default for wing segments in RCAIDE.

        Assumptions:
        None

        Source:
        N/A

        Args:
        None

        Returns:
        None

        """         
        self.tag                     = 'segment'
        self.prev                    = None
        self.next                    = None  
        self.percent_span_location   = 0.0
        self.twist                   = 0.0
        self.taper                   = 0.0
        self.root_chord_percent      = 0.0
        self.dihedral_outboard       = 0.0
        self.thickness_to_chord      = 0.0
        
        self.sweeps                  = Data()
        self.sweeps.quarter_chord    = 0.0
        self.sweeps.leading_edge     = None
    
        self.chords                  = Data()
        self.chords.mean_aerodynamic = 0.0
        
        self.areas                   = Data()
        self.areas.reference         = 0.0
        self.areas.exposed           = 0.0
        self.areas.wetted            = 0.0

        self.Airfoil                 = Container()    
   
        
        
    def append_airfoil(self,airfoil):
        """ Adds an airfoil to the segment

        Assumptions:
        None

        Source:
        N/A

        Args:
        None

        Returns:
        None

        """  
        # assert database type
        if not isinstance(airfoil,Data):
            raise Exception('input component must be of type Data()')

        # store data
        self.Airfoil.append(airfoil)

        
## @ingroup Components-Wings
class Segment_Container(Container):
    """ Container for wing segment
    
    Assumptions:
    None

    Source:
    N/A

    Args:
    None

    Returns:
    None


    """     

    def get_children(self):
        """ Returns the components that can go inside
        
        Assumptions:
        None
    
        Source:
        N/A
    
        Args:
        None
    
        Returns:
        None
    
        """       
        
        return []
