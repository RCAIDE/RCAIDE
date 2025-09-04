# RCAIDE/Methods/Performance/aircraft_loading_diagram.py
# 
# 
# Created:  Dec 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
import RCAIDE
from RCAIDE.Framework.Core import  Data,  Units 
from RCAIDE.Library.Methods.Mass_Properties.estimate_maximum_landing_weight import estimate_maximum_landing_weight

# Pacakge imports 
import numpy as np   

#------------------------------------------------------------------------------
# aircraft_loading_diagram
#------------------------------------------------------------------------------  
def aircraft_loading_diagram(vehicle, number_of_points = 3, aerodynamic_analysis = None, stability_analysis = None,  weights_analysis = None, altitude = None, airspeed = None):
    """
    Computes the loading dragram of an aircraft 
 
 
    Parameters
    --------
    vehicle : Vehicle
        The vehicle instance to be analyzed
    angle_of_attacks : ndarray
        Array of angle of attack values to evaluate [radians]
    mach_numbers : ndarray
        Array of Mach numbers to evaluate 
    altitude : float, optional
        Altitude for atmospheric properties [m], default 0 
 
    Returns
    --------
    results : Data
        Container of analysis results including:
            * Mach : ndarray
                Evaluated Mach numbers
            * alpha : ndarray
                Evaluated angles of attack [rad]
            * loading_lift_coefficient : ndarray
                Computed lift coefficients
            * loading_drag_coefficient : ndarray
                Computed drag coefficients
            * loading_moment_coefficient : ndarray
                Computed Y-moment coefficients
 
    Notes
    -----
    The function uses the US Standard Atmosphere 1976 model for atmospheric properties
    and evaluates aerodynamic coefficients using vortex lattice methods. Can use a surrogate model
    for faster evaluation or just direct evaluation of the aerodynamics. 
 
    **Major Assumptions**
        * Flow is steady and inviscid
        * Small angle approximations apply
        * Linear aerodynamics
        * Atmospheric properties follow US Standard Atmosphere 1976
 
    See Also
    --------
    RCAIDE.Library.Methods.Aerodynamics.Vortex_Lattice_Method
    RCAIDE.Library.Attributes.Atmospheres.Earth.US_Standard_1976
    """
    vehicle.mass_properties.takeoff  = None
    #------------------------------------------------------------------------  
    # Check Input Args
    #------------------------------------------------------------------------
    if altitude == None:
        raise AttributeError('Altitude not set') 
    
    if airspeed  == None:
        raise AttributeError('Airspeed not set')
    
    if aerodynamic_analysis == None:
        raise AttributeError('Aerodynamic analysis not set') 
    
    if weights_analysis  == None:
        raise AttributeError('Weights analysis not set')
    
    if stability_analysis  == None:
        raise AttributeError('Stability analysis not set') 

    # check that cabins are defined with at least one class
    cabin_class_check = False
    
    for fuselage in  vehicle.fuselages: 
        for cabin in fuselage.cabins:
            for _ in cabin.classes:
                cabin_class_check = True
    for wing in vehicle.wings: 
        if isinstance(wing, RCAIDE.Library.Components.Wings.Blended_Wing_Body):
            for cabin in wing.cabins:    
                for _ in cabin.classes:
                    cabin_class_check = True
                    
    if cabin_class_check == False:
        raise AttributeError('At least one cabin class must be defined to create Aircraft mass-C.G. envelope ') 

    # Set up vehicle configs
    configs  = configs_setup(vehicle)

    # create analyses
    analyses = analyses_setup(configs, aerodynamic_analysis,  stability_analysis, weights_analysis)

    # mission analyses 
    mission = mission_setup(analyses, altitude, airspeed)
    
    # create mission instances (for multiple types of missions)
    missions = missions_setup(mission)

    results   = missions.base_mission.evaluate()     
         
    #------------------------------------------------------------------------  
    # Compute Loading Points 
    #------------------------------------------------------------------------
    percent_cargo        =  np.hstack((np.zeros(number_of_points), np.linspace(0, 1, number_of_points)))
    percent_pax          =  np.hstack((np.linspace(0, 1, number_of_points), np.ones(number_of_points)))
    percent_fuel         =  np.linspace(0, 1, number_of_points) 
    
    # create empty data structures 
    loading_lift_coefficient     = np.zeros((len(percent_cargo),len(percent_fuel)))
    loading_drag_coefficient     = np.zeros((len(percent_cargo),len(percent_fuel)))
    loading_moment_coefficient   = np.zeros((len(percent_cargo),len(percent_fuel)))
    loading_neutral_point        = np.zeros((len(percent_cargo),len(percent_fuel)))
    loading_static_margin        = np.zeros((len(percent_cargo),len(percent_fuel)))
    loading_aerodynamic_moment   = np.zeros((len(percent_cargo),len(percent_fuel)))
    loading_mass                 = np.zeros((len(percent_cargo),len(percent_fuel)))  
    
    # compute mass properties of aircraft to get weight distribution
    vehicle_0         = results.segments[0].analyses.weights.vehicle
    weight_breakdown = results.segments[0].analyses.weights.vehicle.mass_properties.weight_breakdown
     
    CARGO =  weight_breakdown.payload.cargo 
    BAG   =  weight_breakdown.payload.baggage 
    PAX   =  weight_breakdown.payload.passengers 
    MTOW  =  vehicle_0.mass_properties.max_takeoff
    OEW   =  weight_breakdown.empty.total
    MLW   =  estimate_maximum_landing_weight(MTOW)   
     
    total_sims = len(percent_cargo) * len(percent_fuel)
    counter    = 0
    for i in range(len(percent_cargo)):
        for j in range(len(percent_fuel)):

            # -------------------------------------------------------------------------
            # Aircraft-Level Properties 
            # -------------------------------------------------------------------------  
            vehicle.mass_properties.takeoff  = None # this ensures that the takeoff weight is computed 
            vehicle.mass_properties.payload  = percent_cargo[i] *CARGO  +  (BAG + PAX) * percent_pax[i]
            vehicle.mass_properties.cargo    = percent_cargo[i] * CARGO
            vehicle.number_of_passengers     = 1 if i == 0 else int(vehicle_0.number_of_passengers * percent_pax[i])

            # -------------------------------------------------------------------------
            # Update Passengers 
            # -------------------------------------------------------------------------            
            # update number of passegers on each cabin class  
            for fuselage in  vehicle.fuselages: 
                for cabin in fuselage.cabins:
                    cabin.filled_seats_arrangement  = 'descending'  
                    for cabin_class in cabin.classes:
                        cabin_class.number_of_passengers =  1 if i == 0 else int(percent_pax[i] *  vehicle_0.fuselages[fuselage.tag].cabins[cabin.tag].classes[cabin_class.tag].number_of_passengers) 
            for wing in vehicle.wings: 
                if isinstance(wing, RCAIDE.Library.Components.Wings.Blended_Wing_Body):
                    for cabin in wing.cabins:    
                        cabin.filled_seats_arrangement  = 'descending'  
                        for cabin_class in cabin.classes:
                            cabin_class.number_of_passengers =  1 if i == 0 else int(percent_pax[i] * vehicle_0.wings[wing.tag].cabins[cabin.tag].classes[cabin_class.tag].number_of_passengers)    
            
            # -------------------------------------------------------------------------
            # Update Fuel 
            # -------------------------------------------------------------------------             
            for network in  vehicle.networks:
                for fuel_line in  network.fuel_lines: 
                    for fuel_tank in fuel_line.fuel_tanks:
                        fuel_tank.fuel.mass_properties.mass = percent_fuel[j] * vehicle_0.networks[network.tag].fuel_lines[fuel_line.tag].fuel_tanks[fuel_tank.tag].fuel.mass_properties.mass
        
            #  run mission
            configs  = configs_setup(vehicle) 
            analyses = analyses_setup(configs, aerodynamic_analysis, stability_analysis,  weights_analysis) 
            mission  = mission_setup(analyses, altitude, airspeed) 
            missions = missions_setup(mission)    
            results = missions.base_mission.evaluate()
            
            segment = results.segments['cruise'] 
            
            # store results 
            loading_lift_coefficient[i,j]    = segment.state.conditions.aerodynamics.coefficients.lift.total[0][0]  
            loading_drag_coefficient[i,j]    = segment.state.conditions.aerodynamics.coefficients.drag.total[0][0]  
            loading_moment_coefficient[i,j]  = segment.state.conditions.static_stability.coefficients.M[0][0]         
            loading_aerodynamic_moment[i,j]  = segment.state.conditions.frames.inertial.total_moment_vector[0][1]
            loading_neutral_point[i,j]       = segment.state.conditions.static_stability.loading_neutral_point[0][0]  
            loading_static_margin[i,j]       = segment.state.conditions.static_stability.loading_static_margin[0][0]
            loading_mass[i,j]                = mission.segments[0].analyses.weights.vehicle.mass_properties.takeoff
            
            counter += 1
            print('***************************************')
            print('Loading Diagram Run:' + str(counter) + ' of ' +  str(total_sims))
            print('***************************************')            

    ## -------------------------------------------------------------------------
    ## Static Margins 
    ## -------------------------------------------------------------------------
    #for k in range(len(loading_static_margins)): 
        ## calculate CG based on static margin 
        #x_cg = loading_neutral_point[i,j]  -  loading_static_margins[k] * reference_chord
        
        ## update vehicle
        #segment.analyses.geometry.vehicle.mass_properties.center_of_gravity[0][0] = x_cg
            
        ##  run mission
        #configs  = configs_setup(vehicle) 
        #analyses = analyses_setup(configs, aerodynamic_analysis, stability_analysis, weights_analysis, update_center_of_gravity = False) 
        #mission  = mission_setup(analyses, altitude, airspeed) 
        #missions = missions_setup(mission)    
        #results = missions.base_mission.evaluate()
        
        ## store results
        #segment = results.segments['cruise'] 
    
        #aero_weight.append(mission.segments[0].analyses.weights.vehicle.mass_properties.takeoff)
        #aero_moment.append(segment.state.conditions.frames.inertial.total_moment_vector[0][1])
        #aero_loading_static_margin.append(segment.state.conditions.static_stability.loading_static_margin[0][0])
        
        #counter += 1
        #print('***************************************')
        #print('Loading Diagram Run:' + str(counter) + ' of ' +  str(total_sims))
        #print('***************************************')

 
    RES = Data(loading_lift_coefficient    = loading_lift_coefficient,
               loading_drag_coefficient    = loading_drag_coefficient,
               loading_moment_coefficient  = loading_moment_coefficient, 
               loading_neutral_point       = loading_neutral_point,         
               loading_static_margin       = loading_static_margin,
               number_of_points            = number_of_points, 
               loading_aerodynamic_moment  = loading_aerodynamic_moment,   
               loading_mass                = loading_mass,               
               MTOW                        = MTOW,          
               OEW                         = OEW, 
               MLW                         = MLW,  
               )
    
    return RES  
 
 
