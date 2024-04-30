# passenger_payload.py
#
# Created:  Apr 2024, J. Smart
# Modified:

# ----------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------- 

from Legacy.trunk.S.Core import Units
from RCAIDE.Library.Components import PhysicalComponent

# -----------------------------------------------------------------------
# Functional/Library Version
# -----------------------------------------------------------------------

def func_passenger_payload(n_passengers,
                           m_passenger = 195. * Units.lbm,
                           m_baggage = 30. * Units.lbm,
                           *args, **kwargs):
    """
    Calculate the total mass of passengers and their baggage.

    Parameters:
    - n_passengers (int): Number of passengers.
    - wt_passenger (float): Weight of a single passenger, defaults to 195 lbm.
    - wt_baggage (float): Weight of the baggage per passenger, defaults to 30 lbm.
    - *args: Variable length argument list.
    - **kwargs: Arbitrary keyword arguments.

    Returns:
    - tuple: (passenger_mass, baggage_mass)
        - passenger_mass (float): Total mass of all passengers.
        - baggage_mass (float): Total mass of all passengers' baggage.
    """

    passenger_mass = n_passengers * m_passenger

    baggage_mass = n_passengers * m_baggage


    return passenger_mass, baggage_mass


# -----------------------------------------------------------------------
# Stateful/Framework Version
# -----------------------------------------------------------------------

def passenger_payload(State, Settings, System):

    n_passengers    = System.number_of_passengers

    passenger_mass, baggage_mass = func_payload(n_passengers)

    def _build_payload(payload: PhysicalComponent):

        if hasattr(payload, 'passengers'):
            payload.passengers.mass_properties.mass = passenger_mass
        else:
            passengers = PhysicalComponent(name='passengers')
            passengers.mass_properties.mass = passenger_mass
            payload.add_subcomponent(passengers)

        if hasattr(payload, 'baggage'):
            payload.baggage.mass_properties.mass = baggage_mass
        else:
            baggage = PhysicalComponent(name='baggage')
            baggage.mass_properties.mass = baggage_mass
            payload.add_subcomponent(baggage)

        payload.sum_mass

        return payload

    if hasattr(System, 'payload'):
        _payload = System.payload
        System.payload = _build_payload(_payload)
        System.sum_mass()
    else:
        _payload = PhysicalComponent(name='payload')
        payload = _build_payload(_payload)
        System.add_subcomponent(payload)

    return State, Settings, System
