## @ingroup Methods-Aerodynamics-Airfoil
# compute_airfoil_properties_from_panel_method.py
# 
# Created:  Oct 2023, Racheal M. Erhard
# Modified: 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import Legacy.trunk.S as SUAVE
from Legacy.trunk.S.Core import Data , Units
from Legacy.trunk.S.Methods.Aerodynamics.Airfoil_Panel_Method.airfoil_analysis import airfoil_analysis
from RCAIDE.Methods.Aerodynamics.Airfoil.compute_airfoil_properties_from_polar_files  import compute_extended_polars
import numpy as np

## @ingroup Methods-Aerodynamics-Airfoil
def compute_airfoil_properties_from_panel_method(settings, airfoil):
    """This computes the aerodynamic properties and coefficients of an airfoil in stall regimes using pre-stall
    characterstics and AERODAS formation for post stall characteristics. This is useful for 
    obtaining a more accurate prediction of wing and blade loading as well as aeroacoustics. Pre stall characteristics 
    are obtained in the form of a text file of airfoil polar data obtained from airfoiltools.com
    
    Assumptions:
        None 
        
    Source
        None
        
    Inputs:
    airfoil_geometry                        <data_structure>
    airfoil_polar_files                     <string>
    boundary_layer_files                    <string>
    use_pre_stall_data                      [Boolean]
    Outputs:
    airfoil_data.
        cl_polars                           [unitless]
        cd_polars                           [unitless]      
        aoa_sweep                           [unitless]
        
        # raw data                          [unitless]
        theta_lower_surface                 [unitless]
        delta_lower_surface                 [unitless]
        delta_star_lower_surface            [unitless] 
        sa_lower_surface                    [unitless]
        ue_lower_surface                    [unitless]
        cf_lower_surface                    [unitless]
        dcp_dx_lower_surface                [unitless] 
        Ret_lower_surface                   [unitless]
        H_lower_surface                     [unitless]
        theta_upper_surface                 [unitless]
        delta_upper_surface                 [unitless]
        delta_star_upper_surface            [unitless] 
        sa_upper_surface                    [unitless]
        ue_upper_surface                    [unitless]
        cf_upper_surface                    [unitless]
        dcp_dx_upper_surface                [unitless] 
        Ret_upper_surface                   [unitless]
        H_upper_surface                     [unitless] 
    
    Properties Used:
    N/A
    """
    # Extract any initialized airfoil data
    Airfoil_Data = compute_boundary_layer_properties(settings, airfoil)
    use_pre_stall_data = settings.use_pre_stall_data
    
    # ----------------------------------------------------------------------------------------
    # Compute airfoil boundary layers properties 
    # ----------------------------------------------------------------------------------------   
    num_polars = len(Airfoil_Data.re_from_polar)
     
    # ----------------------------------------------------------------------------------------
    # Compute extended cl and cd polars 
    # ----------------------------------------------------------------------------------------
    # Get all of the coefficients for AERODAS wings
    neg_post_stall_region = np.linspace(-180, -45, 16) # coarse post-stall refinement
    pos_post_stall_region = np.linspace(45, 180, 16) # coarse post-stall refinement
    mid_region = np.linspace(-45, 45, 25)
    AoA_sweep_deg = np.append(neg_post_stall_region, np.append(mid_region, pos_post_stall_region))
    AoA_sweep_rad = AoA_sweep_deg * Units.degrees
    
    # Create an infinite aspect ratio wing
    geometry              = SUAVE.Components.Wings.Wing()
    geometry.aspect_ratio = np.inf
    geometry.section      = Data()  
    
    # AERODAS   
    CL = np.zeros((num_polars,len(AoA_sweep_deg)))
    CD = np.zeros((num_polars,len(AoA_sweep_deg)))  
    for j in range(num_polars):    
        airfoil_cl  = Airfoil_Data.lift_coefficients[j,:]
        airfoil_cd  = Airfoil_Data.drag_coefficients[j,:]   
        airfoil_aoa = Airfoil_Data.aoa_from_polar[j,:]/Units.degrees 
    
        # compute airfoil cl and cd for extended AoA range 
        CL[j,:],CD[j,:] = compute_extended_polars(airfoil_cl,airfoil_cd,airfoil_aoa,AoA_sweep_deg,geometry,use_pre_stall_data)  
         
    # ----------------------------------------------------------------------------------------
    # Store data 
    # ----------------------------------------------------------------------------------------    
    Airfoil_Data.reynolds_numbers    = Airfoil_Data.re_from_polar
    Airfoil_Data.angle_of_attacks    = AoA_sweep_rad 
    Airfoil_Data.lift_coefficients   = CL 
    Airfoil_Data.drag_coefficients   = CD    
        
    return Airfoil_Data

## @ingroup Methods-Aerodynamics-Airfoil
def compute_boundary_layer_properties(settings, airfoil): 
    '''Computes the boundary layer properties of an airfoil for a sweep of Reynolds numbers 
    and angle of attacks using a panel method.
    
    Source:
    None
    
    Assumptions:
    None 
    
    Inputs:
    airfoil_geometry   <data_structure>
    Airfoil_Data       <data_structure>
    
    Outputs:
    Airfoil_Data       <data_structure>
    
    Properties Used:
    N/A
    '''
    # Extract airfoil geometry and settings for simulation
    airfoil_geometry = airfoil.geometry
    AoA_sweep = settings.panel_method.angle_of_attach_range
    Re_sweep = settings.panel_method.Reynolds_number_range
    AoA_vals = np.tile(AoA_sweep[None,:], (len(Re_sweep) ,1))
    Re_vals = np.tile(Re_sweep[:,None], (1, len(AoA_sweep)))

    # run airfoil analysis
    af_res  = airfoil_analysis(airfoil_geometry, AoA_vals, Re_vals)

    # store data
    Airfoil_Data = Data()
    Airfoil_Data.aoa_from_polar = np.tile(AoA_sweep[None,:],(len(Re_sweep),1)) 
    Airfoil_Data.re_from_polar = Re_sweep 
    Airfoil_Data.lift_coefficients = af_res.cl
    Airfoil_Data.drag_coefficients = af_res.cd
    Airfoil_Data.cm = af_res.cm

    Airfoil_Data.boundary_layer = Data()
    Airfoil_Data.boundary_layer.angle_of_attacks = AoA_sweep 
    Airfoil_Data.boundary_layer.reynolds_numbers = Re_sweep      
    Airfoil_Data.boundary_layer.theta_lower_surface = af_res.theta 
    Airfoil_Data.boundary_layer.delta_lower_surface = af_res.delta  
    Airfoil_Data.boundary_layer.delta_star_lower_surface = af_res.delta_star  
    Airfoil_Data.boundary_layer.Ue_Vinf_lower_surface = af_res.Ue_Vinf   
    Airfoil_Data.boundary_layer.cf_lower_surface = af_res.cf   
    Airfoil_Data.boundary_layer.dcp_dx_lower_surface = af_res.dcp_dx 
    Airfoil_Data.boundary_layer.theta_upper_surface = af_res.theta 
    Airfoil_Data.boundary_layer.delta_upper_surface = af_res.delta 
    Airfoil_Data.boundary_layer.delta_star_upper_surface = af_res.delta_star   
    Airfoil_Data.boundary_layer.Ue_Vinf_upper_surface = af_res.Ue_Vinf     
    Airfoil_Data.boundary_layer.cf_upper_surface = af_res.cf   
    Airfoil_Data.boundary_layer.dcp_dx_upper_surface = af_res.dcp_dx   

    return Airfoil_Data