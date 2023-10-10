

from RCAIDE.Components import Component 
import numpy as np 


#compute MOI

def compute_vehicle_moment_inertia(self):

    I_total = np.array([[0.0,0.0,0.0]])

    for key in self.keys():
        item = self[key]
        if isinstance(item,Motor):
            I_total += cylinder_inertia(item, aircraft_center_of_gravity = self.mass_proerties.center_of_gravity)     
        elif isinstance(item,Fuselage):
            I_total += cone_inertia(item, aircraft_center_of_gravity = self.mass_proerties.center_of_gravity) 
            I_total += cylinder_inertia(item, aircraft_center_of_gravity = self.mass_proerties.center_of_gravity) 
            I_total += cone_inertia(item, aircraft_center_of_gravity = self.mass_proerties.center_of_gravity)   

    


