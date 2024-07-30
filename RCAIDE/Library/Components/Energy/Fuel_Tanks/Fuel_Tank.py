## @ingroup Library-Compoments-Energy-Fuel_Tanks Fuel_Tanks
# RCAIDE/Library/Compoments/Energy/Fuel_Tanks/Fuel_Tank.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
import  RCAIDE
from RCAIDE.Framework.Core              import Data 
from RCAIDE.Framework.Mission.Common    import Residuals  
from RCAIDE.Library.Components          import Component

import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Tank
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Library-Compoments-Energy-Fuel_Tanks 
class Fuel_Tank(Component):
    """Fuel tank compoment.
    """
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """          
        self.tag                         = 'fuel_tank'
        self.type                        = 'fuel_tanks'
        self.fuel_selector_ratio         = 1.0 
        self.mass_properties.empty_mass  = 0.0   
        self.secondary_fuel_flow         = 0.0
        self.fuel                        = None
        
    #def unpack_unknowns(self,segment,fuel_line, fuel_tank):
        #"""Unpacks the unknowns set in the mission to be available for the mission.

        #Assumptions:
        #N/A

        #Source:
        #N/A

        #Inputs: 
            #segment   - data structure of mission segment [-]

        #Outputs: 

        #Properties Used:
        #N/A
        #"""            


        #RCAIDE.Library.Mission.Common.Unpack_Unknowns.energy.fuel_line_unknowns(segment,fuel_line, fuel_tank) 

        #return                    
        
    
                
    def add_unknowns_and_residuals_to_segment(self, segment, fuel_line, fuel_tank):
            
        ones_row    = segment.state.ones_row 
        
    
        segment.state.conditions.energy[fuel_line.tag]       = RCAIDE.Framework.Mission.Common.Conditions()
        segment.state.conditions.energy[fuel_line.tag].fuel_tank       = RCAIDE.Framework.Mission.Common.Conditions()   
        fuel_line_results                                    = segment.state.conditions.energy.distribution_lines[fuel_line.tag]        

                  
        fuel_line_results[fuel_tank.tag]                 = RCAIDE.Framework.Mission.Common.Conditions()  
        fuel_line_results[fuel_tank.tag].mass_flow_rate  = ones_row(1)  
        fuel_line_results[fuel_tank.tag].mass            = ones_row(1)
        
        #segment.process.iterate.unknowns.network   = self.unpack_unknowns(segment, fuel_line,fuel_tank)                   
        return segment            
            