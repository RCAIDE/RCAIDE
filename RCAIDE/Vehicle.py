## @defgroup Vehicle
# Vehicle.py
# (c) Copyright The Board of Trustees of RCAIDE
#
# Created:  Jul 2023, E. Botero
# Modified:  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S import Vehicle as VH
from Legacy.trunk.S.Components.Energy.Networks import Network as legacy_net
from .Energy.Networks import Network
from RCAIDE import Components , Energy



# ----------------------------------------------------------------------------------------------------------------------
#  VEHICLE
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Vehicle
class Vehicle(VH):
    """SUAVE Vehicle container class with database + input / output functionality
    
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
        self.pop('networks')
        self.networks  = Energy.Networks.Network.Container() 
        self.booms     = Components.Booms.Boom.Container()

    def __init__(self,*args,**kwarg):
        """ Sets up the component hierarchy for a vehicle
    
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
        # will set defaults
        super(Vehicle,self).__init__(*args,**kwarg) 

        self._component_root_map.pop(legacy_net)
        self._component_root_map[Network] = self['networks']
 
        return