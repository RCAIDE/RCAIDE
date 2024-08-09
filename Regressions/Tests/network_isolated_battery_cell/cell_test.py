# Regression/scripts/network_isolated_battery_cell/cell_test.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE  
from RCAIDE.Framework.Core                                    import Units, Data 
from RCAIDE.Library.Methods.Energy.Sources.Battery.Common   import initialize_from_mass ,initialize_from_energy_and_power, initialize_from_mass, find_mass_gain_rate, find_total_mass_gain, find_ragone_properties, find_ragone_optimum  
from RCAIDE.Framework.Mission.Common                 import Conditions
from RCAIDE.Library.Plots                           import * 

# package imports  
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.cm as cm

# local imports 
import sys 
sys.path.append('../../Vehicles') 
from Isolated_Battery_Cell   import vehicle_setup , configs_setup  

# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------  

def main(): 
    Ereq                           = 3000*Units.Wh  
    Preq                           = 2000.  
    
    # Aluminum Air Battery Test 
    aluminum_air_battery_test(Ereq,Preq)
    
    # Lithium Sulfur Test 
    lithium_sulphur_battery_test(Ereq,Preq)
    
    # Lithium-Ion Test
    lithium_ion_battery_test(Ereq,Preq)
    return 
     
def aluminum_air_battery_test(Ereq,Preq): 
    battery_al_air                 = RCAIDE.Library.Components.Energy.Sources.Batteries.Aluminum_Air()    
    test_initialize_from_energy_and_power(battery_al_air, Ereq, Preq)
    test_mass_gain(battery_al_air, Preq)
    return 
   
def lithium_sulphur_battery_test(Ereq,Preq):   
    battery_li_s                   = RCAIDE.Library.Components.Energy.Sources.Batteries.Lithium_Sulfur()
    specific_energy_guess          = 400*Units.Wh/Units.kg 
    test_find_ragone_properties(specific_energy_guess,battery_li_s, Ereq,Preq) 
    plot_battery_ragone_diagram(battery_li_s,   save_filename =  'lithium_sulfur')     
    return 

