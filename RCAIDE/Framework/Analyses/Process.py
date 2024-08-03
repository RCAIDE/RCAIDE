# RCAIDE/Framework/Analyses/Process.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Reference.Core import Container
from RCAIDE.Reference.Core import Data

# ----------------------------------------------------------------------------------------------------------------------
# Process
# ----------------------------------------------------------------------------------------------------------------------  
class Process(Container):
    """
    The top-level process container class.

    This class provides a container for storing and executing various analyses.
    It inherits from the `Container` class, which is a part of the RCAIDE framework.

    Methods
    -------
    evaluate(*args, **kwarg)
        Executes the evaluate functions of the analyses stored in the container.

        Parameters
        ----------
        *args : arguments
            Positional arguments to be passed to the evaluate functions.
        **kwarg : keyword arguments
            Keyword arguments to be passed to the evaluate functions.

        Returns
        -------
        results : Data
            A dictionary-like object containing the results of the evaluate functions.

    Attributes
    ----------
    None

    """

    def evaluate(self, *args, **kwarg):
        """
        Executes the evaluate functions of the analyses stored in the container.

        Parameters
        ----------
        *args : arguments
            Positional arguments to be passed to the evaluate functions.
        **kwarg : keyword arguments
            Keyword arguments to be passed to the evaluate functions.

        Returns
        -------
        results : Data
            A dictionary-like object containing the results of the evaluate functions.

        """
        results = Data()

        for tag, step in self.items():
            if hasattr(step, 'evaluate'):
                result = step.evaluate(*args, **kwarg)
            else:
                result = step(*args, **kwarg)

            results[tag] = result

        return results