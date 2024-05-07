## @ingroup Analyses-Stability
# AVL.py
#
# Created:  Apr 2017, M. Clarke 
# Modified: Apr 2020, M. Clarke
#           Mar 2024, M. Clarke, M. Guidotti, D.J. Lee 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import RCAIDE
from RCAIDE.Framework.Core import Units, Data
from RCAIDE.Framework.Core import redirect

from RCAIDE.Library.Methods.Aerodynamics.AVL.write_geometry         import write_geometry
from RCAIDE.Library.Methods.Aerodynamics.AVL.write_mass_file        import write_mass_file
from RCAIDE.Library.Methods.Aerodynamics.AVL.write_run_cases        import write_run_cases
from RCAIDE.Library.Methods.Aerodynamics.AVL.write_input_deck       import write_input_deck
from RCAIDE.Library.Methods.Aerodynamics.AVL.run_analysis           import run_analysis
from RCAIDE.Library.Methods.Aerodynamics.AVL.translate_data         import translate_conditions_to_cases, translate_results_to_conditions 
from RCAIDE.Library.Methods.Aerodynamics.AVL.Data.Settings          import Settings 
from RCAIDE.Library.Methods.Stability.Dynamic_Stability             import compute_dynamic_flight_modes
from RCAIDE.Library.Components.Wings.Control_Surfaces               import Aileron , Elevator , Slat , Flap , Rudder 

# local imports 
from .Stability import Stability

# Package imports 
import os
import numpy as np
import sys  
from shutil import rmtree 
from scipy.interpolate   import RegularGridInterpolator

# ----------------------------------------------------------------------
#  Class
# ----------------------------------------------------------------------

