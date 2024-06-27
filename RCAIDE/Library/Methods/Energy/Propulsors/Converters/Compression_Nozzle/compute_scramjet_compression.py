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
    """This function computes the compression of a scramjet 
    using shock trains.  

    Assumptions: 

    Source: 
    Heiser, William H., Pratt, D. T., Daley, D. H., and Unmeel, B. M.,  
    "Hypersonic Airbreathing Propulsion", 1994  
    Chapter 4 - pgs. 175-180
    
    Args: 
       conditions.freestream. 
       isentropic_expansion_factor        [-] 
       specific_heat_at_constant_pressure [J/(kg K)] 
       pressure                           [Pa] 
       gas_specific_constant              [J/(kg K)] 
       temperature                        [K] 
       mach_number                        [-] 
       velocity                           [m/s] 

    compression_nozzle.inputs. 
       stagnation_temperature             [K] 
       stagnation_pressure                [Pa] 

    compression_nozzle. 
       efficiency                         [-] 
       shock_count                        [-] 
       theta                              [Rad] 
    Returns: 
    compression_nozzle.outputs. 
       stagnation_temperature             [K] 
       stagnation_pressure                [Pa] 
       stagnation_enthalpy                [J/kg] 
       mach_number                        [-] 
       static_temperature                 [K] 
       static_enthalpy                    [J/kg] 
       velocity                           [m/s] 
       specific_heat_at_constant_pressure [J/(kg K)]  
    """ 
    # unpack from conditions 
    gamma       = conditions.freestream.isentropic_expansion_factor 
    Cp          = conditions.freestream.specific_heat_at_constant_pressure 
    P0          = conditions.freestream.pressure 
    T0          = conditions.freestream.temperature 
    M0          = conditions.freestream.mach_number 
    U0          = conditions.freestream.velocity
    R           = conditions.freestream.gas_specific_constant
    
    # unpack from inputs 
    Tt_in       = compression_nozzle.inputs.stagnation_temperature 
    Pt_in       = compression_nozzle.inputs.stagnation_pressure 
    eta         = compression_nozzle.polytropic_efficiency 
    shock_count = compression_nozzle.compression_levels 
    theta       = compression_nozzle.theta
    
    # compute compressed flow variables
    # compute inlet conditions, based on geometry and number of shocks 
    psi, Ptr    = shock_train(M0,gamma,shock_count,theta) 
    
    # Compute/Look Up New gamma and Cp values (Future Work)
    gamma_c     = gamma
    Cp_c        = Cp
    
    # compute outputs 
    T_out       = psi*T0 
    P_out       = P0*(psi/(psi*(1.-eta)+eta))**(Cp_c/R) 
    Pt_out      = Ptr*Pt_in 
    Mach        = np.sqrt((2./(gamma_c-1.))*((T0/T_out)*(1.+(gamma_c-1.)/2.*M0*M0)-1.)) 
    u_out       = np.sqrt(U0*U0-2.*Cp_c*T0*(psi-1.)) 
    h_out       = Cp_c*T_out 
    Tt_out      = Tt_in 
    ht_out      = Cp_c*Tt_out 
    
    # packing output values  
    compression_nozzle.outputs.stagnation_temperature             = Tt_out              
    compression_nozzle.outputs.stagnation_pressure                = Pt_out                
    compression_nozzle.outputs.stagnation_enthalpy                = ht_out         
    compression_nozzle.outputs.mach_number                        = Mach        
    compression_nozzle.outputs.static_temperature                 = T_out        
    compression_nozzle.outputs.static_enthalpy                    = h_out          
    compression_nozzle.outputs.static_pressure                    = P_out
    compression_nozzle.outputs.specific_heat_at_constant_pressure = Cp_c
    compression_nozzle.outputs.velocity                           = u_out
    
    return 