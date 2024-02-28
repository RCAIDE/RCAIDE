## @ingroup Methods-Energy-Propulsors-Converters-Combustor
# RCAIDE/Methods/Energy/Propulsors/Converters/Combustor/compute_supersonic_combustion.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------     

# package imports
import numpy as np 

# ---------------------------------------------------------------------------------------------------------------------- 
# calculate_power_from_throttle
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Energy-Propulsors-Converters-Combustor 
def compute_supersonic_combustion(self,conditions): 
    """ This function computes the output values for supersonic  
    combustion (Scramjet).  This will be done using stream thrust 
    analysis. 
    
    Assumptions: 
    Constant Pressure Combustion      
    Flow is in axial direction at all times 
    Flow properities at exit are 1-Da averages 

    Source: 
    Heiser, William H., Pratt, D. T., Daley, D. H., and Unmeel, B. M., 
    "Hypersonic Airbreathing Propulsion", 1994 
    Chapter 4 - pgs. 175-180
    
    Inputs: 
    conditions.freestream. 
       isentropic_expansion_factor          [-] 
       specific_heat_at_constant_pressure   [J/(kg K)] 
       temperature                          [K] 
       stagnation_temperature               [K]
       universal_gas_constant               [J/(kg K)]  
    self.inputs. 
       stagnation_temperature               [K] 
       stagnation_pressure                  [Pa] 
       inlet_nozzle                         [-] 

    Outputs: 
    self.outputs. 
       stagnation_temperature               [K] 
       stagnation_pressure                  [Pa] 
       stagnation_enthalpy                  [J/kg] 
       fuel_to_air_ratio                    [-] 
       static_temperature                   [K] 
       static_pressure                      [Pa] 
       velocity                             [m/s] 
       mach_number                          [-]          
    
   Properties Used: 
      self.fuel_data.specific_energy       [J/kg] 
      self.efficiency                      [-]
      self.axial_fuel_velocity_ratio       [-] 
      self.fuel_velocity_ratio             [-] 
      self.burner_drag_coefficient         [-] 
      self.temperature_reference           [K] 
      self.absolute_sensible_enthalpy      [J/kg] 
      self.specific_heat_constant_pressure [J/(kg K)] 
      """ 
    # unpack the values 

    # unpacking the values from conditions 
    R      = conditions.freestream.gas_specific_constant 
    Tref   = conditions.freestream.temperature
    
    # unpacking the values from inputs 
    nozzle  = self.inputs.inlet_nozzle 
    Pt_in   = self.inputs.stagnation_pressure 
    Cp_c    = nozzle.specific_heat_at_constant_pressure
    
    # unpacking the values from self 
    htf     = self.fuel_data.specific_energy 
    eta_b   = self.efficiency 
    Vfx_V3  = self.axial_fuel_velocity_ratio 
    Vf_V3   = self.fuel_velocity_ratio 
    Cfb     = self.burner_drag_coefficient 
    hf      = self.absolute_sensible_enthalpy 
    phi     = self.fuel_equivalency_ratio
    
    # compute gamma and Cp over burner 
    Cpb     = Cp_c*1.45          # Estimate from Heiser and Pratt
    gamma_b = (Cpb/R)/(Cpb/R-1.)  
    
    # unpack nozzle input values 
    T_in = nozzle.static_temperature 
    V_in = nozzle.velocity 
    P_in = nozzle.static_pressure 
    
    # setting stoichiometric fuel-to-air  
    f_st = self.fuel_data.stoichiometric_fuel_to_air
    f    = phi*f_st
    
    # compute output velocity, mach and temperature 
    V_out  = V_in*(((1.+f*Vfx_V3)/(1.+f))-(Cfb/(2.*(1.+f)))) 
    T_out  = ((T_in/(1.+f))*(1.+(1./(Cpb*T_in ))*(eta_b*f*htf+f*hf+f*Cpb*Tref+(1.+f*Vf_V3*Vf_V3)*V_in*V_in/2.))) - V_out*V_out/(2.*Cpb) 
    M_out  = V_out/(np.sqrt(gamma_b*R*T_out)) 
    Tt_out = T_out*(1.+(gamma_b-1.)/2.)*M_out*M_out
    
    # compute the exity static and stagnation conditions 
    ht_out = Cpb*Tt_out 
    P_out  = P_in 
    Pt_out = Pt_in*((((gamma_b+1.)*(M_out**2.))/((gamma_b-1.)*M_out**2.+2.))**(gamma_b/(gamma_b-1.)))*((gamma_b+1.)/(2.*gamma_b*M_out**2.-(gamma_b-1.)))**(1./(gamma_b-1.))  
    
    # pack computed quantities into outputs    
    self.outputs.stagnation_temperature          = Tt_out  
    self.outputs.stagnation_pressure             = Pt_out        
    self.outputs.stagnation_enthalpy             = ht_out        
    self.outputs.fuel_to_air_ratio               = f        
    self.outputs.static_temperature              = T_out  
    self.outputs.static_pressure                 = P_out         
    self.outputs.velocity                        = V_out  
    self.outputs.mach_number                     = M_out 
    self.outputs.specific_heat_constant_pressure = Cpb
    self.outputs.isentropic_expansion_factor     = gamma_b
