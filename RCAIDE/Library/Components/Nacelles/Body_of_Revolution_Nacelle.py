# RCAIDE/Compoments/Nacelles/Body_of_Revolution_Nacelle.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from RCAIDE.Framework.Core              import Data  
from .Nacelle import Nacelle
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Nacalle
# ----------------------------------------------------------------------------------------------------------------------  
class Body_of_Revolution_Nacelle(Nacelle):
    """ This is a body of revolution nacelle for a generic aircraft. 
    """
    
    def __defaults__(self):
        """ This sets the default values for the component to function.
        
        Assumptions:
            None
    
        Source:
            None 
        """      
        
        self.tag                       = 'body_of_revolution_nacelle' 
        self.Airfoil                   = Data()
    
    def append_airfoil(self,airfoil):
        """ Adds an airfoil to the segment 
    
        Assumptions:
            None

        Source:
            None

        Args:
            self    (dict): nacelle data structure 
            airfoil (dict): airfoil data structure 

        Returns:
            None 
        """ 

        # Assert database type
        if not isinstance(airfoil,Data):
            raise Exception('input component must be of type Data()')

        # Store data
        self.Airfoil.append(airfoil)

        return            