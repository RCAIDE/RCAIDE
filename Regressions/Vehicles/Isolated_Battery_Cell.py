# Regression/scripts/Vehicles/Isolated_Battery_Cell.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE  
from RCAIDE.Core                           import Units 
from RCAIDE.Methods.Power.Battery.Sizing   import initialize_from_mass ,initialize_from_energy_and_power, initialize_from_mass, initialize_from_circuit_configuration, find_mass_gain_rate, find_total_mass_gain
from RCAIDE.Methods.Power.Battery.Ragone   import find_ragone_properties, find_ragone_optimum 
 
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
         
    net                              = RCAIDE.Energy.Networks.Isolated_Battery_Cell() 
    #------------------------------------------------------------------------------------------------------------------------------------  
    # Bus
    #------------------------------------------------------------------------------------------------------------------------------------  
    bus                              = RCAIDE.Energy.Distributors.Bus_Power_Control_Unit()
    bus.fixed_voltage                = fixed_bus_voltage
    
    #net.dischage_model_fidelity   = cell_chemistry

    # Battery    
    if cell_chemistry == 'Lithium_Ion_NMC': 
        battery = RCAIDE.Energy.Storages.Batteries.Lithium_Ion_NMC()
    elif cell_chemistry == 'Lithium_Ion_LFP': 
        battery = RCAIDE.Energy.Storages.Batteries.Lithium_Ion_LFP() 
    battery.charging_voltage                     = battery.cell.nominal_voltage    
    battery.charging_current                     = current   
    battery.convective_heat_transfer_coefficient = 7.17
    net.voltage                                  = battery.cell.nominal_voltage 
    initialize_from_circuit_configuration(battery)  
    bus.voltage                      =  battery.pack.maximum_voltage  
    bus.batteries.append(battery)                                
      
    # append bus   
    net.busses.append(bus)

    #------------------------------------------------------------------------------------------------------------------------------------  
    # Avionics
    #------------------------------------------------------------------------------------------------------------------------------------  
    avionics                        = RCAIDE.Energy.Peripherals.Avionics()
    avionics.power_draw             = current*3.2
    net.avionics                    = avionics  
    
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