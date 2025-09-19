# RCAIDE/Library/Methods/Stability/Vortex_Lattice_Method/compute_neutral_point.py
#  
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
import RCAIDE 
from RCAIDE.Framework.Core import  Data 
from RCAIDE.Library.Methods.Aerodynamics.Vortex_Lattice_Method.VLM   import VLM 
from copy import deepcopy 

# package imports
import numpy  as np
from scipy.optimize import minimize 

# ----------------------------------------------------------------------------------------------------------------------
#  compute_neutral_point
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_neutral_point(stability):
    """ 
    """
  
    vehicle        = deepcopy(stability.vehicle)
    settings       = stability.settings
    AoA            = stability.training.angle_of_attack 
    Mach           = stability.training.Mach   
    len_Mach       = len(Mach)        
    len_AoA        = len(AoA)
    
    if stability.vehicle.neutral_point == None:  
        AoAs                                            = np.atleast_2d(np.tile(AoA,len_Mach).T.flatten()).T 
        Machs                                           = np.atleast_2d(np.repeat(Mach,len_AoA)).T      
        conditions                                      = RCAIDE.Framework.Mission.Common.Results() 
        conditions.freestream.mach_number               = Machs
        conditions.freestream.velocity                  = np.ones_like(Machs) * 1e-6
        conditions.aerodynamics.angles.alpha            = np.ones_like(Machs)*AoAs 
           
        
        # --------------------------------------------------------------------------------------------------------------
        # Neutral Point 
        # --------------------------------------------------------------------------------------------------------------   
        clean_wing_vehicle_np = deepcopy(vehicle) # Double check this is correct
        for wing in clean_wing_vehicle_np.wings:
            wing.control_surfaces = []
        # use center of gravity as inital guess
        cg     =  vehicle.mass_properties.center_of_gravity[0][0]
        bnds   = [[0, 100]]
        sol = minimize(neutral_point_objective, [cg], args=(conditions,settings,clean_wing_vehicle_np,Mach,AoA) , method='SLSQP', bounds=bnds, tol=1e-4)
         
        stability.vehicle.neutral_point  =  sol.x[0]  
   
    return 

def neutral_point_objective(cg_location,conditions,settings,clean_wing_vehicle_np,Mach,AoA):

    len_Mach       = len(Mach)        
    len_AoA        = len(AoA)
    
    # update neutral point
    clean_wing_vehicle_np.mass_properties.center_of_gravity[0][0] =  cg_location[0]
    
    # run VLM 
    VLM_results = VLM(conditions,settings,clean_wing_vehicle_np)    
    
    AoA       = conditions.aerodynamics.angles.alpha
    CM_res    = VLM_results.CM
    CM        = np.reshape(CM_res,(len_Mach,len_AoA)).T 
    
    # compute dCM_dalpha 
    dCM_dalpha = ( CM[2, 0] - CM[1, 0]) /( AoA[2] - AoA[1])
     
    # find abs 
    return  abs(dCM_dalpha)