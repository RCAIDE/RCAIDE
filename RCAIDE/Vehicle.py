## @defgroup Vehicle
# Vehicle.py
# (c) Copyright The Board of Trustees of RCAIDE
#
# Created:  Jul 2023, E. Botero
# Modified:  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S   import Vehicle as VH
from RCAIDE.Core      import Data
from .Energy.Networks import Network
from RCAIDE           import Components , Energy 
from Legacy.trunk.S.Components.Energy.Networks import Network as legacy_net

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
    
    _energy_network_root_map = None
        

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
        self._energy_network_root_map= {
            Energy.Networks.Network         : self['networks']
            } 
        return
    
    def append_energy_network(self,energy_network):
        """ adds an energy network to vehicle
            
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

        # assert database type
        if not isinstance(energy_network,Data):
            raise Exception('input energy network must be of type Data()')

        # find the place to store data
        energy_network_root = self.find_energy_network_root(energy_network)
        
        # See if the energy network exists, if it does modify the name
        keys = energy_network_root.keys()
        if str.lower(energy_network.tag) in keys:
            string_of_keys = "".join(energy_network_root.keys())
            n_comps = string_of_keys.count(energy_network.tag)
            energy_network.tag = energy_network.tag + str(n_comps+1)

        # store data
        energy_network_root.append(energy_network)

        return    
    


    def find_energy_network_root(self,energy_network):
        """ find pointer to energy network data root.
        
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

        energy_network_type = type(energy_network)

        # find energy network root by type, allow subclasses
        for energy_network_type, energy_network_root in self._energy_network_root_map.items():
            if isinstance(energy_network,energy_network_type):
                break
        else:
            raise Exception("Unable to place energy_network type %s" % energy_network.typestring())

        return energy_network_root
    