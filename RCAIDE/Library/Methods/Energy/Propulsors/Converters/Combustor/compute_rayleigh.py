## @ingroup Methods-Energy-Propulsors-Converters-Combustor
# RCAIDE/Library/Methods/Energy/Propulsors/Converters/Combustor/compute_rayleigh.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------     

# package imports
import numpy as np 
from Legacy.trunk.S.Methods.Propulsion.rayleigh  import rayleigh
from Legacy.trunk.S.Methods.Propulsion.fm_solver import fm_solver

# ---------------------------------------------------------------------------------------------------------------------- 
# compute_rayleigh
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Energy-Propulsors-Converters-Combustor 
def compute_rayleigh(combustor,conditions):
    """ This combutes the temperature and pressure change across the combustor using Rayleigh Line flow.
    The following properties are computed 
        combustor.outputs.
          stagnation_temperature             (numpy.ndarray): [K]  
          stagnation_pressure                (numpy.ndarray): [Pa]
          stagnation_enthalpy                (numpy.ndarray): [J/kg]
          fuel_to_air_ratio                  (numpy.ndarray): [unitless] 
   
    Assumptions:
        1. Constant efficiency and pressure ratio
        2. Limits temepature ratio if thermal choking occures 

    Source:
        https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Args:
        conditions.freestream.
          isentropic_expansion_factor        (numpy.ndarray): [unitless]
          specific_heat_at_constant_pressure (numpy.ndarray): [J/(kg K)]
          temperature                        (numpy.ndarray): [K]
          stagnation_temperature             (numpy.ndarray): [K]
        combustor.inputs. 
          stagnation_temperature             (numpy.ndarray): [K]
          stagnation_pressure                (numpy.ndarray): [Pa]
        combustor.
          turbine_inlet_temperature                  (float): [K]
          pressure_ratio                             (float): [unitless]
          efficiency                                 (float): [unitless]
          area_ratio                                 (float): [unitless]
          fuel_data.specific_energy                  (float): [J/kg]
 
    Returns:
        None 
    """          
    # unpacking the values from conditions
    gamma  = conditions.freestream.isentropic_expansion_factor 
    Cp     = conditions.freestream.specific_heat_at_constant_pressure 
    
    # unpack properties of combustor 
    Tt_in  = combustor.inputs.stagnation_temperature
    Pt_in  = combustor.inputs.stagnation_pressure
    Mach   = combustor.inputs.mach_number
    Tt4    = combustor.turbine_inlet_temperature 
    eta_b  = combustor.efficiency 
    htf    = combustor.fuel_data.specific_energy
    ar     = combustor.area_ratio
    
    # Rayleigh flow analysis, constant pressure burner  
    M_out  = 1*Pt_in/Pt_in
    Ptr    = 1*Pt_in/Pt_in

    # Isentropic decceleration through divergent nozzle
    Mach   = np.atleast_2d(fm_solver(ar,Mach[:,0],gamma[:,0])).T
    
    # Determine max stagnation temperature to thermally choke flow                                     
    Tt4_ray = Tt_in*(1.+gamma*Mach*Mach)**2./((2.*(1.+gamma)*Mach*Mach)*(1.+(gamma-1.)/2.*Mach*Mach))

    # Rayleigh limitations define Tt4, taking max temperature before choking
    Tt4                 = np.ones_like(Tt4_ray) * Tt4 
    Tt4[Tt4_ray <= Tt4] = Tt4_ray[Tt4_ray <= Tt4]
    
    # Rayleigh calculations
    M_out[:,0], Ptr[:,0] = rayleigh(gamma[:,0],Mach[:,0],Tt4[:,0]/Tt_in[:,0]) 
    Pt_out               = Ptr*Pt_in
         
    # Compute the stagnation enthalpies from stagnation temperatures
    ht4     = Tt4 * Cp 
    ht_in   = Tt_in * Cp 
    
    # Using the Turbine exit temperature, the fuel properties and freestream temperature 
    # to compute the fuel to air ratio f
    f       = (ht4 - ht_in)/(eta_b*htf-ht4)

    # Computing the exit static and stagnation conditions
    ht_out  = Tt4 * Cp 
    
    # Pack results 
    combustor.outputs.stagnation_temperature  = Tt4
    combustor.outputs.stagnation_pressure     = Pt_out
    combustor.outputs.stagnation_enthalpy     = ht_out
    combustor.outputs.fuel_to_air_ratio       = f    
    combustor.outputs.mach_number             = M_out
    return 
