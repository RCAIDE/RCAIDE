# RCAIDE/Core/Container.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------        

from RCAIDE.Reference.Core import Data
import random

import string
chars = string.punctuation + string.whitespace
t_table = str.maketrans( chars          + string.ascii_uppercase , 
                            '_'*len(chars) + string.ascii_lowercase )

# ----------------------------------------------------------------------------------------------------------------------
#  Container
# ----------------------------------------------------------------------------------------------------------------------    
class Container(Data):
    """ A dict-type container with attribute, item and index style access
        intended to hold a attribute-accessible list of Data(). This is unordered. 
    """
            
        
    def __defaults__(self):
        """ Defaults function
        
        Assumptions:
            None
    
        Source:
           None 
        """          
        pass
    
    def __init__(self,*args,**kwarg):
        """ Initialization that builds the container
        
        Assumptions:
            None
    
        Source:
           None 
        """          
        super(Container,self).__init__(*args,**kwarg)
        self.__defaults__()
    
    def append(self,val):
        """ Appends the value to the containers
            This overrides the Data class append by allowing for duplicate named components
            The following components will get new names.
        
        Assumptions:
            None
    
        Source:
           None
    
        Args:
           None
    
        Returns:
           None 
        """           
        
        # See if the item tag exists, if it does modify the name
        keys = self.keys()
        
        tag = str.lower(val.tag.translate(t_table))
        if tag in keys:
            string_of_keys = "".join(self.keys())
            n_comps = string_of_keys.count(val.tag)
            val.tag = tag + str(n_comps+1)
            
            # Check again, because theres an outside chance that its duplicate again. Then assign a random
            if val.tag in keys:
                val.tag = tag + str(n_comps+random.randint(0,1000))
        
        Data.append(self,val)
        
    def extend(self,vals):
        """ Append things regressively depending on what is inside.
        
        Assumptions:
            None
    
        Source:
           None
    
        Args:
           None
    
        Returns:
           None 
        """         
        if isinstance(vals,(list,tuple)):
            for v in vals: self.append(v)
        elif isinstance(vals,dict):
            self.update(vals)
        else:
            raise Exception('unrecognized data type')