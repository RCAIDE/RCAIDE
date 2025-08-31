# RCAIDE/Library/Missions/Common/Pre_Process/geometry.py
# 
# 
# Created:  Apr 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from ast import Raise
import RCAIDE
from RCAIDE.Library.Methods.Geometry.LOPA      import  compute_layout_of_passenger_accommodations , compute_fuselage_dimensions
from RCAIDE.Library.Methods.Geometry.Planform  import  fuselage_planform, wing_planform, bwb_wing_planform , compute_fuel_volume 

# python imports
import  numpy as  np 
# ----------------------------------------------------------------------------------------------------------------------
#  geometry
# ----------------------------------------------------------------------------------------------------------------------  
def geometry(mission):
    """
    Initializes and processes geometry for mission segments

    Parameters
    ----------
    mission : Mission
        The mission containing segments to be analyzed
            - analyses.geometry : Analysis
                Stability analysis module
                - vehicle : Vehicle
                    Aircraft geometry definition
                    - wings : list
                        Wing geometry definitions
                - process.compute.lift.inviscid_wings : Process
                    Lift computation process
                - surrogates : Data
                    Stability surrogate models
                - reference_values : Data
                    Reference geometry parameters
        
    
    Returns
    -------
    None
        Updates mission segment analyses directly
    
    Notes
    -----
    This function prepares the geometry for each mission segment 
    
    See Also
    --------
    RCAIDE.Library.Methods.Geometry.Planform
    RCAIDE.Framework.Mission.Segments
    """
    for i ,  segment in enumerate(mission.segments): 
        # --------------------------------------------------------------------------------------------------------------------        
        # check if geometry analysis is defined 
        # --------------------------------------------------------------------------------------------------------------------
        if segment.analyses.geometry is None: 
            raise AssertionError('Geometry Analyses not defined') 
        geometry_preprocess_routine(segment.analyses.geometry)
        
    return 
        
