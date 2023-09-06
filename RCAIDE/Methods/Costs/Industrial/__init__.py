## @defgroup Methods-Costs-Industrial Industrial 
# @ingroup Methods-Costs
# RCAIDE/Methods/Costs/Industrial/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S.Methods.Costs.Correlations.Industrial_Costs.estimate_hourly_rates          import estimate_hourly_rates
from Legacy.trunk.S.Methods.Costs.Correlations.Industrial_Costs.estimate_escalation_factor     import estimate_escalation_factor
from Legacy.trunk.S.Methods.Costs.Correlations.Industrial_Costs.distribute_non_recurring_cost  import distribute_non_recurring_cost
from Legacy.trunk.S.Methods.Costs.Correlations.Industrial_Costs.compute_industrial_costs       import compute_industrial_costs