## @ingroup Methods-Energy-Propulsors-Converters-Compression_Nozzle
# RCAIDE/Library/Methods/Energy/Propulsors/Converters/Compression_Nozzle/compute_scramjet_compression.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------     

# package imports
import numpy as np 
from Legacy.trunk.S.Methods.Propulsion.shock_train import shock_train

# ---------------------------------------------------------------------------------------------------------------------- 
# compute_scramjet_compression
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Energy-Propulsors-Converters-Compression_Nozzle       
def compute_scramjet_compression(compression_nozzle,conditions): 
    """This function computes the compression of a scramjet using shock trains.
        The following properties are computed: 
        compression_nozzle.outputs. 
           stagnation_temperature             (numpy.ndarray): exit stagnation_temperature             [K] 
           stagnation_pressure                (numpy.ndarray): exit stagnation_pressure                [Pa] 
           stagnation_enthalpy                (numpy.ndarray): exit stagnation_enthalpy                [J/kg] 
           mach_number                        (numpy.ndarray): exit mach_number                        [unitless] 
           static_temperature                 (numpy.ndarray): exit static_temperature                 [K] 
           static_enthalpy                    (numpy.ndarray): exit static_enthalpy                    [J/kg] 
           velocity                           (numpy.ndarray): exit velocity                           [m/s] 
           specific_heat_at_constant_pressure (numpy.ndarray): exit specific_heat_at_constant_pressure [J/(kg K)]  

    Assumptions: 
        None 

    Source: 
        Heiser, William H., Pratt, D. T., Daley, D. H., and Unmeel, B. M.,  
        "Hypersonic Airbreathing Propulsion", 1994  
        Chapter 4 - pgs. 175-180
    
    Args: 
       conditions.freestream. 
          isentropic_expansion_factor        (numpy.ndarray): isentropic_expansion_factor        [unitless] 
          specific_heat_at_constant_pressure (numpy.ndarray): specific_heat_at_constant_pressure [J/(kg K)] 
          pressure                           (numpy.ndarray): pressure                           [Pa] 
          gas_specific_constant              (numpy.ndarray): gas_specific_constant              [J/(kg K)] 
          temperature                        (numpy.ndarray): temperature                        [K] 
          mach_number                        (numpy.ndarray): mach_number                        [unitless] 
          velocity                           (numpy.ndarray): velocity                           [m/s]  
       compression_nozzle. 
          inputs.stagnation_temperature      (numpy.ndarray): entering stagnation temperature    [K] 
          inputs.stagnation_pressure         (numpy.ndarray): entering stagnation pressure       [Pa]  
          efficiency                                 (float): efficiency                         [unitless] 
          shock_count                                (float): shock_count                        [unitless] 
          theta                                      (float): theta                              [Rad] 

    Returns:
        None 
    """ 
    # Unpack from conditions 
    P0          = conditions.freestream.pressure 
    T0          = conditions.freestream.temperature 
    M0          = conditions.freestream.mach_number 
    U0          = conditions.freestream.velocity
    R           = conditions.freestream.gas_specific_constant
    gamma       = conditions.freestream.isentropic_expansion_factor 
    Cp          = conditions.freestream.specific_heat_at_constant_pressure 
    
    # Unpack from inputs 
    Tt_in       = compression_nozzle.inputs.stagnation_temperature 
    Pt_in       = compression_nozzle.inputs.stagnation_pressure 
    eta         = compression_nozzle.polytropic_efficiency 
    shock_count = compression_nozzle.compression_levels 
    theta       = compression_nozzle.theta
    
    # compute inlet conditions, based on geometry and number of shocks 
    T_ratio, Pt_ratio   = shock_train(M0,gamma,shock_count,theta)
    
    # Compute new gamma and Cp values (Future Work)
    gamma_c     = gamma
    Cp_c        = Cp
    
    # Compute propertis 
    Mach        = np.sqrt((2./(gamma_c-1.))*((T0/T_out)*(1.+(gamma_c-1.)/2.*M0*M0)-1.)) 
    P_out       = P0*(T_ratio/(T_ratio*(1.-eta)+eta))**(Cp_c/R) 
    T_out       = T_ratio*T0 
    U_out       = np.sqrt(U0*U0-2.*Cp_c*T0*(T_ratio-1.)) 
    h_out       = T_out * Cp_c
    Tt_out      = Tt_in 
    ht_out      = Tt_out * Cp_c
    Pt_out      = Pt_in * Pt_ratio
    
    # packing output values       
    compression_nozzle.outputs.mach_number                        = Mach        
    compression_nozzle.outputs.static_temperature                 = T_out        
    compression_nozzle.outputs.static_enthalpy                    = h_out          
    compression_nozzle.outputs.static_pressure                    = P_out
    compression_nozzle.outputs.specific_heat_at_constant_pressure = Cp_c
    compression_nozzle.outputs.velocity                           = U_out
    compression_nozzle.outputs.stagnation_temperature             = Tt_out              
    compression_nozzle.outputs.stagnation_pressure                = Pt_out                
    compression_nozzle.outputs.stagnation_enthalpy                = ht_out    
    
    return 