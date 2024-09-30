# RCAIDE/Framework/Missions/Conditions/Aerodynamics.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field
import unittest

# package imports
import numpy as np

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Aerodynamics
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class AerodynamicAngles(Conditions):
    """
    A class to represent aerodynamic angles.

    This class inherits from Conditions and uses dataclass with keyword-only arguments.

    Attributes
    ----------
    name : str
        The name of the aerodynamic angles set. Default is 'Aerodynamic Angles'.
    alpha : np.ndarray
        The angle of attack. Default is a 1x1 array of zeros.
    beta : np.ndarray
        The sideslip angle. Default is a 1x1 array of zeros.
    phi : np.ndarray
        The bank angle. Default is a 1x1 array of zeros.
    """

    # Attribute         Type        Default Value
    name:               str         = 'Aerodynamic Angles'

    alpha:              np.ndarray      = field(default_factory=lambda: np.zeros((1, 1)))
    beta:               np.ndarray      = field(default_factory=lambda: np.zeros((1, 1)))
    phi:                np.ndarray      = field(default_factory=lambda: np.zeros((1, 1)))


@dataclass(kw_only=True)
class LiftCoefficients(Conditions):
    """
    A class to represent lift coefficients for aerodynamic analysis.

    This class inherits from Conditions and uses dataclass with keyword-only arguments.

    Attributes
    ----------
    name : str
        The name of the lift coefficients set. Default is 'Lift Coefficients'.
    total : np.ndarray
        The total lift coefficient. Default is a 1x1 array of zeros.
    inviscid_wings : Conditions
        Lift coefficients for inviscid wing calculations. Initialized as a Conditions object with name 'Inviscid Wings'.
    compressible_wings : Conditions
        Lift coefficients for compressible wing calculations. Initialized as a Conditions object with name 'Compressible Wings'.
    """

    # Attribute         Type            Default Value
    name:               str             = 'Lift Coefficients'

    total:              np.ndarray      = field(default_factory=lambda: np.zeros((1, 1)))

    inviscid_wings:     Conditions      = Conditions(name='Inviscid Wings')
    compressible_wings: Conditions      = Conditions(name='Compressible Wings')


@dataclass(kw_only=True)
class InducedDrag(Conditions):
    """
    A class to represent induced drag for aerodynamic analysis.

    This class inherits from Conditions and uses dataclass with keyword-only arguments.

    Attributes
    ----------
    name : str
        The name of the induced drag set. Default is 'Induced Drag'.
    total : np.ndarray
        The total induced drag coefficient. Default is a 1x1 array of zeros.
    inviscid_wings : Conditions
        Induced drag coefficients for inviscid wing calculations. Initialized as a Conditions object with name 'Inviscid Wings'.
    """

    # Attribute         Type            Default Value
    name:               str             = 'Induced Drag'

    total:              np.ndarray      = field(default_factory=lambda: np.zeros((1, 1)))

    inviscid_wings:     Conditions      = Conditions(name='Inviscid Wings')



@dataclass(kw_only=True)
class DragCoefficients(Conditions):
    """
    A class to represent drag coefficients for aerodynamic analysis.

    This class inherits from Conditions and uses dataclass with keyword-only arguments.

    Attributes
    ----------
    name : str
        The name of the drag coefficients set. Default is 'Drag Coefficients'.
    total : np.ndarray
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
    name:               str             = 'Drag Coefficients'

    total:              np.ndarray      = field(default_factory=lambda: np.zeros((1, 1)))

    parasite:           Conditions      = field(default_factory=lambda: Conditions(name='Parasite Drag'))
    compressible:       Conditions      = field(default_factory=lambda: Conditions(name='Compressible Drag'))
    miscellaneous:      Conditions      = field(default_factory=lambda: Conditions(name='Miscellaneous Drag'))
    spoiler:            Conditions      = field(default_factory=lambda: Conditions(name='Spoiler Drag'))

    induced:            InducedDrag     = field(default_factory=lambda: InducedDrag())


@dataclass(kw_only=True)
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
    name:               str             = 'Aerodynamic Coefficients'

    lift:  LiftCoefficients  = field(default_factory=lambda: LiftCoefficients())
    drag:  DragCoefficients  = field(default_factory=lambda: DragCoefficients())


@dataclass(kw_only=True)
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
    name:           str                     = 'Aerodynamics'

    angles:         AerodynamicAngles       = field(default_factory=lambda: AerodynamicAngles())

    coefficients:   AerodynamicCoefficients = field(default_factory=lambda: AerodynamicCoefficients())


# ----------------------------------------------------------------------------------------------------------------------
# Unit Tests
# ----------------------------------------------------------------------------------------------------------------------

class TestAerodynamics(unittest.TestCase):

    def test_aerodynamic_angles(self):
        angles = AerodynamicAngles()
        self.assertEqual(angles.name, 'Aerodynamic Angles')
        self.assertTrue(np.array_equal(angles.alpha, np.zeros((1, 1))))
        self.assertTrue(np.array_equal(angles.beta, np.zeros((1, 1))))
        self.assertTrue(np.array_equal(angles.phi, np.zeros((1, 1))))

    def test_lift_coefficients(self):
        lift = LiftCoefficients()
        self.assertEqual(lift.name, 'Lift Coefficients')
        self.assertTrue(np.array_equal(lift.total, np.zeros((1, 1))))
        self.assertEqual(lift.inviscid_wings.name, 'Inviscid Wings')
        self.assertEqual(lift.compressible_wings.name, 'Compressible Wings')

    def test_induced_drag(self):
        induced = InducedDrag()
        self.assertEqual(induced.name, 'Induced Drag')
        self.assertTrue(np.array_equal(induced.total, np.zeros((1, 1))))
        self.assertEqual(induced.inviscid_wings.name, 'Inviscid Wings')

    def test_drag_coefficients(self):
        drag = DragCoefficients()
        self.assertEqual(drag.name, 'Drag Coefficients')
        self.assertTrue(np.array_equal(drag.total, np.zeros((1, 1))))
        self.assertEqual(drag.parasite.name, 'Parasite Drag')
        self.assertEqual(drag.compressible.name, 'Compressible Drag')
        self.assertEqual(drag.miscellaneous.name, 'Miscellaneous Drag')
        self.assertEqual(drag.spoiler.name, 'Spoiler Drag')
        self.assertIsInstance(drag.induced, InducedDrag)

    def test_aerodynamic_coefficients(self):
        coeff = AerodynamicCoefficients()
        self.assertEqual(coeff.name, 'Aerodynamic Coefficients')
        self.assertIsInstance(coeff.lift, LiftCoefficients)
        self.assertIsInstance(coeff.drag, DragCoefficients)

    def test_aerodynamics_conditions(self):
        cond = AerodynamicsConditions()
        self.assertEqual(cond.name, 'Aerodynamics')
        self.assertIsInstance(cond.angles, AerodynamicAngles)
        self.assertIsInstance(cond.coefficients, AerodynamicCoefficients)


if __name__ == '__main__':
    unittest.main()
