## @ingroup Library-Methods-Mission-Common-Update
# RCAIDE/Library/Methods/Missions/Common/Update/battery_age.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Battery Age
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Mission-Common-Update
def battery_age(segment):  
    """Updates battery age based on operating conditions, cell temperature and time of operation.
       Source: 
       Cell specific. See individual battery cell for more details

       Assumptions:
       Cell specific. See individual battery cell for more details

       Inputs: 
       segment.
           conditions                         - conditions of battery at each segment  [unitless]
           increment_battery_age_by_one_day   - flag to increment battery cycle day    [boolean]

       Outputs:
       N/A  

       Properties Used:
       N/A 
    """  
    # loop throuh networks in vehicle 
    for network in segment.analyses.energy.networks: 
        if 'busses' in network: 
            busses  = network.busses
            for bus in busses:
                for battery in bus.batteries: 
                    increment_day = segment.increment_battery_age_by_one_day
                    battery_conditions  = segment.conditions.energy[bus.tag][battery.tag] 
                    battery.update_battery_age(battery_conditions,increment_battery_age_by_one_day = increment_day) 


def _battery_age(State, Settings, System):
	'''
	Framework version of battery_age.
	Wraps battery_age with State, Settings, System pack/unpack.
	Please see battery_age documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = battery_age('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System