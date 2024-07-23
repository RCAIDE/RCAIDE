# RCAIDE/Library/Components/Propulsors/Converters/Fan.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# 
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
## RCAIDE imports   
from RCAIDE.Framework.Core      import Data
from .                import Propulsor
 

# ---------------------------------------------------------------------------------------------------------------------- 
# Turbojet 
# ---------------------------------------------------------------------------------------------------------------------- 
class Turbojet(Propulsor):
    """This is a  turbojet propulsor

    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):
        # setting the default values
        self.tag                                      = 'Turbojet' 
        self.active_fuel_tanks                        = None
        self.nacelle                                  = None  
        self.ram                                      = None 
        self.inlet_nozzle                             = None 
        self.low_pressure_compressor                  = None 
        self.high_pressure_compressor                 = None 
        self.low_pressure_turbine                     = None 
        self.high_pressure_turbine                    = None 
        self.combustor                                = None 
        self.afterburner                              = None
        self.core_nozzle                              = None      
        
        self.engine_length                            = 0.0
        self.bypass_ratio                             = 0.0 
        self.design_isa_deviation                     = 0.0
        self.design_altitude                          = 0.0
        self.afterburner_active                       = False
        self.SFC_adjustment                           = 0.0  
        self.compressor_nondimensional_massflow       = 0.0
        self.reference_temperature                    = 288.15
        self.reference_pressure                       = 1.01325*10**5 
        self.design_thrust                            = 0.0
        self.mass_flow_rate_design                    = 0.0 
        self.OpenVSP_flow_through                     = False

