from dataclasses import dataclass, field
from RCAIDE.Framework.Core import Process

class Weights_Transport(Process):

    def __post_init__(self):
        self.initial_settings.weight_reduction_factors = dataclass()
        self.initial_settings.weight_reduction_factors.main_wing = 0.
        self.initial_settings.weight_reduction_factors.fuselage  = 0.
        self.initial_settings.weight_reduction_factors.empennage = 0.

        self.initial_settings.FLOPS = dataclass()
        self.initial_settings.FLOPS.aeroelastic_tailoring_factor = 0.
        self.initial_settings.FLOPS.strut_braced_wing_factor     = 0.
        self.initial_settings.FLOPS.composite_utilization_factor = 0.5

        self.initial_settings.Raymer = dataclass()
        self.initial_settings.Raymer.fuselage_mounted_landing_gear_factor = 1.

    def evaluate(self):
