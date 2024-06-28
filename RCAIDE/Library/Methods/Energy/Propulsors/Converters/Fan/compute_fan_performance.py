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
    equations from the source. The following outputs are computed: 
    fan.outputs.
      stagnation_temperature  (numpy.ndarray): exit stagnation_temperature  [K]  
      stagnation_pressure     (numpy.ndarray): exit stagnation_pressure     [Pa]
      stagnation_enthalpy     (numpy.ndarray): exit stagnation_enthalpy     [J/kg]
      work_done               (numpy.ndarray): work_done                    [J/(kg-s)]
 

    Assumptions:
        Constant polytropic efficiency and pressure ratio

    Source:
        https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Args:
        conditions.freestream.
          isentropic_expansion_factor         (numpy.ndarray): isentropic_expansion_factor         [unitless]
          specific_heat_at_constant_pressure  (numpy.ndarray): specific_heat_at_constant_pressure  [J/(kg K)]
        fan
          .inputs.stagnation_temperature      (numpy.ndarray): entering stagnation temperature [K]
          .inputs.stagnation_pressure         (numpy.ndarray): entering stagnation pressure    [Pa] 
          .pressure_ratio                             (float): pressure ratio of fan           [unitless]
          .polytropic_efficiency                      (float): polytropic_efficiency           [unitless]
      
    Returns:
        None
        
    """        
    
    # Unpack flight conditions 
    gamma     = conditions.freestream.isentropic_expansion_factor
    Cp        = conditions.freestream.specific_heat_at_constant_pressure
     
    # unpack from fan
    PR        = fan.pressure_ratio
    etapold   = fan.polytropic_efficiency
    Tt_in     = fan.inputs.stagnation_temperature
    Pt_in     = fan.inputs.stagnation_pressure
     
    
    # Compute the output quantities  
    Pt_out    = Pt_in*PR
    Tt_out    = Tt_in*PR**((gamma-1)/(gamma*etapold))
    ht_out    = Tt_out*Cp   
    ht_in     = Tt_in*Cp
    
    # Compute the work done by the fan (normalized by mass flow i.e. J/(kg/s)
    work_done = ht_out - ht_in
    
    # Store computed quantities into outputs
    fan.outputs.stagnation_temperature  = Tt_out
    fan.outputs.stagnation_pressure     = Pt_out
    fan.outputs.work_done               = work_done
    fan.outputs.stagnation_enthalpy     = ht_out
    
    return 