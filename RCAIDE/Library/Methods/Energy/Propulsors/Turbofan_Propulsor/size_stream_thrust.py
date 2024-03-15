## @ingroup Methods-Energy-Propulsors-Turbofan_Propulsor
# RCAIDE/Library/Methods/Energy/Propulsors/Turbofan_Propulsor/compute_thrust.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#   size_stream_thrust
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Energy-Propulsors-Turbofan_Propulsor
def size_stream_thrust(turbofan,conditions): 
    """Sizes the core flow for the design condition. 

       Assumptions: 
       Perfect gas 

       Source: 
       Heiser, William H., Pratt, D. T., Daley, D. H., and Unmeel, B. M., 
       "Hypersonic Airbreathing Propulsors", 1994 
       Chapter 4 - pgs. 175-180
       
       Inputs: 
       conditions.freestream.speed_of_sound [m/s]  
       turbofan.inputs. 
          bypass_ratio                       [-] 
          total_temperature_reference        [K] 
          total_pressure_reference           [Pa] 
          number_of_engines                  [-] 

        Outputs: 
          turbofan.outputs.non_dimensional_thrust  [-] 

        Properties Used: 
        turbofan. 
           reference_temperature              [K] 
           reference_pressure                 [Pa] 
           total_design                       [N] - Design thrust 
           """              

    # Unpack Inputs
    
    # Unpack Conditions
    a0                      = conditions.freestream.speed_of_sound 
    throttle                = 1.0 
    
    # Unpack from turbofan 
    Tref                        = turbofan.reference_temperature 
    Pref                        = turbofan.reference_pressure  
    
    # Unpack from Inputs
    total_temperature_reference = turbofan.inputs.total_temperature_reference  # low pressure turbine output for turbofan 
    total_pressure_reference    = turbofan.inputs.total_pressure_reference 
    no_eng                      = turbofan.inputs.number_of_engines 
    
    #compute nondimensional thrust 
    turbofan.compute_stream_thrust(conditions) 
    
    #unpack results  
    Fsp                         = turbofan.outputs.non_dimensional_thrust 
    
    #compute dimensional mass flow rates 
    mdot_core                   = turbofan.design_thrust/(Fsp*a0*no_eng*throttle)   
    mdhc                        = mdot_core/ (np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref)) 
    
    #pack outputs 
    turbofan.mass_flow_rate_design               = mdot_core 
    turbofan.compressor_nondimensional_massflow  = mdhc 
    
    return        



def _size_stream_thrust(State, Settings, System):
	'''
	Framework version of size_stream_thrust.
	Wraps size_stream_thrust with State, Settings, System pack/unpack.
	Please see size_stream_thrust documentation for more details.
	'''

	#TODO: turbofan   = [Replace With State, Settings, or System Attribute]
	#TODO: conditions = [Replace With State, Settings, or System Attribute]

	results = size_stream_thrust('turbofan', 'conditions')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System