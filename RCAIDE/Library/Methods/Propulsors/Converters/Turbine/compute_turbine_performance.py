# RCAIDE/Library/Methods/Propulsors/Converters/Turbine/compute_turbine_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke    

# ----------------------------------------------------------------------------------------------------------------------
#  compute_turbine_performance
# ----------------------------------------------------------------------------------------------------------------------     
def compute_turbine_performance(turbine,turbine_conditions,conditions):
    """This computes the output values from the input values according to
    equations from the source. The following properties are computed: 
    turbine.outputs.
      stagnation_temperature   (numpy.ndarray): exiting stagnation_temperature [K]  
      stagnation_pressure      (numpy.ndarray): exiting stagnation_pressure    [Pa]
      stagnation_enthalpy      (numpy.ndarray): exiting stagnation_enthalpy    [J/kg]

    Assumptions:
    Constant polytropic efficiency and pressure ratio

    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Args:
        conditions.freestream.
          isentropic_expansion_factor             (numpy.ndarray): isentropic_expansion_factor         [unitless]
          specific_heat_at_constant_pressure      (numpy.ndarray): specific_heat_at_constant_pressure  [J/(kg K)]
        turbine
          .inputs.stagnation_temperature          (numpy.ndarray): entering stagnation_temperature     [K]
          .inputs.stagnation_pressure             (numpy.ndarray): entering stagnation_pressure        [Pa]
          .inputs.bypass_ratio                    (numpy.ndarray): bypass_ratio                        [unitless]
          .inputs.fuel_to_air_ratio               (numpy.ndarray): fuel-to-air ratio                   [unitless]
          .inputs.compressor.work_done            (numpy.ndarray): compressor work                     [J/(kg/s)]
          .inputs.fan.work_done                   (numpy.ndarray): fan work done                       [J/(kg/s)]
          .inputs.shaft_power_off_take.work_done  (numpy.ndarray): shaft power off take                [J/(kg/s)] 
          .mechanical_efficiency                          (float): mechanical efficiency               [unitless]
          .polytropic_efficiency                          (float): polytropic efficiency               [unitless]

    Returns:
        None 
    """            
    # Unpack flight conditions 
    gamma           = conditions.freestream.isentropic_expansion_factor
    Cp              = conditions.freestream.specific_heat_at_constant_pressure
    
    #Unpack turbine entering properties 
    eta_mech        = turbine.mechanical_efficiency
    etapolt         = turbine.polytropic_efficiency
    alpha           = turbine_conditions.inputs.bypass_ratio
    Tt_in           = turbine_conditions.inputs.stagnation_temperature
    Pt_in           = turbine_conditions.inputs.stagnation_pressure
    compressor_work = turbine_conditions.inputs.compressor.work_done
    fan_work        = turbine_conditions.inputs.fan.work_done
    f               = turbine_conditions.inputs.fuel_to_air_ratio 
    shaft_takeoff   = turbine_conditions.inputs.shaft_power_off_take.work_done 
  
    # Using the work done by the compressors/fan and the fuel to air ratio to compute the energy drop across the turbine
    deltah_ht = -1/(1+f) * (compressor_work + shaft_takeoff + alpha * fan_work) * 1/eta_mech
    
    # Compute the output stagnation quantities from the inputs and the energy drop computed above
    Tt_out    =  Tt_in+deltah_ht/Cp
    ht_out    =  Cp*Tt_out   
    Pt_out    =  Pt_in*(Tt_out/Tt_in)**(gamma/((gamma-1)*etapolt))
    
    # Pack outputs of turbine 
    turbine_conditions.outputs.stagnation_pressure     = Pt_out
    turbine_conditions.outputs.stagnation_temperature  = Tt_out
    turbine_conditions.outputs.stagnation_enthalpy     = ht_out
    
    return