from dataclasses import dataclass, field
from RCAIDE.Framework.Core import Process, ProcessStep
from RCAIDE.Framework.Methods.Mass import Correlation as Mass

class TransportMassAnalysis(Process):

    aircraft_type : str = field(default='medium-range')

    def __post_init__(self):

        # Weight Reduction Factors
        self.initial_settings.weight_reduction_factors = dataclass()
        self.initial_settings.weight_reduction_factors.main_wing    = 0.
        self.initial_settings.weight_reduction_factors.fuselage     = 0.
        self.initial_settings.weight_reduction_factors.empennage    = 0.
        self.initial_settings.weight_reduction_factors.systems      = 0.

        # Propulsion Mass
        Prop = ProcessStep()
        Prop.name = 'Propulsion'
        Prop.function = Mass.Propulsion.jet_mass_from_sls

        # Passenger Payload Mass
        Passengers = ProcessStep()
        Passengers.name = 'Payload'
        Passengers.function = Mass.Transport.passenger_payload

        # Operating Items Mass
        Opers = ProcessStep()
        Opers.name = 'Operating Items'
        Opers.function =

        # Systems Mass
        SYS = ProcessStep()
        SYS.name = 'Systems'
        SYS.function =

        # Main Wings Mass
        M_Wings = ProcessStep()
        M_Wings.name = ''
        M_Wings.function =

        # Wings Mass
        Wings = ProcessStep()
        Wings.name = ''
        Wings.function =

        # H-Tail Mass
        H_Tails = ProcessStep()
        H_Tails.name = ''
        H_Tails.function =

        # V-Tail Mass
        V_Tails = ProcessStep()
        V_Tails.name = ''
        V_Tails.function =

        # Fuselage Mass
        Fuselages = ProcessStep()
        Fuselages.name = ''
        Fuselages.function =

        # Landing Gear Mass
        LGs = ProcessStep()
        LGs.name = ''
        LGs.function =



