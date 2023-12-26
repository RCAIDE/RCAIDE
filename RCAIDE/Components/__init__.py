## @defgroup Components Components
# RCAIDE/Components/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

"""RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S.Components.Component import Component
from Legacy.trunk.S.Components.Mass_Properties import Mass_Properties
from Legacy.trunk.S.Components.Physical_Component import Physical_Component
from Legacy.trunk.S.Components.Lofted_Body import Lofted_Body
from Legacy.trunk.S.Components.Envelope import Envelope

from . import Airfoils
from . import Booms
from . import Configs
from . import Costs
from . import Fuselages
from . import Landing_Gear
from . import Lofted_Body_Segment
from . import Nacelles
from . import Payloads
from . import Systems
from . import Wings