## @ingroup Methods-Weights-Correlations-Propulsion
# engine_jet.py
# 
# Created:  Jan 2014, A. Wendorff
# Modified: Feb 2014, A. Wendorff
#           Feb 2016, E. Botero   


# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from Legacy.trunk.S.Core import Units

# ----------------------------------------------------------------------
#   Jet Engine
# ----------------------------------------------------------------------

## @ingroup Methods-Weights-Correlations-Propulsion
def func_engine_jet(thrust_sls):
    """ Calculate the weight of the dry engine  
    
    Assumptions:
            calculated engine weight from a correlation of engines
    
    Source: 
            N/A
            
    Inputs:
            thrust_sls - sea level static thrust of a single engine [Newtons]
    
    Outputs:
            weight - weight of the dry engine                       [kilograms]
        
    Properties Used:
            N/A
    """     
    # setup
    thrust_sls_en = thrust_sls / Units.force_pound # Convert N to lbs force  
    
    # process
    weight = (0.4054*thrust_sls_en ** 0.9255) * Units.lb # Convert lbs to kg
    
    return weight


engine_jet(State, Settings, System):
	#TODO: thrust_sls = [Replace With State, Settings, or System Attribute]

	results = func_engine_jet('thrust_sls',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System