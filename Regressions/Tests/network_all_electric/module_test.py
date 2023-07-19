# battery_cell_discharge_tests.py 
# 
# Created: Sep 2021, M. Clarke  

#----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
import sys
sys.path.append('../trunk')
import RCAIDE  
from RCAIDE.Core import Units, Data 
from RCAIDE.Methods.Power.Battery.Sizing import initialize_from_mass  
from RCAIDE.Components.Energy.Storages.Batteries import Battery 
from RCAIDE.Methods.Power.Battery.Sizing import initialize_from_energy_and_power, initialize_from_mass, initialize_from_circuit_configuration 
from RCAIDE.Methods.Thermal_Management.Batteries.Channel_Cooling.size_wavy_channel_heat_exchanger  import size_wavy_channel_heat_exchanger 
import numpy as np
import matplotlib.pyplot as plt


def main():
 
    battery_chemistry     = ['NMC']# ,'LFP'] 
    marker                = [['s' ,'s' ,'s' ,'s','s'],['o' ,'o' ,'o' ,'o','o'],['P' ,'P' ,'P' ,'P','P']]
    linestyles            = [['-' ,'-' ,'-' ,'-','-'], ['--' ,'--' ,'--' ,'--'],[':' ,':' ,':' ,':']]
    linecolors            = [['green' , 'blue' , 'red' , 'orange' ],['darkgreen', 'darkblue' , 'darkred'  ,'brown'], ['limegreen', 'lightblue' , 'pink'  ,'yellow']]     
    curr                  = [3] 
    C_rat                 = [1]   
    marker_size           = 8 
    mAh                   = np.array([3550,1500])  
 
    plt.rcParams.update({'font.size': 12})
    fig1 = plt.figure('Cell Comparison') 
    fig1.set_size_inches(12,7)   
    axes1  = fig1.add_subplot(1,2,1)
    axes2  = fig1.add_subplot(1,2,2)     
    
    for j in range(len(curr)):      
        for i in range(len(battery_chemistry)):   
            configs, analyses = full_setup()
            analyses.finalize()     
            mission = analyses.missions.base
            results = mission.evaluate()    
            
            plot_results(results,j,axes1, axes2, marker[i][j],marker_size,linecolors[i][j],linestyles[i][j])  

    #legend_font_size = 12                     
    axes1.set_ylabel('Voltage $(V_{UL}$)')    
    axes1.set_xlabel('Time (min)') 
    #axes1.legend(loc='upper right', prop={'size': legend_font_size})  
      
    
    axes2.set_ylabel(r'Temperature ($\degree$C)')    
    axes2.set_xlabel('Amp-Hours (A-hr)')        
    #axes2.legend(loc='upper left', prop={'size': legend_font_size})
    axes2.set_xlabel('Time (min)') 
     
    plt.tight_layout()
    
    return 

def plot_results(results,j, axes1, axes2,m,ms,lc,ls): 
    
    for segment in results.segments.values():
        time          = segment.conditions.frames.inertial.time[:,0]/60 
        volts         = segment.conditions.propulsion.battery.pack.voltage_under_load[:,0]   
        cell_temp     = segment.conditions.propulsion.battery.cell.temperature[:,0]    
        axes1.plot(time  , volts , marker= m , linestyle = ls,  color= lc , markersize=ms  ) 
        axes2.plot(time  , cell_temp, marker= m , linestyle = ls,  color= lc , markersize=ms)    
     
         
    return

# ----------------------------------------------------------------------
#   Analysis Setup
# ----------------------------------------------------------------------
def full_setup():

    # vehicle data
    vehicle  = vehicle_setup()
    configs  = configs_setup(vehicle)

    # vehicle analyses
    configs_analyses = analyses_setup(configs)

    # mission analyses
    mission  = mission_setup(configs_analyses,vehicle)
    missions_analyses = missions_setup(mission)

    analyses = RCAIDE.Analyses.Analysis.Container()
    analyses.configs  = configs_analyses
    analyses.missions = missions_analyses


    return vehicle, analyses


