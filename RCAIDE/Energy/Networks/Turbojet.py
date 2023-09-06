## @ingroup Networks
# RCAIDE/Energy/Networks/Turbojet.py
# (c) Copyright 2023 Aerospace Research Community LLC
#
# Created:  Aug 2023, E. Botero
# Modified: 


# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------------------------------------------------------

from . import legacy_turbojet
from .Networks import Network


# ----------------------------------------------------------------------------------------------------------------------
#  Turbojet Network
# ----------------------------------------------------------------------------------------------------------------------

class Turbojet(Network,legacy_turbojet):
    """ Turbojet Energy Network
        The Top Level Network Class
            Assumptions:
            None
            Source:
            N/As
    """    
    def __defaults__(self):
        """ This sets the default attributes for the network.
                Assumptions:
                None
                Source:
                N/A
                Inputs:
                None
                Outputs:
                None
                Properties Used:
        """
