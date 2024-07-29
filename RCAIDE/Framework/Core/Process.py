from dataclasses    import dataclass, field
from typing         import Callable, Iterable

from RCAIDE.Framework.Core.Utilities import args_passer

import pandas as pd

@dataclass
class ProcessStep:

    #---------------------------------------------------------------------------
    # Process Step Parameters
    #---------------------------------------------------------------------------

    # Required Parameters

    function:       Callable    = field(init=True, default=args_passer)

    # Optional Parameters

    name:           str         = field(init=True, default="")
    last_result:    object      = field(init=True, default=None)

    State:          dataclass   = field(init=False)
    Settings:       dataclass   = field(init=False)
    System:         dataclass   = field(init=False)

    def __call__(self):

        framework_args = (self.State, self.Settings, self.System)

        return self.function(*framework_args)


def _create_details():

    details = pd.DataFrame(
        columns=['Name',
                 'Function',
                 'Last Result']
    )

    return details


@dataclass
class Process:

    #---------------------------------------------------------------------------
    # Process Parameters
    #---------------------------------------------------------------------------

    # Required Parameters

        # N/A

    # Optional Parameters

    name: str = field(init=True, default="")

    # Internal Parameters

    steps: list[ProcessStep] = field(init=False, default_factory=list)
    details: pd.DataFrame    = field(init=False, default_factory=_create_details)

    current_step: int = field(init=False, default=0)
    start_at: int = field(init=False, default=0)

    initial_state: dataclass = field(init=False)
    initial_settings: dataclass = field(init=False)
    initial_system: dataclass = field(init=False)

    def __getitem__(self, item):
        return self.steps[item]

    def __call__(self, *args, **kwargs):

        self.update_details()

        framework_args = (self.initial_state,
                          self.initial_settings,
                          self.initial_system)

        for index, step in enumerate(self.steps[self.start_at:-1]):
            framework_args = step(*framework_args)
            self.steps[index].last_result = framework_args
            self.details.at[index, 'Last Result'] = framework_args

        results = self.steps[-1](*next_args)
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
        raise NotImplementedError("Process cannot be copied directly."
                                  "Use Process.steps.copy() instead.")

    def count(self):
        raise NotImplementedError("Process steps cannot be counted directly."
                                  "Use Process.steps.count() instead.")

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

    def index(self, value: str | Callable, mode: str = 'name'):

        if mode == 'name':
            index = self._index_name(value)
        elif mode == 'function':
            index = self._index_function(value)
        else:
            raise ValueError("Mode must be 'name' or 'function'.")

        return index

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

    def remove(self, value: object, mode: str = 'name'):

        if mode == 'name':
            self._remove_name(value)
            self.update_details()
        elif mode == 'function':
            self._remove_function(value)
            self.update_details()
        else:
            raise ValueError("Mode must be 'name' or 'function'.")

        return None

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
