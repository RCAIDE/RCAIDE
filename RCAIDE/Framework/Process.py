# RCAIDE/Framework/Process.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import dataclasses
from dataclasses import field
from typing import Callable, Iterable, Self, List

# package imports
import RNUMPY as rp
import pandas as pd
import chex

# RCAIDE imports
import RCAIDE.Framework as rcf


# ----------------------------------------------------------------------------------------------------------------------
#  Argument Passer
# ----------------------------------------------------------------------------------------------------------------------


def skip(*args):
    """
    skip(*args, **kwargs)

    Function to skip arguments and return them as is.

    Parameters
    ----------
    *args : tuple
        Positional arguments.
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    tuple
        The input arguments as a tuple.

    Examples
    --------
    """

    return args


@chex.dataclass(kw_only=True)
class ProcessStep:
    """
    A class representing a single step in a process.

    Attributes:
    function    (Callable): The function to be executed in this step. Default is the `skip` function.
    name        (str):      The name of the process step. Default is "Process Step".
    last_result (object):   The result of the last execution of this step. Default is None.
    state       (State):    The state object to be passed to the function. Default is an empty State object.
    settings    (Settings): The settings object to be passed to the function. Default is an empty Settings object.
    system      (System):   The system object to be passed to the function. Default is an empty System object.

    Methods:
    __call__():             Executes the function with the provided state, settings, and system objects.
    """

    function:       Callable        = skip
    tag:            str             = "Process Step"
    last_result:    object          = None
    state:          "rcf.State"     = None
    system:         "rcf.System"    = None
    settings:       "rcf.Settings"  = None


    def __call__(self):
        """
        __call__(self)
    
        Executes the function associated with the process step.
    
        Parameters
        ----------
        None
    
        Returns
        -------
        object
            The return value of the executed function.
    
        Notes
        -----
        The function is called with the current state, settings, and system objects as arguments.
        The function's return value is stored as the last result of the process step.
    
        Examples
        --------
        """
        framework_args = (self.state, self.system, self.settings)
        return self.function(*framework_args)
    
    def __repr__(self):
        try:
            func_name = getattr(self.function, "__name__", None) or type(self.function).__name__
            state_type = type(self.state).__name__ if self.state is not None else "None"
            system_type = type(self.system).__name__ if self.system is not None else "None"
            settings_type = type(self.settings).__name__ if self.settings is not None else "None"
            last_present = self.last_result is not None
            return (
                f"<{self.__class__.__name__} "
                f"tag={self.tag!r} func={func_name} "
                f"last_result_present={last_present} "
                f"state={state_type} system={system_type} settings={settings_type}>"
            )
        except Exception:
            return object.__repr__(self)



