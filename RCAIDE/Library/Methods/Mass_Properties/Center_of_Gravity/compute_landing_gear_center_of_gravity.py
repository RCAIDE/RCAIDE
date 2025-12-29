# RCAIDE/Library/Methods/Mass_Properties/Center_of_Gravity/compute_landing_gear_center_of_gravity.py 
# 
# Created:  Dec 2025, M. Clarke 


# ----------------------------------------------------------------------------------------------------------------------
#  Compute Landing Gear Center of Gravity
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_landing_gear_center_of_gravity(landing_gear):
    

    landing_gear.mass_properties.center_of_gravity = [[landing_gear.length / 2,0,0 ]]        
    
    
    return landing_gear.mass_properties.center_of_gravity