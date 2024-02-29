## @ingroup Methods-Energy-Propulsors-Converters-Turbine
# RCAIDE/Methods/Energy/Propulsors/Converters/Turbine/compute_turbine_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke    

# ----------------------------------------------------------------------------------------------------------------------
#  compute_turbine_performance
# ----------------------------------------------------------------------------------------------------------------------           
## @ingroup Methods-Energy-Propulsors-Converters-Turbine 
def compute_turbine_performance(turbine,conditions):
    """This computes the output values from the input values according to
    equations from the source.

    Assumptions:
    Constant polytropic efficiency and pressure ratio

    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Inputs:
    conditions.freestream.
      isentropic_expansion_factor         [-]
      specific_heat_at_constant_pressure  [J/(kg K)]
    turbine.inputs.
      stagnation_temperature              [K]
      stagnation_pressure                 [Pa]
      bypass_ratio                        [-]
      fuel_to_air_ratio                   [-]
      compressor.work_done                [J/kg]
      fan.work_done                       [J/kg]
      shaft_power_off_take.work_done      [J/kg]

    Outputs:
    turbine.outputs.
      stagnation_temperature              [K]  
      stagnation_pressure                 [Pa]
      stagnation_enthalpy                 [J/kg]

    Properties Used:
    turbine.
      mechanical_efficiency               [-]
      polytropic_efficiency               [-]
    """           
    #unpack the values
    
    #unpack from conditions
    gamma           = conditions.freestream.isentropic_expansion_factor
    Cp              = conditions.freestream.specific_heat_at_constant_pressure
    
    #unpack from inputs
    Tt_in           = turbine.inputs.stagnation_temperature
    Pt_in           = turbine.inputs.stagnation_pressure
    alpha           = turbine.inputs.bypass_ratio
    f               = turbine.inputs.fuel_to_air_ratio
    compressor_work = turbine.inputs.compressor.work_done
    fan_work        = turbine.inputs.fan.work_done

    if turbine.inputs.shaft_power_off_take is not None:
        shaft_takeoff = turbine.inputs.shaft_power_off_take.work_done
    else:
        shaft_takeoff = 0.

    #unpack from turbine
    eta_mech        =  turbine.mechanical_efficiency
    etapolt         =  turbine.polytropic_efficiency
    
    #method to compute turbine properties
    
    #Using the work done by the compressors/fan and the fuel to air ratio to compute the energy drop across the turbine
    deltah_ht = -1 / (1 + f) * 1 / eta_mech * (compressor_work + shaft_takeoff + alpha * fan_work)
    
    #Compute the output stagnation quantities from the inputs and the energy drop computed above
    Tt_out    =  Tt_in+deltah_ht/Cp
    Pt_out    =  Pt_in*(Tt_out/Tt_in)**(gamma/((gamma-1)*etapolt))
    ht_out    =  Cp*Tt_out   #h(Tt4_5)
    
    
    #pack the computed values into outputs
    turbine.outputs.stagnation_temperature  = Tt_out
    turbine.outputs.stagnation_pressure     = Pt_out
    turbine.outputs.stagnation_enthalpy     = ht_out 