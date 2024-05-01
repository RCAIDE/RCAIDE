# RCAIDE/Library/Attributes/AC_Classes/BusinessJet.py
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
# Business Jet Aircraft Attributes
#-------------------------------------------------------------------------------

@dataclass
class BusinessJet:
    """
    Attributes for Private/Business Jet Aircraft
    """

    #---------------------------------MASSES------------------------------------

    # Operating items, incl. unusuable fuel, engine oil, passenger service, etc.
    operating_items_mass            : float = field(init=False,
                                                    default=17.0*Units.lbm)
    # Instruments
    instruments_mass                : float = field(init=False,
                                                    default=800.0*Units.lbm)
    # Avionics
    avionics_mass                   : float = field(init=False,
                                                    default=900.0*Units.lbm)
    # Supplemental Furnishings Per Seat
    supplemental_furnishings_mass   : float = field(init=False,
                                                    default=0.0*Units.lbm)

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