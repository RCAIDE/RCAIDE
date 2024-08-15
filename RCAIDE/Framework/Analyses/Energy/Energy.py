## @ingroup Analyses-Energy
# RCAIDE/Framework/Analyses/Energy/Energy.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports
from RCAIDE.Framework.Core     import Data
from RCAIDE.Framework.Analyses import Analysis 

# ----------------------------------------------------------------------------------------------------------------------
#  ANALYSIS
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Analyses-Energy

# ----------------------------------------------------------------------------------------------------------------------
#  Energy Analysis
# ----------------------------------------------------------------------------------------------------------------------   
class Energy(Analysis):
    """ This is the base class for energy analyses.
    """
    def __defaults__(self):
        """This sets the default values and methods for the analysis.
            
        Assumptions:
            None

        Source:
            None 
        """        
        self.tag      = 'energy'
        self.vehicle  = Data()
        
    def evaluate(self,state): 
        """Evaluate the thrust produced by the energy network.
    
        Assumptions:
            None

        Source:
            None

        Args:
            state (dict): flight conditions [-]

        Returns:
            results : results of the thrust evaluation method. 
        """ 
            
        networks = self.vehicle.networks
        cg       = self.vehicle.mass_properties.center_of_gravity
        networks.evaluate(state,cg)
        return  
    