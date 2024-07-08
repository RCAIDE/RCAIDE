# RCAIDE/Library/Methods/Aerodynamics/Vortex_Lattice_Method/VLM_aerdoynamics_solver.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core                                     import Data 
from RCAIDE.Library.Methods.Aerodynamics.Vortex_Lattice_Method import Vortex_Lattice_Method 
from RCAIDE.Library.Methods.Utilities                          import Cubic_Spline_Blender  

# package imports
import numpy as np 
from scipy.interpolate import RectBivariateSpline, RegularGridInterpolator

# ----------------------------------------------------------------------------------------------------------------------
#  Vortex_Lattice
# ---------------------------------------------------------------------------------------------------------------------- 
def evaluate_surrogate(state,settings,geometry):
    """Evaluates lift and drag using available surrogates.

    Assumptions:
        None

    Source:
        None

    Args:
        state.conditions.freestream.dynamics_pressure       (numpy.ndarray) : dynamics_pressure[unitless]
        state.conditions.freestream.angle_of_attack         (numpy.ndarray) : angle_of_attack  [radians]
        state.conditions.freestream.mach_number             (numpy.ndarray) : mach_number      [unitless]
        state.analyses.aerodynamics.surrogates                       (dict) : surrogates       [-]
        settings                                                     (dict) : settings         [-]
     
    Returns:
        state.conditions.aerodynamics.coefficients 
            .lift                                                  (numpy.ndarray) : lift coefficent                              [unitless]
            .lift.breakdown.inviscid_wings[wings.*.tag]            (numpy.ndarray) : wing lift coefficent                         [unitless]
            .lift.breakdown.inviscid_wings_lift.total              (numpy.ndarray) : wing lift coefficent                         [unitless]
            .lift.breakdown.inviscid_wings_lift.compressible_wings (numpy.ndarray) : compressible lift coefficent (wing specific) [unitless]
            .drag.breakdown.induced.total                          (numpy.ndarray) : induced drag                                 [unitless]
            .drag.breakdown.induced.inviscid                       (numpy.ndarray) : induced drag                                 [unitless]
            .drag.breakdown.induced.wings_sectional_drag           (numpy.ndarray) : sectional induced drag  (wing specific)      [unitless]
            .drag.breakdown.induced.inviscid_wings                 (numpy.ndarray) : wing induced drag  (wing specific)           [unitless]
    """          
    
    # unpack  
    surrogates  = state.analyses.aerodynamics.surrogates
    hsub_min    = state.analyses.aerodynamics.hsub_min
    hsub_max    = state.analyses.aerodynamics.hsub_max
    hsup_min    = state.analyses.aerodynamics.hsup_min
    hsup_max    = state.analyses.aerodynamics.hsup_max  
    conditions  = state.conditions
    AoA         = state.conditions.aerodynamics.angles.alpha.T[0]
    Mach        = conditions.freestream.mach_number.T[0]
    
    # Unapck the surrogates
    CL_surrogate_sub          = surrogates.lift_coefficient_sub  
    CL_surrogate_sup          = surrogates.lift_coefficient_sup  
    CL_surrogate_trans        = surrogates.lift_coefficient_trans
    CDi_surrogate_sub         = surrogates.drag_coefficient_sub  
    CDi_surrogate_sup         = surrogates.drag_coefficient_sup  
    CDi_surrogate_trans       = surrogates.drag_coefficient_trans
    wing_CL_surrogates_sub    = surrogates.wing_lift_coefficient_sub  
    wing_CL_surrogates_sup    = surrogates.wing_lift_coefficient_sup  
    wing_CL_surrogates_trans  = surrogates.wing_lift_coefficient_trans
    wing_CDi_surrogates_sub   = surrogates.wing_drag_coefficient_sub  
    wing_CDi_surrogates_sup   = surrogates.wing_drag_coefficient_sup  
    wing_CDi_surrogates_trans = surrogates.wing_drag_coefficient_trans 
    
    # 3 Cases for surrogates, subsonic only, supersonic only, and both
    if CL_surrogate_sup == None:
        inviscid_lift = CL_surrogate_sub(AoA,Mach,grid=False)
        inviscid_drag = CDi_surrogate_sub(AoA,Mach,grid=False)
    elif CL_surrogate_sub == None:
        inviscid_lift = CL_surrogate_sup(AoA,Mach,grid=False)
        inviscid_drag = CDi_surrogate_sup(AoA,Mach,grid=False)     
    else:
        # Spline for Subsonic-to-Transonic-to-Supersonic Regimes
        sub_trans_spline = Cubic_Spline_Blender(hsub_min,hsub_max)
        h_sub            = lambda M:sub_trans_spline.compute(M)          
        sup_trans_spline = Cubic_Spline_Blender(hsup_min,hsup_max) 
        h_sup            = lambda M:sup_trans_spline.compute(M)          
    
        inviscid_lift = h_sub(Mach)*CL_surrogate_sub(AoA,Mach,grid=False)   +\
                          (h_sup(Mach) - h_sub(Mach))*CL_surrogate_trans((AoA,Mach))+ \
                          (1- h_sup(Mach))*CL_surrogate_sup(AoA,Mach,grid=False)

        inviscid_drag = h_sub(Mach)*CDi_surrogate_sub(AoA,Mach,grid=False)   +\
                          (h_sup(Mach) - h_sub(Mach))*CDi_surrogate_trans((AoA,Mach))+ \
                          (1- h_sup(Mach))*CDi_surrogate_sup(AoA,Mach,grid=False)
        
    conditions.aerodynamics.coefficients.lift.total                      = np.atleast_2d(inviscid_lift).T
    conditions.aerodynamics.coefficients.lift.breakdown.total            = np.atleast_2d(inviscid_lift).T
    conditions.aerodynamics.coefficients.drag.breakdown.induced.inviscid = np.atleast_2d(inviscid_drag).T
    
    for wing in geometry.wings.keys():  
        if CL_surrogate_sup == None:
            inviscid_wing_lifts = wing_CL_surrogates_sub[wing](AoA,Mach,grid=False)
            inviscid_wing_drags = wing_CDi_surrogates_sub[wing](AoA,Mach,grid=False)            
            
        elif CL_surrogate_sub == None:
            inviscid_wing_lifts = wing_CL_surrogates_sup[wing](AoA,Mach,grid=False)
            inviscid_wing_drags = wing_CDi_surrogates_sup[wing](AoA,Mach,grid=False)                
        
        else:
            inviscid_wing_lifts = h_sub(Mach)*wing_CL_surrogates_sub[wing](AoA,Mach,grid=False)    + \
                                    (h_sup(Mach) - h_sub(Mach))*wing_CL_surrogates_trans[wing]((AoA,Mach))+ \
                                    (1- h_sup(Mach))*wing_CL_surrogates_sup[wing](AoA,Mach,grid=False)
            
            inviscid_wing_drags = h_sub(Mach)*wing_CDi_surrogates_sub[wing](AoA,Mach,grid=False)  + \
                                    (h_sup(Mach) - h_sub(Mach))*wing_CDi_surrogates_trans[wing]((AoA,Mach))+ \
                                    (1- h_sup(Mach))*wing_CDi_surrogates_sup[wing](AoA,Mach,grid=False) 
        conditions.aerodynamics.coefficients.lift.breakdown.inviscid_wings[wing]         = np.atleast_2d(inviscid_wing_lifts).T
        conditions.aerodynamics.coefficients.lift.breakdown.compressible_wings[wing]     = np.atleast_2d(inviscid_wing_lifts).T
        conditions.aerodynamics.coefficients.drag.breakdown.induced.inviscid_wings[wing] = np.atleast_2d(inviscid_wing_drags).T
     
    return     

