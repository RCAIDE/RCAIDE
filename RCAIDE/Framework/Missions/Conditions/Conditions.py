# RCAIDE/Framework/Missions/Conditions/Conditions.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import chex
from dataclasses import field
import unittest

# package imports
import RNUMPY as rp
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Conditions
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class Conditions:
    """
    A class representing a set of conditions for engineering simulations.

    This class is designed to hold various attributes and methods related to
    simulation conditions, allowing for dynamic expansion of rows and packing
    of data into arrays.

    Attributes
    ----------
    name : str
        The name of the conditions set. Default is 'Conditions'.
    _number_of_rows : int
        The number of rows in the conditions set. Default is 1.
    row_size_adjustment : int
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

    tag: str = 'Conditions'

    _number_of_rows:        int = field(default=1, init=False)

    row_size_adjustment:    int = 0

    _attributes_frozen: bool = False

    def _get_subconditions(self):
        return [getattr(self, k) for k in vars(self) if isinstance(getattr(self, k), Conditions)]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            subconkeys = [k for k in vars(self) if isinstance(getattr(self, k), Conditions)]
            if key < len(subconkeys):
                setattr(self, subconkeys.index(key), value)
            else:
                setattr(self, str(key), value)
        else:
            setattr(self, key, value)

    def __post_init__(self):
        self.expand_rows(self._number_of_rows)
        # self.expand_columns(self._number_of_columns)
        self._attributes_frozen = True

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
          `self.row_size_adjustment` from the input `rows`.
        - Numpy arrays are resized to match the new number of rows while maintaining
          their original number of columns.
        - Nested Conditions objects are expanded recursively.

        """
        max_rows = int(rows) + self.row_size_adjustment
        rows = max(1, max_rows)
        self._number_of_rows = rows

        for k, v in vars(self).items():
            if isinstance(v, Conditions) and k != 'initials':
                v.expand_rows(rows)
            elif isinstance(v, rp.ndarray) and len(v.shape) <= 2 and k not in ["unknowns", "residuals"]:  # Scalar-valued arrays
                vars(self)[k] = rp.resize(v, (self._number_of_rows, v.shape[1]))
            elif isinstance(v, rp.ndarray) and k not in ["unknowns", "residuals"]:  # Vector-valued arrays
                new_shape = list(v.shape)
                new_shape[0] = self._number_of_rows
                vars(self)[k] = rp.resize(v, tuple(new_shape))

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
        return rp.concatenate([v.flatten() for v in vars(self).values() if isinstance(v, rp.ndarray)], axis=0)

    def unpack_array(self, array):
        """
        Unpacks a 1-dimensional array into numpy arrays, placing them in the object's attributes.

        Parameters
        ----------
        array : numpy.ndarray
            A 1-dimensional array containing all flattened numpy arrays.

        Returns
        -------
        None

        Notes
        -----
        - Only considers attributes that are numpy arrays.
        - The order of unpacking is determined by the order of attributes in vars(self).
        """
        i = 0
        for k, v in vars(self).items():
            if isinstance(v, rp.ndarray):
                vars(self)[k] = array[i:i+v.size].reshape(v.shape)
                i += v.size

# Overwrite Chex dataclass's getitem, setattr methods to allow indexing of subcomponents and semi-freeze attributes


def _conditions_getitem(self, item):
    if isinstance(item, slice | int):
        return self._get_subconditions()[item]
    elif isinstance(item, str):
        return self.__dict__[item.replace(' ', '_').lower()]
    else:
        raise TypeError(f"Conditions indices must be slices, integers or strings, not {type(item).__name__}")


def _conditions_setattr(self, key, value):
        if not hasattr(self, key) and self._attributes_frozen:
            allowable = [f for f in self.__dataclass_fields__.keys() if f[0] is not "_"]
            raise AttributeError(f"Cannot add new attribute {key!r} to {self.tag}. Allowable attributes:\n\t" + '\n\t'.join(allowable))
        super(Conditions, self).__setattr__(key, value)


def _conditions_iter(self):
    for sc in self.subcomponents:
        yield sc


Conditions.__getitem__ = _conditions_getitem
Conditions.__setattr__ = _conditions_setattr
Conditions.__iter__ = _conditions_iter


