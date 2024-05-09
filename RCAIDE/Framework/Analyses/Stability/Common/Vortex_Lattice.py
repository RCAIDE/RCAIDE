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
        self.training.angle_of_attack                 = np.array([-10, -7.5, -5, -2.5, 0, 2.5, 5, 7.5, 10]) * Units.deg 
        self.training.sideslip_angle                  = np.array([0, 5]) * Units.deg
        self.training.aileron_deflection              = np.array([0, 1]) * Units.deg 
        self.training.elevator_deflection             = np.array([0, 1]) * Units.deg    
        self.training.rudder_deflection               = np.array([0, 1]) * Units.deg  
        self.training.flap_deflection                 = np.array([-5, 0])* Units.deg      
        self.training.slat_deflection                 = np.array([0, 1]) * Units.deg       
        self.training.u                               = np.array([0, 1]) * Units.knots
        self.training.v                               = np.array([0, 1]) * Units.knots
        self.training.w                               = np.array([0, 1]) * Units.knots  
        self.training.pitch_rate                      = np.array([0, 0.01])  * Units.rad / Units.sec
        self.training.roll_rate                       = np.array([0, 0.3])  * Units.rad / Units.sec
        self.training.yaw_rate                        = np.array([0, 0.01])  * Units.rad / Units.sec        

        # force coefficients 
        self.training.Clift                           = None
        self.training.Cdrag                           = None
        self.training.CX                              = None
        self.training.CY                              = None 
        self.training.CZ                              = None  
                                                      
        # moment coefficients                         
        self.training.CL                              = None 
        self.training.CM                              = None 
        self.training.CN                              = None
                                                      
        self.training.static_margin                   = None
        self.training.pitch_rate                      = None
        self.training.roll_rate                       = None 
        self.training.yaw_rate                        = None 
        
        # force derivatives
        self.training.Clift_alpha                     = None
        self.training.Clift_beta                      = None
        self.training.Clift_delta_a                   = None
        self.training.Clift_delta_e                   = None
        self.training.Clift_delta_r                   = None
        self.training.Clift_delta_f                   = None
        self.training.Clift_delta_s                   = None
        self.training.Clift_u                         = None
        self.training.Clift_v                         = None
        self.training.Clift_w                         = None
        self.training.Clift_p                         = None
        self.training.Clift_q                         = None
        self.training.Clift_r                         = None
        self.training.Cdrag_alpha                     = None
        self.training.Cdrag_beta                      = None
        self.training.Cdrag_delta_a                   = None
        self.training.Cdrag_delta_e                   = None
        self.training.Cdrag_delta_r                   = None
        self.training.Cdrag_delta_f                   = None
        self.training.Cdrag_delta_s                   = None
        self.training.Cdrag_u                         = None
        self.training.Cdrag_v                         = None
        self.training.Cdrag_w                         = None
        self.training.Cdrag_p                         = None
        self.training.Cdrag_q                         = None
        self.training.Cdrag_r                         = None
        self.training.CX_alpha                        = None
        self.training.CX_beta                         = None
        self.training.CX_delta_a                      = None
        self.training.CX_delta_e                      = None
        self.training.CX_delta_r                      = None
        self.training.CX_delta_f                      = None
        self.training.CX_delta_s                      = None
        self.training.CX_u                            = None
        self.training.CX_v                            = None
        self.training.CX_w                            = None
        self.training.CX_p                            = None
        self.training.CX_q                            = None
        self.training.CX_r                            = None
        self.training.CY_alpha                        = None
        self.training.CY_beta                         = None
        self.training.CY_delta_a                      = None
        self.training.CY_delta_e                      = None
        self.training.CY_delta_r                      = None
        self.training.CY_delta_f                      = None
        self.training.CY_delta_s                      = None
        self.training.CY_u                            = None
        self.training.CY_v                            = None
        self.training.CY_w                            = None
        self.training.CY_p                            = None
        self.training.CY_q                            = None
        self.training.CY_r                            = None
        self.training.CZ_alpha                        = None
        self.training.CZ_beta                         = None
        self.training.CZ_delta_a                      = None
        self.training.CZ_delta_e                      = None
        self.training.CZ_delta_r                      = None
        self.training.CZ_delta_f                      = None
        self.training.CZ_delta_s                      = None
        self.training.CZ_u                            = None
        self.training.CZ_v                            = None
        self.training.CZ_w                            = None
        self.training.CZ_p                            = None
        self.training.CZ_q                            = None
        self.training.CZ_r                            = None
           
        # moment derivatives
        self.training.CL_alpha                        = None
        self.training.CL_beta                         = None
        self.training.CL_delta_a                      = None
        self.training.CL_delta_e                      = None
        self.training.CL_delta_r                      = None
        self.training.CL_delta_f                      = None
        self.training.CL_delta_s                      = None
        self.training.CL_u                            = None
        self.training.CL_v                            = None
        self.training.CL_w                            = None
        self.training.CL_p                            = None
        self.training.CL_q                            = None
        self.training.CL_r                            = None
        self.training.CM_alpha                        = None
        self.training.CM_beta                         = None
        self.training.CM_delta_a                      = None
        self.training.CM_delta_e                      = None
        self.training.CM_delta_r                      = None
        self.training.CM_delta_f                      = None
        self.training.CM_delta_s                      = None
        self.training.CM_u                            = None
        self.training.CM_v                            = None
        self.training.CM_w                            = None
        self.training.CM_p                            = None
        self.training.CM_q                            = None
        self.training.CM_r                            = None
        self.training.CN_alpha                        = None
        self.training.CN_beta                         = None
        self.training.CN_delta_a                      = None
        self.training.CN_delta_e                      = None
        self.training.CN_delta_r                      = None
        self.training.CN_delta_f                      = None
        self.training.CN_delta_s                      = None
        self.training.CN_u                            = None
        self.training.CN_v                            = None
        self.training.CN_w                            = None
        self.training.CN_p                            = None
        self.training.CN_q                            = None
        self.training.CN_r                            = None
        
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
        self.surrogates.pitch_rate                    = None
        self.surrogates.roll_rate                     = None  
        self.surrogates.yaw_rate                      = None
        
        self.surrogates.Clift_alpha                   = None    
        self.surrogates.Clift_beta                    = None    
        self.surrogates.Clift_delta_a                 = None    
        self.surrogates.Clift_delta_e                 = None    
        self.surrogates.Clift_delta_r                 = None    
        self.surrogates.Clift_delta_f                 = None    
        self.surrogates.Clift_delta_s                 = None    
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
        self.surrogates.Cdrag_delta_s                 = None    
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
        self.surrogates.CX_delta_s                    = None    
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
        self.surrogates.CY_delta_s                    = None    
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
        self.surrogates.CZ_delta_s                    = None    
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
        self.surrogates.CL_delta_s                    = None     
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
        self.surrogates.CM_delta_s                    = None     
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
        self.surrogates.CN_delta_s                    = None     
        self.surrogates.CN_u                          = None     
        self.surrogates.CN_v                          = None     
        self.surrogates.CN_w                          = None     
        self.surrogates.CN_p                          = None     
        self.surrogates.CN_q                          = None     
        self.surrogates.CN_r                          = None
        
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
        delta_s     = np.atleast_2d(conditions.control_surfaces.slat.deflection)
        pitch_rate  = np.atleast_2d(conditions.static_stability.pitch_rate)
        roll_rate  = np.atleast_2d(conditions.static_stability.roll_rate)
        yaw_rate = np.atleast_2d(conditions.static_stability.yaw_rate)  
  
         
        # Query surrogates 
        pts            = np.hstack((AoA,Mach))
        Clift          = np.atleast_2d(surrogates.Clift(pts)).T         
        Cdrag          = np.atleast_2d(surrogates.Cdrag (pts)).T   
        CX_0           = np.atleast_2d(surrogates.CX_0(pts)).T
        CY_0           = np.atleast_2d(surrogates.CY_0(pts)).T
        CZ_0           = np.atleast_2d(surrogates.CZ_0(pts)).T
        CL_0           = np.atleast_2d(surrogates.CL_0(pts)).T
        CM_0           = np.atleast_2d(surrogates.CM_0(pts)).T         
        CN_0           = np.atleast_2d(surrogates.CN_0(pts)).T 
        CY_beta        = np.atleast_2d(surrogates.CY_beta(pts)).T
        CL_beta        = np.atleast_2d(surrogates.CL_beta(pts)).T 
        CN_beta        = np.atleast_2d(surrogates.CN_beta(pts)).T 
        CM_delta_e     = np.atleast_2d(surrogates.CM_delta_e(pts)).T
        Clift_delta_e  = np.atleast_2d(surrogates.Clift_delta_e(pts)).T 
        CY_ddelta_a    = np.atleast_2d(surrogates.CY_ddelta_a(pts)).T
        CL_delta_a     = np.atleast_2d(surrogates.CL_delta_a(pts)).T
        CN_delta_a     = np.atleast_2d(surrogates.CN_delta_a(pts)).T
        CY_ddelta_r    = np.atleast_2d(surrogates.CY_ddelta_r(pts)).T
        Cl_ddelta_r    = np.atleast_2d(surrogates.Cl_ddelta_r(pts)).T
        CN_delta_r     = np.atleast_2d(surrogates.CN_delta_r(pts)).T
        
        # Stability Results  
        #conditions.S_ref                                                  = # Need to Update 
        #conditions.c_ref                                                  = # Need to Update
        #conditions.b_ref                                                  = # Need to Update
        #conditions.X_ref                                                  = # Need to Update
        #conditions.Y_ref                                                  = # Need to Update
        #conditions.Z_ref                                                  = # Need to Update 
        #conditions.aerodynamics.oswald_efficiency                         = # Need to Update
        conditions.static_stability.coefficients.lift                     = Clift + Clift_delta_e*delta_e 
        conditions.static_stability.coefficients.drag                     = Cdrag     
        conditions.static_stability.coefficients.X                        = CX_0 
        conditions.static_stability.coefficients.Y                        = CY_0 + CY_beta * Beta + CY_ddelta_a * delta_a + CY_ddelta_r * delta_r
        conditions.static_stability.coefficients.Z                        = CZ_0
        conditions.static_stability.coefficients.L                        = CL_0 + CL_beta * Beta + CL_delta_a * delta_a + Cl_ddelta_r * delta_r #+ CL_p *( pitch_rate / conditions.freestream.velocity) # rates are normalized 
        conditions.static_stability.coefficients.M                        = CM_0 + CM_delta_e*delta_e
        conditions.static_stability.coefficients.N                        = CN_0 + CN_beta * Beta + CN_delta_a * delta_a + CN_delta_r * delta_r 
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
        geometry   = self.geometry
        settings   = self.settings
        training   = self.training
        AoA        = training.angle_of_attack 
        Mach       = training.Mach                             
        delta_e    = training.elevator_deflection  
        Beta       = training.sideslip_angle         
        delta_a    = training.aileron_deflection                
        delta_r    = training.rudder_deflection     
        pitch_rate = training.pitch_rate
        roll_rate  = training.roll_rate
        yaw_rate   = training.yaw_rate
        u          = training.u
        v          = training.v
        w          = training.w

        
        len_AoA        = len(AoA)   
        len_Mach       = len(Mach) 
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
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Elevator: 
                    len_d_e        = len(delta_e)   
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Rudder:  
                    len_d_r        = len(delta_r)   
                if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Aileron: 
                    len_d_a        = len(delta_a)  
        

        # Setup new array shapes for vectorization 
        # stakcing 3x3x3 matrices into one horizontal line(27)  
        AoAs       = np.atleast_2d(np.tile(AoA,len_Mach).T.flatten()).T 
        Machs      = np.atleast_2d(np.repeat(Mach,len_AoA)).T
     
        # --------------------------------------------------------------------------------------------------------------
        # Beta 
        # --------------------------------------------------------------------------------------------------------------        
        Clift_beta     = np.zeros((len_AoA,len_Mach,len_Beta)) 
        Cdrag_beta     = np.zeros((len_AoA,len_Mach,len_Beta)) 
        CX_beta        = np.zeros((len_AoA,len_Mach,len_Beta)) 
        CY_beta        = np.zeros((len_AoA,len_Mach,len_Beta)) 
        CZ_beta        = np.zeros((len_AoA,len_Mach,len_Beta)) 
        CL_beta        = np.zeros((len_AoA,len_Mach,len_Beta)) 
        CM_beta        = np.zeros((len_AoA,len_Mach,len_Beta)) 
        CN_beta        = np.zeros((len_AoA,len_Mach,len_Beta))

        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.aerodynamics.angles.alpha            = AoAs
        conditions.freestream.mach_number               = Machs 
        conditions.static_stability.pitch_rate         = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate          = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate           = np.zeros_like(Machs)  
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.freestream.velocity                  = np.zeros_like(Machs) 
        
        for beta_i in range(len_Beta):               
            conditions.aerodynamics.angles.beta         =  np.ones_like(Machs)*Beta[beta_i]
            Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)     
            Clift_beta[:,:,beta_i] = np.reshape(Clift_res,(len_Mach,len_AoA)).T 
            Cdrag_beta[:,:,beta_i] = np.reshape(Cdrag_res,(len_Mach,len_AoA)).T                                 
            CX_beta[:,:,beta_i]    = np.reshape(CX_res,(len_Mach,len_AoA)).T 
            CY_beta[:,:,beta_i]    = np.reshape(CY_res,(len_Mach,len_AoA)).T 
            CZ_beta[:,:,beta_i]    = np.reshape(CZ_res,(len_Mach,len_AoA)).T 
            CL_beta[:,:,beta_i]    = np.reshape(CL_res,(len_Mach,len_AoA)).T 
            CM_beta[:,:,beta_i]    = np.reshape(CM_res,(len_Mach,len_AoA)).T 
            CN_beta[:,:,beta_i]    = np.reshape(CN_res,(len_Mach,len_AoA)).T 
                     

        # --------------------------------------------------------------------------------------------------------------
        # Zero Lift 
        # --------------------------------------------------------------------------------------------------------------
        Clift          = np.zeros((len_AoA,len_Mach)) 
        Cdrag          = np.zeros((len_AoA,len_Mach)) 
        CX_0           = np.zeros((len_AoA,len_Mach)) 
        CY_0           = np.zeros((len_AoA,len_Mach)) 
        CZ_0           = np.zeros((len_AoA,len_Mach)) 
        CL_0           = np.zeros((len_AoA,len_Mach)) 
        CM_0           = np.zeros((len_AoA,len_Mach)) 
        CN_0           = np.zeros((len_AoA,len_Mach)) 
        
        # reset conditions 
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.aerodynamics.angles.alpha            = AoAs 
        conditions.freestream.mach_number               = Machs 
        conditions.static_stability.pitch_rate         = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate          = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate           = np.zeros_like(Machs)  
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.freestream.velocity                  = np.zeros_like(Machs)  
        
        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry) 
        Clift[:,:]   = np.reshape(Clift_res,(len_Mach,len_AoA)).T 
        Cdrag[:,:]   = np.reshape(Cdrag_res,(len_Mach,len_AoA)).T 
        CX_0[:,:]    = np.reshape(CX_res,(len_Mach,len_AoA)).T 
        CY_0[:,:]    = np.reshape(CY_res,(len_Mach,len_AoA)).T 
        CZ_0[:,:]    = np.reshape(CZ_res,(len_Mach,len_AoA)).T 
        CL_0[:,:]    = np.reshape(CL_res,(len_Mach,len_AoA)).T 
        CM_0[:,:]    = np.reshape(CM_res,(len_Mach,len_AoA)).T 
        CN_0[:,:]    = np.reshape(CN_res,(len_Mach,len_AoA)).T   

        # --------------------------------------------------------------------------------------------------------------
        # Elevator 
        # --------------------------------------------------------------------------------------------------------------
        Clift_d_e      = np.zeros((len_AoA,len_Mach,len_d_e)) 
        Cdrag_d_e      = np.zeros((len_AoA,len_Mach,len_d_e)) 
        CX_d_e         = np.zeros((len_AoA,len_Mach,len_d_e)) 
        CY_d_e         = np.zeros((len_AoA,len_Mach,len_d_e)) 
        CZ_d_e         = np.zeros((len_AoA,len_Mach,len_d_e)) 
        CL_d_e         = np.zeros((len_AoA,len_Mach,len_d_e)) 
        CM_d_e         = np.zeros((len_AoA,len_Mach,len_d_e)) 
        CN_d_e         = np.zeros((len_AoA,len_Mach,len_d_e))

        # reset conditions 
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.aerodynamics.angles.alpha            = AoAs 
        conditions.freestream.mach_number               = Machs 
        conditions.static_stability.pitch_rate         = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate          = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate           = np.zeros_like(Machs)  
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.freestream.velocity                  = np.zeros_like(Machs) 
        
        for e_i in range(len_d_e): 
            for wing in geometry.wings: 
                # Elevator 
                for control_surface in wing.control_surfaces:
                    if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Elevator: 
                        control_surface.deflection                                    = delta_e[e_i]
                        conditions.control_surfaces.elevator.deflection[:,0]          = delta_e[e_i]                
                        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)     
                        Clift_d_e[:,:,e_i] = np.reshape(Clift_res,(len_Mach,len_AoA)).T 
                        Cdrag_d_e[:,:,e_i] = np.reshape(Cdrag_res,(len_Mach,len_AoA)).T                                 
                        CX_d_e[:,:,e_i]    = np.reshape(CX_res,(len_Mach,len_AoA)).T 
                        CY_d_e[:,:,e_i]    = np.reshape(CY_res,(len_Mach,len_AoA)).T 
                        CZ_d_e[:,:,e_i]    = np.reshape(CZ_res,(len_Mach,len_AoA)).T 
                        CL_d_e[:,:,e_i]    = np.reshape(CL_res,(len_Mach,len_AoA)).T 
                        CM_d_e[:,:,e_i]    = np.reshape(CM_res,(len_Mach,len_AoA)).T 
                        CN_d_e[:,:,e_i]    = np.reshape(CN_res,(len_Mach,len_AoA)).T       
                        
                
        # --------------------------------------------------------------------------------------------------------------
        # Aileron 
        # --------------------------------------------------------------------------------------------------------------    
        Clift_d_a      = np.zeros((len_AoA,len_Mach,len_d_a)) 
        Cdrag_d_a      = np.zeros((len_AoA,len_Mach,len_d_a)) 
        CX_d_a         = np.zeros((len_AoA,len_Mach,len_d_a)) 
        CY_d_a         = np.zeros((len_AoA,len_Mach,len_d_a)) 
        CZ_d_a         = np.zeros((len_AoA,len_Mach,len_d_a)) 
        CL_d_a         = np.zeros((len_AoA,len_Mach,len_d_a)) 
        CM_d_a         = np.zeros((len_AoA,len_Mach,len_d_a)) 
        CN_d_a         = np.zeros((len_AoA,len_Mach,len_d_a))   

        # reset conditions         
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.aerodynamics.angles.alpha            = AoAs 
        conditions.freestream.mach_number               = Machs 
        conditions.static_stability.pitch_rate         = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate          = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate           = np.zeros_like(Machs)  
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.freestream.velocity                  = np.zeros_like(Machs) 
        
        for a_i in range(len_d_a): 
            for wing in geometry.wings: 
                # Elevator 
                for control_surface in wing.control_surfaces:
                    if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Aileron:
                        
                        control_surface.deflection                                    = delta_a[a_i]
                        conditions.control_surfaces.aileron.deflection[:,0]           = delta_a[a_i]                
                        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)  
                        Clift_d_a[:,:,a_i] = np.reshape(Clift_res,(len_Mach,len_AoA)).T 
                        Cdrag_d_a[:,:,a_i] = np.reshape(Cdrag_res,(len_Mach,len_AoA)).T                                 
                        CX_d_a[:,:,a_i]    = np.reshape(CX_res,(len_Mach,len_AoA)).T 
                        CY_d_a[:,:,a_i]    = np.reshape(CY_res,(len_Mach,len_AoA)).T 
                        CZ_d_a[:,:,a_i]    = np.reshape(CZ_res,(len_Mach,len_AoA)).T 
                        CL_d_a[:,:,a_i]    = np.reshape(CL_res,(len_Mach,len_AoA)).T 
                        CM_d_a[:,:,a_i]    = np.reshape(CM_res,(len_Mach,len_AoA)).T 
                        CN_d_a[:,:,a_i]    = np.reshape(CN_res,(len_Mach,len_AoA)).T 
        
        
                
        # --------------------------------------------------------------------------------------------------------------
        # Rudder 
        # --------------------------------------------------------------------------------------------------------------         
        Clift_d_r      = np.zeros((len_AoA,len_Mach,len_d_r)) 
        Cdrag_d_r      = np.zeros((len_AoA,len_Mach,len_d_r)) 
        CX_d_r         = np.zeros((len_AoA,len_Mach,len_d_r)) 
        CY_d_r         = np.zeros((len_AoA,len_Mach,len_d_r)) 
        CZ_d_r         = np.zeros((len_AoA,len_Mach,len_d_r)) 
        CL_d_r         = np.zeros((len_AoA,len_Mach,len_d_r)) 
        CM_d_r         = np.zeros((len_AoA,len_Mach,len_d_r)) 
        CN_d_r         = np.zeros((len_AoA,len_Mach,len_d_r))  

        # reset conditions         
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.aerodynamics.angles.alpha            = AoAs 
        conditions.freestream.mach_number               = Machs 
        conditions.static_stability.pitch_rate         = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate          = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate           = np.zeros_like(Machs)  
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.freestream.velocity                  = np.zeros_like(Machs) 
        for r_i in range(len_d_r): 
            for wing in geometry.wings: 
                # Elevator 
                for control_surface in wing.control_surfaces:
                    if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Rudder:
                        
                        control_surface.deflection                                    = delta_r[r_i]
                        conditions.control_surfaces.rudder.deflection[:,0]            = delta_r[r_i]                
                        Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)      

                        Clift_d_r[:,:,r_i] = np.reshape(Clift_res,(len_Mach,len_AoA)).T 
                        Cdrag_d_r[:,:,r_i] = np.reshape(Cdrag_res,(len_Mach,len_AoA)).T                                 
                        CX_d_r[:,:,r_i]    = np.reshape(CX_res,(len_Mach,len_AoA)).T 
                        CY_d_r[:,:,r_i]    = np.reshape(CY_res,(len_Mach,len_AoA)).T 
                        CZ_d_r[:,:,r_i]    = np.reshape(CZ_res,(len_Mach,len_AoA)).T 
                        CL_d_r[:,:,r_i]    = np.reshape(CL_res,(len_Mach,len_AoA)).T 
                        CM_d_r[:,:,r_i]    = np.reshape(CM_res,(len_Mach,len_AoA)).T 
                        CN_d_r[:,:,r_i]    = np.reshape(CN_res,(len_Mach,len_AoA)).T         
                
                
                
        # -------------------------------------------------------               
        # Velocity u 
        # -------------------------------------------------------
        '''
        for u velocity, change mach number by 0.1
        
        for v velocity, beta
        
        for w velocity, alpha  
        
        '''
        Clift_u     = np.zeros((len_AoA,len_Mach,len_u)) 
        Cdrag_u     = np.zeros((len_AoA,len_Mach,len_u)) 
        CX_u        = np.zeros((len_AoA,len_Mach,len_u)) 
        CY_u        = np.zeros((len_AoA,len_Mach,len_u)) 
        CZ_u        = np.zeros((len_AoA,len_Mach,len_u)) 
        CL_u        = np.zeros((len_AoA,len_Mach,len_u)) 
        CM_u        = np.zeros((len_AoA,len_Mach,len_u)) 
        CN_u        = np.zeros((len_AoA,len_Mach,len_u))
        
        # reset conditions         
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.aerodynamics.angles.alpha            = AoAs   
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        
        for u_i in range(len_u): 
            conditions.freestream.mach_number               = Machs + u[u_i] / 343 
            Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)  
            Clift_u[:,:,u_i]     = np.reshape(Clift_res,(len_Mach,len_AoA)).T 
            Cdrag_u[:,:,u_i]     = np.reshape(Cdrag_res,(len_Mach,len_AoA)).T 
            CX_u[:,:,u_i]        = np.reshape(CX_res,(len_Mach,len_AoA)).T  
            CY_u[:,:,u_i]        = np.reshape(CY_res,(len_Mach,len_AoA)).T  
            CZ_u[:,:,u_i]        = np.reshape(CZ_res,(len_Mach,len_AoA)).T  
            CL_u[:,:,u_i]        = np.reshape(CL_res,(len_Mach,len_AoA)).T  
            CM_u[:,:,u_i]        = np.reshape(CM_res,(len_Mach,len_AoA)).T  
            CN_u[:,:,u_i]        = np.reshape(CN_res,(len_Mach,len_AoA)).T
                            
    
        # -------------------------------------------------------               
        # Pitch Rate 
        # -------------------------------------------------------       
        Clift_pitch_rate     = np.zeros((len_AoA,len_Mach,len_pitch_rate)) 
        Cdrag_pitch_rate     = np.zeros((len_AoA,len_Mach,len_pitch_rate)) 
        CX_pitch_rate        = np.zeros((len_AoA,len_Mach,len_pitch_rate)) 
        CY_pitch_rate        = np.zeros((len_AoA,len_Mach,len_pitch_rate)) 
        CZ_pitch_rate        = np.zeros((len_AoA,len_Mach,len_pitch_rate)) 
        CL_pitch_rate        = np.zeros((len_AoA,len_Mach,len_pitch_rate)) 
        CM_pitch_rate        = np.zeros((len_AoA,len_Mach,len_pitch_rate)) 
        CN_pitch_rate        = np.zeros((len_AoA,len_Mach,len_pitch_rate))
        
        # reset conditions         
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.aerodynamics.angles.alpha            = AoAs 
        conditions.freestream.mach_number               = Machs
        conditions.freestream.velocity                  = Machs * 343 # speed of sound  
        conditions.static_stability.pitch_rate         = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate          = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate           = np.zeros_like(Machs)  
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        
        for pitch_i in range(len_pitch_rate):  
            conditions.static_stability.pitch_rate[:,0]                 = pitch_rate[pitch_i]  
            Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)  
            Clift_pitch_rate[:,:,pitch_i]     = np.reshape(Clift_res,(len_Mach,len_AoA)).T 
            Cdrag_pitch_rate[:,:,pitch_i]     = np.reshape(Cdrag_res,(len_Mach,len_AoA)).T 
            CX_pitch_rate[:,:,pitch_i]        = np.reshape(CX_res,(len_Mach,len_AoA)).T  
            CY_pitch_rate[:,:,pitch_i]        = np.reshape(CY_res,(len_Mach,len_AoA)).T  
            CZ_pitch_rate[:,:,pitch_i]        = np.reshape(CZ_res,(len_Mach,len_AoA)).T  
            CL_pitch_rate[:,:,pitch_i]        = np.reshape(CL_res,(len_Mach,len_AoA)).T  
            CM_pitch_rate[:,:,pitch_i]        = np.reshape(CM_res,(len_Mach,len_AoA)).T  
            CN_pitch_rate[:,:,pitch_i]        = np.reshape(CN_res,(len_Mach,len_AoA)).T  
    
    
        # -------------------------------------------------------               
        # Roll  Rate 
        # -------------------------------------------------------                                                     
        Clift_roll_rate     = np.zeros((len_AoA,len_Mach,len_roll_rate)) 
        Cdrag_roll_rate     = np.zeros((len_AoA,len_Mach,len_roll_rate)) 
        CX_roll_rate        = np.zeros((len_AoA,len_Mach,len_roll_rate)) 
        CY_roll_rate        = np.zeros((len_AoA,len_Mach,len_roll_rate)) 
        CZ_roll_rate        = np.zeros((len_AoA,len_Mach,len_roll_rate)) 
        CL_roll_rate        = np.zeros((len_AoA,len_Mach,len_roll_rate)) 
        CM_roll_rate        = np.zeros((len_AoA,len_Mach,len_roll_rate)) 
        CN_roll_rate        = np.zeros((len_AoA,len_Mach,len_roll_rate))
        
        # reset conditions         
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.aerodynamics.angles.alpha            = AoAs 
        conditions.freestream.mach_number               = Machs
        conditions.freestream.velocity                  = Machs * 343 # speed of sound  
        conditions.static_stability.pitch_rate         = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate          = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate           = np.zeros_like(Machs)  
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)        
        
        for roll_i in range(len_roll_rate):  
            conditions.static_stability.roll_rate[:,0]                  = roll_rate[roll_i]             
            Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)  
            
            Clift_roll_rate[:,:,roll_i]     = np.reshape(Clift_res,(len_Mach,len_AoA)).T 
            Cdrag_roll_rate[:,:,roll_i]     = np.reshape(Cdrag_res,(len_Mach,len_AoA)).T 
            CX_roll_rate[:,:,roll_i]        = np.reshape(CX_res,(len_Mach,len_AoA)).T  
            CY_roll_rate[:,:,roll_i]        = np.reshape(CY_res,(len_Mach,len_AoA)).T  
            CZ_roll_rate[:,:,roll_i]        = np.reshape(CZ_res,(len_Mach,len_AoA)).T  
            CL_roll_rate[:,:,roll_i]        = np.reshape(CL_res,(len_Mach,len_AoA)).T  
            CM_roll_rate[:,:,roll_i]        = np.reshape(CM_res,(len_Mach,len_AoA)).T  
            CN_roll_rate[:,:,roll_i]        = np.reshape(CN_res,(len_Mach,len_AoA)).T        
            

        # -------------------------------------------------------               
        # Yaw Rate 
        # -------------------------------------------------------           
        Clift_yaw_rate     = np.zeros((len_AoA,len_Mach,len_yaw_rate)) 
        Cdrag_yaw_rate     = np.zeros((len_AoA,len_Mach,len_yaw_rate)) 
        CX_yaw_rate        = np.zeros((len_AoA,len_Mach,len_yaw_rate)) 
        CY_yaw_rate        = np.zeros((len_AoA,len_Mach,len_yaw_rate)) 
        CZ_yaw_rate        = np.zeros((len_AoA,len_Mach,len_yaw_rate)) 
        CL_yaw_rate        = np.zeros((len_AoA,len_Mach,len_yaw_rate)) 
        CM_yaw_rate        = np.zeros((len_AoA,len_Mach,len_yaw_rate)) 
        CN_yaw_rate        = np.zeros((len_AoA,len_Mach,len_yaw_rate))

        # reset conditions         
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.aerodynamics.angles.alpha            = AoAs 
        conditions.freestream.mach_number               = Machs
        conditions.freestream.velocity                  = Machs * 343 # speed of sound  
        conditions.static_stability.pitch_rate          = np.zeros_like(Machs)      
        conditions.static_stability.roll_rate           = np.zeros_like(Machs)
        conditions.static_stability.yaw_rate            = np.zeros_like(Machs)  
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        
        for yaw_i in range(len_yaw_rate): 
            conditions.static_stability.yaw_rate[:,0]                  = yaw_rate[yaw_i]             
            Clift_res,Cdrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = evaluate_VLM(conditions,settings,geometry)  
            Clift_yaw_rate[:,:,yaw_i]     = np.reshape(Clift_res,(len_Mach,len_AoA)).T 
            Cdrag_yaw_rate[:,:,yaw_i]     = np.reshape(Cdrag_res,(len_Mach,len_AoA)).T 
            CX_yaw_rate[:,:,yaw_i]        = np.reshape(CX_res,(len_Mach,len_AoA)).T  
            CY_yaw_rate[:,:,yaw_i]        = np.reshape(CY_res,(len_Mach,len_AoA)).T  
            CZ_yaw_rate[:,:,yaw_i]        = np.reshape(CZ_res,(len_Mach,len_AoA)).T  
            CL_yaw_rate[:,:,yaw_i]        = np.reshape(CL_res,(len_Mach,len_AoA)).T  
            CM_yaw_rate[:,:,yaw_i]        = np.reshape(CM_res,(len_Mach,len_AoA)).T  
            CN_yaw_rate[:,:,yaw_i]        = np.reshape(CN_res,(len_Mach,len_AoA)).T
              
        training.Clift        = Clift  
        training.Cdrag        = Cdrag
        training.CX_0         = CX_0 
        training.CY_0         = CY_0 
        training.CZ_0         = CZ_0 
        training.CL_0         = CL_0 
        training.CM_0         = CM_0 
        training.CN_0         = CN_0 
        training.CM_alpha     = (CM_d_e[0,:,:] - CM_d_e[1,:,:])   / (AoA[0]-AoA[1]) 
        training.Clift_alpha  = (Clift_d_e[0,:,:] - Clift_d_e[1,:,:])   / (AoA[0]-AoA[1])  
        training.Clift_delta_e= (Clift_d_e[:,:,0] - Clift_d_e[:,:,1])   /  (delta_e[0]-delta_e[1]) 
        training.CM_delta_e   = (CM_d_e[:,:,0] - CM_d_e[:,:,1])   / (delta_e[0]-delta_e[1])    
        training.CY_beta      = (CY_beta[:,:,0] - CY_beta[:,:,1])   / (Beta[0]-Beta[1])
        training.CL_beta      = -(CL_beta[:,:,0] - CL_beta[:,:,1])   / (Beta[0]-Beta[1])  # negative sign due definition in literature
        training.CN_beta      = (CN_beta[:,:,0] - CN_beta[:,:,1])   / (Beta[0]-Beta[1])
        training.CY_ddelta_a  = (CY_d_a[:,:,0] -  CY_d_a[:,:,1])   / (delta_a[0]-delta_a[1])
        training.CL_delta_a   = (CL_d_a[:,:,0] - CL_d_a[:,:,1])   / (delta_a[0]-delta_a[1]) 
        training.CN_delta_a   = (CN_d_a[:,:,0] - CN_d_a[:,:,1])   / (delta_a[0]-delta_a[1])
        training.CY_ddelta_r  = (CY_d_r[:,:,0] - CY_d_r[:,:,1])   /  (delta_r[0]-delta_r[1])
        training.Cl_ddelta_r  = (CL_d_r[:,:,0] - CL_d_r[:,:,1])   / (delta_r[0]-delta_r[1])
        training.CN_delta_r   = -(CN_d_r[:,:,0] - CN_d_r[:,:,1])   / (delta_r[0]-delta_r[1]) # negative sign due definition in literature 
                          
        training.Clift_p       = (Clift_roll_rate[:,:,0] - CX_roll_rate[:,:,1])   / (roll_rate[0]-roll_rate[1])          
        training.Clift_q       = (Clift_pitch_rate[:,:,0] - CX_pitch_rate[:,:,1])   / (pitch_rate[1]-pitch_rate[0])        
        training.Clift_r       = (Clift_yaw_rate[:,:,0] - CX_yaw_rate[:,:,1])   / (yaw_rate[1]-yaw_rate[0])             
        training.CX_u          =  0 #    
        training.CX_v          =  0 #    
        training.CX_w          =  0 #    
        training.CY_u          =  0 #    
        training.CY_v          =  0 #    
        training.CY_w          =  0 #    
        training.CZ_u          =  (CX_u[:,:,0] - CX_u[:,:,1])   / (u[0]-u[1])   
        training.CZ_v          =  0 #    
        training.CZ_w          =  0 #    
        training.CL_u          =  0 #    
        training.CL_v          =  0 #    
        training.CL_w          =  0 #    
        training.CM_u          =  0 #    
        training.CM_v          =  0 #    
        training.CM_w          =  0 #    
        training.CN_u          =  0 #    
        training.CN_v          =  0 #    
        training.CN_w          =  0 #    
        training.CX_p          = (CX_roll_rate[:,:,0] - CX_roll_rate[:,:,1])   / (roll_rate[0]-roll_rate[1])      
        training.CX_q          = (CX_pitch_rate[:,:,0] - CX_pitch_rate[:,:,1])   / (pitch_rate[1]-pitch_rate[0])     
        training.CX_r          = (CX_yaw_rate[:,:,0] - CX_yaw_rate[:,:,1])   / (yaw_rate[1]-yaw_rate[0])     
        training.CY_p          = (CY_roll_rate[:,:,0] - CY_roll_rate[:,:,1])   / (roll_rate[0]-roll_rate[1])    
        training.CY_q          = (CY_pitch_rate[:,:,0] - CY_pitch_rate[:,:,1])   / (pitch_rate[1]-pitch_rate[0])    
        training.CY_r          = (CY_yaw_rate[:,:,0] - CY_yaw_rate[:,:,1])   / (yaw_rate[1]-yaw_rate[0])     
        training.CZ_p          = (CZ_roll_rate[:,:,0] - CZ_roll_rate[:,:,1])   / (roll_rate[0]-roll_rate[1])     
        training.CZ_q          = (CZ_pitch_rate[:,:,0] - CZ_pitch_rate[:,:,1])   / (pitch_rate[1]-pitch_rate[0])    
        training.CZ_r          = (CZ_yaw_rate[:,:,0] - CZ_yaw_rate[:,:,1])   / (yaw_rate[1]-yaw_rate[0])     
        training.CL_p          = (CL_roll_rate[:,:,0] - CL_roll_rate[:,:,1])   / (roll_rate[0]-roll_rate[1])     
        training.CL_q          = (CL_pitch_rate[:,:,0] - CL_pitch_rate[:,:,1])   / (pitch_rate[1]-pitch_rate[0])     
        training.CL_r          = (CL_yaw_rate[:,:,0] - CL_yaw_rate[:,:,1])   / (yaw_rate[1]-yaw_rate[0])     
        training.CM_p          = (CM_roll_rate[:,:,0] - CM_roll_rate[:,:,1])   / (roll_rate[0]-roll_rate[1])     
        training.CM_q          = (CM_pitch_rate[:,:,0] - CM_pitch_rate[:,:,1])   / (pitch_rate[1]-pitch_rate[0])     
        training.CM_r          = (CM_yaw_rate[:,:,0] - CM_yaw_rate[:,:,1])   / (yaw_rate[1]-yaw_rate[0])     
        training.CN_p          = (CN_roll_rate[:,:,0] - CN_roll_rate[:,:,1])   / (roll_rate[0]-roll_rate[1])      
        training.CN_q          = (CN_pitch_rate[:,:,0] - CN_pitch_rate[:,:,1])   / (pitch_rate[1]-pitch_rate[0])     
        training.CN_r          = (CN_yaw_rate[:,:,0] - CN_yaw_rate[:,:,1])   / (yaw_rate[1]-yaw_rate[0])     
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
        surrogates.Clift          = RegularGridInterpolator((AoA_data,mach_data),training.Clift    ,method = 'linear',   bounds_error=False, fill_value=None)   
        surrogates.Cdrag          = RegularGridInterpolator((AoA_data,mach_data),training.Cdrag     ,method = 'linear',   bounds_error=False, fill_value=None)    
        surrogates.CM_delta_e     = RegularGridInterpolator((AoA_data,mach_data),training.CM_delta_e,method = 'linear',   bounds_error=False, fill_value=None)   
        surrogates.CM_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.CM_alpha ,method = 'linear',   bounds_error=False, fill_value=None)    
        surrogates.Clift_alpha    = RegularGridInterpolator((AoA_data,mach_data),training.Clift_alpha,method = 'linear',   bounds_error=False, fill_value=None)   
        surrogates.Clift_delta_e  = RegularGridInterpolator((AoA_data,mach_data),training.Clift_delta_e,method = 'linear',   bounds_error=False, fill_value=None)    
        surrogates.CX_0           = RegularGridInterpolator((AoA_data,mach_data),training.CX_0        ,method = 'linear',   bounds_error=False, fill_value=None)     
        surrogates.CY_0           = RegularGridInterpolator((AoA_data,mach_data),training.CY_0        ,method = 'linear',   bounds_error=False, fill_value=None)     
        surrogates.CZ_0           = RegularGridInterpolator((AoA_data,mach_data),training.CZ_0        ,method = 'linear',   bounds_error=False, fill_value=None)     
        surrogates.CL_0           = RegularGridInterpolator((AoA_data,mach_data),training.CL_0        ,method = 'linear',   bounds_error=False, fill_value=None)     
        surrogates.CM_0           = RegularGridInterpolator((AoA_data,mach_data),training.CM_0        ,method = 'linear',   bounds_error=False, fill_value=None)     
        surrogates.CN_0           = RegularGridInterpolator((AoA_data,mach_data),training.CN_0    ,method = 'linear',   bounds_error=False, fill_value=None)
        surrogates.CY_beta        = RegularGridInterpolator((AoA_data,mach_data),training.CY_beta,method = 'linear',   bounds_error=False, fill_value=None)
        surrogates.CL_beta        = RegularGridInterpolator((AoA_data,mach_data),training.CL_beta     ,method = 'linear',   bounds_error=False, fill_value=None)
        surrogates.CN_beta        = RegularGridInterpolator((AoA_data,mach_data),training.CN_beta     ,method = 'linear',   bounds_error=False, fill_value=None)
        surrogates.CY_ddelta_a    = RegularGridInterpolator((AoA_data,mach_data),training.CY_ddelta_a ,method = 'linear',   bounds_error=False, fill_value=None)
        surrogates.CL_delta_a     = RegularGridInterpolator((AoA_data,mach_data),training.CL_delta_a  ,method = 'linear',   bounds_error=False, fill_value=None)
        surrogates.CN_delta_a     = RegularGridInterpolator((AoA_data,mach_data),training.CN_delta_a  ,method = 'linear',   bounds_error=False, fill_value=None)
        surrogates.CY_ddelta_r    = RegularGridInterpolator((AoA_data,mach_data),training.CY_ddelta_r,method = 'linear',   bounds_error=False, fill_value=None)
        surrogates.Cl_ddelta_r    = RegularGridInterpolator((AoA_data,mach_data),training.Cl_ddelta_r,method = 'linear',   bounds_error=False, fill_value=None)
        surrogates.CN_delta_r     = RegularGridInterpolator((AoA_data,mach_data),training.CN_delta_r ,method = 'linear',   bounds_error=False, fill_value=None) 
        surrogates.CL_p_surrogate = RegularGridInterpolator((AoA_data,mach_data),training.CL_p  ,method = 'linear',   bounds_error=False, fill_value=None)
        
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

    return Clift,Cdrag,CX,CY,CZ,CL,CM, CN

