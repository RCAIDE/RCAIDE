## @ingroup  Library-Methods-Aerodynamics-Vortex_Lattice_Method
# RCAIDE/Library/Methods/Aerodynamics/Vortex_Lattice_Method/evaluate_VLM.py
#  
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
import RCAIDE 
from RCAIDE.Framework.Core import  Data 
from RCAIDE.Library.Methods.Aerodynamics.Vortex_Lattice_Method   import VLM
from RCAIDE.Library.Methods.Utilities                            import Cubic_Spline_Blender 

# package imports
import numpy                                                     as np  

# ----------------------------------------------------------------------------------------------------------------------
#  Vortex_Lattice
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Stability  
def evaluate_surrogate(state,settings,geometry):
    """Evaluates surrogates forces and moments using built surrogates 
    
    Assumptions:
        None
        
    Source:
        None

    Args:
        aerodynamics : VLM analysis  [unitless]
        state        : flight conditions     [unitless]
        settings     : VLM analysis settings [unitless]
        geometry     : vehicle configuration [unitless] 
        
    Returns: 
        None  
    """          
    conditions    = state.conditions
    aerodynamics  = state.analyses.aerodynamics
    trim          = aerodynamics.settings.trim_aircraft
    sub_sur       = aerodynamics.surrogates.subsonic
    sup_sur       = aerodynamics.surrogates.supersonic
    trans_sur     = aerodynamics.surrogates.transonic 
    AoA           = np.atleast_2d(conditions.aerodynamics.angles.alpha)  
    Beta          = np.atleast_2d(conditions.aerodynamics.angles.beta)    
    Mach          = np.atleast_2d(conditions.freestream.mach_number)  
     
    # loop through wings to determine what control surfaces are present
    delta_a = np.zeros_like(Mach)
    delta_e = np.zeros_like(Mach)
    delta_r = np.zeros_like(Mach)
    delta_s = np.zeros_like(Mach)
    delta_f = np.zeros_like(Mach)
    
    for wing in geometry.wings: 
        for control_surface in wing.control_surfaces:  
            if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Aileron:
                if trim ==  True: 
                    delta_a        = np.atleast_2d(conditions.control_surfaces.aileron.deflection)
                else:
                    delta_a        = np.ones_like(Mach) * control_surface.deflection  
            if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Elevator: 
                if trim ==  True: 
                    delta_e        = np.atleast_2d(conditions.control_surfaces.elevator.deflection)
                else:  
                    delta_e        = np.ones_like(Mach) * control_surface.deflection
            if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Rudder: 
                if trim ==  True: 
                    delta_r        = np.atleast_2d(conditions.control_surfaces.rudder.deflection)
                else:  
                    delta_r        = np.ones_like(Mach) * control_surface.deflection
            if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Slat:  
                delta_s        = np.ones_like(Mach) * control_surface.deflection
            if type(control_surface) == RCAIDE.Library.Components.Wings.Control_Surfaces.Flap:   
                delta_f        = np.ones_like(Mach) * control_surface.deflection
    
    if np.all((Mach<=1.0) == True): 
        surrogates    = aerodynamics.surrogates.subsonic    
        aerodynamics  = state.analyses.aerodynamics
                    
        # only compute derivative if control surface exists
        if aerodynamics.aileron_flag: 
            pts_delta_a    = np.hstack((delta_a,Mach))
            Clift_delta_a  = np.atleast_2d(surrogates.Clift_delta_a(pts_delta_a)).T
            Cdrag_delta_a  = np.atleast_2d(surrogates.Cdrag_delta_a(pts_delta_a)).T  
            CX_delta_a     = np.atleast_2d(surrogates.CX_delta_a(pts_delta_a)).T 
            CY_delta_a     = np.atleast_2d(surrogates.CY_delta_a(pts_delta_a)).T     
            CZ_delta_a     = np.atleast_2d(surrogates.CZ_delta_a(pts_delta_a)).T     
            CL_delta_a     = np.atleast_2d(surrogates.CL_delta_a(pts_delta_a)).T     
            CM_delta_a     = np.atleast_2d(surrogates.CM_delta_a(pts_delta_a)).T     
            CN_delta_a     = np.atleast_2d(surrogates.CN_delta_a(pts_delta_a)).T  
            
        if aerodynamics.elevator_flag: 
            pts_delta_e    = np.hstack((delta_e,Mach))   
            Clift_delta_e  = np.atleast_2d(surrogates.Clift_delta_e(pts_delta_e)).T  
            Cdrag_delta_e  = np.atleast_2d(surrogates.Cdrag_delta_e(pts_delta_e)).T 
            CX_delta_e     = np.atleast_2d(surrogates.CX_delta_e(pts_delta_e)).T
            CY_delta_e     = np.atleast_2d(surrogates.CY_delta_e(pts_delta_e)).T     
            CZ_delta_e     = np.atleast_2d(surrogates.CZ_delta_e(pts_delta_e)).T     
            CL_delta_e     = np.atleast_2d(surrogates.CL_delta_e(pts_delta_e)).T     
            CM_delta_e     = np.atleast_2d(surrogates.CM_delta_e(pts_delta_e)).T     
            CN_delta_e     = np.atleast_2d(surrogates.CN_delta_e(pts_delta_e)).T  
            
        if aerodynamics.rudder_flag: 
            pts_delta_r    = np.hstack((delta_r,Mach))
            Clift_delta_r  = np.atleast_2d(surrogates.Clift_delta_r(pts_delta_r)).T 
            Cdrag_delta_r  = np.atleast_2d(surrogates.Cdrag_delta_r(pts_delta_r)).T 
            CX_delta_r     = np.atleast_2d(surrogates.CX_delta_r(pts_delta_r)).T
            CY_delta_r     = np.atleast_2d(surrogates.CY_delta_r(pts_delta_r)).T     
            CZ_delta_r     = np.atleast_2d(surrogates.CZ_delta_r(pts_delta_r)).T     
            CL_delta_r     = np.atleast_2d(surrogates.CL_delta_r(pts_delta_r)).T     
            CM_delta_r     = np.atleast_2d(surrogates.CM_delta_r(pts_delta_r)).T     
            CN_delta_r     = np.atleast_2d(surrogates.CN_delta_r(pts_delta_r)).T  
            
        if aerodynamics.flap_flag:   
            pts_delta_f    = np.hstack((delta_f,Mach))   
            Clift_delta_f  = np.atleast_2d(surrogates.Clift_delta_f(pts_delta_f)).T  
            Cdrag_delta_f  = np.atleast_2d(surrogates.Cdrag_delta_f(pts_delta_f)).T 
            CX_delta_f     = np.atleast_2d(surrogates.CX_delta_f(pts_delta_f)).T  
            CY_delta_f     = np.atleast_2d(surrogates.CY_delta_f(pts_delta_f)).T     
            CZ_delta_f     = np.atleast_2d(surrogates.CZ_delta_f(pts_delta_f)).T     
            CL_delta_f     = np.atleast_2d(surrogates.CL_delta_f(pts_delta_f)).T     
            CM_delta_f     = np.atleast_2d(surrogates.CM_delta_f(pts_delta_f)).T     
            CN_delta_f     = np.atleast_2d(surrogates.CN_delta_f(pts_delta_f)).T                
            
        if aerodynamics.slat_flag: 
            pts_delta_s    = np.hstack((delta_s,Mach))        
            Clift_delta_s  = np.atleast_2d(surrogates.Clift_delta_s(pts_delta_s)).T
            Cdrag_delta_s  = np.atleast_2d(surrogates.Cdrag_delta_s(pts_delta_s)).T 
            CX_delta_s     = np.atleast_2d(surrogates.CX_delta_s(pts_delta_s)).T    
            CY_delta_s     = np.atleast_2d(surrogates.CY_delta_s(pts_delta_s)).T     
            CZ_delta_s     = np.atleast_2d(surrogates.CZ_delta_s(pts_delta_s)).T     
            CL_delta_s     = np.atleast_2d(surrogates.CL_delta_s(pts_delta_s)).T     
            CM_delta_s     = np.atleast_2d(surrogates.CM_delta_s(pts_delta_s)).T     
            CN_delta_s     = np.atleast_2d(surrogates.CN_delta_s(pts_delta_s)).T   
    
        u           = np.atleast_2d(conditions.freestream.u)
        v           = np.atleast_2d(conditions.freestream.v)
        w           = np.atleast_2d(conditions.freestream.w)
        p           = np.atleast_2d(conditions.static_stability.roll_rate)        
        q           = np.atleast_2d(conditions.static_stability.pitch_rate)
        r           = np.atleast_2d(conditions.static_stability.yaw_rate)  
    
        # Query surrogates  
        pts_alpha            = np.hstack((AoA,Mach))
        pts_beta             = np.hstack((Beta,Mach))  
        pts_u                = np.hstack((u,Mach))
        pts_v                = np.hstack((v,Mach))
        pts_w                = np.hstack((w,Mach))
        pts_p                = np.hstack((p,Mach))
        pts_q                = np.hstack((q,Mach))
        pts_r                = np.hstack((r,Mach))
         
        # Pack 
        Clift_alpha    = np.atleast_2d(surrogates.Clift_alpha(pts_alpha)).T    
        Cdrag_alpha    = np.atleast_2d(surrogates.Cdrag_alpha(pts_alpha)).T  
         
        Clift_beta     = np.atleast_2d(surrogates.Clift_beta(pts_beta)).T
        Clift_u        = np.atleast_2d(surrogates.Clift_u(pts_u)).T
        Clift_v        = np.atleast_2d(surrogates.Clift_v(pts_v)).T
        Clift_w        = np.atleast_2d(surrogates.Clift_w(pts_w)).T
        Clift_p        = np.atleast_2d(surrogates.Clift_p(pts_p)).T
        Clift_q        = np.atleast_2d(surrogates.Clift_q(pts_q)).T
        Clift_r        = np.atleast_2d(surrogates.Clift_r(pts_r)).T
        Cdrag_beta     = np.atleast_2d(surrogates.Cdrag_beta(pts_beta)).T 
    
        Cdrag_u        = np.atleast_2d(surrogates.Cdrag_u(pts_u)).T
        Cdrag_v        = np.atleast_2d(surrogates.Cdrag_v(pts_v)).T
        Cdrag_w        = np.atleast_2d(surrogates.Cdrag_w(pts_w)).T
        Cdrag_p        = np.atleast_2d(surrogates.Cdrag_p(pts_p)).T
        Cdrag_q        = np.atleast_2d(surrogates.Cdrag_q(pts_q)).T
        Cdrag_r        = np.atleast_2d(surrogates.Cdrag_r(pts_r)).T
        CX_alpha       = np.atleast_2d(surrogates.CX_alpha(pts_alpha)).T
        CX_beta        = np.atleast_2d(surrogates.CX_beta(pts_beta)).T 
        
        CX_u           = np.atleast_2d(surrogates.CX_u(pts_u)).T
        CX_v           = np.atleast_2d(surrogates.CX_v(pts_v)).T
        CX_w           = np.atleast_2d(surrogates.CX_w(pts_w)).T
        CX_p           = np.atleast_2d(surrogates.CX_p(pts_p)).T
        CX_q           = np.atleast_2d(surrogates.CX_q(pts_q)).T
        CX_r           = np.atleast_2d(surrogates.CX_r(pts_r)).T
        CY_alpha       = np.atleast_2d(surrogates.CY_alpha(pts_alpha)).T
        CY_beta        = np.atleast_2d(surrogates.CY_beta(pts_beta)).T
    
        CY_u           = np.atleast_2d(surrogates.CY_u(pts_u)).T
        CY_v           = np.atleast_2d(surrogates.CY_v(pts_v)).T
        CY_w           = np.atleast_2d(surrogates.CY_w(pts_w)).T
        CY_p           = np.atleast_2d(surrogates.CY_p(pts_p)).T
        CY_q           = np.atleast_2d(surrogates.CY_q(pts_q)).T
        CY_r           = np.atleast_2d(surrogates.CY_r(pts_r)).T
        CZ_alpha       = np.atleast_2d(surrogates.CZ_alpha(pts_alpha)).T
        CZ_beta        = np.atleast_2d(surrogates.CZ_beta(pts_beta)).T 
        
        CZ_u           = np.atleast_2d(surrogates.CZ_u(pts_u)).T
        CZ_v           = np.atleast_2d(surrogates.CZ_v(pts_v)).T
        CZ_w           = np.atleast_2d(surrogates.CZ_w(pts_w)).T
        CZ_p           = np.atleast_2d(surrogates.CZ_p(pts_p)).T
        CZ_q           = np.atleast_2d(surrogates.CZ_q(pts_q)).T
        CZ_r           = np.atleast_2d(surrogates.CZ_r(pts_r)).T
        CL_alpha       = np.atleast_2d(surrogates.CL_alpha(pts_alpha)).T
        CL_beta        = np.atleast_2d(surrogates.CL_beta(pts_beta)).T   
        
        CL_u           = np.atleast_2d(surrogates.CL_u(pts_u)).T
        CL_v           = np.atleast_2d(surrogates.CL_v(pts_v)).T
        CL_w           = np.atleast_2d(surrogates.CL_w(pts_w)).T
        CL_p           = np.atleast_2d(surrogates.CL_p(pts_p)).T
        CL_q           = np.atleast_2d(surrogates.CL_q(pts_q)).T
        CL_r           = np.atleast_2d(surrogates.CL_r(pts_r)).T
        CM_alpha       = np.atleast_2d(surrogates.CM_alpha(pts_alpha)).T
        CM_beta        = np.atleast_2d(surrogates.CM_beta(pts_beta)).T 
        
        CM_u           = np.atleast_2d(surrogates.CM_u(pts_u)).T
        CM_v           = np.atleast_2d(surrogates.CM_v(pts_v)).T
        CM_w           = np.atleast_2d(surrogates.CM_w(pts_w)).T
        CM_p           = np.atleast_2d(surrogates.CM_p(pts_p)).T
        CM_q           = np.atleast_2d(surrogates.CM_q(pts_q)).T
        CM_r           = np.atleast_2d(surrogates.CM_r(pts_r)).T
        CN_alpha       = np.atleast_2d(surrogates.CN_alpha(pts_alpha)).T
        CN_beta        = np.atleast_2d(surrogates.CN_beta(pts_beta)).T 
        
        CN_u           = np.atleast_2d(surrogates.CN_u(pts_u)).T
        CN_v           = np.atleast_2d(surrogates.CN_v(pts_v)).T
        CN_w           = np.atleast_2d(surrogates.CN_w(pts_w)).T
        CN_p           = np.atleast_2d(surrogates.CN_p(pts_p)).T
        CN_q           = np.atleast_2d(surrogates.CN_q(pts_q)).T
        CN_r           = np.atleast_2d(surrogates.CN_r(pts_r)).T
    
        # Stability Results  
        conditions.S_ref                                                  = aerodynamics.S_ref              
        conditions.c_ref                                                  = aerodynamics.c_ref              
        conditions.b_ref                                                  = aerodynamics.b_ref
        conditions.X_ref                                                  = aerodynamics.X_ref
        conditions.Y_ref                                                  = aerodynamics.Y_ref
        conditions.Z_ref                                                  = aerodynamics.Z_ref 
        
        conditions.static_stability.coefficients.lift                     = Clift_alpha + Clift_beta + Clift_u + Clift_v + Clift_w + Clift_p + Clift_q + Clift_r 
        conditions.static_stability.coefficients.drag                     = Cdrag_alpha + Cdrag_beta + Cdrag_u + Cdrag_v + Cdrag_w + Cdrag_p + Cdrag_q + Cdrag_r 
        conditions.static_stability.coefficients.X                        = CX_alpha + CX_beta + CX_u + CX_v + CX_w + CX_p + CX_q + CX_r
        conditions.static_stability.coefficients.Y                        = CY_alpha + CY_beta + CY_u + CY_v + CY_w + CY_p + CY_q + CY_r
        conditions.static_stability.coefficients.Z                        = CZ_alpha + CZ_beta + CZ_u + CZ_v + CZ_w + CZ_p + CZ_q + CZ_r
        conditions.static_stability.coefficients.L                        = CL_alpha + CL_beta + CL_u + CL_v + CL_w + CL_p + CL_q + CL_r
        conditions.static_stability.coefficients.M                        = CM_alpha + CM_beta + CM_u + CM_v + CM_w + CM_p + CM_q + CM_r
        conditions.static_stability.coefficients.N                        = CN_alpha + CN_beta + CN_u + CN_v + CN_w + CN_p + CN_q + CN_r
        
        if aerodynamics.aileron_flag: 
            conditions.static_stability.coefficients.lift += Clift_delta_a
            conditions.static_stability.coefficients.drag += Cdrag_delta_a
            conditions.static_stability.coefficients.X    += CX_delta_a 
            conditions.static_stability.coefficients.Y    += CY_delta_a
            conditions.static_stability.coefficients.Z    += CZ_delta_a
            conditions.static_stability.coefficients.L    += CL_delta_a
            conditions.static_stability.coefficients.M    += CM_delta_a
            conditions.static_stability.coefficients.N    += CN_delta_a 
    
            conditions.control_surfaces.aileron.static_stability.coefficients.lift       = Clift_delta_a         
            conditions.control_surfaces.aileron.static_stability.coefficients.drag       = Cdrag_delta_a            
            conditions.control_surfaces.aileron.static_stability.coefficients.X          = CX_delta_a             
            conditions.control_surfaces.aileron.static_stability.coefficients.Y          = CY_delta_a            
            conditions.control_surfaces.aileron.static_stability.coefficients.Z          = CZ_delta_a          
            conditions.control_surfaces.aileron.static_stability.coefficients.L          = CL_delta_a          
            conditions.control_surfaces.aileron.static_stability.coefficients.M          = CM_delta_a          
            conditions.control_surfaces.aileron.static_stability.coefficients.N          = CN_delta_a             
            
        if aerodynamics.elevator_flag: 
            conditions.static_stability.coefficients.lift += Clift_delta_e
            conditions.static_stability.coefficients.drag += Cdrag_delta_e
            conditions.static_stability.coefficients.X    += CX_delta_e 
            conditions.static_stability.coefficients.Y    += CY_delta_e
            conditions.static_stability.coefficients.Z    += CZ_delta_e
            conditions.static_stability.coefficients.L    += CL_delta_e
            conditions.static_stability.coefficients.M    += CM_delta_e
            conditions.static_stability.coefficients.N    += CN_delta_e
            
            conditions.control_surfaces.elevator.static_stability.coefficients.lift       = Clift_delta_e         
            conditions.control_surfaces.elevator.static_stability.coefficients.drag       = Cdrag_delta_e            
            conditions.control_surfaces.elevator.static_stability.coefficients.X          = CX_delta_e             
            conditions.control_surfaces.elevator.static_stability.coefficients.Y          = CY_delta_e            
            conditions.control_surfaces.elevator.static_stability.coefficients.Z          = CZ_delta_e          
            conditions.control_surfaces.elevator.static_stability.coefficients.L          = CL_delta_e          
            conditions.control_surfaces.elevator.static_stability.coefficients.M          = CM_delta_e          
            conditions.control_surfaces.elevator.static_stability.coefficients.N          = CN_delta_e            
            
        if aerodynamics.rudder_flag:  
            conditions.static_stability.coefficients.lift += Clift_delta_r
            conditions.static_stability.coefficients.drag += Cdrag_delta_r
            conditions.static_stability.coefficients.X    += CX_delta_r 
            conditions.static_stability.coefficients.Y    += CY_delta_r
            conditions.static_stability.coefficients.Z    += CZ_delta_r
            conditions.static_stability.coefficients.L    += CL_delta_r
            conditions.static_stability.coefficients.M    += CM_delta_r
            conditions.static_stability.coefficients.N    += CN_delta_r
    
            conditions.control_surfaces.rudder.static_stability.coefficients.lift       = Clift_delta_r         
            conditions.control_surfaces.rudder.static_stability.coefficients.drag       = Cdrag_delta_r            
            conditions.control_surfaces.rudder.static_stability.coefficients.X          = CX_delta_r             
            conditions.control_surfaces.rudder.static_stability.coefficients.Y          = CY_delta_r            
            conditions.control_surfaces.rudder.static_stability.coefficients.Z          = CZ_delta_r          
            conditions.control_surfaces.rudder.static_stability.coefficients.L          = CL_delta_r          
            conditions.control_surfaces.rudder.static_stability.coefficients.M          = CM_delta_r          
            conditions.control_surfaces.rudder.static_stability.coefficients.N          = CN_delta_r         
            
        if aerodynamics.flap_flag:
            conditions.static_stability.coefficients.lift += Clift_delta_f
            conditions.static_stability.coefficients.drag += Cdrag_delta_f
            conditions.static_stability.coefficients.X    += CX_delta_f 
            conditions.static_stability.coefficients.Y    += CY_delta_f
            conditions.static_stability.coefficients.Z    += CZ_delta_f
            conditions.static_stability.coefficients.L    += CL_delta_f
            conditions.static_stability.coefficients.M    += CM_delta_f
            conditions.static_stability.coefficients.N    += CN_delta_f
            
    
            conditions.control_surfaces.flap.static_stability.coefficients.lift       = Clift_delta_f         
            conditions.control_surfaces.flap.static_stability.coefficients.drag       = Cdrag_delta_f            
            conditions.control_surfaces.flap.static_stability.coefficients.X          = CX_delta_f             
            conditions.control_surfaces.flap.static_stability.coefficients.Y          = CY_delta_f            
            conditions.control_surfaces.flap.static_stability.coefficients.Z          = CZ_delta_f          
            conditions.control_surfaces.flap.static_stability.coefficients.L          = CL_delta_f          
            conditions.control_surfaces.flap.static_stability.coefficients.M          = CM_delta_f          
            conditions.control_surfaces.flap.static_stability.coefficients.N          = CN_delta_f           
            
    
        if aerodynamics.slat_flag: 
            conditions.static_stability.coefficients.lift += Clift_delta_s
            conditions.static_stability.coefficients.drag += Cdrag_delta_s
            conditions.static_stability.coefficients.X    += CX_delta_s 
            conditions.static_stability.coefficients.Y    += CY_delta_s
            conditions.static_stability.coefficients.Z    += CZ_delta_s
            conditions.static_stability.coefficients.L    += CL_delta_s
            conditions.static_stability.coefficients.M    += CM_delta_s
            conditions.static_stability.coefficients.N    += CN_delta_s
    
            conditions.control_surfaces.slat.static_stability.coefficients.lift       = Clift_delta_s         
            conditions.control_surfaces.slat.static_stability.coefficients.drag       = Cdrag_delta_s            
            conditions.control_surfaces.slat.static_stability.coefficients.X          = CX_delta_s             
            conditions.control_surfaces.slat.static_stability.coefficients.Y          = CY_delta_s            
            conditions.control_surfaces.slat.static_stability.coefficients.Z          = CZ_delta_s          
            conditions.control_surfaces.slat.static_stability.coefficients.L          = CL_delta_s          
            conditions.control_surfaces.slat.static_stability.coefficients.M          = CM_delta_s          
            conditions.control_surfaces.slat.static_stability.coefficients.N          = CN_delta_s                     
         
        
        conditions.static_stability.derivatives.Clift_alpha               = surrogates.dClift_dalpha(Mach)
        conditions.static_stability.derivatives.CY_alpha                  = surrogates.dCY_dalpha(Mach)
        conditions.static_stability.derivatives.CL_alpha                  = surrogates.dCL_dalpha(Mach)
        conditions.static_stability.derivatives.CM_alpha                  = surrogates.dCM_dalpha(Mach)
        conditions.static_stability.derivatives.CN_alpha                  = surrogates.dCN_dalpha(Mach)
        conditions.static_stability.derivatives.Clift_beta                = surrogates.dClift_dbeta(Mach)
        conditions.static_stability.derivatives.CY_beta                   = surrogates.dCY_dbeta(Mach)
        conditions.static_stability.derivatives.CL_beta                   = surrogates.dCL_dbeta(Mach)
        conditions.static_stability.derivatives.CM_beta                   = surrogates.dCM_dbeta(Mach)
        conditions.static_stability.derivatives.CN_beta                   = surrogates.dCN_dbeta(Mach)
        conditions.static_stability.derivatives.Clift_p                   = surrogates.dClift_dp(Mach)
        conditions.static_stability.derivatives.Clift_q                   = surrogates.dClift_dq(Mach)
        conditions.static_stability.derivatives.Clift_r                   = surrogates.dClift_dr(Mach)
        
        conditions.static_stability.derivatives.CX_u                      = surrogates.dCX_du(Mach)
        conditions.static_stability.derivatives.CX_v                      = surrogates.dCX_dv(Mach)
        conditions.static_stability.derivatives.CX_w                      = surrogates.dCX_dw(Mach)
        conditions.static_stability.derivatives.CY_u                      = surrogates.dCY_du(Mach)
        conditions.static_stability.derivatives.CY_v                      = surrogates.dCY_dv(Mach)
        conditions.static_stability.derivatives.CY_w                      = surrogates.dCY_dw(Mach)
        conditions.static_stability.derivatives.CZ_u                      = surrogates.dCZ_du(Mach)
        conditions.static_stability.derivatives.CZ_v                      = surrogates.dCZ_dv(Mach)
        conditions.static_stability.derivatives.CZ_w                      = surrogates.dCZ_dw(Mach)
        conditions.static_stability.derivatives.CL_u                      = surrogates.dCL_du(Mach)
        conditions.static_stability.derivatives.CL_v                      = surrogates.dCL_dv(Mach)
        conditions.static_stability.derivatives.CL_w                      = surrogates.dCL_dw(Mach)
        conditions.static_stability.derivatives.CM_u                      = surrogates.dCM_du(Mach)
        conditions.static_stability.derivatives.CM_v                      = surrogates.dCM_dv(Mach)
        conditions.static_stability.derivatives.CM_w                      = surrogates.dCM_dw(Mach)
        conditions.static_stability.derivatives.CN_u                      = surrogates.dCN_du(Mach)
        conditions.static_stability.derivatives.CN_v                      = surrogates.dCN_dv(Mach)
        conditions.static_stability.derivatives.CN_w                      = surrogates.dCN_dw(Mach)
        
        conditions.static_stability.derivatives.CX_p                      = surrogates.dCX_dp(Mach)
        conditions.static_stability.derivatives.CX_q                      = surrogates.dCX_dq(Mach)
        conditions.static_stability.derivatives.CX_r                      = surrogates.dCX_dr(Mach)
        conditions.static_stability.derivatives.CY_p                      = surrogates.dCY_dp(Mach)
        conditions.static_stability.derivatives.CY_q                      = surrogates.dCY_dq(Mach)
        conditions.static_stability.derivatives.CY_r                      = surrogates.dCY_dr(Mach)
        conditions.static_stability.derivatives.CZ_p                      = surrogates.dCZ_dp(Mach)
        conditions.static_stability.derivatives.CZ_q                      = surrogates.dCZ_dq(Mach)
        conditions.static_stability.derivatives.CZ_r                      = surrogates.dCZ_dr(Mach)
        conditions.static_stability.derivatives.CL_p                      = surrogates.dCL_dp(Mach)
        conditions.static_stability.derivatives.CL_q                      = surrogates.dCL_dq(Mach)
        conditions.static_stability.derivatives.CL_r                      = surrogates.dCL_dr(Mach)
        conditions.static_stability.derivatives.CM_p                      = surrogates.dCM_dp(Mach)
        conditions.static_stability.derivatives.CM_q                      = surrogates.dCM_dq(Mach)
        conditions.static_stability.derivatives.CM_r                      = surrogates.dCM_dr(Mach)
        conditions.static_stability.derivatives.CN_p                      = surrogates.dCN_dp(Mach)
        conditions.static_stability.derivatives.CN_q                      = surrogates.dCN_dq(Mach)
        conditions.static_stability.derivatives.CN_r                      = surrogates.dCN_dr(Mach)
        #conditions.static_stability.neutral_point                         = # Need to Update
        #conditions.static_stability.spiral_criteria                       = # Need to Update
        
        for wing in geometry.wings: 
            inviscid_wing_lifts = np.atleast_2d(surrogates.Clift_wing_alpha[wing.tag](pts_alpha)).T
            inviscid_wing_drags = np.atleast_2d(surrogates.Cdrag_wing_alpha[wing.tag](pts_alpha)).T
            # Pack 
            conditions.aerodynamics.coefficients.lift.inviscid_wings[wing.tag]         = inviscid_wing_lifts 
            conditions.aerodynamics.coefficients.lift.compressible_wings[wing.tag]     = inviscid_wing_lifts 
            conditions.aerodynamics.coefficients.drag.induced.inviscid_wings[wing.tag] = inviscid_wing_drags 
        
    else: 
        geometry      = aerodynamics.geometry 
        hsub_min      = aerodynamics.hsub_min
        hsub_max      = aerodynamics.hsub_max
        hsup_min      = aerodynamics.hsup_min
        hsup_max      = aerodynamics.hsup_max
    
        # Spline for Subsonic-to-Transonic-to-Supersonic Regimes
        sub_trans_spline = Cubic_Spline_Blender(hsub_min,hsub_max)
        h_sub            = lambda M:sub_trans_spline.compute(M)          
        sup_trans_spline = Cubic_Spline_Blender(hsup_max, hsup_min) 
        h_sup            = lambda M:sup_trans_spline.compute(M)    
     
        # only compute derivative if control surface exists
        if aerodynamics.aileron_flag:  
            pts_delta_a    = np.hstack((delta_a,Mach))
            
            results_delta_a =  compute_coefficients(sub_sur.Clift_delta_a,sub_sur.Cdrag_delta_a,sub_sur.CX_delta_a,sub_sur.CY_delta_a,sub_sur.CZ_delta_a,sub_sur.CL_delta_a,sub_sur.CM_delta_a, sub_sur.CN_delta_a,
             trans_sur.Clift_delta_a,trans_sur.Cdrag_delta_a,trans_sur.CX_delta_a,trans_sur.CY_delta_a,trans_sur.CZ_delta_a,trans_sur.CL_delta_a,trans_sur.CM_delta_a, trans_sur.CN_delta_a,
             sup_sur.Clift_delta_a,sup_sur.Cdrag_delta_a,sup_sur.CX_delta_a,sup_sur.CY_delta_a,sup_sur.CZ_delta_a,sup_sur.CL_delta_a,sup_sur.CM_delta_a, sup_sur.CN_delta_a,
            h_sub,h_sup,Mach, pts_delta_a)
             
            Clift_delta_a   = results_delta_a.Clift   
            Cdrag_delta_a   = results_delta_a.Cdrag   
            CX_delta_a      = results_delta_a.CX      
            CY_delta_a      = results_delta_a.CY      
            CZ_delta_a      = results_delta_a.CZ      
            CL_delta_a      = results_delta_a.CL      
            CM_delta_a      = results_delta_a.CM      
            CN_delta_a      = results_delta_a.CN      
               
             
        if aerodynamics.elevator_flag: 
            pts_delta_e    = np.hstack((delta_e,Mach))

            results_delta_e =  compute_coefficients(sub_sur.Clift_delta_e,sub_sur.Cdrag_delta_e,sub_sur.CX_delta_e,sub_sur.CY_delta_e,sub_sur.CZ_delta_e,sub_sur.CL_delta_e,sub_sur.CM_delta_e, sub_sur.CN_delta_e,
             trans_sur.Clift_delta_e,trans_sur.Cdrag_delta_e,trans_sur.CX_delta_e,trans_sur.CY_delta_e,trans_sur.CZ_delta_e,trans_sur.CL_delta_e,trans_sur.CM_delta_e, trans_sur.CN_delta_e,
             sup_sur.Clift_delta_e,sup_sur.Cdrag_delta_e,sup_sur.CX_delta_e,sup_sur.CY_delta_e,sup_sur.CZ_delta_e,sup_sur.CL_delta_e,sup_sur.CM_delta_e, sup_sur.CN_delta_e,
            h_sub,h_sup,Mach, pts_delta_e)
             
            Clift_delta_e   = results_delta_e.Clift   
            Cdrag_delta_e   = results_delta_e.Cdrag   
            CX_delta_e      = results_delta_e.CX      
            CY_delta_e      = results_delta_e.CY      
            CZ_delta_e      = results_delta_e.CZ      
            CL_delta_e      = results_delta_e.CL      
            CM_delta_e      = results_delta_e.CM      
            CN_delta_e      = results_delta_e.CN
            
        if aerodynamics.rudder_flag: 
            pts_delta_r    = np.hstack((delta_r,Mach))
            
            results_delta_r =  compute_coefficients(sub_sur.Clift_delta_r,sub_sur.Cdrag_delta_r,sub_sur.CX_delta_r,sub_sur.CY_delta_r,sub_sur.CZ_delta_r,sub_sur.CL_delta_r,sub_sur.CM_delta_r, sub_sur.CN_delta_r,
             trans_sur.Clift_delta_r,trans_sur.Cdrag_delta_r,trans_sur.CX_delta_r,trans_sur.CY_delta_r,trans_sur.CZ_delta_r,trans_sur.CL_delta_r,trans_sur.CM_delta_r, trans_sur.CN_delta_r,
             sup_sur.Clift_delta_r,sup_sur.Cdrag_delta_r,sup_sur.CX_delta_r,sup_sur.CY_delta_r,sup_sur.CZ_delta_r,sup_sur.CL_delta_r,sup_sur.CM_delta_r, sup_sur.CN_delta_r,
            h_sub,h_sup,Mach, pts_delta_r)
             
            Clift_delta_r   = results_delta_r.Clift   
            Cdrag_delta_r   = results_delta_r.Cdrag   
            CX_delta_r      = results_delta_r.CX      
            CY_delta_r      = results_delta_r.CY      
            CZ_delta_r      = results_delta_r.CZ      
            CL_delta_r      = results_delta_r.CL      
            CM_delta_r      = results_delta_r.CM      
            CN_delta_r      = results_delta_r.CN 
                          
        if aerodynamics.flap_flag:   
            pts_delta_f    = np.hstack((delta_f,Mach))
            
            results_delta_f =  compute_coefficients(sub_sur.Clift_delta_f,sub_sur.Cdrag_delta_f,sub_sur.CX_delta_f,sub_sur.CY_delta_f,sub_sur.CZ_delta_f,sub_sur.CL_delta_f,sub_sur.CM_delta_f, sub_sur.CN_delta_f,
             trans_sur.Clift_delta_f,trans_sur.Cdrag_delta_f,trans_sur.CX_delta_f,trans_sur.CY_delta_f,trans_sur.CZ_delta_f,trans_sur.CL_delta_f,trans_sur.CM_delta_f, trans_sur.CN_delta_f,
             sup_sur.Clift_delta_f,sup_sur.Cdrag_delta_f,sup_sur.CX_delta_f,sup_sur.CY_delta_f,sup_sur.CZ_delta_f,sup_sur.CL_delta_f,sup_sur.CM_delta_f, sup_sur.CN_delta_f,
            h_sub,h_sup,Mach, pts_delta_f)
             
            Clift_delta_f   = results_delta_f.Clift   
            Cdrag_delta_f   = results_delta_f.Cdrag   
            CX_delta_f      = results_delta_f.CX      
            CY_delta_f      = results_delta_f.CY      
            CZ_delta_f      = results_delta_f.CZ      
            CL_delta_f      = results_delta_f.CL      
            CM_delta_f      = results_delta_f.CM      
            CN_delta_f      = results_delta_f.CN
                         
        if aerodynamics.slat_flag: 
            pts_delta_s    = np.hstack((delta_s,Mach)) 
            
            results_delta_s =  compute_coefficients(sub_sur.Clift_delta_s,sub_sur.Cdrag_delta_s,sub_sur.CX_delta_s,sub_sur.CY_delta_s,sub_sur.CZ_delta_s,sub_sur.CL_delta_s,sub_sur.CM_delta_s, sub_sur.CN_delta_s,
             trans_sur.Clift_delta_s,trans_sur.Cdrag_delta_s,trans_sur.CX_delta_s,trans_sur.CY_delta_s,trans_sur.CZ_delta_s,trans_sur.CL_delta_s,trans_sur.CM_delta_s, trans_sur.CN_delta_s,
             sup_sur.Clift_delta_s,sup_sur.Cdrag_delta_s,sup_sur.CX_delta_s,sup_sur.CY_delta_s,sup_sur.CZ_delta_s,sup_sur.CL_delta_s,sup_sur.CM_delta_s, sup_sur.CN_delta_s,
            h_sub,h_sup,Mach, pts_delta_s)
             
            Clift_delta_s   = results_delta_s.Clift   
            Cdrag_delta_s   = results_delta_s.Cdrag   
            CX_delta_s      = results_delta_s.CX      
            CY_delta_s      = results_delta_s.CY      
            CZ_delta_s      = results_delta_s.CZ      
            CL_delta_s      = results_delta_s.CL      
            CM_delta_s      = results_delta_s.CM      
            CN_delta_s      = results_delta_s.CN
             
        u           = np.atleast_2d(conditions.freestream.u)
        v           = np.atleast_2d(conditions.freestream.v)
        w           = np.atleast_2d(conditions.freestream.w)
        p           = np.atleast_2d(conditions.static_stability.roll_rate)        
        q           = np.atleast_2d(conditions.static_stability.pitch_rate)
        r           = np.atleast_2d(conditions.static_stability.yaw_rate)  
    
        # Query surrogates  
        pts_alpha            = np.hstack((AoA,Mach))
        pts_beta             = np.hstack((Beta,Mach))  
        pts_u                = np.hstack((u,Mach))
        pts_v                = np.hstack((v,Mach))
        pts_w                = np.hstack((w,Mach))
        pts_p                = np.hstack((p,Mach))
        pts_q                = np.hstack((q,Mach))
        pts_r                = np.hstack((r,Mach))
        
        # Alpha 
        results_alpha    = compute_coefficients( sub_sur.Clift_alpha,  sub_sur.Cdrag_alpha,  sub_sur.CX_alpha,  sub_sur.CY_alpha,  sub_sur.CZ_alpha,  sub_sur.CL_alpha,  sub_sur.CM_alpha,   sub_sur.CN_alpha,
                                               trans_sur.Clift_alpha,trans_sur.Cdrag_alpha,trans_sur.CX_alpha,trans_sur.CY_alpha,trans_sur.CZ_alpha,trans_sur.CL_alpha,trans_sur.CM_alpha, trans_sur.CN_alpha,
                                                 sup_sur.Clift_alpha,  sup_sur.Cdrag_alpha,  sup_sur.CX_alpha,  sup_sur.CY_alpha,  sup_sur.CZ_alpha,  sup_sur.CL_alpha,  sup_sur.CM_alpha,   sup_sur.CN_alpha,
                                                  h_sub,h_sup,Mach, pts_alpha)        

        Clift_alpha    = results_alpha.Clift   
        Cdrag_alpha    = results_alpha.Cdrag   
        CX_alpha       = results_alpha.CX      
        CY_alpha       = results_alpha.CY      
        CZ_alpha       = results_alpha.CZ      
        CL_alpha       = results_alpha.CL      
        CM_alpha       = results_alpha.CM      
        CN_alpha       = results_alpha.CN         
         
        # Beta 
        results_beta =  compute_coefficients(sub_sur.Clift_beta,  sub_sur.Cdrag_beta,  sub_sur.CX_beta,  sub_sur.CY_beta,  sub_sur.CZ_beta,  sub_sur.CL_beta,  sub_sur.CM_beta,   sub_sur.CN_beta,
                                           trans_sur.Clift_beta,trans_sur.Cdrag_beta,trans_sur.CX_beta,trans_sur.CY_beta,trans_sur.CZ_beta,trans_sur.CL_beta,trans_sur.CM_beta, trans_sur.CN_beta,
                                             sup_sur.Clift_beta,  sup_sur.Cdrag_beta,  sup_sur.CX_beta,  sup_sur.CY_beta,  sup_sur.CZ_beta,  sup_sur.CL_beta,  sup_sur.CM_beta,   sup_sur.CN_beta,
                                             h_sub,h_sup,Mach, pts_beta)
         
        Clift_beta   = results_beta.Clift   
        Cdrag_beta   = results_beta.Cdrag   
        CX_beta      = results_beta.CX      
        CY_beta      = results_beta.CY      
        CZ_beta      = results_beta.CZ      
        CL_beta      = results_beta.CL      
        CM_beta      = results_beta.CM      
        CN_beta      = results_beta.CN 

        # u  
        results_u    =  compute_coefficients(sub_sur.Clift_u,  sub_sur.Cdrag_u,  sub_sur.CX_u,  sub_sur.CY_u,  sub_sur.CZ_u,  sub_sur.CL_u,  sub_sur.CM_u,   sub_sur.CN_u,
                                           trans_sur.Clift_u,trans_sur.Cdrag_u,trans_sur.CX_u,trans_sur.CY_u,trans_sur.CZ_u,trans_sur.CL_u,trans_sur.CM_u, trans_sur.CN_u,
                                             sup_sur.Clift_u,  sup_sur.Cdrag_u,  sup_sur.CX_u,  sup_sur.CY_u,  sup_sur.CZ_u,  sup_sur.CL_u,  sup_sur.CM_u,   sup_sur.CN_u,
                                             h_sub,h_sup,Mach, pts_u)
         
        Clift_u   = results_u.Clift   
        Cdrag_u   = results_u.Cdrag   
        CX_u      = results_u.CX      
        CY_u      = results_u.CY      
        CZ_u      = results_u.CZ      
        CL_u      = results_u.CL      
        CM_u      = results_u.CM      
        CN_u      = results_u.CN          

        # v  
        results_v    =  compute_coefficients(sub_sur.Clift_v,  sub_sur.Cdrag_v,  sub_sur.CX_v,  sub_sur.CY_v,  sub_sur.CZ_v,  sub_sur.CL_v,  sub_sur.CM_v,   sub_sur.CN_v,
                                           trans_sur.Clift_v,trans_sur.Cdrag_v,trans_sur.CX_v,trans_sur.CY_v,trans_sur.CZ_v,trans_sur.CL_v,trans_sur.CM_v, trans_sur.CN_v,
                                             sup_sur.Clift_v,  sup_sur.Cdrag_v,  sup_sur.CX_v,  sup_sur.CY_v,  sup_sur.CZ_v,  sup_sur.CL_v,  sup_sur.CM_v,   sup_sur.CN_v,
                                             h_sub,h_sup,Mach, pts_v)
         
        Clift_v   = results_v.Clift   
        Cdrag_v   = results_v.Cdrag   
        CX_v      = results_v.CX      
        CY_v      = results_v.CY      
        CZ_v      = results_v.CZ      
        CL_v      = results_v.CL      
        CM_v      = results_v.CM      
        CN_v      = results_v.CN       

        # w  
        results_w    =  compute_coefficients(sub_sur.Clift_w,  sub_sur.Cdrag_w,  sub_sur.CX_w,  sub_sur.CY_w,  sub_sur.CZ_w,  sub_sur.CL_w,  sub_sur.CM_w,   sub_sur.CN_w,
                                           trans_sur.Clift_w,trans_sur.Cdrag_w,trans_sur.CX_w,trans_sur.CY_w,trans_sur.CZ_w,trans_sur.CL_w,trans_sur.CM_w, trans_sur.CN_w,
                                             sup_sur.Clift_w,  sup_sur.Cdrag_w,  sup_sur.CX_w,  sup_sur.CY_w,  sup_sur.CZ_w,  sup_sur.CL_w,  sup_sur.CM_w,   sup_sur.CN_w,
                                            h_sub,h_sup,Mach, pts_w)
         
        Clift_w   = results_w.Clift   
        Cdrag_w   = results_w.Cdrag   
        CX_w      = results_w.CX      
        CY_w      = results_w.CY      
        CZ_w      = results_w.CZ      
        CL_w      = results_w.CL      
        CM_w      = results_w.CM      
        CN_w      = results_w.CN
        

        # p  
        results_p    =  compute_coefficients(sub_sur.Clift_p,  sub_sur.Cdrag_p,  sub_sur.CX_p,  sub_sur.CY_p,  sub_sur.CZ_p,  sub_sur.CL_p,  sub_sur.CM_p,   sub_sur.CN_p,
                                           trans_sur.Clift_p,trans_sur.Cdrag_p,trans_sur.CX_p,trans_sur.CY_p,trans_sur.CZ_p,trans_sur.CL_p,trans_sur.CM_p, trans_sur.CN_p,
                                             sup_sur.Clift_p,  sup_sur.Cdrag_p,  sup_sur.CX_p,  sup_sur.CY_p,  sup_sur.CZ_p,  sup_sur.CL_p,  sup_sur.CM_p,   sup_sur.CN_p,
                                            h_sub,h_sup,Mach, pts_p)
         
        Clift_p   = results_p.Clift   
        Cdrag_p   = results_p.Cdrag   
        CX_p      = results_p.CX      
        CY_p      = results_p.CY      
        CZ_p      = results_p.CZ      
        CL_p      = results_p.CL      
        CM_p      = results_p.CM      
        CN_p      = results_p.CN
         

        # q  
        results_q    =  compute_coefficients(sub_sur.Clift_q,  sub_sur.Cdrag_q,  sub_sur.CX_q,  sub_sur.CY_q,  sub_sur.CZ_q,  sub_sur.CL_q,  sub_sur.CM_q,   sub_sur.CN_q,
                                           trans_sur.Clift_q,trans_sur.Cdrag_q,trans_sur.CX_q,trans_sur.CY_q,trans_sur.CZ_q,trans_sur.CL_q,trans_sur.CM_q, trans_sur.CN_q,
                                             sup_sur.Clift_q,  sup_sur.Cdrag_q,  sup_sur.CX_q,  sup_sur.CY_q,  sup_sur.CZ_q,  sup_sur.CL_q,  sup_sur.CM_q,   sup_sur.CN_q,
                                            h_sub,h_sup,Mach, pts_q)
         
        Clift_q   = results_q.Clift   
        Cdrag_q   = results_q.Cdrag   
        CX_q      = results_q.CX      
        CY_q      = results_q.CY      
        CZ_q      = results_q.CZ      
        CL_q      = results_q.CL      
        CM_q      = results_q.CM      
        CN_q      = results_q.CN
        
        # r  
        results_r    =  compute_coefficients(sub_sur.Clift_r,  sub_sur.Cdrag_r,  sub_sur.CX_r,  sub_sur.CY_r,  sub_sur.CZ_r,  sub_sur.CL_r,  sub_sur.CM_r,   sub_sur.CN_r,
                                           trans_sur.Clift_r,trans_sur.Cdrag_r,trans_sur.CX_r,trans_sur.CY_r,trans_sur.CZ_r,trans_sur.CL_r,trans_sur.CM_r, trans_sur.CN_r,
                                             sup_sur.Clift_r,  sup_sur.Cdrag_r,  sup_sur.CX_r,  sup_sur.CY_r,  sup_sur.CZ_r,  sup_sur.CL_r,  sup_sur.CM_r,   sup_sur.CN_r,
                                            h_sub,h_sup,Mach, pts_r)
         
        Clift_r   = results_r.Clift   
        Cdrag_r   = results_r.Cdrag   
        CX_r      = results_r.CX      
        CY_r      = results_r.CY      
        CZ_r      = results_r.CZ      
        CL_r      = results_r.CL      
        CM_r      = results_r.CM      
        CN_r      = results_r.CN 
    
        # Stability Results  
        conditions.S_ref                                                  = aerodynamics.S_ref              
        conditions.c_ref                                                  = aerodynamics.c_ref              
        conditions.b_ref                                                  = aerodynamics.b_ref
        conditions.X_ref                                                  = aerodynamics.X_ref
        conditions.Y_ref                                                  = aerodynamics.Y_ref
        conditions.Z_ref                                                  = aerodynamics.Z_ref 
        
        conditions.static_stability.coefficients.lift                     = Clift_alpha + Clift_beta + Clift_u + Clift_v + Clift_w + Clift_p + Clift_q + Clift_r 
        conditions.static_stability.coefficients.drag                     = Cdrag_alpha + Cdrag_beta + Cdrag_u + Cdrag_v + Cdrag_w + Cdrag_p + Cdrag_q + Cdrag_r 
        conditions.static_stability.coefficients.X                        = CX_alpha + CX_beta + CX_u + CX_v + CX_w + CX_p + CX_q + CX_r
        conditions.static_stability.coefficients.Y                        = CY_alpha + CY_beta + CY_u + CY_v + CY_w + CY_p + CY_q + CY_r
        conditions.static_stability.coefficients.Z                        = CZ_alpha + CZ_beta + CZ_u + CZ_v + CZ_w + CZ_p + CZ_q + CZ_r
        conditions.static_stability.coefficients.L                        = CL_alpha + CL_beta + CL_u + CL_v + CL_w + CL_p + CL_q + CL_r
        conditions.static_stability.coefficients.M                        = CM_alpha + CM_beta + CM_u + CM_v + CM_w + CM_p + CM_q + CM_r
        conditions.static_stability.coefficients.N                        = CN_alpha + CN_beta + CN_u + CN_v + CN_w + CN_p + CN_q + CN_r
        
        if aerodynamics.aileron_flag: 
            conditions.static_stability.coefficients.lift += Clift_delta_a
            conditions.static_stability.coefficients.drag += Cdrag_delta_a
            conditions.static_stability.coefficients.X    += CX_delta_a 
            conditions.static_stability.coefficients.Y    += CY_delta_a
            conditions.static_stability.coefficients.Z    += CZ_delta_a
            conditions.static_stability.coefficients.L    += CL_delta_a
            conditions.static_stability.coefficients.M    += CM_delta_a
            conditions.static_stability.coefficients.N    += CN_delta_a
            
    
            conditions.control_surfaces.aileron.static_stability.coefficients.lift       = Clift_delta_a         
            conditions.control_surfaces.aileron.static_stability.coefficients.drag       = Cdrag_delta_a            
            conditions.control_surfaces.aileron.static_stability.coefficients.X          = CX_delta_a             
            conditions.control_surfaces.aileron.static_stability.coefficients.Y          = CY_delta_a            
            conditions.control_surfaces.aileron.static_stability.coefficients.Z          = CZ_delta_a          
            conditions.control_surfaces.aileron.static_stability.coefficients.L          = CL_delta_a          
            conditions.control_surfaces.aileron.static_stability.coefficients.M          = CM_delta_a          
            conditions.control_surfaces.aileron.static_stability.coefficients.N          = CN_delta_a             
            
        if aerodynamics.elevator_flag: 
            conditions.static_stability.coefficients.lift += Clift_delta_e
            conditions.static_stability.coefficients.drag += Cdrag_delta_e
            conditions.static_stability.coefficients.X    += CX_delta_e 
            conditions.static_stability.coefficients.Y    += CY_delta_e
            conditions.static_stability.coefficients.Z    += CZ_delta_e
            conditions.static_stability.coefficients.L    += CL_delta_e
            conditions.static_stability.coefficients.M    += CM_delta_e
            conditions.static_stability.coefficients.N    += CN_delta_e
            
            conditions.control_surfaces.elevator.static_stability.coefficients.lift       = Clift_delta_e         
            conditions.control_surfaces.elevator.static_stability.coefficients.drag       = Cdrag_delta_e            
            conditions.control_surfaces.elevator.static_stability.coefficients.X          = CX_delta_e             
            conditions.control_surfaces.elevator.static_stability.coefficients.Y          = CY_delta_e            
            conditions.control_surfaces.elevator.static_stability.coefficients.Z          = CZ_delta_e          
            conditions.control_surfaces.elevator.static_stability.coefficients.L          = CL_delta_e          
            conditions.control_surfaces.elevator.static_stability.coefficients.M          = CM_delta_e          
            conditions.control_surfaces.elevator.static_stability.coefficients.N          = CN_delta_e            
            
        if aerodynamics.rudder_flag:  
            conditions.static_stability.coefficients.lift += Clift_delta_r
            conditions.static_stability.coefficients.drag += Cdrag_delta_r
            conditions.static_stability.coefficients.X    += CX_delta_r 
            conditions.static_stability.coefficients.Y    += CY_delta_r
            conditions.static_stability.coefficients.Z    += CZ_delta_r
            conditions.static_stability.coefficients.L    += CL_delta_r
            conditions.static_stability.coefficients.M    += CM_delta_r
            conditions.static_stability.coefficients.N    += CN_delta_r
    
            conditions.control_surfaces.rudder.static_stability.coefficients.lift       = Clift_delta_r         
            conditions.control_surfaces.rudder.static_stability.coefficients.drag       = Cdrag_delta_r            
            conditions.control_surfaces.rudder.static_stability.coefficients.X          = CX_delta_r             
            conditions.control_surfaces.rudder.static_stability.coefficients.Y          = CY_delta_r            
            conditions.control_surfaces.rudder.static_stability.coefficients.Z          = CZ_delta_r          
            conditions.control_surfaces.rudder.static_stability.coefficients.L          = CL_delta_r          
            conditions.control_surfaces.rudder.static_stability.coefficients.M          = CM_delta_r          
            conditions.control_surfaces.rudder.static_stability.coefficients.N          = CN_delta_r         
            
        if aerodynamics.flap_flag:
            conditions.static_stability.coefficients.lift += Clift_delta_f
            conditions.static_stability.coefficients.drag += Cdrag_delta_f
            conditions.static_stability.coefficients.X    += CX_delta_f 
            conditions.static_stability.coefficients.Y    += CY_delta_f
            conditions.static_stability.coefficients.Z    += CZ_delta_f
            conditions.static_stability.coefficients.L    += CL_delta_f
            conditions.static_stability.coefficients.M    += CM_delta_f
            conditions.static_stability.coefficients.N    += CN_delta_f
            
    
            conditions.control_surfaces.flap.static_stability.coefficients.lift       = Clift_delta_f         
            conditions.control_surfaces.flap.static_stability.coefficients.drag       = Cdrag_delta_f            
            conditions.control_surfaces.flap.static_stability.coefficients.X          = CX_delta_f             
            conditions.control_surfaces.flap.static_stability.coefficients.Y          = CY_delta_f            
            conditions.control_surfaces.flap.static_stability.coefficients.Z          = CZ_delta_f          
            conditions.control_surfaces.flap.static_stability.coefficients.L          = CL_delta_f          
            conditions.control_surfaces.flap.static_stability.coefficients.M          = CM_delta_f          
            conditions.control_surfaces.flap.static_stability.coefficients.N          = CN_delta_f           
            
    
        if aerodynamics.slat_flag: 
            conditions.static_stability.coefficients.lift += Clift_delta_s
            conditions.static_stability.coefficients.drag += Cdrag_delta_s
            conditions.static_stability.coefficients.X    += CX_delta_s 
            conditions.static_stability.coefficients.Y    += CY_delta_s
            conditions.static_stability.coefficients.Z    += CZ_delta_s
            conditions.static_stability.coefficients.L    += CL_delta_s
            conditions.static_stability.coefficients.M    += CM_delta_s
            conditions.static_stability.coefficients.N    += CN_delta_s
    
            conditions.control_surfaces.slat.static_stability.coefficients.lift       = Clift_delta_s         
            conditions.control_surfaces.slat.static_stability.coefficients.drag       = Cdrag_delta_s            
            conditions.control_surfaces.slat.static_stability.coefficients.X          = CX_delta_s             
            conditions.control_surfaces.slat.static_stability.coefficients.Y          = CY_delta_s            
            conditions.control_surfaces.slat.static_stability.coefficients.Z          = CZ_delta_s          
            conditions.control_surfaces.slat.static_stability.coefficients.L          = CL_delta_s          
            conditions.control_surfaces.slat.static_stability.coefficients.M          = CM_delta_s          
            conditions.control_surfaces.slat.static_stability.coefficients.N          = CN_delta_s                     
         
        
        conditions.static_stability.derivatives.Clift_alpha = compute_stability_derivative(sub_sur.dClift_dalpha ,trans_sur.dClift_dalpha ,sup_sur.dClift_dalpha , h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CX_alpha    = compute_stability_derivative(sub_sur.dCX_dalpha    ,trans_sur.dCX_dalpha    ,sup_sur.dCX_dalpha    , h_sub,h_sup,Mach)  
        conditions.static_stability.derivatives.CY_alpha    = compute_stability_derivative(sub_sur.dCY_dalpha    ,trans_sur.dCY_dalpha    ,sup_sur.dCY_dalpha    , h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CZ_alpha    = compute_stability_derivative(sub_sur.dCZ_dalpha    ,trans_sur.dCZ_dalpha    ,sup_sur.dCZ_dalpha    , h_sub,h_sup,Mach) 
        conditions.static_stability.derivatives.CL_alpha    = compute_stability_derivative(sub_sur.dCL_dalpha    ,trans_sur.dCL_dalpha    ,sup_sur.dCL_dalpha    , h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CM_alpha    = compute_stability_derivative(sub_sur.dCM_dalpha    ,trans_sur.dCM_dalpha    ,sup_sur.dCM_dalpha    , h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CN_alpha    = compute_stability_derivative(sub_sur.dCN_dalpha    ,trans_sur.dCN_dalpha    ,sup_sur.dCN_dalpha    , h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.Clift_beta  = compute_stability_derivative(sub_sur.dClift_dbeta  ,trans_sur.dClift_dbeta  ,sup_sur.dClift_dbeta  , h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CX_beta     = compute_stability_derivative(sub_sur.dCX_dbeta     ,trans_sur.dCX_dbeta     ,sup_sur.dCX_dbeta     , h_sub,h_sup,Mach)  
        conditions.static_stability.derivatives.CY_beta     = compute_stability_derivative(sub_sur.dCY_dbeta     ,trans_sur.dCY_dbeta     ,sup_sur.dCY_dbeta     , h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CZ_beta     = compute_stability_derivative(sub_sur.dCZ_dbeta     ,trans_sur.dCZ_dbeta     ,sup_sur.dCZ_dbeta     , h_sub,h_sup,Mach) 
        conditions.static_stability.derivatives.CL_beta     = compute_stability_derivative(sub_sur.dCL_dbeta     ,trans_sur.dCL_dbeta     ,sup_sur.dCL_dbeta     , h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CM_beta     = compute_stability_derivative(sub_sur.dCM_dbeta     ,trans_sur.dCM_dbeta     ,sup_sur.dCM_dbeta     , h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CN_beta     = compute_stability_derivative(sub_sur.dCN_dbeta     ,trans_sur.dCN_dbeta     ,sup_sur.dCN_dbeta     , h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.Clift_p     = compute_stability_derivative(sub_sur.dClift_dp     ,trans_sur.dClift_dp     ,sup_sur.dClift_dp     , h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.Clift_q     = compute_stability_derivative(sub_sur.dClift_dq     ,trans_sur.dClift_dq     ,sup_sur.dClift_dq     , h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.Clift_r     = compute_stability_derivative(sub_sur.dClift_dr     ,trans_sur.dClift_dr     ,sup_sur.dClift_dr     , h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CX_u        = compute_stability_derivative(sub_sur.dCX_du, trans_sur.dCX_du, sup_sur.dCX_du, h_sub,h_sup,Mach)   
        conditions.static_stability.derivatives.CX_v        = compute_stability_derivative(sub_sur.dCX_dv, trans_sur.dCX_dv, sup_sur.dCX_dv, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CX_w        = compute_stability_derivative(sub_sur.dCX_dw, trans_sur.dCX_dw, sup_sur.dCX_dw, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CY_u        = compute_stability_derivative(sub_sur.dCY_du, trans_sur.dCY_du, sup_sur.dCY_du, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CY_v        = compute_stability_derivative(sub_sur.dCY_dv, trans_sur.dCY_dv, sup_sur.dCY_dv, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CY_w        = compute_stability_derivative(sub_sur.dCY_dw, trans_sur.dCY_dw, sup_sur.dCY_dw, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CZ_u        = compute_stability_derivative(sub_sur.dCZ_du, trans_sur.dCZ_du, sup_sur.dCZ_du, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CZ_v        = compute_stability_derivative(sub_sur.dCZ_dv, trans_sur.dCZ_dv, sup_sur.dCZ_dv, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CZ_w        = compute_stability_derivative(sub_sur.dCZ_dw, trans_sur.dCZ_dw, sup_sur.dCZ_dw, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CL_u        = compute_stability_derivative(sub_sur.dCL_du, trans_sur.dCL_du, sup_sur.dCL_du, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CL_v        = compute_stability_derivative(sub_sur.dCL_dv, trans_sur.dCL_dv, sup_sur.dCL_dv, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CL_w        = compute_stability_derivative(sub_sur.dCL_dw, trans_sur.dCL_dw, sup_sur.dCL_dw, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CM_u        = compute_stability_derivative(sub_sur.dCM_du, trans_sur.dCM_du, sup_sur.dCM_du, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CM_v        = compute_stability_derivative(sub_sur.dCM_dv, trans_sur.dCM_dv, sup_sur.dCM_dv, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CM_w        = compute_stability_derivative(sub_sur.dCM_dw, trans_sur.dCM_dw, sup_sur.dCM_dw, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CN_u        = compute_stability_derivative(sub_sur.dCN_du, trans_sur.dCN_du, sup_sur.dCN_du, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CN_v        = compute_stability_derivative(sub_sur.dCN_dv, trans_sur.dCN_dv, sup_sur.dCN_dv, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CN_w        = compute_stability_derivative(sub_sur.dCN_dw, trans_sur.dCN_dw, sup_sur.dCN_dw, h_sub,h_sup,Mach) 
        conditions.static_stability.derivatives.CX_p        = compute_stability_derivative(sub_sur.dCX_dp, trans_sur.dCX_dp, sup_sur.dCX_dp, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CX_q        = compute_stability_derivative(sub_sur.dCX_dq, trans_sur.dCX_dq, sup_sur.dCX_dq, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CX_r        = compute_stability_derivative(sub_sur.dCX_dr, trans_sur.dCX_dr, sup_sur.dCX_dr, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CY_p        = compute_stability_derivative(sub_sur.dCY_dp, trans_sur.dCY_dp, sup_sur.dCY_dp, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CY_q        = compute_stability_derivative(sub_sur.dCY_dq, trans_sur.dCY_dq, sup_sur.dCY_dq, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CY_r        = compute_stability_derivative(sub_sur.dCY_dr, trans_sur.dCY_dr, sup_sur.dCY_dr, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CZ_p        = compute_stability_derivative(sub_sur.dCZ_dp, trans_sur.dCZ_dp, sup_sur.dCZ_dp, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CZ_q        = compute_stability_derivative(sub_sur.dCZ_dq, trans_sur.dCZ_dq, sup_sur.dCZ_dq, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CZ_r        = compute_stability_derivative(sub_sur.dCZ_dr, trans_sur.dCZ_dr, sup_sur.dCZ_dr, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CL_p        = compute_stability_derivative(sub_sur.dCL_dp, trans_sur.dCL_dp, sup_sur.dCL_dp, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CL_q        = compute_stability_derivative(sub_sur.dCL_dq, trans_sur.dCL_dq, sup_sur.dCL_dq, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CL_r        = compute_stability_derivative(sub_sur.dCL_dr, trans_sur.dCL_dr, sup_sur.dCL_dr, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CM_p        = compute_stability_derivative(sub_sur.dCM_dp, trans_sur.dCM_dp, sup_sur.dCM_dp, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CM_q        = compute_stability_derivative(sub_sur.dCM_dq, trans_sur.dCM_dq, sup_sur.dCM_dq, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CM_r        = compute_stability_derivative(sub_sur.dCM_dr, trans_sur.dCM_dr, sup_sur.dCM_dr, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CN_p        = compute_stability_derivative(sub_sur.dCN_dp, trans_sur.dCN_dp, sup_sur.dCN_dp, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CN_q        = compute_stability_derivative(sub_sur.dCN_dq, trans_sur.dCN_dq, sup_sur.dCN_dq, h_sub,h_sup,Mach)
        conditions.static_stability.derivatives.CN_r        = compute_stability_derivative(sub_sur.dCN_dr, trans_sur.dCN_dr, sup_sur.dCN_dr, h_sub,h_sup,Mach)
        #conditions.static_stability.neutral_point           = # Need to Update
        #conditions.static_stability.spiral_criteria         = # Need to Update  

        for wing in geometry.wings:   
            inviscid_wing_lifts = compute_coefficient(sub_sur.Clift_wing_alpha[wing.tag],trans_sur.Clift_wing_alpha[wing.tag],sup_sur.Cdrag_wing_alpha[wing.tag],h_sub,h_sup,Mach,pts_alpha)
            inviscid_wing_drags = compute_coefficient(sub_sur.Cdrag_wing_alpha[wing.tag],trans_sur.Cdrag_wing_alpha[wing.tag],sup_sur.Cdrag_wing_alpha[wing.tag],h_sub,h_sup,Mach,pts_alpha)
            # Pack 
            conditions.aerodynamics.coefficients.lift.inviscid_wings[wing.tag]         =  inviscid_wing_lifts 
            conditions.aerodynamics.coefficients.lift.compressible_wings[wing.tag]     =  inviscid_wing_lifts 
            conditions.aerodynamics.coefficients.drag.induced.inviscid_wings[wing.tag] =  inviscid_wing_drags   
    
    conditions.aerodynamics.coefficients.lift.total            = conditions.static_stability.coefficients.lift 
    conditions.aerodynamics.coefficients.drag.induced.inviscid = conditions.static_stability.coefficients.drag   

    return

def compute_stability_derivative(sub_sur,trans_sur,sup_sur,h_sub,h_sup,Mach): 
    derivative = h_sub(Mach)*sub_sur(Mach) +   (h_sup(Mach) - h_sub(Mach))*trans_sur(Mach)  + h_sub(Mach)*sup_sur(Mach) 
    return derivative

def compute_coefficients(sub_sur_Clift,sub_sur_Cdrag,sub_sur_CX,sub_sur_CY,sub_sur_CZ,sub_sur_CL,sub_sur_CM,sub_sur_CN,
                         trans_sur_Clift,trans_sur_Cdrag,trans_sur_CX,trans_sur_CY,trans_sur_CZ,trans_sur_CL,trans_sur_CM,trans_sur_CN,
                         sup_sur_Clift,sup_sur_Cdrag,sup_sur_CX,sup_sur_CY,sup_sur_CZ,sup_sur_CL,sup_sur_CM,sup_sur_CN,
                         h_sub,h_sup,Mach, pts): 

    #  subsonic 
    sub_Clift  = np.atleast_2d(sub_sur_Clift(pts)).T  
    sub_Cdrag  = np.atleast_2d(sub_sur_Cdrag(pts)).T  
    sub_CX     = np.atleast_2d(sub_sur_CX(pts)).T 
    sub_CY     = np.atleast_2d(sub_sur_CY(pts)).T     
    sub_CZ     = np.atleast_2d(sub_sur_CZ(pts)).T     
    sub_CL     = np.atleast_2d(sub_sur_CL(pts)).T     
    sub_CM     = np.atleast_2d(sub_sur_CM(pts)).T     
    sub_CN     = np.atleast_2d(sub_sur_CN(pts)).T
  
    # transonic 
    trans_Clift  = np.atleast_2d(trans_sur_Clift(pts)).T  
    trans_Cdrag  = np.atleast_2d(trans_sur_Cdrag(pts)).T  
    trans_CX     = np.atleast_2d(trans_sur_CX(pts)).T 
    trans_CY     = np.atleast_2d(trans_sur_CY(pts)).T     
    trans_CZ     = np.atleast_2d(trans_sur_CZ(pts)).T     
    trans_CL     = np.atleast_2d(trans_sur_CL(pts)).T     
    trans_CM     = np.atleast_2d(trans_sur_CM(pts)).T     
    trans_CN     = np.atleast_2d(trans_sur_CN(pts)).T
    
    # supersonic 
    sup_Clift  = np.atleast_2d(sup_sur_Clift(pts)).T  
    sup_Cdrag  = np.atleast_2d(sup_sur_Cdrag(pts)).T  
    sup_CX     = np.atleast_2d(sup_sur_CX(pts)).T 
    sup_CY     = np.atleast_2d(sup_sur_CY(pts)).T     
    sup_CZ     = np.atleast_2d(sup_sur_CZ(pts)).T     
    sup_CL     = np.atleast_2d(sup_sur_CL(pts)).T     
    sup_CM     = np.atleast_2d(sup_sur_CM(pts)).T     
    sup_CN     = np.atleast_2d(sup_sur_CN(pts)).T            
    
    # apply 
    results       = Data() 
    results.Clift = h_sub(Mach)*sub_Clift +   (1 - (h_sup(Mach) + h_sub(Mach)))*trans_Clift  + h_sup(Mach)*sup_Clift
    results.Cdrag = h_sub(Mach)*sub_Cdrag +   (1 - (h_sup(Mach) + h_sub(Mach)))*trans_Cdrag  + h_sup(Mach)*sup_Cdrag
    results.CX    = h_sub(Mach)*sub_CX    +   (1 - (h_sup(Mach) + h_sub(Mach)))*trans_CX     + h_sup(Mach)*sup_CX   
    results.CY    = h_sub(Mach)*sub_CY    +   (1 - (h_sup(Mach) + h_sub(Mach)))*trans_CY     + h_sup(Mach)*sup_CY   
    results.CZ    = h_sub(Mach)*sub_CZ    +   (1 - (h_sup(Mach) + h_sub(Mach)))*trans_CZ     + h_sup(Mach)*sup_CZ   
    results.CL    = h_sub(Mach)*sub_CL    +   (1 - (h_sup(Mach) + h_sub(Mach)))*trans_CL     + h_sup(Mach)*sup_CL   
    results.CM    = h_sub(Mach)*sub_CM    +   (1 - (h_sup(Mach) + h_sub(Mach)))*trans_CM     + h_sup(Mach)*sup_CM   
    results.CN    = h_sub(Mach)*sub_CN    +   (1 - (h_sup(Mach) + h_sub(Mach)))*trans_CN     + h_sup(Mach)*sup_CN
  
    return results


def compute_coefficient(sub_sur_coef,trans_sur_coef, sup_sur_coef, h_sub,h_sup,Mach, pts): 

    #  subsonic 
    sub_coef  = np.atleast_2d(sub_sur_coef(pts)).T     
  
    # transonic 
    trans_coef  = np.atleast_2d(trans_sur_coef(pts)).T    
    
    # supersonic 
    sup_coef  = np.atleast_2d(sub_sur_coef(pts)).T             
    
    # apply  
    coef = h_sub(Mach)*sub_coef +   (1 - (h_sup(Mach) + h_sub(Mach)))*trans_coef  + h_sub(Mach)*sup_coef 
  
    return coef 

 
def evaluate_no_surrogate(state,settings,geometry):
    """Evaluates forces and moments directly using VLM.
    
    Assumptions:
        None
        
    Source:
        None

    Args:
        aerodynamics       : VLM analysis          [unitless]
        state      : flight conditions     [unitless]
        settings   : VLM analysis settings [unitless]
        geometry   : vehicle configuration [unitless] 
        
    Returns: 
        None  
    """          

    # unpack 
    conditions     = state.conditions 
    results        = VLM(conditions,settings,geometry)   

    # Dimensionalize the lift and drag for each wing
    areas            = geometry.vortex_distribution.wing_areas
    dim_wing_lifts   = results.CL_wing * areas
    dim_wing_drags   = results.CDi_wing * areas  
    i = 0 
    for wing in geometry.wings:
        ref = wing.areas.reference
        if wing.symmetric:
            Clift_wing  = np.atleast_2d(np.sum(dim_wing_lifts[:,i:(i+2)],axis=1)).T/ref
            Cdrag_wing  = np.atleast_2d(np.sum(dim_wing_drags[:,i:(i+2)],axis=1)).T/ref 
            i+=1
        else:
            Clift_wing  = np.atleast_2d(dim_wing_lifts[:,i]).T/ref
            Cdrag_wing  = np.atleast_2d(dim_wing_drags[:,i]).T/ref 
        i+=1
         
        conditions.aerodynamics.coefficients.lift.inviscid_wings[wing.tag]         = Clift_wing
        conditions.aerodynamics.coefficients.lift.compressible_wings[wing.tag]     = Clift_wing
        conditions.aerodynamics.coefficients.drag.induced.inviscid_wings[wing.tag] = Cdrag_wing
        
         
    # Pack
    conditions.aerodynamics.coefficients.lift.total                =  results.CL  
    conditions.aerodynamics.coefficients.drag.induced.inviscid     =  results.CDi   
    
    return