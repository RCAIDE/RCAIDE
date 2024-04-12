## @ingroup Methods-Weights-Correlations-Propulsion
# hts_motor.py
# 
# Created:  Jan 2014, M. Vegh, 
# Modified: Feb 2014, A. Wendorff
#           Feb 2016, E. Botero    
#           Mar 2020, M. Clarke

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from Legacy.trunk.S.Core import Units 

# ----------------------------------------------------------------------
#   HTS Motor
# ----------------------------------------------------------------------

## @ingroup Methods-Weights-Correlations-Propulsion
def func_hts_motor(max_power):
    """ Calculate the weight of a high temperature superconducting motor
    
   Assumptions:
           calculated from fit of commercial available motors
           
   Source: [10] Snyder, C., Berton, J., Brown, G. et all
           'Propulsion Investigation for Zero and Near-Zero Emissions Aircraft,' NASA STI Program,
           NASA Glenn,  2009.012. page 12
           
   Inputs:
           max_power- maximum power the motor can deliver safely   [Watts]
   
   Outputs:
           weight- weight of the motor                             [kilograms]
       
    Properties Used:
           N/A
    """   

    mass = 2.28*((max_power/1000.)**.6616)*Units.lbs # conversion to kg
    
    return mass


hts_motor(State, Settings, System):
	#TODO: max_power = [Replace With State, Settings, or System Attribute]

	results = func_hts_motor('max_power',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System