## @ingroup Methods-Weights-Correlations-General_Aviation
# landing_gear.py
# 
# Created:  Feb 2018, M. Vegh
# Modified: 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from Legacy.trunk.S.Core import Data,Units
import numpy as np

# ----------------------------------------------------------------------
#   Landing Gear
# ----------------------------------------------------------------------

## @ingroup Methods-Weights-Correlations-General_Aviation
def func_landing_gear(landing_weight, Nult, strut_length_main, strut_length_nose):
    """ 
        Calculate the weight of the landing gear

        Source: Raymer- Aircraft Design: a Conceptual Approach (pg 460 in 4th edition)
        
        Inputs:
            Nult - ultimate landing load factor
            landing_weight- landing weight of the aircraft [kilograms]
           
        Outputs:
            weight - weight of the landing gear            [kilograms]
            
        Assumptions:
            calculating the landing gear weight based on the landing weight, load factor, and strut length 
    """ 

    #unpack
    W_l = landing_weight/Units.lbs
    l_n = strut_length_nose/Units.inches
    l_m = strut_length_main/Units.inches
    main_weight = .095*((Nult*W_l)**.768)*(l_m/12.)**.409
    nose_weight = .125*((Nult*W_l)**.566)*(l_n/12.)**.845

    #pack outputs
    output = Data
    output.main = main_weight*Units.lbs
    output.nose = nose_weight*Units.lbs

    return output


landing_gear(State, Settings, System):
	#TODO: landing_weight    = [Replace With State, Settings, or System Attribute]
	#TODO: Nult              = [Replace With State, Settings, or System Attribute]
	#TODO: strut_length_main = [Replace With State, Settings, or System Attribute]
	#TODO: strut_length_nose = [Replace With State, Settings, or System Attribute]

	results = func_landing_gear('landing_weight', 'Nult', 'strut_length_main', 'strut_length_nose')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System