# RCAIDE/Library/Methods/Powertrain/Converters/Pump/compute_pump_performance.py

# 
# Created:  Jan 2026, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports
import  RCAIDE
from RCAIDE.Framework.Core import  Units

# package imports 
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  compute_pump_performance
# ----------------------------------------------------------------------------------------------------------------------   
def compute_pump_performance(pump,state,fuel_line,bus):
    """Computes the size of the pump"""
     
    # compute delta P
    pressure_rise = pump.design_outlet_pressure - pump.design_inlet_pressure
    
    # mass flow 
    m_dot  = state.conditions.energy.fuel_lines[fuel_line.tag].fuel_mass_flow_rate
    
    # volumetric flow rate
    Q  = m_dot /pump.working_fluid.density
    
    # hydraulic power
    Hydraulic_Power  =  Q * pressure_rise
    
    # mass of pump 
    total_efficiency =  pump.pump_efficiency * pump.turbine_efficiency
    
    # shaft power 
    Shaft_Power = Hydraulic_Power / total_efficiency
     
    return  