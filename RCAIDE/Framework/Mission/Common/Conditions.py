# RCAIDE/Framework/Functions/Segments/Conditions/Conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team
 
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
                cols   (int) : number of columns  
    
            Returns:
                vector (numpy.ndarray): expanded vector  
        """     
        return np.ones([self._size,cols])
    
    def ones_row_m1(self,cols):
        """ returns an N-1 row vector of ones with given number of columns
        
            Assumptions:
                None
    
            Source:
                None
    
            Args:
                cols   (int) : number of columns  
    
            Returns:
                vector (numpy.ndarray): expanded vector    
        """ 
        return expanded_array(cols, 1)    
    
    def expand_rows(self,rows: int,override=False):
        """ Makes a 1-D array the right size. Often used after a mission is initialized to size out the vectors to the
            right size. Will not overwrite an array if it already exists, unless override is True.
            
            Assumptions:
                None
    
            Source:
                None
    
            Args:
                rows (int) : number of rows
                override (bool):   
    
            Returns:
                vector (numpy.ndarray): expanded vector    
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
              
class expanded_array(Data):
    """ This is an array that will expand later when the mission is initialized. It is called specifically by conditions  
    """  
    _size = 1
    
    def __init__(self, cols: int, adjustment: int):
        """ Initialization that sets expansion later
        
            Assumptions:
                None
        
            Source:
                None
        
            Args:
                self
                cols       (int): number of columns     
                adjustment (int): new number of columns                  
        
            Returns:
                None 
        """          
        
        self._adjustment = adjustment
        self._cols       = cols
        self._array      = np.array([[1]])
        
        
    def resize(self,rows: int):
        """ This function actually completes the resizing. After this it's no longer an expanded array. That way it
            doesn't propogate virally. That means if one wishes to resize later the conditions need to be reset.
        
            Assumptions:
                None
        
            Source:
                None
        
            Args:
                self (numpy.ndarray): array
                rows (int) : number of rows                        
        
            Returns:
                arg (numpy.ndarray) : properly sized                 
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
                self (numpy.ndarray): array

            Returns:
                self (numpy.ndarray): array   
        """           
        
        return self._array
    
    def __mul__(self,A):
        """ Performs multiplication and returns self
        
            Assumptions:
                None
        
            Source:
                 None
        
            Args:
                 self (numpy.ndarray): array
                 A    (int or tuple of int): Shape of resized array.

            Returns:
                 self (numpy.ndarray): array
        """          
        
        self._array = np.resize(A,[1,1])
        
        return self

    def __rmul__(self,A):
        """ Performs multiplication and returns self
        
            Assumptions:
                 None
        
            Source:
                 None
        
            Args:
                 self (numpy.ndarray): array
                 A    (int or tuple of int): Shape of resized array.

            Returns:
                self (numpy.ndarray): array  
        """                 
        
        self._array = np.resize(A,[1,1])
        
        return self    
        
    