# RCAIDE/Library/Components/Powertrain/Systems/Hydraulics.py
# 
# Created:  Jan 2026, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from .Systems import Systems
from RCAIDE.Library.Methods.Powertrain.Systems.append_hydraulics_conditions import append_hydraulics_conditions
 
# ----------------------------------------------------------------------------------------------------------------------
#  Hydraulics
# ----------------------------------------------------------------------------------------------------------------------            
class Hydraulics(Systems):
    """
    A class representing hydraulic systems and their power requirements. 
    """        
    def __defaults__(self):
        """
        Sets default values for the hydraulic system attributes.
        """                  
        self.tag        = 'hydraulic' 
        
    def append_operating_conditions(self, segment, bus): 
        """
        Adds operating conditions for the hydraulic systems system to a mission segment.

        Parameters
        ----------
        segment : Data
            Mission segment to which conditions are being added
        bus : Data
            Electrical bus supplying power to the hydraulic systems
        """
        append_hydraulics_conditions(self, segment, bus)
        
        return