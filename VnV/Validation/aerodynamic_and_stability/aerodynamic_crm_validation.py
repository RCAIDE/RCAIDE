# aerodynamic_crm_validation.py
# Aerodynamic validation of the Common Research Model (CRM) using VLM
# against experimental wind tunnel data at Mach 0.85.

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import RCAIDE
from RCAIDE.Framework.Core                                             import Units, Data
from RCAIDE.Framework.External_Interfaces.OpenVSP.import_vsp_vehicle  import import_vsp_vehicle
from RCAIDE.Library.Methods.Performance                                import aircraft_aerodynamic_analysis
from RCAIDE.Library.Methods.Powertrain.Propulsors.Turbofan             import design_turbofan

from copy     import deepcopy
from io       import StringIO
import pickle
import os
from RCAIDE.Library.Plots import plot_3d_vehicle
import numpy as np
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------
#   Experimental Reference Data (Mach ~0.85, Re ~5e7)
#   Source: CRM wind tunnel campaign
# ----------------------------------------------------------------------

raw_data_92 = """\
AoA (deg)\tMach\tRE_ref\tTemperature (F)\tCL\tCD\tCM
-2.83992\t0.849892\t5.0033698\t119.5240021\t-0.290069\t0.0254703\t0.296253
-1.80837\t0.850047\t5.0030799\t119.5780029\t-0.152055\t0.0180762\t0.243471
-1.31433\t0.849711\t5.00035\t119.6259995\t-0.0854695\t0.0164904\t0.218967
-0.820749\t0.849448\t5.0002298\t119.6289978\t-0.0205704\t0.0157003\t0.195744
-0.312387\t0.850052\t5.0008998\t119.7030029\t0.0466929\t0.0155093\t0.172404
0.229618\t0.850203\t5.0014701\t119.6900024\t0.116596\t0.0157593\t0.148772
0.668474\t0.850193\t4.9999299\t119.7979965\t0.174459\t0.0162941\t0.130109
1.15677\t0.849777\t4.9980602\t119.8730011\t0.239466\t0.0172128\t0.110187
1.6593699\t0.850219\t4.9994798\t119.9169998\t0.307011\t0.0186479\t0.0912732
1.9300801\t0.850103\t4.9969702\t120.0759964\t0.344069\t0.0196483\t0.0816128
2.1863999\t0.850218\t4.9969802\t120.1190033\t0.379054\t0.0208287\t0.0724932
2.4152701\t0.850923\t4.9980202\t120.1460037\t0.415042\t0.0220803\t0.0629309
2.65643\t0.850738\t4.9979\t120.1750031\t0.453787\t0.0237041\t0.0519673
2.9351599\t0.850357\t4.9967399\t120.1679993\t0.492912\t0.0260218\t0.0400815
3.16377\t0.849942\t4.99582\t120.1269989\t0.525882\t0.0282517\t0.0304636
3.4015601\t0.850893\t4.9960299\t120.2770004\t0.556315\t0.0312678\t0.0243156
3.6719799\t0.850949\t4.9979801\t120.1760025\t0.580371\t0.0351033\t0.0252739
3.9244299\t0.850595\t4.9980898\t120.1719971\t0.599312\t0.0389397\t0.0290647
4.21771\t0.849216\t4.9941802\t120.0790024\t0.61983\t0.043213\t0.0326177
4.42237\t0.850891\t4.9988899\t120.1719971\t0.630447\t0.047249\t0.0391618
4.6530199\t0.850985\t4.9976001\t120.125\t0.645526\t0.0512715\t0.0432939
4.9145002\t0.850835\t4.9985499\t120.112999\t0.661954\t0.0556064\t0.0461898
5.1538601\t0.850516\t4.9973698\t120.1039963\t0.678735\t0.0596733\t0.0475863
5.6085401\t0.849873\t4.9970002\t120.0230026\t0.701978\t0.0662093\t0.050425
6.21034\t0.84843\t4.9924302\t120.1029968\t0.724428\t0.0748343\t0.0603281
6.7125502\t0.849285\t4.9938598\t120.1750031\t0.744763\t0.0841753\t0.0662167
7.1406398\t0.848729\t4.9906602\t120.2979965\t0.761114\t0.0921219\t0.0616133
7.5858102\t0.849791\t4.9962702\t120.0770035\t0.785667\t0.10216\t0.037346
8.0290203\t0.850005\t4.9960999\t120.1070023\t0.803596\t0.111904\t0.0019705
8.6389103\t0.850149\t4.9965901\t120.1179962\t0.832168\t0.126354\t-0.038431
9.0966501\t0.84901\t4.9932199\t120.0630035\t0.838642\t0.13557\t-0.0567955
9.4848003\t0.849567\t4.99472\t120.1500015\t0.847626\t0.14586\t-0.0794967
10.2521\t0.850526\t4.9964099\t120.2220001\t0.854065\t0.164255\t-0.0851677
"""

# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main():
    vehicle           = vehicle_setup()
    run_aero_analysis(vehicle)
    return


# ----------------------------------------------------------------------
#   Aerodynamic Analysis
# ----------------------------------------------------------------------

def run_aero_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Build analysis
    # ------------------------------------------------------------------
    analyses = RCAIDE.Framework.Analyses.Vehicle()
    analyses.vehicle = vehicle

    geometry = RCAIDE.Framework.Analyses.Geometry.Geometry()
    geometry.settings.compute_fuel_volume = False
    analyses.append(geometry)

    aerodynamics = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method()
    aerodynamics.vehicle                            = vehicle
    aerodynamics.settings.number_of_spanwise_vortices  = 25
    aerodynamics.settings.number_of_chordwise_vortices = 4
    aerodynamics.settings.model_fuselage            = True
    analyses.append(aerodynamics)

    # ------------------------------------------------------------------
    #   Parse experimental data
    # ------------------------------------------------------------------
    data    = pd.read_csv(StringIO(raw_data_92), sep='\t')
    AoAs    = np.atleast_2d(np.array(data['AoA (deg)']) * Units.degrees).T
    Machs   = np.atleast_2d(np.array(data['Mach'])).T
    RE_refs = np.atleast_2d(np.array(data['RE_ref'])).T * 1e7
    Ts      = (np.atleast_2d(np.array(data['Temperature (F)'])).T - 32) * 5/9 + 273.15

    Cref        = 275.80 * Units.inches
    Non_Dim_Res = RE_refs / Cref

    # ------------------------------------------------------------------
    #   Run VLM
    # ------------------------------------------------------------------
    results = aircraft_aerodynamic_analysis(
        analyses                         = analyses,
        angle_of_attacks                 = AoAs,
        mach_numbers                     = Machs,
        non_dimensional_reynolds_numbers = Non_Dim_Res,
        temperatures                     = Ts,
    )
    results_data = pd.DataFrame({'Mach': results.Mach.flatten(), 'Alpha': results.alpha.flatten(), 'Lift': results.lift_coefficient.flatten(), 'Total Drag': results.drag_coefficient.flatten(), 'Parasite Drag': results.parasite_drag_coefficient.flatten(), 'Wave Drag': results.compressibility_drag_coefficient.flatten(), 'Induced Drag': results.induced_drag_coefficient.flatten(), 'Form Drag': results.form_drag_coefficient.flatten(),  })
    results_data.to_csv('CRM_Drag_output.csv')
  

    return


# ----------------------------------------------------------------------
#   Vehicle Setup
# ----------------------------------------------------------------------

