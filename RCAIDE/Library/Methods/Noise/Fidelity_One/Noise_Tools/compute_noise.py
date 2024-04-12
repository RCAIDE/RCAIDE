## @ingroup Methods-Noise-Fidelity_One-Noise_Tools
# approach_noise.py
# 
# Created:  Oct 2020, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np  
from Legacy.trunk.S.Methods.Noise.Fidelity_One.Engine                         import noise_SAE  
from Legacy.trunk.S.Methods.Noise.Fidelity_One.Airframe.noise_airframe_Fink   import noise_airframe_Fink 
from Legacy.trunk.S.Methods.Noise.Fidelity_One.Noise_Tools                    import noise_geometric

# ----------------------------------------------------------------------        
#   NOISE CALCULATION
# ----------------------------------------------------------------------

## @ingroup Methods-Noise-Fidelity_One-Noise_Tools
def func_compute_noise(config,analyses,noise_segment,noise_settings):
    """This method computes the noise of a turbofan aircraft
            
    Assumptions:
        N/A

    Source:
        N/A 

    Inputs:
        config.
        networks.turbofan     - SUAVE turbofan data structure               [None]
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

    geometric         = noise_geometric(noise_segment,analyses,config)

    airframe_noise    = noise_airframe_Fink(noise_segment,analyses,config,noise_settings,print_output,outputfile)

    engine_noise      = noise_SAE(turbofan,noise_segment,analyses,config,noise_settings,print_output,outputfile_engine)

    noise_sum         = 10. * np.log10(10**(airframe_noise.EPNL_total/10)+ (engine_flag)*10**(engine_noise.EPNL_total/10))
    
    return noise_sum



def compute_noise(State, Settings, System):
	#TODO: config         = [Replace With State, Settings, or System Attribute]
	#TODO: analyses       = [Replace With State, Settings, or System Attribute]
	#TODO: noise_segment  = [Replace With State, Settings, or System Attribute]
	#TODO: noise_settings = [Replace With State, Settings, or System Attribute]

	results = func_compute_noise('config', 'analyses', 'noise_segment', 'noise_settings')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System