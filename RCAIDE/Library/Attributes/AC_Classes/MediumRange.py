# RCAIDE/Library/Attributes/AC_Classes/MediumRange.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created:  May 2024, J. Smart
# Modified:

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from Legacy.trunk.S.Core import Units
from dataclasses import dataclass, field

#-------------------------------------------------------------------------------
# Medium Range Aircraft Attributes
#-------------------------------------------------------------------------------

@dataclass
class MediumRange:
    """
    Attributes for Medium Range Transport Aircraft
    """

    #---------------------------------MASSES------------------------------------

    # Operating items, incl. unusuable fuel, engine oil, passenger service, etc.
    operating_items_mass            : float = field(init=False,
                                                    default=028.0*Units.lbm)
    # Instruments
    instruments_mass                : float = field(init=False,
                                                    default=000.0*Units.lbm)
    # Avionics
    avionics_mass                   : float = field(init=False,
                                                    default=000.0*Units.lbm)
    # Supplemental Furnishings Per Seat
    supplemental_furnishings_mass   : float = field(init=False,
                                                    default=000.0*Units.lbm)

    # -----------------------------CONTROL TYPE----------------------------------

    full_powered_control            : bool = field(init=True,
                                                   default=True)

    partially_powered_control       : bool = field(init=True,
                                                   default=False)

    full_aerodynamic_control        : bool = field(init=True,
                                                   default=False)

    # -------------------------------POST-INIT-----------------------------------
    def __post_init__(self):
        # Check that only one control type is selected

        assert (self.full_powered_control +
                self.partially_powered_control +
                self.full_aerodynamic_control) == 1, \
            ("Only one control type can be selected when creating an "
             "aircraft class instance")