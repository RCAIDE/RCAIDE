from abc import ABC
from dataclasses import dataclass
from RCAIDE.Framework.Core import Process, ProcessStep
from RCAIDE.Library.Methods.Mass import Correlation as Mass


@dataclass(kw_only=True)
class TransportMassAnalysis(Process):
    """
    Transport Mass Analysis Class

    This class is used to perform mass analysis for a transport aircraft. It inherits from the `Process` class.

    Attributes
    ----------
    main_wing_mass_reduction_factor : float
        The mass reduction factor for the main wing.
    fuselage_mass_reduction_factor : float
        The mass reduction factor for the fuselage.
    empennage_mass_reduction_factor : float
        The mass reduction factor for the empennage.
    systems_mass_reduction_factor : float
        The mass reduction factor for the systems.
    rudder_sizing_fraction : float
        The rudder area as a fraction of the main wing area.

    Methods
    -------
    __post_init__():
        Initializes the settings for the mass analysis.

        If the appropriate datastructures aren't already in settings, creates them.
        Maps analysis settings into settings datastructure for later retrieval.
        Adds default process steps for mass calculations.
    """

    # Make settings analysis class attributes so that users can see what settings can/must be set when initializing
    # an instance of this analysis, and so that they appear in the docstring of the analysis

    # Mass Reduction Factors
    main_wing_mass_reduction_factor: float = 0.
    fuselage_mass_reduction_factor: float = 0.
    empennage_mass_reduction_factor: float = 0.
    systems_mass_reduction_factor: float = 0.

    # Rudder Sizing Fraction
    rudder_sizing_fraction: float = 0.25

    def __post_init__(self):
        # If the appropriate datastructures aren't already in settings, create them:
        if 'mass_reduction_factors' not in vars(self.initial_settings).keys():
            self.initial_settings.mass_reduction_factors = dataclass()
        if 'sizing' not in vars(self.initial_settings).keys():
            self.initial_settings.sizing = dataclass()

        # Map analysis settings into settings datastructure for later retreival
        self.initial_settings.mass_reduction_factors.main_wing    = self.main_wing_mass_reduction_factor
        self.initial_settings.mass_reduction_factors.fuselage     = self.fuselage_mass_reduction_factor
        self.initial_settings.mass_reduction_factors.empennage    = self.empennage_mass_reduction_factor
        self.initial_settings.mass_reduction_factors.systems      = self.systems_mass_reduction_factor

        self.initial_settings.sizing.rudder_fraction              = self.rudder_sizing_fraction

        ###---Default Process Steps---###

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
