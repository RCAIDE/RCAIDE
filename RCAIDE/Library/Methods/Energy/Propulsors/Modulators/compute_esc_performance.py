## @ingroup Methods-Energy-Propulsors-Modulators
# RCAIDE/Library/Methods/Energy/Propulsors/Modulators/compute_esc_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
# compute_electric_rotor_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsors-Modulators
def compute_voltage_out_from_throttle(esc,eta):
    """ The voltage out of the electronic speed controller
    
        Assumptions:
        The ESC's output voltage is linearly related to throttle setting

        Source:
        N/A

        Inputs:
        conditions.energy.throttle     [0-1] 
        esc.inputs.voltage            [volts]

        Outputs:
        voltsout                       [volts]
        esc.outputs.voltageout        [volts]

        Properties Used:
        None
       
    """ 
    # Negative throttle is bad
    eta[eta<=0.0] = 0.0
    
    # Cap the throttle
    eta[eta>=1.0] = 1.0
    voltsout = eta*esc.inputs.voltage
    
    # Pack the output
    esc.outputs.voltage  = voltsout
    
    return


# ----------------------------------------------------------------------------------------------------------------------
# compute_voltage_in_from_throttle
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsors-Modulators
def compute_voltage_in_from_throttle(esc,eta):
    """ The voltage out of the electronic speed controller

        Assumptions:
        The ESC's output voltage is linearly related to throttle setting

        Source:
        N/A

        Inputs:
        conditions.energy.throttle     [0-1]
        esc.inputs.voltage            [volts]

        Outputs:
        voltsout                       [volts]
        esc.outputs.voltageout        [volts]

        Properties Used:
        None

    """
    # Negative throttle is bad
    eta[eta<=0.0] = 0.0

    # Cap the throttle
    eta[eta>=1.0] = 1.0
    voltsin = esc.outputs.voltage/eta

    # Pack the output
    esc.inputs.throttle = eta
    esc.inputs.voltage  = voltsin

    return


# ----------------------------------------------------------------------------------------------------------------------
# compute_throttle_from_voltages
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsors-Modulators
def compute_throttle_from_voltages(esc):

    """ The voltage out of the electronic speed controller

        Assumptions:
        The ESC's output voltage is linearly related to throttle setting

        Source:
        N/A

        Inputs:
        conditions.energy.throttle     [0-1]
        esc.inputs.voltage            [volts]

        Outputs:
        voltsout                       [volts]
        esc.outputs.voltageout        [volts]

        Properties Used:
        None

    """
    eta  = esc.outputs.voltage/esc.inputs.voltage

    # Negative throttle is bad
    eta[eta<=0.0] = 0.0

    # Cap the throttle
    eta[eta>=1.0] = 1.0
    esc.inputs.throttle = eta
    return


# ----------------------------------------------------------------------------------------------------------------------
# compute_current_in_from_throttle
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsors-Modulators
def compute_current_in_from_throttle(esc,eta):
    """ The current going into the speed controller
    
        Assumptions:
            The ESC draws current.
        
        Inputs:
            esc.inputs.currentout [amps]
           
        Outputs:
            outputs.currentin      [amps]
        
        Properties Used:
            esc.efficiency - [0-1] efficiency of the ESC
           
    """
    
    # Unpack, don't modify the throttle   
    eff        = esc.efficiency
    currentout = esc.outputs.current 
    currentin  = currentout*eta/eff # The inclusion of eta satisfies a power balance: p_in = p_out/eff
    
    # Pack 
    esc.inputs.current   = currentin
    esc.inputs.power     = esc.inputs.voltage *currentin
    
    return