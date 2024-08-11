# RCAIDE/Library/Methods/Propulsors/Electric_Rotor_Propulsor/append_electric_rotor_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
 # RCAIDE imports 
import RCAIDE  
from RCAIDE.Framework.Mission.Common                      import Conditions 
from RCAIDE.Library.Components.Propulsors.Converters.Propeller   import Propeller 
from RCAIDE.Library.Components.Propulsors.Converters.Lift_Rotor  import Lift_Rotor 
from RCAIDE.Library.Components.Propulsors.Converters.Prop_Rotor  import Prop_Rotor 


# ---------------------------------------------------------------------------------------------------------------------- 
#  append electric rotor network conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_electric_rotor_conditions(propulsor,segment,bus,add_additional_network_equation): 
    ones_row    = segment.state.ones_row
                
    segment.state.conditions.energy[bus.tag][propulsor.tag]                      = Conditions()  
    segment.state.conditions.energy[bus.tag][propulsor.tag].throttle             = 0. * ones_row(1)      
    segment.state.conditions.energy[bus.tag][propulsor.tag].orientation          = 0. * ones_row(1)  
    segment.state.conditions.energy[bus.tag][propulsor.tag].thrust               = 0. * ones_row(3) 
    segment.state.conditions.energy[bus.tag][propulsor.tag].power                = 0. * ones_row(1) 
    segment.state.conditions.energy[bus.tag][propulsor.tag].moment               = 0. * ones_row(3)  
    segment.state.conditions.noise[bus.tag][propulsor.tag]                       = Conditions()

    if type(segment) == RCAIDE.Framework.Mission.Segments.Ground.Battery_Recharge: 
        segment.state.conditions.energy.recharging  = True 
        segment.state.unknowns['recharge']          =  0* ones_row(1)  
        segment.state.residuals.network['recharge'] =  0* ones_row(1)
    else:
        segment.state.conditions.energy.recharging = False   
        if add_additional_network_equation:                       
            rotor   = propulsor.rotor  
            if type(rotor) == Propeller:
                cp_init  = float(rotor.cruise.design_power_coefficient)
            elif (type(rotor) == Lift_Rotor) or (type(rotor) == Prop_Rotor):
                cp_init  = float(rotor.hover.design_power_coefficient)    
            segment.state.unknowns[ propulsor.tag  + '_rotor_cp']                    = cp_init * ones_row(1)  
            segment.state.residuals.network[ propulsor.tag  + '_rotor_motor_torque'] = 0. * ones_row(1)    
    return