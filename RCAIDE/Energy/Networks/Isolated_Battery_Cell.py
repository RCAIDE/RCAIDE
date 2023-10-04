## @ingroup Energy-Networks
# RCAIDE/Energy/Networks/Battery_Cell_Isolated.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
 # RCAIDE imports 
import RCAIDE
from RCAIDE.Analyses.Mission.Common                                        import Residuals
from RCAIDE.Core                                                           import Data
from RCAIDE.Components.Component                                           import Container  
from RCAIDE.Methods.Power.Battery.Common.pack_battery_conditions           import pack_battery_conditions
from RCAIDE.Methods.Power.Battery.Common.append_initial_battery_conditions import append_initial_battery_conditions
from .Network import Network 
 
# package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Isolated_Battery_Cell
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Networks
class Isolated_Battery_Cell(Network):
    """ This is a test bench to analyze the discharge and charge profile 
        of a battery cell.
    
        Assumptions:
        None
        
        Source:
        None
    """  
    def __defaults__(self):
        """ This sets the default values for the network to function.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            N/A
        """      
        self.tag                     = 'isolated_battery_cell' 
        self.avionics                = RCAIDE.Energy.Peripherals.Avionics()
        self.payload                 = RCAIDE.Energy.Peripherals.Payload()
        self.busses                  = Container()
        self.system_voltage          = None          
        
    # manage process with a driver function
    def evaluate_thrust(self,state):
        """ Evaluate the state variables of a cycled cell
    
            Assumptions: 
            None
    
            Source:
            N/A
    
            Inputs:
            state [state()]
    
            Outputs: 
            conditions.energy: 
                current                            [amps]
                battery.power                      [watts]
                initial.battery_state_of_charge    [joules]
                battery.voltage_open_circuit       [volts]
                battery.voltage_under_load         [volts]  
    
            Properties Used:
            Defaulted values
        """        
        

        # unpack   
        conditions = state.conditions
        numerics   = state.numerics
        busses     = self.busses
        avionics   = self.avionics
        payload    = self.payload 

        total_thrust  = 0. * state.ones_row(3) 
        total_power   = 0. * state.ones_row(3)          
        for bus in busses:
            batteries = bus.batteries      

            for battery in batteries:               
                battery_conditions                = conditions.energy[bus.tag][battery.tag] 
                battery.pack.current_energy       = battery_conditions.pack.energy     
                battery.pack.temperature          = battery_conditions.pack.temperature
                battery.cell.age                  = battery_conditions.cell.cycle_in_day    
                battery.cell.charge_throughput    = battery_conditions.cell.charge_throughput   
                battery.cell.temperature          = battery_conditions.cell.temperature 
                battery_discharge_flag            = battery_conditions.battery_discharge_flag               
             
                if bus.fixed_voltage: 
                    voltage = bus.voltage * state.ones_row(1)
                else:    
                    voltage = battery.compute_voltage(battery_conditions)   
                    
                if battery_discharge_flag:    
                    total_current       = 0. 
                     
                    # Avionics Power Consumtion 
                    avionics.power() 
                    
                    # Payload Power Consumtion 
                    payload.power()
                    
                    if bus.fixed_voltage:      
                        bus.outputs.avionics_power  = avionics.inputs.power 
                        bus.outputs.payload_power   = payload.inputs.power 
                        bus.outputs.total_esc_power = total_current*voltage
                        bus.logic(conditions,numerics)             
                
                        # link to battery                  
                        battery.outputs.current     = abs(bus.outputs.power)/voltage
                        battery.outputs.power       = bus.outputs.power*battery.bus_power_split_ratio 
                
                    else:       
                        # link to battery   
                        battery.outputs.current     = total_current + (avionics.inputs.power + payload.inputs.power)/voltage
                        battery.outputs.power       = battery.outputs.current*voltage
                
                    battery.energy_calc(numerics,conditions,bus.tag,battery_discharge_flag)       
                    pack_battery_conditions(battery_conditions,battery)               
                
                else: 
                    if bus.fixed_voltage:     
                        battery.outputs.current    =  battery.cell.charging_current*battery.pack.electrical_configuration.parallel * np.ones_like(voltage) 
                        battery.outputs.power      = -battery.outputs.current * (battery.cell.charging_voltage*battery.pack.electrical_configuration.series)*battery.bus_power_split_ratio   
                    else: 
                        # link to battery     
                        battery.outputs.current    =  battery.cell.charging_current*battery.pack.electrical_configuration.parallel * np.ones_like(voltage) 
                        battery.outputs.power      = -battery.outputs.current * (battery.cell.charging_voltage*battery.pack.electrical_configuration.series) 

                 
                battery.energy_calc(numerics,conditions,bus.tag,battery_discharge_flag) 
                pack_battery_conditions(battery_conditions,battery)             
                        
           
        conditions.energy.thrust_force_vector  = total_thrust
        conditions.energy.power                = total_power 
        conditions.energy.vehicle_mass_rate    = state.ones_row(1)*0.0   
        
        # A PATCH TO BE DELETED IN RCAIDE
        results                           = Data()
        results.thrust_force_vector       = np.zeros_like(voltage)  * [0,0,0]      
        results.vehicle_mass_rate         = state.ones_row(1)*0.0 
        
        return results 
     
    def unpack_unknowns(self,segment):
        """ This adds additional unknowns which are unpacked from the mission solver and send to the network.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs: 
            unknowns specific to the battery cell                  
    
            Outputs: 
            conditions specific to the battery cell 
    
            Properties Used:
            N/A
        """                          
        # unpack the ones function 
        busses       = segment.analyses.energy.networks.isolated_battery_cell.busses
        
        for bus in busses: 
            for battery in bus.batteries: 
                battery.assign_battery_unknowns(segment,bus,battery)        
        
        return     
     
    
    
    def residuals(self,segment):
        """ This packs the residuals to be sent to the mission solver.
   
           Assumptions:
           None
   
           Source:
           N/A
   
           Inputs: 
           residuals soecific to the battery cell   
           
           Outputs:
           residuals specific to battery cell and network
   
           Properties Used: 
           N/A
       """           
 
        busses   = segment.analyses.energy.networks.isolated_battery_cell.busses 
        for bus in busses:   
            for battery in bus.batteries: 
                battery.assign_battery_residuals(segment,bus,battery)    
         
        return      

    def add_unknowns_and_residuals_to_segment(self, 
                                              segment,  
                                              estimated_battery_voltages          = [[400]], 
                                              estimated_battery_cell_temperature  = [[283.]], 
                                              estimated_battery_state_of_charges  = [[0.5]],
                                              estimated_battery_cell_currents     = [[5.]]):
        """ This function sets up the information that the mission needs to run a mission segment using this network
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:  
            self                                [None]
            segment                             [None]
            estimated_battery_voltages          [volts]
            estimated_battery_cell_temperature  [Kelvin]
            estimated_battery_state_of_charges  [unitless]
            estimated_battery_cell_currents     [Amperes]
            
            Outputs
            None
            
            Properties Used:
            N/A
        """          
        busses   = segment.analyses.energy.networks.isolated_battery_cell.busses
        ones_row = segment.state.ones_row 
        segment.state.residuals.network = Residuals()  
         
        for bus_i, bus in enumerate(busses):   
            batteries                 = bus.batteries 

            # ------------------------------------------------------------------------------------------------------            
            # Create bus results data structure  
            # ------------------------------------------------------------------------------------------------------
            segment.state.conditions.energy[bus.tag] = RCAIDE.Analyses.Mission.Common.Conditions()            

            # ------------------------------------------------------------------------------------------------------            
            # Determine number of propulsor groups in bus
            # ------------------------------------------------------------------------------------------------------ 
            bus_results                             = segment.state.conditions.energy[bus.tag] 
             
            # ------------------------------------------------------------------------------------------------------
            # Assign battery residuals, unknowns and results data structures 
            # ------------------------------------------------------------------------------------------------------  
            
            if len(batteries) > 1 and (bus.fixed_voltage == False): 
                assert('The bus must have a fixed voltage is more than one battery is specified on the bus')  
                
            for b_i , battery in enumerate(batteries):        
                bus_results[battery.tag]                               = RCAIDE.Analyses.Mission.Common.Conditions() 
                bus_results[battery.tag].pack                          = RCAIDE.Analyses.Mission.Common.Conditions() 
                bus_results[battery.tag].pack.energy                   = ones_row(1)
                bus_results[battery.tag].pack.voltage_under_load       = ones_row(1)
                bus_results[battery.tag].pack.voltage_open_circuit     = ones_row(1)
                bus_results[battery.tag].pack.temperature              = ones_row(1)
                bus_results[battery.tag].pack.temperature              = ones_row(1)
                bus_results[battery.tag].cell                          = RCAIDE.Analyses.Mission.Common.Conditions() 
                bus_results[battery.tag].cell.state_of_charge          = ones_row(1)
                bus_results[battery.tag].cell.temperature              = ones_row(1)
                bus_results[battery.tag].cell.charge_throughput        = ones_row(1) 
                bus_results[battery.tag].cell.cycle_in_day             = 0
                bus_results[battery.tag].cell.resistance_growth_factor = 1.
                bus_results[battery.tag].cell.capacity_fade_factor     = 1.  
                append_initial_battery_conditions(segment,bus,battery)    
                
                # add unknowns and residuals specific to battery cell
                battery.append_battery_unknowns_and_residuals_to_segment(segment,
                                                                         bus,
                                                                         battery,
                                                                         estimated_battery_voltages[bus_i][b_i],
                                                                         estimated_battery_cell_temperature[bus_i][b_i], 
                                                                         estimated_battery_state_of_charges[bus_i][b_i], 
                                                                         estimated_battery_cell_currents[bus_i][b_i] )    
                
    
                # ------------------------------------------------------------------------------------------------------
                # Assign network-specific  residuals, unknowns and results data structures
                # ------------------------------------------------------------------------------------------------------ 
                if bus.fixed_voltage:   
                    # appennd residuals and unknowns for recharge segment                     
                    segment.state.unknowns['fv_' + battery.tag]          =  0* ones_row(1)  
                    segment.state.residuals.network['fv_' + battery.tag] =  0* ones_row(1)                
            
        # Ensure the mission knows how to pack and unpack the unknowns and residuals
        segment.process.iterate.unknowns.network                    = self.unpack_unknowns
        segment.process.iterate.residuals.network                   = self.residuals     

        return segment
    
    __call__ = evaluate_thrust


