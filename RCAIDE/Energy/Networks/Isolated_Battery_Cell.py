# RCAIDE/Energy/Networks/Battery_Cell_Isolated.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
 # RCAIDE imports   
from RCAIDE.Analyses.Mission.Segments.Conditions                           import Residuals
from RCAIDE.Core                                                           import Data
from RCAIDE.Methods.Power.Battery.Common.pack_battery_conditions           import pack_battery_conditions
from RCAIDE.Methods.Power.Battery.Common.append_initial_battery_conditions import append_initial_battery_conditions
from .Network import Network 
from RCAIDE.Components.Component                  import Container  
 
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
        self.avionics                = None
        self.voltage                 = None  
        self.batteries               = Container()
        
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
                current                       [amps]
                battery_power_draw            [watts]
                initial_battery_state_of_charge              [joules]
                battery_voltage_open_circuit  [volts]
                battery_voltage_under_load    [volts]  
    
            Properties Used:
            Defaulted values
        """          
    
        # unpack
        conditions        = state.conditions
        numerics          = state.numerics 
        avionics          = self.avionics 
        batteries         = self.batteries    
         

        battery_key                      = list(batteries.keys())[0]
        battery                          = batteries[battery_key] 
        battery_conditions               = conditions.energy['battery_0'] 
        battery.pack.current_energy      = battery_conditions.pack.energy
        battery.pack.maximum_energy      = battery_conditions.pack.maximum_degraded_battery_energy  
        battery.pack.temperature         = battery_conditions.pack.temperature
        battery.cell.charge_throughput   = battery_conditions.cell.charge_throughput     
        battery.cell.age                 = battery_conditions.cell.cycle_in_day        
        battery.cell.R_growth_factor     = battery_conditions.cell.resistance_growth_factor
        battery.cell.E_growth_factor     = battery_conditions.cell.capacity_fade_factor 
        battery_discharge_flag           = battery_conditions.battery_discharge_flag     
        volts                            = battery.compute_voltage(battery_conditions)   
           
        #-------------------------------------------------------------------------------
        # Discharge
        #-------------------------------------------------------------------------------
        if battery_discharge_flag:
            # Calculate avionics and payload power
            avionics_power = np.ones((numerics.number_of_control_points,1))*avionics.current * volts
        
            # Calculate avionics and payload current
            avionics_current =  np.ones((numerics.number_of_control_points,1))*avionics.current    
            
            # link
            battery.outputs.current  = avionics_current
            battery.outputs.power    = -avionics_power
            battery.inputs.voltage  = volts
            battery.energy_calc(numerics,conditions.freestream,battery_discharge_flag)          
            
        else: 
            battery.outputs.current  = -battery.charging_current * np.ones_like(volts)
            battery.inputs.voltage  =  battery.charging_voltage * np.ones_like(volts) 
            battery.outputs.power    =  -battery.outputs.current * battery.inputs.voltage * np.ones_like(volts)
            battery.energy_calc(numerics,conditions.freestream,battery_discharge_flag)        
        
        # Pack the conditions for outputs       
        pack_battery_conditions(battery_conditions,battery) 
          
        F     = np.zeros_like(volts)  * [0,0,0]      
        mdot  = state.ones_row(1)*0.0 
         
        results                           = Data()
        results.thrust_force_vector       = F
        results.vehicle_mass_rate         = mdot
        
        return results 
    

     
    def unpack_unknowns(self,segment):
        """ This is an extra set of unknowns which are unpacked from the mission solver and send to the network.
    
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
        # unpack 
        batteries      = self.batteries  
        for b_i in range(len(batteries)): 
            battery_key    = list(batteries.keys())[b_i] 
            battery        = batteries[battery_key]  
              
            # append battery unknowns 
            battery.assign_battery_unknowns(segment,b_i)   
        return  

    
    
    def residuals(self,segment):
        """ This packs the residuals to be sent to the mission solver.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            unknowns specific to the battery cell 
            
            Outputs:
            residuals specific to the battery cell
    
            Properties Used: 
            N/A
        """         
        # unpack 
        network        = self 
        batteries      = self.batteries 
        for b_i in range(len(batteries)): 
            battery_key    = list(batteries.keys())[b_i] 
            battery        = batteries[battery_key]  
             
            # append battery residuals 
            battery.assign_battery_residuals(segment,b_i,network)   
                
        return     

    def add_unknowns_and_residuals_to_segment(self, 
                                              segment, 
                                              estimated_battery_voltages             = None, 
                                              estimated_battery_cell_temperature     = [300] , 
                                              estimated_battery_state_of_charges     = [0.5],
                                              estimated_battery_cell_currents        = [5.]):
        """ This function sets up the information that the mission needs to run a mission segment using this network
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:  
            estimated_battery_voltages                  [volts]
            estimated_battery_cell_temperature      [Kelvin]
            estimated_battery_state_of_charges  [unitless]
            estimated_battery_cell_currents          [Amperes]
            
            Outputs
            None
            
            Properties Used:
            N/A
        """          
        
        batteries      = self.batteries 
        for b_i in range(len(batteries)): 
            battery_key    = list(batteries.keys())[b_i] 
            battery        = batteries[battery_key]  
     
            for b_i in range(len(batteries)):  
                battery_key    = list(batteries.keys())[b_i] 
                battery        = batteries[battery_key]   
                if estimated_battery_voltages  == None: 
                    estimated_voltage  = battery.pack.maximum_voltage 
                else:
                    estimated_voltage  = estimated_battery_voltages[b_i]            
            
            # Assign initial segment conditions to segment if missing 
            append_initial_battery_conditions(segment,battery,b_i)          
                
            segment.state.residuals.network = Residuals()
            
            # add unknowns and residuals specific to battery cell
            battery.append_battery_unknowns_and_residuals_to_segment(segment,
                                                                     bus_tag,
                                                                     estimated_voltage,
                                                                     estimated_battery_cell_temperature[b_i], 
                                                                     estimated_battery_state_of_charges[b_i],
                                                                     estimated_battery_cell_currents[b_i])  
        
        # Ensure the mission knows how to pack and unpack the unknowns and residuals
        segment.process.iterate.unknowns.network  = self.unpack_unknowns
        segment.process.iterate.residuals.network = self.residuals        

        return segment
    
    __call__ = evaluate_thrust


