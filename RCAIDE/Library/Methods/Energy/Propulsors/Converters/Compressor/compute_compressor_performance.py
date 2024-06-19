## @ingroup Library-Methods-Energy-Propulsors-Converters-Compressor
# RCAIDE/Library/Methods/Energy/Propulsors/Converters/Compressor/compute_compressor_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke     

# ---------------------------------------------------------------------------------------------------------------------- 
# compute_compression_nozzle_performance
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Components-Propulsors-Converters-Compressor
def compute_compressor_performance(compressor,conditions):
    """ This computes the output values from the input values according to
    equations from the source.

    Assumptions:
    Constant polytropic efficiency and pressure ratio

    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Inputs:
    conditions.freestream.
      isentropic_expansion_factor         [-]
      specific_heat_at_constant_pressure  [J/(kg K)]
    compressor.inputs.
      stagnation_temperature              [K]
      stagnation_pressure                 [Pa]

    Outputs:
    compressor.outputs.
      stagnation_temperature              [K]  
      stagnation_pressure                 [Pa]
      stagnation_enthalpy                 [J/kg]
      work_done                           [J/kg]

    Properties Used:
    compressor.
      pressure_ratio                      [-]
      polytropic_efficiency               [-]
    """          
    #unpack the values
    
    #unpack from conditions
    gamma    = conditions.freestream.isentropic_expansion_factor
    Cp       = conditions.freestream.specific_heat_at_constant_pressure
    
    #unpack from inputs
    Tt_in    = compressor.inputs.stagnation_temperature
    Pt_in    = compressor.inputs.stagnation_pressure
    
    #unpack from compressor
    pid      = compressor.pressure_ratio
    etapold  = compressor.polytropic_efficiency
    
    #Method to compute compressor properties
    
    #Compute the output stagnation quantities based on the pressure ratio of the component
    ht_in     = Cp*Tt_in
    Pt_out    = Pt_in*pid
    Tt_out    = Tt_in*pid**((gamma-1)/(gamma*etapold))
    ht_out    = Cp*Tt_out
    
    #compute the work done by the compressor(for matching with the turbine)
    work_done = ht_out- ht_in
    
    #pack computed quantities into the outputs
    compressor.outputs.stagnation_temperature  = Tt_out
    compressor.outputs.stagnation_pressure     = Pt_out
    compressor.outputs.stagnation_enthalpy     = ht_out
    compressor.outputs.work_done               = work_done
    
    return 

