# RCAIDE/Framework/Missions/Conditions/Aerodynamics.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import chex
from dataclasses import field
import unittest

# package imports
import RNUMPY as rp

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Aerodynamics
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class AerodynamicAngles(Conditions):
    """
    A class to represent aerodynamic angles.

    This class inherits from Conditions and uses dataclass with keyword-only arguments.

    Attributes
    ----------
    name : str
        The name of the aerodynamic angles set. Default is 'Aerodynamic Angles'.
    alpha : rp.ndarray
        The angle of attack. Default is a 1x1 array of zeros.
    beta : rp.ndarray
        The sideslip angle. Default is a 1x1 array of zeros.
    phi : rp.ndarray
        The bank angle. Default is a 1x1 array of zeros.
    """

    # Attribute         Type        Default Value
    tag:                str         = 'Aerodynamic Angles'

    alpha:              rp.ndarray      = field(default_factory=lambda: rp.zeros((1, 1)))
    beta:               rp.ndarray      = field(default_factory=lambda: rp.zeros((1, 1)))
    phi:                rp.ndarray      = field(default_factory=lambda: rp.zeros((1, 1)))


@chex.dataclass(kw_only=True)
class LiftCoefficients(Conditions):
    """
    A class to represent lift coefficients for aerodynamic analysis.

    This class inherits from Conditions and uses dataclass with keyword-only arguments.

    Attributes
    ----------
    name : str
        The name of the lift coefficients set. Default is 'Lift Coefficients'.
    total : rp.ndarray
        The total lift coefficient. Default is a 1x1 array of zeros.
    inviscid_wings : Conditions
        Lift coefficients for inviscid wing calculations. Initialized as a Conditions object with name 'Inviscid Wings'.
    compressible_wings : Conditions
        Lift coefficients for compressible wing calculations. Initialized as a Conditions object with name 'Compressible Wings'.
    """

    # Attribute     Type            Default Value
    tag:            str             = 'Lift Coefficients'

    total:          rp.ndarray      = field(default_factory=lambda: rp.zeros((1, 1)))

    inviscid:       Conditions      = field(default_factory=lambda: Conditions(tag='Inviscid Bodies'))
    compressible:   Conditions      = field(default_factory=lambda: Conditions(tag='Compressible Bodies'))


@chex.dataclass(kw_only=True)
class InducedDrag(Conditions):
    """
    A class to represent induced drag for aerodynamic analysis.

    This class inherits from Conditions and uses dataclass with keyword-only arguments.

    Attributes
    ----------
    name : str
        The name of the induced drag set. Default is 'Induced Drag'.
    total : rp.ndarray
        The total induced drag coefficient. Default is a 1x1 array of zeros.
    inviscid_wings : Conditions
        Induced drag coefficients for inviscid wing calculations. Initialized as a Conditions object with name 'Inviscid Wings'.
    """

    # Attribute         Type            Default Value
    tag:                str             = 'Induced Drag'

    total:              rp.ndarray      = field(default_factory=lambda: rp.zeros((1, 1)))

    inviscid_wings:     Conditions      = field(default_factory=lambda: Conditions(tag='Inviscid Wings'))



@chex.dataclass(kw_only=True)
class DragCoefficients(Conditions):
    """
    A class to represent drag coefficients for aerodynamic analysis.

    This class inherits from Conditions and uses dataclass with keyword-only arguments.

    Attributes
    ----------
    name : str
        The name of the drag coefficients set. Default is 'Drag Coefficients'.
    total : rp.ndarray
        The total drag coefficient. Default is a 1x1 array of zeros.
    parasite : Conditions
        Parasite drag coefficients. Initialized as a Conditions object with name 'Parasite Drag'.
    compressible : Conditions
        Compressible drag coefficients. Initialized as a Conditions object with name 'Compressible Drag'.
    miscellaneous : Conditions
        Miscellaneous drag coefficients. Initialized as a Conditions object with name 'Miscellaneous Drag'.
    spoiler : Conditions
        Spoiler drag coefficients. Initialized as a Conditions object with name 'Spoiler Drag'.
    induced : InducedDrag
        Induced drag coefficients. Initialized as an InducedDrag object.
    """

    # Attribute         Type            Default Value
    tag:                str             = 'Drag Coefficients'

    total:              rp.ndarray      = field(default_factory=lambda: rp.zeros((1, 1)))

    parasite:           Conditions      = field(default_factory=lambda: Conditions(tag='Parasite Drag'))
    compressible:       Conditions      = field(default_factory=lambda: Conditions(tag='Compressible Drag'))
    miscellaneous:      Conditions      = field(default_factory=lambda: Conditions(tag='Miscellaneous Drag'))
    spoiler:            Conditions      = field(default_factory=lambda: Conditions(tag='Spoiler Drag'))

    induced:            InducedDrag     = field(default_factory=lambda: InducedDrag())


