# regression/scripts/network_battery/cell_test.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE  
from RCAIDE.Core                           import Units, Data 
from RCAIDE.Methods.Power.Battery.Sizing   import initialize_from_mass ,initialize_from_energy_and_power, initialize_from_mass, initialize_from_circuit_configuration, find_mass_gain_rate, find_total_mass_gain
from RCAIDE.Methods.Power.Battery.Ragone   import find_ragone_properties, find_ragone_optimum 

# package imports  
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------  

def main():
    # size the battery 
    Ereq                           = 3000*Units.Wh # required energy for the mission in Joules 
    Preq                           = 2000. # maximum power requirements for mission in W
    
    # instantiate differet battery types 
    numerics                       = Data()
    battery_inputs                 = Data() #create inputs data structure for inputs for testing discharge model
    specific_energy_guess          = 400*Units.Wh/Units.kg 
    battery_al_air                 = RCAIDE.Energy.Storages.Batteries.Aluminum_Air()    
    battery_li_ion                 = RCAIDE.Energy.Storages.Batteries.Lithium_Ion_LFP()
    battery_li_s                   = RCAIDE.Energy.Storages.Batteries.Lithium_Sulfur()
    li_ion_mass                    = 20*Units.kg
      
    # build numerics  
    numerics.time                  = Data()
    numerics.time.integrate        = np.array([[0, 0],[0, 10]])
    numerics.time.differentiate    = np.array([[0, 0],[0, 1]])
    numerics.time.control_points   = np.array([[0], [1]])
    
    # define battery inputs (i.e. current, power)
    battery_inputs.current          = np.array([[100],[100]])*Units.amps
    battery_inputs.power_in         = np.array([[Preq/2.] ,[ Preq]])
    print('battery_inputs=', battery_inputs)
    battery_li_ion.inputs = battery_inputs
    battery_li_ion.pack.maximum_voltage = battery_li_ion.cell.maximum_voltage
    
    # run tests on functionality
    test_initialize_from_energy_and_power(battery_al_air, Ereq, Preq)
    test_mass_gain(battery_al_air, Preq)
    test_find_ragone_properties(specific_energy_guess,battery_li_s, Ereq,Preq)
    test_find_ragone_optimum(battery_li_ion,Ereq,Preq) 
    test_initialize_from_mass(battery_li_ion,li_ion_mass)
    
    # initiate battery energy at fully changed state
    battery_li_ion.pack.current_energy    = np.array([[battery_li_ion.pack.maximum_energy], [battery_li_ion.pack.maximum_energy]]) 
    battery_li_ion.pack.temperature       = np.array([[30],[30]])
    battery_li_ion.cell.charge_throughput = np.array([[0],[0]])
    battery_li_ion.cell.R_growth_factor   = 1
    battery_li_ion.cell.E_growth_factor   = 1 
    
    # run discharge models
    battery_li_ion.energy_calc(numerics)
    print(battery_li_ion)
    #plot_ragone(battery_li_ion, 'lithium ion')
    #plot_ragone(battery_li_s,   'lithium sulfur') 
     
    battery_chemistry     = ['NMC','LFP'] 
    marker                = ['s' ,'o' ,'P']
    linestyles            = ['-','--',':']
    linecolors            = [['green' , 'blue' , 'red' ],['darkgreen', 'darkblue' , 'darkred'], ['limegreen', 'lightblue' , 'pink']]     
    curr                  = [1.5, 3, 6 ] 
    C_rat                 = [0.5,1,2]   
    marker_size           = 8 
    mAh                   = np.array([3550,1500]) 
    V_ul_true  = np.array([[3.9446784139104443,3.5590281079836554],
                           [3.890187851174907,3.546414176818607],
                           [3.698158733645092,3.5211734513546005],])
    bat_temp_true     = np.array([[290.88689276343854,289.1293674284379],
                                  [295.39761123008685,290.03365301513804],
                                  [307.85017179101123,291.84526567740375],])  
 
    plt.rcParams.update({'font.size': 12})
    fig1 = plt.figure('Cell Test') 
    fig1.set_size_inches(12,7)   
    axes1  = fig1.add_subplot(2,3,1)
    axes2  = fig1.add_subplot(2,3,2)    
    axes3  = fig1.add_subplot(2,3,3)
    axes4  = fig1.add_subplot(2,3,4) 
    axes5  = fig1.add_subplot(2,3,5)
    axes6  = fig1.add_subplot(2,3,6)  
    
    for j in range(len(curr)):      
        for i in range(len(battery_chemistry)):   
            configs, analyses = full_setup(curr[j],battery_chemistry[i],mAh[i] )
            analyses.finalize()     
            mission = analyses.missions.base
            results = mission.evaluate()   
            
            # Voltage Regression
            V_ul        = results.segments[0].conditions.energy.battery_0.pack.voltage_under_load[2][0]   
            print('Under load voltage: ' + str(V_ul))
            V_ul_diff   = np.abs(V_ul - V_ul_true[j,i])
            print('Under load voltage difference')
            print(V_ul_diff)
            #assert np.abs((V_ul_diff)/V_ul_true[j,i]) < 1e-6 
            
            # Temperature Regression
            bat_temp        = results.segments[1].conditions.energy.battery_0.cell.temperature[2][0]  
            print('cell temperature: ' + str(bat_temp))
            bat_temp_diff   = np.abs(bat_temp  - bat_temp_true[j,i]) 
            print('cell temperature difference')
            print(bat_temp_diff)
            #assert np.abs((bat_temp_diff)/bat_temp_true[j,i]) < 1e-6    
            
            plot_results(results,j,battery_chemistry[i], axes1, axes2, axes3, axes4, axes5, axes6,
                         marker[i],marker_size,linecolors[i],linestyles[i],C_rat[j])  

    legend_font_size = 12                     
    axes1.set_ylabel('Voltage $(V_{UL}$)')    
    axes1.set_xlabel('Amp-Hours (A-hr)') 
    axes1.legend(loc='upper right', ncol = 2, prop={'size': legend_font_size})  
    axes1.set_ylim([2.5,5]) 
    axes1.set_xlim([0,7])
    axes2.set_xlabel('Amp-Hours (A-hr)') 
    axes2.legend(loc='upper right', ncol = 2, prop={'size': legend_font_size})  
    axes2.set_ylim([2.5,5])   
    axes2.set_xlim([0,7])
    axes3.set_xlabel('Amp-Hours (A-hr)')
    axes3.legend(loc='upper right', ncol = 2, prop={'size': legend_font_size})  
    axes3.set_ylim([2.5,5]) 
    axes3.set_xlim([0,7])

    axes4.set_xlabel('Amp-Hours (A-hr)') 
    axes4.legend(loc='upper right', ncol = 2, prop={'size': legend_font_size})
    axes4.set_ylim([273,320])
    axes4.set_xlim([0,7]) 
    axes5.set_ylabel(r'Temperature ($\degree$C)')    
    axes5.set_xlabel('Amp-Hours (A-hr)')        
    axes5.legend(loc='upper left', ncol = 2, prop={'size': legend_font_size})
    axes5.set_ylim([273,320])
    axes5.set_xlim([0,7]) 
    axes6.set_xlabel('Amp-Hours (A-hr)')     
    axes6.legend(loc='upper left', ncol = 2,  prop={'size': legend_font_size})  
    axes6.set_ylim([273,320])
    axes6.set_xlim([0,7]) 
    
    plt.tight_layout()
    
    return 

