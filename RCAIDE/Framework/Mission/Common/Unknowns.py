## @ingroup Analyses-Mission-Segments-Conditions 
# RCAIDE/Framework/Analyses/Mission/Segments/Conditions/Unknowns.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from .Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Unknowns
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Analyses-Mission-Segments-Conditions
class Unknowns(Conditions):
    """ Creates the data structure for the unknowns that solved in a mission
    
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
        self.tag = 'unknowns'