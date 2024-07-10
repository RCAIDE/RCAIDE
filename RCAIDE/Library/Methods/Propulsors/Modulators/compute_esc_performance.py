# RCAIDE/Library/Methods/Propulsors/Modulators/compute_esc_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
# compute_electric_rotor_performance
# ----------------------------------------------------------------------------------------------------------------------  
def compute_voltage_out_from_throttle(esc,throttle):
    """ Compute output voltage from electronic speed controller based on throttle  
    
        Assumptions:
            The ESC's output voltage is linearly related to throttle setting

        Source:
            None

        Args:
            esc.inputs.voltage   (numpy.ndarray): voltage      [V]
            throttle             (numpy.ndarray): throttle     [unitless]

        Returns:
            None 
    """  
    # Cap the throttle, negative throttle is bad
    throttle[throttle>=1.0] = 1.0
    throttle[throttle<=0.0] = 0.0
    voltsout = throttle*esc.inputs.voltage
    
    # Pack the output
    esc.outputs.voltage  = voltsout
    
    return


# ----------------------------------------------------------------------------------------------------------------------
# compute_voltage_in_from_throttle
# ----------------------------------------------------------------------------------------------------------------------  
def compute_voltage_in_from_throttle(esc,throttle):
    """ Computes the input voltage from throttle
    
        Assumptions:
            The ESC's output voltage is linearly related to throttle setting

        Source:
            None

        Args:
            esc.outputs.voltage   (numpy.ndarray): voltage     [V]
            throttle             (numpy.ndarray): throttle     [unitless]

        Returns:
            None
    """ 

    # Cap the throttle, negative throttle is bad
    throttle[throttle<=0.0] = 0.0
    throttle[throttle>=1.0] = 1.0
    voltsin = esc.outputs.voltage/throttle

    # Pack the output
    esc.inputs.throttle = throttle
    esc.inputs.voltage  = voltsin

    return


# ----------------------------------------------------------------------------------------------------------------------
# compute_throttle_from_voltages
# ----------------------------------------------------------------------------------------------------------------------  
def compute_throttle_from_voltages(esc): 
    """ Computes ESC throttle from input and output voltages 

        Assumptions:
            The ESC's output voltage is linearly related to throttle setting

        Source:
            None

        Args:
            esc.inputs.voltage   (numpy.ndarray): voltage     [V]
            esc.outputs.voltage   (numpy.ndarray): voltage     [V]

        Returns:
            None  

    """
    throttle  = esc.outputs.voltage/esc.inputs.voltage
    
    # Cap the throttle, negative throttle is bad
    throttle[throttle<=0.0] = 0.0
    throttle[throttle>=1.0] = 1.0
    esc.inputs.throttle = throttle
    return


# ----------------------------------------------------------------------------------------------------------------------
# compute_current_in_from_throttle
# ----------------------------------------------------------------------------------------------------------------------  
def compute_current_in_from_throttle(esc,throttle):
    """ Computes the current going into the electronic speed controller
    
        Assumptions:
            The ESC draws current.
        
        Args: 
            esc.inputs.currentout  (numpy.ndarray): current               [A]
            esc.efficiency         (numpy.ndarray): efficiency of the ESC [unitless] 
           
        Returns:
            None 
    """
    
    # compute current -  the inclusion of throttle satisfies a power balance: p_in = p_out/eff
    currentin  = esc.outputs.current*throttle/esc.efficiency 
    
    # Pack inputs 
    esc.inputs.power     = currentin *  esc.inputs.voltage 
    esc.inputs.current   = currentin
    
    return