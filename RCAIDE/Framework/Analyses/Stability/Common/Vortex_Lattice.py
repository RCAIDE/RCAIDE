## @ingroup Analyses-Stability
# RCAIDE/Framework/Analyses/Stability/Common/Vortex_Lattice.py
# 
# 
# Created:  Apr 2024, M. Clarke
# Updated:  Mat 2024, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core                                       import Data, Units  
from RCAIDE.Library.Methods.Aerodynamics.Vortex_Lattice_Method   import VLM  
from RCAIDE.Framework.Analyses.Stability                         import Stability
from RCAIDE.Library.Methods.Stability.Dynamic_Stability          import compute_dynamic_flight_modes

# package imports
import numpy                                                     as np 
from scipy.interpolate                                           import RegularGridInterpolator
from scipy import interpolate

# ----------------------------------------------------------------------------------------------------------------------
#  Vortex_Lattice
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Analyses-Stability
class Vortex_Lattice(Stability):
    """This builds a surrogate and computes forces and moments using a basic vortex lattice for stability analyses. 
    """ 

    def __defaults__(self):
        """This sets the default values and methods for the analysis.
         
        Assumptions:
            None
            
        Source:
            None
    
        Args:
            None
            
        Returns: 
            None 
        """  
        self.tag                                      = 'Vortex_Lattice' 
        self.geometry                                 = Data()
        self.settings                                 = Data()
        self.settings.number_of_spanwise_vortices     = 25
        self.settings.number_of_chordwise_vortices    = 5
        self.settings.wing_spanwise_vortices          = None
        self.settings.wing_chordwise_vortices         = None
        self.settings.fuselage_spanwise_vortices      = None
        self.settings.fuselage_chordwise_vortices     = None 
        
        self.settings.spanwise_cosine_spacing         = True
        self.settings.vortex_distribution             = Data()   
        self.settings.model_fuselage                  = False            # It's better to model the fuselage
        self.settings.model_nacelle                   = False
        self.settings.leading_edge_suction_multiplier = 1.0
        self.settings.propeller_wake_model            = False
        self.settings.discretize_control_surfaces     = True 
        self.settings.use_VORLAX_matrix_calculation   = False
        self.settings.floating_point_precision        = np.float32
        self.settings.use_surrogate                   = True

        # conditions table, used for surrogate model training
        self.training                                 = Data()
        self.training.Mach                            = np.array([0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5])        
        #self.training.angle_of_attack                 = np.array([-10, -7.5, -5, -2.5, 0, 2.5, 5, 7.5, 10]) * Units.deg
        self.training.angle_of_attack                 = np.array([0, 5]) * Units.deg         
        self.training.sideslip_angle                  = np.array([0, 5]) * Units.deg
        self.training.aileron_deflection              = np.array([0, 1]) * Units.deg 
        self.training.elevator_deflection             = np.array([0, 1]) * Units.deg    
        self.training.rudder_deflection               = np.array([0, 1]) * Units.deg  
        self.training.flap_deflection                 = np.array([-5, 0])* Units.deg      
        #self.training.slat_deflection                 = np.array([0, 1]) * Units.deg       
        self.training.u                               = np.array([0, 1]) * Units.meters / Units.sec
        self.training.v                               = np.array([0, 1]) * Units.meters / Units.sec
        self.training.w                               = np.array([0, 1]) * Units.meters / Units.sec  
        self.training.pitch_rate                      = np.array([0, 0.01])  * Units.rad / Units.sec
        self.training.roll_rate                       = np.array([0, 0.3])  * Units.rad / Units.sec
        self.training.yaw_rate                        = np.array([0, 0.01])  * Units.rad / Units.sec        
        
        # surrogoate models
        self.surrogates                               = Data()   
        self.surrogates.Clift                         = None    
        self.surrogates.Cdrag                         = None 
        self.surrogates.CX                            = None 
        self.surrogates.CY                            = None 
        self.surrogates.CZ                            = None   
        self.surrogates.CL                            = None 
        self.surrogates.CM                            = None   
        self.surrogates.CN                            = None
        self.surrogates.static_margin                 = None
        
        self.surrogates.Clift_alpha                   = None    
        self.surrogates.Clift_beta                    = None    
        self.surrogates.Clift_delta_a                 = None    
        self.surrogates.Clift_delta_e                 = None    
        self.surrogates.Clift_delta_r                 = None    
        self.surrogates.Clift_delta_f                 = None    
        #self.surrogates.Clift_delta_s                 = None    
        self.surrogates.Clift_u                       = None    
        self.surrogates.Clift_v                       = None    
        self.surrogates.Clift_w                       = None    
        self.surrogates.Clift_p                       = None    
        self.surrogates.Clift_q                       = None    
        self.surrogates.Clift_r                       = None    
        self.surrogates.Cdrag_alpha                   = None    
        self.surrogates.Cdrag_beta                    = None    
        self.surrogates.Cdrag_delta_a                 = None    
        self.surrogates.Cdrag_delta_e                 = None    
        self.surrogates.Cdrag_delta_r                 = None    
        self.surrogates.Cdrag_delta_f                 = None    
        #self.surrogates.Cdrag_delta_s                 = None    
        self.surrogates.Cdrag_u                       = None    
        self.surrogates.Cdrag_v                       = None    
        self.surrogates.Cdrag_w                       = None    
        self.surrogates.Cdrag_p                       = None    
        self.surrogates.Cdrag_q                       = None    
        self.surrogates.Cdrag_r                       = None    
        self.surrogates.CX_alpha                      = None    
        self.surrogates.CX_beta                       = None    
        self.surrogates.CX_delta_a                    = None    
        self.surrogates.CX_delta_e                    = None    
        self.surrogates.CX_delta_r                    = None    
        self.surrogates.CX_delta_f                    = None    
        #self.surrogates.CX_delta_s                    = None    
        self.surrogates.CX_u                          = None    
        self.surrogates.CX_v                          = None    
        self.surrogates.CX_w                          = None    
        self.surrogates.CX_p                          = None    
        self.surrogates.CX_q                          = None    
        self.surrogates.CX_r                          = None    
        self.surrogates.CY_alpha                      = None    
        self.surrogates.CY_beta                       = None    
        self.surrogates.CY_delta_a                    = None    
        self.surrogates.CY_delta_e                    = None    
        self.surrogates.CY_delta_r                    = None    
        self.surrogates.CY_delta_f                    = None    
        #self.surrogates.CY_delta_s                    = None    
        self.surrogates.CY_u                          = None    
        self.surrogates.CY_v                          = None    
        self.surrogates.CY_w                          = None    
        self.surrogates.CY_p                          = None    
        self.surrogates.CY_q                          = None    
        self.surrogates.CY_r                          = None    
        self.surrogates.CZ_alpha                      = None    
        self.surrogates.CZ_beta                       = None    
        self.surrogates.CZ_delta_a                    = None    
        self.surrogates.CZ_delta_e                    = None    
        self.surrogates.CZ_delta_r                    = None    
        self.surrogates.CZ_delta_f                    = None    
        #self.surrogates.CZ_delta_s                    = None    
        self.surrogates.CZ_u                          = None    
        self.surrogates.CZ_v                          = None    
        self.surrogates.CZ_w                          = None    
        self.surrogates.CZ_p                          = None    
        self.surrogates.CZ_q                          = None    
        self.surrogates.CZ_r                          = None
        self.surrogates.CL_alpha                      = None     
        self.surrogates.CL_beta                       = None     
        self.surrogates.CL_delta_a                    = None     
        self.surrogates.CL_delta_e                    = None     
        self.surrogates.CL_delta_r                    = None     
        self.surrogates.CL_delta_f                    = None     
        #self.surrogates.CL_delta_s                    = None     
        self.surrogates.CL_u                          = None     
        self.surrogates.CL_v                          = None     
        self.surrogates.CL_w                          = None     
        self.surrogates.CL_p                          = None     
        self.surrogates.CL_q                          = None     
        self.surrogates.CL_r                          = None     
        self.surrogates.CM_alpha                      = None     
        self.surrogates.CM_beta                       = None     
        self.surrogates.CM_delta_a                    = None     
        self.surrogates.CM_delta_e                    = None     
        self.surrogates.CM_delta_r                    = None     
        self.surrogates.CM_delta_f                    = None     
        #self.surrogates.CM_delta_s                    = None     
        self.surrogates.CM_u                          = None     
        self.surrogates.CM_v                          = None     
        self.surrogates.CM_w                          = None     
        self.surrogates.CM_p                          = None     
        self.surrogates.CM_q                          = None     
        self.surrogates.CM_r                          = None     
        self.surrogates.CN_alpha                      = None     
        self.surrogates.CN_beta                       = None     
        self.surrogates.CN_delta_a                    = None     
        self.surrogates.CN_delta_e                    = None     
        self.surrogates.CN_delta_r                    = None     
        self.surrogates.CN_delta_f                    = None     
        #self.surrogates.CN_delta_s                    = None     
        self.surrogates.CN_u                          = None     
        self.surrogates.CN_v                          = None     
        self.surrogates.CN_w                          = None     
        self.surrogates.CN_p                          = None     
        self.surrogates.CN_q                          = None     
        self.surrogates.CN_r                          = None        
        
        self.surrogates.dClift_dalpha                   = None    
        self.surrogates.dClift_dbeta                    = None    
        self.surrogates.dClift_ddelta_a                 = None    
        self.surrogates.dClift_ddelta_e                 = None    
        self.surrogates.dClift_ddelta_r                 = None    
        self.surrogates.dClift_ddelta_f                 = None    
        #self.surrogates.dClift_ddelta_s                 = None    
        self.surrogates.dClift_du                       = None    
        self.surrogates.dClift_dv                       = None    
        self.surrogates.dClift_dw                       = None    
        self.surrogates.dClift_dp                       = None    
        self.surrogates.dClift_dq                       = None    
        self.surrogates.dClift_dr                       = None    
        self.surrogates.dCdrag_dalpha                   = None    
        self.surrogates.dCdrag_dbeta                    = None    
        self.surrogates.dCdrag_ddelta_a                 = None    
        self.surrogates.dCdrag_ddelta_e                 = None    
        self.surrogates.dCdrag_ddelta_r                 = None    
        self.surrogates.dCdrag_ddelta_f                 = None    
        #self.surrogates.dCdrag_ddelta_s                 = None    
        self.surrogates.dCdrag_du                       = None    
        self.surrogates.dCdrag_dv                       = None    
        self.surrogates.dCdrag_dw                       = None    
        self.surrogates.dCdrag_dp                       = None    
        self.surrogates.dCdrag_dq                       = None    
        self.surrogates.dCdrag_dr                       = None    
        self.surrogates.dCX_dalpha                      = None    
        self.surrogates.dCX_dbeta                       = None    
        self.surrogates.dCX_ddelta_a                    = None    
        self.surrogates.dCX_ddelta_e                    = None    
        self.surrogates.dCX_ddelta_r                    = None    
        self.surrogates.dCX_ddelta_f                    = None    
        #self.surrogates.dCX_ddelta_s                    = None    
        self.surrogates.dCX_du                          = None    
        self.surrogates.dCX_dv                          = None    
        self.surrogates.dCX_dw                          = None    
        self.surrogates.dCX_dp                          = None    
        self.surrogates.dCX_dq                          = None    
        self.surrogates.dCX_dr                          = None    
        self.surrogates.dCY_dalpha                      = None    
        self.surrogates.dCY_dbeta                       = None    
        self.surrogates.dCY_ddelta_a                    = None    
        self.surrogates.dCY_ddelta_e                    = None    
        self.surrogates.dCY_ddelta_r                    = None    
        self.surrogates.dCY_ddelta_f                    = None    
        #self.surrogates.dCY_ddelta_s                    = None    
        self.surrogates.dCY_du                          = None    
        self.surrogates.dCY_dv                          = None    
        self.surrogates.dCY_dw                          = None    
        self.surrogates.dCY_dp                          = None    
        self.surrogates.dCY_dq                          = None    
        self.surrogates.dCY_dr                          = None    
        self.surrogates.dCZ_dalpha                      = None    
        self.surrogates.dCZ_dbeta                       = None    
        self.surrogates.dCZ_ddelta_a                    = None    
        self.surrogates.dCZ_ddelta_e                    = None    
        self.surrogates.dCZ_ddelta_r                    = None    
        self.surrogates.dCZ_ddelta_f                    = None    
        #self.surrogates.dCZ_ddelta_s                    = None    
        self.surrogates.dCZ_du                          = None    
        self.surrogates.dCZ_dv                          = None    
        self.surrogates.dCZ_dw                          = None    
        self.surrogates.dCZ_dp                          = None    
        self.surrogates.dCZ_dq                          = None    
        self.surrogates.dCZ_dr                          = None
        self.surrogates.dCL_dalpha                      = None     
        self.surrogates.dCL_dbeta                       = None     
        self.surrogates.dCL_ddelta_a                    = None     
        self.surrogates.dCL_ddelta_e                    = None     
        self.surrogates.dCL_ddelta_r                    = None     
        self.surrogates.dCL_ddelta_f                    = None     
        #self.surrogates.dCL_ddelta_s                    = None     
        self.surrogates.dCL_du                          = None     
        self.surrogates.dCL_dv                          = None     
        self.surrogates.dCL_dw                          = None     
        self.surrogates.dCL_dp                          = None     
        self.surrogates.dCL_dq                          = None     
        self.surrogates.dCL_dr                          = None     
        self.surrogates.dCM_dalpha                      = None     
        self.surrogates.dCM_dbeta                       = None     
        self.surrogates.dCM_ddelta_a                    = None     
        self.surrogates.dCM_ddelta_e                    = None     
        self.surrogates.dCM_ddelta_r                    = None     
        self.surrogates.dCM_ddelta_f                    = None     
        #self.surrogates.dCM_ddelta_s                    = None     
        self.surrogates.dCM_du                          = None     
        self.surrogates.dCM_dv                          = None     
        self.surrogates.dCM_dw                          = None     
        self.surrogates.dCM_dp                          = None     
        self.surrogates.dCM_dq                          = None     
        self.surrogates.dCM_dr                          = None     
        self.surrogates.dCN_dalpha                      = None     
        self.surrogates.dCN_dbeta                       = None     
        self.surrogates.dCN_ddelta_a                    = None     
        self.surrogates.dCN_ddelta_e                    = None     
        self.surrogates.dCN_ddelta_r                    = None     
        self.surrogates.dCN_ddelta_f                    = None     
        #self.surrogates.dCN_ddelta_s                    = None     
        self.surrogates.dCN_du                          = None     
        self.surrogates.dCN_dv                          = None     
        self.surrogates.dCN_dw                          = None     
        self.surrogates.dCN_dp                          = None     
        self.surrogates.dCN_dq                          = None     
        self.surrogates.dCN_dr                          = None
        
        self.evaluate                                = None  
            
    def initialize(self): 
        settings                                      = self.settings  
        use_surrogate                                 = settings.use_surrogate 
        
        # If we are using the surrogate
        if use_surrogate == True: 
            # sample training data
            self.sample_training()
                        
            # build surrogate
            self.build_surrogate()        
            
            self.evaluate                             = self.evaluate_surrogate
                                                      
        else:                                         
            self.evaluate                             = self.evaluate_no_surrogate


    def evaluate_surrogate(self,state,settings,geometry):
        """Evaluates surrogates forces and moments using built surrogates 
        
        Assumptions:
            None
            
        Source:
            None
    
        Args:
            self       : VLM analysis          [unitless]
            state      : flight conditions     [unitless]
            settings   : VLM analysis settings [unitless]
            geometry   : vehicle configuration [unitless] 
            
        Returns: 
            None  
        """          
        
        # unpack        
        conditions  = state.conditions
        settings    = self.settings
        geometry    = self.geometry
        surrogates  = self.surrogates 

        AoA         = np.atleast_2d(conditions.aerodynamics.angles.alpha)  
        Beta        = np.atleast_2d(conditions.aerodynamics.angles.beta)    
        Mach        = np.atleast_2d(conditions.freestream.mach_number)   
        delta_a     = np.atleast_2d(conditions.control_surfaces.aileron.deflection)
        delta_e     = np.atleast_2d(conditions.control_surfaces.elevator.deflection)   
        delta_r     = np.atleast_2d(conditions.control_surfaces.rudder.deflection)  
        delta_f     = np.atleast_2d(conditions.control_surfaces.flap.deflection)   
        #delta_s     = np.atleast_2d(conditions.control_surfaces.slat.deflection)
        u           = np.atleast_2d(conditions.freestream.u)
        v           = np.atleast_2d(conditions.freestream.v)
        w           = np.atleast_2d(conditions.freestream.w)
        p           = np.atleast_2d(conditions.static_stability.roll_rate)        
        q           = np.atleast_2d(conditions.static_stability.pitch_rate)
        r           = np.atleast_2d(conditions.static_stability.yaw_rate)  
  
        # Query surrogates 
        
        pts_alpha            = np.hstack((AoA,Mach))
        pts_beta             = np.hstack((Beta,Mach))
        pts_delta_a          = np.hstack((delta_a,Mach))
        pts_delta_e          = np.hstack((delta_e,Mach))
        pts_delta_r          = np.hstack((delta_r,Mach))
        pts_delta_f          = np.hstack((delta_f,Mach))
        #pts_delta_s          = np.hstack((delta_s,Mach))
        pts_u                = np.hstack((u,Mach))
        pts_v                = np.hstack((v,Mach))
        pts_w                = np.hstack((w,Mach))
        pts_p                = np.hstack((p,Mach))
        pts_q                = np.hstack((q,Mach))
        pts_r                = np.hstack((r,Mach))
        
        Clift_alpha    = np.atleast_2d(surrogates.Clift_alpha(pts_alpha)).T
        Clift_beta     = np.atleast_2d(surrogates.Clift_beta(pts_beta)).T
        Clift_delta_a  = np.atleast_2d(surrogates.Clift_delta_a(pts_delta_a)).T
        Clift_delta_e  = np.atleast_2d(surrogates.Clift_delta_e(pts_delta_e)).T
        Clift_delta_r  = np.atleast_2d(surrogates.Clift_delta_r(pts_delta_r)).T
        Clift_delta_f  = np.atleast_2d(surrogates.Clift_delta_f(pts_delta_f)).T
        #Clift_delta_s  = np.atleast_2d(surrogates.Clift_delta_s(pts_delta_s)).T
        Clift_u        = np.atleast_2d(surrogates.Clift_u(pts_u)).T
        Clift_v        = np.atleast_2d(surrogates.Clift_v(pts_v)).T
        Clift_w        = np.atleast_2d(surrogates.Clift_w(pts_w)).T
        Clift_p        = np.atleast_2d(surrogates.Clift_p(pts_p)).T
        Clift_q        = np.atleast_2d(surrogates.Clift_q(pts_q)).T
        Clift_r        = np.atleast_2d(surrogates.Clift_r(pts_r)).T
        Cdrag_alpha    = np.atleast_2d(surrogates.Cdrag_alpha(pts_alpha)).T
        Cdrag_beta     = np.atleast_2d(surrogates.Cdrag_beta(pts_beta)).T
        Cdrag_delta_a  = np.atleast_2d(surrogates.Cdrag_delta_a(pts_delta_a)).T
        Cdrag_delta_e  = np.atleast_2d(surrogates.Cdrag_delta_e(pts_delta_e)).T
        Cdrag_delta_r  = np.atleast_2d(surrogates.Cdrag_delta_r(pts_delta_r)).T
        Cdrag_delta_f  = np.atleast_2d(surrogates.Cdrag_delta_f(pts_delta_f)).T
        #Cdrag_delta_s  = np.atleast_2d(surrogates.Cdrag_delta_s(pts_delta_s)).T
        Cdrag_u        = np.atleast_2d(surrogates.Cdrag_u(pts_u)).T
        Cdrag_v        = np.atleast_2d(surrogates.Cdrag_v(pts_v)).T
        Cdrag_w        = np.atleast_2d(surrogates.Cdrag_w(pts_w)).T
        Cdrag_p        = np.atleast_2d(surrogates.Cdrag_p(pts_p)).T
        Cdrag_q        = np.atleast_2d(surrogates.Cdrag_q(pts_q)).T
        Cdrag_r        = np.atleast_2d(surrogates.Cdrag_r(pts_r)).T
        CX_alpha       = np.atleast_2d(surrogates.CX_alpha(pts_alpha)).T
        CX_beta        = np.atleast_2d(surrogates.CX_beta(pts_beta)).T
        CX_delta_a     = np.atleast_2d(surrogates.CX_delta_a(pts_delta_a)).T
        CX_delta_e     = np.atleast_2d(surrogates.CX_delta_e(pts_delta_e)).T
        CX_delta_r     = np.atleast_2d(surrogates.CX_delta_r(pts_delta_r)).T
        CX_delta_f     = np.atleast_2d(surrogates.CX_delta_f(pts_delta_f)).T
        #CX_delta_s     = np.atleast_2d(surrogates.CX_delta_s(pts_delta_s)).T
        CX_u           = np.atleast_2d(surrogates.CX_u(pts_u)).T
        CX_v           = np.atleast_2d(surrogates.CX_v(pts_v)).T
        CX_w           = np.atleast_2d(surrogates.CX_w(pts_w)).T
        CX_p           = np.atleast_2d(surrogates.CX_p(pts_p)).T
        CX_q           = np.atleast_2d(surrogates.CX_q(pts_q)).T
        CX_r           = np.atleast_2d(surrogates.CX_r(pts_r)).T
        CY_alpha       = np.atleast_2d(surrogates.CY_alpha(pts_alpha)).T
        CY_beta        = np.atleast_2d(surrogates.CY_beta(pts_beta)).T
        CY_delta_a     = np.atleast_2d(surrogates.CY_delta_a(pts_delta_a)).T
        CY_delta_e     = np.atleast_2d(surrogates.CY_delta_e(pts_delta_e)).T
        CY_delta_r     = np.atleast_2d(surrogates.CY_delta_r(pts_delta_r)).T
        CY_delta_f     = np.atleast_2d(surrogates.CY_delta_f(pts_delta_f)).T
        #CY_delta_s     = np.atleast_2d(surrogates.CY_delta_s(pts_delta_s)).T
        CY_u           = np.atleast_2d(surrogates.CY_u(pts_u)).T
        CY_v           = np.atleast_2d(surrogates.CY_v(pts_v)).T
        CY_w           = np.atleast_2d(surrogates.CY_w(pts_w)).T
        CY_p           = np.atleast_2d(surrogates.CY_p(pts_p)).T
        CY_q           = np.atleast_2d(surrogates.CY_q(pts_q)).T
        CY_r           = np.atleast_2d(surrogates.CY_r(pts_r)).T
        CZ_alpha       = np.atleast_2d(surrogates.CZ_alpha(pts_alpha)).T
        CZ_beta        = np.atleast_2d(surrogates.CZ_beta(pts_beta)).T
        CZ_delta_a     = np.atleast_2d(surrogates.CZ_delta_a(pts_delta_a)).T
        CZ_delta_e     = np.atleast_2d(surrogates.CZ_delta_e(pts_delta_e)).T
        CZ_delta_r     = np.atleast_2d(surrogates.CZ_delta_r(pts_delta_r)).T
        CZ_delta_f     = np.atleast_2d(surrogates.CZ_delta_f(pts_delta_f)).T
        #CZ_delta_s     = np.atleast_2d(surrogates.CZ_delta_s(pts_delta_s)).T
        CZ_u           = np.atleast_2d(surrogates.CZ_u(pts_u)).T
        CZ_v           = np.atleast_2d(surrogates.CZ_v(pts_v)).T
        CZ_w           = np.atleast_2d(surrogates.CZ_w(pts_w)).T
        CZ_p           = np.atleast_2d(surrogates.CZ_p(pts_p)).T
        CZ_q           = np.atleast_2d(surrogates.CZ_q(pts_q)).T
        CZ_r           = np.atleast_2d(surrogates.CZ_r(pts_r)).T
        CL_alpha       = np.atleast_2d(surrogates.CL_alpha(pts_alpha)).T
        CL_beta        = np.atleast_2d(surrogates.CL_beta(pts_beta)).T
        CL_delta_a     = np.atleast_2d(surrogates.CL_delta_a(pts_delta_a)).T
        CL_delta_e     = np.atleast_2d(surrogates.CL_delta_e(pts_delta_e)).T
        CL_delta_r     = np.atleast_2d(surrogates.CL_delta_r(pts_delta_r)).T
        CL_delta_f     = np.atleast_2d(surrogates.CL_delta_f(pts_delta_f)).T
        #CL_delta_s     = np.atleast_2d(surrogates.CL_delta_s(pts_delta_s)).T
        CL_u           = np.atleast_2d(surrogates.CL_u(pts_u)).T
        CL_v           = np.atleast_2d(surrogates.CL_v(pts_v)).T
        CL_w           = np.atleast_2d(surrogates.CL_w(pts_w)).T
        CL_p           = np.atleast_2d(surrogates.CL_p(pts_p)).T
        CL_q           = np.atleast_2d(surrogates.CL_q(pts_q)).T
        CL_r           = np.atleast_2d(surrogates.CL_r(pts_r)).T
        CM_alpha       = np.atleast_2d(surrogates.CM_alpha(pts_alpha)).T
        CM_beta        = np.atleast_2d(surrogates.CM_beta(pts_beta)).T
        CM_delta_a     = np.atleast_2d(surrogates.CM_delta_a(pts_delta_a)).T
        CM_delta_e     = np.atleast_2d(surrogates.CM_delta_e(pts_delta_e)).T
        CM_delta_r     = np.atleast_2d(surrogates.CM_delta_r(pts_delta_r)).T
        CM_delta_f     = np.atleast_2d(surrogates.CM_delta_f(pts_delta_f)).T
        #CM_delta_s     = np.atleast_2d(surrogates.CM_delta_s(pts_delta_s)).T
        CM_u           = np.atleast_2d(surrogates.CM_u(pts_u)).T
        CM_v           = np.atleast_2d(surrogates.CM_v(pts_v)).T
        CM_w           = np.atleast_2d(surrogates.CM_w(pts_w)).T
        CM_p           = np.atleast_2d(surrogates.CM_p(pts_p)).T
        CM_q           = np.atleast_2d(surrogates.CM_q(pts_q)).T
        CM_r           = np.atleast_2d(surrogates.CM_r(pts_r)).T
        CN_alpha       = np.atleast_2d(surrogates.CN_alpha(pts_alpha)).T
        CN_beta        = np.atleast_2d(surrogates.CN_beta(pts_beta)).T
        CN_delta_a     = np.atleast_2d(surrogates.CN_delta_a(pts_delta_a)).T
        CN_delta_e     = np.atleast_2d(surrogates.CN_delta_e(pts_delta_e)).T
        CN_delta_r     = np.atleast_2d(surrogates.CN_delta_r(pts_delta_r)).T
        CN_delta_f     = np.atleast_2d(surrogates.CN_delta_f(pts_delta_f)).T
        #CN_delta_s     = np.atleast_2d(surrogates.CN_delta_s(pts_delta_s)).T
        CN_u           = np.atleast_2d(surrogates.CN_u(pts_u)).T
        CN_v           = np.atleast_2d(surrogates.CN_v(pts_v)).T
        CN_w           = np.atleast_2d(surrogates.CN_w(pts_w)).T
        CN_p           = np.atleast_2d(surrogates.CN_p(pts_p)).T
        CN_q           = np.atleast_2d(surrogates.CN_q(pts_q)).T
        CN_r           = np.atleast_2d(surrogates.CN_r(pts_r)).T
 
        # Stability Results  
        #conditions.S_ref                                                  = # Need to Update 
        #conditions.c_ref                                                  = # Need to Update
        #conditions.b_ref                                                  = # Need to Update
        #conditions.X_ref                                                  = # Need to Update
        #conditions.Y_ref                                                  = # Need to Update
        #conditions.Z_ref                                                  = # Need to Update 
        #conditions.aerodynamics.oswald_efficiency                         = # Need to Update
        conditions.static_stability.coefficients.lift                     = Clift_alpha + Clift_beta + Clift_delta_a + Clift_delta_e + Clift_delta_r + Clift_delta_f + Clift_u + Clift_v + Clift_w + Clift_p + Clift_q + Clift_r # + Clift_delta_s
        conditions.static_stability.coefficients.drag                     = Cdrag_alpha + Cdrag_beta + Cdrag_delta_a + Cdrag_delta_e + Cdrag_delta_r + Cdrag_delta_f + Cdrag_u + Cdrag_v + Cdrag_w + Cdrag_p + Cdrag_q + Cdrag_r # + Cdrag_delta_s     
        conditions.static_stability.coefficients.X                        = CX_alpha + CX_beta + CX_delta_a + CX_delta_e + CX_delta_r + CX_delta_f + CX_u + CX_v + CX_w + CX_p + CX_q + CX_r # + CX_delta_s     
        conditions.static_stability.coefficients.Y                        = CY_alpha + CY_beta + CY_delta_a + CY_delta_e + CY_delta_r + CY_delta_f + CY_u + CY_v + CY_w + CY_p + CY_q + CY_r # + CY_delta_s     
        conditions.static_stability.coefficients.Z                        = CZ_alpha + CZ_beta + CZ_delta_a + CZ_delta_e + CZ_delta_r + CZ_delta_f + CZ_u + CZ_v + CZ_w + CZ_p + CZ_q + CZ_r # + CZ_delta_s     
        conditions.static_stability.coefficients.L                        = CL_alpha + CL_beta + CL_delta_a + CL_delta_e + CL_delta_r + CL_delta_f + CL_u + CL_v + CL_w + CL_p + CL_q + CL_r # + CL_delta_s
        conditions.static_stability.coefficients.M                        = CM_alpha + CM_beta + CM_delta_a + CM_delta_e + CM_delta_r + CM_delta_f + CM_u + CM_v + CM_w + CM_p + CM_q + CM_r # + CM_delta_s
        conditions.static_stability.coefficients.N                        = CN_alpha + CN_beta + CN_delta_a + CN_delta_e + CN_delta_r + CN_delta_f + CN_u + CN_v + CN_w + CN_p + CN_q + CN_r # + CN_delta_s
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
     
    def evaluate_no_surrogate(self,state,settings,geometry):
        """Evaluates forces and moments directly using VLM.
        
        Assumptions:
            None
            
        Source:
            None
    
        Args:
            self       : VLM analysis          [unitless]
            state      : flight conditions     [unitless]
            settings   : VLM analysis settings [unitless]
            geometry   : vehicle configuration [unitless] 
            
        Returns: 
            None  
        """          

        # unpack        
        conditions = state.conditions
        settings   = self.settings
        geometry   = self.geometry     
        
        # if in transonic regime, use surrogate
        Clift,Cdrag,CX,CY,CZ,CL_mom,CM,CN = evaluate_VLM(conditions,settings,geometry) 

        # compute deriviatives and pack   
        conditions.static_stability.coefficients.lift    = np.atleast_2d(Clift).T
        conditions.static_stability.coefficients.drag    = np.atleast_2d(Cdrag).T 
        conditions.static_stability.coefficients.X      = np.atleast_2d(CX).T # NEED TO CHANGE np.atleast_2d(CX).T
        conditions.static_stability.coefficients.Y      = np.atleast_2d(CY).T
        conditions.static_stability.coefficients.Z      = np.atleast_2d(CZ).T # NEED TO CHANGE np.atleast_2d(CZ).T
        conditions.static_stability.coefficients.L      = np.atleast_2d(CL_mom).T
        conditions.static_stability.coefficients.M      = np.atleast_2d(CM).T
        conditions.static_stability.coefficients.N      = np.atleast_2d(CN).T 
        return  
    
    def sample_training(self):
        """Call methods to run VLM for sample point evaluation. 
        
        Assumptions:
            None
            
        Source:
            None
    
        Args:
            self       : VLM analysis          [unitless] 
            
        Returns: 
            None    
        """
        # unpack
        geometry       = self.geometry
        settings       = self.settings
        training       = self.training
        Mach           = training.Mach
        AoA            = training.angle_of_attack                  
        Beta           = training.sideslip_angle         
        delta_a        = training.aileron_deflection              
        delta_e        = training.elevator_deflection                
        delta_r        = training.rudder_deflection
        delta_f        = training.flap_deflection
        #delta_s        = training.slat_deflection          
        u              = training.u
        v              = training.v
        w              = training.w
        pitch_rate     = training.pitch_rate
        roll_rate      = training.roll_rate
        yaw_rate       = training.yaw_rate

        len_Mach       = len(Mach)        
        len_AoA        = len(AoA)  
        len_Beta       = len(Beta)
        len_u          = len(u)
        len_v          = len(v)
        len_w          = len(w)
        len_pitch_rate = len(pitch_rate)
        len_roll_rate  = len(roll_rate) 
        len_yaw_rate   = len(yaw_rate)
        
        # only compute derivative if control surface exists
        for wing in geometry.wings: 
            # Elevator 
            for control_surface in wing.control_surfaces:  
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Aileron: 
                    len_d_a        = len(delta_a)
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Elevator: 
                    len_d_e        = len(delta_e)   
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Rudder:  
                    len_d_r        = len(delta_r) 
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Flap:  
                    len_d_f        = len(delta_f)  
                #if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Slat:  
                    #len_d_s        = len(delta_s)
        
        # --------------------------------------------------------------------------------------------------------------
        # Alpha
        # --------------------------------------------------------------------------------------------------------------
        
        # Setup new array shapes for vectorization 
        # stakcing 9x9 matrices into one horizontal line(81)  
        AoAs       = np.atleast_2d(np.tile(AoA,len_Mach).T.flatten()).T 
        Machs      = np.atleast_2d(np.repeat(Mach,len_AoA)).T        
        
        # reset conditions 
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.freestream.mach_number               = Machs
        conditions.aerodynamics.angles.alpha            = np.ones_like(Machs)*AoAs
        conditions.aerodynamics.angles.beta             = np.zeros_like(Machs)   
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs) 
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.control_surfaces.flap.deflection     = np.zeros_like(Machs)
        #conditions.control_surfaces.slat.deflection     = np.zeros_like(Machs)
        conditions.freestream.u                         = np.zeros_like(Machs)
        conditions.freestream.v                         = np.zeros_like(Machs)
        conditions.freestream.w                         = np.zeros_like(Machs)
        conditions.static_stability.pitch_rate          = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate           = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate            = np.zeros_like(Machs)
        conditions.freestream.velocity                  = np.zeros_like(Machs)  
        
        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)
        
        Clift_alpha   = np.reshape(Clift_res,(len_Mach,len_AoA)).T 
        Cdrag_alpha   = np.reshape(Cdrag_res,(len_Mach,len_AoA)).T 
        CX_alpha      = np.reshape(CX_res,(len_Mach,len_AoA)).T 
        CY_alpha      = np.reshape(CY_res,(len_Mach,len_AoA)).T 
        CZ_alpha      = np.reshape(CZ_res,(len_Mach,len_AoA)).T 
        CL_alpha      = np.reshape(CL_res,(len_Mach,len_AoA)).T 
        CM_alpha      = np.reshape(CM_res,(len_Mach,len_AoA)).T 
        CN_alpha      = np.reshape(CN_res,(len_Mach,len_AoA)).T
        
        # --------------------------------------------------------------------------------------------------------------
        # Beta 
        # --------------------------------------------------------------------------------------------------------------
        Betas         = np.atleast_2d(np.tile(Beta,len_Mach).T.flatten()).T 
        Machs         = np.atleast_2d(np.repeat(Mach,len_Beta)).T        

        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.freestream.mach_number               = Machs
        conditions.aerodynamics.angles.alpha            = np.zeros_like(Machs)
        conditions.aerodynamics.angles.beta             = np.ones_like(Machs)*Betas  
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs) 
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.control_surfaces.flap.deflection     = np.zeros_like(Machs)
        #conditions.control_surfaces.slat.deflection     = np.zeros_like(Machs)
        conditions.freestream.u                         = np.zeros_like(Machs)
        conditions.freestream.v                         = np.zeros_like(Machs)
        conditions.freestream.w                         = np.zeros_like(Machs)
        conditions.static_stability.pitch_rate          = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate           = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate            = np.zeros_like(Machs)
        conditions.freestream.velocity                  = np.zeros_like(Machs) 
        
        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)
        
        Clift_beta = np.reshape(Clift_res,(len_Mach,len_Beta)).T 
        Cdrag_beta = np.reshape(Cdrag_res,(len_Mach,len_Beta)).T                                 
        CX_beta = np.reshape(CX_res,(len_Mach,len_Beta)).T 
        CY_beta = np.reshape(CY_res,(len_Mach,len_Beta)).T 
        CZ_beta = np.reshape(CZ_res,(len_Mach,len_Beta)).T 
        CL_beta = np.reshape(CL_res,(len_Mach,len_Beta)).T 
        CM_beta = np.reshape(CM_res,(len_Mach,len_Beta)).T 
        CN_beta = np.reshape(CN_res,(len_Mach,len_Beta)).T 
                     
        # --------------------------------------------------------------------------------------------------------------
        # Aileron 
        # --------------------------------------------------------------------------------------------------------------    
        Delta_a_s     = np.atleast_2d(np.tile(delta_a,len_Mach).T.flatten()).T 
        Machs         = np.atleast_2d(np.repeat(Mach,len_d_a)).T    

        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.freestream.mach_number               = Machs
        conditions.aerodynamics.angles.alpha            = np.zeros_like(Machs)
        conditions.aerodynamics.angles.beta             = np.zeros_like(Machs) 
        conditions.control_surfaces.aileron.deflection  = np.ones_like(Machs) *Delta_a_s
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.control_surfaces.flap.deflection     = np.zeros_like(Machs)
        #conditions.control_surfaces.slat.deflection     = np.zeros_like(Machs)
        conditions.freestream.u                         = np.zeros_like(Machs)
        conditions.freestream.v                         = np.zeros_like(Machs)
        conditions.freestream.w                         = np.zeros_like(Machs)
        conditions.static_stability.pitch_rate          = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate           = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate            = np.zeros_like(Machs)
        conditions.freestream.velocity                  = np.zeros_like(Machs)
        
        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)
        
        Clift_d_a = np.reshape(Clift_res,(len_Mach,len_d_a)).T 
        Cdrag_d_a = np.reshape(Cdrag_res,(len_Mach,len_d_a)).T                                 
        CX_d_a    = np.reshape(CX_res,(len_Mach,len_d_a)).T 
        CY_d_a    = np.reshape(CY_res,(len_Mach,len_d_a)).T 
        CZ_d_a    = np.reshape(CZ_res,(len_Mach,len_d_a)).T 
        CL_d_a    = np.reshape(CL_res,(len_Mach,len_d_a)).T 
        CM_d_a    = np.reshape(CM_res,(len_Mach,len_d_a)).T 
        CN_d_a    = np.reshape(CN_res,(len_Mach,len_d_a)).T         

        # --------------------------------------------------------------------------------------------------------------
        # Elevator 
        # --------------------------------------------------------------------------------------------------------------
        Delta_e_s     = np.atleast_2d(np.tile(delta_e,len_Mach).T.flatten()).T 
        Machs         = np.atleast_2d(np.repeat(Mach,len_d_e)).T        
            
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.freestream.mach_number               = Machs
        conditions.aerodynamics.angles.alpha            = np.zeros_like(Machs)
        conditions.aerodynamics.angles.beta             = np.zeros_like(Machs) 
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs) 
        conditions.control_surfaces.elevator.deflection = np.ones_like(Machs)*Delta_e_s
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.control_surfaces.flap.deflection     = np.zeros_like(Machs)
        #conditions.control_surfaces.slat.deflection     = np.zeros_like(Machs)
        conditions.freestream.u                         = np.zeros_like(Machs)
        conditions.freestream.v                         = np.zeros_like(Machs)
        conditions.freestream.w                         = np.zeros_like(Machs)
        conditions.static_stability.pitch_rate          = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate           = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate            = np.zeros_like(Machs)
        conditions.freestream.velocity                  = np.zeros_like(Machs)
        
        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)
        
        Clift_d_e = np.reshape(Clift_res,(len_Mach,len_d_e)).T 
        Cdrag_d_e = np.reshape(Cdrag_res,(len_Mach,len_d_e)).T                                 
        CX_d_e    = np.reshape(CX_res,(len_Mach,len_d_e)).T 
        CY_d_e    = np.reshape(CY_res,(len_Mach,len_d_e)).T 
        CZ_d_e    = np.reshape(CZ_res,(len_Mach,len_d_e)).T 
        CL_d_e    = np.reshape(CL_res,(len_Mach,len_d_e)).T 
        CM_d_e    = np.reshape(CM_res,(len_Mach,len_d_e)).T 
        CN_d_e    = np.reshape(CN_res,(len_Mach,len_d_e)).T       
                        
        # --------------------------------------------------------------------------------------------------------------
        # Rudder 
        # --------------------------------------------------------------------------------------------------------------
        Delta_r_s     = np.atleast_2d(np.tile(delta_r,len_Mach).T.flatten()).T 
        Machs         = np.atleast_2d(np.repeat(Mach,len_d_r)).T        
                
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.freestream.mach_number               = Machs
        conditions.aerodynamics.angles.alpha            = np.zeros_like(Machs)
        conditions.aerodynamics.angles.beta             = np.zeros_like(Machs) 
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs) 
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.ones_like(Machs)*Delta_r_s
        conditions.control_surfaces.flap.deflection     = np.zeros_like(Machs)
        #conditions.control_surfaces.slat.deflection     = np.zeros_like(Machs)
        conditions.freestream.u                         = np.zeros_like(Machs)
        conditions.freestream.v                         = np.zeros_like(Machs)
        conditions.freestream.w                         = np.zeros_like(Machs)
        conditions.static_stability.pitch_rate          = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate           = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate            = np.zeros_like(Machs)
        conditions.freestream.velocity                  = np.zeros_like(Machs)
        
        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)      
    
        Clift_d_r = np.reshape(Clift_res,(len_Mach,len_d_r)).T 
        Cdrag_d_r = np.reshape(Cdrag_res,(len_Mach,len_d_r)).T                                 
        CX_d_r    = np.reshape(CX_res,(len_Mach,len_d_r)).T 
        CY_d_r    = np.reshape(CY_res,(len_Mach,len_d_r)).T 
        CZ_d_r    = np.reshape(CZ_res,(len_Mach,len_d_r)).T 
        CL_d_r    = np.reshape(CL_res,(len_Mach,len_d_r)).T 
        CM_d_r    = np.reshape(CM_res,(len_Mach,len_d_r)).T 
        CN_d_r    = np.reshape(CN_res,(len_Mach,len_d_r)).T
                        
        # --------------------------------------------------------------------------------------------------------------
        # Flap 
        # --------------------------------------------------------------------------------------------------------------
        Delta_f_s     = np.atleast_2d(np.tile(delta_f, len_Mach).T.flatten()).T 
        Machs         = np.atleast_2d(np.repeat(Mach,len_d_f)).T          

        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.freestream.mach_number               = Machs
        conditions.aerodynamics.angles.alpha            = np.zeros_like(Machs)
        conditions.aerodynamics.angles.beta             = np.zeros_like(Machs) 
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs) 
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.control_surfaces.flap.deflection     = np.ones_like(Machs)*Delta_f_s
        #conditions.control_surfaces.slat.deflection     = np.zeros_like(Machs)
        conditions.freestream.u                         = np.zeros_like(Machs)
        conditions.freestream.v                         = np.zeros_like(Machs)
        conditions.freestream.w                         = np.zeros_like(Machs)
        conditions.static_stability.pitch_rate          = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate           = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate            = np.zeros_like(Machs)
        conditions.freestream.velocity                  = np.zeros_like(Machs)
        
        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)      

        Clift_d_f = np.reshape(Clift_res,(len_Mach,len_d_f)).T 
        Cdrag_d_f = np.reshape(Cdrag_res,(len_Mach,len_d_f)).T                                 
        CX_d_f    = np.reshape(CX_res,(len_Mach,len_d_f)).T 
        CY_d_f    = np.reshape(CY_res,(len_Mach,len_d_f)).T 
        CZ_d_f    = np.reshape(CZ_res,(len_Mach,len_d_f)).T 
        CL_d_f    = np.reshape(CL_res,(len_Mach,len_d_f)).T 
        CM_d_f    = np.reshape(CM_res,(len_Mach,len_d_f)).T 
        CN_d_f    = np.reshape(CN_res,(len_Mach,len_d_f)).T
                        
        ## --------------------------------------------------------------------------------------------------------------
        ## Slat 
        ## --------------------------------------------------------------------------------------------------------------         
        #Delta_s_s     = np.atleast_2d(np.tile(delta_s, len_Mach).T.flatten()).T 
        #Machs         = np.atleast_2d(np.repeat(Mach,len_d_s)).T          

        #conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        #conditions.freestream.mach_number               = Machs
        #conditions.aerodynamics.angles.alpha            = np.zeros_like(Machs)
        #conditions.aerodynamics.angles.beta             = np.zeros_like(Machs) 
        #conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs) 
        #conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        #conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        #conditions.control_surfaces.flap.deflection     = np.zeros_like(Machs)
        #conditions.control_surfaces.slat.deflection     = np.ones_like(Machs)*Delta_s_s
        #conditions.freestream.u                         = np.zeros_like(Machs)
        #conditions.freestream.v                         = np.zeros_like(Machs)
        #conditions.freestream.w                         = np.zeros_like(Machs)
        #conditions.static_stability.pitch_rate          = np.zeros_like(Machs)      
        #conditions.static_stability.roll_rate           = np.zeros_like(Machs)
        #conditions.static_stability.yaw_rate            = np.zeros_like(Machs)
        #conditions.freestream.velocity                  = np.zeros_like(Machs)
        
        #Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)      
    
        #Clift_d_s = np.reshape(Clift_res,(len_Mach,len_d_s)).T 
        #Cdrag_d_s = np.reshape(Cdrag_res,(len_Mach,len_d_s)).T                                 
        #CX_d_s    = np.reshape(CX_res,(len_Mach,len_d_s)).T 
        #CY_d_s    = np.reshape(CY_res,(len_Mach,len_d_s)).T 
        #CZ_d_s    = np.reshape(CZ_res,(len_Mach,len_d_s)).T 
        #CL_d_s    = np.reshape(CL_res,(len_Mach,len_d_s)).T 
        #CM_d_s    = np.reshape(CM_res,(len_Mach,len_d_s)).T 
        #CN_d_s    = np.reshape(CN_res,(len_Mach,len_d_s)).T                          
                
        # -------------------------------------------------------               
        # Velocity u 
        # -------------------------------------------------------
        u_s     = np.atleast_2d(np.tile(u, len_Mach).T.flatten()).T 
        Machs         = np.atleast_2d(np.repeat(Mach,len_u)).T                  
        
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.aerodynamics.angles.alpha            = np.zeros_like(Machs)
        conditions.aerodynamics.angles.beta             = np.zeros_like(Machs) 
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs) 
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.control_surfaces.flap.deflection     = np.zeros_like(Machs)
        #conditions.control_surfaces.slat.deflection     = np.zeros_like(Machs)
        conditions.freestream.u                         = np.ones_like(Machs)*u_s
        conditions.freestream.v                         = np.zeros_like(Machs)
        conditions.freestream.w                         = np.zeros_like(Machs)
        conditions.static_stability.pitch_rate          = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate           = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate            = np.zeros_like(Machs)
        conditions.freestream.velocity                  = np.zeros_like(Machs)
        conditions.freestream.mach_number               = Machs + conditions.freestream.u/343
        
        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)
        
        Clift_u     = np.reshape(Clift_res,(len_Mach,len_u)).T 
        Cdrag_u     = np.reshape(Cdrag_res,(len_Mach,len_u)).T 
        CX_u        = np.reshape(CX_res,(len_Mach,len_u)).T  
        CY_u        = np.reshape(CY_res,(len_Mach,len_u)).T  
        CZ_u        = np.reshape(CZ_res,(len_Mach,len_u)).T  
        CL_u        = np.reshape(CL_res,(len_Mach,len_u)).T  
        CM_u        = np.reshape(CM_res,(len_Mach,len_u)).T  
        CN_u        = np.reshape(CN_res,(len_Mach,len_u)).T
        
        # -------------------------------------------------------               
        # Velocity v 
        # -------------------------------------------------------
        v_s     = np.atleast_2d(np.tile(v, len_Mach).T.flatten()).T 
        Machs         = np.atleast_2d(np.repeat(Mach,len_v)).T    
        
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.aerodynamics.angles.alpha            = np.zeros_like(Machs)
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs) 
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.control_surfaces.flap.deflection     = np.zeros_like(Machs)
        #conditions.control_surfaces.slat.deflection     = np.zeros_like(Machs)
        conditions.freestream.u                         = np.zeros_like(Machs)
        conditions.freestream.v                         = np.ones_like(Machs)*v_s
        conditions.freestream.w                         = np.zeros_like(Machs)
        conditions.static_stability.pitch_rate          = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate           = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate            = np.zeros_like(Machs)
        conditions.freestream.velocity                  = np.zeros_like(Machs)
        conditions.freestream.mach_number               = Machs
        conditions.aerodynamics.angles.beta             = np.arcsin(conditions.freestream.v/(conditions.freestream.mach_number*343))         
        
        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)
        
        Clift_v     = np.reshape(Clift_res,(len_Mach,len_v)).T 
        Cdrag_v     = np.reshape(Cdrag_res,(len_Mach,len_v)).T 
        CX_v        = np.reshape(CX_res,(len_Mach,len_v)).T  
        CY_v        = np.reshape(CY_res,(len_Mach,len_v)).T  
        CZ_v        = np.reshape(CZ_res,(len_Mach,len_v)).T  
        CL_v        = np.reshape(CL_res,(len_Mach,len_v)).T  
        CM_v        = np.reshape(CM_res,(len_Mach,len_v)).T  
        CN_v        = np.reshape(CN_res,(len_Mach,len_v)).T
        
        # -------------------------------------------------------               
        # Velocity w 
        # -------------------------------------------------------
        w_s     = np.atleast_2d(np.tile(w, len_Mach).T.flatten()).T 
        Machs         = np.atleast_2d(np.repeat(Mach,len_w)).T    
        
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs) 
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.control_surfaces.flap.deflection     = np.zeros_like(Machs)
        #conditions.control_surfaces.slat.deflection     = np.zeros_like(Machs)
        conditions.freestream.u                         = np.zeros_like(Machs)
        conditions.freestream.v                         = np.zeros_like(Machs)
        conditions.freestream.w                         = np.ones_like(Machs)*w_s
        conditions.static_stability.pitch_rate          = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate           = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate            = np.zeros_like(Machs)
        conditions.freestream.velocity                  = np.zeros_like(Machs)
        conditions.freestream.mach_number               = Machs
        conditions.aerodynamics.angles.beta             = np.zeros_like(Machs)
        conditions.aerodynamics.angles.alpha            = np.arcsin(conditions.freestream.w/(conditions.freestream.velocity*343))
        
        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)
        
        Clift_w     = np.reshape(Clift_res,(len_Mach,len_w)).T 
        Cdrag_w     = np.reshape(Cdrag_res,(len_Mach,len_w)).T 
        CX_w        = np.reshape(CX_res,(len_Mach,len_w)).T  
        CY_w        = np.reshape(CY_res,(len_Mach,len_w)).T  
        CZ_w        = np.reshape(CZ_res,(len_Mach,len_w)).T  
        CL_w        = np.reshape(CL_res,(len_Mach,len_w)).T  
        CM_w        = np.reshape(CM_res,(len_Mach,len_w)).T  
        CN_w        = np.reshape(CN_res,(len_Mach,len_w)).T            
                        
        # -------------------------------------------------------               
        # Pitch Rate 
        # -------------------------------------------------------
        q_s     = np.atleast_2d(np.tile(pitch_rate, len_Mach).T.flatten()).T 
        Machs         = np.atleast_2d(np.repeat(Mach,len_pitch_rate)).T
        
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.freestream.mach_number               = Machs
        conditions.aerodynamics.angles.alpha            = np.zeros_like(Machs)
        conditions.aerodynamics.angles.beta             = np.zeros_like(Machs) 
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs) 
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.control_surfaces.flap.deflection     = np.zeros_like(Machs)
        #conditions.control_surfaces.slat.deflection     = np.zeros_like(Machs)
        conditions.freestream.u                         = np.zeros_like(Machs)
        conditions.freestream.v                         = np.zeros_like(Machs)
        conditions.freestream.w                         = np.zeros_like(Machs)
        conditions.static_stability.pitch_rate          = np.ones_like(Machs)*q_s      
        conditions.static_stability.roll_rate           = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate            = np.zeros_like(Machs)
        conditions.freestream.velocity                  = Machs * 343 # speed of sound   
        
        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)
        
        Clift_pitch_rate     = np.reshape(Clift_res,(len_Mach,len_pitch_rate)).T 
        Cdrag_pitch_rate     = np.reshape(Cdrag_res,(len_Mach,len_pitch_rate)).T 
        CX_pitch_rate        = np.reshape(CX_res,(len_Mach,len_pitch_rate)).T  
        CY_pitch_rate        = np.reshape(CY_res,(len_Mach,len_pitch_rate)).T  
        CZ_pitch_rate        = np.reshape(CZ_res,(len_Mach,len_pitch_rate)).T  
        CL_pitch_rate        = np.reshape(CL_res,(len_Mach,len_pitch_rate)).T  
        CM_pitch_rate        = np.reshape(CM_res,(len_Mach,len_pitch_rate)).T  
        CN_pitch_rate        = np.reshape(CN_res,(len_Mach,len_pitch_rate)).T  
    
        # -------------------------------------------------------               
        # Roll  Rate 
        # -------------------------------------------------------    
        p_s     = np.atleast_2d(np.tile(roll_rate, len_Mach).T.flatten()).T 
        Machs         = np.atleast_2d(np.repeat(Mach,len_roll_rate)).T
        
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.freestream.mach_number               = Machs
        conditions.aerodynamics.angles.alpha            = np.zeros_like(Machs)
        conditions.aerodynamics.angles.beta             = np.zeros_like(Machs) 
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs) 
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.control_surfaces.flap.deflection     = np.zeros_like(Machs)
        #conditions.control_surfaces.slat.deflection     = np.zeros_like(Machs)
        conditions.freestream.u                         = np.zeros_like(Machs)
        conditions.freestream.v                         = np.zeros_like(Machs)
        conditions.freestream.w                         = np.zeros_like(Machs)
        conditions.static_stability.pitch_rate          = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate           = np.ones_like(Machs)*p_s
        conditions.static_stability.yaw_rate            = np.zeros_like(Machs)
        conditions.freestream.velocity                  = Machs * 343 # speed of sound           
            
        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)  
            
        Clift_roll_rate     = np.reshape(Clift_res,(len_Mach,len_roll_rate)).T 
        Cdrag_roll_rate     = np.reshape(Cdrag_res,(len_Mach,len_roll_rate)).T 
        CX_roll_rate        = np.reshape(CX_res,(len_Mach,len_roll_rate)).T  
        CY_roll_rate        = np.reshape(CY_res,(len_Mach,len_roll_rate)).T  
        CZ_roll_rate        = np.reshape(CZ_res,(len_Mach,len_roll_rate)).T  
        CL_roll_rate        = np.reshape(CL_res,(len_Mach,len_roll_rate)).T  
        CM_roll_rate        = np.reshape(CM_res,(len_Mach,len_roll_rate)).T  
        CN_roll_rate        = np.reshape(CN_res,(len_Mach,len_roll_rate)).T        

        # -------------------------------------------------------               
        # Yaw Rate 
        # -------------------------------------------------------        
        r_s     = np.atleast_2d(np.tile(yaw_rate, len_Mach).T.flatten()).T 
        Machs         = np.atleast_2d(np.repeat(Mach,len_yaw_rate)).T

        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.freestream.mach_number               = Machs
        conditions.aerodynamics.angles.alpha            = np.zeros_like(Machs)
        conditions.aerodynamics.angles.beta             = np.zeros_like(Machs) 
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs) 
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.control_surfaces.flap.deflection     = np.zeros_like(Machs)
        #conditions.control_surfaces.slat.deflection     = np.zeros_like(Machs)
        conditions.freestream.u                         = np.zeros_like(Machs)
        conditions.freestream.v                         = np.zeros_like(Machs)
        conditions.freestream.w                         = np.zeros_like(Machs)
        conditions.static_stability.pitch_rate          = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate           = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate            = np.ones_like(Machs)*r_s
        conditions.freestream.velocity                  = Machs * 343 # speed of sound  
        
        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)
        
        Clift_yaw_rate     = np.reshape(Clift_res,(len_Mach,len_yaw_rate)).T 
        Cdrag_yaw_rate     = np.reshape(Cdrag_res,(len_Mach,len_yaw_rate)).T 
        CX_yaw_rate        = np.reshape(CX_res,(len_Mach,len_yaw_rate)).T  
        CY_yaw_rate        = np.reshape(CY_res,(len_Mach,len_yaw_rate)).T  
        CZ_yaw_rate        = np.reshape(CZ_res,(len_Mach,len_yaw_rate)).T  
        CL_yaw_rate        = np.reshape(CL_res,(len_Mach,len_yaw_rate)).T  
        CM_yaw_rate        = np.reshape(CM_res,(len_Mach,len_yaw_rate)).T  
        CN_yaw_rate        = np.reshape(CN_res,(len_Mach,len_yaw_rate)).T
            
        training.Clift_alpha    = Clift_alpha   
        training.Clift_beta     = Clift_beta    
        training.Clift_delta_a  = Clift_d_a 
        training.Clift_delta_e  = Clift_d_e 
        training.Clift_delta_r  = Clift_d_r 
        training.Clift_delta_f  = Clift_d_f 
        #training.Clift_delta_s  = Clift_d_s 
        training.Clift_u        = Clift_u       
        training.Clift_v        = Clift_v       
        training.Clift_w        = Clift_w       
        training.Clift_p        = Clift_roll_rate       
        training.Clift_q        = Clift_pitch_rate       
        training.Clift_r        = Clift_yaw_rate       
        training.Cdrag_alpha    = Cdrag_alpha   
        training.Cdrag_beta     = Cdrag_beta    
        training.Cdrag_delta_a  = Cdrag_d_a 
        training.Cdrag_delta_e  = Cdrag_d_e 
        training.Cdrag_delta_r  = Cdrag_d_r 
        training.Cdrag_delta_f  = Cdrag_d_f 
        #training.Cdrag_delta_s  = Cdrag_d_s 
        training.Cdrag_u        = Cdrag_u       
        training.Cdrag_v        = Cdrag_v       
        training.Cdrag_w        = Cdrag_w       
        training.Cdrag_p        = Cdrag_roll_rate        
        training.Cdrag_q        = Cdrag_pitch_rate       
        training.Cdrag_r        = Cdrag_yaw_rate         
        training.CX_alpha       = CX_alpha      
        training.CX_beta        = CX_beta       
        training.CX_delta_a     = CX_d_a    
        training.CX_delta_e     = CX_d_e    
        training.CX_delta_r     = CX_d_r    
        training.CX_delta_f     = CX_d_f    
        #training.CX_delta_s     = CX_d_s    
        training.CX_u           = CX_u          
        training.CX_v           = CX_v          
        training.CX_w           = CX_w          
        training.CX_p           = CX_roll_rate           
        training.CX_q           = CX_pitch_rate          
        training.CX_r           = CX_yaw_rate            
        training.CY_alpha       = CY_alpha      
        training.CY_beta        = CY_beta       
        training.CY_delta_a     = CY_d_a    
        training.CY_delta_e     = CY_d_e    
        training.CY_delta_r     = CY_d_r    
        training.CY_delta_f     = CY_d_f    
        #training.CY_delta_s     = CY_d_s    
        training.CY_u           = CY_u          
        training.CY_v           = CY_v          
        training.CY_w           = CY_w          
        training.CY_p           = CY_roll_rate            
        training.CY_q           = CY_pitch_rate           
        training.CY_r           = CY_yaw_rate             
        training.CZ_alpha       = CZ_alpha      
        training.CZ_beta        = CZ_beta       
        training.CZ_delta_a     = CZ_d_a    
        training.CZ_delta_e     = CZ_d_e    
        training.CZ_delta_r     = CZ_d_r    
        training.CZ_delta_f     = CZ_d_f    
        #training.CZ_delta_s     = CZ_d_s    
        training.CZ_u           = CZ_u          
        training.CZ_v           = CZ_v          
        training.CZ_w           = CZ_w          
        training.CZ_p           = CZ_roll_rate           
        training.CZ_q           = CZ_pitch_rate          
        training.CZ_r           = CZ_yaw_rate            
        training.CL_alpha       = CL_alpha      
        training.CL_beta        = CL_beta       
        training.CL_delta_a     = CL_d_a    
        training.CL_delta_e     = CL_d_e    
        training.CL_delta_r     = CL_d_r    
        training.CL_delta_f     = CL_d_f    
        #training.CL_delta_s     = CL_d_s    
        training.CL_u           = CL_u          
        training.CL_v           = CL_v          
        training.CL_w           = CL_w          
        training.CL_p           = CL_roll_rate           
        training.CL_q           = CL_pitch_rate          
        training.CL_r           = CL_yaw_rate            
        training.CM_alpha       = CM_alpha      
        training.CM_beta        = CM_beta       
        training.CM_delta_a     = CM_d_a    
        training.CM_delta_e     = CM_d_e    
        training.CM_delta_r     = CM_d_r    
        training.CM_delta_f     = CM_d_f    
        #training.CM_delta_s     = CM_d_s    
        training.CM_u           = CM_u          
        training.CM_v           = CM_v          
        training.CM_w           = CM_w          
        training.CM_p           = CM_roll_rate             
        training.CM_q           = CM_pitch_rate            
        training.CM_r           = CM_yaw_rate              
        training.CN_alpha       = CN_alpha      
        training.CN_beta        = CN_beta       
        training.CN_delta_a     = CN_d_a    
        training.CN_delta_e     = CN_d_e    
        training.CN_delta_r     = CN_d_r    
        training.CN_delta_f     = CN_d_f    
        #training.CN_delta_s     = CN_d_s    
        training.CN_u           = CN_u          
        training.CN_v           = CN_v          
        training.CN_w           = CN_w          
        training.CN_p           = CN_roll_rate            
        training.CN_q           = CN_pitch_rate           
        training.CN_r           = CN_yaw_rate             
        
        training.dClift_dalpha = (Clift_alpha[0,:] - Clift_alpha[1,:]) / (AoA[0] - AoA[1])
        training.dClift_dbeta = (Clift_beta[0,:] - Clift_beta[1,:]) / (Beta[0] - Beta[1])
        training.dClift_ddelta_da = (Clift_d_a[0,:] - Clift_d_a[1,:]) / (delta_a[0] - delta_a[1])
        training.dClift_ddelta_de = (Clift_d_e[0,:] - Clift_d_e[1,:]) / (delta_e[0] - delta_e[1])   
        training.dClift_ddelta_dr = (Clift_d_r[0,:] - Clift_d_r[1,:]) / (delta_r[0] - delta_r[1])   
        training.dClift_ddelta_df = (Clift_d_f[0,:] - Clift_d_f[1,:]) / (delta_f[0] - delta_f[1])   
        #training.dClift_ddelta_ds = (Clift_d_s[0,:] - Clift_d_s[1,:]) / (delta_s[0] - delta_s[1])   
        training.dClift_du = (Clift_u[0,:] - Clift_u[1,:]) / (u[0] - u[1])            
        training.dClift_dv = (Clift_v[0,:] - Clift_v[1,:]) / (v[0] - v[1])          
        training.dClift_dw = (Clift_w[0,:] - Clift_w[1,:]) / (w[0] - w[1])         
        training.dClift_dp = (Clift_roll_rate[0,:] - Clift_roll_rate[1,:]) / (roll_rate[0]-roll_rate[1])            
        training.dClift_dq = (Clift_pitch_rate[0,:] - Clift_pitch_rate[1,:]) / (pitch_rate[0]-pitch_rate[1])        
        training.dClift_dr = (Clift_yaw_rate[0,:] - Clift_yaw_rate[1,:]) / (yaw_rate[0]-yaw_rate[1])                
        training.dCdrag_dalpha = (Cdrag_alpha[0,:] - Cdrag_alpha[1,:]) / (AoA[0] - AoA[1])    
        training.dCdrag_dbeta = (Cdrag_beta[0,:] - Cdrag_beta[1,:]) / (Beta[0] - Beta[1])      
        training.dCdrag_ddelta_a = (Cdrag_d_a[0,:] - Cdrag_d_a[1,:]) / (delta_a[0] - delta_a[1])   
        training.dCdrag_ddelta_e = (Cdrag_d_e[0,:] - Cdrag_d_e[1,:]) / (delta_e[0] - delta_e[1])   
        training.dCdrag_ddelta_r = (Cdrag_d_r[0,:] - Cdrag_d_r[1,:]) / (delta_r[0] - delta_r[1])   
        training.dCdrag_ddelta_f = (Cdrag_d_f[0,:] - Cdrag_d_f[1,:]) / (delta_f[0] - delta_f[1])   
        #training.dCdrag_ddelta_s = (Cdrag_d_s[0,:] - Cdrag_d_s[1,:]) / (delta_s[0] - delta_s[1])   
        training.dCdrag_du = (Cdrag_u[0,:] - Cdrag_u[1,:]) / (u[0] - u[1])                     
        training.dCdrag_dv = (Cdrag_v[0,:] - Cdrag_v[1,:]) / (v[0] - v[1])                   
        training.dCdrag_dw = (Cdrag_w[0,:] - Cdrag_w[1,:]) / (w[0] - w[1])                  
        training.dCdrag_dp = (Cdrag_roll_rate[0,:] - Cdrag_roll_rate[1,:]) / (roll_rate[0]-roll_rate[1])             
        training.dCdrag_dq = (Cdrag_pitch_rate[0,:] - Cdrag_pitch_rate[1,:]) / (pitch_rate[0]-pitch_rate[1])         
        training.dCdrag_dr = (Cdrag_yaw_rate[0,:] - Cdrag_yaw_rate[1,:]) / (yaw_rate[0]-yaw_rate[1])                 
        training.dCX_dalpha = (CX_alpha[0,:] - CX_alpha[1,:]) / (AoA[0] - AoA[1])            
        training.dCX_dbeta = (CX_beta[0,:] - CX_beta[1,:]) / (Beta[0] - Beta[1])              
        training.dCX_ddelta_a = (CX_d_a[0,:] - CX_d_a[1,:]) / (delta_a[0] - delta_a[1])      
        training.dCX_ddelta_e = (CX_d_e[0,:] - CX_d_e[1,:]) / (delta_e[0] - delta_e[1])      
        training.dCX_ddelta_r = (CX_d_r[0,:] - CX_d_r[1,:]) / (delta_r[0] - delta_r[1])      
        training.dCX_ddelta_f = (CX_d_f[0,:] - CX_d_f[1,:]) / (delta_f[0] - delta_f[1])      
        #training.dCX_ddelta_s = (CX_d_s[0,:] - CX_d_s[1,:]) / (delta_s[0] - delta_s[1])      
        training.dCX_du = (CX_u[0,:] - CX_u[1,:]) / (u[0] - u[1])                                 
        training.dCX_dv = (CX_v[0,:] - CX_v[1,:]) / (v[0] - v[1])                               
        training.dCX_dw = (CX_w[0,:] - CX_w[1,:]) / (w[0] - w[1])                              
        training.dCX_dp = (CX_roll_rate[0,:] - CX_roll_rate[1,:]) / (roll_rate[0]-roll_rate[1])                
        training.dCX_dq = (CX_pitch_rate[0,:] - CX_pitch_rate[1,:]) / (pitch_rate[0]-pitch_rate[1])            
        training.dCX_dr = (CX_yaw_rate[0,:] - CX_yaw_rate[1,:]) / (yaw_rate[0]-yaw_rate[1])                    
        training.dCY_dalpha = (CY_alpha[0,:] - CY_alpha[1,:]) / (AoA[0] - AoA[1])         
        training.dCY_dbeta = (CY_beta[0,:] - CY_beta[1,:]) / (Beta[0] - Beta[1])          
        training.dCY_ddelta_a = (CY_d_a[0,:] - CY_d_a[1,:]) / (delta_a[0] - delta_a[1])      
        training.dCY_ddelta_e = (CY_d_e[0,:] - CY_d_e[1,:]) / (delta_e[0] - delta_e[1])      
        training.dCY_ddelta_r = (CY_d_r[0,:] - CY_d_r[1,:]) / (delta_r[0] - delta_r[1])      
        training.dCY_ddelta_f = (CY_d_f[0,:] - CY_d_f[1,:]) / (delta_f[0] - delta_f[1])      
        #training.dCY_ddelta_s = (CY_d_s[0,:] - CY_d_s[1,:]) / (delta_s[0] - delta_s[1])      
        training.dCY_du = (CY_u[0,:] - CY_u[1,:]) / (u[0] - u[1])                                             
        training.dCY_dv = (CY_v[0,:] - CY_v[1,:]) / (v[0] - v[1])                                           
        training.dCY_dw = (CY_w[0,:] - CY_w[1,:]) / (w[0] - w[1])                                          
        training.dCY_dp = (CY_roll_rate[0,:] - CY_roll_rate[1,:]) / (roll_rate[0]-roll_rate[1])                 
        training.dCY_dq = (CY_pitch_rate[0,:] - CY_pitch_rate[1,:]) / (pitch_rate[0]-pitch_rate[1])             
        training.dCY_dr = (CY_yaw_rate[0,:] - CY_yaw_rate[1,:]) / (yaw_rate[0]-yaw_rate[1])                     
        training.dCZ_dalpha = (CZ_alpha[0,:] - CZ_alpha[1,:]) / (AoA[0] - AoA[1])             
        training.dCZ_dbeta = (CZ_beta[0,:] - CZ_beta[1,:]) / (Beta[0] - Beta[1])              
        training.dCZ_ddelta_a = (CZ_d_a[0,:] - CZ_d_a[1,:]) / (delta_a[0] - delta_a[1])      
        training.dCZ_ddelta_e = (CZ_d_e[0,:] - CZ_d_e[1,:]) / (delta_e[0] - delta_e[1])      
        training.dCZ_ddelta_r = (CZ_d_r[0,:] - CZ_d_r[1,:]) / (delta_r[0] - delta_r[1])      
        training.dCZ_ddelta_f = (CZ_d_f[0,:] - CZ_d_f[1,:]) / (delta_f[0] - delta_f[1])      
        #training.dCZ_ddelta_s = (CZ_d_s[0,:] - CZ_d_s[1,:]) / (delta_s[0] - delta_s[1])      
        training.dCZ_du = (CZ_u[0,:] - CZ_u[1,:]) / (u[0] - u[1])                                              
        training.dCZ_dv = (CZ_v[0,:] - CZ_v[1,:]) / (v[0] - v[1])                                              
        training.dCZ_dw = (CZ_w[0,:] - CZ_w[1,:]) / (w[0] - w[1])                                              
        training.dCZ_dp = (CZ_roll_rate[0,:] - CZ_roll_rate[1,:]) / (roll_rate[0]-roll_rate[1])                
        training.dCZ_dq = (CZ_pitch_rate[0,:] - CZ_pitch_rate[1,:]) / (pitch_rate[0]-pitch_rate[1])            
        training.dCZ_dr = (CZ_yaw_rate[0,:] - CZ_yaw_rate[1,:]) / (yaw_rate[0]-yaw_rate[1])                    
        training.dCL_dalpha = (CL_alpha[0,:] - CL_alpha[1,:]) / (AoA[0] - AoA[1])         
        training.dCL_dbeta = (CL_beta[0,:] - CL_beta[1,:]) / (Beta[0] - Beta[1])          
        training.dCL_ddelta_a = (CL_d_a[0,:] - CL_d_a[1,:]) / (delta_a[0] - delta_a[1])      
        training.dCL_ddelta_e = (CL_d_e[0,:] - CL_d_e[1,:]) / (delta_e[0] - delta_e[1])      
        training.dCL_ddelta_r = (CL_d_r[0,:] - CL_d_r[1,:]) / (delta_r[0] - delta_r[1])      
        training.dCL_ddelta_f = (CL_d_f[0,:] - CL_d_f[1,:]) / (delta_f[0] - delta_f[1])      
        #training.dCL_ddelta_s = (CL_d_s[0,:] - CL_d_s[1,:]) / (delta_s[0] - delta_s[1])      
        training.dCL_du = (CL_u[0,:] - CL_u[1,:]) / (u[0] - u[1])                                              
        training.dCL_dv = (CL_v[0,:] - CL_v[1,:]) / (v[0] - v[1])                                              
        training.dCL_dw = (CL_w[0,:] - CL_w[1,:]) / (w[0] - w[1])                                              
        training.dCL_dp = (CL_roll_rate[0,:] - CL_roll_rate[1,:]) / (roll_rate[0]-roll_rate[1])                
        training.dCL_dq = (CL_pitch_rate[0,:] - CL_pitch_rate[1,:]) / (pitch_rate[0]-pitch_rate[1])            
        training.dCL_dr = (CL_yaw_rate[0,:] - CL_yaw_rate[1,:]) / (yaw_rate[0]-yaw_rate[1])                    
        training.dCM_dalpha = (CM_alpha[0,:] - CM_alpha[1,:]) / (AoA[0] - AoA[1])          
        training.dCM_dbeta = (CM_beta[0,:] - CM_beta[1,:]) / (Beta[0] - Beta[1])           
        training.dCM_ddelta_a = (CM_d_a[0,:] - CM_d_a[1,:]) / (delta_a[0] - delta_a[1])      
        training.dCM_ddelta_e = (CM_d_e[0,:] - CM_d_e[1,:]) / (delta_e[0] - delta_e[1])      
        training.dCM_ddelta_r = (CM_d_r[0,:] - CM_d_r[1,:]) / (delta_r[0] - delta_r[1])      
        training.dCM_ddelta_f = (CM_d_f[0,:] - CM_d_f[1,:]) / (delta_f[0] - delta_f[1])      
        #training.dCM_ddelta_s = (CM_d_s[0,:] - CM_d_s[1,:]) / (delta_s[0] - delta_s[1])      
        training.dCM_du = (CM_u[0,:] - CM_u[1,:]) / (u[0] - u[1])                                               
        training.dCM_dv = (CM_v[0,:] - CM_v[1,:]) / (v[0] - v[1])                                               
        training.dCM_dw = (CM_w[0,:] - CM_w[1,:]) / (w[0] - w[1])                                               
        training.dCM_dp = (CM_roll_rate[0,:] - CM_roll_rate[1,:]) / (roll_rate[0]-roll_rate[1])                 
        training.dCM_dq = (CM_pitch_rate[0,:] - CM_pitch_rate[1,:]) / (pitch_rate[0]-pitch_rate[1])             
        training.dCM_dr = (CM_yaw_rate[0,:] - CM_yaw_rate[1,:]) / (yaw_rate[0]-yaw_rate[1])                     
        training.dCN_dalpha = (CN_alpha[0,:] - CN_alpha[1,:]) / (AoA[0] - AoA[1])          
        training.dCN_dbeta = (CN_beta[0,:] - CN_beta[1,:]) / (Beta[0] - Beta[1])           
        training.dCN_ddelta_a = (CN_d_a[0,:] - CN_d_a[1,:]) / (delta_a[0] - delta_a[1])      
        training.dCN_ddelta_e = (CN_d_e[0,:] - CN_d_e[1,:]) / (delta_e[0] - delta_e[1])      
        training.dCN_ddelta_r = (CN_d_r[0,:] - CN_d_r[1,:]) / (delta_r[0] - delta_r[1])      
        training.dCN_ddelta_f = (CN_d_f[0,:] - CN_d_f[1,:]) / (delta_f[0] - delta_f[1])      
        #training.dCN_ddelta_s = (CN_d_s[0,:] - CN_d_s[1,:]) / (delta_s[0] - delta_s[1])      
        training.dCN_du = (CN_u[0,:] - CN_u[1,:]) / (u[0] - u[1])                                               
        training.dCN_dv = (CN_v[0,:] - CN_v[1,:]) / (v[0] - v[1])                                               
        training.dCN_dw = (CN_w[0,:] - CN_w[1,:]) / (w[0] - w[1])                                               
        training.dCN_dp = (CN_roll_rate[0,:] - CN_roll_rate[1,:]) / (roll_rate[0]-roll_rate[1])                 
        training.dCN_dq = (CN_pitch_rate[0,:] - CN_pitch_rate[1,:]) / (pitch_rate[0]-pitch_rate[1])             
        training.dCN_dr = (CN_yaw_rate[0,:] - CN_yaw_rate[1,:]) / (yaw_rate[0]-yaw_rate[1])                     
            
        training.NP            = 0  
        
        return
        
    def build_surrogate(self):
        """Build a surrogate using sample evaluation results.
        
        Assumptions:
            None
            
        Source:
            None
    
        Args:
            self       : VLM analysis          [unitless] 
            
        Returns: 
            None  
        """        
        # unpack data
        surrogates     = self.surrogates
        training       = self.training  
        AoA_data       = training.angle_of_attack 
        mach_data      = training.Mach        
        
        # Pack the outputs    
        
        surrogates.Clift_alpha    = RegularGridInterpolator((training.angle_of_attack,mach_data),training.Clift_alpha    ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Clift_beta     = RegularGridInterpolator((AoA_data,mach_data),training.Clift_beta     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Clift_delta_a  = RegularGridInterpolator((AoA_data,mach_data),training.Clift_delta_a  ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Clift_delta_e  = RegularGridInterpolator((AoA_data,mach_data),training.Clift_delta_e  ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Clift_delta_r  = RegularGridInterpolator((AoA_data,mach_data),training.Clift_delta_r  ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Clift_delta_f  = RegularGridInterpolator((AoA_data,mach_data),training.Clift_delta_f  ,method = 'linear',   bounds_error=False, fill_value=None)      
        #surrogates.Clift_delta_s  = RegularGridInterpolator((AoA_data,mach_data),training.Clift_delta_s  ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Clift_u        = RegularGridInterpolator((AoA_data,mach_data),training.Clift_u        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Clift_v        = RegularGridInterpolator((AoA_data,mach_data),training.Clift_v        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Clift_w        = RegularGridInterpolator((AoA_data,mach_data),training.Clift_w        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Clift_p        = RegularGridInterpolator((AoA_data,mach_data),training.Clift_p        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Clift_q        = RegularGridInterpolator((AoA_data,mach_data),training.Clift_q        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Clift_r        = RegularGridInterpolator((AoA_data,mach_data),training.Clift_r        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Cdrag_alpha    = RegularGridInterpolator((AoA_data,mach_data),training.Cdrag_alpha    ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Cdrag_beta     = RegularGridInterpolator((AoA_data,mach_data),training.Cdrag_beta     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Cdrag_delta_a  = RegularGridInterpolator((AoA_data,mach_data),training.Cdrag_delta_a  ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Cdrag_delta_e  = RegularGridInterpolator((AoA_data,mach_data),training.Cdrag_delta_e  ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Cdrag_delta_r  = RegularGridInterpolator((AoA_data,mach_data),training.Cdrag_delta_r  ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Cdrag_delta_f  = RegularGridInterpolator((AoA_data,mach_data),training.Cdrag_delta_f  ,method = 'linear',   bounds_error=False, fill_value=None)      
        #surrogates.Cdrag_delta_s  = RegularGridInterpolator((AoA_data,mach_data),training.Cdrag_delta_s  ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Cdrag_u        = RegularGridInterpolator((AoA_data,mach_data),training.Cdrag_u        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Cdrag_v        = RegularGridInterpolator((AoA_data,mach_data),training.Cdrag_v        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Cdrag_w        = RegularGridInterpolator((AoA_data,mach_data),training.Cdrag_w        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Cdrag_p        = RegularGridInterpolator((AoA_data,mach_data),training.Cdrag_p        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Cdrag_q        = RegularGridInterpolator((AoA_data,mach_data),training.Cdrag_q        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.Cdrag_r        = RegularGridInterpolator((AoA_data,mach_data),training.Cdrag_r        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CX_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.CX_alpha       ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CX_beta        = RegularGridInterpolator((AoA_data,mach_data),training.CX_beta        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CX_delta_a     = RegularGridInterpolator((AoA_data,mach_data),training.CX_delta_a     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CX_delta_e     = RegularGridInterpolator((AoA_data,mach_data),training.CX_delta_e     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CX_delta_r     = RegularGridInterpolator((AoA_data,mach_data),training.CX_delta_r     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CX_delta_f     = RegularGridInterpolator((AoA_data,mach_data),training.CX_delta_f     ,method = 'linear',   bounds_error=False, fill_value=None)      
        #surrogates.CX_delta_s     = RegularGridInterpolator((AoA_data,mach_data),training.CX_delta_s     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CX_u           = RegularGridInterpolator((AoA_data,mach_data),training.CX_u           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CX_v           = RegularGridInterpolator((AoA_data,mach_data),training.CX_v           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CX_w           = RegularGridInterpolator((AoA_data,mach_data),training.CX_w           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CX_p           = RegularGridInterpolator((AoA_data,mach_data),training.CX_p           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CX_q           = RegularGridInterpolator((AoA_data,mach_data),training.CX_q           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CX_r           = RegularGridInterpolator((AoA_data,mach_data),training.CX_r           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CY_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.CY_alpha       ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CY_beta        = RegularGridInterpolator((AoA_data,mach_data),training.CY_beta        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CY_delta_a     = RegularGridInterpolator((AoA_data,mach_data),training.CY_delta_a     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CY_delta_e     = RegularGridInterpolator((AoA_data,mach_data),training.CY_delta_e     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CY_delta_r     = RegularGridInterpolator((AoA_data,mach_data),training.CY_delta_r     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CY_delta_f     = RegularGridInterpolator((AoA_data,mach_data),training.CY_delta_f     ,method = 'linear',   bounds_error=False, fill_value=None)      
        #surrogates.CY_delta_s     = RegularGridInterpolator((AoA_data,mach_data),training.CY_delta_s     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CY_u           = RegularGridInterpolator((AoA_data,mach_data),training.CY_u           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CY_v           = RegularGridInterpolator((AoA_data,mach_data),training.CY_v           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CY_w           = RegularGridInterpolator((AoA_data,mach_data),training.CY_w           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CY_p           = RegularGridInterpolator((AoA_data,mach_data),training.CY_p           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CY_q           = RegularGridInterpolator((AoA_data,mach_data),training.CY_q           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CY_r           = RegularGridInterpolator((AoA_data,mach_data),training.CY_r           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CZ_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.CZ_alpha       ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CZ_beta        = RegularGridInterpolator((AoA_data,mach_data),training.CZ_beta        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CZ_delta_a     = RegularGridInterpolator((AoA_data,mach_data),training.CZ_delta_a     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CZ_delta_e     = RegularGridInterpolator((AoA_data,mach_data),training.CZ_delta_e     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CZ_delta_r     = RegularGridInterpolator((AoA_data,mach_data),training.CZ_delta_r     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CZ_delta_f     = RegularGridInterpolator((AoA_data,mach_data),training.CZ_delta_f     ,method = 'linear',   bounds_error=False, fill_value=None)      
        #surrogates.CZ_delta_s     = RegularGridInterpolator((AoA_data,mach_data),training.CZ_delta_s     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CZ_u           = RegularGridInterpolator((AoA_data,mach_data),training.CZ_u           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CZ_v           = RegularGridInterpolator((AoA_data,mach_data),training.CZ_v           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CZ_w           = RegularGridInterpolator((AoA_data,mach_data),training.CZ_w           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CZ_p           = RegularGridInterpolator((AoA_data,mach_data),training.CZ_p           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CZ_q           = RegularGridInterpolator((AoA_data,mach_data),training.CZ_q           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CZ_r           = RegularGridInterpolator((AoA_data,mach_data),training.CZ_r           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CL_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.CL_alpha       ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CL_beta        = RegularGridInterpolator((AoA_data,mach_data),training.CL_beta        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CL_delta_a     = RegularGridInterpolator((AoA_data,mach_data),training.CL_delta_a     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CL_delta_e     = RegularGridInterpolator((AoA_data,mach_data),training.CL_delta_e     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CL_delta_r     = RegularGridInterpolator((AoA_data,mach_data),training.CL_delta_r     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CL_delta_f     = RegularGridInterpolator((AoA_data,mach_data),training.CL_delta_f     ,method = 'linear',   bounds_error=False, fill_value=None)      
        #surrogates.CL_delta_s     = RegularGridInterpolator((AoA_data,mach_data),training.CL_delta_s     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CL_u           = RegularGridInterpolator((AoA_data,mach_data),training.CL_u           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CL_v           = RegularGridInterpolator((AoA_data,mach_data),training.CL_v           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CL_w           = RegularGridInterpolator((AoA_data,mach_data),training.CL_w           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CL_p           = RegularGridInterpolator((AoA_data,mach_data),training.CL_p           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CL_q           = RegularGridInterpolator((AoA_data,mach_data),training.CL_q           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CL_r           = RegularGridInterpolator((AoA_data,mach_data),training.CL_r           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CM_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.CM_alpha       ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CM_beta        = RegularGridInterpolator((AoA_data,mach_data),training.CM_beta        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CM_delta_a     = RegularGridInterpolator((AoA_data,mach_data),training.CM_delta_a     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CM_delta_e     = RegularGridInterpolator((AoA_data,mach_data),training.CM_delta_e     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CM_delta_r     = RegularGridInterpolator((AoA_data,mach_data),training.CM_delta_r     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CM_delta_f     = RegularGridInterpolator((AoA_data,mach_data),training.CM_delta_f     ,method = 'linear',   bounds_error=False, fill_value=None)      
        #surrogates.CM_delta_s     = RegularGridInterpolator((AoA_data,mach_data),training.CM_delta_s     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CM_u           = RegularGridInterpolator((AoA_data,mach_data),training.CM_u           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CM_v           = RegularGridInterpolator((AoA_data,mach_data),training.CM_v           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CM_w           = RegularGridInterpolator((AoA_data,mach_data),training.CM_w           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CM_p           = RegularGridInterpolator((AoA_data,mach_data),training.CM_p           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CM_q           = RegularGridInterpolator((AoA_data,mach_data),training.CM_q           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CM_r           = RegularGridInterpolator((AoA_data,mach_data),training.CM_r           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CN_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.CN_alpha       ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CN_beta        = RegularGridInterpolator((AoA_data,mach_data),training.CN_beta        ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CN_delta_a     = RegularGridInterpolator((AoA_data,mach_data),training.CN_delta_a     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CN_delta_e     = RegularGridInterpolator((AoA_data,mach_data),training.CN_delta_e     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CN_delta_r     = RegularGridInterpolator((AoA_data,mach_data),training.CN_delta_r     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CN_delta_f     = RegularGridInterpolator((AoA_data,mach_data),training.CN_delta_f     ,method = 'linear',   bounds_error=False, fill_value=None)      
        #surrogates.CN_delta_s     = RegularGridInterpolator((AoA_data,mach_data),training.CN_delta_s     ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CN_u           = RegularGridInterpolator((AoA_data,mach_data),training.CN_u           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CN_v           = RegularGridInterpolator((AoA_data,mach_data),training.CN_v           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CN_w           = RegularGridInterpolator((AoA_data,mach_data),training.CN_w           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CN_p           = RegularGridInterpolator((AoA_data,mach_data),training.CN_p           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CN_q           = RegularGridInterpolator((AoA_data,mach_data),training.CN_q           ,method = 'linear',   bounds_error=False, fill_value=None)      
        surrogates.CN_r           = RegularGridInterpolator((AoA_data,mach_data),training.CN_r           ,method = 'linear',   bounds_error=False, fill_value=None)
        
        surrogates.dClift_dalpha    = interpolate.interp1d(training.dClift_dalpha    , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dClift_dbeta     = interpolate.interp1d(training.dClift_dbeta     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dClift_ddelta_a  = interpolate.interp1d(training.dClift_ddelta_a  , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dClift_ddelta_e  = interpolate.interp1d(training.dClift_ddelta_e  , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dClift_ddelta_r  = interpolate.interp1d(training.dClift_ddelta_r  , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dClift_ddelta_f  = interpolate.interp1d(training.dClift_ddelta_f  , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        #surrogates.dClift_ddelta_s  = interpolate.interp1d(training.dClift_ddelta_s  , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dClift_du        = interpolate.interp1d(training.dClift_du        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dClift_dv        = interpolate.interp1d(training.dClift_dv        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dClift_dw        = interpolate.interp1d(training.dClift_dw        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dClift_dp        = interpolate.interp1d(training.dClift_dp        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dClift_dq        = interpolate.interp1d(training.dClift_dq        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dClift_dr        = interpolate.interp1d(training.dClift_dr        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCdrag_dalpha    = interpolate.interp1d(training.dCdrag_dalpha    , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCdrag_dbeta     = interpolate.interp1d(training.dCdrag_dbeta     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCdrag_ddelta_a  = interpolate.interp1d(training.dCdrag_ddelta_a  , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCdrag_ddelta_e  = interpolate.interp1d(training.dCdrag_ddelta_e  , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCdrag_ddelta_r  = interpolate.interp1d(training.dCdrag_ddelta_r  , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCdrag_ddelta_f  = interpolate.interp1d(training.dCdrag_ddelta_f  , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        #surrogates.dCdrag_ddelta_s  = interpolate.interp1d(training.dCdrag_ddelta_s  , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCdrag_du        = interpolate.interp1d(training.dCdrag_du        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCdrag_dv        = interpolate.interp1d(training.dCdrag_dv        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCdrag_dw        = interpolate.interp1d(training.dCdrag_dw        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCdrag_dp        = interpolate.interp1d(training.dCdrag_dp        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCdrag_dq        = interpolate.interp1d(training.dCdrag_dq        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCdrag_dr        = interpolate.interp1d(training.dCdrag_dr        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCX_dalpha       = interpolate.interp1d(training.dCX_dalpha       , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCX_dbeta        = interpolate.interp1d(training.dCX_dbeta        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCX_ddelta_a     = interpolate.interp1d(training.dCX_ddelta_a     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCX_ddelta_e     = interpolate.interp1d(training.dCX_ddelta_e     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCX_ddelta_r     = interpolate.interp1d(training.dCX_ddelta_r     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCX_ddelta_f     = interpolate.interp1d(training.dCX_ddelta_f     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        #surrogates.dCX_ddelta_s     = interpolate.interp1d(training.dCX_ddelta_s     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCX_du           = interpolate.interp1d(training.dCX_du           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCX_dv           = interpolate.interp1d(training.dCX_dv           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCX_dw           = interpolate.interp1d(training.dCX_dw           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCX_dp           = interpolate.interp1d(training.dCX_dp           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCX_dq           = interpolate.interp1d(training.dCX_dq           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCX_dr           = interpolate.interp1d(training.dCX_dr           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCY_dalpha       = interpolate.interp1d(training.dCY_dalpha       , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCY_dbeta        = interpolate.interp1d(training.dCY_dbeta        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCY_ddelta_a     = interpolate.interp1d(training.dCY_ddelta_a     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCY_ddelta_e     = interpolate.interp1d(training.dCY_ddelta_e     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCY_ddelta_r     = interpolate.interp1d(training.dCY_ddelta_r     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCY_ddelta_f     = interpolate.interp1d(training.dCY_ddelta_f     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        #surrogates.dCY_ddelta_s     = interpolate.interp1d(training.dCY_ddelta_s     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCY_du           = interpolate.interp1d(training.dCY_du           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCY_dv           = interpolate.interp1d(training.dCY_dv           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCY_dw           = interpolate.interp1d(training.dCY_dw           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCY_dp           = interpolate.interp1d(training.dCY_dp           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCY_dq           = interpolate.interp1d(training.dCY_dq           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCY_dr           = interpolate.interp1d(training.dCY_dr           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCZ_dalpha       = interpolate.interp1d(training.dCZ_dalpha       , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCZ_dbeta        = interpolate.interp1d(training.dCZ_dbeta        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCZ_ddelta_a     = interpolate.interp1d(training.dCZ_ddelta_a     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCZ_ddelta_e     = interpolate.interp1d(training.dCZ_ddelta_e     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCZ_ddelta_r     = interpolate.interp1d(training.dCZ_ddelta_r     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCZ_ddelta_f     = interpolate.interp1d(training.dCZ_ddelta_f     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        #surrogates.dCZ_ddelta_s     = interpolate.interp1d(training.dCZ_ddelta_s     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCZ_du           = interpolate.interp1d(training.dCZ_du           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCZ_dv           = interpolate.interp1d(training.dCZ_dv           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCZ_dw           = interpolate.interp1d(training.dCZ_dw           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCZ_dp           = interpolate.interp1d(training.dCZ_dp           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCZ_dq           = interpolate.interp1d(training.dCZ_dq           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCZ_dr           = interpolate.interp1d(training.dCZ_dr           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCL_dalpha       = interpolate.interp1d(training.dCL_dalpha       , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCL_dbeta        = interpolate.interp1d(training.dCL_dbeta        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCL_ddelta_a     = interpolate.interp1d(training.dCL_ddelta_a     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCL_ddelta_e     = interpolate.interp1d(training.dCL_ddelta_e     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCL_ddelta_r     = interpolate.interp1d(training.dCL_ddelta_r     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCL_ddelta_f     = interpolate.interp1d(training.dCL_ddelta_f     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        #surrogates.dCL_ddelta_s     = interpolate.interp1d(training.dCL_ddelta_s     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCL_du           = interpolate.interp1d(training.dCL_du           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCL_dv           = interpolate.interp1d(training.dCL_dv           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCL_dw           = interpolate.interp1d(training.dCL_dw           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCL_dp           = interpolate.interp1d(training.dCL_dp           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCL_dq           = interpolate.interp1d(training.dCL_dq           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCL_dr           = interpolate.interp1d(training.dCL_dr           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCM_dalpha       = interpolate.interp1d(training.dCM_dalpha       , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCM_dbeta        = interpolate.interp1d(training.dCM_dbeta        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCM_ddelta_a     = interpolate.interp1d(training.dCM_ddelta_a     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCM_ddelta_e     = interpolate.interp1d(training.dCM_ddelta_e     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCM_ddelta_r     = interpolate.interp1d(training.dCM_ddelta_r     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCM_ddelta_f     = interpolate.interp1d(training.dCM_ddelta_f     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        #surrogates.dCM_ddelta_s     = interpolate.interp1d(training.dCM_ddelta_s     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCM_du           = interpolate.interp1d(training.dCM_du           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCM_dv           = interpolate.interp1d(training.dCM_dv           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCM_dw           = interpolate.interp1d(training.dCM_dw           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCM_dp           = interpolate.interp1d(training.dCM_dp           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCM_dq           = interpolate.interp1d(training.dCM_dq           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCM_dr           = interpolate.interp1d(training.dCM_dr           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCN_dalpha       = interpolate.interp1d(training.dCN_dalpha       , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCN_dbeta        = interpolate.interp1d(training.dCN_dbeta        , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCN_ddelta_a     = interpolate.interp1d(training.dCN_ddelta_a     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCN_ddelta_e     = interpolate.interp1d(training.dCN_ddelta_e     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCN_ddelta_r     = interpolate.interp1d(training.dCN_ddelta_r     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCN_ddelta_f     = interpolate.interp1d(training.dCN_ddelta_f     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        #surrogates.dCN_ddelta_s     = interpolate.interp1d(training.dCN_ddelta_s     , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCN_du           = interpolate.interp1d(training.dCN_du           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCN_dv           = interpolate.interp1d(training.dCN_dv           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCN_dw           = interpolate.interp1d(training.dCN_dw           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCN_dp           = interpolate.interp1d(training.dCN_dp           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCN_dq           = interpolate.interp1d(training.dCN_dq           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)      
        surrogates.dCN_dr           = interpolate.interp1d(training.dCN_dr           , mach_data,kind = 'linear',   bounds_error=False, fill_value=nan)
        
        return

# ----------------------------------------------------------------------
#  Helper Functions
# ----------------------------------------------------------------------
def evaluate_VLM(conditions,settings,geometry):
    """Calculate stability coefficients inluding specific wing coefficients using the VLM
        
    Assumptions:
        None
        
    Source:
        None

    Args: 
        conditions : flight conditions     [unitless]
        settings   : VLM analysis settings [unitless]
        geometry   : vehicle configuration [unitless] 
        
    Returns: 
        None  
    """    
    results = VLM(conditions,settings,geometry)
    Clift   = results.CL       
    Cdrag   = results.CDi      
    CX      = results.CX       
    CY      = results.CY       
    CZ      = results.CZ       
    CL      = results.CL_mom   
    CM      = results.CM       
    CN      = results.CN

    return Clift,Cdrag,CX,CY,CZ,CL,CM,CN