# ----------------------------------------------------------------------
#   Build the Vehicle
# ----------------------------------------------------------------------
def vehicle_setup(): 

    vehicle                       = RCAIDE.Vehicle() 
    vehicle.tag                   = 'battery'   
    vehicle.reference_area        = 1

    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------    
    # mass properties
    vehicle.mass_properties.takeoff         = 100*0.048 * Units.kg 
    vehicle.mass_properties.max_takeoff     = 100*0.048 * Units.kg 
    
    # basic parameters
    vehicle.reference_area      = 1.    
    # ------------------------------------------------------------------        
    #   Main Wing
    # ------------------------------------------------------------------   
    wing                         = RCAIDE.Components.Wings.Wing()
    wing.tag                     = 'main_wing' 
    wing.areas.reference         = 1.
    wing.spans.projected         = 1.
    wing.aspect_ratio            = 1.
    wing.symmetric               = True
    wing.thickness_to_chord      = 0.12
    wing.taper                   = 1.
    wing.dynamic_pressure_ratio  = 1.
    wing.chords.mean_aerodynamic = 1.
    wing.chords.root             = 1.
    wing.chords.tip              = 1.
    wing.origin                  = [[0.0,0.0,0.0]] # meters
    wing.aerodynamic_center      = [0.0,0.0,0.0] # meters
    
    # add to vehicle
    vehicle.append_component(wing)
     

    net                           = RCAIDE.Components.Energy.Networks.Battery_Cell_Cycler()
    net.tag                       ='battery_cell'    

    # Component 5: the Battery  
    air_cooled_flag  = False
    bat                                                  = RCAIDE.Components.Energy.Storages.Batteries.Constant_Mass.Lithium_Ion_LiNiMnCoO2_18650() 
    bat.pack.electrical_configuration.series             = 10 
    bat.pack.electrical_configuration.parallel           = 10 
    bat.pack.electrical_configuration.total              = bat.pack.electrical_configuration.series * bat.pack.electrical_configuration.parallel 
    initialize_from_circuit_configuration(bat)            
    bat.module_config.number_of_modules                  = 1     
    bat.module.geometrtic_configuration.normal_count     = 10
    bat.module.geometrtic_configuration.parallel_count   = 10 
    bat.module.geometrtic_configuration.total            = 100
    bat.module_config.voltage                            = bat.pack.max_voltage/bat.module_config.number_of_modules
    net.voltage                                          = bat.pack.max_voltage 

    # Component 6: the BTMS 
    if air_cooled_flag:
        btms  = RCAIDE.Components.Energy.Thermal_Management.Batteries.Direct_Convection_Cooling.Atmospheric_Air_Convection_Heat_Exchanger()  
        btms.cooling_fluid.flowspeed                  = 1.0                                     
        btms.convective_heat_transfer_coefficient     = 35.     # [W/m^2K]  
        bat.thermal_management_system                 = btms
    else:
        btms = RCAIDE.Components.Energy.Thermal_Management.Batteries.Channel_Cooling.Wavy_Channel_Gas_Liquid_Heat_Exchanger()
        btms.heat_exchanger.length_of_hot_fluid                        = 0.6
        btms.heat_exchanger.length_of_cold_fluid                       = 0.9
        btms.heat_exchanger.stack_height                               = 0.24
        btms.heat_exchanger.hydraulic_diameter_of_hot_fluid_channel    = 5e-4
        btms.heat_exchanger.aspect_ratio_of_hot_fluid_channel          = 1
        btms.heat_exchanger.hydraulic_diameter_of_cold_fluid_channel   = 1e-2
        btms.heat_exchanger.aspect_ratio_of_cold_fluid_channel         = 3 
        btms.heat_exchanger.mass_flow_rate_of_cold_fluid               = 2  
        btms.heat_exchanger.pressure_ratio_of_hot_fluid                = 0.7
        btms.heat_exchanger.pressure_ratio_of_cold_fluid               = 0.98    # CHANGE IN OPTIMIZER
        btms.heat_exchanger.pressure_at_inlet_of_hot_fluid             = 101325
        btms.wavy_channel.channel_numbers_of_module                    = 10 
        btms.mass_flow_rate_of_hot_fluid                               = 1       # CHANGE IN OPTIMIZER
        size_wavy_channel_heat_exchanger(btms,bat,bat.pack.electrical_configuration.total)  
        bat.thermal_management_system = btms
    net.battery                                          = bat 
    
    initialize_from_circuit_configuration(bat) 
    net.battery                     = bat  
    
    vehicle.mass_properties.takeoff = bat.mass_properties.mass 

    avionics                      = RCAIDE.Components.Energy.Peripherals.Avionics()
    avionics.current              = 108 # C rate of 3
    net.avionics                  = avionics  

    vehicle.append_component(net)

    return vehicle

