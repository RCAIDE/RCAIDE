## @ingroup Networks
# RCAIDE/Energy/Networks/Turboshaft_Engine_Network.py
#
# Created:  Oct 2023, M. Clarke
# Modified: Jun 2024, M. Guidotti 

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE Imports  
import RCAIDE 
from RCAIDE.Framework.Core                                                                        import Data 
from RCAIDE.Framework.Mission.Common                                                              import Residuals    
from RCAIDE.Library.Methods.Propulsors.Turboshaft_Propulsor.compute_turboshaft_performance import compute_turboshaft_performance
from .Network                                                                                     import Network  
                                                                                              
# ----------------------------------------------------------------------------------------------------------------------
#  Turboshaft
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Networks
class Turboshaft_Engine_Network(Network):
    """ This is a turboshaft. 
    
        Assumptions:
        None
        
        Source:
        Most of the componentes come from this book:
        https://soaneemrana.org/onewebmedia/ELEMENTS%20OF%20GAS%20TURBINE%20PROPULTION2.pdf
        
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

        self.tag                          = 'turboshaft_engine'  
        self.system_voltage               = None   
        
    # linking the different network components
    def evaluate_power(self,state):
        """ Calculate power given the current state of the vehicle
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            state [state()]
    
            Outputs:
            results.power               [Watt]
            results.vehicle_mass_rate   [kg/s]
            conditions.noise.sources.turboshaft:
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
        fuel_lines     = self.fuel_lines  
         
        total_power   = 0. * state.ones_row(1) 
        total_mdot    = 0. * state.ones_row(1)   
        
        # Step 2: loop through compoments of network and determine performance
        for fuel_line in fuel_lines:
            if fuel_line.active:   
                
                # Step 2.1: Compute and store perfomrance of all propulsors 
                fuel_line_P = compute_turboshaft_performance(fuel_line,state)    
                total_power  += fuel_line_P  
                
                # Step 2.2: Link each turboshaft the its respective fuel tank(s)
                for fuel_tank in fuel_line.fuel_tanks:
                    mdot = 0. * state.ones_row(1)   
                    for turboshaft in fuel_line.propulsors:
                        for source in (turboshaft.active_fuel_tanks):
                            if fuel_tank.tag == source: 
                                mdot += conditions.energy[fuel_line.tag][turboshaft.tag].fuel_flow_rate 
                        
                    # Step 2.3 : Determine cumulative fuel flow from fuel tank 
                    fuel_tank_mdot = fuel_tank.fuel_selector_ratio*mdot + fuel_tank.secondary_fuel_flow 
                    
                    # Step 2.4: Store mass flow results 
                    conditions.energy[fuel_line.tag][fuel_tank.tag].mass_flow_rate  = fuel_tank_mdot  
                    total_mdot += fuel_tank_mdot                    
                            
        # Step 3: Pack results 
        conditions.energy.power                = total_power 
        conditions.energy.vehicle_mass_rate    = total_mdot     
          
        # A PATCH TO BE DELETED IN RCAIDE
        results = Data()
        results.power                     = total_power
        results.vehicle_mass_rate         = total_mdot     
        # -------------------------------------------------- 
        
        return results 
     
    
    def size(self,state):  
        """ Size the turboshaft
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            State [state()]
    
            Outputs:
            None
    
            Properties Used:
            N/A
        """             
        
        #Unpack components
        conditions = state.conditions
        power     = self.power
        power.size(conditions) 
    
    def unpack_unknowns(self,segment):
        """Unpacks the unknowns set in the mission to be available for the mission.

        Assumptions:
        N/A
        
        Source:
        N/A
        
        Inputs:
        state.unknowns.rpm                   [rpm] 
        state.unknowns.throttle              [-] 
        
        Outputs:
        state.conditions.energy.rotor.rpm    [rpm] 
        state.conditions.energy.throttle     [-] 

        
        Properties Used:
        N/A
        """            
        
        fuel_lines = segment.analyses.energy.networks.turboshaft_engine.fuel_lines
        RCAIDE.Library.Mission.Common.Unpack_Unknowns.energy.fuel_line_unknowns(segment,fuel_lines) 
        
        return    
     
    def add_unknowns_and_residuals_to_segment(self, segment ):
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
        fuel_lines  = segment.analyses.energy.networks.turboshaft_engine.fuel_lines
        ones_row    = segment.state.ones_row 
        segment.state.residuals.network = Residuals()  
         
        for fuel_line_i, fuel_line in enumerate(fuel_lines):    
            # ------------------------------------------------------------------------------------------------------            
            # Create fuel_line results data structure  
            # ------------------------------------------------------------------------------------------------------
            segment.state.conditions.energy[fuel_line.tag]       = RCAIDE.Framework.Mission.Common.Conditions()       
            fuel_line_results                                    = segment.state.conditions.energy[fuel_line.tag]   
            fuel_line_results.throttle                           = 0. * ones_row(1) 
            segment.state.conditions.noise[fuel_line.tag]        = RCAIDE.Framework.Mission.Common.Conditions()  
            noise_results                                        = segment.state.conditions.noise[fuel_line.tag]  
     
            for fuel_tank in fuel_line.fuel_tanks:               
                fuel_line_results[fuel_tank.tag]                 = RCAIDE.Framework.Mission.Common.Conditions()  
                fuel_line_results[fuel_tank.tag].mass_flow_rate  = ones_row(1)  
                fuel_line_results[fuel_tank.tag].mass            = ones_row(1)  
                
            # ------------------------------------------------------------------------------------------------------
            # Assign network-specific  residuals, unknowns and results data structures
            # ------------------------------------------------------------------------------------------------------
            for turboshaft in fuel_line.propulsors:               
                fuel_line_results[turboshaft.tag]                  = RCAIDE.Framework.Mission.Common.Conditions() 
                fuel_line_results[turboshaft.tag].throttle         = 0. * ones_row(1)    
                fuel_line_results[turboshaft.tag].y_axis_rotation  = 0. * ones_row(1)    
                fuel_line_results[turboshaft.tag].power            = 0. * ones_row(1) 
                noise_results[turboshaft.tag]                      = RCAIDE.Framework.Mission.Common.Conditions() 
                noise_results[turboshaft.tag].turboshaft           = RCAIDE.Framework.Mission.Common.Conditions() 
                                                                 
        segment.process.iterate.unknowns.network                   = self.unpack_unknowns                   
        return segment    
        
    __call__ = evaluate_power
