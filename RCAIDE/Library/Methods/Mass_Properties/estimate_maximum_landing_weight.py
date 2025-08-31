# RCAIDE/Methods/Mass_Properties/estimate_maximum_landing_weight.py
# 
# 
# Created:  Sep 2025, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
def estimate_maximum_landing_weight(MTOW):
    MLW = 7E-13 *( MTOW **3) - 7E-07 *( MTOW **2)  + 0.8783 *( MTOW)  + 1601.9 
    return MLW