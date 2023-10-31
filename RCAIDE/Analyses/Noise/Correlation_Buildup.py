## @ingroup Analyses-Noise
# RCAIDE/Analyses/Noise/Correlation_Buildup.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
import RCAIDE  
from .Noise      import Noise  
from RCAIDE.Components.Component import Container 

# noise imports 
from RCAIDE.Methods.Noise.Correlation_Buildup.Airframe.airframe_noise                              import airframe_noise
from RCAIDE.Methods.Noise.Correlation_Buildup.Turbofan.turbofan_engine_noise                       import turbofan_engine_noise  
from RCAIDE.Methods.Noise.Certification.compute_certification_distance_and_emission_angles         import compute_certification_distance_and_emission_angles
from RCAIDE.Methods.Noise.Common.decibel_arithmetic                                                import SPL_arithmetic
from RCAIDE.Methods.Noise.Common.generate_microphone_locations                                     import generate_zero_elevation_microphone_locations, generate_noise_hemisphere_microphone_locations
from RCAIDE.Methods.Noise.Common.compute_relative_noise_evaluation_locations                       import compute_relative_noise_evaluation_locations  

# package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Correlation_Buildup
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Analyses-Noise
class Correlation_Buildup(Noise): 
    """  
    """
    
    def __defaults__(self):
        
        """ This sets the default values for the analysis.
        
            Assumptions:
            Ground microphone angles start in front of the aircraft (0 deg) and sweep in a lateral direction 
            to the starboard wing and around to the tail (180 deg)
            
            Source:
            N/A
            
            Inputs:
            None
            
            Output:
            None
            
            Properties Used:
            N/A
        """
        
        # Initialize quantities
        settings                                        = self.settings
        settings.harmonics                              = np.arange(1,30) 
        settings.flyover                                = False    
        settings.approach                               = False
        settings.sideline                               = False
        settings.sideline_x_position                    = 0 
        settings.print_noise_output                     = False  
        settings.mean_sea_level_altitude                = True 
        settings.aircraft_destination_location          = np.array([0,0,0])
        settings.aircraft_departure_location            = np.array([0,0,0])
        
        settings.topography_file                        = None
        settings.ground_microphone_locations            = None   
        settings.ground_microphone_coordinates          = None
        settings.ground_microphone_x_resolution         = 100
        settings.ground_microphone_y_resolution         = 100
        settings.ground_microphone_x_stencil            = 2
        settings.ground_microphone_y_stencil            = 2
        settings.ground_microphone_min_x                = 1E-6
        settings.ground_microphone_max_x                = 5000 
        settings.ground_microphone_min_y                = 1E-6
        settings.ground_microphone_max_y                = 450  
        
        settings.noise_hemisphere                       = False 
        settings.noise_hemisphere_radius                = 20 
        settings.noise_hemisphere_microphone_resolution = 20
        settings.noise_hemisphere_phi_angle_bounds      = np.array([0,np.pi])
        settings.noise_hemisphere_theta_angle_bounds    = np.array([0,2*np.pi])
         
                
        # settings for acoustic frequency resolution
        settings.center_frequencies                   = np.array([16,20,25,31.5,40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, \
                                                                  500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150,
                                                                  4000, 5000, 6300, 8000, 10000])        
        settings.lower_frequencies                    = np.array([14,18,22.4,28,35.5,45,56,71,90,112,140,180,224,280,355,450,560,710,\
                                                                  900,1120,1400,1800,2240,2800,3550,4500,5600,7100,9000 ])
        settings.upper_frequencies                    = np.array([18,22.4,28,35.5,45,56,71,90,112,140,180,224,280,355,450,560,710,900,1120,\
                                                                 1400,1800,2240,2800,3550,4500,5600,7100,9000,11200 ])
        
        return
            
    def evaluate_noise(self,segment):
        """ Process vehicle to setup geometry, condititon and configuration
    
        Assumptions:
        None
    
        Source:
        N/4
    
        Inputs:
        self.settings.
            center_frequencies  - 1/3 octave band frequencies   [unitless]
    
        Outputs:
        None
    
        Properties Used:
        self.geometry
        """         
    
        # unpack 
        config        = segment.analyses.noise.geometry
        analyses      = segment.analyses
        settings      = self.settings 
        print_flag    = settings.print_noise_output  
        conditions    = segment.state.conditions  
        dim_cf        = len(settings.center_frequencies ) 
        ctrl_pts      = int(segment.state.numerics.number_of_control_points) 
        
        # generate noise valuation points
        if settings.noise_hemisphere == True:
            generate_noise_hemisphere_microphone_locations(settings)     
            
        elif type(settings.ground_microphone_locations) is not np.ndarray: 
            generate_zero_elevation_microphone_locations(settings)     
        
        REGML,EGML,TGML,num_gm_mic,mic_stencil = compute_relative_noise_evaluation_locations(settings,segment)
          
        # append microphone locations to conditions  
        conditions.noise.ground_microphone_stencil_locations   = mic_stencil        
        conditions.noise.evaluated_ground_microphone_locations = EGML       
        conditions.noise.total_ground_microphone_locations     = TGML
        conditions.noise.number_of_ground_microphones          = num_gm_mic 
        conditions.noise.total_microphone_locations            = REGML 
        conditions.noise.total_number_of_microphones           = num_gm_mic 
        
        # create empty arrays for results      
        total_SPL_dBA          = np.ones((ctrl_pts,num_gm_mic))*1E-16 
        total_SPL_spectra      = np.ones((ctrl_pts,num_gm_mic,dim_cf))*1E-16  
         
        # iterate through sources 
        for source in conditions.noise.sources.keys():  
            for network in config.networks.keys(): 
                if source  == 'turbofan': 
                    
                    geometric = compute_certification_distance_and_emission_angles(segment,analyses,config)  
                     
                    # flap noise - only applicable for turbofan aircraft
                    if 'flap' in config.wings.main_wing.control_surfaces:   
                
                        source_SPLs_dBA    = np.zeros((ctrl_pts,1,num_gm_mic)) 
                        source_SPL_spectra = np.zeros((ctrl_pts,1,num_gm_mic,dim_cf))
                        
                        airframe_noise_res           = airframe_noise(segment,analyses,config,settings)  
                        source_SPLs_dBA[:,0,:]       = airframe_noise_res.SPL_dBA          
                        source_SPL_spectra[:,0,:,5:] = np.repeat(airframe_noise_res.SPL_spectrum[:,np.newaxis,:], num_gm_mic , axis =1)
                        
                        # add noise 
                        total_SPL_dBA     = SPL_arithmetic(np.concatenate((total_SPL_dBA[:,None,:],source_SPLs_dBA),axis =1),sum_axis=1)
                        total_SPL_spectra = SPL_arithmetic(np.concatenate((total_SPL_spectra[:,None,:,:],source_SPL_spectra),axis =1),sum_axis=1)
                    
                    
                    if bool(conditions.noise.sources[source].fan) and bool(conditions.noise.sources[source].core): 

                        source_SPLs_dBA    = np.zeros((ctrl_pts,1,num_gm_mic)) 
                        source_SPL_spectra = np.zeros((ctrl_pts,1,num_gm_mic,dim_cf ))
                                                
                                              
                        config.networks[source].fan.rotation             = 0 # FUTURE WORK: NEED TO UPDATE ENGINE MODEL WITH FAN SPEED in RPM
                        config.networks[source].fan_nozzle.noise_speed   = conditions.noise.sources.turbofan.fan.exit_velocity 
                        config.networks[source].core_nozzle.noise_speed  = conditions.noise.sources.turbofan.core.exit_velocity
                        engine_noise                                     = turbofan_engine_noise(config.networks[source],segment,analyses,config,settings,ioprint = print_flag)  
                        source_SPLs_dBA[:,0,:]                           = np.repeat(np.atleast_2d(engine_noise.SPL_dBA).T, num_gm_mic , axis =1)     # noise measures at one microphone location in segment
                        source_SPL_spectra[:,0,:,5:]                     = np.repeat(engine_noise.SPL_spectrum[:,np.newaxis,:], num_gm_mic , axis =1) # noise measures at one microphone location in segment
                   
                        # add noise 
                        total_SPL_dBA     = SPL_arithmetic(np.concatenate((total_SPL_dBA[:,None,:],source_SPLs_dBA),axis =1),sum_axis=1)
                        total_SPL_spectra = SPL_arithmetic(np.concatenate((total_SPL_spectra[:,None,:,:],source_SPL_spectra),axis =1),sum_axis=1) 
                            
             
        conditions.noise.total_SPL_dBA              = total_SPL_dBA
        conditions.noise.total_SPL_1_3_spectrum_dBA = total_SPL_spectra
        
        return   

