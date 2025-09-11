# RCAIDE/Library/Methods/Stability/Vortex_Lattice_Method/evaluate_VLM.py
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports   
from RCAIDE.Framework.Core     import Data   
from RCAIDE.Library.Methods.Mass_Properties.Center_of_Gravity     import compute_vehicle_center_of_gravity

# package imports
import numpy   as np
from copy      import  deepcopy 

# ----------------------------------------------------------------------------------------------------------------------
#  Vortex_Lattice
# ---------------------------------------------------------------------------------------------------------------------- 
def evaluate(state,settings,vehicle):
    """Evaluates static margin and neutral point using built surrogates 
    
    Assumptions: 
        
    Source:
        None

    Args:
        stability    : VLM analysis  [unitless]
        state        : flight conditions     [unitless]
        settings     : VLM analysis settings [unitless]
        vehicle      : vehicle configuration [unitless] 
        
    Returns: 
        None  
    """ 
   
    # --------------------------------------------------------------------------
    # unpack 
    # --------------------------------------------------------------------------
    conditions    = state.conditions 
    AoA           = conditions.aerodynamics.angles.alpha  

    # --------------------------------------------------------------------------       
    # update center of gravity 
    # --------------------------------------------------------------------------
    # create aircraft copy without fuel mass 
    vehicle_no_fuel =  deepcopy(vehicle)
    for network in vehicle_no_fuel.networks: 
        for fuel_line in network.fuel_lines:   
            for fuel_tank in fuel_line.fuel_tanks: 
                fuel_tank.fuel.mass_properties.mass = 0.0
    
    # run c.g. function to get total mass  and moment without updating C.G.
    _ , Mom_0, Mass_0 = compute_vehicle_center_of_gravity(vehicle_no_fuel, update_center_of_gravity= False) 
    
    # determine original fuel mass and moment and remove it from total mass and moment
    Mom_fuel = np.array([[0.0, 0.0, 0.0]])
    M_fuel   = np.zeros_like(AoA)
    for network in vehicle.networks: 
        for fuel_line in network.fuel_lines:  
            fuel_line_results   = conditions.energy.fuel_lines[fuel_line.tag]
            for fuel_tank in fuel_line.fuel_tanks: 
                m_fuel        = fuel_line_results.fuel_tanks[fuel_tank.tag].fuel_mass 
                global_cg_loc = np.array(fuel_tank.fuel.mass_properties.center_of_gravity) + np.array(fuel_tank.fuel.origin)  
                M_fuel        += m_fuel
                Mom_fuel      += np.multiply(m_fuel, global_cg_loc)                
    
    # recompute mass and moment of fuel
    Mom_aircraft = Mom_0 + Mom_fuel
    M_aircraft   = Mass_0 + M_fuel
     
    # compute updated C.G. 
    CG   = Mom_aircraft / M_aircraft

    # --------------------------------------------------------------------------       
    # update moment of intertia 
    # --------------------------------------------------------------------------
    # Future work
 
    # --------------------------------------------------------------------------------------------      
    # Vehicle Properties 
    # --------------------------------------------------------------------------------------------      
    c_ref         = vehicle.reference_chord   
    NP            = vehicle.neutral_point
    
    # --------------------------------------------------------------------------------------------      
    # Store Results 
    # --------------------------------------------------------------------------------------------      
    conditions.static_stability.center_of_gravity      = CG       
    conditions.static_stability.neutral_point[:,0]     = NP 
    conditions.static_stability.static_margin          = (NP - np.atleast_2d(CG[:, 0])).T / c_ref      
        
    return

def compute_stability_derivative(sub_sur,trans_sur,sup_sur,h_sub,h_sup,Mach):
    if trans_sur ==  None and  sup_sur == None:
        derivative = h_sub(Mach)*sub_sur(Mach) 
        return derivative
        
    derivative = h_sub(Mach)*sub_sur(Mach) +   (1 - (h_sup(Mach) + h_sub(Mach)))*trans_sur(Mach)  + h_sup(Mach)*sup_sur(Mach) 
    return derivative



