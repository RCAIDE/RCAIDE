# RCAIDE/Framework/Analyses/Weights/Electric_Transport.py
#
# Created:  Oct. 2025, A. Molloy
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

from .Electric import Electric

# ----------------------------------------------------------------------------------------------------------------------
#  Electric General Aviation weights class
# ----------------------------------------------------------------------------------------------------------------------
class Electric_Transport(Electric):
    """ This is class that evaluates the weight of an electric transport class aircraft

    Assumptions:
        None

    Source:
        N/A

    Inputs:
        None

    Outputs:
        None

    Properties Used:
         N/A
    """

    def __defaults__(self):
        """This sets the default values and methods for the tube and wing
        aircraft weight analysis.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """  
        self.method                                        = 'Semi_Empirical'
        self.aircraft_type                                 = 'Transport'
     