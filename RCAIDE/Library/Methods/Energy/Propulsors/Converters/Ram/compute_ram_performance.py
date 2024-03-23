## @ingroup Methods-Energy-Propulsors-Converters-Ram
# RCAIDE/Library/Methods/Energy/Propulsors/Converters/Ram/compute_ram_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke    

# ----------------------------------------------------------------------------------------------------------------------
# compute_ram_performance
# ----------------------------------------------------------------------------------------------------------------------           
## @ingroup Methods-Energy-Propulsors-Converters-Ram 
def compute_ram_performance(ram,conditions):
    """ This computes the output values from the input values according to
    equations from the source.

    Assumptions:
    None

    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Inputs:
    conditions.freestream.
      pressure
      temperature
      mach_number
    ram.inputs.working_fluid

    Outputs:
    ram.outputs.
      stagnation_temperature              [K]
      stagnation_pressure                 [Pa]
      isentropic_expansion_factor         [-]
      specific_heat_at_constant_pressure  [J/(kg K)]
      gas_specific_constant               [J/(kg K)]
    conditions.freestream.
      stagnation_temperature              [K]
      stagnation_pressure                 [Pa]
      isentropic_expansion_factor         [-]
      specific_heat_at_constant_pressure  [J/(kg K)]
      gas_specific_constant               [J/(kg K)]
      speed_of_sound                      [m/s]

    Properties Used:
    None
    """
    #unpack from conditions
    Po = conditions.freestream.pressure
    To = conditions.freestream.temperature
    M  = conditions.freestream.mach_number

    #unpack from inputs
    working_fluid          = ram.inputs.working_fluid

    #method to compute the ram properties

    #computing the working fluid properties
    gamma                  = working_fluid.compute_gamma(To,Po) 
    Cp                     = working_fluid.compute_cp(To,Po)
    R                      = working_fluid.gas_specific_constant

    #Compute the stagnation quantities from the input static quantities
    stagnation_temperature = To*(1.+((gamma-1.)/2.*M*M))
    stagnation_pressure    = Po*((1.+(gamma-1.)/2.*M*M )**(gamma/(gamma-1.)))

    #pack computed outputs
    #pack the values into conditions
    ram.outputs.stagnation_temperature              = stagnation_temperature
    ram.outputs.stagnation_pressure                 = stagnation_pressure
    ram.outputs.isentropic_expansion_factor         = gamma
    ram.outputs.specific_heat_at_constant_pressure  = Cp
    ram.outputs.gas_specific_constant               = R

    #pack the values into outputs
    conditions.freestream.stagnation_temperature               = stagnation_temperature
    conditions.freestream.stagnation_pressure                  = stagnation_pressure
    conditions.freestream.isentropic_expansion_factor          = gamma
    conditions.freestream.specific_heat_at_constant_pressure   = Cp
    conditions.freestream.gas_specific_constant                = R
    
    return 


def _compute_ram_performance(State, Settings, System):
	'''
	Framework version of compute_ram_performance.
	Wraps compute_ram_performance with State, Settings, System pack/unpack.
	Please see compute_ram_performance documentation for more details.
	'''

	#TODO: ram        = [Replace With State, Settings, or System Attribute]
	#TODO: conditions = [Replace With State, Settings, or System Attribute]

	results = compute_ram_performance('ram', 'conditions')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System