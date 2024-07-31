## @ingroup Methods-Energy-Propulsors-Modulators
# RCAIDE/Methods/Energy/Propulsors/Modulators/compute_esc_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
# compute_electric_rotor_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsors-Modulators
def compute_voltage_out_from_throttle(esc,esc_conditions,freestream):
    """ The voltage out of the electronic speed controller
    
        Assumptions:
        The ESC's output voltage is linearly related to throttle setting

        Source:
        N/A

        Inputs:
        conditions.energy.throttle     [0-1] 
        esc_conditions.inputs.voltage            [volts]

        Outputs:
        voltsout                       [volts]
        esc_conditions.outputs.voltageout        [volts]

        Properties Used:
        None
       
    """ 
    eta        = esc_conditions.throttle
    
    # Negative throttle is bad
    eta[eta<=0.0] = 0.0
    
    # Cap the throttle
    eta[eta>=1.0] = 1.0
    voltsout = eta*esc_conditions.inputs.voltage
    
    # Pack the output
    esc_conditions.outputs.voltage  = voltsout
    
    return


# ----------------------------------------------------------------------------------------------------------------------
# compute_voltage_in_from_throttle
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsors-Modulators
def compute_voltage_in_from_throttle(esc,esc_conditions,freestream):
    """ The voltage out of the electronic speed controller

        Assumptions:
        The ESC's output voltage is linearly related to throttle setting

        Source:
        N/A

        Inputs:
        conditions.energy.throttle     [0-1]
        esc_conditions.inputs.voltage            [volts]

        Outputs:
        voltsout                       [volts]
        esc_conditions.outputs.voltageout        [volts]

        Properties Used:
        None

    """
    eta        = esc_conditions.throttle
    
    # Negative throttle is bad
    eta[eta<=0.0] = 0.0

    # Cap the throttle
    eta[eta>=1.0] = 1.0
    voltsin = esc_conditions.outputs.voltage/eta

    # Pack the output
    esc_conditions.inputs.throttle = eta
    esc_conditions.inputs.voltage  = voltsin

    return


# ----------------------------------------------------------------------------------------------------------------------
# compute_throttle_from_voltages
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsors-Modulators
def compute_throttle_from_voltages(esc,esc_conditions,freestream):

    """ The voltage out of the electronic speed controller

        Assumptions:
        The ESC's output voltage is linearly related to throttle setting

        Source:
        N/A

        Inputs:
        conditions.energy.throttle     [0-1]
        esc_conditions.inputs.voltage            [volts]

        Outputs:
        voltsout                       [volts]
        esc_conditions.outputs.voltageout        [volts]

        Properties Used:
        None

    """
    eta  = esc_conditions.outputs.voltage/esc_conditions.inputs.voltage

    # Negative throttle is bad
    eta[eta<=0.0] = 0.0

    # Cap the throttle
    eta[eta>=1.0] = 1.0
    esc_conditions.inputs.throttle = eta
    return


# ----------------------------------------------------------------------------------------------------------------------
# compute_current_in_from_throttle
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Propulsors-Modulators
def compute_current_in_from_throttle(esc,esc_conditions,freestream):
    """ The current going into the speed controller
    
        Assumptions:
            The ESC draws current.
        
        Inputs:
            esc_conditions.inputs.currentout [amps]
           
        Outputs:
            outputs.currentin      [amps]
        
        Properties Used:
            esc.efficiency - [0-1] efficiency of the ESC
           
    """
    
    # Unpack, don't modify the throttle
    eta        = esc_conditions.throttle
    eff        = esc.efficiency
    currentout = esc_conditions.outputs.current 
    currentin  = currentout*eta/eff # The inclusion of eta satisfies a power balance: p_in = p_out/eff
    
    # Pack 
    esc_conditions.inputs.current   = currentin
    esc_conditions.inputs.power     = esc_conditions.inputs.voltage *currentin
    
    return