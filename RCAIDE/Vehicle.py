# Vehicle.py
# (c) Copyright 2023 Aerospace Research Community LLC
#
# Created: Mar 2024, RCAIDE Team
# Modified:
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
from RCAIDE                    import Framework
from RCAIDE.Framework.Core     import Data 
from RCAIDE.Library            import Components, Attributes 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Vehicle
# ----------------------------------------------------------------------------------------------------------------------  
class Vehicle(Data):
    """RCAIDE Vehicle container class with database + input / output functionality
    """    

    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """    
        self.tag                          = 'vehicle'
        self.fuselages                    = Components.Fuselages.Fuselage.Container()
        self.wings                        = Components.Wings.Wing.Container()
        self.networks                     = Framework.Networks.Network.Container()
        self.nacelles                     = Components.Nacelles.Nacelle.Container()
        self.avionics                     = Components.Systems.Avionics.Container()
        self.systems                      = Components.Systems.System.Container()
        self.booms                        = Components.Booms.Boom.Container()
        self.mass_properties              = Vehicle_Mass_Properties()
        self.payload                      = Components.Payloads.Payload.Container()
        self.costs                        = Data() 
        self.costs.industrial             = Attributes.Costs.Industrial_Costs()
        self.costs.operating              = Attributes.Costs.Operating_Costs()     
        self.landing_gear                 = Components.Landing_Gear.Landing_Gear.Container()
        self.reference_area               = 0.0
        self.passengers                   = 0.0
        self.maximum_cross_sectional_area = 0.0 
         
    _energy_network_root_map = None 

    def __init__(self,*args,**kwarg):
        """ Sets up the component hierarchy for a vehicle
    
            Assumptions:
                None
    
            Source:
                None
    
            Args:
                None
    
            Returns:
                None 
        """          
        # will set defaults
        super(Vehicle,self).__init__(*args,**kwarg)  

        self._component_root_map = {
            Components.Fuselages.Fuselage              : self['fuselages']        ,
            Components.Wings.Wing                      : self['wings']            ,
            Components.Systems.System                  : self['systems']          ,
            Components.Systems.Avionics                : self['avionics']         ,
            Components.Payloads.Payload                : self['payload']          , 
            Framework.Networks.Network                 : self['networks']         , 
            Components.Booms.Boom                      : self['booms']            ,
            Components.Landing_Gear.Landing_Gear       : self['landing_gear']     ,
        }

        self._energy_network_root_map= {
            Framework.Networks.Network                 : self['networks']         , 
            }    
                         
        return
    

    def find_component_root(self,component):
        """ find pointer to component data root.
        
            Assumptions:
                None
    
            Source:
                None 
    
            Args:
                None
    
            Returns:
                None 
        """  

        # find component root by type, allow subclasses
        for component_type, component_root in self._component_root_map.items():
            if isinstance(component,component_type):
                break
        else:
            raise Exception("Unable to place component type %s" % component.typestring())

        return component_root


    def append_component(self,component):
        """ Adds a component to vehicle
        
            Assumptions:
                None
    
            Source:
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

    def sum_mass(self):
        """ Regresses through the vehicle and sums the masses
        
            Assumptions:
                None
    
            Source:
                None
        """  

        total = 0.0
        
        for key in self.keys():
            item = self[key]
            if isinstance(item,Components.Component.Container):
                total += item.sum_mass()

        return total
    
    
    def center_of_gravity(self):
        """ will recursively search the data tree and sum
            any Comp.Mass_Properties.mass, and return the total sum
        
            Assumptions:
                None
    
            Source:
                None
        """   
        total = np.array([[0.0,0.0,0.0]])

        for key in self.keys():
            item = self[key]
            if isinstance(item,Components.Component.Container):
                total += item.total_moment()
                
        mass = self.sum_mass()
        if mass ==0:
            mass = 1.
                
        CG = total/mass
        
        self.mass_properties.center_of_gravity = CG
                
        return CG 
    
    
    def append_energy_network(self,energy_network):
        """ Adds an energy network to vehicle 
        
            Assumptions:
                None
    
            Source:
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
        """ Find pointer to energy network data root.
        
            Assumptions:
                None
    
            Source:
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

 
class Vehicle_Mass_Properties(Components.Mass_Properties): 
    """ The vehicle's mass properties.
        
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
                None
            """         

        self.tag                         = 'mass_properties'
        self.operating_empty             = 0.0
        self.max_takeoff                 = 0.0
        self.takeoff                     = 0.0
        self.max_landing                 = 0.0
        self.landing                     = 0.0
        self.max_cargo                   = 0.0
        self.cargo                       = 0.0
        self.max_payload                 = 0.0
        self.max_fuel                    = 0.0
        self.max_zero_fuel               = 0.0
        self.center_of_gravity           = [[0.0,0.0,0.0]]
        self.zero_fuel_center_of_gravity = np.array([[0.0,0.0,0.0]])    