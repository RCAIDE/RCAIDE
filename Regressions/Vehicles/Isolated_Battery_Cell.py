# Regression/scripts/Vehicles/Isolated_Battery_Cell.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE  
from RCAIDE.Core                                    import Units 
from RCAIDE.Methods.Energy.Sources.Battery.Sizing   import initialize_from_circuit_configuration  
 
# ----------------------------------------------------------------------------------------------------------------------
#  Build the Vehicle
# ----------------------------------------------------------------------------------------------------------------------   

def vehicle_setup(current,cell_chemistry,fixed_bus_voltage): 

    vehicle                       = RCAIDE.Vehicle() 
    vehicle.tag                   = 'battery'   
    vehicle.reference_area        = 1
 
    # ################################################# Vehicle-level Properties #####################################################   
    # mass properties
    vehicle.mass_properties.takeoff         = 1 * Units.kg 
    vehicle.mass_properties.max_takeoff     = 1 * Units.kg 
         
    net                              = RCAIDE.Energy.Networks.Isolated_Battery_Cell_Network() 
    #------------------------------------------------------------------------------------------------------------------------------------  
    # Bus
    #------------------------------------------------------------------------------------------------------------------------------------  
    bus                              = RCAIDE.Energy.Networks.Distribution.Electrical_Bus() 
 
    # Battery    
    if cell_chemistry == 'lithium_ion_nmc': 
        battery = RCAIDE.Energy.Sources.Batteries.Lithium_Ion_NMC()
    elif cell_chemistry == 'lithium_ion_lfp': 
        battery = RCAIDE.Energy.Sources.Batteries.Lithium_Ion_LFP()  
    HAS                 = RCAIDE.Energy.Thermal_Management.Batteries.Heat_Acquisition_Systems.Direct_Air() 
    HAS.convective_heat_transfer_coefficient    = 7.17
    battery.thermal_management_system.heat_acquisition_system = HAS 
    net.voltage                                 = battery.cell.nominal_voltage 
    initialize_from_circuit_configuration(battery)  
    bus.voltage                      =  battery.pack.maximum_voltage  
    bus.batteries.append(battery)                                
      
    # append bus   
    net.busses.append(bus) 
    
    # append network 
    vehicle.append_energy_network(net) 
 
    # ##################################   Determine Vehicle Mass Properties Using Physic Based Methods  ################################       
    vehicle.mass_properties.takeoff = battery.mass_properties.mass 
    return vehicle


def configs_setup(vehicle): 
    configs         = RCAIDE.Components.Configs.Config.Container()  
    base_config     = RCAIDE.Components.Configs.Config(vehicle)
    base_config.tag = 'base' 
    configs.append(base_config)   
    return configs 