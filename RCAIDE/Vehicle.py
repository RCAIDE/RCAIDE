# RCAIDE/Vehicle.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Core       import Data, DataOrdered
from RCAIDE            import Components
from RCAIDE            import Energy
from RCAIDE.Components import Physical_Component

# package imports 
import numpy as np 
import string
characters   = string.punctuation + string.whitespace
t_table      = str.maketrans( characters          + string.ascii_uppercase , 
                            '_'*len(characters) + string.ascii_lowercase )


# ----------------------------------------------------------------------------------------------------------------------
#  VEHICLE
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Vehicle
class Vehicle(Data):
    """RCAIDE Vehicle container class with database + input / output functionality
    
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
        self.tag                    = 'vehicle'
        self.fuselages              = Components.Fuselages.Fuselage.Container()
        self.booms                  = Components.Booms.Boom.Container()
        self.wings                  = Components.Wings.Wing.Container()
        self.networks               = Energy.Networks.Network.Container()
        self.nacelles               = Components.Nacelles.Nacelle.Container()
        self.systems                = Components.Systems.System.Container()
        self.mass_properties        = Vehicle_Mass_Container()
        self.payload                = Components.Payloads.Payload.Container()
        self.costs                  = Costs()
        self.envelope               = Components.Envelope()
        self.landing_gear           = Components.Landing_Gear.Landing_Gear.Container()
        self.reference_area         = 0.0
        self.passengers             = 0.0
        self.performance            = DataOrdered()

    _component_root_map = None
    _network_root_map   = None

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

        self._component_root_map = {
            Components.Booms.Boom                      : self['booms']            ,
            Components.Envelope                        : self['envelope']         ,
            Components.Fuselages.Fuselage              : self['fuselages']        ,
            Components.Landing_Gear.Landing_Gear       : self['landing_gear']     ,
            Components.Nacelles.Nacelle                : self['nacelles']         ,
            Components.Systems.System                  : self['systems']          , 
            Components.Wings.Wing                      : self['wings']            ,
            Vehicle_Mass_Properties                    : self['mass_properties']  ,
        }
        

        self._network_root_map = { 
            Energy.Networks.Network                    : self['networks']         , 
            Vehicle_Mass_Properties                    : self['mass_properties']  ,
        }        
        
        self.append_component(Vehicle_Mass_Properties())
        self.append_network(Vehicle_Mass_Properties())
        
        return


    def append_component(self,component):
        """ Adds a component to vehicle
            
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
        if not isinstance(component,Data):
            raise Exception('input component must be of type Data()')

        # find the place to store data
        component_root = self.find_component_root(component)
        
        # See if the component exists, if it does modify the name
        keys = component_root.keys()
        if str.lower(component.tag) in keys:
            string_of_keys = "".join(component_root.keys())
            n_comps = string_of_keys.count(component.tag)
            component.tag = component.tag + str(n_comps+1)

        # store data
        component_root.append(component)

        return
    


    def append_network(self,network):
        """ Adds a network to vehicle
            
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
        if not isinstance(network,Data):
            raise Exception('input network must be of type Data()')

        # find the place to store data
        network_root = self.find_network_root(network)
        
        # See if the network exists, if it does modify the name
        keys = network_root.keys()
        if str.lower(network.tag) in keys:
            string_of_keys = "".join(network_root.keys())
            n_comps = string_of_keys.count(network.tag)
            network.tag = network.tag + str(n_comps+1)

        # store data
        network_root.append(network)

        return
    
    def find_component_root(self,component):
        """ Find pointer to component data root.
        
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

        component_type = type(component)

        # find component root by type, allow subclasses
        for component_type, component_root in self._component_root_map.items():
            if isinstance(component,component_type):
                break
        else:
            raise Exception("Unable to place component type %s" % component.typestring())

        return component_root

    def find_network_root(self,network):
        """ Find pointer to network data root.
        
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

        network_type = type(network)

        # find network root by type, allow subclasses
        for network_type, network_root in self._network_root_map.items():
            if isinstance(network,network_type):
                break
        else:
            raise Exception("Unable to place network type %s" % network.typestring())

        return network_root
    
    def sum_mass(self):
        """ Regresses through the vehicle and sums the masses
        
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

        total = 0.0
        
        for key in self.keys():
            item = self[key]
            if isinstance(item,Physical_Component.Container):
                total += item.sum_mass()

        return total
    
    
    def center_of_gravity(self):
        """ Recursively searches the data tree and sum
            any Comp.Mass_Properties.mass, and return the total sum
            
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
        total = np.array([[0.0,0.0,0.0]])

        for key in self.keys():
            item = self[key]
            if isinstance(item,Physical_Component.Container):
                total += item.total_moment()
                
        mass = self.sum_mass()
        if mass ==0:
            mass = 1.
                
        CG = total/mass
        
        self.mass_properties.center_of_gravity = CG
                
        return CG


## @ingroup Vehicle
class Vehicle_Mass_Properties(Components.Mass_Properties):

    """ Vehicle_Mass_Properties():
        The vehicle's mass properties.

    
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

        self.tag                               = 'mass_properties'
        self.operating_empty                   = 0.0
        self.max_takeoff                       = 0.0
        self.takeoff                           = 0.0
        self.max_landing                       = 0.0
        self.landing                           = 0.0
        self.max_cargo                         = 0.0
        self.cargo                             = 0.0
        self.max_payload                       = 0.0
        self.payload                           = 0.0
        self.passenger                         = 0.0
        self.crew                              = 0.0
        self.max_fuel                          = 0.0
        self.fuel                              = 0.0
        self.max_zero_fuel                     = 0.0
        self.center_of_gravity                 = [[0.0,0.0,0.0]]
        self.zero_fuel_center_of_gravity       = np.array([[0.0,0.0,0.0]])      

## @ingroup Vehicle
class Costs(Data):
    """ Costs class for organizing the costs of things

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
        self.tag = 'costs'
        self.industrial = Components.Costs.Industrial_Costs()
        self.operating  = Components.Costs.Operating_Costs()
        
        
class Vehicle_Mass_Container(Components.Physical_Component.Container,Vehicle_Mass_Properties):
        
    def append(self,value,key=None):
        """ Appends the vehicle mass, but only let's one ever exist. Keeps the newest one
        
        Assumptions:
        None
    
        Source:
        N/A
    
        Inputs:
        None
    
        Outputs:
        None
    
        Properties Used:
        N/A
        """      
        self.clear()
        for key in value.keys():
            self[key] = value[key]

    def get_children(self):
        """ Returns the components that can go inside
        
        Assumptions:
        None
    
        Source:
        N/A
    
        Inputs:
        None
    
        Outputs:
        None
    
        Properties Used:
        N/A
        """       
        
        return [Vehicle_Mass_Properties]
