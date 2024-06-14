## @ingroup Framework-Analyses-Energy
# RCAIDE/Framework/Analyses/Energy/Energy.py
# (c) Copyright 2023 Aerospace Research Community LLC

# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports   
from RCAIDE.Framework.Analyses import Analysis

# ----------------------------------------------------------------------------------------------------------------------
#  Energy Analysis
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Framework-Analyses-Energy
class Energy(Analysis):
    """ RCAIDE.Framework.Analyses.Energy.Energy()
    """
    def __defaults__(self):
        """This sets the default values and methods for the analysis.
            
        Assumptions:
            None

        Source:
            N/A 
        """        
        self.tag      = 'energy'
        self.networks = None
        
    def evaluate_thrust(self,state): 
        """Evaluate the thrust produced by the energy network.
    
        Assumptions:
            None

        Source:
            N/A

        Inputs:
            self  : energy network    [unitless]
            state : flight conditions [unitless]

        Returns:
            results : results of the thrust evaluation method.
 
        """ 
            
        networks = self.networks
        results  = networks.evaluate_thrust(state) 
        
        return results
    