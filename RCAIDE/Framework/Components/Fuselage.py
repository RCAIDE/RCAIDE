# RCAIDE/Library/Components/Fuselage.py
# (c) Copyright 2024 Aerospace Research Community LLC
# Created:  May 2024, J. Smart
# Modified:

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

from RCAIDE.Framework.Component import Component, ComponentRatios

from dataclasses import dataclass, field


#-------------------------------------------------------------------------------
# Fuselage Component
#-------------------------------------------------------------------------------


@dataclass
class Fuselage(Component):

    differential_pressure: float = field(default=0.0)
    fineness: ComponentRatios = ComponentRatios()

    def __post_init__(self):

        if len(self.segments) > 0:
            for segment in self.segments:
                self.add_subcomponent(segment)

        self.add_subcomponent(Component(name='cabin'))

        self.fineness.nose = 0.0
        self.fineness.tail = 0.0

        self.lengths.ordinal_direction = True


