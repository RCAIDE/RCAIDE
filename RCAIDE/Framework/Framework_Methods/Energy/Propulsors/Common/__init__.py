## @defgroup Framework-Methods-Energy-Propulsors " + f"Common
# RCAIDE/Library/Methods/Energy/Propulsors/Common/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Energy-Propulsors

from .Legacy.trunk.S.Methods.Propulsion.fm_id import _fm_id as fm_id
from .Legacy.trunk.S.Methods.Propulsion.fm_solver import _fm_solver as fm_solver
from .Legacy.trunk.S.Methods.Propulsion.rayleigh import _rayleigh as rayleigh
from .Legacy.trunk.S.Methods.Propulsion.nozzle_calculations import _exit_Mach_shock as exit_Mach_shock
from .Legacy.trunk.S.Methods.Propulsion.nozzle_calculations import _mach_area as mach_area
from .Legacy.trunk.S.Methods.Propulsion.nozzle_calculations import _normal_shock as normal_shock
from .Legacy.trunk.S.Methods.Propulsion.nozzle_calculations import _pressure_ratio_isentropic as pressure_ratio_isentropic
from .Legacy.trunk.S.Methods.Propulsion.nozzle_calculations import _pressure_ratio_shock_in_nozzle as pressure_ratio_shock_in_nozzle
