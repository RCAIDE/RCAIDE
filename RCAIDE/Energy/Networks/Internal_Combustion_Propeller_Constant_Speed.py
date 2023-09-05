# RCAIDE/Energy/Networks/Internal_Combustion_Propeller_Constant_Speed.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Core                                                       import Data  
from RCAIDE.Components.Component                                       import Container    
from RCAIDE.Methods.Propulsion.internal_combustion_engine_cs_propulsor import compute_propulsor_performance ,compute_unique_propulsor_groups 
from .Network                                                          import Network   
 
# ----------------------------------------------------------------------------------------------------------------------
#  Internal_Combustion_Propeller_Constant_Speed
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Networks
class Internal_Combustion_Propeller_Constant_Speed(Network):
    """ An internal combustion engine with a constant speed propeller.
    
        Assumptions:
        0.5 Throttle corresponds to 0 propeller pitch. Less than 0.5 throttle implies negative propeller pitch.
        
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
        self.engines                      = Container()
        self.propellers                   = Container() 
        self.rated_speed                  = 0.0   
         
    # manage process with a driver function
    def evaluate_thrust(self,state):
        """ Calculate thrust given the current state of the vehicle
    
            Assumptions:
    
            Source:
            N/A
    
            Inputs:
            state [state()]
    
            Outputs:
            results.thrust_force_vector [newtons]
            results.vehicle_mass_rate   [kg/s]
            conditions.energy:
                rpm                     [radians/sec]
                torque                  [N-M]
                power                   [W]
    
            Properties Used:
            Defaulted values
        """           
        # unpack
        conditions   = state.conditions
        engines      = self.engines
        propellers   = self.propellers    
     
        total_mdot   = 0.
        total_thrust = 0. * state.ones_row(3)
        total_power  = 0. 
 
        for i in range(state.conditions.energy[self.tag].number_of_propulsor_groups):
            if self.active_propulsor_groups[i]:           
                pg_tag                 = state.conditions.energy[self.tag].active_propulsor_groups[i]
                N_rotors               = state.conditions.energy[self.tag].N_rotors
                outputs , T , P, mdot  = compute_propulsor_performance(i,self.tag,pg_tag,engines,propellers,N_rotors,state)  
                total_mdot             += mdot
                total_thrust           += T       
                total_power            += P    
                 
        # Create the outputs
        conditions.energy.power = total_power
        
        results = Data()
        results.thrust_force_vector       = total_thrust
        results.vehicle_mass_rate         = mdot  
        
        return results

    __call__ = evaluate_thrust
