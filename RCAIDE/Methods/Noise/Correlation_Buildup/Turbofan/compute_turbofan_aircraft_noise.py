## @ingroup Methods-Noise-Correlation_Buildup-Turbofan
# RCAIDE/Methods/Noise/Correlation_Buildup/Turbofan/compute_turbofan_aircraft_noise.py
# 
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE Imports 
from RCAIDE.Methods.Noise.Correlation_Buildup.Turbofan                                      import turbofan_engine_noise  
from RCAIDE.Methods.Noise.Correlation_Buildup.Airframe.airframe_noise                       import airframe_noise 
from RCAIDE.Methods.Noise.Certification.compute_certification_distance_and_emission_angles import compute_certification_distance_and_emission_angles

# Python package imports   
import numpy as np   

# ----------------------------------------------------------------------------------------------------------------------     
#  Compute Turbofan Noise 
# ----------------------------------------------------------------------------------------------------------------------    
## @ingroup Methods-Noise-Correlation_Buildup-Turbofan
def compute_turbofan_aircraft_noise(config,analyses,noise_segment,noise_settings):
    """This method computes the noise of a turbofan aircraft
            
    Assumptions:
        N/A

    Source:
        N/A 

    Inputs:
        config.
        networks.turbofan     - RCAIDE turbofan data structure               [None]
        output_file           - flag to write noise outout to file          [Boolean]
        output_file_engine    - flag to write engine outout to file         [Boolean]
        print_output          - flag to print outout to file                [Boolean]
        engine_flag           - flag to include engine in noise calculation [Boolean]
        
    Outputs: 
        noise_sum                                                           [dB]

    Properties Used:
        N/A 
        
    """  
 
    turbofan          = config.networks['turbofan'] 
    outputfile        = config.output_file
    outputfile_engine = config.output_file_engine
    print_output      = config.print_output
    engine_flag       = config.engine_flag   

    geometric         = compute_certification_distance_and_emission_angles(noise_segment,analyses,config)

    airframe_noise    = airframe_noise(noise_segment,analyses,config,noise_settings,print_output,outputfile)

    engine_noise      = turbofan_engine_noise(turbofan,noise_segment,analyses,config,noise_settings,print_output,outputfile_engine)

    noise_sum         = 10. * np.log10(10**(airframe_noise.EPNL_total/10)+ (engine_flag)*10**(engine_noise.EPNL_total/10))
    
    return noise_sum
