## @defgroup Library-Methods-Weights-Correlations-Transport Transport
# RCAIDE/Library/Methods/Weights/Correlations/Transport/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
"""RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S.Methods.Weights.Correlations.Transport.tail_horizontal    import tail_horizontal
from Legacy.trunk.S.Methods.Weights.Correlations.Transport.tail_vertical      import tail_vertical
from Legacy.trunk.S.Methods.Weights.Correlations.Transport.tube               import tube

from .passenger_payload import passenger_payload, func_passenger_payload