## @ingroup Analyses-Stability
class AVL(Stability):
    """This builds a surrogate and computes moment using AVL.

    Assumptions:
    None

    Source:
    None
    """  

    def __defaults__(self):
        """This sets the default values and methods for the analysis.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        
        """
        self.tag                                    = 'avl' 
        
        self.current_status                         = Data()        
        self.current_status.batch_index             = 0
        self.current_status.batch_file              = None
        self.current_status.deck_file               = None
        self.current_status.cases                   = None      
        self.geometry                               = None   
                                                    
        self.settings                               = Settings()
        self.settings.use_surrogate                 = True 
        self.settings.filenames.log_filename        = sys.stdout
        self.settings.filenames.err_filename        = sys.stderr        
        self.settings.number_of_spanwise_vortices   = 20
        self.settings.number_of_chordwise_vortices  = 10
        self.settings.maximum_lift_coefficient      = np.inf
        self.settings.trim_aircraft                 = False 
        self.settings.print_output                  = False
                                                    
        # Regression Status      
        self.settings.keep_files                    = False
        self.settings.save_regression_results       = False          
        self.settings.regression_flag               = False 

        # Conditions table, used for surrogate model training
        self.training                               = Data()   
        
        # Standard subsonic/transonic aircarft
        self.training.angle_of_attack               = np.array([-2.,0., 2.,5., 7., 10.])*Units.degrees
        self.training.Mach                          = np.array([0.05,0.15,0.25, 0.45,0.65,0.85]) 
        self.settings.sideslip_angle                = 0.0
        self.settings.roll_rate_coefficient         = 0.0
        self.settings.pitch_rate_coefficient        = 0.0 
        self.settings.lift_coefficient              = None 
        self.training_file                          = None
                                                    
        # Surrogate model
        self.surrogates                             = Data()
        self.surrogates.moment_coefficient          = None
        self.surrogates.Cm_alpha_moment_coefficient = None
        self.surrogates.Cn_beta_moment_coefficient  = None      
        self.surrogates.neutral_point               = None
    
        # Initialize quantities
        self.configuration                          = Data()    
        self.geometry                               = Data()
                                                    
    def initialize(self):
        """Drives functions to get training samples and build a surrogate.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        self.tag = 'avl_analysis_of_{}'.format( )

        Properties Used:
        self.geometry.tag
        """          
        geometry                  = self.geometry 
        self.tag                  = 'avl_analysis_of_{}'.format(geometry.tag) 
        settings                  = self.settings  
        use_surrogate             = settings.use_surrogate   

        # If we are using the surrogate
        if use_surrogate == True: 
            # sample training data
            self.sample_training()
                        
            # build surrogate
            self.build_surrogate()        
            
            self.evaluate = self.evaluate_surrogate
               
        else:
            self.evaluate = self.evaluate_no_surrogate
            
    
        return

    def evaluate_surrogate(self,segment):
        """Evaluates moment coefficient, stability and body axis deriviatives and neutral point using available surrogates.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        state.conditions.
          mach_number      [-]
          angle_of_attack  [radians]

        Outputs:
        results
            results.static_stability
            results.stability.dynamic
        

        Properties Used:
        self.surrogates.
           pitch_moment_coefficient [-] CM
           cm_alpha                 [-] Cm_alpha
           cn_beta                  [-] Cn_beta
           neutral_point            [-] NP

        """          
        
        # Unpack
        surrogates          = self.surrogates
        conditions          = segment.conditions 
        Mach                = conditions.freestream.mach_number
        AoA                 = conditions.aerodynamics.angles.alpha 
        Beta                = conditions.aerodynamics.angles.beta
        cg                  = self.geometry.mass_properties.center_of_gravity[0]
        MAC                 = self.geometry.wings.main_wing.chords.mean_aerodynamic
        delta_e             = np.atleast_2d(conditions.control_surfaces.elevator.deflection) 
        delta_a             = np.atleast_2d(conditions.control_surfaces.aileron.deflection)   
        delta_r             = np.atleast_2d(conditions.control_surfaces.rudder.deflection)   
        delta_s             = np.atleast_2d(conditions.control_surfaces.slat.deflection)  
        delta_f             = np.atleast_2d(conditions.control_surfaces.flap.deflection)
        pitch_rate          = np.atleast_2d(conditions.static_stability.pitch_rate)   
        
        # Query surrogates  
        pts            = np.hstack((AoA,Mach))       
        neutral_point  = np.atleast_2d(surrogates.neutral_point(pts)).T 
        CM_0           = np.atleast_2d(surrogates.CM_0(pts)).T      
        CN_beta        = np.atleast_2d(surrogates.CN_beta(pts)).T  
        
        
        # Stability Results  
        #conditions.S_ref                                                  = # Need to Update 
        #conditions.c_ref                                                  = # Need to Update
        #conditions.b_ref                                                  = # Need to Update
        #conditions.X_ref                                                  = # Need to Update
        #conditions.Y_ref                                                  = # Need to Update
        #conditions.Z_ref                                                  = # Need to Update 
        #conditions.aerodynamics.oswald_efficiency                         = # Need to Update
        conditions.static_stability.coefficients.lift                     = 0
        conditions.static_stability.coefficients.drag                     =  0 
        conditions.static_stability.coefficients.X                        =  0 
        conditions.static_stability.coefficients.Y                        =  0 
        conditions.static_stability.coefficients.Z                        =  0 
        conditions.static_stability.coefficients.L                        =  0 
        conditions.static_stability.coefficients.M                        =  0 
        conditions.static_stability.coefficients.N                        =  0 
        #conditions.static_stability.derivatives.Clift_alpha               = # Need to Update 
        #conditions.static_stability.derivatives.CY_alpha                  = # Need to Update
        #conditions.static_stability.derivatives.CL_alpha                  = # Need to Update
        #conditions.static_stability.derivatives.CM_alpha                  = # Need to Update
        #conditions.static_stability.derivatives.CN_alpha                  = # Need to Update
        #conditions.static_stability.derivatives.Clift_beta                = # Need to Update
        #conditions.static_stability.derivatives.CY_beta                   = # Need to Update
        #conditions.static_stability.derivatives.CL_beta                   = # Need to Update
        #conditions.static_stability.derivatives.CM_beta                   = # Need to Update
        #conditions.static_stability.derivatives.CN_beta                   = # Need to Update
        #conditions.static_stability.derivatives.Clift_p                   = # Need to Update
        #conditions.static_stability.derivatives.Clift_q                   = # Need to Update
        #conditions.static_stability.derivatives.Clift_r                   = # Need to Update

        #conditions.static_stability.derivatives.CX_u                      = # Need to Update
        #conditions.static_stability.derivatives.CX_v                      = # Need to Update
        #conditions.static_stability.derivatives.CX_w                      = # Need to Update
        #conditions.static_stability.derivatives.CY_u                      = # Need to Update
        #conditions.static_stability.derivatives.CY_v                      = # Need to Update
        #conditions.static_stability.derivatives.CY_w                      = # Need to Update
        #conditions.static_stability.derivatives.CZ_u                      = # Need to Update
        #conditions.static_stability.derivatives.CZ_v                      = # Need to Update
        #conditions.static_stability.derivatives.CZ_w                      = # Need to Update
        #conditions.static_stability.derivatives.CL_u                      = # Need to Update
        #conditions.static_stability.derivatives.CL_v                      = # Need to Update
        #conditions.static_stability.derivatives.CL_w                      = # Need to Update
        #conditions.static_stability.derivatives.CM_u                      = # Need to Update
        #conditions.static_stability.derivatives.CM_v                      = # Need to Update
        #conditions.static_stability.derivatives.CM_w                      = # Need to Update
        #conditions.static_stability.derivatives.CN_u                      = # Need to Update
        #conditions.static_stability.derivatives.CN_v                      = # Need to Update
        #conditions.static_stability.derivatives.CN_w                      = # Need to Update
        
        #conditions.static_stability.derivatives.CX_p                      = # Need to Update
        #conditions.static_stability.derivatives.CX_q                      = # Need to Update
        #conditions.static_stability.derivatives.CX_r                      = # Need to Update
        #conditions.static_stability.derivatives.CY_p                      = # Need to Update
        #conditions.static_stability.derivatives.CY_q                      = # Need to Update
        #conditions.static_stability.derivatives.CY_r                      = # Need to Update
        #conditions.static_stability.derivatives.CZ_p                      = # Need to Update
        #conditions.static_stability.derivatives.CZ_q                      = # Need to Update
        #conditions.static_stability.derivatives.CZ_r                      = # Need to Update
        #conditions.static_stability.derivatives.CL_p                      = # Need to Update
        #conditions.static_stability.derivatives.CL_q                      = # Need to Update
        #conditions.static_stability.derivatives.CL_r                      = # Need to Update
        #conditions.static_stability.derivatives.CM_p                      = # Need to Update
        #conditions.static_stability.derivatives.CM_q                      = # Need to Update
        #conditions.static_stability.derivatives.CM_r                      = # Need to Update
        #conditions.static_stability.derivatives.CN_p                      = # Need to Update
        #conditions.static_stability.derivatives.CN_q                      = # Need to Update
        #conditions.static_stability.derivatives.CN_r                      = # Need to Update 
        #conditions.static_stability.neutral_point                         = # Need to Update
        #conditions.static_stability.spiral_criteria                       = # Need to Update 
        
        conditions.aerodynamics.coefficients.lift               = conditions.static_stability.coefficients.lift # overwrite lift in aerodynamic results 
        conditions.aerodynamics.lift_breakdown.total            = conditions.static_stability.coefficients.lift # overwrite lift in aerodynamic results 
        conditions.aerodynamics.drag_breakdown.induced.inviscid = conditions.static_stability.coefficients.drag 

        # -----------------------------------------------------------------------------------------------------------------------                     
        # Dynamic Stability & System Identification
        # -----------------------------------------------------------------------------------------------------------------------      
        # Dynamic Stability
        #if np.count_nonzero(geometry.mass_properties.moments_of_inertia.tensor) > 0:  
            #compute_dynamic_flight_modes(conditions,geometry) 

        return  


    def sample_training(self):
        """Call methods to run AVL for sample point evaluation.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        see properties used

        Outputs:
        self.training.
          coefficients     [-] CM, Cm_alpha, Cn_beta
          neutral point    [-] NP
          grid_points      [radians,-] angles of attack and Mach numbers 

        Properties Used:
        self.geometry.tag  <string>
        self.training.     
          angle_of_attack  [radians]
          Mach             [-]
        self.training_file (optional - file containing previous AVL data)
        """ 
        # Unpack
        run_folder             = os.path.abspath(self.settings.filenames.run_folder)
        geometry               = self.geometry
        training               = self.training 
        trim_aircraft          = self.settings.trim_aircraft  
        AoA                    = training.angle_of_attack
        Mach                   = training.Mach
        sideslip_angle         = self.settings.sideslip_angle
        roll_rate_coefficient  = self.settings.roll_rate_coefficient
        pitch_rate_coefficient = self.settings.pitch_rate_coefficient
        lift_coefficient       = self.settings.lift_coefficient
        atmosphere             = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
        atmo_data              = atmosphere.compute_values(altitude = 0.0)         
                               
        CM                     = np.zeros((len(AoA),len(Mach)))
        Cm_alpha               = np.zeros_like(CM)
        Cn_beta                = np.zeros_like(CM)
        NP                     = np.zeros_like(CM)
       
        # remove old files in run directory  
        if os.path.exists('avl_files'):
            if not self.settings.regression_flag:
                rmtree(run_folder)
                
        for i,_ in enumerate(Mach):
            # Set training conditions
            run_conditions = RCAIDE.Framework.Mission.Common.Results()
            run_conditions.freestream.density                   = atmo_data.density[0,0] 
            run_conditions.freestream.gravity                   = 9.81            
            run_conditions.freestream.speed_of_sound            = atmo_data.speed_of_sound[0,0]  
            run_conditions.freestream.velocity                  = Mach[i] * run_conditions.freestream.speed_of_sound
            run_conditions.freestream.mach_number               = Mach[i] 
            run_conditions.aerodynamics.angles.beta             = sideslip_angle
            run_conditions.aerodynamics.angles.alpha            = AoA 
            run_conditions.aerodynamics.coefficients.p          = roll_rate_coefficient
            run_conditions.aerodynamics.coefficients.lift       = lift_coefficient
            run_conditions.aerodynamics.coefficients.q          = pitch_rate_coefficient
            
            # Run Analysis  
            results =  self.evaluate_AVL(run_conditions, trim_aircraft)
            
            drag          = results.aerodynamics.drag_breakdown.induced.total         
            e             = results.aerodynamics.oswald_efficiency                       
            lift          = results.static_stability.coefficients.lift                 
            CX_0          = results.static_stability.coefficients.X                      
            CY_0          = results.static_stability.coefficients.Y                      
            CZ_0          = results.static_stability.coefficients.Z                      
            CL_0          = results.static_stability.coefficients.L                      
            CM_0          = results.static_stability.coefficients.M                      
            CN_0          = results.static_stability.coefficients.N     
            Clift_alpha   = results.static_stability.derivatives.Clift_alpha          
            CY_alpha      = results.static_stability.derivatives.CY_alpha             
            CL_alpha      = results.static_stability.derivatives.CL_alpha             
            CM_alpha      = results.static_stability.derivatives.CM_alpha              
            CN_alpha      = results.static_stability.derivatives.CN_alpha              
            Clift_beta    = results.static_stability.derivatives.Clift_beta            
            CY_beta       = results.static_stability.derivatives.CY_beta              
            CL_beta       = results.static_stability.derivatives.CL_beta              
            CM_beta       = results.static_stability.derivatives.CM_beta              
            CN_beta       = results.static_stability.derivatives.CN_beta                    
            Clift_p       = results.static_stability.derivatives.Clift_p              
            Clift_q       = results.static_stability.derivatives.Clift_q              
            Clift_r       = results.static_stability.derivatives.Clift_r                  
            CX_u          = results.static_stability.derivatives.CX_u                 
            CX_v          = results.static_stability.derivatives.CX_v                 
            CX_w          = results.static_stability.derivatives.CX_w                 
            CY_u          = results.static_stability.derivatives.CY_u                 
            CY_v          = results.static_stability.derivatives.CY_v                 
            CY_w          = results.static_stability.derivatives.CY_w                 
            CZ_u          = results.static_stability.derivatives.CZ_u                 
            CZ_v          = results.static_stability.derivatives.CZ_v                 
            CZ_w          = results.static_stability.derivatives.CZ_w                 
            CL_u          = results.static_stability.derivatives.CL_u                 
            CL_v          = results.static_stability.derivatives.CL_v                 
            CL_w          = results.static_stability.derivatives.CL_w                 
            CM_u          = results.static_stability.derivatives.CM_u                 
            CM_v          = results.static_stability.derivatives.CM_v                 
            CM_w          = results.static_stability.derivatives.CM_w                 
            CN_u          = results.static_stability.derivatives.CN_u                 
            CN_v          = results.static_stability.derivatives.CN_v                 
            CN_w          = results.static_stability.derivatives.CN_w                 
            CX_p          = results.static_stability.derivatives.CX_p                 
            CX_q          = results.static_stability.derivatives.CX_q                 
            CX_r          = results.static_stability.derivatives.CX_r                 
            CY_p          = results.static_stability.derivatives.CY_p                 
            CY_q          = results.static_stability.derivatives.CY_q                 
            CY_r          = results.static_stability.derivatives.CY_r                 
            CZ_p          = results.static_stability.derivatives.CZ_p                 
            CZ_q          = results.static_stability.derivatives.CZ_q                 
            CZ_r          = results.static_stability.derivatives.CZ_r                 
            CL_p          = results.static_stability.derivatives.CL_p                 
            CL_q          = results.static_stability.derivatives.CL_q                 
            CL_r          = results.static_stability.derivatives.CL_r                 
            CM_p          = results.static_stability.derivatives.CM_p                 
            CM_q          = results.static_stability.derivatives.CM_q                 
            CM_r          = results.static_stability.derivatives.CM_r                 
            CN_p          = results.static_stability.derivatives.CN_p                 
            CN_q          = results.static_stability.derivatives.CN_q                 
            CN_r          = results.static_stability.derivatives.CN_r                 
            NP            = results.static_stability.neutral_point            
            SC            = results.static_stability.spiral_criteria          
             
        
        if self.training_file:
            # load data 
            data_array   = np.loadtxt(self.training_file)  
            CM_1D        = np.atleast_2d(data_array[:,0]) 
            Cm_alpha_1D  = np.atleast_2d(data_array[:,1])            
            Cn_beta_1D   = np.atleast_2d(data_array[:,2])
            NP_1D        = np.atleast_2d(data_array[:,3])
            
            # convert from 1D to 2D
            CM_0      = np.reshape(CM_1D, (len(AoA),-1))
            CM_alpha  = np.reshape(Cm_alpha_1D, (len(AoA),-1))
            CN_beta   = np.reshape(Cn_beta_1D , (len(AoA),-1))
            NP        = np.reshape(NP_1D , (len(AoA),-1))
        
        # Save the data for regression 
        if self.settings.save_regression_results:
            # convert from 2D to 1D
            CM_1D       = CM.reshape([len(AoA)*len(Mach),1]) 
            Cm_alpha_1D = Cm_alpha.reshape([len(AoA)*len(Mach),1])  
            Cn_beta_1D  = Cn_beta.reshape([len(AoA)*len(Mach),1])         
            NP_1D       = Cn_beta.reshape([len(AoA)*len(Mach),1]) 
            np.savetxt(geometry.tag+'_stability_data.txt',np.hstack([CM_1D,Cm_alpha_1D, Cn_beta_1D,NP_1D ]),fmt='%10.8f',header='   CM       Cm_alpha       Cn_beta       NP ')
        
        # Store training data   
        training.CM_0          = CM_0    
        training.CM_alpha      = CM_alpha 
        training.CN_beta       = CN_beta
        training.neutral_point = NP
        
        return        

    def build_surrogate(self):
        """Builds a surrogate based on sample evalations using a Guassian process.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        self.training.
          coefficients     [-] CM, Cm_alpha, Cn_beta 
          neutral point    [meters] NP
          grid_points      [radians,-] angles of attack and Mach numbers 

        Outputs:
        self.surrogates.
          moment_coefficient           
          Cm_alpha_moment_coefficient  
          Cn_beta_moment_coefficient   
          neutral_point                      

        Properties Used:
        No others
        """  
        # Unpack data
        training       = self.training
        surrogates     = self.surrogates
        AoA_data       = training.angle_of_attack
        mach_data      = training.Mach
        
        # Pack the outputs
        surrogates.CM_0           = RegularGridInterpolator((AoA_data,mach_data),training.CM_0 ,method = 'linear',   bounds_error=False, fill_value=None)    
        surrogates.CM_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.CM_alpha ,method = 'linear',   bounds_error=False, fill_value=None)    
        surrogates.CN_beta        = RegularGridInterpolator((AoA_data,mach_data),training.CN_beta     ,method = 'linear',   bounds_error=False, fill_value=None)
        surrogates.neutral_point  = RegularGridInterpolator((AoA_data,mach_data),training.NP  ,method = 'linear',   bounds_error=False, fill_value=None)
 
        return

    