def plot_results(results,j,bat_chem, axes1, axes2, axes3, axes4, axes5, axes6,m,ms,lc,ls,C_rat): 
    
    for segment in results.segments.values(): 
        volts         = segment.conditions.energy.battery_0.pack.voltage_under_load[:,0]   
        cell_temp     = segment.conditions.energy.battery_0.cell.temperature[:,0]   
        Amp_Hrs       = segment.conditions.energy.battery_0.cell.charge_throughput[:,0]                   
          
        if j == 0:
            axes1.plot(Amp_Hrs , volts , marker= m , linestyle = ls,  color= lc[0] , markersize=ms   ,label = bat_chem + ': '+ str(C_rat) + ' C') 
            axes4.plot(Amp_Hrs , cell_temp, marker= m , linestyle = ls,  color= lc[0] , markersize=ms,label = bat_chem + ': '+ str(C_rat) + ' C')   
        elif  j == 1: 
            axes2.plot(Amp_Hrs , volts , marker= m , linestyle = ls,  color= lc[1] , markersize=ms   ,label = bat_chem + ': '+ str(C_rat) + ' C') 
            axes5.plot(Amp_Hrs , cell_temp, marker= m , linestyle = ls,  color= lc[1] , markersize=ms,label = bat_chem + ': '+ str(C_rat) + ' C')                   
        elif  j == 2: 
            axes3.plot(Amp_Hrs , volts , marker= m , linestyle = ls,  color= lc[2] , markersize=ms   ,label = bat_chem + ': '+ str(C_rat) + ' C') 
            axes6.plot(Amp_Hrs , cell_temp, marker= m , linestyle = ls,  color= lc[2] , markersize=ms,label = bat_chem + ': '+ str(C_rat) + ' C')       
    return

