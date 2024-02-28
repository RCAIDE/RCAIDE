## @ingroup Methods-Energy-Propulsors-Converters-Combustor
# RCAIDE/Methods/Energy/Propulsors/Converters/Combustor/compute_combustor_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke  

# ---------------------------------------------------------------------------------------------------------------------- 
# compute_combustor_performance
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Energy-Propulsors-Converters-Combustor  
def compute_combustor_performance(self,conditions):
    """ This computes the output values from the input values according to
    equations from the source.

    Assumptions:
    Constant efficiency and pressure ratio

    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Inputs:
    conditions.freestream.
      isentropic_expansion_factor         [-]
      specific_heat_at_constant_pressure  [J/(kg K)]
      temperature                         [K]
      stagnation_temperature              [K]
    self.inputs.
      stagnation_temperature              [K]
      stagnation_pressure                 [Pa]
      nondim_mass_ratio                   [-]

    Outputs:
    self.outputs.
      stagnation_temperature              [K]  
      stagnation_pressure                 [Pa]
      stagnation_enthalpy                 [J/kg]
      fuel_to_air_ratio                   [-]

    Properties Used:
    self.
      turbine_inlet_temperature           [K]
      pressure_ratio                      [-]
      efficiency                          [-]
      area_ratio                          [-]
      fuel_data.specific_energy           [J/kg]
    """         
    # unpack the values

    # unpacking the values from conditions
    gamma  = conditions.freestream.isentropic_expansion_factor 
    Cp     = conditions.freestream.specific_heat_at_constant_pressure
    To     = conditions.freestream.temperature
    Tto    = conditions.freestream.stagnation_temperature
    
    # unpacking the values form inputs
    Tt_in    = self.inputs.stagnation_temperature
    Pt_in    = self.inputs.stagnation_pressure
    Tt4      = self.turbine_inlet_temperature
    pib      = self.pressure_ratio
    eta_b    = self.efficiency
    nondim_r = self.inputs.nondim_mass_ratio
    
    # unpacking values from self
    htf    = self.fuel_data.specific_energy
    ar     = self.area_ratio
    
    # compute pressure
    Pt_out = Pt_in*pib


    # method to compute combustor properties

    # method - computing the stagnation enthalpies from stagnation temperatures
    ht4     = Cp*Tt4*nondim_r
    ht_in   = Cp*Tt_in*nondim_r
    ho      = Cp*To
    
    # Using the Turbine exit temperature, the fuel properties and freestream temperature to compute the fuel to air ratio f
    f       = (ht4 - ht_in)/(eta_b*htf-ht4)

    # Computing the exit static and stagnation conditions
    ht_out  = Cp*Tt4
    
    # pack computed quantities into outputs
    self.outputs.stagnation_temperature  = Tt4
    self.outputs.stagnation_pressure     = Pt_out
    self.outputs.stagnation_enthalpy     = ht_out
    self.outputs.fuel_to_air_ratio       = f 
