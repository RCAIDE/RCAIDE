## @defgroup Framework-Methods-Costs " + f"Industrial_Costs
# RCAIDE/Library/Methods/Costs/Industrial_Costs/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Costs

from .Legacy.trunk.S.Methods.Costs.Correlations.Industrial_Costs.estimate_hourly_rates import _estimate_hourly_rates as estimate_hourly_rates
from .Legacy.trunk.S.Methods.Costs.Correlations.Industrial_Costs.estimate_escalation_factor import _estimate_escalation_factor as estimate_escalation_factor
from .Legacy.trunk.S.Methods.Costs.Correlations.Industrial_Costs.distribute_non_recurring_cost import _distribute_non_recurring_cost as distribute_non_recurring_cost
from .Legacy.trunk.S.Methods.Costs.Correlations.Industrial_Costs.compute_industrial_costs import _compute_industrial_costs as compute_industrial_costs
