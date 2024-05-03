## @ingroup Analyses-Stability
# RCAIDE/Framework/Analyses/Stability/Common/Vortex_Lattice.py
# 
# 
# Created:  Apr 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core                                       import Data, Units  
from RCAIDE.Library.Methods.Aerodynamics.Vortex_Lattice_Method   import VLM  
from RCAIDE.Framework.Analyses.Stability                         import Stability

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
        self.settings.model_fuselage                  = False
        self.settings.model_nacelle                   = False
        self.settings.leading_edge_suction_multiplier = 1.0
        self.settings.propeller_wake_model            = False
        self.settings.discretize_control_surfaces     = True 
        self.settings.use_VORLAX_matrix_calculation   = False
        self.settings.floating_point_precision        = np.float32
        self.settings.use_surrogate                   = True

        # conditions table, used for surrogate model training
        self.training                                = Data()
        self.training.angle_of_attack                = np.array([-5.  , 0.  , 5.])  * Units.deg 
        self.training.Mach                           = np.array([0.1 , 0.2 , 0.5 ])       
        self.training.sideslip_angle                 = np.array([-5  , 0   , 5.0])* Units.deg 
        self.training.elevator_deflection            = np.array([-1.  , 0.,  1.0])  * Units.deg   
        self.training.aileron_deflection             = np.array([-1.  , 0.,  1.0])  * Units.deg   
        self.training.slat_deflection                = np.array([-1.  , 0.,  1.0])  * Units.deg   
        self.training.flap_deflection                = np.array([-10.  , -5.,  0])  * Units.deg   
        self.training.rudder_deflection              = np.array([-1.  , 0.,  1.0])  * Units.deg 
        self.training.pitch_rate                     = np.array([-0.01  , 0.,  0.01])  * Units.rad / Units.sec
        self.training.roll_rate                      = np.array([-0.3  , 0.,  0.3])  * Units.rad / Units.sec
        self.training.yaw_rate                       = np.array([-0.01  , 0.,  0.01])  * Units.rad / Units.sec        

        # force coefficients 
        self.training.CX                             = None 
        self.training.CY                             = None 
        self.training.CZ                             = None  
                     
        # moment coefficients              
        self.training.CL                             = None 
        self.training.CM                             = None 
        self.training.CN                             = None
        
        self.training.static_margin                  = None
        
        # moment derivatives
        self.training.CM_delta_e                     = None
        self.training.dCM_dalpha                     = None
        self.training.dCL_dalpha                     = None
        self.training.dCY_dbeta                      = None
        #self.training.dCY_dp                         = None
        #self.training.dCY_dr                         = None
        self.training.dCl_dbeta                      = None
        #self.training.dCl_dr                         = None
        self.training.dCl_dp                         = None
        self.training.dCn_dbeta                      = None
        #self.training.dCn_dr                         = None
        #self.training.dCn_dp                         = None
        self.training.dCl_ddelta_a                   = None
        self.training.dCn_ddelta_a                   = None
        self.training.dCn_ddelta_r                   = None
        
        # surrogoate models
        self.surrogates                              = Data()   
        self.surrogates.CLift                        = None    
        self.surrogates.CDrag                        = None 
        self.surrogates.CX                           = None 
        self.surrogates.CY                           = None 
        self.surrogates.CZ                           = None  
        self.surrogates.CM                           = None  
        self.surrogates.CL                           = None   
        self.surrogates.CN                           = None
        self.surrogates.static_margin                = None
        self.surrogates.pitch_rate                   = None
        self.surrogates.roll_rate                    = None  
        self.surrogates.yaw_rate                     = None            
        
        self.surrogates.CM_delta_e                   = None
        self.surrogates.dCM_dalpha                   = None
        self.surrogates.dCL_dalpha                   = None
        self.surrogates.dCY_dbeta                    = None
        #self.surrogates.dCY_dp                       = None
        #self.surrogates.dCY_dr                       = None
        self.surrogates.dCl_dbeta                    = None
        #self.surrogates.dCl_dr                       = None
        self.surrogates.dCl_dp                       = None
        self.surrogates.dCn_dbeta                    = None
        #self.surrogates.dCn_dr                       = None
        #self.surrogates.dCn_dp                       = None
        self.surrogates.dCl_ddelta_a                 = None
        self.surrogates.dCn_ddelta_a                 = None
        self.surrogates.dCn_ddelta_r                 = None
        
        self.evaluate                                = None  
            
    def initialize(self): 
        settings                  = self.settings  
        use_surrogate             = settings.use_surrogate
        propeller_wake_model      = settings.propeller_wake_model 
        n_sw                      = settings.number_of_spanwise_vortices
        n_cw                      = settings.number_of_chordwise_vortices
        mf                        = settings.model_fuselage
        mn                        = settings.model_nacelle
        dcs                       = settings.discretize_control_surfaces 
             
        # Unpack:
        settings = self.settings      
        
        if n_sw is not None:
            settings.number_of_spanwise_vortices  = n_sw
        
        if n_cw is not None:
            settings.number_of_chordwise_vortices = n_cw 
            
        settings.use_surrogate              = use_surrogate
        settings.propeller_wake_model       = propeller_wake_model 
        settings.discretize_control_surfaces= dcs
        settings.model_fuselage             = mf
        settings.model_nacelle              = mn
        
        # If we are using the surrogate
        if use_surrogate == True: 
            # sample training data
            self.sample_training()
                        
            # build surrogate
            self.build_surrogate()        
            
            self.evaluate = self.evaluate_surrogate
               
        else:
            self.evaluate = self.evaluate_no_surrogate


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
        delta_e     = np.atleast_2d(conditions.control_surfaces.elevator.deflection) 
        delta_a     = np.atleast_2d(conditions.control_surfaces.aileron.deflection)   
        delta_r     = np.atleast_2d(conditions.control_surfaces.rudder.deflection)   
        delta_s     = np.atleast_2d(conditions.control_surfaces.slat.deflection)  
        delta_f     = np.atleast_2d(conditions.control_surfaces.flap.deflection)
        pitch_rate    = np.atleast_2d(conditions.stability.dynamic.pitch_rate)  

        CLift_surrogate         = surrogates.CLift    
        CDrag_surrogate         = surrogates.CDrag 
        CX_0_surrogate          = surrogates.CX_0
        CY_0_surrogate          = surrogates.CY_0
        CZ_0_surrogate          = surrogates.CZ_0
        CL_0_surrogate          = surrogates.CL_0
        CM_0_surrogate          = surrogates.CM_0
        CN_0_surrogate          = surrogates.CN_0
        
        dCM_delta_e_surrogate  = surrogates.dCM_delta_e
        #dCM_dalpha_surrogate   = surrogates.dCM_dalpha
        #dCL_dalpha_surrogate   = surrogates.dCL_dalpha
        dCL_delta_e_surrogate  = surrogates.dCL_delta_e
        
        dCY_dbeta_surrogate    = surrogates.dCY_dbeta
        dCl_dbeta_surrogate    = surrogates.dCl_dbeta
        dCn_dbeta_surrogate    = surrogates.dCn_dbeta
        dCY_ddelta_a_surrogate = surrogates.dCY_ddelta_a
        dCl_ddelta_a_surrogate = surrogates.dCl_ddelta_a
        dCn_ddelta_a_surrogate = surrogates.dCn_ddelta_a
        dCY_ddelta_r_surrogate = surrogates.dCY_ddelta_r
        dCl_ddelta_r_surrogate = surrogates.dCl_ddelta_r
        dCn_ddelta_r_surrogate = surrogates.dCn_ddelta_r
        
        dCl_dp_surrogate = surrogates.dCl_dp_surrogate
        
        pts          = np.hstack((AoA,Mach))
        CLift        = np.atleast_2d(CLift_surrogate(pts)).T         # this surrogate is basically CLalpha*alpha 
        CDrag        = np.atleast_2d(CDrag_surrogate(pts)).T   
        CX_0 = np.atleast_2d(CX_0_surrogate(pts)).T
        CY_0 = np.atleast_2d(CY_0_surrogate(pts)).T
        CZ_0 = np.atleast_2d(CZ_0_surrogate(pts)).T
        CL_0 = np.atleast_2d(CL_0_surrogate(pts)).T
        CM_0 = np.atleast_2d(CM_0_surrogate(pts)).T        # this surrogate is basically Cm0 and Cmalpha*alpha
        CN_0 = np.atleast_2d(CN_0_surrogate(pts)).T

        dCY_dbeta  = np.atleast_2d(dCY_dbeta_surrogate(pts)).T
        dCl_dbeta  = np.atleast_2d(dCl_dbeta_surrogate(pts)).T 
        dCn_dbeta = np.atleast_2d(dCn_dbeta_surrogate(pts)).T
        
        dCM_delta_e  = np.atleast_2d(dCM_delta_e_surrogate(pts)).T
        dCL_delta_e  = np.atleast_2d(dCL_delta_e_surrogate(pts)).T 
        dCY_ddelta_a = np.atleast_2d(dCY_ddelta_a_surrogate(pts)).T
        dCl_ddelta_a = np.atleast_2d(dCl_ddelta_a_surrogate(pts)).T
        dCn_ddelta_a = np.atleast_2d(dCn_ddelta_a_surrogate(pts)).T
        dCY_ddelta_r = np.atleast_2d(dCY_ddelta_r_surrogate(pts)).T
        dCl_ddelta_r = np.atleast_2d(dCl_ddelta_r_surrogate(pts)).T
        dCn_ddelta_r = np.atleast_2d(dCn_ddelta_r_surrogate(pts)).T
        dCl_dp = np.atleast_2d(dCl_dp_surrogate(pts)).T
           
        #dCM_dalpha   = np.atleast_2d(dCM_dalpha_surrogate(pts)).T    # not needed as we can build a surrogate of CM (which already has in AoA) 
        #dCL_dalpha   = np.atleast_2d(dCL_dalpha_surrogate(pts)).T    # not needed as we can build a surrogate of CL (which already has in AoA)
        

        #conditions.stability.static.derivatives.CM_delta_e   = np.atleast_2d(CM_delta_e)
        #conditions.stability.static.derivatives.dCM_dalpha   = np.atleast_2d(dCM_dalpha)
        #conditions.stability.static.derivatives.dCL_dalpha   = np.atleast_2d(dCL_dalpha)
        #conditions.stability.static.derivatives.dCY_dbeta    = np.atleast_2d(dCY_dbeta)
        #conditions.stability.static.derivatives.dCY_dp       = np.atleast_2d(dCY_dp) 
        #conditions.stability.static.derivatives.dCY_dr       = np.atleast_2d(dCY_dr)
        #conditions.stability.static.derivatives.dCl_dbeta    = np.atleast_2d(dCl_dbeta)
        #conditions.stability.static.derivatives.dCl_dr       = np.atleast_2d(dCl_dr)
        #conditions.stability.static.derivatives.dCl_dp       = np.atleast_2d(dCl_dp)
        #conditions.stability.static.derivatives.dCn_dbeta    = np.atleast_2d(dCn_dbeta)
        #conditions.stability.static.derivatives.dCn_dr       = np.atleast_2d(dCn_dr)
        #conditions.stability.static.derivatives.dCn_dp       = np.atleast_2d(dCn_dp)        
        #conditions.stability.static.derivatives.dCl_ddelta_a = np.atleast_2d(dCl_ddelta_a)
        #conditions.stability.static.derivatives.dCn_ddelta_a = np.atleast_2d(dCn_ddelta_a)
        #conditions.stability.static.derivatives.dCn_ddelta_r = np.atleast_2d(dCn_ddelta_r) 
        
        
        state.conditions.aerodynamics.coefficients.lift         = CLift + dCL_delta_e*delta_e 
        conditions.aerodynamics.lift_breakdown.total            = CLift + dCL_delta_e*delta_e
        conditions.aerodynamics.drag_breakdown.induced.inviscid = CDrag 
        
        conditions.stability.static.coefficients.CX        = CX_0 
        conditions.stability.static.coefficients.CY        = CY_0 + dCY_dbeta * Beta + dCY_ddelta_a * delta_a + dCY_ddelta_r * delta_r
        conditions.stability.static.coefficients.CZ        = CZ_0
        conditions.stability.static.coefficients.CL        = CL_0 + dCl_dbeta * Beta + dCl_ddelta_a * delta_a + dCl_ddelta_r * delta_r #+ dCl_dp *( pitch_rate / conditions.freestream.velocity) # rates are normalized 
        conditions.stability.static.coefficients.CM        = CM_0 + dCM_delta_e*delta_e
        conditions.stability.static.coefficients.CN        = CN_0 + dCn_dbeta * Beta + dCn_ddelta_a * delta_a + dCn_ddelta_r * delta_r
        #conditions.stability.static_margin                 = np.atleast_2d(static_margin)
        
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
        CLift,CDrag,CX,CY,CZ,CL_mom,CM,CN = calculate_VLM(conditions,settings,geometry) 

        # compute deriviatives and pack   
        conditions.stability.static.coefficients.lift    = np.atleast_2d(CLift).T
        conditions.stability.static.coefficients.drag    = np.atleast_2d(CDrag).T 
        conditions.stability.static.coefficients.CX      = np.atleast_2d(CX).T # NEED TO CHANGE np.atleast_2d(CX).T
        conditions.stability.static.coefficients.CY      = np.atleast_2d(CY).T
        conditions.stability.static.coefficients.CZ      = np.atleast_2d(CZ).T # NEED TO CHANGE np.atleast_2d(CZ).T
        conditions.stability.static.coefficients.CL      = np.atleast_2d(CL_mom).T
        conditions.stability.static.coefficients.CM      = np.atleast_2d(CM).T
        conditions.stability.static.coefficients.CN      = np.atleast_2d(CN).T 
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
        
        len_AoA        = len(AoA)   
        len_Mach       = len(Mach) 
        len_Beta       = len(Beta)     
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
        CLift_beta     = np.zeros((len_AoA,len_Mach,len_Beta)) 
        CDrag_beta     = np.zeros((len_AoA,len_Mach,len_Beta)) 
        CX_beta        = np.zeros((len_AoA,len_Mach,len_Beta)) 
        CY_beta        = np.zeros((len_AoA,len_Mach,len_Beta)) 
        CZ_beta        = np.zeros((len_AoA,len_Mach,len_Beta)) 
        CL_beta        = np.zeros((len_AoA,len_Mach,len_Beta)) 
        CM_beta        = np.zeros((len_AoA,len_Mach,len_Beta)) 
        CN_beta        = np.zeros((len_AoA,len_Mach,len_Beta))

        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.aerodynamics.angles.alpha            = AoAs
        conditions.freestream.mach_number               = Machs 
        conditions.stability.dynamic.pitch_rate         = np.zeros_like(Machs)      
        conditions.stability.dynamic.roll_rate          = np.zeros_like(Machs)
        conditions.stability.dynamic.yaw_rate           = np.zeros_like(Machs)  
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.freestream.velocity                  = np.zeros_like(Machs) 
        
        for beta_i in range(len_Beta):               
            conditions.aerodynamics.angles.beta         =  np.ones_like(Machs)*Beta[beta_i]
            CLift_res,CDrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = calculate_VLM(conditions,settings,geometry)     
            CLift_beta[:,:,beta_i] = np.reshape(CLift_res,(len_Mach,len_AoA)).T 
            CDrag_beta[:,:,beta_i] = np.reshape(CDrag_res,(len_Mach,len_AoA)).T                                 
            CX_beta[:,:,beta_i]    = np.reshape(CX_res,(len_Mach,len_AoA)).T 
            CY_beta[:,:,beta_i]    = np.reshape(CY_res,(len_Mach,len_AoA)).T 
            CZ_beta[:,:,beta_i]    = np.reshape(CZ_res,(len_Mach,len_AoA)).T 
            CL_beta[:,:,beta_i]    = np.reshape(CL_res,(len_Mach,len_AoA)).T 
            CM_beta[:,:,beta_i]    = np.reshape(CM_res,(len_Mach,len_AoA)).T 
            CN_beta[:,:,beta_i]    = np.reshape(CN_res,(len_Mach,len_AoA)).T 
                     

        # --------------------------------------------------------------------------------------------------------------
        # Zero Lift 
        # --------------------------------------------------------------------------------------------------------------
        CLift          = np.zeros((len_AoA,len_Mach)) 
        CDrag          = np.zeros((len_AoA,len_Mach)) 
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
        conditions.stability.dynamic.pitch_rate         = np.zeros_like(Machs)      
        conditions.stability.dynamic.roll_rate          = np.zeros_like(Machs)
        conditions.stability.dynamic.yaw_rate           = np.zeros_like(Machs)  
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        conditions.freestream.velocity                  = np.zeros_like(Machs)  
        
        CLift_res,CDrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = calculate_VLM(conditions,settings,geometry) 
        CLift[:,:]   = np.reshape(CLift_res,(len_Mach,len_AoA)).T 
        CDrag[:,:]   = np.reshape(CDrag_res,(len_Mach,len_AoA)).T 
        CX_0[:,:]    = np.reshape(CX_res,(len_Mach,len_AoA)).T 
        CY_0[:,:]    = np.reshape(CY_res,(len_Mach,len_AoA)).T 
        CZ_0[:,:]    = np.reshape(CZ_res,(len_Mach,len_AoA)).T 
        CL_0[:,:]    = np.reshape(CL_res,(len_Mach,len_AoA)).T 
        CM_0[:,:]    = np.reshape(CM_res,(len_Mach,len_AoA)).T 
        CN_0[:,:]    = np.reshape(CN_res,(len_Mach,len_AoA)).T   

        # --------------------------------------------------------------------------------------------------------------
        # Elevator 
        # --------------------------------------------------------------------------------------------------------------
        CLift_d_e      = np.zeros((len_AoA,len_Mach,len_d_e)) 
        CDrag_d_e      = np.zeros((len_AoA,len_Mach,len_d_e)) 
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
        conditions.stability.dynamic.pitch_rate         = np.zeros_like(Machs)      
        conditions.stability.dynamic.roll_rate          = np.zeros_like(Machs)
        conditions.stability.dynamic.yaw_rate           = np.zeros_like(Machs)  
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
                        CLift_res,CDrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = calculate_VLM(conditions,settings,geometry)     
                        CLift_d_e[:,:,e_i] = np.reshape(CLift_res,(len_Mach,len_AoA)).T 
                        CDrag_d_e[:,:,e_i] = np.reshape(CDrag_res,(len_Mach,len_AoA)).T                                 
                        CX_d_e[:,:,e_i]    = np.reshape(CX_res,(len_Mach,len_AoA)).T 
                        CY_d_e[:,:,e_i]    = np.reshape(CY_res,(len_Mach,len_AoA)).T 
                        CZ_d_e[:,:,e_i]    = np.reshape(CZ_res,(len_Mach,len_AoA)).T 
                        CL_d_e[:,:,e_i]    = np.reshape(CL_res,(len_Mach,len_AoA)).T 
                        CM_d_e[:,:,e_i]    = np.reshape(CM_res,(len_Mach,len_AoA)).T 
                        CN_d_e[:,:,e_i]    = np.reshape(CN_res,(len_Mach,len_AoA)).T       
                        
                
        # --------------------------------------------------------------------------------------------------------------
        # Aileron 
        # --------------------------------------------------------------------------------------------------------------    
        CLift_d_a      = np.zeros((len_AoA,len_Mach,len_d_a)) 
        CDrag_d_a      = np.zeros((len_AoA,len_Mach,len_d_a)) 
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
        conditions.stability.dynamic.pitch_rate         = np.zeros_like(Machs)      
        conditions.stability.dynamic.roll_rate          = np.zeros_like(Machs)
        conditions.stability.dynamic.yaw_rate           = np.zeros_like(Machs)  
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
                        CLift_res,CDrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = calculate_VLM(conditions,settings,geometry)  
                        CLift_d_a[:,:,a_i] = np.reshape(CLift_res,(len_Mach,len_AoA)).T 
                        CDrag_d_a[:,:,a_i] = np.reshape(CDrag_res,(len_Mach,len_AoA)).T                                 
                        CX_d_a[:,:,a_i]    = np.reshape(CX_res,(len_Mach,len_AoA)).T 
                        CY_d_a[:,:,a_i]    = np.reshape(CY_res,(len_Mach,len_AoA)).T 
                        CZ_d_a[:,:,a_i]    = np.reshape(CZ_res,(len_Mach,len_AoA)).T 
                        CL_d_a[:,:,a_i]    = np.reshape(CL_res,(len_Mach,len_AoA)).T 
                        CM_d_a[:,:,a_i]    = np.reshape(CM_res,(len_Mach,len_AoA)).T 
                        CN_d_a[:,:,a_i]    = np.reshape(CN_res,(len_Mach,len_AoA)).T 
        
        
                
        # --------------------------------------------------------------------------------------------------------------
        # Rudder 
        # --------------------------------------------------------------------------------------------------------------         
        CLift_d_r      = np.zeros((len_AoA,len_Mach,len_d_r)) 
        CDrag_d_r      = np.zeros((len_AoA,len_Mach,len_d_r)) 
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
        conditions.stability.dynamic.pitch_rate         = np.zeros_like(Machs)      
        conditions.stability.dynamic.roll_rate          = np.zeros_like(Machs)
        conditions.stability.dynamic.yaw_rate           = np.zeros_like(Machs)  
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
                        CLift_res,CDrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = calculate_VLM(conditions,settings,geometry)      

                        CLift_d_r[:,:,r_i] = np.reshape(CLift_res,(len_Mach,len_AoA)).T 
                        CDrag_d_r[:,:,r_i] = np.reshape(CDrag_res,(len_Mach,len_AoA)).T                                 
                        CX_d_r[:,:,r_i]    = np.reshape(CX_res,(len_Mach,len_AoA)).T 
                        CY_d_r[:,:,r_i]    = np.reshape(CY_res,(len_Mach,len_AoA)).T 
                        CZ_d_r[:,:,r_i]    = np.reshape(CZ_res,(len_Mach,len_AoA)).T 
                        CL_d_r[:,:,r_i]    = np.reshape(CL_res,(len_Mach,len_AoA)).T 
                        CM_d_r[:,:,r_i]    = np.reshape(CM_res,(len_Mach,len_AoA)).T 
                        CN_d_r[:,:,r_i]    = np.reshape(CN_res,(len_Mach,len_AoA)).T         
                
        # -------------------------------------------------------               
        # Pitch Rate 
        # -------------------------------------------------------       
        CLift_pitch_rate     = np.zeros((len_AoA,len_Mach,len_pitch_rate)) 
        CDrag_pitch_rate     = np.zeros((len_AoA,len_Mach,len_pitch_rate)) 
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
        conditions.stability.dynamic.pitch_rate         = np.zeros_like(Machs)      
        conditions.stability.dynamic.roll_rate          = np.zeros_like(Machs)
        conditions.stability.dynamic.yaw_rate           = np.zeros_like(Machs)  
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        
        for pitch_i in range(len_pitch_rate):  
            conditions.stability.dynamic.pitch_rate[:,0]                 = pitch_rate[pitch_i]  
            CLift_res,CDrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = calculate_VLM(conditions,settings,geometry)  
            CLift_pitch_rate[:,:,pitch_i]     = np.reshape(CLift_res,(len_Mach,len_AoA)).T 
            CDrag_pitch_rate[:,:,pitch_i]     = np.reshape(CDrag_res,(len_Mach,len_AoA)).T 
            CX_pitch_rate[:,:,pitch_i]        = np.reshape(CX_res,(len_Mach,len_AoA)).T  
            CY_pitch_rate[:,:,pitch_i]        = np.reshape(CY_res,(len_Mach,len_AoA)).T  
            CZ_pitch_rate[:,:,pitch_i]        = np.reshape(CZ_res,(len_Mach,len_AoA)).T  
            CL_pitch_rate[:,:,pitch_i]        = np.reshape(CL_res,(len_Mach,len_AoA)).T  
            CM_pitch_rate[:,:,pitch_i]        = np.reshape(CM_res,(len_Mach,len_AoA)).T  
            CN_pitch_rate[:,:,pitch_i]        = np.reshape(CN_res,(len_Mach,len_AoA)).T      
        
    
    
        # -------------------------------------------------------               
        # Roll  Rate 
        # -------------------------------------------------------                                                     
        CLift_roll_rate     = np.zeros((len_AoA,len_Mach,len_roll_rate)) 
        CDrag_roll_rate     = np.zeros((len_AoA,len_Mach,len_roll_rate)) 
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
        conditions.stability.dynamic.pitch_rate         = np.zeros_like(Machs)      
        conditions.stability.dynamic.roll_rate          = np.zeros_like(Machs)
        conditions.stability.dynamic.yaw_rate           = np.zeros_like(Machs)  
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)        
        
        for roll_i in range(len_roll_rate):  
            conditions.stability.dynamic.roll_rate[:,0]                  = roll_rate[roll_i]             
            CLift_res,CDrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = calculate_VLM(conditions,settings,geometry)  
            
            CLift_roll_rate[:,:,roll_i]     = np.reshape(CLift_res,(len_Mach,len_AoA)).T 
            CDrag_roll_rate[:,:,roll_i]     = np.reshape(CDrag_res,(len_Mach,len_AoA)).T 
            CX_roll_rate[:,:,roll_i]        = np.reshape(CX_res,(len_Mach,len_AoA)).T  
            CY_roll_rate[:,:,roll_i]        = np.reshape(CY_res,(len_Mach,len_AoA)).T  
            CZ_roll_rate[:,:,roll_i]        = np.reshape(CZ_res,(len_Mach,len_AoA)).T  
            CL_roll_rate[:,:,roll_i]        = np.reshape(CL_res,(len_Mach,len_AoA)).T  
            CM_roll_rate[:,:,roll_i]        = np.reshape(CM_res,(len_Mach,len_AoA)).T  
            CN_roll_rate[:,:,roll_i]        = np.reshape(CN_res,(len_Mach,len_AoA)).T        
            

        # -------------------------------------------------------               
        # Yaw Rate 
        # -------------------------------------------------------           
        CLift_yaw_rate     = np.zeros((len_Beta,len_Mach,len_yaw_rate)) 
        CDrag_yaw_rate     = np.zeros((len_Beta,len_Mach,len_yaw_rate)) 
        CX_yaw_rate        = np.zeros((len_Beta,len_Mach,len_yaw_rate)) 
        CY_yaw_rate        = np.zeros((len_Beta,len_Mach,len_yaw_rate)) 
        CZ_yaw_rate        = np.zeros((len_Beta,len_Mach,len_yaw_rate)) 
        CL_yaw_rate        = np.zeros((len_Beta,len_Mach,len_yaw_rate)) 
        CM_yaw_rate        = np.zeros((len_Beta,len_Mach,len_yaw_rate)) 
        CN_yaw_rate        = np.zeros((len_Beta,len_Mach,len_yaw_rate))

        # reset conditions         
        conditions                                      = RCAIDE.Framework.Mission.Common.Results()
        conditions.aerodynamics.angles.alpha            = AoAs 
        conditions.freestream.mach_number               = Machs
        conditions.freestream.velocity                  = Machs * 343 # speed of sound  
        conditions.stability.dynamic.pitch_rate         = np.zeros_like(Machs)      
        conditions.stability.dynamic.roll_rate          = np.zeros_like(Machs)
        conditions.stability.dynamic.yaw_rate           = np.zeros_like(Machs)  
        conditions.control_surfaces.elevator.deflection = np.zeros_like(Machs)
        conditions.control_surfaces.aileron.deflection  = np.zeros_like(Machs)
        conditions.control_surfaces.rudder.deflection   = np.zeros_like(Machs)
        
        for yaw_i in range(len_yaw_rate): 
            conditions.stability.dynamic.yaw_rate[:,0]                  = yaw_rate[yaw_i]             
            CLift_res,CDrag_res,CX_res,CY_res,CZ_res,CL_res,CM_res,CN_res = calculate_VLM(conditions,settings,geometry)  
            CLift_yaw_rate[:,:,yaw_i]     = np.reshape(CLift_res,(len_Mach,len_AoA)).T 
            CDrag_yaw_rate[:,:,yaw_i]     = np.reshape(CDrag_res,(len_Mach,len_AoA)).T 
            CX_yaw_rate[:,:,yaw_i]        = np.reshape(CX_res,(len_Mach,len_AoA)).T  
            CY_yaw_rate[:,:,yaw_i]        = np.reshape(CY_res,(len_Mach,len_AoA)).T  
            CZ_yaw_rate[:,:,yaw_i]        = np.reshape(CZ_res,(len_Mach,len_AoA)).T  
            CL_yaw_rate[:,:,yaw_i]        = np.reshape(CL_res,(len_Mach,len_AoA)).T  
            CM_yaw_rate[:,:,yaw_i]        = np.reshape(CM_res,(len_Mach,len_AoA)).T  
            CN_yaw_rate[:,:,yaw_i]        = np.reshape(CN_res,(len_Mach,len_AoA)).T
            
        # Longitudinal Derviatives    
        training.CLift        = CLift  
        training.CDrag        = CDrag
        training.CX_0         = CX_0 
        training.CY_0         = CY_0 
        training.CZ_0         = CZ_0 
        training.CL_0         = CL_0 
        training.CM_0         = CM_0 
        training.CN_0         = CN_0 
        training.dCM_dalpha   = (CM_d_e[0,:,:] - CM_d_e[1,:,:])   / (AoA[0]-AoA[1]) 
        training.dCL_dalpha   = (CLift_d_e[0,:,:] - CLift_d_e[1,:,:])   / (AoA[0]-AoA[1])  
        training.dCL_delta_e  = (CLift_d_e[:,:,0] - CLift_d_e[:,:,1])   /  (delta_e[0]-delta_e[1]) 
        training.dCM_delta_e  = (CM_d_e[:,:,0] - CM_d_e[:,:,1])   / (delta_e[0]-delta_e[1])   
        
        # Lateral Derviatives
        training.dCY_dbeta    = (CY_beta[:,:,0] - CY_beta[:,:,1])   / (Beta[0]-Beta[1])
        training.dCl_dbeta    = -(CL_beta[:,:,0] - CL_beta[:,:,1])   / (Beta[0]-Beta[1])  # negative sign due definition in literature
        training.dCn_dbeta    = (CN_beta[:,:,0] - CN_beta[:,:,1])   / (Beta[0]-Beta[1])
        training.dCY_ddelta_a = (CY_d_a[:,:,0] -  CY_d_a[:,:,1])   / (delta_a[0]-delta_a[1])
        training.dCl_ddelta_a = (CL_d_a[:,:,0] - CL_d_a[:,:,1])   / (delta_a[0]-delta_a[1]) 
        training.dCn_ddelta_a = (CN_d_a[:,:,0] - CN_d_a[:,:,1])   / (delta_a[0]-delta_a[1])
        training.dCY_ddelta_r = (CY_d_r[:,:,0] - CY_d_r[:,:,1])   /  (delta_r[0]-delta_r[1])
        training.dCl_ddelta_r = (CL_d_r[:,:,0] - CL_d_r[:,:,1])   / (delta_r[0]-delta_r[1])
        training.dCn_ddelta_r = -(CN_d_r[:,:,0] - CN_d_r[:,:,1])   / (delta_r[0]-delta_r[1]) # negative sign due definition in literature
        
        #training.dCY_dp      = np.mean((CY_pitch_rate[:,:,0] - CY_pitch_rate[:,:,1])   / (pitch_rate[1]-pitch_rate[0]))
        #training.dCY_dr       = np.mean((CL_d_e[:,:,0] - CL_d_e[:,:,1])   / (AoA[1]-AoA[0]))        
        #training.dCl_dr       = np.mean((CL_d_e[:,:,0] - CL_d_e[:,:,1])   / (AoA[1]-AoA[0]))
        training.dCl_dp       = (CL_roll_rate[:,:,0] - CL_roll_rate[:,:,1])   / (roll_rate[0]-roll_rate[1])
        #training.dCn_dr       = np.mean((CL_d_e[:,:,0] - CL_d_e[:,:,1])   / (AoA[1]-AoA[0]))
        #training.dCn_dp       = np.mean((CN_pitch_rate[:,:,0] - CN_pitch_rate[:,:,1])   / (pitch_rate[1]-pitch_rate[0]))        
        #training.static_margin = -training.dCM_dalpha / training.dCL_dalpha 
        
        
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
        geometry       = self.geometry  
              
        CLift_data          = training.CLift    
        CDrag_data          = training.CDrag     
        dCM_delta_e_data    = training.dCM_delta_e
        dCM_dalpha_data     = training.dCM_dalpha 
        dCL_dalpha_data     = training.dCL_dalpha
        dCL_delta_e_data    = training.dCL_delta_e 
        CX_0_data           = training.CX_0         
        CY_0_data           = training.CY_0         
        CZ_0_data           = training.CZ_0         
        CL_0_data           = training.CL_0         
        CM_0_data           = training.CM_0         
        CN_0_data           = training.CN_0   
        
        dCY_dbeta_data    = training.dCY_dbeta   
        dCl_dbeta_data    = training.dCl_dbeta     
        dCn_dbeta_data    = training.dCn_dbeta     
        dCY_ddelta_a_data = training.dCY_ddelta_a  
        dCl_ddelta_a_data = training.dCl_ddelta_a  
        dCn_ddelta_a_data = training.dCn_ddelta_a  
        dCY_ddelta_r_data = training.dCY_ddelta_r        
        dCl_ddelta_r_data = training.dCl_ddelta_r  
        dCn_ddelta_r_data = training.dCn_ddelta_r 
        dCl_dp_data       = training.dCl_dp
        

        #static_margin       = training.static_margin
        #dCY_dp_data         = training.dCY_dp
        
        # Instantiate surrogates 
        CLift_surrogate       = None 
        CDrag_surrogate       = None  
        dCM_delta_e_surrogate = None
        dCM_dalpha_surrogate  = None
        dCL_dalpha_surrogate  = None
        dCL_delta_e_surrogate = None 
        
        dCY_dbeta_surrogate    = None
        dCl_dbeta_surrogate    = None
        dCn_dbeta_surrogate    = None
        dCY_ddelta_a_surrogate = None
        dCl_ddelta_a_surrogate = None
        dCn_ddelta_a_surrogate = None
        dCY_ddelta_r_surrogate = None
        dCl_ddelta_r_surrogate = None
        dCn_ddelta_r_surrogate = None
        dCl_dp_surrogate        = None
        
        # Do the subsonic surrogates: 
        CLift_surrogate       = RegularGridInterpolator((AoA_data, mach_data),CLift_data,method = 'linear',   bounds_error=False, fill_value=None)   
        CDrag_surrogate       = RegularGridInterpolator((AoA_data, mach_data),CDrag_data,method = 'linear',   bounds_error=False, fill_value=None)    
        dCM_delta_e_surrogate = RegularGridInterpolator((AoA_data, mach_data),dCM_delta_e_data,method = 'linear',   bounds_error=False, fill_value=None)   
        dCM_dalpha_surrogate  = RegularGridInterpolator((AoA_data, mach_data),dCM_dalpha_data,method = 'linear',   bounds_error=False, fill_value=None)    
        dCL_dalpha_surrogate  = RegularGridInterpolator((AoA_data, mach_data),dCL_dalpha_data,method = 'linear',   bounds_error=False, fill_value=None)   
        dCL_delta_e_surrogate = RegularGridInterpolator((AoA_data, mach_data),dCL_delta_e_data ,method = 'linear',   bounds_error=False, fill_value=None)    
        CX_0_surrogate        = RegularGridInterpolator((AoA_data, mach_data),CX_0_data ,method = 'linear',   bounds_error=False, fill_value=None)     
        CY_0_surrogate        = RegularGridInterpolator((AoA_data, mach_data),CY_0_data ,method = 'linear',   bounds_error=False, fill_value=None)     
        CZ_0_surrogate        = RegularGridInterpolator((AoA_data, mach_data),CZ_0_data ,method = 'linear',   bounds_error=False, fill_value=None)     
        CL_0_surrogate        = RegularGridInterpolator((AoA_data, mach_data),CL_0_data ,method = 'linear',   bounds_error=False, fill_value=None)     
        CM_0_surrogate        = RegularGridInterpolator((AoA_data, mach_data),CM_0_data ,method = 'linear',   bounds_error=False, fill_value=None)     
        CN_0_surrogate        = RegularGridInterpolator((AoA_data, mach_data),CN_0_data ,method = 'linear',   bounds_error=False, fill_value=None)
        dCY_dbeta_surrogate   = RegularGridInterpolator((AoA_data,mach_data),dCY_dbeta_data   ,method = 'linear',   bounds_error=False, fill_value=None)
        dCl_dbeta_surrogate   = RegularGridInterpolator((AoA_data,mach_data),dCl_dbeta_data   ,method = 'linear',   bounds_error=False, fill_value=None)
        dCn_dbeta_surrogate   = RegularGridInterpolator((AoA_data,mach_data),dCn_dbeta_data   ,method = 'linear',   bounds_error=False, fill_value=None)
        dCY_ddelta_a_surrogate= RegularGridInterpolator((AoA_data,mach_data),dCY_ddelta_a_data,method = 'linear',   bounds_error=False, fill_value=None)
        dCl_ddelta_a_surrogate= RegularGridInterpolator((AoA_data,mach_data),dCl_ddelta_a_data,method = 'linear',   bounds_error=False, fill_value=None)
        dCn_ddelta_a_surrogate= RegularGridInterpolator((AoA_data,mach_data),dCn_ddelta_a_data,method = 'linear',   bounds_error=False, fill_value=None)
        dCY_ddelta_r_surrogate= RegularGridInterpolator((AoA_data,mach_data),dCY_ddelta_r_data,method = 'linear',   bounds_error=False, fill_value=None)
        dCl_ddelta_r_surrogate= RegularGridInterpolator((AoA_data,mach_data),dCl_ddelta_r_data,method = 'linear',   bounds_error=False, fill_value=None)
        dCn_ddelta_r_surrogate= RegularGridInterpolator((AoA_data,mach_data),dCn_ddelta_r_data,method = 'linear',   bounds_error=False, fill_value=None) 
        dCl_dp_surrogate      = RegularGridInterpolator((AoA_data,mach_data),dCl_dp_data,method = 'linear',   bounds_error=False, fill_value=None)
        
        
        # Pack the outputs
        surrogates.CLift       = CLift_surrogate    
        surrogates.CDrag       = CDrag_surrogate   
        surrogates.dCM_delta_e = dCM_delta_e_surrogate
        surrogates.dCM_dalpha  = dCM_dalpha_surrogate 
        surrogates.dCL_dalpha  = dCL_dalpha_surrogate 
        surrogates.dCL_delta_e = dCL_delta_e_surrogate
        
        surrogates.CX_0 = CX_0_surrogate   
        surrogates.CY_0 = CY_0_surrogate  
        surrogates.CZ_0 = CZ_0_surrogate  
        surrogates.CL_0 = CL_0_surrogate  
        surrogates.CM_0 = CM_0_surrogate  
        surrogates.CN_0 = CN_0_surrogate      
        
        surrogates.dCY_dbeta    = dCY_dbeta_surrogate   
        surrogates.dCl_dbeta    = dCl_dbeta_surrogate   
        surrogates.dCn_dbeta    = dCn_dbeta_surrogate   
        surrogates.dCY_ddelta_a = dCY_ddelta_a_surrogate
        surrogates.dCl_ddelta_a = dCl_ddelta_a_surrogate
        surrogates.dCn_ddelta_a = dCn_ddelta_a_surrogate
        surrogates.dCY_ddelta_r = dCY_ddelta_r_surrogate
        surrogates.dCl_ddelta_r = dCl_ddelta_r_surrogate
        surrogates.dCn_ddelta_r = dCn_ddelta_r_surrogate 
        surrogates.dCl_dp_surrogate = dCl_dp_surrogate
        #surrogates.static_margin= static_margin
        #surrogates.dCY_dp        = dCY_dp_data 
        return

# ----------------------------------------------------------------------
#  Helper Functions
# ----------------------------------------------------------------------
def calculate_VLM(conditions,settings,geometry):
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
    CLift   = results.CL       
    CDrag   = results.CDi      
    CX      = results.CX       
    CY      = results.CY       
    CZ      = results.CZ       
    CL      = results.CL_mom   
    CM      = results.CM       
    CN      = results.CN

    return CLift,CDrag,CX,CY,CZ,CL,CM, CN