def analyses_setup(configs):

    analyses = RCAIDE.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config)
        analyses[tag] = analysis

    return analyses

def base_analysis(vehicle):   
    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Analyses.Vehicle()

    # ------------------------------------------------------------------
    #  Basic Geometry Relations
    sizing = RCAIDE.Analyses.Sizing.Sizing()
    sizing.features.vehicle = vehicle
    analyses.append(sizing)

    # ------------------------------------------------------------------
    #  Weights
    weights = RCAIDE.Analyses.Weights.Weights_eVTOL()
    weights.vehicle = vehicle
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics = RCAIDE.Analyses.Aerodynamics.Fidelity_Zero() 
    aerodynamics.geometry = vehicle
    aerodynamics.settings.drag_coefficient_increment = 0.0000
    analyses.append(aerodynamics)  

    # ------------------------------------------------------------------	
    #  Stability Analysis	
    stability = RCAIDE.Analyses.Stability.Fidelity_Zero()    	
    stability.geometry = vehicle	
    analyses.append(stability) 

    # ------------------------------------------------------------------
    #  Energy
    energy= RCAIDE.Analyses.Energy.Energy()
    energy.network = vehicle.networks 
    analyses.append(energy)

    # ------------------------------------------------------------------
    #  Planet Analysis
    planet = RCAIDE.Analyses.Planets.Planet()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere = RCAIDE.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   

    # done!
    return analyses    



def configs_setup(vehicle): 
    configs         = RCAIDE.Components.Configs.Config.Container()  
    base_config     = RCAIDE.Components.Configs.Config(vehicle)
    base_config.tag = 'base' 
    configs.append(base_config)   
    return configs

def mission_setup(analyses,vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------

    mission     = RCAIDE.Analyses.Mission.Sequential_Segments()
    mission.tag = 'the_mission'  
       
    # unpack Segments module
    Segments     = RCAIDE.Analyses.Mission.Segments

    # base segment
    base_segment                                                              = Segments.Segment()
    ones_row                                                                  = base_segment.state.ones_row
    base_segment.process.initialize.initialize_battery                        = RCAIDE.Methods.Missions.Segments.Common.Energy.initialize_battery 
    base_segment.process.finalize.post_process.update_battery_state_of_health = RCAIDE.Methods.Missions.Segments.Common.Energy.update_battery_state_of_health    
    
   
    bat                                                      = vehicle.networks.battery_cell.battery    
    base_segment.max_energy                                  = bat.pack.max_energy
    base_segment.charging_SOC_cutoff                         = bat.cell.charging_SOC_cutoff 
    base_segment.charging_current                            = bat.charging_current
    base_segment.charging_voltage                            = bat.charging_voltage 
    discharge_time                                           = 0.33 * Units.hrs  # approx 3C
    
    # Discharge Segment 
    segment                                             = Segments.Ground.Battery_Charge_Discharge(base_segment) 
    segment.analyses.extend(analyses.base)       
    segment.tag                                         = 'NMC_Module_Discharge'
    segment.time                                        = discharge_time 
    segment.battery_energy                              = bat.pack.max_energy * 1.
    segment = vehicle.networks.battery_cell.add_unknowns_and_residuals_to_segment(segment,initial_battery_cell_temperature = 295 )    
    mission.append_segment(segment)         
    
    # Charge Segment 
    segment                   = Segments.Ground.Battery_Charge_Discharge(base_segment)      
    segment.analyses.extend(analyses.base) 
    segment.tag               = 'NMC_Module_Charge'
    segment.battery_discharge = False        
    segment = vehicle.networks.battery_cell.add_unknowns_and_residuals_to_segment(segment,initial_battery_cell_temperature = 303 )      
    mission.append_segment(segment) 
         

    return mission 

def missions_setup(base_mission):

    # the mission container
    missions = RCAIDE.Analyses.Mission.Mission.Container()

    # ------------------------------------------------------------------
    #   Base Mission
    # ------------------------------------------------------------------
    missions.base = base_mission

    # done!
    return missions    

if __name__ == '__main__':
    main()
    plt.show()