from dataclasses import dataclass, field
from RCAIDE.Framework.Core import Process, ProcessStep
from RCAIDE.Framework.Methods.Mass import Correlation as Mass

class TransportMassAnalysis(Process):

    def __post_init__(self):

        # Weight Reduction Factors

        self.initial_settings.mass_reduction_factors = dataclass()
        self.initial_settings.mass_reduction_factors.main_wing    = 0.
        self.initial_settings.mass_reduction_factors.fuselage     = 0.
        self.initial_settings.mass_reduction_factors.empennage    = 0.
        self.initial_settings.mass_reduction_factors.systems      = 0.

        self.initial_settings.sizing.rudder_fraction = 0.25

        # Propulsion Mass
        Prop = ProcessStep()
        Prop.name = 'Propulsion'
        Prop.function = Mass.Propulsion.jet_mass_from_sls
        self.append(Prop)

        # Passenger Payload Mass
        Passengers = ProcessStep()
        Passengers.name = 'Payload'
        Passengers.function = Mass.Transport.passenger_payload
        self.append(Passengers)

        # Operating Items and Systems Mass
        OpSys = ProcessStep()
        OpSys.name = 'Operating Systems'
        OpSys.function = Mass.Transport.operating_systems
        self.append(OpSys)

        # Main Wing Mass
        M_Wing = ProcessStep()
        M_Wing.name = 'Main Wing'
        M_Wing.function = Mass.Transport.segmented_main_wing
        self.append(M_Wing)

        # H-Tail Mass
        H_Tail = ProcessStep()
        H_Tail.name = 'Horizontal Tail'
        H_Tail.function = Mass.Transport.horizontal_tail
        self.append(H_Tail)

        # V-Tail Mass
        V_Tail = ProcessStep()
        V_Tail.name = 'Vertical Tail'
        V_Tail.function = Mass.Transport.vertical_tail
        self.append(V_Tail)

        # Fuselage Mass
        Fuselages = ProcessStep()
        Fuselages.name = 'Fuselage'
        Fuselages.function = Mass.Transport.fuselage
        self.append(Fuselages)

        # Landing Gear Mass
        LG = ProcessStep()
        LG.name = 'Landing Gear'
        LG.function = Mass.Transport.landing_gear
        self.append(LG)