def evaluate_no_surrogate(state,settings,geometry):
    """Evaluates lift and drag directly using the Vortex Lattice Method
    
    Assumptions:
        No changes to initial geometry or settings
    
    Source:
        None
    
    Args: 
        state     (dict) : flight conditions    [unitless]
        settings  (dict) : settings             [unitless]
        geometry  (dict) : aircraft geometry    [unitless]
      
    Returns:
        state.conditions.aerodynamics.coefficients
            .lift.breakdown.inviscid_wings_lift[wings.*.tag]         (numpy.ndarray) : wing lift coefficent                         [unitless]
            .lift.breakdown.inviscid_wings_lift.total                (numpy.ndarray) : wing lift coefficent                         [unitless]
            .lift.breakdown.inviscid_wings_sectional                 (numpy.ndarray) : sectional lift coefficent                    [unitless]
            .lift.breakdown.compressible_wing                        (numpy.ndarray) : compressible lift coefficent (wing specific) [unitless]
            .drag.breakdown.induced.total                            (numpy.ndarray) : induced drag                                 [unitless]
            .drag.breakdown.induced.inviscid                         (numpy.ndarray) : induced drag                                 [unitless]
            .drag.breakdown.induced.wings_sectional_drag             (numpy.ndarray) : sectional induced drag  (wing specific)      [unitless]
            .drag.breakdown.induced.induced.inviscid_wings           (numpy.ndarray) : wing induced drag  (wing specific)           [unitless]       
    """          
    
    # unpack         
    conditions = state.conditions
    settings   = state.analyses.aerodynamics.settings
    geometry   = state.analyses.aerodynamics.geometry      
    
    # Evaluate the VLM 
    inviscid_lift, inviscid_drag, wing_lifts, wing_drags, wing_lift_distribution, \
    wing_drag_distribution, induced_angle_distribution = calculate_VLM(conditions,settings,geometry)
     
    conditions.aerodynamics.coefficients.lift.total                              = inviscid_lift  
    conditions.aerodynamics.coefficients.lift.breakdown.total                    = inviscid_lift        
    conditions.aerodynamics.coefficients.lift.breakdown.compressible_wings       = wing_lifts
    conditions.aerodynamics.coefficients.lift.breakdown.inviscid_wings           = wing_lifts
    conditions.aerodynamics.coefficients.lift.breakdown.inviscid_wings_sectional = wing_lift_distribution 
    conditions.aerodynamics.coefficients.drag.breakdown.induced.total            = inviscid_drag     
    conditions.aerodynamics.coefficients.drag.breakdown.induced.inviscid         = inviscid_drag     
    conditions.aerodynamics.coefficients.drag.breakdown.induced.inviscid_wings   = wing_drags
    conditions.aerodynamics.coefficients.drag.breakdown.induced.wings_sectional  = wing_drag_distribution 
    conditions.aerodynamics.coefficients.drag.breakdown.induced.angle            = induced_angle_distribution
     
    return  