def compute_coefficients(sub_sur_Clift,sub_sur_Cdrag,sub_sur_CX,sub_sur_CY,sub_sur_CZ,sub_sur_CL,sub_sur_CM,sub_sur_CN,
                         trans_sur_Clift,trans_sur_Cdrag,trans_sur_CX,trans_sur_CY,trans_sur_CZ,trans_sur_CL,trans_sur_CM,trans_sur_CN,
                         sup_sur_Clift,sup_sur_Cdrag,sup_sur_CX,sup_sur_CY,sup_sur_CZ,sup_sur_CL,sup_sur_CM,sup_sur_CN,
                         h_sub,h_sup,Mach, pts): 
    

     #  subsonic 
    sub_Clift     = np.atleast_2d(sub_sur_Clift(pts)).T  
    sub_Cdrag     = np.atleast_2d(sub_sur_Cdrag(pts)).T  
    sub_CX        = np.atleast_2d(sub_sur_CX(pts)).T 
    sub_CY        = np.atleast_2d(sub_sur_CY(pts)).T     
    sub_CZ        = np.atleast_2d(sub_sur_CZ(pts)).T     
    sub_CL        = np.atleast_2d(sub_sur_CL(pts)).T     
    sub_CM        = np.atleast_2d(sub_sur_CM(pts)).T     
    sub_CN        = np.atleast_2d(sub_sur_CN(pts)).T
    
    
    if trans_sur_Clift ==  None and  sup_sur_Clift == None:
    
        results       = Data() 
        results.Clift = h_sub(Mach) * sub_Clift
        results.Cdrag = h_sub(Mach) * sub_Cdrag
        results.CX    = h_sub(Mach) * sub_CX   
        results.CY    = h_sub(Mach) * sub_CY   
        results.CZ    = h_sub(Mach) * sub_CZ   
        results.CL    = h_sub(Mach) * sub_CL   
        results.CM    = h_sub(Mach) * sub_CM   
        results.CN    = h_sub(Mach) * sub_CN   
        
        return results
   
    
    # transonic   
    trans_Clift   = np.atleast_2d(trans_sur_Clift(pts)).T  
    trans_Cdrag   = np.atleast_2d(trans_sur_Cdrag(pts)).T  
    trans_CX      = np.atleast_2d(trans_sur_CX(pts)).T 
    trans_CY      = np.atleast_2d(trans_sur_CY(pts)).T     
    trans_CZ      = np.atleast_2d(trans_sur_CZ(pts)).T     
    trans_CL      = np.atleast_2d(trans_sur_CL(pts)).T     
    trans_CM      = np.atleast_2d(trans_sur_CM(pts)).T     
    trans_CN      = np.atleast_2d(trans_sur_CN(pts)).T

    # supersonic 
    sup_Clift     = np.atleast_2d(sup_sur_Clift(pts)).T  
    sup_Cdrag     = np.atleast_2d(sup_sur_Cdrag(pts)).T  
    sup_CX        = np.atleast_2d(sup_sur_CX(pts)).T 
    sup_CY        = np.atleast_2d(sup_sur_CY(pts)).T     
    sup_CZ        = np.atleast_2d(sup_sur_CZ(pts)).T     
    sup_CL        = np.atleast_2d(sup_sur_CL(pts)).T     
    sup_CM        = np.atleast_2d(sup_sur_CM(pts)).T     
    sup_CN        = np.atleast_2d(sup_sur_CN(pts)).T            

    # apply 
    results       = Data() 
    results.Clift = h_sub(Mach)*sub_Clift + (1 - (h_sup(Mach) + h_sub(Mach)))*trans_Clift  + h_sup(Mach)*sup_Clift
    results.Cdrag = h_sub(Mach)*sub_Cdrag + (1 - (h_sup(Mach) + h_sub(Mach)))*trans_Cdrag  + h_sup(Mach)*sup_Cdrag
    results.CX    = h_sub(Mach)*sub_CX    + (1 - (h_sup(Mach) + h_sub(Mach)))*trans_CX     + h_sup(Mach)*sup_CX   
    results.CY    = h_sub(Mach)*sub_CY    + (1 - (h_sup(Mach) + h_sub(Mach)))*trans_CY     + h_sup(Mach)*sup_CY   
    results.CZ    = h_sub(Mach)*sub_CZ    + (1 - (h_sup(Mach) + h_sub(Mach)))*trans_CZ     + h_sup(Mach)*sup_CZ   
    results.CL    = h_sub(Mach)*sub_CL    + (1 - (h_sup(Mach) + h_sub(Mach)))*trans_CL     + h_sup(Mach)*sup_CL   
    results.CM    = h_sub(Mach)*sub_CM    + (1 - (h_sup(Mach) + h_sub(Mach)))*trans_CM     + h_sup(Mach)*sup_CM   
    results.CN    = h_sub(Mach)*sub_CN    + (1 - (h_sup(Mach) + h_sub(Mach)))*trans_CN     + h_sup(Mach)*sup_CN

    return results


def compute_coefficient(sub_sur_coef,trans_sur_coef, sup_sur_coef, h_sub,h_sup,Mach, pts): 

    #  subsonic 
    sub_coef  = np.atleast_2d(sub_sur_coef(pts)).T     
   
    if trans_sur_coef == None and sup_sur_coef == None:
        coef = h_sub(Mach) 
        return  coef
    
    # transonic 
    trans_coef  = np.atleast_2d(trans_sur_coef(pts)).T    

    # supersonic 
    sup_coef  = np.atleast_2d(sub_sur_coef(pts)).T             

    # apply  
    coef = h_sub(Mach)*sub_coef +   (1 - (h_sup(Mach) + h_sub(Mach)))*trans_coef  + h_sub(Mach)*sup_coef 

    return coef 