# RCAIDE/Library/Attributes/Costs/Operating_Costs.py
# (c) Copyright 2023 Aerospace Research Community LLC
#
# Created: Mar 2024, RCAIDE Team

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 
 
from RCAIDE.Framework.Core import Data

# ---------------------------------------------------------------------------------------------------------------------- 
#  Operating_Costs Class
# ----------------------------------------------------------------------------------------------------------------------   
class Operating_Costs(Data):
    """A class containing operating cost variables.
    """    
    def __defaults__(self):
        """This sets the default values used in the operating cost methods. 
        
        Assumptions:
            None
        
        Source:
            None 
        """          
        self.tag = 'operating_costs'
        self.depreciate_years = 0.0
        self.fuel_price       = 0.0
        self.oil_price        = 0.0
        self.insure_rate      = 0.0
        self.maintenance_rate = 0.0
        self.pilot_rate       = 0.0
        self.crew_rate        = 0.0
        self.inflator         = 0.0
        self.reference_dollars= 0.0