@chex.dataclass(kw_only=True)
class _ArrayConditions(Conditions):
    test_array: rp.ndarray = field(default_factory=lambda: rp.zeros((1, 1)))


class TestConditions(unittest.TestCase):
    def setUp(self):
        self.conditions = Conditions()

    def test_initial_state(self):
        self.assertEqual(self.conditions.tag, 'Conditions')
        self.assertEqual(self.conditions._number_of_rows, 1)
        self.assertEqual(self.conditions.row_size_adjustment, 0)

    def test_expand_rows_detailed(self):
        # Initialize Conditions
        self.conditions = Conditions()

        # Test initial state
        self.assertEqual(self.conditions._number_of_rows, 1)

        # Test basic expansion
        self.conditions.expand_rows(5)
        self.assertEqual(self.conditions._number_of_rows, 5)

        # Test expansion with row_size_adjustment
        self.conditions.row_size_adjustment = -2
        self.conditions.expand_rows(10)
        self.assertEqual(self.conditions._number_of_rows, 8)  # 10 - 2 = 8

        # Test with numpy arrays
        self.conditions.array1 = rp.zeros((1, 3))
        self.conditions.array2 = rp.ones((2, 2))
        self.conditions.expand_rows(12)
        self.assertEqual(self.conditions._number_of_rows, 10)  # 12 - 2 = 10
        self.assertEqual(self.conditions.array1.shape, (10, 3))
        self.assertEqual(self.conditions.array2.shape, (10, 2))

        # Test preserving data in numpy arrays
        original_data = rp.array([[1, 2, 3], [4, 5, 6]])
        self.conditions.data_array = original_data
        self.conditions.expand_rows(15)
        np.testing.assert_array_equal(self.conditions.data_array[:2, :], original_data)
        self.assertEqual(self.conditions.data_array.shape, (13, 3))  # 15 - 2 = 13

        # Test with nested Conditions
        self.conditions.nested = _ArrayConditions()
        self.conditions.nested.test_array = rp.zeros((1, 4))
        self.conditions.expand_rows(20)
        self.assertEqual(self.conditions._number_of_rows, 18)  # 20 - 2 = 18
        self.assertEqual(self.conditions.nested.test_array.shape, (18, 4))

        # Test with zero or negative input
        self.conditions.expand_rows(0)
        self.assertEqual(self.conditions._number_of_rows, 1)
        self.conditions.expand_rows(-5)
        self.assertEqual(self.conditions._number_of_rows, 1)

    def test_expand_columns(self):
        # Initialize Conditions with a numpy array
        self.conditions = _ArrayConditions()
        self.conditions.test_array = rp.zeros((1, 2))

        # Test expanding columns
        self.conditions.expand_columns(4)
        self.assertEqual(self.conditions.test_array.shape, (1, 4))

        # Test that existing data is preserved
        self.conditions.test_array[:, :2] = 1
        self.conditions.expand_columns(6)
        np.testing.assert_array_equal(self.conditions.test_array[:, :2], rp.ones((1, 2)))
        self.assertEqual(self.conditions.test_array.shape, (1, 6))

    def test_expand_columns_with_nested_conditions(self):
        # Initialize nested Conditions
        self.conditions = _ArrayConditions()
        self.conditions.nested = _ArrayConditions()
        self.conditions.test_array = rp.zeros((1, 2))
        self.conditions.nested.test_array = rp.zeros((1, 2))

        # Test expanding columns in nested structure
        self.conditions.expand_columns(4)
        self.assertEqual(self.conditions.test_array.shape, (1, 4))
        self.assertEqual(self.conditions.nested.test_array.shape, (1, 4))

    def test_expand_columns_reduce(self):
        # Initialize Conditions with a larger array
        self.conditions = _ArrayConditions()
        self.conditions.test_array = rp.ones((1, 5))

        # Test reducing columns
        self.conditions.expand_columns(3)
        self.assertEqual(self.conditions.test_array.shape, (1, 3))
        np.testing.assert_array_equal(self.conditions.test_array, rp.ones((1, 3)))

    def test_pack_array(self):
        self.conditions.array1 = rp.array([1, 2, 3])
        self.conditions.array2 = rp.array([4, 5, 6])
        packed = self.conditions.pack_array()
        np.testing.assert_array_equal(packed, rp.array([1, 2, 3, 4, 5, 6]))


if __name__ == '__main__':
    unittest.main()
