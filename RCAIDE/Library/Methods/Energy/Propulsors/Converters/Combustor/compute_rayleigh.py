## @ingroup Methods-Energy-Propulsors-Converters-Combustor
# RCAIDE/Library/Methods/Energy/Propulsors/Converters/Combustor/compute_rayleigh.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------     

# package imports
import numpy as np 
from Legacy.trunk.S.Methods.Propulsion.rayleigh import rayleigh
from Legacy.trunk.S.Methods.Propulsion.fm_solver import fm_solver

# ---------------------------------------------------------------------------------------------------------------------- 
# compute_rayleigh
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Energy-Propulsors-Converters-Combustor 
def compute_rayleigh(self,conditions):
    """ This combutes the temperature and pressure change across the
    the combustor using Rayleigh Line flow; it checks for themal choking.

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
    Tt_in  = self.inputs.stagnation_temperature
    Pt_in  = self.inputs.stagnation_pressure
    Mach   = self.inputs.mach_number
    Tt4    = self.turbine_inlet_temperature
    pib    = self.pressure_ratio
    eta_b  = self.efficiency
    
    # unpacking values from self
    htf    = self.fuel_data.specific_energy
    ar     = self.area_ratio
    
    # Rayleigh flow analysis, constant pressure burner
        
    # Initialize arrays
    M_out  = 1*Pt_in/Pt_in
    Ptr    = 1*Pt_in/Pt_in

    # Isentropic decceleration through divergent nozzle
    Mach   = np.atleast_2d(fm_solver(ar,Mach[:,0],gamma[:,0])).T
    
    # Determine max stagnation temperature to thermally choke flow                                     
    Tt4_ray = Tt_in*(1.+gamma*Mach*Mach)**2./((2.*(1.+gamma)*Mach*Mach)*(1.+(gamma-1.)/2.*Mach*Mach))

    # Rayleigh limitations define Tt4, taking max temperature before choking
    Tt4 = Tt4 * np.ones_like(Tt4_ray)
    Tt4[Tt4_ray <= Tt4] = Tt4_ray[Tt4_ray <= Tt4]
    
    #Rayleigh calculations
    M_out[:,0], Ptr[:,0] = rayleigh(gamma[:,0],Mach[:,0],Tt4[:,0]/Tt_in[:,0]) 
    Pt_out     = Ptr*Pt_in
        
    # method to compute combustor properties
    # method - computing the stagnation enthalpies from stagnation temperatures
    ht4     = Cp*Tt4
    ho      = Cp*To
    ht_in   = Cp*Tt_in
    
    # Using the Turbine exit temperature, the fuel properties and freestream temperature to compute the fuel to air ratio f
    f       = (ht4 - ht_in)/(eta_b*htf-ht4)

    # Computing the exit static and stagnation conditions
    ht_out  = Cp*Tt4   #May be double counting here.....no need (maybe)
    
    # pack computed quantities into outputs
    self.outputs.stagnation_temperature  = Tt4
    self.outputs.stagnation_pressure     = Pt_out
    self.outputs.stagnation_enthalpy     = ht_out
    self.outputs.fuel_to_air_ratio       = f    
    self.outputs.mach_number             = M_out