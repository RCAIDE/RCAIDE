# RCAIDE/Framework/Process.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import dataclasses
from dataclasses import dataclass, field
from typing import Callable, Iterable, Self, TypeVar, List

# package imports
import pandas as pd

# RCAIDE imports
from RCAIDE.Framework import State, Settings, System


# ----------------------------------------------------------------------------------------------------------------------
#  Argument Passer
# ----------------------------------------------------------------------------------------------------------------------


def skip(*args, **kwargs):
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
    >>> skip(1, 2, name='test')
    (1, 2, {'name': 'test'})
    """
    
    return *args, kwargs



@dataclass(kw_only=True)
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

    function:       Callable    = skip
    name:           str         = "Process Step"
    last_result:    object      = None
    state:          State       = State()
    settings:       Settings    = Settings()
    system:         System      = System()

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
        >>> process_step = ProcessStep(my_function)
        >>> result = process_step()
        """
        framework_args = (self.state, self.settings, self.system)
        return self.function(*framework_args)


def _create_details():
    """
    _create_details()

    Create a pandas DataFrame to store process step details.

    Parameters
    ----------
    None

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame with columns 'Name', 'Function', and 'Last Result'.

    Notes
    -----
    This function initializes a pandas DataFrame with three columns: 'Name', 'Function', and 'Last Result'.
    The DataFrame is used to keep track of the name, function, and last result of each process step.

    Examples
    --------
    >>> details = _create_details()
    >>> print(details.columns)
    Index(['Name', 'Function', 'Last Result'], dtype='object')
    """

    details = pd.DataFrame(
        columns=['Name',
                 'Function',
                 'Last Result']
    )

    return details

# TypeVar for Process, used to type hint that Process objects can contain either ProcessStep or Process objects.
ProcessType = TypeVar('ProcessType', bound='Process')


@dataclass(kw_only=True)
class Process:
    """
    A class representing a process made up of multiple process steps.

    Attributes:
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

    Methods:
    __getitem__(self, item):    Returns the process step at the specified index.
    __delitem__(self, key):     Deletes the process step at the specified index.
    
    __call__(self, *args, **kwargs):    Executes the process, passing the initial state, settings, and system to each process step.
    
    append(self, step: ProcessStep | Self): Appends a process step to the end of the process.
    clear(self):                            Clears all process steps from the process.
    copy(self):                             Returns a shallow copy of the process.
    count(self, step: ProcessStep):         Returns the number of occurrences of the specified process step in the process.
    extend(self, extension: Iterable):      Extends the process with the process steps from the specified iterable.
    
    _index_name(self, name: str):                               Returns the index of the process step with the specified name.
    _index_function(self, function: Callable):                  Returns the index of the process step with the specified function.
    index(self, value: str | Callable | ProcessStep | Self):    Returns the index of the process step with the specified value.
    
    insert(self, index: int, step: ProcessStep | Self): Inserts a process step at the specified index in the process.
    pop(self, index: int):                              Removes and returns the process step at the specified index.
    
    _remove_name(self, name: str):                              Removes the process step with the specified name.
    _remove_function(self, function: Callable):                 Removes the process step with the specified function.
    remove(self, value: str | Callable | ProcessStep | Self):   Removes the process step with the specified value.
    
    reverse(self):          Raises a NotImplementedError, as RCAIDE processes cannot be reversed.
    sort(self):             Raises a NotImplementedError, as RCAIDE processes cannot be sorted.
    
    update_details(self):   Updates the details DataFrame with the current process steps.
    """

    name:               str                 = "Process"

    steps:              List[ProcessStep | ProcessType] = field(default_factory=list)
    details:            pd.DataFrame                    = field(default_factory=_create_details)

    step:               int                 = 0
    initial_step:       int                 = 0

    initial_state:      State               = State()
    initial_settings:   Settings            = Settings()
    initial_system:     System              = System()

    state:              State               = None
    settings:           Settings            = None
    system:             System              = None

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
        >>> process = Process()
        >>> process.append(ProcessStep(my_function))
        >>> step = process[0]
        """
        return self.steps[item]

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
        >>> process = Process()
        >>> process.append(ProcessStep(my_function))
        >>> del process[0]
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
        The function updates the details DataFrame before executing the process steps.
        The state, settings, and system are passed to each process step in the order they are defined in the steps list.
        The last result of each process step is stored in the corresponding ProcessStep object and in the details DataFrame.
        The return value of the last process step is returned as the result of the __call__ method.
        """
    
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
        >>> process = Process()
        >>> process.append(ProcessStep(my_function))
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
        >>> process = Process()
        >>> process.append(ProcessStep(my_function))
        >>> process.clear()
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
        >>> process = Process()
        >>> copied_process = process.copy()
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
        >>> process = Process()
        >>> process.append(ProcessStep(my_function))
        >>> process.append(ProcessStep(my_function))
        >>> count = process.count(ProcessStep(my_function))
        >>> print(count)
        2
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
        >>> process = Process()
        >>> process.append(ProcessStep(my_function))
        >>> process.extend([ProcessStep(my_other_function), ProcessStep(my_third_function)])
        """
    
        self.steps.extend(extension)
        self.update_details()
    
        return None

    def _index_name(self, name: str):
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
        >>> process = Process()
        >>> process.append(ProcessStep(my_function, name="My Function"))
        >>> index = process._index_name("My Function")
        >>> print(index)
        0
        """
    
        names = [step.name for step in self.steps]
        index = names.index(name)
    
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
        >>> process = Process()
        >>> process.append(ProcessStep(my_function))
        >>> index = process._index_function(my_function)
        >>> print(index)
        0
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
        >>> process = Process()
        >>> process.append(ProcessStep(my_function, name="My Function"))
        >>> index = process.index("My Function")
        >>> print(index)
        0
        """
    
        if isinstance(value, str):
            return self._index_name(value)
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
        >>> process = Process()
        >>> process.append(ProcessStep(my_function))
        >>> process.insert(1, ProcessStep(my_other_function))
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
        >>> process = Process()
        >>> process.append(ProcessStep(my_function))
        >>> process.pop(0)
        """
    
        self.steps.pop(index)
        self.update_details()
    
        return None

    def _remove_name(self, name: str):
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
        >>> process = Process()
        >>> process.append(ProcessStep(my_function, name="My Function"))
        >>> process._remove_name("My Function")
        """

        self.steps.pop(self._index_name(name))
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
        >>> process = Process()
        >>> process.append(ProcessStep(my_function))
        >>> process._remove_function(my_function)
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
        >>> process = Process()
        >>> process.append(ProcessStep(my_function, name="My Function"))
        >>> process.remove("My Function")
        >>> process.remove(my_function)
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
        >>> process = Process()
        >>> process.reverse()  # Raises NotImplementedError
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
        >>> process = Process()
        >>> process.sort()  # Raises NotImplementedError
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
        >>> process = Process()
        >>> process.append(ProcessStep(my_function, name="My Function"))
        >>> process.update_details()
        """

        new_details_list = [[step.name,
                             step.function.__name__,
                             step.last_result]
                            for step in self.steps]

        new_details = pd.DataFrame(new_details_list,
                                   columns=self.details.columns,
                                   index=[*range(len(self.steps))])

        self.details = new_details

        return None