def lithium_ion_battery_test(Ereq,Preq):  
    battery_li_ion                        = RCAIDE.Library.Components.Energy.Sources.Batteries.Lithium_Ion_LFP() 
    battery_li_ion.outputs                = Data() 
    battery_li_ion.outputs.current        = np.array([[100],[100]])*Units.amps
    battery_li_ion.outputs.power          = np.array([[Preq/2.] ,[ Preq]])   
    battery_li_ion.pack.maximum_voltage   = battery_li_ion.cell.maximum_voltage
    test_find_ragone_optimum(battery_li_ion,Ereq,Preq)   
    test_initialize_from_mass(battery_li_ion,20*Units.kg)   
    
    bus,state  = set_up_conditions(battery_li_ion) 
     
    battery_li_ion.energy_calc(state,bus) 
    plot_battery_ragone_diagram(battery_li_ion, save_filename =  'lithium_ion')
     
    battery_chemistry     = ['lithium_ion_nmc','lithium_ion_lfp'] 
    marker                = ['s' ,'o' ,'P']
    linestyles            = ['-','--',':']
    linecolors            = cm.inferno(np.linspace(0.2,0.8,3))    
    curr                  = [1.5,3]  
    C_rat                 = [0.5,1]  
    marker_size           = 5 
    mAh                   = np.array([3550,1500]) 
    V_ul_true             = np.array([[3.975168373018457,3.6014784556230786], [3.9183378825662967,3.6144686722140595]])
    bat_temp_true         = np.array([[289.97131015127644,288.5183202197621], [293.3954825563414,289.1586753541579]])  
 
    plt.rcParams.update({'font.size': 12})
    fig1 = plt.figure('Cell Test') 
    fig1.set_size_inches(12,7)   
    axes1  = fig1.add_subplot(3,2,1)
    axes2  = fig1.add_subplot(3,2,2)  
    axes3  = fig1.add_subplot(3,2,3) 
    axes4  = fig1.add_subplot(3,2,4) 
    axes5  = fig1.add_subplot(3,2,5) 
    axes6  = fig1.add_subplot(3,2,6) 
    
    fixed_bus_voltage = False 
    for j in range(len(curr)):      
        for i in range(len(battery_chemistry)):   
            vehicle  = vehicle_setup(curr[j],battery_chemistry[i],fixed_bus_voltage) 
            
            # Set up vehicle configs
            configs  = configs_setup(vehicle)
        
            # create analyses
            analyses = analyses_setup(configs)
        
            # mission analyses
            mission  = mission_setup(analyses,vehicle,battery_chemistry[i],curr[j],mAh[i]) 
            
            # create mission instances (for multiple types of missions)
            missions = missions_setup(mission) 
             
            # mission analysis 
            results = missions.base_mission.evaluate()  
            
            # Voltage Regression
            V_ul        = results.segments[0].conditions.energy.bus[battery_chemistry[i]].pack.voltage_under_load[2][0]   
            print('Under load voltage: ' + str(V_ul))
            V_ul_diff   = np.abs(V_ul - V_ul_true[j,i])
            print('Under load voltage difference')
            print(V_ul_diff)
            assert np.abs((V_ul_diff)/V_ul_true[j,i]) < 1e-6 
            
            # Temperature Regression
            bat_temp        = results.segments[1].conditions.energy.bus[battery_chemistry[i]].cell.temperature[2][0]  
            print('cell temperature: ' + str(bat_temp))
            bat_temp_diff   = np.abs(bat_temp  - bat_temp_true[j,i]) 
            print('cell temperature difference')
            print(bat_temp_diff)
            assert np.abs((bat_temp_diff)/bat_temp_true[j,i]) < 1e-6    
           
       
            for segment in results.segments.values(): 
                volts         = segment.conditions.energy.bus[battery_chemistry[i]].pack.voltage_under_load[:,0] 
                SOC           = segment.conditions.energy.bus[battery_chemistry[i]].cell.state_of_charge[:,0]   
                cell_temp     = segment.conditions.energy.bus[battery_chemistry[i]].cell.temperature[:,0]   
                Amp_Hrs       = segment.conditions.energy.bus[battery_chemistry[i]].cell.charge_throughput[:,0]                   
                  
                if battery_chemistry[i] == 'lithium_ion_nmc':
                    axes1.plot(Amp_Hrs , volts , marker= marker[i], linestyle = linestyles[i],  color= linecolors[j]  , markersize=marker_size   ,label = battery_chemistry[i] + ': '+ str(C_rat[j]) + ' C') 
                    axes3.plot(Amp_Hrs , SOC   , marker= marker[i] , linestyle = linestyles[i],  color= linecolors[j], markersize=marker_size   ,label = battery_chemistry[i] + ': '+ str(C_rat[j]) + ' C') 
                    axes5.plot(Amp_Hrs , cell_temp, marker= marker[i] , linestyle = linestyles[i],  color= linecolors[j] , markersize=marker_size,label = battery_chemistry[i] + ': '+ str(C_rat[j]) + ' C')              
                else:
                    axes2.plot(Amp_Hrs , volts , marker= marker[i], linestyle = linestyles[i],  color= linecolors[j] , markersize=marker_size   ,label = battery_chemistry[i] + ': '+ str(C_rat[j]) + ' C') 
                    axes4.plot(Amp_Hrs , SOC   , marker= marker[i] , linestyle = linestyles[i],  color= linecolors[j], markersize=marker_size   ,label = battery_chemistry[i] + ': '+ str(C_rat[j]) + ' C') 
                    axes6.plot(Amp_Hrs , cell_temp, marker= marker[i] , linestyle = linestyles[i],  color= linecolors[j] , markersize=marker_size,label = battery_chemistry[i] + ': '+ str(C_rat[j]) + ' C')              
             

    legend_font_size = 6                     
    axes1.set_ylabel('Voltage $(V_{UL}$)')  
    axes1.legend(loc='upper right', ncol = 2, prop={'size': legend_font_size})  
    axes1.set_ylim([2.5,5]) 
    axes1.set_xlim([0,7])
    axes2.set_xlabel('Amp-Hours (A-hr)') 
    axes2.legend(loc='upper right', ncol = 2, prop={'size': legend_font_size})  
    axes2.set_ylim([2.5,5])   
    axes2.set_xlim([0,7])   
    axes3.set_ylabel('SOC')  
    axes3.legend(loc='upper right', ncol = 2, prop={'size': legend_font_size})  
    axes3.set_ylim([0,1]) 
    axes3.set_xlim([0,7]) 
    axes4.legend(loc='upper right', ncol = 2, prop={'size': legend_font_size})  
    axes4.set_ylim([0,1])   
    axes4.set_xlim([0,7])      
    axes5.set_xlabel('Amp-Hours (A-hr)') 
    axes5.legend(loc='upper right', ncol = 2, prop={'size': legend_font_size})
    axes5.set_ylim([273,320])
    axes5.set_xlim([0,7]) 
    axes5.set_ylabel(r'Temperature ($\degree$C)')    
    axes6.set_xlabel('Amp-Hours (A-hr)')        
    axes6.legend(loc='upper left', ncol = 2, prop={'size': legend_font_size})
    axes6.set_ylim([273,320])
    axes6.set_xlim([0,7])  
    
    return 

