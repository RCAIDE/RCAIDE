## @ingroup Framework-Mission-Segments-Conditions 
# RCAIDE/Framework/Mission/Segments/Conditions/Unknowns.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from .Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Unknowns
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Framework-Mission-Segments-Conditions
class Unknowns(Conditions):
    """ Creates the data structure for the unknowns that solved in a mission.
    """     
    
    def __defaults__(self):
        """This sets the default values.
    
            Assumptions:
            None
    
            Source:
            None 
        """           
        self.tag = 'unknowns'