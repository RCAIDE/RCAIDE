# RCAIDE/Library/Missions/Common/Pre_Process/use_previous_segment_pre_processed_data.py
#  
# Created:  Jan 2026, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
import RCAIDE

# python imports
from copy import deepcopy 

# ----------------------------------------------------------------------------------------------------------------------
#  use_previous_segment_pre_processed_data
# ---------------------------------------------------------------------------------------------------------------------- 
def use_previous_segment_pre_processed_data(mission,segment,i):
    '''
    Reuses previous segment pre processed data to save computational time.
    Ensures that changes in configuration are not overwritten.    
    '''
    vehicle_0 = deepcopy(segment.analyses.vehicle)
    segment.analyses.vehicle = deepcopy(mission.segments[i-1].analyses.vehicle)
    for wing in segment.analyses.vehicle.wings:
        for control_surface in wing.control_surfaces:
            control_surface.deflection = vehicle_0.wings[wing.tag].control_surfaces[control_surface.tag].deflection
    for landing_gear in segment.analyses.vehicle.landing_gears:
        landing_gear.gear_extended = vehicle_0.landing_gears[landing_gear.tag].gear_extended
    
    for network in segment.analyses.vehicle.networks: 
        for bus in network.busses:
            bus.active = vehicle_0.networks[network.tag].busses[bus.tag].active
        for propulsor in network.propulsors:
            if isinstance(propulsor, RCAIDE.Library.Components.Powertrain.Propulsors.Turbofan):
                propulsor_0 =  vehicle_0.networks[network.tag].propulsors[propulsor.tag]
                propulsor.fan.angular_velocity        = propulsor_0.fan.angular_velocity        
                propulsor.fan_nozzle.exit_velocity    = propulsor_0.fan_nozzle.exit_velocity 
                propulsor.core_nozzle.exit_velocity   = propulsor_0.core_nozzle.exit_velocity
                
            if isinstance(propulsor, RCAIDE.Library.Components.Powertrain.Propulsors.Electric_Rotor):
                propulsor_0 =  vehicle_0.networks[network.tag].propulsors[propulsor.tag]
                propulsor.rotor.orientation_euler_angles =  propulsor_0.rotor.orientation_euler_angles 
                propulsor.rotor.blade_pitch_command      =  propulsor_0.rotor.blade_pitch_command
    return