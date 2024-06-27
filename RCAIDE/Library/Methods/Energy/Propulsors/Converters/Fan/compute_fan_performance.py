## @ingroup Methods-Energy-Propulsors-Converters-Fan
# RCAIDE/Library/Methods/Energy/Propulsors/Converters/Fan/compute_fan_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke    

# ----------------------------------------------------------------------------------------------------------------------
#  Fan 
# ----------------------------------------------------------------------------------------------------------------------           
## @ingroup Methods-Energy-Propulsors-Converters-Fan
def compute_fan_performance(fan,conditions):
    """ This computes the output values from the input values according to
    equations from the source.

    Assumptions:
    Constant polytropic efficiency and pressure ratio

    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Args:
    conditions.freestream.
      isentropic_expansion_factor         [-]
      specific_heat_at_constant_pressure  [J/(kg K)]
    fan.inputs.
      stagnation_temperature              [K]
      stagnation_pressure                 [Pa]

    fan.
      pressure_ratio                      [-]
      polytropic_efficiency               [-]
      
    Returns:
    fan.outputs.
      stagnation_temperature              [K]  
      stagnation_pressure                 [Pa]
      stagnation_enthalpy                 [J/kg]
      work_done                           [J/kg]
 
    """        
    
    #unpack from conditions
    gamma     = conditions.freestream.isentropic_expansion_factor
    Cp        = conditions.freestream.specific_heat_at_constant_pressure
    
    #unpack from inputs
    Tt_in     = fan.inputs.stagnation_temperature
    Pt_in     = fan.inputs.stagnation_pressure
    
    #unpack from fan
    pid       = fan.pressure_ratio
    etapold   = fan.polytropic_efficiency
    
    #method to compute the fan properties
    
    #Compute the output stagnation quantities 
    ht_in     = Cp*Tt_in
    
    Pt_out    = Pt_in*pid
    Tt_out    = Tt_in*pid**((gamma-1)/(gamma*etapold))
    ht_out    = Cp*Tt_out    
    
    #computing the wok done by the fan (for matching with turbine)
    work_done = ht_out- ht_in
    
    #pack the computed quantities into outputs
    fan.outputs.stagnation_temperature  = Tt_out
    fan.outputs.stagnation_pressure     = Pt_out
    fan.outputs.stagnation_enthalpy     = ht_out
    fan.outputs.work_done               = work_done   
    
    return 