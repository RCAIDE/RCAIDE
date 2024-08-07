# RCAIDE/Framework/Process.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import dataclasses
from dataclasses import dataclass, field
from typing      import Callable, Iterable

# package imports
import numpy as np
import pandas as pd

# RCAIDE imports
from RCAIDE.Framework import State, Settings, System


# ----------------------------------------------------------------------------------------------------------------------
#  Argument Passer
# ----------------------------------------------------------------------------------------------------------------------


def _args_passer(*args, **kwargs):
    return *args, kwargs


@dataclass(kw_only=True)
class ProcessStep:

    #---------------------------------------------------------------------------
    # Process Step Parameters
    #---------------------------------------------------------------------------

    # Required Parameters

    function:       Callable    = _args_passer

    # Optional Parameters

    name:           str         = "Process Step"
    last_result:    object      = None

    state:          State       = State()
    settings:       Settings    = Settings()
    system:         System      = System()

    def __call__(self):

        framework_args = (self.state, self.settings, self.system)

        return self.function(*framework_args)


def _create_details():

    details = pd.DataFrame(
        columns=['Name',
                 'Function',
                 'Last Result']
    )

    return details


@dataclass(kw_only=True)
class Process:

    name:               str                 = "Process"

    steps:              list[ProcessStep]   = field(default_factory=list)
    details:            pd.DataFrame        = field(default_factory=_create_details)

    step:               int                 = 0
    initial_step:       int                 = 0

    initial_state:      State               = State()
    initial_settings:   Settings            = Settings()
    initial_system:     System              = System()

    state:              State               = None
    settings:           Settings            = None
    system:             System              = None

    def __getitem__(self, item):
        return self.steps[item]

    def __delitem__(self, key):
        del self.steps[key]
        self.update_details()

    def __call__(self, *args, **kwargs):

        self.update_details()

        framework_args = (self.initial_state,
                          self.initial_settings,
                          self.initial_system)

        for index, step in enumerate(self.steps[self.initial_step:-1]):
            framework_args = step(*framework_args)
            self.steps[index].last_result = framework_args
            self.details.at[index, 'Last Result'] = framework_args

        results = self.steps[-1](*framework_args)
        self.details.at[len(self.steps)-1, 'Last Result'] = results

        return results

    def append(self, step: ProcessStep):

        self.steps.append(step)
        self.update_details()

        return None

    def clear(self):

        self.steps.clear()
        self.update_details()

        return None

    def copy(self):
        return dataclasses.replace(self)

    def count(self, step: ProcessStep):
        return self.steps.count(step)

    def extend(self, extension: Iterable):
        self.steps.extend(extension)
        self.update_details()

        return None

    def _index_name(self, name: str):

        names = [step.name for step in self.steps]
        index = names.index(name)

        return index

    def _index_function(self, function: Callable):

        functions = [step.function for step in self.steps]
        index = functions.index(function)

        return index

    def index(self, value: str | Callable | ProcessStep):

        if insinstance(value, str):
            return self._index_name(value)
        elif isinstance(value, Callable):
            return self._index_function(value)
        elif isinstance(value, ProcessStep):
            return self.steps.index(value)

        else:
            raise ValueError("RCAIDE processes can only be indexed by name, function, or ProcessStep object.")

    def insert(self, index: int, step: ProcessStep):

        self.steps.insert(index, step)
        self.update_details()

        return None

    def pop(self, index: int):

        self.steps.pop(index)
        self.update_details()

        return None

    def _remove_name(self, name: str):

        self.steps.pop(self.index_name(name))
        self.update_details()

        return None

    def _remove_function(self, function: Callable):

        self.steps.pop(self.index_function(function))
        self.update_details()

        return None

    def remove(self, value: str | Callable | ProcessStep):

        if isinstance(value, str):
            self._remove_name(value)
            self.update_details()
        elif isinstance(value, Callable):
            self._remove_function(value)
            self.update_details()
        elif isinstance(value, ProcessStep):
            self.steps.remove(value)
            self.update_details()

    def reverse(self):
        raise NotImplementedError("Process cannot be reversed.")

    def sort(self):
        raise NotImplementedError("Process cannot be sorted.")

    def update_details(self):

        new_details_list = [[step.name,
                             step.function.__name__,
                             step.last_result]
                            for step in self.steps]

        new_details = pd.DataFrame(new_details_list,
                                   columns=self.details.columns,
                                   index=[*range(len(self.steps))])

        self.details = new_details

        return None
