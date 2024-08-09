## @ingroup Components-Propulsors-Electric_Rotor
# RCAIDE/Library/Components/Propulsors/Electric_Rotor.py
# 
# 
# 
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports 
from .   import Propulsor 
from RCAIDE.Library.Methods.Propulsors.Electric_Rotor_Propulsor.unpack_electric_rotor_unknowns       import unpack_electric_rotor_unknowns
from RCAIDE.Library.Methods.Propulsors.Electric_Rotor_Propulsor.pack_electric_rotor_residuals        import pack_electric_rotor_residuals
from RCAIDE.Library.Methods.Propulsors.Electric_Rotor_Propulsor.append_electric_rotor_conditions     import append_electric_rotor_conditions
from RCAIDE.Library.Methods.Propulsors.Electric_Rotor_Propulsor.compute_electric_rotor_performance   import compute_electric_rotor_performance, reuse_stored_electric_rotor_data

# ----------------------------------------------------------------------
#  Fan Component
# ----------------------------------------------------------------------
## @ingroup Components-Propulsors-Converters
class Electric_Rotor(Propulsor):
    """This is a electric motor-rotor propulsor 
    
    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):    
        # setting the default values
        self.tag                          = 'electric_rotor'   
        self.active_batteries             = None
        self.motor                        = None
        self.rotor                        = None 
        self.electronic_speed_controller  = None   
 

    def append_operating_conditions(self,segment,bus,add_additional_network_equation = False):
        append_electric_rotor_conditions(self,segment,bus,add_additional_network_equation)
        return

    def unpack_propulsor_unknowns(self,segment,bus,add_additional_network_equation = False):  
        unpack_electric_rotor_unknowns(self,segment,bus,add_additional_network_equation)
        return 

    def pack_propulsor_residuals(self,segment,bus,add_additional_network_equation = False): 
        pack_electric_rotor_residuals(self,segment,bus,add_additional_network_equation)
        return    
    
    def compute_performance(self,state,bus,voltage,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power,current,stored_results_flag,stored_propulsor_tag =  compute_electric_rotor_performance(self,state,bus,voltage,center_of_gravity)
        return thrust,moment,power,stored_results_flag,stored_propulsor_tag
    
    def reuse_stored_data(turboshaft,state,bus,stored_propulsor_tag,center_of_gravity = [[0, 0, 0]]):
        thrust,moment,power,current, = reuse_stored_electric_rotor_data(turboshaft,state,bus,stored_propulsor_tag,center_of_gravity)
        return thrust,moment,power,current,
