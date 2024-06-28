## @ingroup Methods-Energy-Propulsors-Converters-Ram
# RCAIDE/Library/Methods/Energy/Propulsors/Converters/Ram/compute_ram_performance.py
# 
# 
# Created:  Jun 2024, M. Clarke    

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

    Args:
    conditions.freestream.
      pressure
      temperature
      mach_number
    ram.inputs.working_fluid

    Returns:
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
    """
    # Unpack flight conditions 
    Po = conditions.freestream.pressure
    To = conditions.freestream.temperature
    M  = conditions.freestream.mach_number

    #Unpack component inputs
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