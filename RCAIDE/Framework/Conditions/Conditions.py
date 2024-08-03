# RCAIDE/Framework/Core/State.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field

# package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Conditions
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class Conditions:

    name: str = 'Conditions'

    number_of_rows: int = 1
    adjustment_from_parent: int = 0

    def __post_init__(self):
        self.expand_rows(self.number_of_rows)

    def expand_rows(self, rows: int, override: bool = False):

        self.number_of_rows = np.maximum(rows - self.adjustment_from_parent, 0)

        for k, v in vars(self).items():
            if isinstance(v, Conditions):
                v.expand_rows(rows, override=override)
            elif isinstance(v, np.ndarray):
                vars(self)[k] = np.resize(v, (self.number_of_rows, v.shape[1]))
