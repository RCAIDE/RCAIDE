## @ingroup Framework-Mission-Segments-Conditions 
# RCAIDE/Framework/Mission/Segments/Conditions/Conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
from RCAIDE.Framework.Core                    import Data 

# python imports 
import numpy as np 
# ----------------------------------------------------------------------------------------------------------------------
#  Conditions
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Framework-Mission-Segments-Conditions
class Conditions(Data):
    """ Conditions are the magic Data that contains the information about the vehicle in flight.
        At this point none of the information really exists. What is here are the methods that allow a mission
        to collect the information. 
    """  
    _size = 1
    
    def ones_row(self,cols):
        """ returns a row vector of ones with given number of columns 
        
            Assumptions:
                None
    
            Source:
                None
    
            Args:
                cols   : number of columns  [integer]
    
            Returns:
                vector : expanded vector    [array] 
        """     
        return np.ones([self._size,cols])
    
    def ones_row_m1(self,cols):
        """ returns an N-1 row vector of ones with given number of columns
        
            Assumptions:
                None
    
            Source:
                None
    
            Args:
                cols   : number of columns  [integer]
    
            Returns:
                vector : expanded vector    [array] 
        """ 
        return expanded_array(cols, 1)    
    
    def expand_rows(self,rows,override=False):
        """ Makes a 1-D array the right size. Often used after a mission is initialized to size out the vectors to the
            right size. Will not overwrite an array if it already exists, unless override is True.
            
            Assumptions:
                None
    
            Source:
                None
    
            Args:
                rows     : number of rows    [integer]
                override :                   [boolean]
    
            Returns:
                vector : expanded vector   [np.array]
                
        """           
        
        # store
        self._size = rows
        
        # recursively initialize condition and unknown arrays to have given row length 
        for k,v in self.items():
            try:
                rank = v.ndim
            except:
                rank = 0 
            if isinstance(v,Conditions):
                v.expand_rows(rows,override=override)
            elif isinstance(v,expanded_array):
                self[k] = v.resize(rows) 
            elif rank == 2: # Check if it's already expanded
                if v.shape[0]<=1 or override:
                    self[k] = np.resize(v,[rows,v.shape[1]])
        
        return
        
## @ingroup Framework-Mission-Segments-Conditions        
class expanded_array(Data):
    """ This is an array that will expand later when the mission is initialized. It is called specifically by conditions  
    """  
    _size = 1
    
    def __init__(self, cols, adjustment):
        """ Initialization that sets expansion later
        
            Assumptions:
                None
        
            Source:
                None
        
            Args:
                self
                cols       : columns                          [integer]
                adjustment : how much smaller                 [integer]
        
            Returns:
                None 
        """          
        
        self._adjustment = adjustment
        self._cols       = cols
        self._array      = np.array([[1]])
        
        
    def resize(self,rows):
        """ This function actually completes the resizing. After this it's no longer an expanded array. That way it
            doesn't propogate virally. That means if one wishes to resize later the conditions need to be reset.
        
            Assumptions:
                None
        
            Source:
                None
        
            Args:
                self : 
                rows :   rows                             [integer]
                v    :   values (really self)             [integer]
        
            Returns:
                np.array : properly sized                   [array] 
        """    
        adjustment = self._adjustment 
        self._size = rows
        value      = self._array
        
        return np.resize(value,[rows-adjustment,value.shape[1]])
    
    def __call__(self):
        """ This returns the value and shape of the array as is
        
            Assumptions:
                None
        
            Source:
                None
        
            Args:
                self

            Returns:
                np.array   : properly sized                   [array] 
        """           
        
        return self._array
    
    def __mul__(self,other):
        """ Performs multiplication and returns self
        
            Assumptions:
                None
        
            Source:
                 None
        
            Args:
                 self
                 other      - something can be multiplied      [float]

            Returns:
                 self
        """          
        
        self._array = np.resize(other,[1,1])
        
        return self

    def __rmul__(self,other):
        """ Performs multiplication and returns self
        
            Assumptions:
                 None
        
            Source:
                 None
        
            Args:
                  self
                  other      : something can be multiplied      [float]

            Returns:
                  self 
        """                 
        
        self._array = np.resize(other,[1,1])
        
        return self    
        
    