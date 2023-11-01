## @ingroup Methods-Aerodynamics-Airfoil
# compute_airfoil_properties_from_polar_files.py
# 
# Created:  Oct 2023, Racheal M. Erhard
# Modified: 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import Legacy.trunk.S as SUAVE
from Legacy.trunk.S.Core                                                                          import Data, Units
from Legacy.trunk.S.Methods.Aerodynamics.AERODAS.pre_stall_coefficients                           import pre_stall_coefficients
from Legacy.trunk.S.Methods.Aerodynamics.AERODAS.post_stall_coefficients                          import post_stall_coefficients
from Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Cross_Section.Airfoil.compute_airfoil_properties import compute_extended_polars
from RCAIDE.Methods.Aerodynamics.Airfoil.import_airfoil_polars  import import_airfoil_polars   
import numpy as np
import os

## @ingroup Methods-Aerodynamics-Airfoil
def compute_airfoil_properties_from_polar_files(airfoil_analysis, airfoil_component):
    """
    Takes the airfoil and extracts the attached polar data from the polar files. This data is then used to
    construct airfoil polar surrogates over the provided Reynolds, Mach, and angle of attack ranges.
    The aerodynamic properties of the airfoil in stall regimes are computed with post stall modeling provided
    from AERODAS formulation. A blending is provided between pre- and post-stall coefficient data.
    Pre stall characteristics are obtained in the form of a text file of airfoil polar data.
    
    Assumptions:
        None 
        
    Source
        None
        
    Inputs:
    airfoil                                <data_structure>
    use_pre_stall_data                      [Boolean]
    
    Outputs:
    airfoil_data.
        cl_polars                           [unitless]
        cd_polars                           [unitless]      
        aoa_sweep                           [unitless]
    
    Properties Used:
    N/A
    """
    # ----------------------------------------------------------------------------------------
    # Extract settings and check for polar data
    # ----------------------------------------------------------------------------------------
    use_pre_stall_data = airfoil_analysis.settings.use_pre_stall_data
    polars_directory = f"{airfoil_component.airfoil_directory}/Polars"
    # Find polars in airfoil data directory
    if not os.path.exists(polars_directory):
        raise Exception(f"Must include Polars directory in {airfoil_component.airfoil_directory}!")
    else:
        airfoil_analysis.polar_files = os.listdir(polars_directory)
        airfoil_analysis.polar_files = sorted([f"{polars_directory}/{file}" for file in airfoil_analysis.polar_files])
    
    if airfoil_analysis.polar_files is None:
        raise Exception('No airfoil polar files included in Polars directory! Required for running compute_airfoil_properties_from_polar_files()!')

    # ----------------------------------------------------------------------------------------
    # Compute extended cl and cd polars 
    # ----------------------------------------------------------------------------------------
    # check number of polars per airfoil in batch
    num_polars = len(airfoil_analysis.polar_files)
    if num_polars < 3:
        raise AttributeError('Provide three or more airfoil polars to compute surrogate')     
     
    # read in polars from files overwrite panel code  
    Airfoil_Data = import_airfoil_polars(airfoil_analysis)
        
    # Get all of the coefficients for AERODAS wings
    neg_post_stall_region = np.linspace(-180, -45, 16) # coarse post-stall refinement
    pos_post_stall_region = np.linspace(45, 180, 16) # coarse post-stall refinement
    mid_region = np.linspace(-45, 45, 25)
    AoA_sweep_deg = np.append(neg_post_stall_region, np.append(mid_region, pos_post_stall_region))
    AoA_sweep_rad = AoA_sweep_deg * Units.degrees       
    
    # Create an infinite aspect ratio wing
    geometry = SUAVE.Components.Wings.Wing()
    geometry.aspect_ratio = np.inf
    geometry.section = Data()  
    
    # AERODAS   
    CL = np.zeros((num_polars, len(AoA_sweep_deg)))
    CD = np.zeros((num_polars, len(AoA_sweep_deg)))  
    for j in range(num_polars):    
        airfoil_cl = Airfoil_Data.lift_coefficients[j,:]
        airfoil_cd = Airfoil_Data.drag_coefficients[j,:]   
        airfoil_aoa = Airfoil_Data.aoa_from_polar[j,:] / Units.degrees 
    
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
def apply_pre_stall_data(AoA_sweep_deg, airfoil_aoa, airfoil_cl, airfoil_cd, CL, CD): 
    '''Applies pre-stall data to lift and drag curve slopes
    
    Assumptions:
    None
    
    Source:
    None
    
    Inputs:
    AoA_sweep_deg  [degrees]
    airfoil_aoa    [degrees]
    airfoil_cl     [unitless]
    airfoil_cd     [unitless]
    CL             [unitless] 
    CD             [unitless]
    
    Outputs
    CL             [unitless]
    CD             [unitless] 
    
    
    Properties Used:
    N/A
    
    '''

    # Coefficients in pre-stall regime taken from experimental data:
    aoa_locs    = (AoA_sweep_deg>=airfoil_aoa[0]) * (AoA_sweep_deg<=airfoil_aoa[-1])
    aoa_in_data = AoA_sweep_deg[aoa_locs]
    
    # if the data is within experimental use it, if not keep the surrogate values
    CL[aoa_locs] = airfoil_cl[abs(aoa_in_data[:,None] - airfoil_aoa[None,:]).argmin(axis=-1)]
    CD[aoa_locs] = airfoil_cd[abs(aoa_in_data[:,None] - airfoil_aoa[None,:]).argmin(axis=-1)]
    
    # remove kinks/overlap between pre- and post-stall                
    data_lb       = np.where(CD == CD[np.argmin(CD - airfoil_cd[0])])[0][0]
    data_ub       = np.where(CD == CD[np.argmin(CD - airfoil_cd[-1])])[0][-1]
    CD[0:data_lb] = np.maximum(CD[0:data_lb], CD[data_lb] * np.ones_like(CD[0:data_lb]))
    CD[data_ub:]  = np.maximum(CD[data_ub:],  CD[data_ub] * np.ones_like(CD[data_ub:])) 
    
    return CL, CD
