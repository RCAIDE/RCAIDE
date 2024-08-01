# RCAIDE/Library/Methods/Propulsors/Converters/Compression_Nozzle/compute_compression_nozzle_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------     

# package imports
import numpy as np  
from warnings import warn

# ---------------------------------------------------------------------------------------------------------------------- 
# compute_compression_nozzle_performance
# ----------------------------------------------------------------------------------------------------------------------    
def compute_compression_nozzle_performance(compression_nozzle,nozzle_conditions,freestream):
    """  Computes the performance of a compression nozzle bases on its polytropic efficiency.
         The following properties are computed: 
        compression_nozzle.outputs.
          stagnation_temperature             (numpy.ndarray): exit stagnation temperature [K]
          stagnation_pressure                (numpy.ndarray): exit stagnation pressure    [Pa]
          stagnation_enthalpy                (numpy.ndarray): exit stagnation enthalpy    [J/kg]
          mach_number                        (numpy.ndarray): exit Mach number            [unitless]
          static_temperature                 (numpy.ndarray): exit static temperature     [K]
          static_enthalpy                    (numpy.ndarray): exit static enthalpy        [J/kg]
          velocity                           (numpy.ndarray): exit nozzle velocity        [m/s]
          

    Assumptions:  
        1. Pressure ratio and polytropic efficiency do not change with varying conditions.
        2. Adiabatic
        3. Subsonic or choked output.

    Source:
        https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Args:
        conditions.freestream.
          isentropic_expansion_factor         (numpy.ndarray): isentropic_expansion_factor        [unitless]
          specific_heat_at_constant_pressure  (numpy.ndarray): specific_heat_at_constant_pressure [J/(kg K)]
          pressure                            (numpy.ndarray): pressure                           [Pa]
          gas_specific_constant               (numpy.ndarray): gas_specific_constant              [J/(kg K)]
        compression_nozzle.
          inputs.stagnation_temperature       (numpy.ndarra): entering stagnation_temperature     [K]
          inputs.stagnation_pressure          (numpy.ndarra): entering stagnation_pressure        [Pa] 
          pressure_ratio                             (float): pressure_ratio                      [unitless]
          polytropic_efficiency                      (float): polytropic_efficiency               [unitless]
          pressure_recovery                          (float): pressure_recovery                   [unitless]

    Returns:
    """

    # Unpack conditions
    gamma   = freestream.isentropic_expansion_factor
    Cp      = freestream.specific_heat_at_constant_pressure
    P0      = freestream.pressure
    M0      = freestream.mach_number 

    # Unpack inpust
    Tt_in                   = nozzle_conditions.inputs.stagnation_temperature
    Pt_in                   = nozzle_conditions.inputs.stagnation_pressure
    PR                      = compression_nozzle.pressure_ratio
    eta_p_old               = compression_nozzle.polytropic_efficiency
    eta_rec                 = compression_nozzle.pressure_recovery
    compressibility_effects = compression_nozzle.compressibility_effects
 
    # Compute output stagnation quantities
    Pt_out  = Pt_in*PR*eta_rec
    Tt_out  = Tt_in*(PR*eta_rec)**((gamma-1)/(gamma*eta_p_old))
    ht_out  = Tt_out*Cp 

    if compressibility_effects: 
        # initilize arrays
        Pt_out   = np.ones_like(Tt_in)
        Mach     = np.ones_like(Tt_in)
        T_out    = np.ones_like(Tt_in)
        P_out    = np.ones_like(Tt_in)

        # if Inlet Mach <= 1.0, use isentropic relations
        i_low          = M0 <= 1.0
        Pt_out[i_low]  = Pt_in[i_low]*PR
        Mach[i_low]    = np.sqrt( (((Pt_out[i_low]/P0[i_low])**((gamma[i_low]-1.)/gamma[i_low]))-1.) *2./(gamma[i_low]-1.) ) 
        T_out[i_low]   = Tt_out[i_low]/(1.+(gamma[i_low]-1.)/2.*Mach[i_low]*Mach[i_low])

        # if Inlet Mach > 1.0, use normal shock
        i_high         = M0 > 1.0
        Mach[i_high]   = np.sqrt((1.+(gamma[i_high]-1.)/2.*M0[i_high]**2.)/(gamma[i_high]*M0[i_high]**2-(gamma[i_high]-1.)/2.))
        T_out[i_high]  = Tt_out[i_high]/(1.+(gamma[i_high]-1.)/2*Mach[i_high]*Mach[i_high])
        Pt_out[i_high] = PR*Pt_in[i_high]*((((gamma[i_high]+1.)*(M0[i_high]**2.))/((gamma[i_high]-1.)*\
                        M0[i_high]**2.+2.))**(gamma[i_high]/(gamma[i_high]-1.)))*((gamma[i_high]+1.)/(2.*gamma[i_high]*\
                        M0[i_high]**2.-(gamma[i_high]-1.)))**(1./(gamma[i_high]-1.))
        P_out[i_high]  = Pt_out[i_high]*(1.+(gamma[i_high]-1.)/2.*Mach[i_high]**2.)**(-gamma[i_high]/(gamma[i_high]-1.))
    else:
        Pt_out  = Pt_in*PR*eta_rec 
        if np.any(Pt_out<P0): # in case pressures go too low
            warn('Pt_out goes too low',RuntimeWarning)
            Pt_out[Pt_out<P0] = P0[Pt_out<P0] 
        Mach   = np.sqrt( (((Pt_out/P0)**((gamma-1.)/gamma))-1.) *2./(gamma-1.) )
        T_out  = Tt_out/(1.+(gamma-1.)/2.*Mach*Mach)
        
    # Compute exit ethalpy and velocity  
    h_out   = Cp*T_out
    u_out   = np.sqrt(2.*(ht_out-h_out))

    # Pack computed quantities into outputs
    nozzle_conditions.outputs.mach_number             = Mach
    nozzle_conditions.outputs.static_temperature      = T_out
    nozzle_conditions.outputs.static_enthalpy         = h_out
    nozzle_conditions.outputs.velocity                = u_out
    nozzle_conditions.outputs.stagnation_temperature  = Tt_out
    nozzle_conditions.outputs.stagnation_pressure     = Pt_out
    nozzle_conditions.outputs.stagnation_temperature  = Tt_out
    nozzle_conditions.outputs.stagnation_pressure     = Pt_out
    nozzle_conditions.outputs.stagnation_enthalpy     = ht_out
    
    return 