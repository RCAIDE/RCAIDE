## @ingroup Analyses-Emissions
# RCAIDE/Framework/Analyses/Emissions/Emission_Index_Correlation_Method.py
# 
# 
# Created:  Jul 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import  RCAIDE
from RCAIDE.Framework.Core import Data ,  Units  
 
# package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Correlation_Buildup
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Analyses-Noise  
def emissions_index_correlation_method(self,segment):
    """  
    """    
    # unpack
    state           = segment.state
    vehicle         =  state.analyses.emissions.vehicle
    I               = state.numerics.time.integrate
    
    NOx_total = 0 * ones_row(1) 
    CO2_total = 0 * ones_row(1) 
    SO2_total = 0 * ones_row(1) 
    H2O_total = 0 * ones_row(1) 

    for network in vehicle.networks:
        for fuel_line in  network.fuel_lines:
            for propulsor in  propulsor:
                if (type(propulsor) ==  RCAIDE.Library.Components.Propulsors.Turbofan) or \
                    type(propulsor) ==  RCAIDE.Library.Components.Propulsors.Turboshaft or \
                    type(propulsor) ==  RCAIDE.Library.Components.Propulsors.Turbojet:    
        
                    combustor_results =  state.conditions[fuel_line.tag][propulsor.combustor.tag]  
                    p3              = combustor_results.inputs.stagnation_pressure/Units.psi
                    T3              = combustor_results.inputs.stagnation_temperature/Units.degR 
                    T4              = combustor_results.outputs.stagnation_temperature/Units.degR
                    mdot   =
                    
    
                    EI_NOx = .004194*T4*((p3/439.)**.37)*np.exp((T3-1471.)/345.)
                    EI_CO2 = self.emission_indices.CO2
                    EI_H2O = self.emission_indices.H2O
                    EI_SO2 = self.emission_indices.SO2
                    
                    #correlation in g Nox/kg fuel; convert to kg Nox/kg
                    NOx = NOx * (Units.g/Units.kg) 
                    
                    # Integrate them over the entire segment
                    NOx_total += np.dot(I,mdot*EI_NOx)
                    CO2_total += np.dot(I,mdot*EI_CO2)
                    SO2_total += np.dot(I,mdot*EI_SO2)
                    H2O_total += np.dot(I,mdot*EI_H2O) 
                

    emissions           = Data()
    emissions.total     = Data()
    emissions.index     = Data()
    emissions.total.NOx = NOx_total
    emissions.total.CO2 = CO2_total
    emissions.total.H2O = H2O_total
    emissions.total.SO2 = SO2_total 
    emissions.index.NOx = EI_NOx
    emissions.index.CO2 = EI_CO2
    emissions.index.H2O = EI_H2O
    emissions.index.SO2 = EI_SO2
    
    segment.conditions.emissions =  emissions
    return   

