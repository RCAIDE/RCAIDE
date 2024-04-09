## @ingroup Methods-Center_of_Gravity
# compute_mission_center_of_gravity.py
#
# Created:  Nov 2015, M. Vegh
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#  Computer Mission Center of Gravity
# ----------------------------------------------------------------------

## @ingroup Methods-Center_of_Gravity
def func_compute_mission_center_of_gravity(vehicle, mission_fuel_weight):
    """ computes the CG for the vehicle based on the mzfw cg of the
    vehicle, and an assigned fuel

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    vehicle 
    mission_fuel_weight           [Newtons]

    Outputs:
    cg                            [meters]

    Properties Used:
    N/A
    """  

    mzf_cg     = vehicle.mass_properties.zero_fuel_center_of_gravity
    mzf_weight = vehicle.mass_properties.max_zero_fuel
    fuel       = vehicle.fuel
    fuel_cg    = vehicle.fuel.mass_properties.center_of_gravity
    
    cg         =((mzf_cg)*mzf_weight+(fuel_cg+fuel.origin)*mission_fuel_weight)/(mission_fuel_weight+mzf_weight)
   
    return cg



def compute_mission_center_of_gravity(State, Settings, System):
	#TODO: vehicle             = [Replace With State, Settings, or System Attribute]
	#TODO: mission_fuel_weight = [Replace With State, Settings, or System Attribute]

	results = func_compute_mission_center_of_gravity('vehicle', 'mission_fuel_weight')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System