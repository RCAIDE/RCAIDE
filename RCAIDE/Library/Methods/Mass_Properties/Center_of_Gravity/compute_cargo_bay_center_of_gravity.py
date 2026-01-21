# RCAIDE/Library/Methods/Mass_Properties/Center_of_Gravity/compute_cargo_bay_center_of_gravity.py 
# 
# Created:  Dec 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Cargo Bay Center of Gravity
# ---------------------------------------------------------------------------------------------------------------------- 
def compute_cargo_bay_center_of_gravity(cargo_bay):
    """Compute the center of gravity of a cargo bay
    Assumtions
    ___________
    Cargo, Baggage and Container C.G. are the same location.
    """
    cargo_bay.cargo.origin     = cargo_bay.origin 
    cargo_bay.baggage.origin   = cargo_bay.origin    
    cargo_bay.container.origin = cargo_bay.origin
    
    cargo_bay.mass_properties.center_of_gravity           = [[cargo_bay.length / 2,0,0 ]]    
    cargo_bay.cargo.mass_properties.center_of_gravity     = cargo_bay.mass_properties.center_of_gravity
    cargo_bay.baggage.mass_properties.center_of_gravity   = cargo_bay.mass_properties.center_of_gravity
    cargo_bay.container.mass_properties.center_of_gravity = cargo_bay.mass_properties.center_of_gravity
    
    return cargo_bay.mass_properties.center_of_gravity