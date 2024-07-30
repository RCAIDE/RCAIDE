## @ingroup Library-Missions-Segments-Common-Pre_Process
# RCAIDE/Library/Missions/Common/Pre_Process/energy.py
# 
# 
# Created:  Jul 2023, M. Clarke

import  RCAIDE
 
# ----------------------------------------------------------------------------------------------------------------------
#  energy
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Missions-Segments-Common-Pre_Process

    
def unpack_unknowns(segment, fuel_lines):
    """Unpacks the unknowns set in the mission to be available for the mission.

    Assumptions:
    N/A
    
    Source:
    N/A
    
    Inputs: 
        segment   - data structure of mission segment [-]
    
    Outputs: 
    
    Properties Used:
    N/A
    """            
     
    
    RCAIDE.Library.Mission.Common.Unpack_Unknowns.energy.fuel_line_unknowns(segment,fuel_lines) 
        
    return        



def energy(mission):
    """ Appends all unknows and residuals to the network 
    
        Assumptions:
            N/A
        
        Inputs:
            None
            
        Outputs:
            None 

        Properties Used:
        N/A                
    """
    
    i =  0
    for segment in mission.segments:
        for network in segment.analyses.energy.networks:
            for distribution_line in network.distribution_lines:
                for propulsor in  distribution_line.propulsors:
                    propulsor.add_unknowns_and_residuals_to_segment(segment, distribution_line, propulsor, i)
                    i = i + 1
                for fuel_tank in  distribution_line.fuel_tanks:
                    fuel_tank.add_unknowns_and_residuals_to_segment(segment, distribution_line, fuel_tank)
            segment.process.iterate.unknowns.network   = unpack_unknowns(segment, network.distribution_lines)
        
    return 