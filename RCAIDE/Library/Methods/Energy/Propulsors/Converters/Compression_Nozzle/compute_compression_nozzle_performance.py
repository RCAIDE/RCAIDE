## @ingroup Methods-Energy-Propulsors-Converters-Compression_Nozzle
# RCAIDE/Library/Methods/Energy/Propulsors/Converters/Compression_Nozzle/compute_compression_nozzle_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------     

# package imports
import numpy as np  
from warnings import warn

# ---------------------------------------------------------------------------------------------------------------------- 
# compute_compression_nozzle_performance
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Energy-Propulsors-Converters-Compression_Nozzle
def compute_compression_nozzle_performance(compression_nozzle,conditions):
    """ This computes the output values from the input values according to
    equations from the source.

    Assumptions:
    Constant polytropic efficiency and pressure ratio
    Adiabatic

    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Inputs:
    conditions.freestream.
      isentropic_expansion_factor         [-]
      specific_heat_at_constant_pressure  [J/(kg K)]
      pressure                            [Pa]
      gas_specific_constant               [J/(kg K)]
    compression_nozzle.inputs.
      stagnation_temperature              [K]
      stagnation_pressure                 [Pa]

    Outputs:
    compression_nozzle.outputs.
      stagnation_temperature              [K]
      stagnation_pressure                 [Pa]
      stagnation_enthalpy                 [J/kg]
      mach_number                         [-]
      static_temperature                  [K]
      static_enthalpy                     [J/kg]
      velocity                            [m/s]

    Properties Used:
    compression_nozzle.
      pressure_ratio                      [-]
      polytropic_efficiency               [-]
      pressure_recovery                   [-]
    """

    #unpack from conditions
    gamma   = conditions.freestream.isentropic_expansion_factor
    Cp      = conditions.freestream.specific_heat_at_constant_pressure
    Po      = conditions.freestream.pressure
    Mo      = conditions.freestream.mach_number
    R       = conditions.freestream.gas_specific_constant

    #unpack from inpust
    Tt_in   = compression_nozzle.inputs.stagnation_temperature
    Pt_in   = compression_nozzle.inputs.stagnation_pressure

    #unpack from compression_nozzle
    pid     =  compression_nozzle.pressure_ratio
    etapold =  compression_nozzle.polytropic_efficiency
    eta_rec =  compression_nozzle.pressure_recovery
    compressibility_effects =  compression_nozzle.compressibility_effects

    #Method to compute the output variables

    #--Getting the output stagnation quantities
    Pt_out  = Pt_in*pid*eta_rec
    Tt_out  = Tt_in*(pid*eta_rec)**((gamma-1)/(gamma*etapold))
    ht_out  = Cp*Tt_out

    if compressibility_effects :

        # Checking from Mach numbers below, above 1.0
        i_low  = Mo <= 1.0
        i_high = Mo > 1.0

        #initializing the arrays
        Mach     = np.ones_like(Pt_in)
        T_out    = np.ones_like(Pt_in)
        Mo       = Mo * np.ones_like(Pt_in)
        Pt_out   = np.ones_like(Pt_in)
        P_out    = np.ones_like(Pt_in)

        #-- Inlet Mach <= 1.0, isentropic relations
        Pt_out[i_low]  = Pt_in[i_low]*pid
        Mach[i_low]    = np.sqrt( (((Pt_out[i_low]/Po[i_low])**((gamma[i_low]-1.)/gamma[i_low]))-1.) *2./(gamma[i_low]-1.) ) 
        T_out[i_low]   = Tt_out[i_low]/(1.+(gamma[i_low]-1.)/2.*Mach[i_low]*Mach[i_low])

        #-- Inlet Mach > 1.0, normal shock
        Mach[i_high]   = np.sqrt((1.+(gamma[i_high]-1.)/2.*Mo[i_high]**2.)/(gamma[i_high]*Mo[i_high]**2-(gamma[i_high]-1.)/2.))
        T_out[i_high]  = Tt_out[i_high]/(1.+(gamma[i_high]-1.)/2*Mach[i_high]*Mach[i_high])
        Pt_out[i_high] = pid*Pt_in[i_high]*((((gamma[i_high]+1.)*(Mo[i_high]**2.))/((gamma[i_high]-1.)*Mo[i_high]**2.+2.))**(gamma[i_high]/(gamma[i_high]-1.)))*((gamma[i_high]+1.)/(2.*gamma[i_high]*Mo[i_high]**2.-(gamma[i_high]-1.)))**(1./(gamma[i_high]-1.))
        P_out[i_high]  = Pt_out[i_high]*(1.+(gamma[i_high]-1.)/2.*Mach[i_high]**2.)**(-gamma[i_high]/(gamma[i_high]-1.))
    else:
        Pt_out  = Pt_in*pid*eta_rec
        
        # in case pressures go too low
        if np.any(Pt_out<Po):
            warn('Pt_out goes too low',RuntimeWarning)
            Pt_out[Pt_out<Po] = Po[Pt_out<Po]

        Mach    = np.sqrt( (((Pt_out/Po)**((gamma-1.)/gamma))-1.) *2./(gamma-1.) )
        T_out  = Tt_out/(1.+(gamma-1.)/2.*Mach*Mach)


    #-- Compute exit velocity and enthalpy
    h_out   = Cp*T_out
    u_out   = np.sqrt(2.*(ht_out-h_out))

    #pack computed quantities into outputs
    compression_nozzle.outputs.stagnation_temperature  = Tt_out
    compression_nozzle.outputs.stagnation_pressure     = Pt_out
    compression_nozzle.outputs.stagnation_enthalpy     = ht_out
    compression_nozzle.outputs.mach_number             = Mach
    compression_nozzle.outputs.static_temperature      = T_out
    compression_nozzle.outputs.static_enthalpy         = h_out
    compression_nozzle.outputs.velocity                = u_out