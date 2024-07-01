## @ingroup Library-Methods-Energy-Sources-Battery-Lithium_Ion_Generic
# RCAIDE/Library/Methods/Energy/Sources/Battery/Lithium_Ion_Generic/compute_generic_li_cell_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Feb 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from RCAIDE.Library.Methods.Energy.Sources.Battery.Lithium_Ion_LFP import compute_lfp_cell_performance
# ----------------------------------------------------------------------------------------------------------------------
# compute_generic_li_cell_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Sources-Batteries-Lithium_Ion_Generic 
def compute_generic_li_cell_performance(battery,state,bus,battery_discharge_flag): 
    """This computes the electric performance of a generic Li-ion cell  
       
       Assumptions:
          Dsischarge model for the LFP cell is used 
       
       Source:
          None 
       
       Args:
            battery                         (dict): battery data structure              [-] 
            state                           (dict): operating conditions                [-]
            bus                             (dict): data structure of electric bus      [-]
            battery_discharge_flag       (boolean): current flow flag                   [unitless] 
       
       Returns:
           None  
    """ 
    compute_lfp_cell_performance(battery,state,bus,battery_discharge_flag)
    return       