@chex.dataclass(kw_only=True)
class AerodynamicCoefficients(Conditions):
    """
    A class to represent aerodynamic coefficients for lift and drag.

    This class inherits from Conditions and uses dataclass with keyword-only arguments.

    Attributes
    ----------
    name : str
        The name of the aerodynamic coefficients set. Default is 'Aerodynamic Coefficients'.
    lift : LiftCoefficients
        An instance of LiftCoefficients representing the lift-related aerodynamic coefficients.
    drag : DragCoefficients
        An instance of DragCoefficients representing the drag-related aerodynamic coefficients.
    """

    # Attribute         Type            Default Value
    tag:                str             = 'Aerodynamic Coefficients'

    lift:  LiftCoefficients  = field(default_factory=lambda: LiftCoefficients())
    drag:  DragCoefficients  = field(default_factory=lambda: DragCoefficients())


@chex.dataclass(kw_only=True)
class AerodynamicsConditions(Conditions):
    """
    A class representing aerodynamic conditions for a flight simulation.

    This class inherits from Conditions and uses dataclass with keyword-only arguments.
    It encapsulates aerodynamic angles and coefficients for comprehensive aerodynamic analysis.

    Attributes
    ----------
    name : str
        The name of the aerodynamic conditions set. Default is 'Aerodynamics'.
    angles : AerodynamicAngles
        An instance of AerodynamicAngles representing the aerodynamic angles (alpha, beta, phi).
        Default is a new AerodynamicAngles object.
    coefficients : AerodynamicCoefficients
        An instance of AerodynamicCoefficients representing lift and drag coefficients.
        Default is a new AerodynamicCoefficients object.
    """

    # Attribute     Type                    Default Value
    tag:            str                     = 'Aerodynamics'

    angles:         AerodynamicAngles       = field(default_factory=lambda: AerodynamicAngles())

    coefficients:   AerodynamicCoefficients = field(default_factory=lambda: AerodynamicCoefficients())


# ----------------------------------------------------------------------------------------------------------------------
# Unit Tests
# ----------------------------------------------------------------------------------------------------------------------

class TestAerodynamics(unittest.TestCase):

    def test_aerodynamic_angles(self):
        angles = AerodynamicAngles()
        self.assertEqual(angles.tag, 'Aerodynamic Angles')
        self.assertTrue(rp.array_equal(angles.alpha, rp.zeros((1, 1))))
        self.assertTrue(rp.array_equal(angles.beta, rp.zeros((1, 1))))
        self.assertTrue(rp.array_equal(angles.phi, rp.zeros((1, 1))))

    def test_lift_coefficients(self):
        lift = LiftCoefficients()
        self.assertEqual(lift.tag, 'Lift Coefficients')
        self.assertTrue(rp.array_equal(lift.total, rp.zeros((1, 1))))
        self.assertEqual(lift.inviscid_wings.tag, 'Inviscid Wings')
        self.assertEqual(lift.compressible_wings.tag, 'Compressible Wings')

    def test_induced_drag(self):
        induced = InducedDrag()
        self.assertEqual(induced.tag, 'Induced Drag')
        self.assertTrue(rp.array_equal(induced.total, rp.zeros((1, 1))))
        self.assertEqual(induced.inviscid_wings.tag, 'Inviscid Wings')

    def test_drag_coefficients(self):
        drag = DragCoefficients()
        self.assertEqual(drag.tag, 'Drag Coefficients')
        self.assertTrue(rp.array_equal(drag.total, rp.zeros((1, 1))))
        self.assertEqual(drag.parasite.tag, 'Parasite Drag')
        self.assertEqual(drag.compressible.tag, 'Compressible Drag')
        self.assertEqual(drag.miscellaneous.tag, 'Miscellaneous Drag')
        self.assertEqual(drag.spoiler.tag, 'Spoiler Drag')
        self.assertIsInstance(drag.induced, InducedDrag)

    def test_aerodynamic_coefficients(self):
        coeff = AerodynamicCoefficients()
        self.assertEqual(coeff.tag, 'Aerodynamic Coefficients')
        self.assertIsInstance(coeff.lift, LiftCoefficients)
        self.assertIsInstance(coeff.drag, DragCoefficients)

    def test_aerodynamics_conditions(self):
        cond = AerodynamicsConditions()
        self.assertEqual(cond.tag, 'Aerodynamics')
        self.assertIsInstance(cond.angles, AerodynamicAngles)
        self.assertIsInstance(cond.coefficients, AerodynamicCoefficients)


if __name__ == '__main__':
    unittest.main()
