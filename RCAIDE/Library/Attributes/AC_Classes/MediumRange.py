# RCAIDE/Library/Attributes/AC_Classes/MediumRange.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created:  May 2024, J. Smart
# Modified:

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from pint import UnitRegistry
Units = UnitRegistry()
from dataclasses import dataclass, field

#-------------------------------------------------------------------------------
# Medium Range Aircraft Attributes
#-------------------------------------------------------------------------------

fixed_masses = {'fixed': True,
                'per_seat': False}

per_seat_masses = {'fixed': False,
                   'per_seat': True}


@dataclass
class MediumRange:

    """
    Attributes for Private/Business Jet Aircraft
    """

    #-------------------------------FIXED MASSES--------------------------------

    # Flight Crew (3x @ 240 lbm)
    flight_crew_mass               : float = field(default=720.0 * Units.lb, metadata=fixed_masses)

    # Flight Attendants (5x @ 210 lbm)
    flight_attendants_mass         : float = field(default=1050.0 * Units.lb, metadata=fixed_masses)

    # Instruments
    instruments_mass                : float = field(default=800.0 * Units.lb, metadata=fixed_masses)
    # Avionics
    avionics_mass                   : float = field(default=900.0 * Units.lb, metadata=fixed_masses)

    # Auxiliary Power Unit
    apu_mass                        : float = field(default=154.0 * Units.lb, metadata=fixed_masses)

    # Flight Controls (Sized from Empennage in Analysis)
    flight_control_mass             : float = field(default=0.0 * Units.lb, metadata=fixed_masses)

    # Hydraulics and Pneumatics (Sized from Empennage in Analysis)
    hyd_pnu_mass                    : float = field(default=0.0 * Units.lb, metadata=fixed_masses)

    #-------------------------------PER SEAT MASSES-----------------------------

    # Operating items, incl. unusuable fuel, engine oil, passenger service, etc.
    operating_items_mass            : float = field(default=28.0*Units.lb, metadata=per_seat_masses)

    # Electrical Equipment
    electrical_equipment_mass       : float = field(default=13.0*Units.lb, metadata=per_seat_masses)

    # Environmental Control/Anti-Ice
    environmental_mass              : float = field(default=15.0*Units.lb, metadata=per_seat_masses)

    # Supplemental Furnishings Per Seat
    furnishings_mass                : float = field(default=89.663*Units.lb, metadata=per_seat_masses)

    # -----------------------------CONTROL TYPE----------------------------------

    full_powered_control            : bool = field(default=True)
    partially_powered_control       : bool = field(default=False)
    full_aerodynamic_control        : bool = field(default=False)

    # -------------------------------POST-INIT-----------------------------------
    def __post_init__(self):
        # Check that only one control type is selected

        assert (self.full_powered_control +
                self.partially_powered_control +
                self.full_aerodynamic_control) == 1, \
            ("Only one control type can be selected when creating an "
             "aircraft class instance")

if __name__ == '__main__':
    A = MediumRange()
    print(A)