def vehicle_setup():

    # ------------------------------------------------------------------
    #   Geometry
    # ------------------------------------------------------------------
    try:
        vehicle = import_vsp_vehicle(
            os.path.join(base_dir, 'CRM-2_nac.vsp3'),
            main_wing_tag  = 'main_wing',
            network_type   = RCAIDE.Framework.Networks.Fuel(),
            propulsor_type = RCAIDE.Library.Components.Powertrain.Propulsors.Turbofan(),
            units_type     = 'inches',
        )
    except:
        pickle_path = os.path.join(base_dir, 'CRM.pkl')
        with open(pickle_path, 'rb') as f:
            vehicle = pickle.load(f)
    
    for index , segment in enumerate(vehicle.wings.main_wing.segments):
        segment.airfoil.coordinate_file = base_dir + os.sep + "CRM_Airfoils" + os.sep + f"main_wing_airfoil_XSec_{index}.dat"

    vehicle.wings.main_wing.chords.mean_aerodynamic     = 275.80 * Units.inches
    vehicle.reference_area                              = 4000.0 * Units['ft**2']
    vehicle.mass_properties.center_of_gravity[0][0]    = 1325.90 * Units.inches
    vehicle.mass_properties.center_of_gravity[0][2]    = 0

    # ------------------------------------------------------------------
    #   Turbofan Network
    # ------------------------------------------------------------------
    net       = RCAIDE.Framework.Networks.Fuel()
    fuel_line = RCAIDE.Library.Components.Powertrain.Distributors.Fuel_Line()

    # ------------------------------------------------------------------
    #   Propulsor 1 (Starboard)
    # ------------------------------------------------------------------
    turbofan1                      = RCAIDE.Library.Components.Powertrain.Propulsors.Turbofan()
    turbofan1.tag                  = 'propulsor_1'
    turbofan1.origin               = [[17.818,  10.000, -0.953]]
    turbofan1.length               = 4.928
    turbofan1.diameter             = 2.822
    turbofan1.bypass_ratio         = 9.1
    turbofan1.design_altitude      = 36000 * Units.ft
    turbofan1.design_mach_number   = 0.85
    turbofan1.design_thrust        = 80000 * Units.N
    turbofan1.working_fluid        = RCAIDE.Library.Attributes.Gases.Air()

    ram                            = RCAIDE.Library.Components.Powertrain.Converters.Ram()
    ram.tag                        = 'ram'
    turbofan1.ram                  = ram

    inlet_nozzle                          = RCAIDE.Library.Components.Powertrain.Converters.Compression_Nozzle()
    inlet_nozzle.tag                      = 'inlet nozzle'
    inlet_nozzle.polytropic_efficiency    = 0.98
    inlet_nozzle.pressure_ratio           = 1
    inlet_nozzle.compressibility_effects  = False
    turbofan1.inlet_nozzle                = inlet_nozzle

    fan                            = RCAIDE.Library.Components.Powertrain.Converters.Fan()
    fan.tag                        = 'fan'
    fan.polytropic_efficiency      = 0.98
    fan.pressure_ratio             = 1.4
    turbofan1.fan                  = fan

    lpc                            = RCAIDE.Library.Components.Powertrain.Converters.Compressor()
    lpc.tag                        = 'lpc'
    lpc.polytropic_efficiency      = 0.98
    lpc.pressure_ratio             = 1.3
    turbofan1.low_pressure_compressor = lpc

    hpc                            = RCAIDE.Library.Components.Powertrain.Converters.Compressor()
    hpc.tag                        = 'hpc'
    hpc.polytropic_efficiency      = 0.98
    hpc.pressure_ratio             = 23.9
    turbofan1.high_pressure_compressor = hpc

    lpt                            = RCAIDE.Library.Components.Powertrain.Converters.Turbine()
    lpt.tag                        = 'lpt'
    lpt.mechanical_efficiency      = 0.99
    lpt.polytropic_efficiency      = 0.98
    turbofan1.low_pressure_turbine = lpt

    hpt                            = RCAIDE.Library.Components.Powertrain.Converters.Turbine()
    hpt.tag                        = 'hpt'
    hpt.mechanical_efficiency      = 0.99
    hpt.polytropic_efficiency      = 0.98
    turbofan1.high_pressure_turbine = hpt

    combustor                          = RCAIDE.Library.Components.Powertrain.Converters.Combustor()
    combustor.tag                      = 'Comb'
    combustor.efficiency               = 0.997
    combustor.turbine_inlet_temperature = 1440
    combustor.pressure_ratio           = 0.94
    combustor.fuel_data                = RCAIDE.Library.Attributes.Propellants.Jet_A()
    turbofan1.combustor                = combustor

    core_nozzle                        = RCAIDE.Library.Components.Powertrain.Converters.Expansion_Nozzle()
    core_nozzle.tag                    = 'core nozzle'
    core_nozzle.polytropic_efficiency  = 0.98
    core_nozzle.pressure_ratio         = 0.995
    core_nozzle.diameter               = 1.5
    turbofan1.core_nozzle              = core_nozzle

    fan_nozzle                         = RCAIDE.Library.Components.Powertrain.Converters.Expansion_Nozzle()
    fan_nozzle.tag                     = 'fan nozzle'
    fan_nozzle.polytropic_efficiency   = 0.98
    fan_nozzle.pressure_ratio          = 0.995
    fan_nozzle.diameter                = 2.822
    turbofan1.fan_nozzle               = fan_nozzle

    design_turbofan(turbofan1)

    nacelle                      = RCAIDE.Library.Components.Nacelles.Body_of_Revolution_Nacelle()
    nacelle.tag                  = 'nacelle_1'
    nacelle.diameter             = 3.556
    nacelle.length               = 4.9
    nacelle.inlet_diameter       = 2.5
    nacelle.origin               = [[17.818, 10.000, -0.953]]
    nacelle.areas.wetted         = np.pi * nacelle.diameter * nacelle.length
    nacelle_airfoil              = RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil()
    nacelle_airfoil.NACA_4_Series_code = '0010'
    nacelle.append_airfoil(nacelle_airfoil)
    turbofan1.nacelle            = nacelle

    net.propulsors.append(turbofan1)

    # ------------------------------------------------------------------
    #   Propulsor 2 (Port) — mirror of starboard
    # ------------------------------------------------------------------
    turbofan2                  = deepcopy(turbofan1)
    turbofan2.tag              = 'propulsor_2'
    turbofan2.origin           = [[17.818, -10.000, -0.953]]
    turbofan2.nacelle.origin   = [[17.818, -10.000, -0.953]]
    net.propulsors.append(turbofan2)

    # ------------------------------------------------------------------
    #   Fuel Tanks
    # ------------------------------------------------------------------
    fuel_tank_1                              = RCAIDE.Library.Components.Powertrain.Sources.Fuel_Tanks.Integral_Tank(vehicle.wings.main_wing)
    fuel_tank_1.fuel                         = RCAIDE.Library.Attributes.Propellants.Jet_A1()
    fuel_tank_1.segments_bounding_tank       = ['root', 'yehudi']
    fuel_tank_1.segments_percent_chord_start = [0.1, 0.1]
    fuel_tank_1.segments_percent_chord_end   = [0.7, 0.7]
    fuel_line.fuel_tanks.append(fuel_tank_1)

    fuel_tank_2                              = RCAIDE.Library.Components.Powertrain.Sources.Fuel_Tanks.Integral_Tank(vehicle.wings.main_wing)
    fuel_tank_2.fuel                         = RCAIDE.Library.Attributes.Propellants.Jet_A1()
    fuel_tank_2.segments_bounding_tank       = ['yehudi', 'tip']
    fuel_tank_2.segments_percent_chord_start = [0.1, 0.1]
    fuel_tank_2.segments_percent_chord_end   = [0.7, 0.7]
    fuel_line.fuel_tanks.append(fuel_tank_2)

    fuel_line.assigned_propulsors = [['propulsor_1', 'propulsor_2']]
    net.fuel_lines.append(fuel_line)
    vehicle.append_energy_network(net)

    return vehicle


# ----------------------------------------------------------------------
#   Entry Point
# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
