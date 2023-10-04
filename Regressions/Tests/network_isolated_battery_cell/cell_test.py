# Regression/scripts/network_isolated_battery_cell/cell_test.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE  
from RCAIDE.Core                                 import Units, Data 
from RCAIDE.Methods.Power.Battery.Sizing         import initialize_from_mass ,initialize_from_energy_and_power, initialize_from_mass, initialize_from_circuit_configuration, find_mass_gain_rate, find_total_mass_gain
from RCAIDE.Methods.Power.Battery.Ragone         import find_ragone_properties, find_ragone_optimum 
from RCAIDE.Analyses.Mission.Common    import Conditions
from RCAIDE.Visualization import * 

# package imports  
import numpy as np
import matplotlib.pyplot as plt

# local imports 
import sys 
sys.path.append('../../Vehicles') 
from Isolated_Battery_Cell   import vehicle_setup , configs_setup  

# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------  

def main():
    # size the battery 
    Ereq                           = 3000*Units.Wh # required energy for the mission in Joules 
    Preq                           = 2000. # maximum power requirements for mission in W
    
    # instantiate differet battery types 
    numerics                       = Data()
    battery_outputs                = Data() #create inputs data structure for inputs for testing discharge model
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
    battery_outputs.current          = np.array([[100],[100]])*Units.amps
    battery_outputs.power            = np.array([[Preq/2.] ,[ Preq]])
    print('battery outputs=', battery_outputs)
    battery_li_ion.outputs           = battery_outputs
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
    
    conditions                                        = Conditions() 
    conditions.energy                                 = Conditions() 
    conditions.freestream                             = Conditions() 
    conditions.energy['bus']                          = Conditions()
    conditions.energy['bus'][battery_li_ion.tag]      = Conditions()
    conditions.energy['bus'][battery_li_ion.tag].pack = Conditions()
    conditions.energy['bus'][battery_li_ion.tag].pack.maximum_initial_energy =  np.array([[battery_li_ion.pack.maximum_energy], [battery_li_ion.pack.maximum_energy]]) 
    conditions.energy['bus'][battery_li_ion.tag].cell = Conditions()
    conditions.energy['bus'][battery_li_ion.tag].cell.capacity_fade_factor = 1.0
    conditions.energy['bus'][battery_li_ion.tag].cell.resistance_growth_factor = 1.0
    

    conditions.freestream                             = None
    
    # run discharge models
    battery_li_ion.energy_calc(numerics,conditions,bus_tag = 'bus')
    print(battery_li_ion)
    plot_battery_ragone_diagram(battery_li_ion, save_filename =  'lithium_ion')
    plot_battery_ragone_diagram(battery_li_s,   save_filename =  'lithium_sulfur') 
     
    battery_chemistry     = ['Lithium_Ion_NMC','Lithium_Ion_LFP'] 
    marker                = ['s' ,'o' ,'P']
    linestyles            = ['-','--',':']
    linecolors            = [['green' , 'blue' ],['darkgreen', 'darkblue'], ['limegreen', 'lightblue' ]]     
    curr                  = [1.5, 3] 
    C_rat                 = [0.5,1]   
    marker_size           = 8 
    mAh                   = np.array([3550,1500]) 
    V_ul_true  = np.array([[3.9785956029658225,3.5766346818252552],
                           [3.9624907292567415,3.5649333172718887]])
    bat_temp_true     = np.array([[291.56685519189483,288.99463326715926],
                                  [293.3579773814795,289.66533632286996]])  
 
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
            if j == 1: 
                fixed_bus_voltage = True 
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
            
            plot_results(results,j,battery_chemistry[i], axes1, axes2, axes3, axes4, axes5, axes6, 
                         marker[i],marker_size,linecolors[i],linestyles[i],C_rat[j])  

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

