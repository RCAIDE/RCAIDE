# RCAIDE/Compoments/Booms/Boom.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports 
from RCAIDE.Reference.Components import Component
from RCAIDE.Reference.Core import Data, Container
 
# ----------------------------------------------------------------------------------------------------------------------
# Boom 
# ----------------------------------------------------------------------------------------------------------------------  
class Boom(Component):
    """This is a standard boom for a rotor"""
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """       
        
        self.tag                                    = 'boom'
        self.origin                                 = [[0.0,0.0,0.0]]
        self.aerodynamic_center                     = [0.0,0.0,0.0]  
                 
        self.areas                                  = Data()
        self.areas.front_projected                  = 0.0
        self.areas.side_projected                   = 0.0
        self.areas.wetted                           = 0.0
                         
        self.effective_diameter                     = 0.0
        self.width                                  = 0.0 
                         
        self.heights                                = Data()
        self.heights.maximum                        = 0.0
        self.heights.at_quarter_length              = 0.0
        self.heights.at_three_quarters_length       = 0.0
        self.heights.at_wing_root_quarter_chord     = 0.0
        self.heights.at_vertical_root_quarter_chord = 0.0
        
        self.x_rotation                             = 0.0
        self.y_rotation                             = 0.0
        self.z_rotation                             = 0.0
             
        self.lengths                                = Data()
        self.lengths.nose                           = 0.0
        self.lengths.tail                           = 0.0
        self.lengths.total                          = 0.0
        self.lengths.cabin                          = 0.0
        self.lengths.fore_space                     = 0.0
        self.lengths.aft_space                      = 0.0
                 
        self.fineness                               = Data()
        self.fineness.nose                          = 0.0
        self.fineness.tail                          = 0.0
              
        # For VSP     
        self.vsp_data                               = Data()
        self.vsp_data.xsec_surf_id                  = ''    # There is only one XSecSurf in each VSP geom.
        self.vsp_data.xsec_num                      = None  # Number if XSecs in rotor_boom geom.
                        
        self.Segments                               = Container()
        
    def append_segment(self,segment):
        """ Adds a segment to the rotor_boom. 
    
        Assumptions:
            None
            
        Source:
            None
        
        Args:
            self    (dict): boom                  [-]
            segment (dict): cross-section of boom [-]   
            
        Returns:
            None 
        """ 

        # Assert database type
        if not isinstance(segment,Data):
            raise Exception('input component must be of type Data()')

        # Store data
        self.Segments.append(segment) 
        
        return 

# ------------------------------------------------------------
#  Handle Linking
# ------------------------------------------------------------ 
Boom.Container = Container
