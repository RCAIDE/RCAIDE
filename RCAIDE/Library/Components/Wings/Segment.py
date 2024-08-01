# RCAIDE/Compoments/Wings/Segment.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from RCAIDE.Framework.Core import Data, Container
from RCAIDE.Library.Components import Component  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Segment
# ----------------------------------------------------------------------------------------------------------------------   
class Segment(Component):
    """ Wing segment compoment class.
    """
    def __defaults__(self):
        """This sets the default for wing segments.

        Assumptions:
            None

        Source:
            None 
        """         
        self.tag                     = 'segment'
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
            None

        Args:
            self    (dict): wing data structure
            airfoil (dict): airfoil data structure

        Returns:
            None

        """  
        # assert database type
        if not isinstance(airfoil,Data):
            raise Exception('input component must be of type Data()')

        # store data
        self.Airfoil.append(airfoil)

         
Segment_Container = Container         
