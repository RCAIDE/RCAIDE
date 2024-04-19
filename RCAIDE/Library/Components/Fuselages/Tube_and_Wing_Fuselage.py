## @ingroup Library-Components-Fuselages
# RCAIDE/Compoments/Fuselages/Tube_and_Wing_Fuselage.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports     
from .Fuselage import Fuselage
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Tube_and_Wing_Fuselage
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Components-Fuselages 
class Tube_and_Wing_Fuselage(Fuselage):
    """ This is a standard fuselage for a tube and wing aircraft.
    
    Assumptions:
    Conventional fuselage
    
    Source:
    N/A
    """
    
    def __defaults__(self):
        """ This sets the default values for the component to function.
        
        Assumptions:
        None
    
        Source:
        N/A
    
        Inputs:
        None
    
        Outputs:
        None
    
        Properties Used:
        None
        """      
        
        self.tag                                    = 'fuselage'
        self.origin                                 = [[0.0,0.0,0.0]]
        self.aerodynamic_center                     = [0.0,0.0,0.0] 
        self.differential_pressure                  = 0.0    
        self.seats_abreast                          = 0.0
        self.seat_pitch                             = 0.0
 
        self.areas.front_projected                  = 0.0
        self.areas.side_projected                   = 0.0
        self.areas.wetted                           = 0.0
        
        self.effective_diameter                     = 0.0
        self.width                                  = 0.0
         
        self.heights.maximum                        = 0.0
        self.heights.at_quarter_length              = 0.0
        self.heights.at_three_quarters_length       = 0.0
        self.heights.at_wing_root_quarter_chord     = 0.0
        self.heights.at_vertical_root_quarter_chord = 0.0
        
        self.x_rotation                             = 0.0
        self.y_rotation                             = 0.0
        self.z_rotation                             = 0.0
                              
        self.lengths.nose                           = 0.0
        self.lengths.tail                           = 0.0
        self.lengths.total                          = 0.0
        self.lengths.cabin                          = 0.0
        self.lengths.fore_space                     = 0.0
        self.lengths.aft_space                      = 0.0 
                                  
        self.fineness.nose                          = 0.0
        self.fineness.tail                          = 0.0 
        self.nose_curvature                         = 1.5
        self.tail_curvature                         = 1.5   
  