import equinox as eqx
from RCAIDE.Framework import Process, ProcessStep
from RCAIDE.Library.Methods.Mass import Transport as Mass

from RCAIDE.Framework.Methods.Mass.Energy import Jet_Mass_from_SLS


def _build_transport_steps() -> tuple[ProcessStep, ...]:
    """Builds the static pipeline of turbofan cycle analysis steps."""
    return (
        ProcessStep(tag='Propulsion Mass', function=Jet_Mass_from_SLS),
        ProcessStep(tag='Passenger & Payload Mass', function=Mass.passenger_payload),
        ProcessStep(tag='Operating System Mass', function=Mass.operating_systems),
        ProcessStep(tag='Main Wing Mass', function=Mass.segmented_main_wing),
        ProcessStep(tag='Horizontal Tail Mass', function=Mass.horizontal_tail),
        ProcessStep(tag='Vertical Tail Mass', function=Mass.vertical_tail),
        ProcessStep(tag='Fuselage Mass', function=Mass.fuselage),
        ProcessStep(tag='Landing Gear', function=Mass.landing_gear),
    )

class Transport(Process):

    tag: str = eqx.field(static=True, default="Transport Mass Analysis")
    steps: tuple[ProcessStep, ...] = eqx.field(default_factory=_build_transport_steps)


        