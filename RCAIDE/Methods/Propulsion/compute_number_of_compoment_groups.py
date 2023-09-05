# RCAIDE/Methods/Propulsion/compute_number_of_compoment_groups.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke
  
# ----------------------------------------------------------------------------------------------------------------------
#  compute_number_of_compoment_groups
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Propulsion 
def compute_number_of_compoment_groups(components,active_propulsor_groups): 
    '''Looped through compoments and determine the number of unique propulsor groups
    
        Assumptions:
        None

        Source:
        N/A

        Inputs:
        components              - compoment data structure     [-]
        active_propulsor_groups - active propulsor group tags  [string(s)]
        
        Outputs: 
        comp_group_indexes      - component group indexes      [-]
        comp_groups             - compoment groups             [string(s)]
        unique_tags             - unique compoment tags        [string(s)]

        Properties Used:
        N/A
    ''' 
    comp_groups        = [] 
    comp_group_indexes = []
    group_iterator     = 0 
    unique_tags        = []
    for comp in components: 
        for i in range(len(active_propulsor_groups)):  
            if comp.propulsor_group == active_propulsor_groups[i]:
                if (comp.propulsor_group) in comp_groups: 
                    # find index in list  
                    c_i = comp_groups.index(comp.propulsor_group)
                    
                    # append it to group index 
                    comp_group_indexes.append(c_i)
                    
                else: 
                    unique_tags.append(comp.tag)
                    comp_groups.append(comp.propulsor_group)
        
                    # append it to group index 
                    comp_group_indexes.append(group_iterator) 
                    
                    # increment iterator 
                    group_iterator+= 1  
    return comp_group_indexes,comp_groups,unique_tags  