# ----------------------------------------------------------------------
#   Analysis Setup
# ----------------------------------------------------------------------
def full_setup(current,battery_chemistry,mAh ):

    # vehicle data
    vehicle  = vehicle_setup(current,battery_chemistry)
    configs  = configs_setup(vehicle)

    # vehicle analyses
    configs_analyses = analyses_setup(configs)

    # mission analyses
    mission  = mission_setup(configs_analyses,vehicle,battery_chemistry,current,mAh )
    missions_analyses = missions_setup(mission)

    analyses = RCAIDE.Analyses.Analysis.Container()
    analyses.configs  = configs_analyses
    analyses.missions = missions_analyses 

    return vehicle, analyses


# ----------------------------------------------------------------------
#   Build the Vehicle
# ----------------------------------------------------------------------
def vehicle_setup(current,battery_chemistry): 

    vehicle                       = RCAIDE.Vehicle() 
    vehicle.tag                   = 'battery'   
    vehicle.reference_area        = 1

    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------    
    # mass properties
    vehicle.mass_properties.takeoff         = 1 * Units.kg 
    vehicle.mass_properties.max_takeoff     = 1 * Units.kg 
       
    # ------------------------------------------------------------------        
    #   Main Wing
    # ------------------------------------------------------------------   
    wing                         = RCAIDE.Components.Wings.Wing()
    wing.tag                     = 'main_wing' 
    wing.areas.reference         = 1.
    wing.spans.projected         = 1.
    wing.aspect_ratio            = 1.
    wing.symmetric               = True
    wing.thickness_to_chord      = 0.10
    wing.taper                   = 1.
    wing.dynamic_pressure_ratio  = 1.
    wing.chords.mean_aerodynamic = 1.
    wing.chords.root             = 1.
    wing.chords.tip              = 1.
    wing.origin                  = [[0.0,0.0,0.0]] # meters
    wing.aerodynamic_center      = [0.0,0.0,0.0] # meters
    
    # add to vehicle
    vehicle.append_component(wing)
     

    net                           = RCAIDE.Energy.Networks.Isolated_Battery_Cell()
    net.tag                       ='single_cell_network'   
    net.dischage_model_fidelity   = battery_chemistry

    # Battery    
    if battery_chemistry == 'NMC': 
        battery = RCAIDE.Energy.Storages.Batteries.Lithium_Ion_NMC()
    elif battery_chemistry == 'LFP': 
        battery = RCAIDE.Energy.Storages.Batteries.Lithium_Ion_LFP() 
    battery.charging_voltage                     = battery.cell.nominal_voltage    
    battery.charging_current                     = current   
    battery.convective_heat_transfer_coefficient = 7.17
    net.voltage                                  = battery.cell.nominal_voltage 
    initialize_from_circuit_configuration(battery) 
    net.batteries.append(battery)   
    
    vehicle.mass_properties.takeoff = battery.mass_properties.mass 

    avionics                      = RCAIDE.Energy.Peripherals.Avionics()
    avionics.current              = current 
    net.avionics                  = avionics  

    vehicle.append_energy_network(net)

    return vehicle

def analyses_setup(configs):

    analyses = RCAIDE.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config)
        analyses[tag] = analysis

    return analyses

def base_analysis(vehicle):    
    #   Initialize the Analyses     
    analyses = RCAIDE.Analyses.Vehicle()  
    
    #  Energy
    energy         = RCAIDE.Analyses.Energy.Energy()
    energy.network = vehicle.networks 
    analyses.append(energy)
 
    #  Planet Analysis
    planet  = RCAIDE.Analyses.Planets.Planet()
    analyses.append(planet)
 
    #  Atmosphere Analysis
    atmosphere                 = RCAIDE.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   
 
    return analyses     

def configs_setup(vehicle): 
    configs         = RCAIDE.Components.Configs.Config.Container()  
    base_config     = RCAIDE.Components.Configs.Config(vehicle)
    base_config.tag = 'base' 
    configs.append(base_config)   
    return configs

