## @ingroup Components-Propulsors 
# RCAIDE/Library/Components/Propulsors/Constant_Speed_ICE_Propeller.py
# 
# 
# 
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from .                import Propulsor 
from RCAIDE.Library.Methods.Propulsors.Constant_Speed_ICE_Propulsor.append_ice_cs_propeller_conditions  import append_ice_cs_propeller_conditions
from RCAIDE.Library.Methods.Propulsors.Constant_Speed_ICE_Propulsor.compute_cs_ice_performance          import compute_cs_ice_performance, reuse_stored_ice_cs_prop_data
 
# ----------------------------------------------------------------------
#  Fan Component
# ----------------------------------------------------------------------
## @ingroup Components-Propulsors-Converters
class Constant_Speed_ICE_Propeller(Propulsor):
    """This is an internal engine-propeller propulsor
    
    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):    
        # setting the default values
        self.tag                          = 'ice_constant_speed_propeller'   
        self.active_fuel_tanks            = None
        self.engine                       = None
        self.propeller                    = None  
          

    def append_operating_conditions(self,segment,fuel_line,add_additional_network_equation = False):
        append_ice_cs_propeller_conditions(self,segment,fuel_line,add_additional_network_equation)
        return

    def unpack_propulsor_unknowns(self,segment,fuel_line,add_additional_network_equation = False):   
        return 

    def pack_propulsor_residuals(self,segment,fuel_line,add_additional_network_equation = False): 
        return        
    
    def compute_performance(self,state,fuel_line,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power,stored_results_flag,stored_propulsor_tag =  compute_cs_ice_performance(self,state,fuel_line,center_of_gravity)
        return thrust,moment,power,stored_results_flag,stored_propulsor_tag
    
    def reuse_stored_data(ICE_cs_prop,state,fuel_line,stored_propulsor_tag,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power  = reuse_stored_ice_cs_prop_data(ICE_cs_prop,state,fuel_line,stored_propulsor_tag,center_of_gravity)
        return thrust,moment,power           
 
