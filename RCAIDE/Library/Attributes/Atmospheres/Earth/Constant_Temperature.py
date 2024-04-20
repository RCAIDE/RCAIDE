## @ingroup Library-Attributes-Atmospheres-Earth
# RCAIDE/Library/Attributes/Atmospheres/Earth/Constant_Temperature.py
# 
#
# Created:  Mar 2024, M. Clarke

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 
 
from RCAIDE.Framework.Core import Data , Units
from RCAIDE.Library.Attributes.Gases import Air
from RCAIDE.Library.Attributes.Atmospheres import Atmosphere
from RCAIDE.Library.Attributes.Planets import Earth 
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
# Constant_Temperature Class
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Attributes-Atmospheres-Earth   
class Constant_Temperature(Atmosphere):
    """Contains US Standard 1976 values with temperature modified to be constant. 
    """
    def __defaults__(self):
        """This sets the default values at breaks in the atmosphere.

        Assumptions:
            Constant temperature

        Source:
            U.S. Standard Atmosphere (1976 version)

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """          
        self.fluid_properties = Air()
        self.planet = Earth()
        self.breaks = Data()
        self.breaks.altitude    = np.array( [-2.00    , 0.00,     11.00,      20.00,      32.00,      47.00,      51.00,      71.00,      84.852]) * Units.km     # m, geopotential altitude
        self.breaks.temperature = np.array( [301.15   , 301.15,    301.15,    301.15,     301.15,     301.15,     301.15,     301.15,     301.15])      # K
        self.breaks.pressure    = np.array( [127774.0 , 101325.0, 22632.1,    5474.89,    868.019,    110.906,    66.9389,    3.95642,    0.3734])      # Pa
        self.breaks.density     = np.array( [1.545586 , 1.2256523,.273764,	 .0662256,	0.0105000 ,	1.3415E-03,	8.0971E-04,	4.78579E-05, 4.51674E-06]) #kg/m^3 
    
    pass
