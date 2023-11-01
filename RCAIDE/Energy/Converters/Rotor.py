## @ingroup Energy-Converters
# Rotor.py
#
# Created:  Oct 2023, Racheal M. Erhard
# Modified: 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
from Legacy.trunk.S.Components.Energy.Converters import Rotor as Rotor_Legacy
from Legacy.trunk.S.Core import ContainerOrdered, Data

from RCAIDE.Components.Airfoils.Airfoil import Airfoil as Airfoil_Component



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
        
        self.Airfoil_Components = ContainerOrdered() # The instances of airfoil components used in rotor
        self.Airfoil_Analyses = None# The instances of airfoil analyses used for each airfoil in rotor
        
        return
    
    def finalize(self, airfoil_analysis):
        
        # If no airfoil components were specified, attach a default airfoil
        if not bool(self.Airfoil_Components):
            airfoil = Airfoil_Component()
            self.append_airfoil_component(airfoil)
            
        # If airfoil stations are not set by the user, default to use the first attached airfoil
        if self.airfoil_polar_stations is None:
            self.airfoil_polar_stations = [0] * self.number_of_radial_stations
        

        # New airfoil methods
        # Legacy code has self.Airfoils as the combined component and analysis outputs. 
        # RCAIDE treats these separately. The spin function in legacy uses only the analysis part, so
        # here we replace the self.Airfoils with the self.Airfoil_Analyses    
        airfoil_analysis.geometry = self
        airfoil_analysis.initialize()
        airfoil_analysis.evaluate()
        
        for airfoil in self.Airfoil_Components:
            airfoil.initialize()
            
        self.Airfoil_Analyses = airfoil_analysis     
        

        
        # Replace self.Airfoils with airfoil analyses (This is for use in legacy code)
        for key in list(self.Airfoil_Analyses.airfoil_data.keys()):
            
            self.Airfoils[key] = Data()
            self.Airfoils[key].polars = self.Airfoil_Analyses.airfoil_data[key]
        return
    
    def append_airfoil_component(self,airfoil):
        """ Adds an airfoil component to the rotor

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
        # assert database type
        if not isinstance(airfoil, Airfoil_Component):
            raise Exception('input component must be of type Data()')


        # See if the component exists, if it does modify the name
        keys = self.keys()
        if airfoil.tag in keys:
            string_of_keys = "".join(self.keys())
            n_comps = string_of_keys.count(airfoil.tag)
            airfoil.tag = f"{airfoil.tag}{n_comps+1}"    
            
        # store data
        self.Airfoil_Components.append(airfoil)
        
