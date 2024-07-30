## @ingroup Components-Propulsors-Converters
# RCAIDE/Library/Components/Propulsors/Converters/Fan.py
# 
# 
# 
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
    # RCAIDE imports
import RCAIDE 
from RCAIDE.Framework.Core      import Data, Units
from RCAIDE.Framework.Core                                                                     import Data 
from RCAIDE.Framework.Mission.Common                                                           import Residuals    
from RCAIDE.Library.Methods.Propulsors.Turbofan_Propulsor.compute_turbofan_performance         import compute_turbofan_performance
from . import Propulsor

import numpy as np 

# ----------------------------------------------------------------------
#  Fan Component
# ----------------------------------------------------------------------
## @ingroup Components-Propulsors-Converters
class Turbofan(Propulsor):
    """This is a turbofan propulsor.

    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):    
        # setting the default values
        self.tag                                      = 'Turbofan'
        self.engine_type                              = 'Turbofan'
        self.nacelle                                  = None 
        self.fan                                      = None 
        self.ram                                      = None 
        self.inlet_nozzle                             = None 
        self.low_pressure_compressor                  = None 
        self.high_pressure_compressor                 = None 
        self.low_pressure_turbine                     = None 
        self.high_pressure_turbine                    = None 
        self.combustor                                = None 
        self.core_nozzle                              = None 
        self.fan_nozzle                               = None  
        self.active_fuel_tanks                        = None         
        self.engine_length                            = 0.0
        self.engine_height                            = 0.5     # Engine centerline heigh above the ground plane
        self.exa                                      = 1       # distance from fan face to fan exit/ fan diameter)
        self.plug_diameter                            = 0.1     # dimater of the engine plug
        self.geometry_xe                              = 1.      # Geometry information for the installation effects function
        self.geometry_ye                              = 1.      # Geometry information for the installation effects function
        self.geometry_Ce                              = 2.      # Geometry information for the installation effects function
        self.bypass_ratio                             = 0.0 
        self.design_isa_deviation                     = 0.0
        self.design_altitude                          = 0.0
        self.SFC_adjustment                           = 0.0 # Less than 1 is a reduction
        self.compressor_nondimensional_massflow       = 0.0
        self.reference_temperature                    = 288.15
        self.reference_pressure                       = 1.01325*10**5 
        self.design_thrust                            = 0.0
        self.mass_flow_rate_design                    = 0.0
        self.OpenVSP_flow_through                     = False

        #areas needed for drag; not in there yet
        self.areas                                    = Data()
        self.areas.wetted                             = 0.0
        self.areas.maximum                            = 0.0
        self.areas.exit                               = 0.0
        self.areas.inflow                             = 0.0

        self.inputs                                   = Data()
        self.outputs                                  = Data()

        self.inputs.fuel_to_air_ratio                 = 0.0
        self.outputs.thrust                           = 0.0 
        self.outputs.thrust_specific_fuel_consumption = 0.0
        self.outputs.specific_impulse                 = 0.0
        self.outputs.non_dimensional_thrust           = 0.0
        self.outputs.core_mass_flow_rate              = 0.0
        self.outputs.fuel_flow_rate                   = 0.0
        self.outputs.fuel_mass                        = 0.0
        self.outputs.power                            = 0.0

        self.reverse_thrust                           = False
        self.active                                   = True

    #def unpack_unknowns(self,segment,fuel_line, turbofan):
            #"""Unpacks the unknowns set in the mission to be available for the mission.

            #Assumptions:
            #N/A

            #Source:
            #N/A

            #Inputs: 
                #segment   - data structure of mission segment [-]

            #Outputs: 

            #Properties Used:
            #N/A
            #"""            


            #RCAIDE.Library.Mission.Common.Unpack_Unknowns.energy.fuel_line_unknowns(segment,fuel_line, turbofan) 

            #return            

    def add_unknowns_and_residuals_to_segment(self, segment, fuel_line, turbofan, first_propulsor):
        """ This function sets up the information that the mission needs to run a mission segment using this network 

            Assumptions:
            None

            Source:
            N/A

            Inputs:
            segment
            eestimated_throttles           [-]
            estimated_propulsor_group_rpms [-]  

            Outputs:
            segment

            Properties Used:
            N/A
        """


        ones_row    = segment.state.ones_row 
        segment.state.residuals.network = Residuals()  


        # ------------------------------------------------------------------------------------------------------            
        # Create fuel_line results data structure  
        # ------------------------------------------------------------------------------------------------------
        if first_propulsor ==  True:
            segment.state.conditions.energy.distribution_lines[fuel_line.tag]                  = RCAIDE.Framework.Mission.Common.Conditions()
            segment.state.conditions.energy.distribution_lines[fuel_line.tag].propulsors       = RCAIDE.Framework.Mission.Common.Conditions()       
            fuel_line_results                                                                    = segment.state.conditions.energy.distribution_lines[fuel_line.tag].propulsors    
            segment.state.conditions.noise.distribution_lines[fuel_line.tag]                    = RCAIDE.Framework.Mission.Common.Conditions()
            segment.state.conditions.noise.distribution_lines[fuel_line.tag].propulsors         = RCAIDE.Framework.Mission.Common.Conditions()  
            noise_results                                                                      = segment.state.conditions.noise.distribution_lines[fuel_line.tag].propulsors
        else:
            fuel_line_results                                    = segment.state.conditions.energy.distribution_lines[fuel_line.tag].propulsors
            noise_results                                        = segment.state.conditions.noise.distribution_lines[fuel_line.tag].propulsors



        # ------------------------------------------------------------------------------------------------------
        # Assign network-specific  residuals, unknowns and results data structures
        # ------------------------------------------------------------------------------------------------------

        fuel_line_results[turbofan.tag]                         = RCAIDE.Framework.Mission.Common.Conditions() 
        fuel_line_results[turbofan.tag].throttle                = 0. * ones_row(1)      
        fuel_line_results[turbofan.tag].y_axis_rotation         = 0. * ones_row(1)  
        fuel_line_results[turbofan.tag].thrust                  = 0. * ones_row(1) 
        fuel_line_results[turbofan.tag].power                   = 0. * ones_row(1) 
        noise_results[turbofan.tag]                             = RCAIDE.Framework.Mission.Common.Conditions() 
        noise_results[turbofan.tag].turbofan                    = RCAIDE.Framework.Mission.Common.Conditions() 

        #segment.process.iterate.unknowns.network   = self.unpack_unknowns(segment,fuel_line, turbofan)                   
        return segment


    def evaluate_thrust(self,state, network):
        """ Calculate thrust given the current state of the vehicle

            Assumptions:
            None

            Source:
            N/A

            Inputs:
            state [state()]

            Outputs:
            results.thrust_force_vector [newtons]
            results.vehicle_mass_rate   [kg/s]
            conditions.noise.sources.turbofan:
                core:
                    exit_static_temperature      
                    exit_static_pressure       
                    exit_stagnation_temperature 
                    exit_stagnation_pressure
                    exit_velocity 
                fan:
                    exit_static_temperature      
                    exit_static_pressure       
                    exit_stagnation_temperature 
                    exit_stagnation_pressure
                    exit_velocity 

            Properties Used:
            Defaulted values
        """           

        # Step 1: Unpack
        conditions     = state.conditions  
        fuel_lines     = network.distribution_lines
        reverse_thrust = self.reverse_thrust
        total_thrust   = 0. * state.ones_row(3) 
        total_power    = 0. * state.ones_row(1) 
        total_mdot     = 0. * state.ones_row(1)   

        # Step 2: loop through compoments of network and determine performance
        for fuel_line in fuel_lines:
            #if fuel_line.active:   

            # Step 2.1: Compute and store perfomrance of all propulsors 
            fuel_line_T,fuel_line_P = compute_turbofan_performance(fuel_line,state)  
            total_thrust += fuel_line_T   
            total_power  += fuel_line_P  

            # Step 2.2: Link each turbofan the its respective fuel tank(s)
            for fuel_tank in fuel_line.fuel_tanks:
                mdot = 0. * state.ones_row(1)   
                for turbofan in fuel_line.propulsors:
                    for source in (turbofan.active_fuel_tanks):
                        if fuel_tank.tag == source: 
                            mdot += conditions.energy.distribution_lines[fuel_line.tag].propulsors[turbofan.tag].fuel_flow_rate 

                # Step 2.3 : Determine cumulative fuel flow from fuel tank 
                fuel_tank_mdot = fuel_tank.fuel_selector_ratio*mdot + fuel_tank.secondary_fuel_flow 

                # Step 2.4: Store mass flow results 
                conditions.energy.distribution_lines[fuel_line.tag][fuel_tank.tag].mass_flow_rate  = fuel_tank_mdot  
                total_mdot += fuel_tank_mdot                    

        # Step 3: Pack results
        if reverse_thrust ==  True:
            total_thrust =  total_thrust * -1

        conditions.energy.thrust_force_vector  = total_thrust
        conditions.energy.power                = total_power 
        conditions.energy.vehicle_mass_rate    = total_mdot           

        # A PATCH TO BE DELETED IN RCAIDE
        results = Data()
        results.thrust_force_vector       = total_thrust
        results.power                     = total_power
        results.vehicle_mass_rate         = total_mdot     
        # -------------------------------------------------- 

        return results     