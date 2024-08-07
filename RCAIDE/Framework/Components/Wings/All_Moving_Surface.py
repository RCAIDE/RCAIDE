# RCAIDE/Compoments/Wings/All_Moving_Surface.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports     
from RCAIDE.Framework.Components import Component
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  All_Moving_Surface
# ----------------------------------------------------------------------------------------------------------------------  
class All_Moving_Surface(Component):
    """ This class is used to allow every all-moving control surface class
    (e.g. Stabilator) to inherit from both a type of Wing (Horizontal_Tail
    in the case of a Stabilator) and this class. This, way All_Moving_Surface
    subclasses can inherit necessary functionality without code bloat or 
    lengthy type checking if-statements.
    
    In general, this class should not be used directly, and should only exist
    as one of the parents of another class that also inherits from Wing   
    """ 

    def __defaults__(self):
        """This sets the default for All_Moving_Surface objects in RCAIDE.
        
        Assumptions:   
        use_constant_hinge_fraction: false by default. If this is true, the hinge vector 
            will follow a constant chord_fraction allong the wing, regardless of what is set
            for hinge_vector. Note that constant hinge fractions are how hinges are handled for 
            Control_Surfaces. If this attribute is false, the hinge vector is described by
            the hinge_vector attribute
        hinge_vector: The vector in body-frame that the hingeline points along. By default, 
            it is [0,0,0], and this is taken to mean that the hinge line is normal to the root
            chord, in-plane with the wing. This attribute does nothing if use_constant_hinge_fraction
            is set to True. 
        
        Source:
            None 
        """ 
        self.tag                         = 'all_moving_surface' 
        self.sign_duplicate              = 1.0
        self.hinge_fraction              = 0.25
        self.deflection                  = 0.0   
        self.Segments                    = Data()   
        self.use_constant_hinge_fraction = False
        self.hinge_vector                = np.array([0.,0.,0.])
