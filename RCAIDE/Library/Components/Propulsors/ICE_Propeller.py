## @ingroup Components-Propulsors 
# RCAIDE/Library/Components/Propulsors/ICE_Propeller.py
# 
# 
# 
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from .                import Propulsor  
from RCAIDE.Library.Methods.Propulsors.ICE_Propulsor.append_ICE_prop_conditions     import append_ICE_prop_conditions 
from RCAIDE.Library.Methods.Propulsors.ICE_Propulsor.compute_ICE_prop_performance   import compute_ICE_prop_performance, reuse_stored_ICE_prop_data
 

# ----------------------------------------------------------------------
#  Fan Component
# ----------------------------------------------------------------------
## @ingroup Components-Propulsors-Converters
class ICE_Propeller(Propulsor):
    """This is an internal engine-propeller propulsor
    
    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):    
        # setting the default values
        self.tag                          = 'ICE_propeller'   
        self.active_fuel_tanks            = None
        self.engine                       = None
        self.propeller                    = None   
 

    def append_operating_conditions(self,segment,fuel_line):
        append_ICE_prop_conditions(self,segment,fuel_line)
        return
    
    def compute_performance(self,state,fuel_line,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power,stored_results_flag,stored_propulsor_tag =  compute_ICE_prop_performance(self,state,fuel_line,center_of_gravity)
        return thrust,moment,power,stored_results_flag,stored_propulsor_tag
    
    def reuse_stored_data(ICE_prop,state,fuel_line,stored_propulsor_tag,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power  = reuse_stored_ICE_prop_data(ICE_prop,state,fuel_line,stored_propulsor_tag,center_of_gravity)
        return thrust,moment,power 