## @ingroup Methods-Energy-Propulsors-Turboshaft_Propulsor
# RCAIDE/Methods/Energy/Propulsors/Turboshaft_Propulsor/size_core.py
# 
# 
# Created:  Jul 2023, M. Clarke
# Modified: Jun 2024, M. Guidotti & D.J. Lee

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from RCAIDE.Library.Methods.Energy.Propulsors.Turboshaft_Propulsor import compute_power

# Python package imports
import numpy                                                       as np

# ----------------------------------------------------------------------------------------------------------------------
#  size_core
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Energy-Propulsors-Turboshaft_Propulsor 
def size_core(turboshaft,conditions):
    """Sizes the core flow for the design condition.

    Assumptions:
    Perfect gas
    Turboshaft engine with free power turbine

    Sources:
    [1] https://soaneemrana.org/onewebmedia/ELEMENTS%20OF%20GAS%20TURBINE%20PROPULTION2.pdf - Page 332 - 336
    [2] https://www.colorado.edu/faculty/kantha/sites/default/files/attached-files/70652-116619_-_luke_stuyvenberg_-_dec_17_2015_1258_pm_-_stuyvenberg_helicopterturboshafts.pdf

    Inputs:
    conditions.freestream.speed_of_sound [m/s] (conditions is also passed to turboshaft.compute(..))
    turboshaft.inputs.
      bypass_ratio                            [-]
      total_temperature_reference             [K]
      total_pressure_reference                [Pa]
      number_of_engines                       [-]

    Outputs:
    turboshaft.outputs.non_dimensional_power  [-]

    Properties Used:
    turboshaft.
      reference_temperature                   [K]
      reference_pressure                      [Pa]
      total_design                            [W] - Design power
    """             
    
    #unpack from turboshaft
    Tref                                           = turboshaft.reference_temperature
    Pref                                           = turboshaft.reference_pressure 
    total_temperature_reference                    = turboshaft.inputs.total_temperature_reference  
    total_pressure_reference                       = turboshaft.inputs.total_pressure_reference 

    #compute nondimensional power
    compute_power(turboshaft,conditions)

    #unpack results 
    Psp                                            = turboshaft.outputs.non_dimensional_power
    
    #compute dimensional mass flow rates
    mdot_core                                      = turboshaft.design_power/Psp
    mdhc                                           = mdot_core/ (np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref))

    #pack outputs
    turboshaft.mass_flow_rate_design               = mdot_core
    turboshaft.compressor_nondimensional_massflow  = mdhc

    return    
