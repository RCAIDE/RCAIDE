## @ingroup Methods-Power-Battery-Cell_Cycle_Models 
# LiNiMnCoO2_cell_cycle_model.py
# 
# Created: Sep 2021, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import numpy as np  

# ----------------------------------------------------------------------
#  Compute NMC cell state variables
# ----------------------------------------------------------------------

## @ingroup Methods-Power-Battery-Cell_Cycle_Models 
def func_compute_NMC_cell_state_variables(battery_data,SOC,T,I):
    """This computes the electrical state variables of a lithium ion 
    battery cell with a  lithium-nickel-cobalt-aluminum oxide cathode 
    chemistry from look-up tables 
     
    Assumtions: 
    N/A
    
    Source:  
    N/A 
     
    Inputs:
        SOC           - state of charge of cell     [unitless]
        battery_data  - look-up data structure      [unitless]
        T             - battery cell temperature    [Kelvin]
        I             - battery cell current        [Amperes]
    
    Outputs:  
        V_ul          - under-load voltage          [Volts] 
        
    """ 

    # Make sure things do not break by limiting current, temperature and current 
    SOC[SOC < 0.]   = 0.  
    SOC[SOC > 1.]   = 1.    
    DOD             = 1 - SOC 
    
    T[np.isnan(T)] = 302.65
    T[T<272.65]    = 272.65 # model does not fit for below 0  degrees
    T[T>322.65]    = 322.65 # model does not fit for above 50 degrees
     
    I[I<0.0]       = 0.0
    I[I>8.0]       = 8.0   
     
    pts            = np.hstack((np.hstack((I, T)),DOD  )) # amps, temp, SOC   
    V_ul           = np.atleast_2d(battery_data.Voltage(pts)[:,1]).T  
    
    return V_ul


def compute_NMC_cell_state_variables(State, Settings, System):
	#TODO: battery_data = [Replace With State, Settings, or System Attribute]
	#TODO: SOC          = [Replace With State, Settings, or System Attribute]
	#TODO: T            = [Replace With State, Settings, or System Attribute]
	#TODO: I            = [Replace With State, Settings, or System Attribute]

	results = func_compute_NMC_cell_state_variables('battery_data', 'SOC', 'T', 'I')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System