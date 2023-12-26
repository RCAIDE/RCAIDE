## @ingroup Analyses-Mission-Segments-Conditions
# Aerodynamics.py
#
# Created:  
# Modified: Feb 2016, Andrew Wendorff
#           Mar 2020, M. Clarke 
#           Apr 2021, M. Clarke
#           Jun 2021, A. Blaufox
#           Nov 2021, S. Claridge

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# python imports
import numpy as np

from Legacy.trunk.S.Analyses.Mission.Segments.Conditions.Conditions   import Conditions
# SUAVE imports  
from Legacy.trunk.S.Analyses.Mission.Segments.Conditions             import Aerodynamics as Legacy_Aero

# ----------------------------------------------------------------------
#  Conditions
# ----------------------------------------------------------------------

## @ingroup Analyses-Mission-Segments-Conditions
class Aerodynamics(Legacy_Aero):
    """ This builds upon Basic, which itself builds on conditions, to add the data structure for aerodynamic mission analyses.
    
        Assumptions:
        None
        
        Source:
        None
    """
    
    
    def __defaults__(self):
        """This sets the default values.
    
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
        
        self.tag = 'aerodynamic_conditions'
        # start default row vectors
        ones_1col = self.ones_row(1)
        ones_2col = self.ones_row(2)
        ones_3col = self.ones_row(3)

        
        self.pop('propulsion')

        # ----------------------------------------------------------------------------------------------------------------------         
        # Noise 
        # ----------------------------------------------------------------------------------------------------------------------       
        self.noise                                            = Conditions() 

        # ----------------------------------------------------------------------------------------------------------------------         
        # Energy
        # ---------------------------------------------------------------------------------------------------------------------- 
        self.energy                                           = Conditions()
        self.energy.throttle                                  = ones_1col * 0  
        self.energy.thrust_breakdown                          = Conditions()     
        
        # ----------------------------------------------------------------------------------------------------------------------         
        # Weights 
        # ----------------------------------------------------------------------------------------------------------------------     
        self.weights                                          = Conditions() 
        self.weights.total_mass                               = ones_1col * 0
        self.weights.weight_breakdown                         = Conditions() 
        self.weights.vehicle_mass_rate                        = ones_1col * 0