def set_up_conditions(battery_li_ion):           
    
    bus                                                                                = RCAIDE.Library.Components.Energy.Distributors.Electrical_Bus()  
    state                                                                              = Conditions()  
    state.numerics                                                                     = Conditions()
    state.numerics.time                                                                = Conditions() 
    state.numerics.time.integrate                                                      = np.array([[0, 0],[0, 10]])
    state.numerics.time.differentiate                                                  = np.array([[0, 0],[0, 1]])
    state.numerics.time.control_points                                                 = np.array([[0], [1]]) 
    state.numerics.number_of_control_points                                            = 2
    state.conditions                                                                   = Conditions() 
    state.conditions.freestream                                                        = None
    state.conditions.frames                                                            = Conditions()  
    state.conditions.frames.inertial                                                   = Conditions() 
    state.conditions.frames.inertial.time                                              = np.array([[0],[1]])  
    state.conditions.energy                                                            = Conditions()   
    state.conditions.energy[bus.tag]                                                   = Conditions()
    state.conditions.energy[bus.tag][battery_li_ion.tag]                               = Conditions()
    state.conditions.energy[bus.tag][battery_li_ion.tag]                               = Conditions() 
    state.conditions.energy[bus.tag][battery_li_ion.tag].pack                          = Conditions() 
    state.conditions.energy[bus.tag][battery_li_ion.tag].cell                          = Conditions() 
    state.conditions.energy[bus.tag][battery_li_ion.tag].pack.energy                   = np.zeros((2,1))    
    state.conditions.energy[bus.tag][battery_li_ion.tag].pack.current                  = np.zeros((2,1))   
    state.conditions.energy[bus.tag][battery_li_ion.tag].pack.voltage_open_circuit     = np.zeros((2,1))  
    state.conditions.energy[bus.tag][battery_li_ion.tag].pack.voltage_under_load       = np.zeros((2,1))  
    state.conditions.energy[bus.tag][battery_li_ion.tag].pack.power                    = np.zeros((2,1))   
    state.conditions.energy[bus.tag][battery_li_ion.tag].pack.temperature              = np.zeros((2,1))   
    state.conditions.energy[bus.tag][battery_li_ion.tag].pack.heat_energy_generated    = np.zeros((2,1))   
    state.conditions.energy[bus.tag][battery_li_ion.tag].pack.internal_resistance      = np.zeros((2,1))   
    state.conditions.energy[bus.tag][battery_li_ion.tag].cell.heat_energy_generated    = np.zeros((2,1))    
    state.conditions.energy[bus.tag][battery_li_ion.tag].cell.state_of_charge          = np.zeros((2,1))   
    state.conditions.energy[bus.tag][battery_li_ion.tag].cell.power                    = np.zeros((2,1))         
    state.conditions.energy[bus.tag][battery_li_ion.tag].cell.energy                   = np.array([[battery_li_ion.pack.maximum_energy], [battery_li_ion.pack.maximum_energy]])   
    state.conditions.energy[bus.tag][battery_li_ion.tag].cell.voltage_under_load       = np.zeros((2,1))         
    state.conditions.energy[bus.tag][battery_li_ion.tag].cell.voltage_open_circuit     = np.zeros((2,1))        
    state.conditions.energy[bus.tag][battery_li_ion.tag].cell.current                  = np.zeros((2,1))         
    state.conditions.energy[bus.tag][battery_li_ion.tag].cell.temperature              = np.zeros((2,1))         
    state.conditions.energy[bus.tag][battery_li_ion.tag].cell.charge_throughput        = np.zeros((2,1))         
    state.conditions.energy[bus.tag][battery_li_ion.tag].cell.depth_of_discharge       = np.zeros((2,1))
    state.conditions.energy[bus.tag][battery_li_ion.tag].pack.maximum_initial_energy   = battery_li_ion.pack.maximum_energy
    state.conditions.energy[bus.tag][battery_li_ion.tag].cell.cycle_in_day             = 0 
    state.conditions.energy[bus.tag][battery_li_ion.tag].cell.resistance_growth_factor = 1.
    state.conditions.energy[bus.tag][battery_li_ion.tag].cell.capacity_fade_factor     = 1.   
    
    return bus,state  
 
