# RCAIDE/Methods/Missions/Segments/Ground/Battery_Charge_or_Discharge.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------  
#  IMPORT 
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports 
import RCAIDE

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Methods-Missions-Segments-Ground
def unpack_unknowns(segment):  
    pass

# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Missions-Segments-Ground 
def initialize_conditions(segment): 
    overcharge_contingency = segment.overcharge_contingency  
    
    # unpack   
    if segment.state.initials: 
        intial_segment_energy     = []
        segment_maximum_energy    = []  
        for b_i in range(segment.state.initials.conditions.energy.number_of_batteries):
            bat = segment.state.initials.conditions.energy['battery_' + str(b_i)] 
            intial_segment_energy.append(bat.pack.energy[-1,0])
            segment_maximum_energy.append(bat.pack.maximum_degraded_battery_energy)
    elif 'initial_battery_state_of_charge' in segment: 
        intial_segment_energy  = segment.initial_battery_state_of_charge  
        segment_maximum_energy = segment.initial_battery_state_of_charge
    
    duration  = segment.time  
    if type(segment) ==  RCAIDE.Analyses.Mission.Segments.Ground.Battery_Recharge: 
        for network in segment.analyses.energy.networks:   
            batteries      = network.batteries 
            for b_i in range(len(batteries)): 
                battery_key    = list(batteries.keys())[b_i] 
                battery        = batteries[battery_key]  
                charge_current = battery.cell.charging_current * battery.pack.electrical_configuration.parallel
                charge_voltage = battery.cell.charging_voltage * battery.pack.electrical_configuration.series
                delta_energy   = segment_maximum_energy[b_i] - intial_segment_energy[b_i]
                duration       = np.maximum(duration,delta_energy*overcharge_contingency/(charge_current*charge_voltage)) 
        
    t_nondim   = segment.state.numerics.dimensionless.control_points
    conditions = segment.state.conditions   
    
    # dimensionalize time
    t_initial = conditions.frames.inertial.time[0,0]
    t_nondim  = segment.state.numerics.dimensionless.control_points
    time      =  t_nondim * (duration) + t_initial
    
    segment.state.conditions.frames.inertial.time[:,0] = time[:,0] 

