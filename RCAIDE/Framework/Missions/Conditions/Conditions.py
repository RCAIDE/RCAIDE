# RCAIDE/Framework/Missions/Conditions/Conditions.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass
import unittest

# package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Conditions
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class Conditions:
    """
    A class representing a set of conditions for aerospace simulations.

    This class is designed to hold various attributes and methods related to
    simulation conditions, allowing for dynamic expansion of rows and packing
    of data into arrays.

    Attributes
    ----------
    name : str
        The name of the conditions set. Default is 'Conditions'.
    number_of_rows : int
        The number of rows in the conditions set. Default is 1.
    adjustment_from_parent : int
        An adjustment factor for row calculations. Default is 0.

    Methods
    -------
    __post_init__()
        Initializes the object after creation, expanding rows as needed.
    expand_rows(rows: int, override: bool = False)
        Expands or resizes the number of rows in the object and its attributes.
    pack_array()
        Packs all numpy arrays in the object into a single flattened array.

    Notes
    -----
    - This class is implemented as a dataclass with keyword-only arguments.
    - It's designed to work with nested Conditions objects and numpy arrays.
    """

    name: str = 'Conditions'

    number_of_rows: int = 1
    adjustment_from_parent: int = 0

    def __post_init__(self):
        self.expand_rows(self.number_of_rows)

    def expand_rows(self, rows: int):
        """
        Expand or resize the number of rows in the Conditions object and its attributes.

        This method adjusts the number of rows in the Conditions object and recursively
        expands any nested Conditions objects. It also resizes numpy arrays to match
        the new number of rows.

        Parameters
        ----------
        rows : int
            The target number of rows to expand to.

        Returns
        -------
        None

        Notes
        -----
        - The actual number of rows after expansion is determined by subtracting
          `self.adjustment_from_parent` from the input `rows`.
        - Numpy arrays are resized to match the new number of rows while maintaining
          their original number of columns.
        - Nested Conditions objects are expanded recursively.

        """

        self.number_of_rows = np.maximum(rows - self.adjustment_from_parent, 0)

        for k, v in vars(self).items():
            if isinstance(v, Conditions):
                v.expand_rows(rows)
            elif isinstance(v, np.ndarray):
                vars(self)[k] = np.resize(v, (self.number_of_rows, v.shape[1]))

    def expand_columns

    def pack_array(self):
        """
        Pack all numpy arrays in the Conditions object into a single flattened array.

        This method concatenates all numpy arrays found in the object's attributes
        into a single 1-dimensional array.

        Returns
        -------
        numpy.ndarray
            A 1-dimensional array containing all flattened numpy arrays from the object's attributes.

        Notes
        -----
        - Only considers attributes that are numpy arrays.
        - The order of concatenation is determined by the order of attributes in vars(self).
        """
        return np.concatenate([v.flatten() for v  in vars(self).values() if isinstance(v, np.ndarray)], axis=0)


class TestConditions(unittest.TestCase):
    def setUp(self):
        self.conditions = Conditions()

    def test_initial_state(self):
        self.assertEqual(self.conditions.name, 'Conditions')
        self.assertEqual(self.conditions.number_of_rows, 1)
        self.assertEqual(self.conditions.adjustment_from_parent, 0)

    def test_expand_rows(self):
        self.conditions.expand_rows(5)
        self.assertEqual(self.conditions.number_of_rows, 5)

    def test_expand_rows_with_adjustment(self):
        self.conditions.adjustment_from_parent = 2
        self.conditions.expand_rows(5)
        self.assertEqual(self.conditions.number_of_rows, 3)

    def test_expand_rows_with_numpy_array(self):
        self.conditions.test_array = np.zeros((1, 3))
        self.conditions.expand_rows(5)
        self.assertEqual(self.conditions.test_array.shape, (5, 3))

    def test_pack_array(self):
        self.conditions.array1 = np.array([1, 2, 3])
        self.conditions.array2 = np.array([4, 5, 6])
        packed = self.conditions.pack_array()
        np.testing.assert_array_equal(packed, np.array([1, 2, 3, 4, 5, 6]))


if __name__ == '__main__':
    unittest.main()
