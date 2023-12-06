## @ingroup Energy-Networks
# RCAIDE/Energy/Networks/Solar.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports 
import RCAIDE
from RCAIDE.Core                                              import Data 
from RCAIDE.Analyses.Mission.Common                           import Residuals   
from RCAIDE.Energy.Propulsors.Converters                      import Propeller, Lift_Rotor, Prop_Rotor 
from RCAIDE.Methods.Power.Battery.Common                      import append_initial_battery_conditions 
from RCAIDE.Methods.Propulsion.Performance.solar_propulsor    import solar_propulsor
from .Network                                                 import Network  
 
# ----------------------------------------------------------------------------------------------------------------------
#  Solar
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Networks
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
        conditions      = state.conditions
        numerics        = state.numerics
        busses          = self.busses
        solar_flux      = self.solar_flux
        total_thrust    = 0. * state.ones_row(3) 
        total_power     = 0. * state.ones_row(1)  
        recharging_flag = conditions.energy.recharging 
        
    
        for bus in busses: 
            avionics        = bus.avionics
            payload         = bus.payload   
            solar_panel     = bus.solar_panel
                  
            # Avionics Power Consumtion 
            avionics.power() 
    
            # Payload Power 
            payload.power() 
             
        
            # step 1
            solar_flux.solar_radiation(conditions)
            
            # link
            solar_panel.inputs.flux = solar_flux.outputs.flux
            
            # step 2
            solar_panel.power() 
    
            # Bus Voltage 
            bus_voltage = bus.voltage * state.ones_row(1)
            if recharging_flag:
                for battery in bus.batteries:   
                    # append compoment power to bus 
                    bus.inputs.secondary_power  = solar_panel.outputs.power/self.maximum_power_point_tracking_efficency  
                    bus.outputs.avionics_power  = avionics.inputs.power*battery.bus_power_split_ratio* state.ones_row(1)
                    bus.outputs.payload_power   = payload.inputs.power*battery.bus_power_split_ratio* state.ones_row(1)            
                    bus.outputs.total_esc_power =  -state.conditions.energy[bus.tag][battery.tag].pack.current*bus_voltage*battery.bus_power_split_ratio
                    bus.outputs.voltage         = bus_voltage
    
                    # run bus 
                    bus.logic(conditions,numerics)                    
    
                    # append bus outputs to battery 
                    battery.outputs.current     = -bus.inputs.current
                    battery.outputs.power       = bus.inputs.power       
                    battery.energy_calc(state,bus,recharging_flag)  
            else:          
                bus_T,bus_P,bus_I  = solar_propulsor(bus,state,bus_voltage)  
                total_thrust      += bus_T
                total_power       += bus_P   
    
                # compute energy calculation for each battery on bus  
                for battery in bus.batteries: 
                    # append compoment power to bus 
                    bus.inputs.secondary_power  = solar_panel.outputs.power/self.maximum_power_point_tracking_efficency  
                    bus.outputs.avionics_power  = avionics.inputs.power*battery.bus_power_split_ratio* state.ones_row(1) 
                    bus.outputs.payload_power   = payload.inputs.power*battery.bus_power_split_ratio * state.ones_row(1)  
                    bus.outputs.total_esc_power = total_power*battery.bus_power_split_ratio 
                    bus.outputs.voltage         = bus_voltage
    
                    # run bus 
                    bus.logic(conditions,numerics)                    
    
                    # append bus outputs to battery 
                    battery.outputs.current     = bus.inputs.current
                    battery.outputs.power       = bus.inputs.power       
                    battery.energy_calc(state,bus,recharging_flag)       
            
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
                for propulsor in bus.propulsors: 
                    bus_results[propulsor.tag].rotor.power_coefficient = segment.state.unknowns[bus.tag + '_rotor_cp'] 
                    if type(segment) != RCAIDE.Analyses.Mission.Segments.Ground.Battery_Recharge:      
                        bus_results.throttle = segment.state.unknowns[bus.tag + '_throttle']
                    else: 
                        bus_results[propulsor.tag].rotor.power_coefficient = 0. * ones_row(1)
                        bus_results.throttle = 0. * ones_row(1)  
      
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
                bus_results   = segment.state.conditions.energy[bus.tag]   
                for propulsor in bus.propulsors:         
                    q_motor   = bus_results[propulsor.tag].motor.torque
                    q_prop    = bus_results[propulsor.tag].rotor.torque 
                    segment.state.residuals.network[ bus.tag + '_rotor_motor_torque'] = q_motor - q_prop
    
        return 
    
    ## @ingroup Components-Energy-Networks
    def add_unknowns_and_residuals_to_segment(self, 
                                              segment, 
                                              estimated_propulsor_group_throttles = [[0.5]], 
                                              estimated_rotor_power_coefficients  = [[0.02]],):
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
            batteries                                = bus.batteries 

            # ------------------------------------------------------------------------------------------------------            
            # Create bus results data structure  
            # ------------------------------------------------------------------------------------------------------
            segment.state.conditions.energy[bus.tag] = RCAIDE.Analyses.Mission.Common.Conditions()    
            bus_results                              = segment.state.conditions.energy[bus.tag]    
            segment.state.conditions.noise[bus.tag]  = RCAIDE.Analyses.Mission.Common.Conditions()  
            noise_results                            = segment.state.conditions.noise[bus.tag] 

            # ------------------------------------------------------------------------------------------------------
            # Assign battery residuals, unknowns and results data structures 
            # ------------------------------------------------------------------------------------------------------  
            for b_i , battery in enumerate(batteries):     
                bus_results[battery.tag]                               = RCAIDE.Analyses.Mission.Common.Conditions() 
                bus_results[battery.tag].pack                          = RCAIDE.Analyses.Mission.Common.Conditions() 
                bus_results[battery.tag].cell                          = RCAIDE.Analyses.Mission.Common.Conditions() 
                bus_results[battery.tag].pack.energy                   = 0 * ones_row(1)    
                bus_results[battery.tag].pack.current                  = 0 * ones_row(1)   
                bus_results[battery.tag].pack.voltage_open_circuit     = 0 * ones_row(1)  
                bus_results[battery.tag].pack.voltage_under_load       = 0 * ones_row(1)  
                bus_results[battery.tag].pack.power                    = 0 * ones_row(1)   
                bus_results[battery.tag].pack.temperature              = 0 * ones_row(1)   
                bus_results[battery.tag].pack.heat_energy_generated    = 0 * ones_row(1)   
                bus_results[battery.tag].pack.internal_resistance      = 0 * ones_row(1)   
                bus_results[battery.tag].cell.heat_energy_generated    = 0 * ones_row(1)    
                bus_results[battery.tag].cell.state_of_charge          = 0 * ones_row(1)   
                bus_results[battery.tag].cell.power                    = 0 * ones_row(1)         
                bus_results[battery.tag].cell.energy                   = 0 * ones_row(1)         
                bus_results[battery.tag].cell.voltage_under_load       = 0 * ones_row(1)         
                bus_results[battery.tag].cell.voltage_open_circuit     = 0 * ones_row(1)        
                bus_results[battery.tag].cell.current                  = 0 * ones_row(1)         
                bus_results[battery.tag].cell.temperature              = 0 * ones_row(1)         
                bus_results[battery.tag].cell.charge_throughput        = 0 * ones_row(1)         
                bus_results[battery.tag].cell.depth_of_discharge       = 0 * ones_row(1)
                bus_results[battery.tag].cell.cycle_in_day             = 0
                bus_results[battery.tag].cell.resistance_growth_factor = 1.
                bus_results[battery.tag].cell.capacity_fade_factor     = 1.  
                append_initial_battery_conditions(segment,bus,battery)      
            # ------------------------------------------------------------------------------------------------------
            # Assign network-specific  residuals, unknowns and results data structures
            # ------------------------------------------------------------------------------------------------------
            for propulsor in bus.propulsors:
                if type(segment) == RCAIDE.Analyses.Mission.Segments.Ground.Battery_Recharge: 
                    segment.state.conditions.energy.recharging  = True 
                    segment.state.unknowns['recharge']          =  0* ones_row(1)  
                    segment.state.residuals.network['recharge'] =  0* ones_row(1)
                else:                 
                    segment.state.conditions.energy.recharging  = False 
                    try: 
                        cp_init = estimated_rotor_power_coefficients[bus_i]
                    except: 
                        rotor   = propulsor.rotor  
                        if type(rotor) == Propeller:
                            cp_init  = float(rotor.cruise.design_power_coefficient)
                        elif (type(rotor) == Lift_Rotor) or (type(rotor) == Prop_Rotor):
                            cp_init  = float(rotor.hover.design_power_coefficient)    
                    segment.state.unknowns[ bus.tag  + '_rotor_cp']                    = cp_init * ones_row(1)  
                    segment.state.residuals.network[ bus.tag  + '_rotor_motor_torque'] = 0. * ones_row(1)            
                    
                    # append throttle unknown 
                    if type(segment) != RCAIDE.Analyses.Mission.Segments.Ground.Takeoff or type(segment) == RCAIDE.Analyses.Mission.Segments.Ground.Landing:  
                        try: 
                            initial_throttle = estimated_propulsor_group_throttles[bus_i][0]
                        except:  
                            initial_throttle = 0.5 
                        segment.state.unknowns[bus.tag + '_throttle'] = initial_throttle* ones_row(1)    
             
                # Results data structure for each propulsor group    
                bus_results[propulsor.tag]                         = RCAIDE.Analyses.Mission.Common.Conditions()
                bus_results[propulsor.tag].motor                   = RCAIDE.Analyses.Mission.Common.Conditions()
                bus_results[propulsor.tag].rotor                   = RCAIDE.Analyses.Mission.Common.Conditions() 
                bus_results[propulsor.tag].esc                     = RCAIDE.Analyses.Mission.Common.Conditions()  
                bus_results[propulsor.tag].motor.efficiency        = 0. * ones_row(1)
                bus_results[propulsor.tag].motor.torque            = 0. * ones_row(1) 
                bus_results[propulsor.tag].throttle                = 0. * ones_row(1)
                bus_results[propulsor.tag].rotor.torque            = 0. * ones_row(1)
                bus_results[propulsor.tag].rotor.thrust            = 0. * ones_row(1)
                bus_results[propulsor.tag].rotor.rpm               = 0. * ones_row(1)
                bus_results[propulsor.tag].rotor.disc_loading      = 0. * ones_row(1)                 
                bus_results[propulsor.tag].rotor.power_loading     = 0. * ones_row(1)
                bus_results[propulsor.tag].rotor.tip_mach          = 0. * ones_row(1)
                bus_results[propulsor.tag].rotor.efficiency        = 0. * ones_row(1)   
                bus_results[propulsor.tag].rotor.figure_of_merit   = 0. * ones_row(1) 
                bus_results[propulsor.tag].rotor.power_coefficient = 0. * ones_row(1)  
                noise_results[propulsor.tag]                       = RCAIDE.Analyses.Mission.Common.Conditions()  

        # Ensure the mission knows how to pack and unpack the unknowns and residuals
        segment.process.iterate.unknowns.network                    = self.unpack_unknowns
        segment.process.iterate.residuals.network                   = self.residuals        

        return segment    
            
    __call__ = evaluate_thrust
