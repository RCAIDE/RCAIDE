from dataclasses import dataclass, field
from RCAIDE.Framework.Core import Process, ProcessStep
from RCAIDE.

class Weights_Transport(Process):

    def __post_init__(self):

        # Weight Reduction Factors

        self.initial_settings.weight_reduction_factors = dataclass()
        self.initial_settings.weight_reduction_factors.main_wing    = 0.
        self.initial_settings.weight_reduction_factors.fuselage     = 0.
        self.initial_settings.weight_reduction_factors.empennage    = 0.
        self.initial_settings.weight_reduction_factors.systems      = 0.

        # Propulsion Weight

        Prop_Weight = ProcessStep()
        Prop_Weight.name = 'Propulsion Weight'
        Prop_Weight.function = Methods.Propulsion.

