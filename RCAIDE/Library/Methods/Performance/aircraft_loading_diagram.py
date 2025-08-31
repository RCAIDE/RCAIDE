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
import matplotlib.pyplot as plt
import matplotlib.tri as tri

#------------------------------------------------------------------------------
# aircraft_loading_diagram
#------------------------------------------------------------------------------  
def aircraft_loading_diagram(vehicle, aerodynamic_analysis = None, weights_analysis = None, altitude = None, airspeed = None, plot_diagram=True):
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
            * lift_coefficient : ndarray
                Computed lift coefficients
            * drag_coefficient : ndarray
                Computed drag coefficients
            * moment_coefficient : ndarray
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
    
    if weights_analysis  == None:
        raise AttributeError('Weights analysis not set')
     
    aerodynamic_analysis.settings.store_training_data = True
    weights_analysis.print_weight_analysis_report = False

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
    analyses = analyses_setup(configs, aerodynamic_analysis, weights_analysis)

    # mission analyses 
    mission = mission_setup(analyses, altitude, airspeed)
    
    # create mission instances (for multiple types of missions)
    missions = missions_setup(mission)

    results   = missions.base_mission.evaluate()     
         
    #------------------------------------------------------------------------  
    # Compute Loading Points 
    #------------------------------------------------------------------------
    percent_payload      =  np.linspace(0, 1, 5)
    percent_fuel         =  np.linspace(0, 1, 5)
    static_margins       =  np.linspace(-0.5,0.5, 5)
    
    # create empty data structures 
    lift_coefficient     = np.zeros((len(percent_payload),len(percent_fuel)))
    drag_coefficient     = np.zeros((len(percent_payload),len(percent_fuel)))
    moment_coefficient   = np.zeros((len(percent_payload),len(percent_fuel)))
    neutral_point        = np.zeros((len(percent_payload),len(percent_fuel)))
    static_margin        = np.zeros((len(percent_payload),len(percent_fuel)))
    aerodynamic_moment   = np.zeros((len(percent_payload),len(percent_fuel)))
    weight               = np.zeros((len(percent_payload),len(percent_fuel))) 
    aero_weight          = []
    aero_moment          = []
    aero_static_margin   = [] 
    
    # compute mass properties of aircraft to get weight distribution
    vehicle_0         = results.segments[0].analyses.weights.vehicle
    payload_breakdown = results.segments[0].analyses.weights.vehicle.mass_properties.weight_breakdown.payload
    
    PLD   =  payload_breakdown.total
    CARGO =  payload_breakdown.cargo 
    MTOW  =  vehicle_0.mass_properties.max_takeoff
    MLW   =  estimate_maximum_landing_weight(MTOW)
    for i in range(len(percent_payload)):
        for j in range(len(percent_fuel)):

            # -------------------------------------------------------------------------
            # Aircraft-Level Properties 
            # -------------------------------------------------------------------------  
            vehicle.mass_properties.takeoff  = None # this ensures that the takeoff weight is computed 
            vehicle.mass_properties.payload  = percent_payload[i] *PLD 
            vehicle.mass_properties.cargo    = percent_payload[i] * CARGO

            # -------------------------------------------------------------------------
            # Update Passengers 
            # -------------------------------------------------------------------------            
            # update number of passegers on each cabin class  
            for fuselage in  vehicle.fuselages: 
                for cabin in fuselage.cabins:
                    for cabin_class in cabin.classes:
                        cabin_class.number_of_passengers = int(percent_payload[i] *  vehicle_0.fuselages[fuselage.tag].cabins[cabin.tag].classes[cabin_class.tag].number_of_passengers) 
            for wing in vehicle.wings: 
                if isinstance(wing, RCAIDE.Library.Components.Wings.Blended_Wing_Body):
                    for cabin in wing.cabins:    
                        for cabin_class in cabin.classes:
                            cabin_class.number_of_passengers = int(percent_payload[i] * vehicle_0.wings[wing.tag].cabins[cabin.tag].classes[cabin_class.tag].number_of_passengers)    
            
            # -------------------------------------------------------------------------
            # Update Fuel 
            # -------------------------------------------------------------------------             
            for network in  vehicle.networks:
                for fuel_line in  network.fuel_lines: 
                    for fuel_tank in fuel_line.fuel_tanks:
                        fuel_tank.percent_filled = percent_fuel[i]  
        
            #  run mission
            configs  = configs_setup(vehicle) 
            analyses = analyses_setup(configs, aerodynamic_analysis, weights_analysis) 
            mission  = mission_setup(analyses, altitude, airspeed) 
            missions = missions_setup(mission)    
            results = missions.base_mission.evaluate()
            
            segment = results.segments['cruise'] 
            
            # store results
            reference_chord          = segment.analyses.aerodynamics.vehicle.reference_chord
            lift_coefficient[i,j]    = segment.state.conditions.aerodynamics.coefficients.lift.total[0][0]  
            drag_coefficient[i,j]    = segment.state.conditions.aerodynamics.coefficients.drag.total[0][0]  
            moment_coefficient[i,j]  = segment.state.conditions.static_stability.coefficients.M[0][0]         
            aerodynamic_moment[i,j]  = segment.state.conditions.frames.wind.moment_vector[0][1]
            neutral_point[i,j]       = segment.state.conditions.static_stability.neutral_point[0][0]  
            static_margin[i,j]       = segment.state.conditions.static_stability.static_margin[0][0]
            weight[i,j]              = mission.segments[0].analyses.weights.vehicle.mass_properties.takeoff 

            # -------------------------------------------------------------------------
            # Static Margins 
            # -------------------------------------------------------------------------
            for k in range(len(static_margins)): 
                # calculate CG based on static margin 
                x_cg = neutral_point[i,j]  -  static_margins[k] * reference_chord
                
                # update vehicle
                segment.analyses.geometry.vehicle.mass_properties.center_of_gravity[0][0] = x_cg
                    
                #  run mission
                configs  = configs_setup(vehicle) 
                analyses = analyses_setup(configs, aerodynamic_analysis, weights_analysis, update_center_of_gravity = False) 
                mission  = mission_setup(analyses, altitude, airspeed) 
                missions = missions_setup(mission)    
                results = missions.base_mission.evaluate()
                
                # store results
                segment = results.segments['cruise'] 
            
                aero_weight.append(mission.segments[0].analyses.weights.vehicle.mass_properties.takeoff[0][0])
                aero_moment.append( segment.state.conditions.frames.wind.moment_vector[0][1])
                aero_static_margin.append(segment.state.conditions.static_stability.static_margin[0][0])
 
    RES = Data(lift_coefficient    = lift_coefficient,
               drag_coefficient    = drag_coefficient,
               moment_coefficient  = moment_coefficient, 
               neutral_point       = neutral_point,         
               static_margin       = static_margin,        
               aerodynamic_moment  = aerodynamic_moment,   
               weight              = weight,               
               aero_weight         = aero_weight,          
               aero_moment         = aero_moment,       
               aero_static_margin  = aero_static_margin, 
               percent_payload     =  percent_payload, 
               percent_fuel        =  percent_fuel,    
               static_margins      =  static_margins, 
               )   
        
    if plot_diagram: 
        # get plotting style 
        ps      = plot_style()  
    
        parameters = {'axes.labelsize': ps.axis_font_size,
                      'xtick.labelsize': ps.axis_font_size,
                      'ytick.labelsize': ps.axis_font_size,
                      'axes.titlesize': ps.title_font_size}
        plt.rcParams.update(parameters)

        fig  = plt.figure('Aircraft Loading Dragram')
        axis = fig.add_subplot(1,1,1)
        
        # fuel loading line
        y_pts_1  = weight[0, :]  
        y_pts_2  = weight[0, -1]  -  weight[0, :]  
        axis.plot( aerodynamic_moment[:,0], y_pts_1, 'go-')
        axis.plot( aerodynamic_moment[:,0], y_pts_2, 'go-')
        
        # payload loading line
        y_pts_3  = weight[:, 0]  
        y_pts_4  = weight[-1, 0]   -  weight[:, 0]  
        axis.plot( aerodynamic_moment[0, :], y_pts_3, 'bo-')
        axis.plot( aerodynamic_moment[0, :], y_pts_4, 'bo-')
        
        
        # Maximum Takeoff Weight line
        x_pts_MTOW = np.linspace(0, 1E8)
        y_pts_MTOW = np.ones_like(x_pts_MTOW)  *MTOW
        axis.plot(x_pts_MTOW, y_pts_MTOW, 'bo-') 
        
        
        # Maximum Landing Weight line
        x_pts_MLW = np.linspace(0, 1E8)
        y_pts_MLW = np.ones_like(x_pts_MLW)  *MLW
        axis.plot(x_pts_MLW, y_pts_MLW, 'bo-') 
        
        
        # Aerodynamics Lines 
          
        #ngridx = 100
        #ngridy = 200
        #x = np.array(aero_weight) 
        #y = np.array(aero_moment)
        #z = np.array(aero_static_margin) 
        
        ## Create grid values first.
        #xi = np.linspace(-2.1, 2.1, ngridx)
        #yi = np.linspace(-2.1, 2.1, ngridy)
        
        ## Linearly interpolate the data (x, y) on a grid defined by (xi, yi).
        #triang       = tri.Triangulation(x, y)
        #interpolator = tri.LinearTriInterpolator(triang, z)
        #Xi, Yi       = np.meshgrid(xi, yi)
        #zi           = interpolator(Xi, Yi)
         
        #axis.contour(xi, yi, zi, levels=14, linewidths=0.5, colors='k')
        #cntr1  = axis.contourf(xi, yi, zi, levels=14, cmap="RdBu_r") 
        #fig.colorbar(cntr1, ax=axis) 
        #axis.set(xlim=(-2, 2), ylim=(-2, 2)) 
         
    
        axis.set_xlabel('Moment')
        axis.set_ylabel('Weight') 
        set_axes(axis) 
        fig.tight_layout()              
  
    return RES  
 
 
def configs_setup(vehicle): 
    configs     = RCAIDE.Library.Components.Configs.Config.Container() 
    base_config = RCAIDE.Library.Components.Configs.Config(vehicle)
    base_config.tag = 'base'  
    configs.append(base_config) 
    return configs
  
def analyses_setup(configs, aerodynamics, weights, update_center_of_gravity=True):

    analyses = RCAIDE.Framework.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config, aerodynamics, weights, update_center_of_gravity)
        analyses[tag] = analysis

    return analyses
 
def base_analysis(vehicle, aerodynamics, weights,update_center_of_gravity):
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
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis 
    aerodynamics          = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method() 
    aerodynamics.vehicle  = vehicle      
    analyses.append(aerodynamics)   

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
    base_segment.state.numerics.solver = 'root_finder'

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
 