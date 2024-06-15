## @ingroup Framework-Mission
# RCAIDE/Framework/Mission/Sequential_Segments.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports   
import RCAIDE
from RCAIDE.Library.Mission.Common.Segments    import  sequential_segments
from RCAIDE.Library.Mission.Common.Pre_Process import  aerodynamics,stability,energy,set_residuals_and_unknowns
from RCAIDE.Framework.Core                     import Container as ContainerBase
from RCAIDE.Framework.Analyses                 import Process 
from . import Segments

# ----------------------------------------------------------------------------------------------------------------------
# ANALYSIS
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Framework-Mission
class Sequential_Segments(Segments.Segment.Container):
    """ Solves each segment sequentially, one at a time
    """
    
    def __defaults__(self):
        """This sets the default values.
    
            Assumptions:
            None
    
            Source:
            None 
        """          

        self.tag = 'mission'
        
        #   Initialize   
        self.process.initialize                                = Process() 
        self.process.initialize.aero                           = aerodynamics
        self.process.initialize.stability                      = stability
        self.process.initialize.energy                         = energy
        self.process.initialize.set_residuals_and_unknowns     = set_residuals_and_unknowns
 
        #   Converge 
        self.process.converge    = sequential_segments
         
        #   Iterate     
        del self.process.iterate  

        return  

    def pre_process(self):
        """ This executes a pre-processing step
    
            Assumptions:
                None
    
            Source:
                None
    
            Args:
                self  : RCAIDE data structure of containing process [-]
    
            Returns:
                self  : RCAIDE data structure of containing process [-]
        """   
        self.process.pre_process(self)
         
        return self 

                        
    def evaluate(self,state=None):
        """ This executes the entire process
    
            Assumptions:
                None
    
            Source:
                None
    
            Args:
                self  : RCAIDE data structure of containing process [-]
    
            Returns:
                self  : RCAIDE data structure of containing process [-]
        """           
        if state is None:
            state = self.state
        self.process(self)
        return self     
        
    
# ----------------------------------------------------------------------
#   Container Class
# ----------------------------------------------------------------------

## @ingroup Framework-Mission
class Container(ContainerBase):
    """ Container for mission.
    """    
    
    def evaluate(self,state=None):
        """ Go through the missions, run through them, save the results 
    
            Assumptions:
                None
    
            Source:
                None
    
            Args:
                self  : RCAIDE data structure of containing process [-]
    
            Returns:
                self  : RCAIDE data structure of containing process [-]
        """   
        results = RCAIDE.Framework.Core.Data()
        
        for key,mission in self.items():
            result = mission.evaluate(state)
            results[key] = result
            
        return results 

# Link container
Sequential_Segments.Container = Container