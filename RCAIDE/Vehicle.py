## @defgroup Vehicle
# Vehicle.py
# (c) Copyright 2023 Aerospace Research Community LLC
#
# Created:  Jul 2023, E. Botero
# Modified: 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from Legacy.trunk.S import Vehicle as VH
from Legacy.trunk.S.Components.Energy.Networks import Network as legacy_net
from .Energy.Networks import Network


# ----------------------------------------------------------------------
#  Vehicle Data Class
# ----------------------------------------------------------------------

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

        self.networks  = Network.Container()
        #self.booms     = 

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
        self.__defaults__()

        self._component_root_map.pop(legacy_net)
        self._component_root_map[Network] = self['networks']    


        return