def plot_results(results,j,bat_chem, axes1, axes2, axes3, axes4,axes5,axes6,m,ms,lc,ls,C_rat): 
    
    for segment in results.segments.values(): 
        volts         = segment.conditions.energy.bus[bat_chem].pack.voltage_under_load[:,0] 
        SOC           = segment.conditions.energy.bus[bat_chem].cell.state_of_charge[:,0]   
        cell_temp     = segment.conditions.energy.bus[bat_chem].cell.temperature[:,0]   
        Amp_Hrs       = segment.conditions.energy.bus[bat_chem].cell.charge_throughput[:,0]                   
          
        if j == 0:
            axes1.set_title('Variable Bus Voltage')
            axes1.plot(Amp_Hrs , volts    , marker= m , linestyle = ls,  color= lc[0] , markersize=ms   ,label = bat_chem + ': '+ str(C_rat) + ' C') 
            axes3.plot(Amp_Hrs , SOC      , marker= m , linestyle = ls,  color= lc[0] , markersize=ms   ,label = bat_chem + ': '+ str(C_rat) + ' C') 
            axes5.plot(Amp_Hrs , cell_temp, marker= m , linestyle = ls,  color= lc[0] , markersize=ms   ,label = bat_chem + ': '+ str(C_rat) + ' C')   
        elif  j == 1: 
            axes2.set_title('Fixed Bus Voltage')
            axes2.plot(Amp_Hrs , volts , marker= m , linestyle = ls,  color= lc[1] , markersize=ms   ,label = bat_chem + ': '+ str(C_rat) + ' C') 
            axes4.plot(Amp_Hrs , SOC   , marker= m , linestyle = ls,  color= lc[1] , markersize=ms   ,label = bat_chem + ': '+ str(C_rat) + ' C') 
            axes6.plot(Amp_Hrs , cell_temp, marker= m , linestyle = ls,  color= lc[1] , markersize=ms,label = bat_chem + ': '+ str(C_rat) + ' C')           
    return
 
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
    energy          = RCAIDE.Analyses.Energy.Energy()
    energy.networks = vehicle.networks 
    analyses.append(energy)
 
    #  Planet Analysis
    planet  = RCAIDE.Analyses.Planets.Planet()
    analyses.append(planet)
 
    #  Atmosphere Analysis
    atmosphere                 = RCAIDE.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   
 
    return analyses     

def mission_setup(analyses,vehicle,battery_chemistry,current,mAh):
 
    #   Initialize the Mission 
    mission            = RCAIDE.Analyses.Mission.Sequential_Segments()
    mission.tag        = 'cell_cycle_test'   
    Segments           = RCAIDE.Analyses.Mission.Segments 
    base_segment       = Segments.Segment()   
    time               = 0.9 * (mAh/1000)/current * Units.hrs 
  
        
    # Discharge Segment 
    segment                                = Segments.Ground.Battery_Discharge(base_segment) 
    segment.analyses.extend(analyses.base) 
    segment.tag                            = 'Discharge_1' 
    segment.time                           = time/2 
    segment.initial_battery_state_of_charge= 1
    segment                                = vehicle.networks.isolated_battery_cell.add_unknowns_and_residuals_to_segment(segment,estimated_battery_cell_temperature = [[295]] )    
    mission.append_segment(segment)         
    

    segment                                = Segments.Ground.Battery_Discharge(base_segment) 
    segment.tag                            = 'Discharge_2'
    segment.analyses.extend(analyses.base)  
    segment.time                           = time/2 
    segment                                = vehicle.networks.isolated_battery_cell.add_unknowns_and_residuals_to_segment(segment,estimated_battery_cell_temperature = [[295]] )    
    mission.append_segment(segment)         
            
    
    # Charge Segment 
    segment                                = Segments.Ground.Battery_Recharge(base_segment)      
    segment.analyses.extend(analyses.base) 
    segment.tag                            = 'Recharge'
    segment.time                           = time
    segment                                = vehicle.networks.isolated_battery_cell.add_unknowns_and_residuals_to_segment(segment,estimated_battery_cell_temperature = [[303]] )      
    mission.append_segment(segment)  
     
        
 

    return mission 

def missions_setup(mission): 
 
    missions         = RCAIDE.Analyses.Mission.Missions()
    
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