# ----------------------------------------------------------------------
#  Helper Functions
# ----------------------------------------------------------------------
        
    def evaluate_AVL(self,run_conditions, trim_aircraft ):
        """Process vehicle to setup geometry, condititon, and configuration.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        run_conditions <RCAIDE data type> aerodynamic conditions; until input
                method is finalized, will assume mass_properties are always as 
                defined in self.features

        Outputs:
        results        <SUAVE data type>

        Properties Used:
        self.settings.filenames.
          run_folder
          output_template
          batch_template
          deck_template
        self.current_status.
          batch_index
          batch_file
          deck_file
          cases
        """           
        
        # unpack
        run_folder                       = os.path.abspath(self.settings.filenames.run_folder)
        run_script_path                  = run_folder.rstrip('avl_files').rstrip('/')
        aero_results_template_1          = self.settings.filenames.aero_output_template_1       # 'stability_axis_derivatives_{}.dat' 
        aero_results_template_2          = self.settings.filenames.aero_output_template_2       # 'surface_forces_{}.dat'
        aero_results_template_3          = self.settings.filenames.aero_output_template_3       # 'strip_forces_{}.dat'   
        aero_results_template_4          = self.settings.filenames.aero_output_template_4       # 'body_axis_derivatives_{}.dat'     
        dynamic_results_template_1       = self.settings.filenames.dynamic_output_template_1    # 'eigen_mode_{}.dat'
        dynamic_results_template_2       = self.settings.filenames.dynamic_output_template_2    # 'system_matrix_{}.dat'
        batch_template                   = self.settings.filenames.batch_template
        deck_template                    = self.settings.filenames.deck_template 
        print_output                     = self.settings.print_output 
        
        # rename defaul avl aircraft tag
        self.tag                         = 'avl_analysis_of_{}'.format(self.geometry.tag) 
        self.settings.filenames.features = self.geometry._base.tag + '.avl'
        self.settings.filenames.mass_file= self.geometry._base.tag + '.mass'
        
        # update current status
        self.current_status.batch_index += 1
        batch_index                      = self.current_status.batch_index
        self.current_status.batch_file   = batch_template.format(batch_index)
        self.current_status.deck_file    = deck_template.format(batch_index)
               
        # control surfaces
        num_cs       = 0
        cs_names     = []
        cs_functions = []
        control_surfaces = False
        for wing in self.geometry.wings: # this parses through the wings to determine how many control surfaces does the vehicle have 
            if wing.control_surfaces:
                control_surfaces = True 
                #wing = populate_control_sections(wing)     
                num_cs_on_wing = len(wing.control_surfaces)
                num_cs +=  num_cs_on_wing
                for ctrl_surf in wing.control_surfaces:
                    cs_names.append(ctrl_surf.tag)  
                    if (type(ctrl_surf) ==  Slat):
                        ctrl_surf_function  = 'slat'
                    elif (type(ctrl_surf) ==  Flap):
                        ctrl_surf_function  = 'flap' 
                    elif (type(ctrl_surf) ==  Aileron):
                        ctrl_surf_function  = 'aileron'                          
                    elif (type(ctrl_surf) ==  Elevator):
                        ctrl_surf_function  = 'elevator' 
                    elif (type(ctrl_surf) ==  Rudder):
                        ctrl_surf_function = 'rudder'                      
                    cs_functions.append(ctrl_surf_function)   
        
        # translate conditions
        cases                            = translate_conditions_to_cases(self, run_conditions)    
        for case in cases:
            case.stability_and_control.number_control_surfaces = num_cs
            case.stability_and_control.control_surface_names   = cs_names
        self.current_status.cases        = cases  
        
       # write casefile names using the templates 
        for case in cases:  
            case.aero_result_filename_1     = aero_results_template_1.format(case.tag)      # 'stability_axis_derivatives_{}.dat'  
            case.aero_result_filename_2     = aero_results_template_2.format(case.tag)      # 'surface_forces_{}.dat'
            case.aero_result_filename_3     = aero_results_template_3.format(case.tag)      # 'strip_forces_{}.dat'  
            case.aero_result_filename_4     = aero_results_template_4.format(case.tag)      # 'body_axis_derivatives_{}.dat'
            case.eigen_result_filename_1    = dynamic_results_template_1.format(case.tag)   # 'eigen_mode_{}.dat'
            case.eigen_result_filename_2    = dynamic_results_template_2.format(case.tag)   # 'system_matrix_{}.dat'
        
        # write the input files
        with redirect.folder(run_folder,force=False):
            write_geometry(self,run_script_path)
            write_mass_file(self,run_conditions)
            write_run_cases(self,trim_aircraft)
            write_input_deck(self, trim_aircraft,control_surfaces)

            # RUN AVL!
            results_avl = run_analysis(self,print_output)
    
        # translate results
        results = translate_results_to_conditions(cases,results_avl)
        
        if not self.settings.keep_files:
            rmtree( run_folder )           
 
        return results
