## @ingroup Analyses
# RCAIDE/Framework/Analyses/Analysis.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Framework.Core import Container as ContainerBase
from RCAIDE.Framework.Core import Data

# ----------------------------------------------------------------------------------------------------------------------
# Analysis
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Analyses
class Analysis(Data):
    """ The Top Level Analysis Class
        
        Assumptions:
           None
        
        Source:
           None
    """
    def __defaults__(self):
        """This sets the default values and methods for the analysis.
        
            Assumptions:
                None
    
            Source:
                None
    
            Args:
                None
    
            Returns:
                None 
            """           
        self.tag    = 'analysis'
        self.features = Data()
        self.settings = Data() 
        
    def initialize(self,*args,**kwarg):
        """Initializes the analysis' specific algorithms.
        
            Assumptions:
                None
                                            
            Source:
                None
                                            
            Args:
                self  : class                           [-] 
                args  : arguments of the class          [-]
                kwarg : keyword arguments of the classs [-]
                                            
            Returns:
                None
            """        
        return
    
    def evaluate(self,*args,**kwarg):
        """This is used to execute the analysis' specific algorithms.
        
            Assumptions:
                None
                                            
            Source:
                None
                                            
            Args:
                self  : class                           [-] 
                args  : arguments of the class          [-]
                kwarg : keyword arguments of the classs [-]
                                            
            Returns:
                None
                
            """             
        raise NotImplementedError 
    
    def post_process(self,*args,**kwarg):
        """Postprocess set of an analysis method
        
            Assumptions:
                None
                                            
            Source:
                None
                                            
            Args:
                self  : class                           [-] 
                args  : arguments of the class          [-]
                kwarg : keyword arguments of the classs [-]
                                            
            Returns:
                None
            """                
        return 
    
    def __call__(self,*args,**kwarg):
        
        """This is used to set the class' call behavior to the evaluate function. 
                                                
            Assumptions:
                None
                                            
            Source:
                None
                                            
            Args:
                self  : class                           [-] 
                args  : arguments of the class          [-]
                kwarg : keyword arguments of the classs [-]
                                            
            Returns:
                results : results of evaluation function [-]
            """                 
        
        return self.evaluate(*args,**kwarg)
    
    
# ----------------------------------------------------------------------------------------------------------------------  
#  CONFIG CONTAINER
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Analyses
class Container(ContainerBase):
    """The Analysis Container Class
        
        Assumptions:
            None
        
        Source:
            None
    """ 
        
    def initialize(self,*args,**kwarg):
        """This is used to execute the initialize functions of the analyses
            stored in the container.
                                        
            Assumptions:
                None
                                    
            Source:
                None
                                    
            Args:
                self  : class                           [-] 
                args  : arguments of the class          [-]
                kwarg : keyword arguments of the classs [-]
                                    
            Returns:
                None 
            """                    
        for tag,analysis in self.items:
            if hasattr(analysis,'initialize'):
                analysis.initialize(*args,**kwarg) 
    
    def evaluate(self,*args,**kwarg):
        """This is used to execute the evaluate functions of the analyses
            stored in the container.
                                                
            Assumptions:
                None
                                            
            Source:
                None
                                            
            Args:
                self  : class                           [-] 
                args  : arguments of the class          [-]
                kwarg : keyword arguments of the classs [-]
                                            
            Returns:
                results : results of evaluation function [-]
            """
        results = Data()
        for tag,analysis in self.items(): 
            if hasattr(analysis,'evaluate'):
                result = analysis.evaluate(*args,**kwarg)
            else:
                result = analysis(*args,**kwarg)
            results[tag] = result
        return results
    
    def post_process(self,*args,**kwarg):
        """This is used to execute post processing functions 
                                                
           Assumptions:
               None
                                           
           Source: 
                                           
           Args:
                self  : class                           [-] 
                args  : arguments of the class          [-]
                kwarg : keyword arguments of the classs [-]
                                           
           Returns:
               None 
            """        
        
        for tag,analysis in self.items():
            if hasattr(analysis,'post_process'):
                analysis.post_process(*args,**kwarg)
                
    
    def __call__(self,*args,**kwarg): 
        """This is used to set the class' call behavior to the evaluate functions.
                                                        
            Assumptions:
                None
                                                    
            Source:
                None
                                                    
            Args:
                self  : class                           [-] 
                args  : arguments of the class          [-]
                kwarg : keyword arguments of the classs [-]
                                                    
            Returns:
                evaluation function
              
            """                
        
        return self.evaluate(*args,**kwarg)

    
# ----------------------------------------------------------------------------------------------------------------------   
#  LINKING
# ----------------------------------------------------------------------------------------------------------------------   
Analysis.Container = Container