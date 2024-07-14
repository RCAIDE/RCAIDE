## @ingroup Library-Missions-Segments-Common-Update
# RCAIDE/Library/Missions/Common/Update/emissions.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  emissions
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Library-Missions-Segments-Common-Update
def emissions(segment):
    """ Updates the emissions produced by the vehicle
        
        Assumptions:
        N/A
        
        Inputs:
            None 
                 
        Outputs: 
            None
      
        Properties Used:
        N/A
                    
    """   
    emissions_model = segment.analyses.emissions
    
    if emissions_model:
        emissions_model.evaluate_emissions(segment)    