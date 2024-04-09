## @ingroup Methods-Weights-Correlations-Common 
# payload.py
# 
# Created:  Jan 2014, A. Wendorff
# Modified: Feb 2014, A. Wendorff
#           Feb 2016, E. Botero
#           Jul 2017, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from Legacy.trunk.S.Core import Units, Data


# ----------------------------------------------------------------------
#   Payload
# ----------------------------------------------------------------------

## @ingroup Methods-Weights-Correlations-Common 
def func_payload(vehicle, wt_passenger=195 * Units.lbs, wt_baggage=30 * Units.lbs):
    """ Calculate the weight of the payload and the resulting fuel mass
    
    Assumptions:
        based on FAA guidelines for weight of passengers
        
    Source: 
        N/A
        
    Inputs:
        TOW -                                                              [kilograms]
        wt_empty - Operating empty weight of the aircraft                  [kilograms]
        num_pax - number of passengers on the aircraft                     [dimensionless]
        wt_cargo - weight of cargo being carried on the aircraft           [kilogram]
        wt_passenger - weight of each passenger on the aircraft            [kilogram]
        wt_baggage - weight of the baggage for each passenger              [kilogram]
    
    Outputs:
        output - a data dictionary with fields:
            payload - weight of the passengers plus baggage and paid cargo [kilograms]
            pax - weight of all the passengers                             [kilogram]
            bag - weight of all the baggage                                [kilogram]
            fuel - weight of the fuel carried                              [kilogram]
            empty - operating empty weight of the aircraft                 [kilograms]
               
    Properties Used:
        N/A
    """

    # process
    num_pax     = vehicle.passengers
    wt_pax      = wt_passenger * num_pax
    wt_bag      = wt_baggage * num_pax
    wt_payload  = wt_pax + wt_bag + vehicle.mass_properties.cargo

    # packup outputs
    output              = Data()
    output.total        = wt_payload
    output.passengers   = wt_pax
    output.baggage      = wt_bag
    output.cargo        = vehicle.mass_properties.cargo

    return output



def payload(State, Settings, System):
	#TODO: vehicle      = [Replace With State, Settings, or System Attribute]
	#TODO: wt_passenger = [Replace With State, Settings, or System Attribute]
	#TODO: wt_baggage   = [Replace With State, Settings, or System Attribute]

	results = func_payload('vehicle', 'wt_passenger', 'wt_baggage')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System