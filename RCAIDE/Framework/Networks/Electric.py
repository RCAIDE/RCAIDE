## @ingroup Energy-Networks
# RCAIDE/Energy/Networks/Electric.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
    # RCAIDE imports 
import RCAIDE  
from RCAIDE.Framework.Mission.Common                      import Residuals
from RCAIDE.Library.Mission.Common.Unpack_Unknowns.energy import bus_unknowns
from .Network                                             import Network              
from RCAIDE.Library.Methods.Propulsors.Common.compute_avionics_power_draw import compute_avionics_power_draw
from RCAIDE.Library.Methods.Propulsors.Common.compute_payload_power_draw  import compute_payload_power_draw
# Python imports
import  numpy as  np 

# ----------------------------------------------------------------------------------------------------------------------
#  All Electric
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Networks
class Electric(Network):
    """ A network comprising battery pack(s) to power rotors using electric motors via a bus.
        Electronic speed controllers, thermal management system, avionics, and other eletric 
        power systes paylaods are also modelled. Rotors and motors are arranged into groups,
        called propulsor groups, to siginify how they are connected in the network.     
        The network adds additional unknowns and residuals to the mission to determinge 
        the torque matching between motors and rotors in each propulsor group.  

        Assumptions:
        The y axis rotation is used for rotating the rotor about the Y-axis for tilt rotors and tiltwings

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

        self.tag                          = 'electric'
        self.system_voltage               = None   
        self.reverse_thrust               = False
        self.wing_mounted                 = True        

    # manage process with a driver function
    def evaluate(self,state,center_of_gravity):
        """ Calculate thrust given the current state of the vehicle

            Assumptions:
            Caps the throttle at 110% and linearly interpolates thrust off that

            Source:
            N/A

            Inputs:
            state [state()]

            Outputs:
            results.thrust_force_vector         [newtons]
            results.vehicle_mass_rate           [kg/s]
            conditions.energy                   [-]    

            Properties Used:
            Defaulted values
        """          

        # unpack   
        conditions      = state.conditions 
        busses          = self.busses
        coolant_lines   = self.coolant_lines
        total_thrust    = 0. * state.ones_row(3) 
        total_power     = 0. * state.ones_row(1) 
        total_moment    = 0. * state.ones_row(3) 
        recharging_flag = conditions.energy.recharging 
        reverse_thrust  = self.reverse_thrust

        for bus in busses:
            if bus.active:             
                avionics        = bus.avionics
                payload         = bus.payload  
                batteries       = bus.batteries

                # Avionics Power Consumtion
                avionics_conditions = state.conditions.energy[bus.tag][avionics.tag]
                compute_avionics_power_draw(avionics,avionics_conditions,conditions)

                # Payload Power
                payload_conditions = state.conditions.energy[bus.tag][payload.tag]
                compute_payload_power_draw(payload,payload_conditions,conditions)

                # Bus Voltage 
                bus_voltage = bus.voltage * state.ones_row(1)

                if recharging_flag:
                    for battery in batteries: 
                        # append compoment power to bus 
                        avionics_power         = (avionics_conditions.power*battery.bus_power_split_ratio)/len(batteries)* state.ones_row(1)
                        payload_power          = (payload_conditions.power*battery.bus_power_split_ratio)/len(batteries)* state.ones_row(1)            
                        total_esc_power        = 0 * state.ones_row(1)     
                        charging_power         = (state.conditions.energy[bus.tag][battery.tag].pack.charging_current*bus_voltage*battery.bus_power_split_ratio)/len(batteries)

                        # append bus outputs to battery
                        battery_conditions                   = state.conditions.energy[bus.tag][battery.tag] 
                        battery_conditions.pack.power_draw   = ((avionics_power + payload_power + total_esc_power) - charging_power)/bus.efficiency
                        battery_conditions.pack.current_draw = -battery_conditions.pack.power_draw/bus_voltage

                else:       
                    # compute energy consumption of each battery on bus  
                    for battery in batteries: 
                        stored_results_flag  = False
                        stored_propulsor_tag = None 
                        for propulsor in bus.propulsors:  
                            if propulsor.active == True:  
                                if bus.identical_propulsors == False:
                                    # run analysis  
                                    T,M,P,stored_results_flag,stored_propulsor_tag = propulsor.compute_performance(state,bus,bus_voltage,center_of_gravity)
                                else:             
                                    if stored_results_flag == False: 
                                        # run propulsor analysis 
                                        T,M,P,stored_results_flag,stored_propulsor_tag = propulsor.compute_performance(state,bus,bus_voltage,center_of_gravity)
                                    else:
                                        # use previous propulsor results 
                                        T,M,P = propulsor.reuse_stored_data(state,bus,stored_propulsor_tag,center_of_gravity)

                                total_thrust += T   
                                total_moment += M   
                                total_power  += P 

                        # compute power from each componemnt 
                        avionics_power  = (avionics_conditions.power*battery.bus_power_split_ratio)/len(batteries)* state.ones_row(1) 
                        payload_power   = (payload_conditions.power*battery.bus_power_split_ratio)/len(batteries) * state.ones_row(1)   
                        charging_power  = (state.conditions.energy[bus.tag][battery.tag].pack.charging_current*bus_voltage*battery.bus_power_split_ratio)/len(batteries) 
                        total_esc_power = total_power*battery.bus_power_split_ratio  

                        # append bus outputs to battery 
                        battery_conditions                    = state.conditions.energy[bus.tag][battery.tag] 
                        battery_conditions.pack.power_draw    = ((avionics_power + payload_power + total_esc_power) - charging_power)/bus.efficiency
                        battery_conditions.pack.current_draw  = battery_conditions.pack.power_draw/bus_voltage
                        #battery.energy_calc(state,bus,coolant_lines,recharging_flag)
        
        time               = state.conditions.frames.inertial.time[:,0] 
        delta_t            = np.diff(time)
        for t_idx in range(state.numerics.number_of_control_points):
            if recharging_flag:
                for bus in  busses:
                    for battery in  bus.batteries:
                        battery.energy_calc(state,bus,coolant_lines, t_idx, delta_t, recharging_flag)                
            else:
                for bus in  busses:
                    for battery in  bus.batteries:
                        battery.energy_calc(state,bus,coolant_lines, t_idx, delta_t, recharging_flag)
                    for coolant_line in  coolant_lines:
                        if t_idx != state.numerics.number_of_control_points-1:
                            for tag, item in  coolant_line.items(): 
                                if tag == 'heat_exchangers':
                                    for heat_exchanger in  item:
                                            heat_exchanger.compute_heat_exchanger_performance(state,coolant_line,delta_t[t_idx],t_idx)
                                if tag == 'reservoirs':
                                    for reservoir in  item:
                                        reservoir.compute_reservior_coolant_temperature(state,coolant_line,delta_t[t_idx],t_idx)      
                                


        if reverse_thrust ==  True:
            total_thrust =  total_thrust * -1     
            total_moment =  total_moment* -1                    
        conditions.energy.thrust_force_vector  = total_thrust
        conditions.energy.power                = total_power 
        conditions.energy.thrust_moment_vector = total_moment
        conditions.energy.vehicle_mass_rate    = state.ones_row(1)*0.0  

        return   
        
        
        


    def unpack_unknowns(self,segment):
        """ This adds additional unknowns which are unpacked from the mission solver and send to the network.

            Assumptions:
            None

            Source:
            N/A

            Inputs:
            unknowns specific to the rotors                        [None] 
            unknowns specific to the battery cell                  

            Outputs:
            state.conditions.energy.bus.rotor.power_coefficient(s) [None] 
            conditions specific to the battery cell 

            Properties Used:
            N/A
        """                          
        # unpack the ones function 
        busses       = segment.analyses.energy.vehicle.networks.electric.busses
        bus_unknowns(segment,busses) 

        for bus in busses:           
            if type(segment) == RCAIDE.Framework.Mission.Segments.Ground.Battery_Recharge or type(segment) == RCAIDE.Framework.Mission.Segments.Ground.Battery_Discharge:
                pass 
            elif bus.active and len(bus.propulsors) > 0:
                reference_propulsor = bus.propulsors[list(bus.propulsors.keys())[0]]                 
                for propulsor in  bus.propulsors: 
                    propulsor.unpack_propulsor_unknowns(reference_propulsor,segment,bus)
                    
        return     

    def residuals(self,segment):
        """ This packs the residuals to be sent to the mission solver.

           Assumptions:
           None

           Source:
           N/A

           Inputs:
           state.conditions.energy:
               motor(s).torque                      [N-m]
               rotor(s).torque                      [N-m] 
           residuals soecific to the battery cell   

           Outputs:
           residuals specific to battery cell and network

           Properties Used: 
           N/A
        """           

        busses   = segment.analyses.energy.vehicle.networks.electric.busses 
        for bus in busses:             
            if type(segment) == RCAIDE.Framework.Mission.Segments.Ground.Battery_Recharge or type(segment) == RCAIDE.Framework.Mission.Segments.Ground.Battery_Discharge:
                pass 
            elif bus.active and len(bus.propulsors) > 0:
                propulsor = bus.propulsors[list(bus.propulsors.keys())[0]]
                propulsor.pack_propulsor_residuals(segment,bus)  
        return     

    ## @ingroup Components-Energy-Networks
    def add_unknowns_and_residuals_to_segment(self, segment):
        """ This function sets up the information that the mission needs to run a mission segment using this network

            Assumptions:
            None

            Source:
            N/A

            Inputs:
            segment
            estimated_battery_voltages                                    [v]
            estimated_rotor_power_coefficients                            [float]s
            estimated_battery_cell_temperature                            [Kelvin]
            estimated_battery_state_of_charges                            [unitless]
            estimated_battery_cell_currents                               [Amperes]

            Outputs: 
            segment

            Properties Used:
            N/Abattery_tms in item
        """              
        busses          = segment.analyses.energy.vehicle.networks.electric.busses
        coolant_lines  = segment.analyses.energy.vehicle.networks.electric.coolant_lines 
        segment.state.residuals.network = Residuals()

        for bus_i, bus in enumerate(busses):  
            # ------------------------------------------------------------------------------------------------------            
            # Create bus results data structure  
            # ------------------------------------------------------------------------------------------------------
            segment.state.conditions.energy[bus.tag] = RCAIDE.Framework.Mission.Common.Conditions() 
            segment.state.conditions.noise[bus.tag]  = RCAIDE.Framework.Mission.Common.Conditions()   

            # ------------------------------------------------------------------------------------------------------
            # Assign network-specific  residuals, unknowns and results data structures
            # ------------------------------------------------------------------------------------------------------ 
            for tag, item in  bus.items():
                if tag == 'batteries':
                    for battery in item:
                        battery.append_operating_conditions(segment,bus)
                elif tag == 'propulsors':  
                    for i, propulsor in enumerate(item):  
                        add_additional_network_equation = (bus.active) and  (i == 0)   
                        propulsor.append_operating_conditions(segment,bus,add_additional_network_equation)
                        for sub_tag, sub_item in  propulsor.items(): 
                            if issubclass(type(sub_item), RCAIDE.Library.Components.Component):
                                sub_item.append_operating_conditions(segment,bus,propulsor)  
                elif issubclass(type(item), RCAIDE.Library.Components.Component):
                    item.append_operating_conditions(segment,bus)
                    
        #ZIP does not work when there is none in the coolant line             
        for coolant_line_i, coolant_line in enumerate(coolant_lines):  
            # ------------------------------------------------------------------------------------------------------            
            # Create coolant_lines results data structure  
            # ------------------------------------------------------------------------------------------------------
            segment.state.conditions.energy[coolant_line.tag] = RCAIDE.Framework.Mission.Common.Conditions()        
            # ------------------------------------------------------------------------------------------------------
            # Assign network-specific  residuals, unknowns and results data structures
            # ------------------------------------------------------------------------------------------------------ 
            for tag, item in  coolant_line.items(): 
                if tag == 'batteries':
                    for battery in item:
                        for btms in  battery:
                            btms.append_operating_conditions(segment,coolant_line)
                if tag == 'heat_exchangers':
                    for heat_exchanger in  item:
                        heat_exchanger.append_operating_conditions(segment, coolant_line)
                if tag == 'reservoirs':
                    for reservoir in  item:
                        reservoir.append_operating_conditions(segment, coolant_line)                

        
        # Ensure the mission knows how to pack and unpack the unknowns and residuals
        segment.process.iterate.unknowns.network            = self.unpack_unknowns
        segment.process.iterate.residuals.network           = self.residuals        

        return segment

    __call__ = evaluate 

