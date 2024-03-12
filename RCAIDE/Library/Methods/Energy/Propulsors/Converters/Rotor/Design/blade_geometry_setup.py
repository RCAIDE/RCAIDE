## @ingroup Methods-Energy-Propulsors-Rotor_Design  
# RCAIDE/Methods/Energy/Propulsors/Rotor_Design/optimization_setup.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 


# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

# RCAIDE Imports 
import RCAIDE   
from RCAIDE.Methods.Geometry.Two_Dimensional.Airfoil  import compute_airfoil_properties, compute_naca_4series, import_airfoil_geometry

# Python package imports   
import numpy as np  
    
# ----------------------------------------------------------------------------------------------------------------------  
#  Blade Geometry Setup 
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Methods-Energy-Propulsors-Rotor_Design    
def blade_geometry_setup(rotor,number_of_stations): 
    """ Defines a dummy vehicle for prop-rotor blade optimization.
          
          Inputs:  
             rotor   - rotor data structure             [None] 
              
          Outputs:  
             configs - configuration used in optimization    [None]
              
          Assumptions: 
             N/A 
        
          Source:
             None
    """    
    
    # Unpack prop-rotor geometry  
    N                     = number_of_stations       
    B                     = rotor.number_of_blades    
    R                     = rotor.tip_radius
    Rh                    = rotor.hub_radius 
    design_thrust_hover   = rotor.hover.design_thrust
    design_power_hover    = rotor.hover.design_power
    chi0                  = Rh/R  
    chi                   = np.linspace(chi0,1,N+1)  
    chi                   = chi[0:N]
    airfoils              = rotor.Airfoils      
    a_loc                 = rotor.airfoil_polar_stations  
    
    # determine target values 
    if (design_thrust_hover == None) and (design_power_hover== None):
        raise AssertionError('Specify either design thrust or design power at hover!') 
    elif (design_thrust_hover!= None) and (design_power_hover!= None):
        raise AssertionError('Specify either design thrust or design power at hover!')     
    num_airfoils = len(airfoils.keys())
    if num_airfoils>0:
        if len(a_loc) != N:
            raise AssertionError('\nDimension of airfoil sections must be equal to number of stations on propeller') 
        
        for _,airfoil in enumerate(airfoils):  
            if airfoil.geometry == None: # first, if airfoil geometry data not defined, import from geoemtry files
                if airfoil.NACA_4_series_flag: # check if naca 4 series of airfoil from datafile
                    airfoil.geometry = compute_naca_4series(airfoil.coordinate_file,airfoil.number_of_points)
                else:
                    airfoil.geometry = import_airfoil_geometry(airfoil.coordinate_file,airfoil.number_of_points) 
    
            if airfoil.polars == None: # compute airfoil polars for airfoils
                airfoil.polars = compute_airfoil_properties(airfoil.geometry, airfoil_polar_files= airfoil.polar_files) 
                     
    # thickness to chord         
    t_c           = np.zeros(N)    
    if num_airfoils>0:
        for j,airfoil in enumerate(airfoils): 
            a_geo         = airfoil.geometry
            locs          = np.where(np.array(a_loc) == j ) 
            t_c[locs]     = a_geo.thickness_to_chord 
            
    # append additional prop-rotor  properties for optimization  
    rotor.number_of_blades             = int(B)  
    rotor.thickness_to_chord           = t_c
    rotor.radius_distribution          = chi*R  
    
    # set oei conditions if they are not set
    if rotor.oei.design_freestream_velocity == None: 
        rotor.oei.design_freestream_velocity = rotor.hover.design_freestream_velocity
    if rotor.oei.design_altitude == None:
        rotor.oei.design_altitude = rotor.hover.design_altitude
    if design_thrust_hover == None:
        if rotor.oei.design_power == None: 
            rotor.oei.design_power = rotor.hover.design_power*1.1
    elif  design_power_hover == None:
        if rotor.oei.design_thrust == None: 
            rotor.oei.design_thrust = rotor.hover.design_thrust*1.1
    
    vehicle                            = RCAIDE.Vehicle()  
    net                                = RCAIDE.Energy.Networks.All_Electric_Network() 
    bus                                = RCAIDE.Energy.Networks.Distribution.Electrical_Bus()
    propulsor                          = RCAIDE.Energy.Propulsors.Propulsor()
    propulsor.rotor                    = rotor  
    bus.propulsors.append(propulsor)
    net.busses.append(bus)
    vehicle.append_energy_network(net)
    
    configs                             = RCAIDE.Components.Configs.Config.Container()
    base_config                         = RCAIDE.Components.Configs.Config(vehicle) 
    
    config                              = RCAIDE.Components.Configs.Config(base_config)
    config.tag                          = 'hover' 
    config.networks.all_electric.busses.bus.propulsors.propulsor.rotor.orientation_euler_angles = [0.0,np.pi/2,0.0]    
    configs.append(config)        

    config                              = RCAIDE.Components.Configs.Config(base_config)
    config.tag                          = 'oei' 
    config.networks.all_electric.busses.bus.propulsors.propulsor.rotor.orientation_euler_angles = [0.0,np.pi/2,0.0]    
    configs.append(config)       
    
    if type(rotor) == RCAIDE.Energy.Propulsors.Converters.Prop_Rotor:  
        design_thrust_cruise  = rotor.cruise.design_thrust 
        design_power_cruise   = rotor.cruise.design_power      
        if (design_thrust_cruise == None) and (design_power_cruise== None):
            raise AssertionError('Specify either design thrust or design power at cruise!') 
        elif (design_thrust_cruise!= None) and (design_power_cruise!= None):
            raise AssertionError('Specify either design thrust or design power at cruise!') 
        
        config                          = RCAIDE.Components.Configs.Config(base_config)
        config.tag                      = 'cruise'
        config.networks.all_electric.busses.bus.propulsors.propulsor.rotor.orientation_euler_angles = [0.0,np.pi/2,0.0] 
        configs.append(config)
    return configs 