def analyses_setup(configs):

    analyses = RCAIDE.Framework.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config)
        analyses[tag] = analysis

    return analyses

def base_analysis(vehicle):    
    #   Initialize the Analyses     
    analyses = RCAIDE.Framework.Analyses.Vehicle()  
    
    #  Energy
    energy          = RCAIDE.Framework.Analyses.Energy.Energy()
    energy.networks = vehicle.networks 
    analyses.append(energy)
 
    #  Planet Analysis
    planet  = RCAIDE.Framework.Analyses.Planets.Planet()
    analyses.append(planet)
 
    #  Atmosphere Analysis
    atmosphere                 = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   
 
    return analyses     

def mission_setup(analyses,vehicle,battery_chemistry,current,mAh):
 
    #   Initialize the Mission 
    mission            = RCAIDE.Framework.Mission.Sequential_Segments()
    mission.tag        = 'cell_cycle_test'   
    Segments           = RCAIDE.Framework.Mission.Segments 
    base_segment       = Segments.Segment()   
    time               = 0.8 * (mAh/1000)/current * Units.hrs  
        
    # Discharge Segment 
    segment                                 = Segments.Ground.Battery_Discharge(base_segment) 
    segment.analyses.extend(analyses.base)  
    segment.tag                             = 'Discharge_1' 
    segment.time                            = time/2 
    segment.current                         = current
    segment.initial_battery_state_of_charge = 1  
    mission.append_segment(segment)         
    

    segment                                = Segments.Ground.Battery_Discharge(base_segment) 
    segment.tag                            = 'Discharge_2'
    segment.analyses.extend(analyses.base)  
    segment.current                        = current
    segment.time                           = time/2  
    mission.append_segment(segment)         
            
    
    # Charge Segment 
    segment                                = Segments.Ground.Battery_Recharge(base_segment)      
    segment.analyses.extend(analyses.base) 
    segment.tag                            = 'Recharge'
    segment.current                        = current
    segment.time                           = time     
    mission.append_segment(segment)   

    return mission 

def missions_setup(mission): 
 
    missions         = RCAIDE.Framework.Mission.Missions()
    
    # base mission 
    mission.tag  = 'base_mission'
    missions.append(mission)
 
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