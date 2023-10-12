## @ingroup Planform
#rescale_non_dimensional.py

# Created : May 2020, E. Botero
# Modified:

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import Legacy.trunk.S as SUAVE
import numpy as np


# ----------------------------------------------------------------------
#  Set Origin Non-Dimensional
# ----------------------------------------------------------------------

def set_origin_non_dimensional(vehicle,length_scale=None):
    """ Places the origin of all major components in a 
    non-dimensional fashion. This is useful for optimization or
    generative design 

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        vehicle    [SUAVE Vehicle]
              .fuselages.*.origin
              .fuselages.fuselage.lengths.total
              .wings.*.origin
              .wings.main_wing.lengths.total
              .networks.*.origin

        Outputs:
        vehicle    [SUAVE Vehicle]
              .fuselages.*.non_dimensional_origin
              .wings.*.non_dimensional_origin
              .networks.*.non_dimensional_origin

        Properties Used:
        None
    """        
    
    if length_scale==None:
        try:
            length_scale = vehicle.fuselages.fuselage.lengths.total
        except:
            try:
                length_scale = vehicle.wings.main_wing.lengths.total
            except:
                length_scale = 1.

    for wing in vehicle.wings:
        origin  = wing.origin
        non_dim = np.array(origin)/length_scale
        
        wing.non_dimensional_origin = non_dim.tolist()
    
    for fuse in vehicle.fuselages:
        origin  = fuse.origin
        non_dim = np.array(origin)/length_scale
        
        fuse.non_dimensional_origin = non_dim.tolist()  

    for prop in vehicle.networks:
        origins  = prop.origin
        prop.non_dimensional_origin.clear()
        for eng in range(int(prop.number_of_engines)):
            origin = np.array(origins[eng])/length_scale
            prop.non_dimensional_origin.append(origin.tolist())       
    
        
    return vehicle


# ----------------------------------------------------------------------
#  Scale to Non-Dimensional
# ----------------------------------------------------------------------

def set_origin_dimensional(vehicle,length_scale=None):
    """ Places the origin of all components 

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        vehicle    [SUAVE Vehicle]

        Outputs:
        vehicle    [SUAVE Vehicle]

        Properties Used:
        None
    """    
    
    if length_scale==None:
        try:
            length_scale = vehicle.fuselages.fuselage.lengths.total
        except:
            try:
                length_scale = vehicle.wings.main_wing.lengths.total
            except:
                length_scale = 1.

    for wing in vehicle.wings:
        non_dim = wing.non_dimensional_origin
        origin  = np.array(non_dim)*length_scale
        
        wing.origin = origin.tolist()
    
    for fuse in vehicle.fuselages:
        non_dim = fuse.non_dimensional_origin
        origin  = np.array(non_dim)*length_scale
        
        fuse.origin = origin.tolist()
                
    nac_id = 0 # The nacelle index
    nacs   = list(vehicle.nacelles.keys()) 
    for net in vehicle.networks:
        n = int(net.number_of_engines)
        non_dims  = net.non_dimensional_origin
        
        net.origin = np.array(non_dims[0])*length_scale

        # Apply the origin to the nacelles
        for eng in range(nac_id,n+nac_id):
            nac = vehicle.nacelles[nacs[eng]]
            nac.origin = np.array(non_dims[0])*length_scale
            nac.origin = np.atleast_2d(nac.origin)
            
            
        # Shift for symmetry
        if n==1:
            nac = vehicle.nacelles[nacs[0]]
            nac.origin[0][1] = 0.
        elif n==2:
            nac = vehicle.nacelles[nacs[1]]
            nac.origin[0][1] = -nac.origin[0][1]
        elif n==3:
            nac2 = vehicle.nacelles[nacs[1]]
            nac2.origin[0][1] = 0    
            nac3 = vehicle.nacelles[nacs[2]]
            nac3.origin[0][1] = -nac3.origin[0][1]                       
        elif n==4:
            nac1 = vehicle.nacelles[nacs[0]]
            nac2 = vehicle.nacelles[nacs[1]]
            nac3 = vehicle.nacelles[nacs[2]]
            nac4 = vehicle.nacelles[nacs[3]]
            
            nac1.origin[0][1] = 1.25*nac1.origin[0][1]
            nac2.origin[0][1] = 0.75*nac2.origin[0][1]
            nac3.origin[0][1] = -0.75*nac3.origin[0][1]
            nac4.origin[0][1] = -1.25*nac4.origin[0][1]            

        
    return vehicle