def sample_training(aero):
    """Call methods to run vortex lattice for sample point evaluation.

    Assumptions:
        None

    Source:
        None

    Args: 
        aero (dict) : aerodynamics analyses   [unitless]
        
    Returns:
        None  
    """
    # unpack
    geometry      = aero.geometry
    settings      = aero.settings
    training      = aero.training
    AoA           = training.angle_of_attack 
    Mach          = training.Mach
    lenAoA        = len(AoA)
    #sub_len       = int(sum(Mach<1.))
    #sup_len       = len(Mach)-sub_len
    
    # Assign placeholders        
    CL_w_sub  = Data()
    CL_w_sup  = Data()
    CDi_w_sub = Data()
    CDi_w_sup = Data() 
        
    # Setup new array shapes for vectorization 
    Machs  = np.atleast_2d(np.tile(Mach,lenAoA).flatten()).T 
    
    # Setup conditions    
    cons                              = RCAIDE.Framework.Mission.Common.Results()
    cons.aerodynamics.angles.alpha    = np.atleast_2d(np.tile(AoA,len(Mach) ).T.flatten()).T
    cons.freestream.mach_number       = Machs
    cons.freestream.velocity          = np.zeros_like(Machs)
    
    total_lift, total_drag, wing_lifts, wing_drags, _ , _ , _ = calculate_VLM(cons,settings,geometry)     

    # Split subsonic from supersonic
    if np.sum(Machs<1.)==0:
        sub_sup_split = 0
    else:
        sub_sup_split = np.where(Machs < 1.0)[0][-1] + 1 
    len_sub_mach  = np.sum(Mach<1.)
    len_sup_mach  = len(Mach)  - len_sub_mach
    
    # Reshape
    CL_sub  = np.reshape(total_lift[0:sub_sup_split,0],(len_sub_mach,lenAoA)).T
    CL_sup  = np.reshape(total_lift[sub_sup_split:,0],(len_sup_mach,lenAoA)).T
    CDi_sub = np.reshape(total_drag[0:sub_sup_split,0],(len_sub_mach,lenAoA)).T
    CDi_sup = np.reshape(total_drag[sub_sup_split:,0],(len_sup_mach,lenAoA)).T
    
    # Now do the same for each wing
    for wing in geometry.wings.keys():
        
        # Slice out the sub and supersonic
        CL_wing_sub  = wing_lifts[wing][0:sub_sup_split,0]
        CL_wing_sup  = wing_lifts[wing][sub_sup_split:,0]
        CDi_wing_sub = wing_drags[wing][0:sub_sup_split,0]  
        CDi_wing_sup = wing_drags[wing][sub_sup_split:,0]  
        
        # Rearrange and pack
        CL_w_sub[wing]  = np.reshape(CL_wing_sub,(len_sub_mach,lenAoA)).T
        CL_w_sup[wing]  = np.reshape(CL_wing_sup,(len_sup_mach,lenAoA)).T
        CDi_w_sub[wing] = np.reshape(CDi_wing_sub,(len_sub_mach,lenAoA)).T   
        CDi_w_sup[wing] = np.reshape(CDi_wing_sup,(len_sup_mach,lenAoA)).T   
    
    # Store training data 
    training.lift_coefficient_sub         = CL_sub
    training.lift_coefficient_sup         = CL_sup
    training.wing_lift_coefficient_sub    = CL_w_sub        
    training.wing_lift_coefficient_sup    = CL_w_sup
    training.drag_coefficient_sub         = CDi_sub
    training.drag_coefficient_sup         = CDi_sup
    training.wing_drag_coefficient_sub    = CDi_w_sub        
    training.wing_drag_coefficient_sup    = CDi_w_sup
    
    return
    
