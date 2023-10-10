
from RCAIDE.Components import Component 
from Legacy.trunk.S.Components import Physical_Component 
import numpy as np 

def compute_vehicle_center_of_gravity(vehicle):
    """  
    """   
    total = np.array([[0.0,0.0,0.0]])

    for key in vehicle.keys():
        item = vehicle[key]
        if isinstance(item,Physical_Component.Container):
            total +=  total_moment(item)
            
    mass = sum_mass(vehicle)
    if mass ==0:
        mass = 1.
            
    CG = total/mass
    
    vehicle.mass_properties.center_of_gravity = CG
            
    return CG

def sum_mass(vehicle): 

    total = 0.0
    
    for key in vehicle.keys():
        item = vehicle[key]
        if isinstance(item,Physical_Component.Container):
            total += item.sum_mass()

    return total


def total_moment(compoment):
    """ will recursively search the data tree and sum
        any Comp.Mass_Properties.mass, and return the total sum of moments
        
        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        total moment [kg*m]

        Properties Used:
        None
    """   
    total = np.array([[0.0,0.0,0.0]])
    for key,Comp in compoment.items():
        if isinstance(Comp,Physical_Component.Container):
            total += Comp.total_moment() # recursive!
        elif isinstance(Comp,Physical_Component):
            print(Comp.tag)
            print(Comp.mass_properties.center_of_gravity)
            total += Comp.mass_properties.mass*(np.sum(np.array(Comp.origin),axis=0)/len(Comp.origin)+Comp.mass_properties.center_of_gravity)

    return total




