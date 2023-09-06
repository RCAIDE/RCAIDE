## @defgroup Components-Wings Wings
# RCAIDE/Components/Wings/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

"""RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S.Components.Wings.Wing                      import Wing
from Legacy.trunk.S.Components.Wings.Main_Wing                 import Main_Wing
from Legacy.trunk.S.Components.Wings.Vertical_Tail             import Vertical_Tail
from Legacy.trunk.S.Components.Wings.Horizontal_Tail           import Horizontal_Tail
from Legacy.trunk.S.Components.Wings.Segment                   import Segment, Segment_Container
from Legacy.trunk.S.Components.Wings.All_Moving_Surface        import All_Moving_Surface
from Legacy.trunk.S.Components.Wings.Stabilator                import Stabilator
from Legacy.trunk.S.Components.Wings.Vertical_Tail_All_Moving  import Vertical_Tail_All_Moving

# packages
from . import Control_Surfaces