def build_surrogate(aero):
    """Build a surrogate using sample evaluation results.

    Assumptions:
        None

    Source:
        None

    Args: 
        aero (dict) : aerodynamics analyses   [unitless]

    Returns:
        None 
    """           

    # unpack data
    surrogates     = aero.surrogates
    training       = aero.training
    geometry       = aero.geometry
    Mach           = training.Mach
    AoA_data       = training.angle_of_attack[:,0]
    if np.sum(Mach<1.)==0:
        sub_sup_split = 0
    else:
        sub_sup_split = np.where(Mach < 1.0)[0][-1] + 1 
    mach_data_sub  = training.Mach[0:sub_sup_split,0]
    mach_data_sup  = training.Mach[sub_sup_split:,0]
    CL_data_sub    = training.lift_coefficient_sub   
    CL_data_sup    = training.lift_coefficient_sup
    CDi_data_sub   = training.drag_coefficient_sub         
    CDi_data_sup   = training.drag_coefficient_sup 
    CL_w_data_sub  = training.wing_lift_coefficient_sub
    CL_w_data_sup  = training.wing_lift_coefficient_sup     
    CDi_w_data_sub = training.wing_drag_coefficient_sub         
    CDi_w_data_sup = training.wing_drag_coefficient_sup
      
    # Check for 3 different cases, pure subsonic, pure supersonic, both
    SUB = np.shape(CL_data_sub)[1]>0
    SUP = np.shape(CL_data_sup)[1]>0

    # Do the subsonic surrogates
    if SUB:
        CL_surrogate_sub  = RectBivariateSpline(AoA_data, mach_data_sub, CL_data_sub)
        CDi_surrogate_sub = RectBivariateSpline(AoA_data, mach_data_sub, CDi_data_sub)  
    
    # Do the supersonic surrogates
    if SUP:
        CL_surrogate_sup  = RectBivariateSpline(AoA_data, mach_data_sup, CL_data_sup) 
        CDi_surrogate_sup = RectBivariateSpline(AoA_data, mach_data_sup, CDi_data_sup)    
            
    # Do the transonic regime surrogates
    if SUB and SUP:	                             
        CL_data_trans        = np.zeros((len(AoA_data),3))	      
        CDi_data_trans       = np.zeros((len(AoA_data),3))	 
        CL_data_trans[:,0]   = CL_data_sub[:,-1]    	     
        CL_data_trans[:,1]   = CL_data_sup[:,0] 
        CL_data_trans[:,2]   = CL_data_sup[:,1] 
        CDi_data_trans[:,0]  = CDi_data_sub[:,-1]	     
        CDi_data_trans[:,1]  = CDi_data_sup[:,0]  
        mach_data_trans_CL   = np.array([mach_data_sub[-1],mach_data_sup[0],mach_data_sup[1]]) 
        mach_data_trans_CDi  = np.array([mach_data_sub[-1],mach_data_sup[0],mach_data_sup[1]])  
        CL_surrogate_trans   = RegularGridInterpolator((AoA_data, mach_data_trans_CL), CL_data_trans,method = 'linear', bounds_error=False, fill_value=None)  
        CDi_surrogate_trans  = RegularGridInterpolator((AoA_data, mach_data_trans_CDi), CDi_data_trans,method = 'linear', bounds_error=False, fill_value=None)  

    CL_w_surrogates_sub     = Data() 
    CL_w_surrogates_sup     = Data() 
    CL_w_surrogates_trans   = Data() 
    CDi_w_surrogates_sub    = Data()             
    CDi_w_surrogates_sup    = Data() 
    CDi_w_surrogates_trans  = Data() 	      
    CL_w_data_trans         = Data()	                     
    CDi_w_data_trans        = Data()    
    for wing in geometry.wings.keys():  
        # Do the subsonic surrogates
        if SUB:
            CL_w_surrogates_sub[wing]    = RectBivariateSpline(AoA_data, mach_data_sub, CL_w_data_sub[wing]) 
            CDi_w_surrogates_sub[wing]   = RectBivariateSpline(AoA_data, mach_data_sub, CDi_w_data_sub[wing])  
        # Do the supersonic surrogates
        if SUP:
            CL_w_surrogates_sup[wing]    = RectBivariateSpline(AoA_data, mach_data_sup, CL_w_data_sup[wing]) 
            CDi_w_surrogates_sup[wing]   = RectBivariateSpline(AoA_data, mach_data_sup, CDi_w_data_sup[wing])
        # Do the transonic regime surrogates:
        if SUB and SUP:	  
            CLw                    = np.zeros_like(CL_data_trans)   
            CLw[:,0]               = CL_w_data_sub[wing][:,-1]   	 
            CLw[:,1]               = CL_w_data_sup[wing][:,0]  	
            CLw[:,2]               = CL_w_data_sup[wing][:,1]  	
            CDiw                   = np.zeros_like(CDi_data_trans)         
            CDiw[:,0]              = CDi_w_data_sub[wing][:,-1]    
            CDiw[:,1]              = CDi_w_data_sup[wing][:,0]   
            CDiw[:,2]              = CDi_w_data_sup[wing][:,1]   
            CL_w_data_trans[wing]  = CLw
            CDi_w_data_trans[wing] = CDiw   
            CL_w_surrogates_trans[wing]  = RegularGridInterpolator((AoA_data, mach_data_trans_CL), CL_w_data_trans[wing],method = 'linear',bounds_error=False, fill_value=None)     
            CDi_w_surrogates_trans[wing] = RegularGridInterpolator((AoA_data, mach_data_trans_CL), CDi_w_data_trans[wing],method = 'linear', bounds_error=False, fill_value=None)           

    # Pack the outputs
    surrogates.lift_coefficient_sub        = CL_surrogate_sub  
    surrogates.lift_coefficient_sup        = CL_surrogate_sup  
    surrogates.lift_coefficient_trans      = CL_surrogate_trans
    surrogates.wing_lift_coefficient_sub   = CL_w_surrogates_sub  
    surrogates.wing_lift_coefficient_sup   = CL_w_surrogates_sup  
    surrogates.wing_lift_coefficient_trans = CL_w_surrogates_trans
    surrogates.drag_coefficient_sub        = CDi_surrogate_sub  
    surrogates.drag_coefficient_sup        = CDi_surrogate_sup  
    surrogates.drag_coefficient_trans      = CDi_surrogate_trans
    surrogates.wing_drag_coefficient_sub   = CDi_w_surrogates_sub  
    surrogates.wing_drag_coefficient_sup   = CDi_w_surrogates_sup  
    surrogates.wing_drag_coefficient_trans = CDi_w_surrogates_trans
    
    return

