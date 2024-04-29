# payload.py
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

def func_payload(n_passengers,
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

def payload(State, Settings, System):

    n_passengers    = System.number_of_passengers

    passenger_mass, baggage_mass = func_payload(n_passengers)

    if not hasattr(System, 'payload'):
        System.payload = PhysicalComponent()

    if not hasattr(System.payload, 'passengers'):
        System.payload.passengers = PhysicalComponent()
    System.payload.passengers.mass = passenger_mass

    if not hasattr(System.payload, 'baggage'):
        System.payload.baggage = PhysicalComponent()
    System.payload.baggage.mass = baggage_mass

    if not hasattr(System.payload, 'cargo'):
        System.payload.cargo = PhysicalComponent()

    System.payload.sum_mass()

    return State, Settings, System