def mission_setup(analyses,vehicle,battery_chemistry,current,mAh):
 
    #   Initialize the Mission 
    mission                                                                   = RCAIDE.Analyses.Mission.Sequential_Segments()
    mission.tag                                                               = 'cell_cycle_test'   
    Segments                                                                  = RCAIDE.Analyses.Mission.Segments 
    base_segment                                                              = Segments.Segment() 
    base_segment.process.initialize.initialize_battery                        = RCAIDE.Methods.Missions.Segments.Common.Energy.initialize_battery 
    base_segment.process.finalize.post_process.update_battery_state_of_health = RCAIDE.Methods.Missions.Segments.Common.Energy.update_battery_state_of_health    
    discharge_time                    = 0.9 * (mAh/1000)/current * Units.hrs
    
    if battery_chemistry == 'LFP':
        discharge_tag = 'LFP_Discharge'   
        charge_tag    = 'LFP_Charge'   
        
        # Discharge Segment 
        segment                                = Segments.Ground.Battery_Discharge(base_segment) 
        segment.analyses.extend(analyses.base) 
        segment.tag                            = discharge_tag
        segment.time                           = discharge_time 
        segment.battery_energies               = [vehicle.networks.single_cell_network.batteries.lithium_ion_lfp.pack.maximum_energy * 1.]
        segment                                = vehicle.networks.single_cell_network.add_unknowns_and_residuals_to_segment(segment,initial_battery_temperatures = [295] )    
        mission.append_segment(segment)         
        
        # Charge Segment 
        segment                                = Segments.Ground.Battery_Recharge(base_segment)      
        segment.analyses.extend(analyses.base)
        segment.tag                            = charge_tag  
        segment                                = vehicle.networks.single_cell_network.add_unknowns_and_residuals_to_segment(segment,initial_battery_temperatures = [303] )      
        mission.append_segment(segment)  
         
        
    elif battery_chemistry == 'NMC':
        discharge_tag = 'NMC_Discharge'  
        charge_tag    = 'NMC_Recharge'  

        # Discharge Segment 
        segment                                = Segments.Ground.Battery_Discharge(base_segment) 
        segment.analyses.extend(analyses.base) 
        segment.tag                            = discharge_tag
        segment.time                           = discharge_time 
        segment.battery_energies               = [vehicle.networks.single_cell_network.batteries.lithium_ion_nmc.pack.maximum_energy * 1.]
        segment                                = vehicle.networks.single_cell_network.add_unknowns_and_residuals_to_segment(segment,initial_battery_temperatures = [295] )    
        mission.append_segment(segment)         
        
        # Charge Segment 
        segment                                = Segments.Ground.Battery_Recharge(base_segment)      
        segment.analyses.extend(analyses.base)
        segment.tag                            = charge_tag     
        segment                                = vehicle.networks.single_cell_network.add_unknowns_and_residuals_to_segment(segment,initial_battery_temperatures =[303] )      
        mission.append_segment(segment)          
    

    return mission 

def missions_setup(base_mission): 
    # mission container 
    missions      = RCAIDE.Analyses.Mission.Mission.Container() 
    missions.base = base_mission 
    return missions  

def test_mass_gain(battery,power):
    print(battery)
    mass_gain       =find_total_mass_gain(battery)
    print('mass_gain      = ', mass_gain)
    mdot            =find_mass_gain_rate(battery,power)
    print('mass_gain_rate = ', mdot)
    return

def test_initialize_from_energy_and_power(battery,energy,power):
    initialize_from_energy_and_power(battery, energy, power)
    print(battery)
    return

def test_find_ragone_properties(specific_energy,battery,energy,power):
    find_ragone_properties( specific_energy, battery, energy,power)
    print(battery)
    print('specific_energy (Wh/kg) = ',battery.specific_energy/(Units.Wh/Units.kg))
    return

def test_find_ragone_optimum(battery, energy, power):
    find_ragone_optimum(battery,energy,power)
    print(battery)
    print('specific_energy (Wh/kg) = ',battery.specific_energy/(Units.Wh/Units.kg))
    print('max_energy [W-h]=', battery.pack.maximum_energy/Units.Wh)
    return

def test_initialize_from_mass(battery,mass):
    initialize_from_mass(battery,mass)
    print(battery)
    return

if __name__ == '__main__':
    main()
    plt.show()