# ----------------------------------------------------------------------
#  Helper Functions
# ----------------------------------------------------------------------
def calculate_VLM(conditions,settings,geometry):
    """Calculate the total vehicle lift coefficient and specific wing coefficients (with specific wing reference areas)
    using a vortex lattice method.

    Assumptions:
        None

    Source:
        None

    Args:
        conditions                      (passed to vortex lattice method)
        settings                        (passed to vortex lattice method)
        geometry 

    Returns:
        CL                  (numpy.ndarray) : lift coefficent                          [unitless]
        CDi                 (numpy.ndarray) : induced drag coefficent                  [unitless]
        wing_lifts          (numpy.ndarray) : wing induced lift coefficient            [unitless]
        wing_drags          (numpy.ndarray) : wing induced drag coefficient            [unitless]
        cl_y                (numpy.ndarray) : sectional induced lift  (wing specific)  [unitless]
        cdi_y               (numpy.ndarray) : sectional induced drag  (wing specific)  [unitless]
        wing_induced_angle  (numpy.ndarray) : wing induced angle                       [unitless]  
    """            
    
    VLM_results = Vortex_Lattice_Method(conditions,settings,geometry)
    CL          = VLM_results.CL
    CDi         = VLM_results.CDi 
    CL_wing     = VLM_results.CL_wing  
    CDi_wing    = VLM_results.CDi_wing 
    cl_y        = VLM_results.cl_y     
    cdi_y       = VLM_results.cdi_y    
    alpha_i     = VLM_results.alpha_i   
    
    # Dimensionalize the lift and drag for each wing 
    dim_wing_lifts = CL_wing  * geometry.vortex_distribution.wing_areas
    dim_wing_drags = CDi_wing * geometry.vortex_distribution.wing_areas
    
    i = 0
    # Assign the lift and drag and non-dimensionalize
    wing_lifts         = Data()
    wing_drags         = Data()
    wing_induced_angle = Data()
    for wing in geometry.wings.values():
        ref = wing.areas.reference
        if wing.symmetric:
            wing_lifts[wing.tag]         = np.atleast_2d(np.sum(dim_wing_lifts[:,i:(i+2)],axis=1)).T/ref
            wing_drags[wing.tag]         = np.atleast_2d(np.sum(dim_wing_drags[:,i:(i+2)],axis=1)).T/ref
            wing_induced_angle[wing.tag] = np.concatenate((alpha_i[i],alpha_i[i+1]),axis=1)
            i+=1
        else:
            wing_lifts[wing.tag]         = np.atleast_2d(dim_wing_lifts[:,i]).T/ref
            wing_drags[wing.tag]         = np.atleast_2d(dim_wing_drags[:,i]).T/ref
            wing_induced_angle[wing.tag] = alpha_i[i]
        i+=1 
    return CL,CDi,wing_lifts, wing_drags,cl_y,cdi_y,wing_induced_angle 
