## @ingroup Methods-Energy-Propulsors-Converters-Fan
# RCAIDE/Library/Methods/Energy/Propulsors/Converters/Fan/compute_fan_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Feb 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
# package imports
import numpy as np 
from Legacy.trunk.S.Methods.Propulsion.fm_id import fm_id

# exceptions/warnings
from warnings import warn

# ----------------------------------------------------------------------------------------------------------------------
#  compute_expansion_nozzle_performance
# ----------------------------------------------------------------------------------------------------------------------           
## @ingroup Methods-Energy-Propulsors-Converters-Expansion_Nozzle
def compute_expansion_nozzle_performance(expansion_nozzle,conditions):
    """ This computes the output values from the input values according to
    equations from the source.

    Assumptions:
    Constant polytropic efficiency and pressure ratio
    If pressures make the Mach number go negative, these values are corrected

    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Inputs:
    conditions.freestream.
      isentropic_expansion_factor         [-]
      specific_heat_at_constant_pressure  [J/(kg K)]
      pressure                            [Pa]
      stagnation_pressure                 [Pa]
      stagnation_temperature              [K]
      specific_gas_constant               [J/(kg K)] 
      mach_number                         [-]
    expansion_nozzle.inputs.
      stagnation_temperature              [K]
      stagnation_pressure                 [Pa]

    Outputs:
    expansion_nozzle.outputs.
      stagnation_temperature              [K]  
      stagnation_pressure                 [Pa]
      stagnation_enthalpy                 [J/kg]
      mach_number                         [-]
      static_temperature                  [K]
      static_enthalpy                     [J/kg]
      velocity                            [m/s]
      static_pressure                     [Pa]
      area_ratio                          [-]
      denisty                             [kg/m^3]

    Properties Used:
    expansion_nozzle.
      pressure_ratio                      [-]
      polytropic_efficiency               [-]
    """                   
#unpack the values
    
    #unpack from conditions
    gamma    = conditions.freestream.isentropic_expansion_factor
    Cp       = conditions.freestream.specific_heat_at_constant_pressure
    Po       = conditions.freestream.pressure
    Pto      = conditions.freestream.stagnation_pressure
    Tto      = conditions.freestream.stagnation_temperature
    R        = conditions.freestream.gas_specific_constant
    Mo       = conditions.freestream.mach_number
    
    #unpack from inputs
    Tt_in    = expansion_nozzle.inputs.stagnation_temperature
    Pt_in    = expansion_nozzle.inputs.stagnation_pressure
    
    #unpack from expansion_nozzle
    pid      = expansion_nozzle.pressure_ratio
    etapold  = expansion_nozzle.polytropic_efficiency
    
    
    #Method for computing the nozzle properties
    
    #--Getting the output stagnation quantities
    Pt_out   = Pt_in*pid
    Tt_out   = Tt_in*pid**((gamma-1)/(gamma)*etapold)
    ht_out   = Cp*Tt_out
    
    # A cap so pressure doesn't go negative
    Pt_out[Pt_out<Po] = Po[Pt_out<Po]
    
    #compute the output Mach number, static quantities and the output velocity
    Mach          = np.sqrt((((Pt_out/Po)**((gamma-1)/gamma))-1)*2/(gamma-1))
    
    #Checking from Mach numbers below, above 1.0
    i_low         = Mach < 1.0
    i_high        = Mach >=1.0
    
    #initializing the Pout array
    P_out         = 1.0 *Mach/Mach
    
    #Computing output pressure and Mach number for the case Mach <1.0
    P_out[i_low]  = Po[i_low]
    Mach[i_low]   = np.sqrt((((Pt_out[i_low]/Po[i_low])**((gamma[i_low]-1.)/gamma[i_low]))-1.)*2./(gamma[i_low]-1.))
    
    #Computing output pressure and Mach number for the case Mach >=1.0        
    Mach[i_high]  = 1.0*Mach[i_high]/Mach[i_high]
    P_out[i_high] = Pt_out[i_high]/(1.+(gamma[i_high]-1.)/2.*Mach[i_high]*Mach[i_high])**(gamma[i_high]/(gamma[i_high]-1.))
    
    # A cap to make sure Mach doesn't go to zero:
    if np.any(Mach<=0.0):
        warn('Pressures Result in Negative Mach Number, making positive',RuntimeWarning)
        Mach[Mach<=0.0] = 0.001
    
    #Computing the output temperature,enthalpy, velocity and density
    T_out         = Tt_out/(1+(gamma-1)/2*Mach*Mach)
    h_out         = Cp*T_out
    u_out         = np.sqrt(2*(ht_out-h_out))
    rho_out       = P_out/(R*T_out)
    
    #Computing the freestream to nozzle area ratio (mainly from thrust computation)
    area_ratio    = (fm_id(Mo,gamma)/fm_id(Mach,gamma)*(1/(Pt_out/Pto))*(np.sqrt(Tt_out/Tto)))
    
    #pack computed quantities into outputs
    expansion_nozzle.outputs.stagnation_temperature  = Tt_out
    expansion_nozzle.outputs.stagnation_pressure     = Pt_out
    expansion_nozzle.outputs.stagnation_enthalpy     = ht_out
    expansion_nozzle.outputs.mach_number             = Mach
    expansion_nozzle.outputs.static_temperature      = T_out
    expansion_nozzle.outputs.density                 = rho_out
    expansion_nozzle.outputs.static_enthalpy         = h_out
    expansion_nozzle.outputs.velocity                = u_out
    expansion_nozzle.outputs.static_pressure         = P_out
    expansion_nozzle.outputs.area_ratio              = area_ratio
    
    return 
