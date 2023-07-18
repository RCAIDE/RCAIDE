## @ingroup Analyses
# RCAIDE/Analyses/Vehicle.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
import RCAIDE
from .Analysis import Analysis

# ----------------------------------------------------------------------------------------------------------------------
# Vehicle
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Analyses
class Vehicle(Analysis.Container):
    """ RCAIDE.Analyses.Vehicle()
    
        The Vehicle Analyses Container Class
        
            Assumptions:
            None
            
            Source:
            N/A
    """
    def __defaults__(self):
        """This sets the default analyses to be applied to the vehicle.
        
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
        self.aerodynamics = None
        self.atmosphere   = None
        self.costs        = None
        self.energy       = None
        self.noise        = None
        self.planet       = None
        self.sizing       = None
        self.stability    = None
        self.weights      = None

    def append(self,analysis):
        """This is used to add new analyses to the container.
        
                Assumptions:
                None
                
                Source:
                N/A
                
                Inputs:
                Analysis to be added
                
                Outputs:
                None
                
                Properties Used:
                N/A
        """

        key = self.get_root(analysis) 
        self[key] = analysis 
    _analyses_map = None

    def __init__(self,*args,**kwarg):
        """This sets the initialization behavior of the vehicle analysis
           container. Maps analysis paths to string keys.
           
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

        Analysis.Container.__init__(self,*args,**kwarg)

        self._analyses_map = { 
            RCAIDE.Analyses.Weights.Weights           : 'weights'      ,
            RCAIDE.Analyses.Aerodynamics.Aerodynamics : 'aerodynamics' ,
            RCAIDE.Analyses.Stability.Stability       : 'stability'    ,
            RCAIDE.Analyses.Energy.Energy             : 'energy'       ,
            RCAIDE.Analyses.Atmospheric.Atmospheric   : 'atmosphere'   ,
            RCAIDE.Analyses.Planets.Planet            : 'planet'       ,
            RCAIDE.Analyses.Noise.Noise               : 'noise'        ,
            RCAIDE.Analyses.Costs.Costs               : 'costs'        ,
        }

    def get_root(self,analysis):

        """ This is used to determine the root of the analysis path associated
            with a particular analysis key by the analysis map.
            
                Assumptions:
                None
                
                Source:
                N/A
                
                Inputs:
                Analysis key to be checked
                
                Outputs:
                Path root of analysis
                
                Properties Used:
                N/A
                
                
        """
        for analysis_type, analysis_root in self._analyses_map.items():
            if isinstance(analysis,analysis_type):
                break
        else:
            raise Exception("Unable to place analysis type %s" % analysis.typestring())

        return analysis_root