def geometry_preprocess_routine(geometry_analysis): 
    vehicle        = geometry_analysis.vehicle
    settings       = geometry_analysis.settings
    
    # initalize variables 
    A_fuselage     = 0
    defined_cabins = False 
    NPF            = 0
    NPB            = 0
    NPE            = 0    
    # ================================================================================================================================================
    # update fuselage properties
    # ================================================================================================================================================  

    for fuselage in vehicle.fuselages: 
        compute_layout_of_passenger_accommodations(fuselage) 
        compute_fuselage_dimensions(fuselage,settings.update_fuselage_properties)
        if fuselage.number_of_passengers > fuselage.layout_of_passenger_accommodations.number_of_seats:
            raise AttributeError('Total number of seats is more than the to number of passengers')  
        fuselage_planform(fuselage) 
        vehicle.length = np.maximum(vehicle.length, fuselage.lengths.total)
        A_fuselage     = np.maximum(A_fuselage,fuselage.areas.front_projected) 
         
        for cabin in fuselage.cabins:
            defined_cabins = True
            for cabin_class in cabin.classes:
                cabin.number_of_passengers += cabin_class.number_of_passengers
                if cabin_class.number_of_seats < cabin_class.number_of_passengers:
                    raise AttributeError('Total number of seats in cabin class is more than the to number of passengers in class') 
                if type(cabin_class) == RCAIDE.Library.Components.Fuselages.Cabins.Classes.Economy:
                    NPE +=  cabin_class.number_of_passengers
                elif type(cabin_class) == RCAIDE.Library.Components.Fuselages.Cabins.Classes.Business:
                    NPB +=  cabin_class.number_of_passengers
                elif type(cabin_class) == RCAIDE.Library.Components.Fuselages.Cabins.Classes.First:
                    NPF +=  cabin_class.number_of_passengers

            if cabin.number_of_passengers == 0:  # enforces that cabin has passegers
                if cabin.number_of_seats < vehicle.number_of_passengers:
                    raise AttributeError('Total number of seats in cabin class is more than the to number of passengers in class') 
        
                cabin.number_of_passengers = vehicle.number_of_passengers                      
                    
    # update landing gear properties 
    for landing_gear in  vehicle.landing_gears:
        if (landing_gear.number_of_gear_types_in_tandem != None) and  (landing_gear.number_of_wheels_in_gear_type != None):
            landing_gear.wheels = landing_gear.number_of_gear_types_in_tandem * landing_gear.number_of_wheels_in_gear_type
            if landing_gear.symmetric:
                landing_gear.wheels *= 2
                
    vehicle.maximum_cross_sectional_area  =  A_fuselage
    
    # ================================================================================================================================================
    # update wing properties 
    # ================================================================================================================================================
    for wing in vehicle.wings:  
        # --------------------------------------------------------------------------------------------------------------------
        #  Blended Wing Body
        # --------------------------------------------------------------------------------------------------------------------
        if isinstance(wing, RCAIDE.Library.Components.Wings.Blended_Wing_Body): 
            compute_layout_of_passenger_accommodations(wing) 
            compute_fuselage_dimensions(wing,settings.update_fuselage_properties) 
            if wing.number_of_passengers > wing.layout_of_passenger_accommodations.number_of_seats:
                raise AttributeError('Total number of seats is more than the to number of passengers')  
            
            # compute planform properties 
            bwb_wing_planform(wing)
            
            # update reference properties 
            if settings.overwrite_reference:
                vehicle.reference_area = wing.areas.reference
     
            for cabin in wing.cabins:
                defined_cabins = True
                cabin.number_of_passengers += cabin_class.number_of_passengers
                for cabin_class in cabin.classes:               
                    for cabin_class in cabin.classes:
                        if cabin_class.number_of_seats < cabin_class.number_of_passengers:
                            raise AttributeError('Total number of seats in cabin class is more than the to number of passengers in class') 
                        if type(cabin_class) == RCAIDE.Library.Components.Fuselages.Cabins.Classes.Economy:
                            NPE +=  cabin_class.number_of_passengers
                        elif type(cabin_class) == RCAIDE.Library.Components.Fuselages.Cabins.Classes.Business:
                            NPB +=  cabin_class.number_of_passengers
                        elif type(cabin_class) == RCAIDE.Library.Components.Fuselages.Cabins.Classes.First:
                            NPF +=  cabin_class.number_of_passengers
            
                if cabin.number_of_passengers == 0: # enforces that cabin has passegers
                    if cabin.number_of_seats < vehicle.number_of_passengers:
                        raise AttributeError('Total number of seats in cabin class is more than the to number of passengers in class') 
            
                    cabin.number_of_passengers = vehicle.number_of_passengers
                        

        # --------------------------------------------------------------------------------------------------------------------
        # All other wing surfaces
        # --------------------------------------------------------------------------------------------------------------------
        else: 
            wing_planform(wing)                   
            if isinstance(wing, RCAIDE.Library.Components.Wings.Main_Wing) and settings.overwrite_reference:
                vehicle.reference_area = wing.areas.reference
             
        # reference chord 
        vehicle.reference_chord  = np.maximum(vehicle.reference_chord , wing.chords.mean_aerodynamic)
        
        # reference span 
        vehicle.reference_span   = np.maximum(vehicle.reference_span  , wing.spans.projected)
        
        # total length 
        vehicle.length = np.maximum(vehicle.length, wing.chords.root)                         
        
        # max cross sectional area 
        A_wing_plus_fuselage   = wing.spans.projected * wing.thickness_to_chord *  wing.chords.root +  A_fuselage
        vehicle.maximum_cross_sectional_area = np.maximum(vehicle.maximum_cross_sectional_area,A_wing_plus_fuselage) 

    # --------------------------------------------------------------------------------------------------------------------
    # Update passenger imformation 
    # --------------------------------------------------------------------------------------------------------------------
  
    if  vehicle.number_of_passengers == 0:
        vehicle.number_of_first_class_passengers     = 0
        vehicle.number_of_business_class_passengers  = 0
        vehicle.number_of_economy_class_passengers   = 0 
        
    else:   
        if defined_cabins:
            if (NPF + NPB + NPE) > vehicle.number_of_passengers:
                raise AttributeError('Total number of seats is more than the to number of passengers') 
            vehicle.number_of_first_class_passengers    = NPF
            vehicle.number_of_business_class_passengers = NPB
            vehicle.number_of_economy_class_passengers  = NPE
        else:  
            vehicle.number_of_first_class_passengers    = vehicle.number_of_passengers / 20.
            vehicle.number_of_business_class_passengers = vehicle.number_of_passengers / 10.
            vehicle.number_of_economy_class_passengers  = vehicle.number_of_passengers - NPF - NPB 
     
    # --------------------------------------------------------------------------------------------------------------------
    # Compute fuel volume  
    # --------------------------------------------------------------------------------------------------------------------
    if settings.update_fuel_volume: 
        total_fuel_mass,total_fuel_volume = compute_fuel_volume(vehicle, update_max_fuel=settings.update_fuel_volume)
        vehicle.mass_properties.fuel = total_fuel_mass  
               
    return 