@chex.dataclass(kw_only=True)
class Process:
    """
    A class representing a process made up of multiple process steps.

    Attributes
    __________
    name    (str):                              The name of the process. Default is "Process".
    steps   (List[ProcessStep | ProcessType]):  A list of process steps in the process. Default is an empty list.
    details (pd.DataFrame):                     A pandas DataFrame to store process step details. Default is a DataFrame
                                                created by _create_details().
    
    step            (int):  The current step in the process. Default is 0.
    initial_step    (int):  The initial step in the process. Default is 0.
    
    initial_state       (State):    The initial state for the process. Default is an empty State object.
    initial_settings    (Settings): The initial settings for the process. Default is an empty Settings object.
    initial_system      (System):   The initial system for the process. Default is an empty System object.
    
    state       (State):    The current state during the process. Default is None.
    settings    (Settings): The current settings during the process. Default is None.
    system      (System):   The current system during the process. Default is None.

    Methods
    _______
    __getitem__(self, item):    Returns the process step at the specified index.
    __delitem__(self, key):     Deletes the process step at the specified index.
    
    __call__(self, *args, **kwargs):    Executes the process, passing the initial state, settings, and system to each process step.
    
    append(self, step: ProcessStep | Self): Appends a process step to the end of the process.
    clear(self):                            Clears all process steps from the process.
    copy(self):                             Returns a shallow copy of the process.
    count(self, step: ProcessStep):         Returns the number of occurrences of the specified process step in the process.
    extend(self, extension: Iterable):      Extends the process with the process steps from the specified iterable.
    
    _index_tag(self, tag: str):                               Returns the index of the process step with the specified name.
    _index_function(self, function: Callable):                  Returns the index of the process step with the specified function.
    index(self, value: str | Callable | ProcessStep | Self):    Returns the index of the process step with the specified value.
    
    insert(self, index: int, step: ProcessStep | Self): Inserts a process step at the specified index in the process.
    pop(self, index: int):                              Removes and returns the process step at the specified index.
    
    _remove_name(self, tag: str):                              Removes the process step with the specified name.
    _remove_function(self, function: Callable):                 Removes the process step with the specified function.
    remove(self, value: str | Callable | ProcessStep | Self):   Removes the process step with the specified value.
    
    reverse(self):          Raises a NotImplementedError, as RCAIDE processes cannot be reversed.
    sort(self):             Raises a NotImplementedError, as RCAIDE processes cannot be sorted.
    
    update_details(self):   Updates the details DataFrame with the current process steps.
    """

    tag:                str             = "Process"
    keep_details:       bool            = False

    steps:              List[Callable]  = field(default_factory=list)
    details:            pd.DataFrame    = None

    current_step:       int             = 0
    initial_step:       int             = 0

    initial_state:      "rcf.State"     = None
    initial_settings:   "rcf.Settings"  = None
    initial_system:     "rcf.System"    = None

    state:              "rcf.State"     = None
    settings:           "rcf.Settings"  = None
    system:             "rcf.System"    = None

    last_result:        object          = None

    def __getitem__(self, item):
        """
        __getitem__(self, item)
    
        Returns the process step at the specified index.
    
        Parameters
        ----------
        item : int
            The index of the process step to retrieve.
    
        Returns
        -------
        ProcessStep | ProcessType
            The process step at the specified index.
    
        Raises
        ------
        IndexError
            If the specified index is out of range.
    
        Examples
        --------
        """
        if isinstance(item, str):
            return self.steps[self._index_tag(item)]
        else:
            return self.steps[item]

    def __setitem__(self, key, value):
        if isinstance(key, str):
            self.steps[self._index_tag(key)] = value
            self.update_details()
        else:
            self.steps[key] = value
            self.update_details()

    def __delitem__(self, key):
        """
        __delitem__(self, key)
    
        Removes and returns the process step at the specified index.
    
        Parameters
        ----------
        key : int
            The index of the process step to remove.
    
        Returns
        -------
        None
    
        Raises
        ------
        IndexError
            If the specified index is out of range.
    
        Examples
        --------
        """
        del self.steps[key]
        self.update_details()

    def __call__(self, *args, **kwargs):
        """
        Executes the process, passing the state, settings, and system to each process step.
    
        Parameters
        ----------
        *args : tuple
            Additional positional arguments to be passed to each process step.
        **kwargs : dict
            Additional keyword arguments to be passed to each process step.
    
        Returns
        -------
        object
            The return value of the last process step.
    
        Notes
        -----
        - The function updates the details DataFrame before executing the process steps.
        - The state, settings, and system are passed to each process step in the order they are defined in the steps list.
        - The last result of each process step is stored in the corresponding ProcessStep object and in the details DataFrame.
        - The return value of the last process step is returned as the result of the __call__ method.
        """
    
        self.update_details()
    
        framework_args = (self.state.initials,
                          self.system,
                          self.settings,)

        self.current_step = self.initial_step

        for index, step in enumerate(self.steps[self.initial_step:]):

            step.state = framework_args[0]
            step.system = framework_args[1]
            step.settings = framework_args[2]

            framework_args = step()

            self.steps[self.initial_step + index].last_result = framework_args
            if self.keep_details:
                self.details.at[self.initial_step + index, 'Last Result'] = framework_args

            self.current_step += 1

        return framework_args

    def run(self, *args, **kwargs):

        return self(*args, **kwargs)

    def append(self, step: ProcessStep | Self):
        """
        Append a process step to the end of the process.
    
        Parameters
        ----------
        step : Union['ProcessStep', 'Self']
            The process step to be appended. It can be an instance of ProcessStep or a nested Process.
    
        Returns
        -------
        None
            The function does not return any value. It modifies the process by appending the given step.
    
        Examples
        --------
        """
    
        self.steps.append(step)
        self.update_details()
    
        return None

    def clear(self):
        """
        Clear all process steps from the process.
    
        Parameters
        ----------
        None
    
        Returns
        -------
        None
            The function does not return any value. It modifies the process by clearing all process steps.
    
        Raises
        ------
        None
            The function does not raise any exceptions.
    
        Examples
        --------
        """
    
        self.steps.clear()
        self.update_details()
    
        return None

    def copy(self):
        """
        Create a shallow copy of the process.
    
        Parameters
        ----------
        None
    
        Returns
        -------
        Process
            A shallow copy of the process.
    
        Raises
        ------
        None
            The function does not raise any exceptions.
    
        Examples
        --------
        """
    
        return dataclasses.replace(self)

    def count(self, step: ProcessStep):
        """
        Count the occurrences of a specific process step in the process.
    
        Parameters
        ----------
        step : ProcessStep
            The process step to count occurrences of.
    
        Returns
        -------
        int
            The number of occurrences of the specified process step in the process.
    
        Raises
        ------
        None
            The function does not raise any exceptions.
    
        Examples
        --------
        """
    
        return self.steps.count(step)

    def extend(self, extension: Iterable):
        """
        Extend the process with the process steps from the specified iterable.
    
        Parameters
        ----------
        extension : Iterable
            An iterable containing process steps to be added to the process.
    
        Returns
        -------
        None
            The function does not return any value. It modifies the process by extending it with the given iterable.
    
        Raises
        ------
        None
            The function does not raise any exceptions.
    
        Examples
        --------
        """
    
        self.steps.extend(extension)
        self.update_details()
    
        return None

    def _index_tag(self, tag: str):
        """
        Find the index of the process step with the specified name.
    
        Parameters
        ----------
        name : str
            The name of the process step to find the index of.
    
        Returns
        -------
        int
            The index of the process step with the specified name. If the name is not found, it returns -1.
    
        Raises
        ------
        None
            The function does not raise any exceptions.
    
        Examples
        --------
        """
    
        tags = [step.tag for step in self.steps]
        index = tags.index(tag)
    
        return index

    def _index_function(self, function: Callable):
        """
        Find the index of the process step with the specified function.
    
        Parameters
        ----------
        function : Callable
            The function of the process step to find the index of.
    
        Returns
        -------
        int
            The index of the process step with the specified function. If the function is not found, it returns -1.
    
        Raises
        ------
        None
            The function does not raise any exceptions.
    
        Examples
        --------
        """
    
        functions = [step.function for step in self.steps]
        index = functions.index(function)
    
        return index

    def index(self, value: str | Callable | ProcessStep | Self):
        """
        Find the index of the process step with the specified value.
    
        Parameters
        ----------
        value : Union[str, Callable, 'ProcessStep', 'Self']
            The value to find the index of. It can be a name (str), a function (Callable), a ProcessStep object, or a nested Process.
    
        Returns
        -------
        int
            The index of the process step with the specified value. If the value is not found, it raises a ValueError.
    
        Raises
        ------
        ValueError
            If the specified value is not found in the process steps.
    
        Examples
        --------
        """
    
        if isinstance(value, str):
            return self._index_tag(value)
        elif isinstance(value, Callable):
            return self._index_function(value)
        elif isinstance(value, ProcessStep):
            return self.steps.index(value)
    
        else:
            raise ValueError("RCAIDE processes can only be indexed by name, function, or ProcessStep object.")

    def insert(self, index: int, step: ProcessStep | Self):
        """
        Insert a process step at the specified index in the process.
    
        Parameters
        ----------
        index : int
            The index at which to insert the process step.
        step : Union['ProcessStep', 'Self']
            The process step to be inserted. It can be an instance of ProcessStep or a nested Process.
    
        Returns
        -------
        None
            The function does not return any value. It modifies the process by inserting the given step at the specified index.
    
        Raises
        ------
        IndexError
            If the specified index is out of range.
    
        Examples
        --------
        """
    
        self.steps.insert(index, step)
        self.update_details()
    
        return None

    def pop(self, index: int):
        """
        Remove and return the process step at the specified index.
    
        Parameters
        ----------
        index : int
            The index of the process step to remove.
    
        Returns
        -------
        None
            The function does not return any value. It modifies the process by removing the process step at the specified index.
    
        Raises
        ------
        IndexError
            If the specified index is out of range.
    
        Examples
        --------
        """
    
        self.steps.pop(index)
        self.update_details()
    
        return None

    def _remove_tag(self, tag: str):
        """
        Remove the process step with the specified name.

        Parameters
        ----------
        name : str
            The name of the process step to remove.

        Returns
        -------
        None
            The function does not return any value. It modifies the process by removing the process step with the specified name.

        Raises
        ------
        ValueError
            If the specified name is not found in the process steps.

        Examples
        --------
        """

        self.steps.pop(self._index_tag(tag))
        self.update_details()

        return None

    def _remove_function(self, function: Callable):
        """
        Remove the process step with the specified function.
    
        Parameters
        ----------
        function : Callable
            The function of the process step to remove.
    
        Returns
        -------
        None
            The function does not return any value. It modifies the process by removing the process step with the specified function.
    
        Raises
        ------
        ValueError
            If the specified function is not found in the process steps.
    
        Examples
        --------
        """
    
        self.steps.pop(self._index_function(function))
        self.update_details()
    
        return None

    def remove(self, value: str | Callable | ProcessStep | Self):
        """
        Remove the process step with the specified value.
    
        Parameters
        ----------
        value : Union[str, Callable, 'ProcessStep', 'Self']
            The value to find and remove the process step. It can be a name (str), a function (Callable), a ProcessStep object, or a nested Process.
    
        Returns
        -------
        None
            The function does not return any value. It modifies the process by removing the process step with the specified value.
    
        Raises
        ------
        ValueError
            If the specified value is not found in the process steps.
    
        Examples
        --------
        """
    
        if isinstance(value, str):
            self._remove_name(value)
            self.update_details()
        elif isinstance(value, Callable):
            self._remove_function(value)
            self.update_details()
        else:
            self.steps.remove(value)
            self.update_details()

    def reverse(self):
        """
        Raises an exception indicating that RCAIDE processes cannot be reversed.
    
        Parameters
        ----------
        None
    
        Returns
        -------
        None
    
        Raises
        ------
        NotImplementedError
            If the method is called.
    
        Examples
        --------
        """
    
        raise NotImplementedError("RCAIDE processes cannot be reversed.")

    def sort(self):
        """
        Raises an exception indicating that RCAIDE processes cannot be sorted.
    
        Parameters
        ----------
        None
    
        Returns
        -------
        None
    
        Raises
        ------
        NotImplementedError
            If the method is called.
    
        Examples
        --------
        """
    
        raise NotImplementedError("RCAIDE processes cannot be sorted.")

    def update_details(self):
        """
        Update the details DataFrame with the current process steps.

        Parameters
        ----------
        None

        Returns
        -------
        None
            The function does not return any value. It modifies the process by updating the details DataFrame.

        Raises
        ------
        None
            The function does not raise any exceptions.

        Examples
        --------
        """

        if not self.keep_details:
            return None

        if not self.details:

            self.details = pd.DataFrame(
                columns=['Name',
                 'Function',
                 'Last Result']
            )

        if any(not isinstance(s, ProcessStep) for s in self.steps):
            if not all(isinstance(s, Callable) for s in self.steps):
                raise ValueError("All process steps must be ProcessSteps, or callable functions/objects.")
            else:
                for i, step in enumerate(self.steps):
                    if not (isinstance(step, ProcessStep) or isinstance(step, Process)):
                        self.steps[i] = ProcessStep(function=step,
                                                    tag=step.__name__)

        new_details_list = [[step.tag,
                             step.function.__name__,
                             step.last_result]
                            if isinstance(step, ProcessStep)
                            else [step.tag,
                                  step.__class__.__name__,
                                  step.last_result]
                             for step in self.steps]

        new_details = pd.DataFrame(new_details_list,
                                   columns=self.details.columns,
                                   index=[*range(len(self.steps))])

        self.details = new_details

        return None
    
    def __repr__(self):
        """
        Safe representation that summarizes steps
        """
        # We use type(self).__name__ instead of self.__class__.__name__ 
        # to avoid potential overhead if __class__ is instrumented by chex/jax.
        return f"<{type(self).__name__} tag='{self.tag}' step={self.current_step}/{len(self.steps)}>"


if __name__ == "__main__":


    def lib_sq_func(x):
        return x**2

    def fw_sq_func(state, system, settings):
        x = state.x
        results = lib_sq_func(x)
        state.x = results

        return state, system, settings


    def lib_add_func(x, y):
        return x + y

    def fw_add_func(state, system, settings):
        x = state.x
        y = state.y
        results = lib_add_func(x, y)
        state.x = results

        return state, system, settings

    square_and_add = Process(
        steps=[fw_sq_func, fw_add_func],
        initial_step=0
    )

    def sq_add_func(x, y):
        square_and_add.initial_state.x = x
        square_and_add.initial_state.y = y
        st, set, sys = square_and_add.run()
        return st.x

    from jax import value_and_grad

    sq_grad = value_and_grad(sq_add_func)

    results = sq_grad(3., 6.)

    print(square_and_add.details)
    print(results)

