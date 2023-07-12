# RCAIDE/Analyses/Analysis.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Core import Container as ContainerBase

# Legacy imports   
from Legacy.trunk.S.Core import Data

# ----------------------------------------------------------------------------------------------------------------------
# ANALYSIS
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Analyses
class Analysis(Data):
    """ RCAIDE.Analyses.Analysis()
    
        The Top Level Analysis Class
        
            Assumptions:
            None
            
            Source:
            N/A
    """
    def __defaults__(self):
        """This sets the default values and methods for the analysis.
        
                Assumptions:
                None
        
                Source:
                N/A
        
                Inputs:
                None
        
                Outputs:
                None
        
                Properties Used:
                N/A
            """           
        self.tag    = 'analysis'
        self.features = Data()
        self.settings = Data()
    
    def compile(self,*args,**kwarg):
        """This is used to compile the data, settings, etc. used in the
           analysis' specific algorithms.
                
                Assumptions:
                None
                
                Source:
                N/A
                
                Inputs:
                None
                
                Outputs:
                None
                
                Properties Used:
                N/A
            """        
        
        return
        
    def initialize(self,*args,**kwarg):
        """This is used to initialize the analysis' specific algorithms.
                
                Assumptions:
                None
                
                Source:
                N/A
                
                Inputs:
                None
                
                Outputs:
                None
                
                Properties Used:
                N/A
            """        
        return
    
    def evaluate(self,*args,**kwarg):
        """This is used to execute the analysis' specific algorithms.
                
                Assumptions:
                None
                
                Source:
                N/A
                
                Inputs:
                None
                
                Outputs:
                None
                
                Properties Used:
                N/A
            """             
        raise NotImplementedError
        return Data()
    
    def finalize(self,*args,**kwarg):
        """This is used to finalize the analysis' specific algorithms.
                
                Assumptions:
                None
                
                Source:
                N/A
                
                Inputs:
                None
                
                Outputs:
                None
                
                Properties Used:
                N/A
            """                
        return 
    
    def __call__(self,*args,**kwarg):
        
        """This is used to set the class' call behavior to the evaluate function.
                        
                Assumptions:
                None
                        
                Source:
                N/A
                        
                Inputs:
                None
                        
                Outputs:
                None
                        
                Properties Used:
                N/A
            """                        
        
        return self.evaluate(*args,**kwarg)
    

# ----------------------------------------------------------------------
#  Config Container
# ----------------------------------------------------------------------

## @ingroup Analyses
class Container(ContainerBase):
    """ RCAIDE.Analyses.Analysis.Container()
    
        The Analysis Container Class
        
            Assumptions:
            None
            
            Source:
            N/A
    """
    
    def compile(self,*args,**kwarg):
        """This is used to execute the compile functions of the analyses
           stored in the container.
                                
                Assumptions:
                None
                                
                Source:
                N/A
                                
                Inputs:
                None
                                
                Outputs:
                None
                                
                Properties Used:
                N/A
            """            
        for tag,analysis in self.items():
            if hasattr(analysis,'compile'):
                analysis.compile(*args,**kwarg)
        
    def initialize(self,*args,**kwarg):
        """This is used to execute the initialize functions of the analyses
            stored in the container.
                                        
                Assumptions:
                None
                                        
                Source:
                N/A
                                        
                Inputs:
                None
                                        
                Outputs:
                None
                                        
                Properties Used:
                N/A
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
                N/A
                                                
                Inputs:
                None
                                                
                Outputs:
                Results of the Evaluate Functions
                                                
                Properties Used:
                N/A
            """
        results = Data()
        for tag,analysis in self.items(): 
            if hasattr(analysis,'evaluate'):
                result = analysis.evaluate(*args,**kwarg)
            else:
                result = analysis(*args,**kwarg)
            results[tag] = result
        return results
    
    def finalize(self,*args,**kwarg):
        """This is used to execute the finalize functions of the analyses
            stored in the container.
                                                
                Assumptions:
                None
                                                
                Source:
                N/A
                                                
                Inputs:
                None
                                                
                Outputs:
                None
                                                
                Properties Used:
                N/A
            """        
        
        for tag,analysis in self.items():
            if hasattr(analysis,'finalize'):
                analysis.finalize(*args,**kwarg)
    
    def __call__(self,*args,**kwarg): 
        """This is used to set the class' call behavior to the evaluate functions.
                                                        
                Assumptions:
                None
                                                        
                Source:
                N/A
                                                        
                Inputs:
                None
                                                        
                Outputs:
                None
                                                        
                Properties Used:
                N/A
            """                
        
        return self.evaluate(*args,**kwarg)


# ------------------------------------------------------------
#  Handle Linking
# ------------------------------------------------------------

Analysis.Container = Container