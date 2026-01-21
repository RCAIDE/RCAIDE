# RCAIDE/Library/Methods/Powertrain/Converters/Pump/compute_pump_mass_from_power_density.py
# 
# Created:  Jan 2026, M. Clarke

# ---------------------------------------------------------------------------------------------------------------------- 
#  RCAIDE imports 
# ----------------------------------------------------------------------------------------------------------------------  
import RCAIDE

# ---------------------------------------------------------------------------------------------------------------------- 
#  compute_pump_mass_from_power_density
# ----------------------------------------------------------------------------------------------------------------------    
def compute_pump_mass_from_power_density(pump):
    
    if isinstance(pump.working_fluid,RCAIDE.Library.Attributes.Coolants) or\
       isinstance(pump.working_fluid,RCAIDE.Library.Attributes.Propellants):
        raise AssertionError('Working fluid must be either a coolant or propellant!')  
         
        
    # compute delta P
    pressure_rise = pump.design_outlet_pressure - pump.design_inlet_pressure

    # mass flow 
    m_dot  = pump.design_mass_flow_rate 

    # volumetric flow rate
    Q  = m_dot /pump.working_fluid.density

    # hydraulic power
    Hydraulic_Power  =  Q * pressure_rise

    # mass of pump 
    total_efficiency =  pump.pump_efficiency * pump.turbine_efficiency

    # shaft power 
    Shaft_Power = Hydraulic_Power / total_efficiency

    # mass 
    mass = Shaft_Power / pump.power_density 
    pump.mass_properties.mass = mass   

    return  