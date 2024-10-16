# RCAIDE/Framework/Functions/Segments/Common/State.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Framework.Core import Data
from .Conditions           import Conditions
from .Residuals            import Residuals
from .Numerics             import Numerics   

# python imports
import RNUMPY as rp

# ----------------------------------------------------------------------------------------------------------------------
#  State
# ----------------------------------------------------------------------------------------------------------------------

class State(Conditions):
    """ Creates the State data structure for storing daata that solved in a mission.
    """  
    def __defaults__(self):
        """ This sets the default values.
        
        Assumptions:
            None
    
        Source:
            None 
        """   
        self.tag        = 'state'
        self.initials   = Conditions()
        self.numerics   = Numerics()
        self.unknowns   = Conditions()
        self.conditions = Conditions()
        self.residuals  = Residuals()
        
    def expand_rows(self,rows,override=False):
        """ Makes a 1-D array the right size. Often used after a mission is initialized to size out the vectors to the
            right size. Will not overwrite an array if it already exists, unless override is True.
        
            Assumptions:
                Doesn't expand initials or numerics
    
            Source:
                None
      
            Args:
                rows (int): number of rows

            Returns:
                None 
        """         
        
        # store
        self._size = rows
        
        for k,v in self.items(): 
            try:
                rank = v.ndim
            except:
                rank = 0            
            # don't expand initials or numerics
            if k in ('initials','numerics'):
                continue 
            # recursion
            elif isinstance(v,Conditions):
                v.expand_rows(rows,override=override)
            # need arrays here
            elif rank == 2:
                self[k] = rp.resize(v,[rows,v.shape[1]]) 
        
# ----------------------------------------------------------------------------------------------------------------------
# Container
# ----------------------------------------------------------------------------------------------------------------------      
class Container(State):
    def __defaults__(self):
        """ This sets the default values.
    
            Assumptions:
               Puts the segments in the right order
    
            Source:
                None 
        """         
        self.segments = Data()
        
    def merged(self):
        """ Combines the states of multiple segments
    
            Assumptions:
                None
    
            Source:
                None
    
            Args:
                None
    
            Returns:
                state_out [State()] 
        """              
        
        state_out = State()
        
        for i,(tag,sub_state) in enumerate(self.segments.items()):
            for key in ['unknowns','conditions','residuals']:
                if i == 0:
                    state_out[key].update(sub_state[key])
                else:
                    state_out[key] = state_out[key].do_recursive(append_array,sub_state[key])
            
        return state_out
        
State.Container = Container 
        
# ----------------------------------------------------------------------------------------------------------------------
# append_array
# ---------------------------------------------------------------------------------------------------------------------- 
def append_array(A,B=None):
    """ A stacking operation used by merged to put together data structures

        Assumptions:
            None

        Source:
            None

        Args:
            A (float): rp.array 
            B (float): rp.array 

        Returns:
             (float): rp.array
    """       
    if isinstance(A,rp.ndarray) and isinstance(B,rp.ndarray):
        return rp.vstack([A,B])
    else:
        return None