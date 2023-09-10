# RCAIDE/Energy/Networks/Solar.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports 
import RCAIDE
from RCAIDE.Core                                  import Data 
from RCAIDE.Analyses.Mission.Segments.Conditions  import Residuals 
from RCAIDE.Components.Component                  import Container   
from RCAIDE.Energy.Converters                     import Propeller, Lift_Rotor, Prop_Rotor 
from RCAIDE.Methods.Power.Battery.Common          import pack_battery_conditions,append_initial_battery_conditions 
from RCAIDE.Methods.Propulsion.solar_propulsor    import compute_propulsor_performance, compute_unique_propulsor_groups
from .Network                                     import Network  

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Solar
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Components-Energy-Networks
class Solar(Network):
    """ A propeller-driven solar powered system with batteries and maximum power point tracking.  
        Electronic speed controllers, thermal management system, avionics, and other eletric 
        power systes paylaods are also modelled. Rotors and motors are arranged into groups,
        called propulsor groups, to siginify how they are connected in the network.  
        This network adds additional unknowns and residuals to the mission to determinge 
        the torque matching between motors and rotors in each propulsor group.  
    
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
        self.tag                                    = 'Solar' 
        self.avionics                               = None
        self.payload                                = None 
        self.busses                                 = Container()
        self.system_voltage                         = None   
        self.solar_flux                             = None
        self.maximum_power_point_tracking_efficency = 1.0
        self.solar_panel                            = None 
        self.system_voltage                         = None    
    
    # manage process with a driver function
    def evaluate_thrust(self,state):
        """ Calculate thrust given the current state of the vehicle
    
            Assumptions:
            Caps the throttle at 110% and linearly interpolates thrust off that
    
            Source:
            N/A
    
            Inputs:
            state [state()]
    
            Outputs:
            results.thrust_force_vector        [newtons]
            results.vehicle_mass_rate          [kg/s]
            conditions.energy                  [-]
    
            Properties Used:
            Defaulted values
        """          

        # unpack   
        conditions   = state.conditions
        numerics     = state.numerics
        busses       = self.busses
        avionics     = self.avionics
        payload      = self.payload 
        solar_flux   = self.solar_flux
        solar_panel  = self.solar_panel 
         
        total_thrust        = 0. * state.ones_row(3)
        total_power         = 0. * state.ones_row(1) 
        for bus in busses:
            batteries      = bus.batteries     
            motors         = bus.motors
            rotors         = bus.rotors 
            escs           = bus.electronic_speed_controllers   

            for battery in batteries:               
                battery_conditions               = state.conditions.energy[bus.tag][battery.tag] 
                battery.pack.current_energy      = battery_conditions.pack.energy 
                battery.pack.maximum_energy      = battery_conditions.pack.maximum_degraded_battery_energy     
                battery.pack.temperature         = battery_conditions.pack.temperature
                battery.cell.age                 = battery_conditions.cell.cycle_in_day    
                battery.cell.charge_throughput   = battery_conditions.cell.charge_throughput   
                battery.cell.temperature         = battery_conditions.cell.temperature
                battery.cell.R_growth_factor     = battery_conditions.cell.resistance_growth_factor
                battery.cell.E_growth_factor     = battery_conditions.cell.capacity_fade_factor  
                battery_discharge_flag           = battery_conditions.battery_discharge_flag              
             
                if bus.fixed_voltage: 
                    voltage = bus.voltage * state.ones_row(1)
                else:    
                    voltage = battery.compute_voltage(battery_conditions)   
                     
                total_current       = 0.  
                for i in range(state.conditions.energy[bus.tag].number_of_propulsor_groups):
                    if bus.active_propulsor_groups[i]:           
                        pg_tag              = state.conditions.energy[bus.tag].active_propulsor_groups[i]
                        N_rotors            = state.conditions.energy[bus.tag].N_rotors
                        outputs , T , P, I  = compute_propulsor_performance(i,bus.tag,pg_tag,motors,rotors,N_rotors,escs,state,voltage)  
                        total_current       += I
                        total_thrust        += T       
                        total_power         += P   
            
                # Avionics Power Consumtion 
                avionics.power() 
                
                # Payload Power Consumtion 
                payload.power() 
            
                # step 1
                solar_flux.solar_radiation(conditions)
                
                # link
                solar_panel.inputs.flux = solar_flux.outputs.flux
                
                # step 2
                solar_panel.power()
                
                # link
                bus.inputs.power            = solar_panel.outputs.power/self.maximum_power_point_tracking_efficency  
                bus.outputs.avionics_power  = avionics.inputs.power 
                bus.outputs.payload_power   = payload.inputs.power 
                bus.outputs.total_esc_power = total_current*voltage 
                bus.logic(conditions,numerics)             
                
                # link to battery                  
                battery.outputs.current     = bus.outputs.power/voltage
                battery.outputs.power       = bus.outputs.power*battery.bus_power_split_ratio
                 
                battery.energy_calc(numerics,conditions.freestream,battery_discharge_flag)       
                pack_battery_conditions(battery_conditions,battery)                
                    
        # Pack the conditions for outputs 
        conditions.energy.solar_flux           = solar_flux.outputs.flux      
        conditions.energy.thrust_force_vector  = total_thrust
        conditions.energy.power                = total_power 
        conditions.energy.vehicle_mass_rate    = state.ones_row(1)*0.0  
        

        # --------------------------------------------------        
        # A PATCH TO BE DELETED IN RCAIDE
        results                           = Data()
        results.thrust_force_vector       = total_thrust
        results.vehicle_mass_rate         = state.ones_row(1)*0.0  
        # --------------------------------------------------
        
        return results 
    
    
    def unpack_unknowns(self,segment):
        """ This is an extra set of unknowns which are unpacked from the mission solver and send to the network.
    
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
        ones_row     = segment.state.ones_row
        busses       = segment.analyses.energy.networks.solar.busses
        
        for bus in busses:
            if type(segment) != RCAIDE.Analyses.Mission.Segments.Ground.Battery_Recharge:  
                bus_results             = segment.state.conditions.energy[bus.tag] 
                active_propulsor_groups = bus_results.active_propulsor_groups
                for i in range(len(active_propulsor_groups)): 
                    pg_tag = active_propulsor_groups[i]           
                    bus_results[pg_tag].rotor.power_coefficient = segment.state.unknowns[bus.tag + '_' + pg_tag + '_rotor_cp'] 
                    if type(segment) != RCAIDE.Analyses.Mission.Segments.Ground.Battery_Recharge:     
                        bus_results[pg_tag].throttle = segment.state.unknowns[bus.tag + '_' + pg_tag + '_throttle']
                    else: 
                        bus_results[pg_tag].rotor.power_coefficient = 0. * ones_row(1)
                        bus_results[pg_tag].throttle                = 0. * ones_row(1)  
      
        return
    
    def residuals(self,segment):
        """ This packs the residuals to be send to the mission solver.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            state.conditions.energy:
                motor_torque                      [N-m]
                rotor_torque                      [N-m]
            
            Outputs:
            None
    
            Properties Used:
            None
        """  
         
        busses   = segment.analyses.energy.networks.solar.busses 
        for bus in busses:  
            if type(segment) != RCAIDE.Analyses.Mission.Segments.Ground.Battery_Recharge:  
                bus_results             = segment.state.conditions.energy[bus.tag] 
                active_propulsor_groups = bus_results.active_propulsor_groups
                for i in range(len(active_propulsor_groups)): 
                    q_motor   = bus_results[active_propulsor_groups[i]].motor.torque
                    q_prop    = bus_results[active_propulsor_groups[i]].rotor.torque 
                    segment.state.residuals.network[ bus.tag + '_' + active_propulsor_groups[i] + '_rotor_motor_torque'] = q_motor - q_prop
    
        return 
    
    ## @ingroup Components-Energy-Networks
    def add_unknowns_and_residuals_to_segment(self, 
                                              segment, 
                                              estimated_propulsor_group_throttles = [[]], 
                                              estimated_rotor_power_coefficients  = [[]],):
        """ This function sets up the information that the mission needs to run a mission segment using this network

            Assumptions:
            None

            Source:
            N/A

            Inputs:
            segment 

            Outputs:
            segment.state.unknowns.battery_voltage_under_load
            segment.state.unknowns.rotor_power_coefficient
            segment.state.conditions.energy.motor.torque
            segment.state.conditions.energy.rotor.torque   

            Properties Used:
            N/A
        """              
        busses   = segment.analyses.energy.networks.solar.busses
        ones_row = segment.state.ones_row 
        segment.state.residuals.network = Residuals() 

        if 'throttle' in segment.state.unknowns: 
            segment.state.unknowns.pop('throttle')
        if 'throttle' in segment.state.conditions.energy: 
            segment.state.conditions.energy.pop('throttle')

        for bus_i, bus in enumerate(busses):  
            active_propulsor_groups   = bus.active_propulsor_groups 
            N_active_propulsor_groups = len(active_propulsor_groups)
            batteries                 = bus.batteries 

            # ------------------------------------------------------------------------------------------------------            
            # Create bus results data structure  
            # ------------------------------------------------------------------------------------------------------
            segment.state.conditions.energy[bus.tag] = RCAIDE.Analyses.Mission.Segments.Conditions.Conditions()            

            # ------------------------------------------------------------------------------------------------------            
            # Determine number of propulsor groups in bus
            # ------------------------------------------------------------------------------------------------------
            sorted_propulsors                       = compute_unique_propulsor_groups(bus)
            bus_results                             = segment.state.conditions.energy[bus.tag]
            bus_results.number_of_propulsor_groups  = N_active_propulsor_groups
            bus_results.active_propulsor_groups     = active_propulsor_groups
            bus_results.N_rotors                    = sorted_propulsors.N_rotors

            # ------------------------------------------------------------------------------------------------------
            # Assign battery residuals, unknowns and results data structures 
            # ------------------------------------------------------------------------------------------------------  
            for b_i , battery in enumerate(batteries):     
                bus_results[battery.tag]                               = RCAIDE.Analyses.Mission.Segments.Conditions.Conditions() 
                bus_results[battery.tag].pack                          = RCAIDE.Analyses.Mission.Segments.Conditions.Conditions() 
                bus_results[battery.tag].cell                          = RCAIDE.Analyses.Mission.Segments.Conditions.Conditions() 
                bus_results[battery.tag].pack.energy                   = ones_row(1)
                bus_results[battery.tag].pack.voltage_under_load       = ones_row(1)
                bus_results[battery.tag].pack.voltage_open_circuit     = ones_row(1)
                bus_results[battery.tag].pack.temperature              = ones_row(1)
                bus_results[battery.tag].cell.state_of_charge          = ones_row(1)
                bus_results[battery.tag].cell.temperature              = ones_row(1)
                bus_results[battery.tag].cell.charge_throughput        = ones_row(1) 
                bus_results[battery.tag].cell.cycle_in_day             = 0
                bus_results[battery.tag].cell.resistance_growth_factor = 1.
                bus_results[battery.tag].cell.capacity_fade_factor     = 1. 
                append_initial_battery_conditions(segment,bus,battery)    

            # ------------------------------------------------------------------------------------------------------
            # Assign network-specific  residuals, unknowns and results data structures
            # ------------------------------------------------------------------------------------------------------
            for i in range(len(sorted_propulsors.unique_rotor_tags)):  
                if type(segment) == RCAIDE.Analyses.Mission.Segments.Ground.Battery_Recharge:   
                    # appennd residuals and unknowns for recharge segment                     
                    segment.state.unknowns['recharge'+ active_propulsor_groups[i]]          =  0* ones_row(1)  
                    segment.state.residuals.network['recharge'+ active_propulsor_groups[i]] =  0* ones_row(1)  
                # appennd rotor power coefficient unknown for each propulsor group                    
                try: 
                    cp_init = estimated_rotor_power_coefficients[bus_i][i]
                except: 
                    rotor   = bus.rotors[sorted_propulsors.unique_rotor_tags[i]] 
                    if rotor.propulsor_group ==  active_propulsor_groups[i]: 
                        if type(rotor) == Propeller:
                            cp_init  = float(rotor.cruise.design_power_coefficient)
                        elif (type(rotor) == Lift_Rotor) or (type(rotor) == Prop_Rotor):
                            cp_init  = float(rotor.hover.design_power_coefficient)    
                segment.state.unknowns[ bus.tag + '_' + active_propulsor_groups[i] + '_rotor_cp']                    = cp_init * ones_row(1)  
                segment.state.residuals.network[ bus.tag + '_' + active_propulsor_groups[i] + '_rotor_motor_torque'] = 0. * ones_row(1)            

                # append throttle unknown 
                if type(segment) != RCAIDE.Analyses.Mission.Segments.Ground.Takeoff or type(segment) == RCAIDE.Analyses.Mission.Segments.Ground.Landing:   
                    try: 
                        initial_throttle = estimated_propulsor_group_throttles[bus_i][i]
                    except:  
                        initial_throttle = 0.5 
                    segment.state.unknowns[bus.tag + '_' + active_propulsor_groups[i]+ '_throttle'] = initial_throttle* ones_row(1)    

                # Results data structure for each propulsor group    
                pg_tag                                      = active_propulsor_groups[i] 
                bus_results[pg_tag]                         = RCAIDE.Analyses.Mission.Segments.Conditions.Conditions()
                bus_results[pg_tag].motor                   = RCAIDE.Analyses.Mission.Segments.Conditions.Conditions()
                bus_results[pg_tag].rotor                   = RCAIDE.Analyses.Mission.Segments.Conditions.Conditions() 
                bus_results[pg_tag].unique_rotor_tags       = sorted_propulsors.unique_rotor_tags
                bus_results[pg_tag].unique_motor_tags       = sorted_propulsors.unique_motor_tags
                bus_results[pg_tag].unique_esc_tags         = sorted_propulsors.unique_esc_tags 
                bus_results[pg_tag].y_axis_rotation         = 0. * ones_row(1)  
                bus_results[pg_tag].motor.efficiency        = 0. * ones_row(1)
                bus_results[pg_tag].motor.torque            = 0. * ones_row(1) 
                bus_results[pg_tag].rotor.torque            = 0. * ones_row(1)
                bus_results[pg_tag].rotor.thrust            = 0. * ones_row(1)
                bus_results[pg_tag].rotor.rpm               = 0. * ones_row(1)
                bus_results[pg_tag].rotor.disc_loading      = 0. * ones_row(1)                 
                bus_results[pg_tag].rotor.power_loading     = 0. * ones_row(1)
                bus_results[pg_tag].rotor.tip_mach          = 0. * ones_row(1)
                bus_results[pg_tag].rotor.efficiency        = 0. * ones_row(1)   
                bus_results[pg_tag].rotor.figure_of_merit   = 0. * ones_row(1) 
                bus_results[pg_tag].rotor.power_coefficient = 0. * ones_row(1)    

        # Ensure the mission knows how to pack and unpack the unknowns and residuals
        segment.process.iterate.unknowns.network                    = self.unpack_unknowns
        segment.process.iterate.residuals.network                   = self.residuals        

        return segment    
            
    __call__ = evaluate_thrust
