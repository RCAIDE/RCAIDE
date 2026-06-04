# RCAIDE/Library/Attributes/AC_Classes.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created:  May 2024, J. Smart
# Modified: Feb 2026, J. Smart

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from typing import Literal

# package imports
import equinox as eqx

# RCAIDE imports
from RCAIDE.Library import Units

#-------------------------------------------------------------------------------
# Aircraft Classes
#-------------------------------------------------------------------------------

ControlType = Literal["full_powered", "partially_powered", "full_aerodynamic"]

class FixedMasses(eqx.Module):

    flight_crew_mass            : float = eqx.field(static=True, default=0.)
    flight_attendants_mass      : float = eqx.field(static=True, default=0.)
    instruments_mass            : float = eqx.field(static=True, default=0.)
    avionics_mass               : float = eqx.field(static=True, default=0.)
    apu_mass                    : float = eqx.field(static=True, default=0.)
    flight_control_mass         : float = eqx.field(static=True, default=0.)
    hyd_pnu_mass                : float = eqx.field(static=True, default=0.)

class PerSeatMasses(eqx.Module):

    operating_items_mass        : float = eqx.field(static=True, default=0.)
    electrical_equipment_mass   : float = eqx.field(static=True, default=0.)
    environmental_mass          : float = eqx.field(static=True, default=0.)
    furnishings_mass            : float = eqx.field(static=True, default=0.)

class AircraftClass(eqx.Module):

    tag             : str           = eqx.field(static=True, default="Aircraft Class")

    control_type    : ControlType   = eqx.field(static=True, default="full_powered")

    fixed_masses    : FixedMasses   = eqx.field(static=True, default_factory=FixedMasses)
    per_seat_masses : PerSeatMasses = eqx.field(static=True, default_factory=PerSeatMasses)

#-------------------------------------------------------------------------------
# Business Jet
#-------------------------------------------------------------------------------

def _BizJetFixed():
    return FixedMasses(
        flight_crew_mass        = 480. * Units.lbm,
        flight_attendants_mass  = 210. * Units.lbm,
        instruments_mass        = 100. * Units.lbm,
        avionics_mass           = 300. * Units.lbm,
        apu_mass                = 154. * Units.lbm,
        flight_control_mass     = 0. * Units.lbm,
        hyd_pnu_mass            = 0. * Units.lbm
    )

def _BizJetPer():
    return PerSeatMasses(
        operating_items_mass        = 28. * Units.lbm,
        electrical_equipment_mass   = 13. * Units.lbm,
        environmental_mass          = 15. * Units.lbm,
        furnishings_mass            = 89.663 * Units.lbm,
    )

class BusinessJet(AircraftClass):

    tag             : str           = eqx.field(static=True, default="Business Jet")

    fixed_masses    : FixedMasses   = eqx.field(static=True, default_factory=_BizJetFixed)
    per_seat_masses : PerSeatMasses = eqx.field(static=True, default_factory=_BizJetPer)

#-------------------------------------------------------------------------------
# Medium Range
#-------------------------------------------------------------------------------

def _MRFixed():
    return FixedMasses(
        flight_crew_mass        = 720. * Units.lbm,
        flight_attendants_mass  = 1050. * Units.lbm,
        instruments_mass        = 800. * Units.lbm,
        avionics_mass           = 900. * Units.lbm,
        apu_mass                = 154. * Units.lbm,
        flight_control_mass     = 0. * Units.lbm,
        hyd_pnu_mass            = 0. * Units.lbm
    )

def _MRPer():
    return PerSeatMasses(
        operating_items_mass        = 28. * Units.lbm,
        electrical_equipment_mass   = 13. * Units.lbm,
        environmental_mass          = 15. * Units.lbm,
        furnishings_mass            = 89.663 * Units.lbm,
    )

class MediumRange(AircraftClass):

    tag             : str           = eqx.field(static=True, default="Medium Range Jet")

    fixed_masses    : FixedMasses   = eqx.field(static=True, default_factory=_MRFixed)
    per_seat_masses : PerSeatMasses = eqx.field(static=True, default_factory=_MRPer)
