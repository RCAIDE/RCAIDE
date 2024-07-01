## @ingroup Library-Methods-Energy-Sources-Battery-Common
# RCAIDE/Library/Methods/Energy/Sources/Battery/Common/size_pack_from_mass.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
# size_pack_from_mass
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Energy-Sources-Battery-Common
def size_pack_from_mass(battery,pack_markup_factor = 1.42 ):
    """ Calculate the pack properties of the battery pack based on
    total mass, cell properties and pack mark-up factor that accounts
    for battery management system, internal wirings etc
    
    Assumptions:
    1) Total battery pack mass contains build-up factor (1.42) for battery casing,
       internal wires, thermal management system and battery management system 
       Factor computed using information of battery properties for X-57 Maxwell
       Aircraft
    2) Constant value of specific energy and power

    Source:
        None
        
    Args:
       battery             (dict): battery data structure [-]
       pack_markup_factor (float): pack mark up factor    [unitless]

    Returns:
        None  
    """
    
    # compute battery mass 
    mass = battery.mass_properties.mass/pack_markup_factor 
    if battery.cell.mass == None: 
        n_series   = 1
        n_parallel = 1 
    else:
        n_cells    = int(mass/battery.cell.mass)
        n_series   = int(battery.pack.maximum_voltage/battery.cell.maximum_voltage)
        n_parallel = int(n_cells/n_series)
        
    battery.pack.maximum_energy                    = mass*battery.specific_energy  
    battery.pack.maximum_power                     = mass*battery.specific_power 
    battery.pack.specific_energy                   = battery.pack.maximum_energy / battery.mass_properties.mass
    battery.pack.initial_maximum_energy            = battery.pack.maximum_energy   
    battery.pack.electrical_configuration.series   = n_series
    battery.pack.electrical_configuration.parallel = n_parallel 
    battery.pack.electrical_configuration.total    = n_parallel*n_series 
     
    # charging 
    battery.pack.charging_voltage                  = battery.cell.charging_voltage * battery.pack.electrical_configuration.series     
    battery.pack.charging_current                  = battery.cell.charging_current * battery.pack.electrical_configuration.parallel
    
    return 