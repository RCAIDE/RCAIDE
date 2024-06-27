## @ingroup Methods-Weights-Buildups-eVTOL 
# RCAIDE/Methods/Weights/Buildups/eVTOL/converge_evtol_weight.py
# 
# 
# Created:  Jun 2024, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Electric import compute_weight
from RCAIDE.Framework.Core import Data

# ----------------------------------------------------------------------------------------------------------------------
# converge_evtol_weight
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Weights-Buildups-eVTOL 
def converge_weight(vehicle,
                    print_iterations              = False,
                    contingency_factor            = 1.1,
                    speed_of_sound                = 340.294,
                    max_tip_mach                  = 0.65,
                    disk_area_factor              = 1.15,
                    safety_factor                 = 1.5,
                    max_thrust_to_weight_ratio    = 1.1,
                    max_g_load                    = 3.8,
                    motor_efficiency              = 0.85 * 0.98):
    '''Converges the maximum takeoff weight of an aircraft using the eVTOL 
    weight buildup routine.  
    
    Source:
    None
    
    Assumptions:
    None
    
    Args:
    vehicle                     RCAIDE Config Data Stucture
    print_iterations            Boolean Flag      
    contingency_factor          Factor capturing uncertainty in vehicle weight [unitless]
    speed_of_sound:             Local Speed of Sound                           [m/s]
    max_tip_mach:               Allowable Tip Mach Number                      [unitless]
    disk_area_factor:           Inverse of Disk Area Efficiency                [unitless]
    max_thrust_to_weight_ratio: Allowable Thrust to Weight Ratio               [unitless]
    safety_factor               Safety Factor in vehicle design                [unitless]
    max_g_load                  Maximum g-forces load for certification        [UNitless]
    motor_efficiency:           Motor Efficiency                               [unitless]
    
    Returns:
    None
    

    '''
    settings       = Data()
    breakdown      = compute_weight(vehicle,contingency_factor,
                           speed_of_sound,max_tip_mach,disk_area_factor,
                           safety_factor,max_thrust_to_weight_ratio,
                           max_g_load,motor_efficiency) 
    build_up_mass  = breakdown.total    
    diff           = vehicle.mass_properties.max_takeoff - build_up_mass
    iterations     = 0
    
    while(abs(diff)>1):
        vehicle.mass_properties.max_takeoff = vehicle.mass_properties.max_takeoff - diff
        
        # Note that 'diff' will be negative if buildup mass is larger than MTOW, so subtractive
        # iteration always moves MTOW toward buildup mass
        
        breakdown      = compute_weight(vehicle,contingency_factor,
                           speed_of_sound,max_tip_mach,disk_area_factor,
                           safety_factor,max_thrust_to_weight_ratio,
                           max_g_load,motor_efficiency)
        build_up_mass  = breakdown.total    
        diff           = vehicle.mass_properties.max_takeoff - build_up_mass 
        iterations     += 1
        if print_iterations:
            print(round(diff,3))
        if iterations == 100:
            print('Weight convergence failed!')
            return False 
    print('Converged MTOW = ' + str(round(vehicle.mass_properties.max_takeoff)) + ' kg')
    
    return True 
