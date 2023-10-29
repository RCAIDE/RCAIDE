## @ingroup Methods-Power-Battery-Sizing
# RCAIDE/Methods/Power/Battery/Sizing/initialize_from_mass.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Power-Battery-Sizing
def initialize_from_mass(battery,module_weight_factor = 1.42 ):
    """
    Calculate the max energy and power based of the mass
    Assumptions:
    A constant value of specific energy and power

    Inputs:
    mass              [kilograms]
    battery.
      specific_energy [J/kg]               
      specific_power  [W/kg]

    Outputs:
     battery.
       maximum_energy
       maximum_power
       mass_properties.
        mass


    """     
    mass = battery.mass_properties.mass/module_weight_factor
    
    if battery.cell.mass == None: 
        n_series   = 1
        n_parallel = 1 
    else:
        n_cells    = int(mass/battery.cell.mass)
        n_series   = int(battery.pack.maximum_voltage/battery.cell.maximum_voltage)
        n_parallel = int(n_cells/n_series)
        
    battery.pack.maximum_energy                    = mass*battery.specific_energy  
    battery.pack.maximum_power                     = mass*battery.specific_power
    battery.pack.initial_maximum_energy            = battery.pack.maximum_energy    
    battery.pack.electrical_configuration.series   = n_series
    battery.pack.electrical_configuration.parallel = n_parallel 
    battery.pack.electrical_configuration.total    = n_parallel*n_series      
    battery.charging_voltage                       = battery.cell.charging_voltage * battery.pack.electrical_configuration.series     
    battery.charging_current                       = battery.cell.charging_current * battery.pack.electrical_configuration.parallel        