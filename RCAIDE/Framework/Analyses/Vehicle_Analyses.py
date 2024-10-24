# RCAIDE/Framework/Analyses/Vehicle.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
import RCAIDE
from .Analysis import Analysis

# ----------------------------------------------------------------------------------------------------------------------
# Vehicle
# ----------------------------------------------------------------------------------------------------------------------   
class Vehicle_Analyses(Analysis.Container):
    """ The Vehicle Analyses Container Class 
    """
    def __defaults__(self):
        """This sets the default analyses to be applied to the vehicle.
        
            Assumptions:
                None
            
            Source:
                None
            
            Args:
                None
            
            Returns:
                None
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
                None
            
            Args:
                Analysis to be added
            
            Returns:
                None
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
               None
            
            Args:
                None
            
            Returns:
                None
        """

        Analysis.Container.__init__(self,*args,**kwarg)

        self._analyses_map = { 
            RCAIDE.Framework.Analyses.Weights.Weights           : 'weights'      ,
            RCAIDE.Framework.Analyses.Aerodynamics.Aerodynamics : 'aerodynamics' ,
            RCAIDE.Framework.Analyses.Stability.Stability       : 'stability'    ,
            RCAIDE.Framework.Analyses.Energy.Energy             : 'energy'       ,
            RCAIDE.Framework.Analyses.Atmospheric.Atmospheric   : 'atmosphere'   ,
            RCAIDE.Framework.Analyses.Planets.Planet            : 'planet'       ,
            #RCAIDE.Framework.Analyses.Noise.Noise               : 'noise'        ,
            RCAIDE.Framework.Analyses.Costs.Costs               : 'costs'        ,
        }

    def get_root(self,analysis):

        """ This is used to determine the root of the analysis path associated
            with a particular analysis key by the analysis map.
            
            Assumptions:
                None
            
            Source:
                None
            
            Args:
                Analysis key to be checked
            
            Returns:
                Path root of analysis  
        """
        for analysis_type, analysis_root in self._analyses_map.items():
            if isinstance(analysis,analysis_type):
                break
        else:
            raise Exception("Unable to place analysis type %s" % analysis.typestring())

        return analysis_root


