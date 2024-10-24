# RCAIDE/Library/Components/Propulsors/Converters/Fan.py
# (c) Copyright 2023 Aerospace Research Community LLC
#  
# Created: Mar 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports  
from RCAIDE.Framework.Core      import Data, Container
from .                          import Propulsor
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Fan Component
# ---------------------------------------------------------------------------------------------------------------------- 
class Turbofan(Propulsor):
    """This is a turbofan propulsor.
    
    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):    
        # setting the default values
        self.tag                                      = 'Turbofan'  
        self.nacelle                                  = Container()
        self.fan                                      = Container()
        self.ram                                      = None 
        self.inlet_nozzle                             = None 
        self.low_pressure_compressor                  = None 
        self.high_pressure_compressor                 = None 
        self.low_pressure_turbine                     = None 
        self.high_pressure_turbine                    = None 
        self.combustor                                = None 
        self.core_nozzle                              = None 
        self.fan_nozzle                               = None  
        self.active_fuel_tanks                        = None         
        self.engine_length                            = 0.0
        self.engine_height                            = 0.5     # Engine centerline heigh above the ground plane
        self.exa                                      = 1       # distance from fan face to fan exit/ fan diameter)
        self.plug_diameter                            = 0.1     # dimater of the engine plug
        self.geometry_xe                              = 1.      # Geometry information for the installation effects function
        self.geometry_ye                              = 1.      # Geometry information for the installation effects function
        self.geometry_Ce                              = 2.      # Geometry information for the installation effects function
        self.bypass_ratio                             = 0.0 
        self.design_isa_deviation                     = 0.0
        self.design_altitude                          = 0.0
        self.SFC_adjustment                           = 0.0 # Less than 1 is a reduction
        self.compressor_nondimensional_massflow       = 0.0
        self.reference_temperature                    = 288.15
        self.reference_pressure                       = 1.01325*10**5 
        self.design_thrust                            = 0.0
        self.mass_flow_rate_design                    = 0.0
        self.OpenVSP_flow_through                     = False 