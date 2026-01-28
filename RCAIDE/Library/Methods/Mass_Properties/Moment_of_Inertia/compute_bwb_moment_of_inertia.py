# RCAIDE/Library/Methods/Mass_Properties/Moment_of_Inertia/compute_bwb_moment_of_inertia.py 
# 
# Created:  January 2026, S. Shekar, A. Molloy M. Clarke,  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import RCAIDE

# package imports 
import numpy as np  
from   copy import deepcopy
import shapely.geometry as geom
from shapely import Polygon, box 
import trimesh

# ----------------------------------------------------------------------------------------------------------------------
#  Compute Blended Wing Body Moment of Inertia
# ----------------------------------------------------------------------------------------------------------------------  
def compute_bwb_moment_of_inertia(bwb_wing, center_of_gravity = [[0, 0, 0]]): 
    ''' computes the moment of inertia tensor for a blended wing body about a given center of gravity.
    Includes the ability to model a  wing fuel tank as a condensed wing

    Assumptions:
    - Wing is solid
    - Wing has a constant density

    Source:
    [1] Moulton, B. C., and Hunsaker, D. F., “Simplified Mass and Inertial Estimates for Aircraft with Components
    of Constant Density,” AIAA SCITECH 2023 Forum, January 2023, AIAA-2023-2432 DOI: 10.2514/
    6.2023-2432
    
    [2] Fuel tank references: These were used to estimate the length percentages. 
    - https://assets.publishing.service.gov.uk/media/5422fa1aed915d13710007a1/2-2007_G-YMME.pdf
    - https://oat.aero/2023/03/17/airbus-a380-general-familiarisation-fuel-storage/
    - http://www.b737.org.uk/fuel.htm
    - https://slideplayer.com/slide/3854059/
    
    Inputs:
    - Wing
    - Wing mass
    - Center of gravity
    - Fuel flag (whether the wing is considered a fuel tank or not)

    Outputs:
    - wing moment of inertia tensor

    Properties Used:
    N/A
    '''

    
    """Compute total MOI about a specified CG.""" 

    ## compute cabin moment of inertia 
    #compute_center_body_moment_of_inertia(bwb_wing.center_body,center_of_gravity)
    
    ## compute aft cabin moment of inertia 
    #compute_aft_center_body_moment_of_inertia(bwb_wing.aft_center_body,center_of_gravity)
     
    ## compute wing moment of intertia 
    #compute_bwb_wing_moment_of_inertia(bwb_wing,center_of_gravity) 

    return  bwb_wing.mass_properties.moments_of_inertia.tensor, bwb_wing.mass_properties.mass   