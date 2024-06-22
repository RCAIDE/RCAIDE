## @ingroup Library-Components-Wings
# RCAIDE/Compoments/Wings/Vertical_Tail.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from .Wing import Wing 
from copy import deepcopy 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Vertical_Tail
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Components-Wings    
class Vertical_Tail(Wing):
    """This class is used to define vertical tails RCAIDE

    Assumptions:
    None

    Source:
    N/A

    Args:
    None

    Returns:
    None

    Properties Used:
    N/A
    """ 
    def __defaults__(self):
        """This sets the default for vertical tails in RCAIDE.
    
        Assumptions:
        None

        Source:
        N/A

        Args:
        None

        Returns:
        None

        Properties Used:
        N/A
        """ 
        self.tag       = 'vertical_stabilizer'
        self.vertical  = True
        self.symmetric = False 
        
    def make_x_z_reflection(self):
        """This returns a Vertical_Tail class or subclass object that is the reflection
        of this object over the x-z plane. This is useful since if Vertical_Tail's symmetric 
        attribute is True, the symmetric wing gets reflected over the x-y plane.
        
        WARNING: this uses deepcopy to achieve its purpose. If this copies too many unwanted 
        attributes, it is recommended that the user should write their own code, taking 
        after the form of this function.
        
        It is also recommended that the user call this function after they set control surface
        or all moving surface deflections. This way the deflection is also properly reflected 
        to the other side
    
        Assumptions:
        None

        Source:
        N/A

        Args:
        None

        Returns:
        None

        Properties Used:
        N/A
        """    
        wing = deepcopy(self)
        wing.dihedral     *= -1
        wing.origin[0][1] *= -1
        
        for segment in wing.Segments:
            segment.dihedral_outboard *= -1
            
        for cs in wing.control_surfaces:
            cs.deflection *= -1*cs.sign_duplicate
                
        return wing 