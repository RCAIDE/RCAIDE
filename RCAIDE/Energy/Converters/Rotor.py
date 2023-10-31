## @ingroup Energy-Converters
# Rotor.py
#
# Created:  Oct 2023, Racheal M. Erhard
# Modified: 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
from Legacy.trunk.S.Components.Energy.Converters import Rotor as Rotor_Legacy
from RCAIDE.Components.Airfoils import Airfoil



# ----------------------------------------------------------------------
#  Generalized Rotor Class
# ----------------------------------------------------------------------
## @ingroup Energy-Converters
class Rotor(Rotor_Legacy):
    """This is a general rotor component. Currently, it inherits from the legacy rotor class.

    Assumptions:
    None

    Source:
    None
    """
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """

        self.number_of_radial_stations = 20 

    def finalize(self):
        # If no airfoils were specified, attach a default airfoil
        airfoil = Airfoil()
        self.append_airfoil(airfoil)
        self.airfoil_stations = [0] * self.number_of_radial_stations
        
        return
    