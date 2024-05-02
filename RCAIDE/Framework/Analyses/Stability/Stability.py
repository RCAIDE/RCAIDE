 
from RCAIDE.Framework.Core import Data
from RCAIDE.Framework.Analyses import Analysis


# ----------------------------------------------------------------------
#  Analysis
# ----------------------------------------------------------------------

## @ingroup Analyses-Stability
class Stability(Analysis):
    """  
    """

    def __defaults__(self):
        """ 
        """           
        self.tag    = 'stability'
        self.geometry = Data()
        self.settings = Data()
 
        return