def configs_setup(vehicle): 
    configs     = RCAIDE.Library.Components.Configs.Config.Container() 
    base_config = RCAIDE.Library.Components.Configs.Config(vehicle)
    base_config.tag = 'base'  
    configs.append(base_config) 
    return configs
  
def analyses_setup(configs, aerodynamics,stability, weights, update_center_of_gravity=True):

    analyses = RCAIDE.Framework.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config, aerodynamics,stability, weights, update_center_of_gravity)
        analyses[tag] = analysis

    return analyses
 
def base_analysis(vehicle, aerodynamics,stability, weights,update_center_of_gravity):
    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Framework.Analyses.Vehicle() 
    
    #  Geometry
    geometry = RCAIDE.Framework.Analyses.Geometry.Geometry()
    geometry.vehicle = vehicle 
    geometry.settings.update_fuselage_properties = True
    geometry.settings.update_fuel_volume         = True     
    analyses.append(geometry)

     # ------------------------------------------------------------------
    #  Weights 
    weights.vehicle                 = vehicle 
    weights.settings.FLOPS.fidelity = 'Complex' 
    weights.settings.update_moment_of_inertia    = update_center_of_gravity 
    weights.settings.update_center_of_gravity    = update_center_of_gravity
    weights.print_weight_analysis_report = False
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis  
    aerodynamics.vehicle  = vehicle      
    analyses.append(aerodynamics)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis  
    stability.vehicle  = vehicle      
    analyses.append(stability)       

    # ------------------------------------------------------------------
    #  Energy
    energy          = RCAIDE.Framework.Analyses.Energy.Energy()
    energy.vehicle  = vehicle 
    analyses.append(energy)

    # ------------------------------------------------------------------
    #  Planet Analysis
    planet = RCAIDE.Framework.Analyses.Planets.Earth()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   

    # done!
    return analyses    

def mission_setup(analyses, altitude, airspeed): 
    
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------

    mission = RCAIDE.Framework.Mission.Sequential_Segments()
    mission.tag = 'mission'
  
    Segments = RCAIDE.Framework.Mission.Segments 
    base_segment = Segments.Segment()
    base_segment.state.numerics.solver.type = 'root_finder'

    # ------------------------------------------------------------------    
    #   Cruise Segment 
    # ------------------------------------------------------------------    

    segment = Segments.Single_Point.Set_Speed_Set_Altitude(base_segment)
    segment.tag = "cruise" 
    segment.analyses.extend( analyses.base )  
    segment.altitude  =  35000 *  Units.ft
    segment.air_speed =  450 * Units['knots'] 
    
    # define flight dynamics to model 
    segment.flight_dynamics.force_x                      = True  
    segment.flight_dynamics.force_z                      = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['starboard_propulsor','port_propulsor']]   
    segment.assigned_control_variables.body_angle.active             = True                
    
    mission.append_segment(segment) 
 

    return mission

def missions_setup(mission): 
 
    missions     = RCAIDE.Framework.Mission.Missions() 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
    return missions   
 