# RCAIDE/Library/Missions/Common/Pre_Process/geometry.py
# 
# 
# Created:  Apr 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import RCAIDE
from RCAIDE.Library.Methods.Geometry.LOPA      import  compute_layout_of_passenger_accommodations 
from RCAIDE.Library.Methods.Geometry.Planform  import  fuselage_planform, wing_planform, bwb_wing_planform , compute_fuel_volume 

# python imports
import  numpy as  np 
# ----------------------------------------------------------------------------------------------------------------------
#  geometry
# ----------------------------------------------------------------------------------------------------------------------  
def geometry(mission):
    """
  
    """  
    for i ,  segment in enumerate(mission.segments):
         
        # --------------------------------------------------------------------------------------------------------------------        
        # check if geometry analysis is defined 
        # --------------------------------------------------------------------------------------------------------------------
        if segment.analyses.geometry is None: 
            segment.analyses.geometry = RCAIDE.Framework.Analyses.Geometry.Geometry()
            segment.analyses.geometry.vehicle = segment.analyses.energy.vehicle    
                
        vehicle  = segment.analyses.geometry.vehicle
        settings = segment.analyses.geometry.settings 
        
        # update passenger properties
        if  vehicle.passengers > 0: 
            NPF      = vehicle.passengers / 20.
            NPB      = vehicle.passengers / 10.
            NPT      = vehicle.passengers - NPF - NPB 
        else:
            NPF = 0
            NPB = 0
            NPT = 0
            
        # update fuselage properties
        total_length = 0
        A_fuselage   = 0
        for fuselage in vehicle.fuselages: 
            if settings.update_fuselage_properties:                 
                compute_layout_of_passenger_accommodations(fuselage)
                fuselage_planform(fuselage) 
            total_length = np.maximum(total_length, fuselage.lengths.total)
            A_fuselage   = np.maximum(A_fuselage,fuselage.areas.front_projected) 
            
            if len(fuselage.cabins) > 0: 
                for cabin in fuselage.cabins:
                    for cabin_class in cabin.classes:
                        if type(cabin_class) == RCAIDE.Library.Components.Fuselages.Cabins.Classes.Economy:
                            NPT =  cabin_class.number_of_seats_abrest *  cabin_class.number_of_rows
                        elif type(cabin_class) == RCAIDE.Library.Components.Fuselages.Cabins.Classes.Business:
                            NPB =  cabin_class.number_of_seats_abrest *  cabin_class.number_of_rows
                        elif type(cabin_class) == RCAIDE.Library.Components.Fuselages.Cabins.Classes.First:
                            NPF =  cabin_class.number_of_seats_abrest *  cabin_class.number_of_rows   
        # update landing gear properties 
        for landing_gear in  vehicle.landing_gears:
            if (landing_gear.number_of_gear_types_in_tandem != None) and  (landing_gear.number_of_wheels_in_gear_type != None):
                landing_gear.wheels = landing_gear.number_of_gear_types_in_tandem * landing_gear.number_of_wheels_in_gear_type
                if landing_gear.symmetric:
                    landing_gear.wheels *= 2
        
        # update wing properties
        Amax_wing =  0
        for wing in vehicle.wings: 

            # --------------------------------------------------------------------------------------------------------------------
            #  Blended Wing Body
            # --------------------------------------------------------------------------------------------------------------------
            if isinstance(wing, RCAIDE.Library.Components.Wings.Blended_Wing_Body):
                if settings.update_fuselage_properties:
                    compute_layout_of_passenger_accommodations(wing)  
                if settings.update_wing_properties and settings.overwrite_reference:
                    bwb_wing_planform(wing,settings.overwrite_reference)
                    vehicle.reference_area = wing.areas.reference
        
                if len(wing.cabins) > 0:  
                    for cabin in wing.cabins:
                        for cabin_class in cabin.classes:               
                            for cabin_class in cabin.classes:
                                if type(cabin_class) == RCAIDE.Library.Components.Fuselages.Cabins.Classes.Economy:
                                    NPT =  cabin_class.number_of_seats_abrest *  cabin_class.number_of_rows
                                elif type(cabin_class) == RCAIDE.Library.Components.Fuselages.Cabins.Classes.Business:
                                    NPB =  cabin_class.number_of_seats_abrest *  cabin_class.number_of_rows
                                elif type(cabin_class) == RCAIDE.Library.Components.Fuselages.Cabins.Classes.First:
                                    NPF =  cabin_class.number_of_seats_abrest *  cabin_class.number_of_rows   
                                    

            # --------------------------------------------------------------------------------------------------------------------
            # All other wing surfaces
            # --------------------------------------------------------------------------------------------------------------------
            else:
                if settings.update_wing_properties:
                    wing_planform(wing, settings.overwrite_reference) 
                    if isinstance(wing, RCAIDE.Library.Components.Wings.Main_Wing) and settings.overwrite_reference:
                        vehicle.reference_area = wing.areas.reference
            
            # total length 
            total_length = np.maximum(total_length, wing.chords.root)                         
            
            # max cross sectional area 
            A_wing    = wing.spans.projected * wing.thickness_to_chord *  wing.chords.root
            Amax_wing =  np.maximum(Amax_wing,A_wing)
            
        vehicle.maximum_cross_sectional_area  = Amax_wing + A_fuselage
        vehicle.length                        = total_length    

        # --------------------------------------------------------------------------------------------------------------------
        # Update passenger imformation 
        # -------------------------------------------------------------------------------------------------------------------- 
        vehicle.first_class_passengers     = NPF
        vehicle.business_class_passengers  = NPB
        vehicle.economy_class_passengers   = NPT 
                       
        # --------------------------------------------------------------------------------------------------------------------
        # Compute fuel volume  
        # --------------------------------------------------------------------------------------------------------------------
        if settings.update_fuel_volume: 
            compute_fuel_volume(vehicle, update_max_fuel=settings.update_fuel_volume) 
                   
    return 