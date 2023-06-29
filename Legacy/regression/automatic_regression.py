# automatic_regression.py
#
# Created:  Jun 2014, T. Lukaczyk
# Modified: Jun 2014, SUAVE Team
#           Jul 2017, SUAVE Team
#           Jan 2018, SUAVE Team
#           May 2019, T. MacDonald
#           Mar 2020, M. Clarke

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') 
import sys, os, traceback, time
from Legacy.trunk.S.Core.DataOrdered import DataOrdered


# ----------------------------------------------------------------------
#   How This Works
# ----------------------------------------------------------------------

# The "modules" list contains the name of the file you would like to run.
# Each test script must include a main function, this will be called by
# this automatic regression script.
#
# For more information, see ../templates/example_test_script.py

# ----------------------------------------------------------------------
#   The Modules to Test
# ----------------------------------------------------------------------

modules = [

    # ----------------------- Regression List --------------------------
    '../Legacy/regression/scripts/aerodynamics/aerodynamics.py',
    '../Legacy/regression/scripts/aerodynamics/all_moving_surfaces_vlm.py',
    '../Legacy/regression/scripts/aerodynamics/control_surfaces_vlm.py',
    '../Legacy/regression/scripts/aerodynamics/sears_haack.py',
    '../Legacy/regression/scripts/aerodynamics/sideslip_and_rotation_vlm.py',
    '../Legacy/regression/scripts/airfoil_import/airfoil_import_test.py',
    '../Legacy/regression/scripts/airfoil_import/airfoil_interpolation_test.py',
    '../Legacy/regression/scripts/airfoil_analysis/airfoil_panel_method_test.py', 
    '../Legacy/regression/scripts/atmosphere/atmosphere.py',
    '../Legacy/regression/scripts/atmosphere/constant_temperature.py',
    '../Legacy/regression/scripts/AVL/test_AVL.py',
    '../Legacy/regression/scripts/B737/mission_B737.py',
    '../Legacy/regression/scripts/battery/aircraft_discharge_comparisons.py',
    '../Legacy/regression/scripts/battery/battery_cell_discharge_tests.py',
    '../Legacy/regression/scripts/cmalpha/cmalpha.py',
    '../Legacy/regression/scripts/cnbeta/cnbeta.py',
    '../Legacy/regression/scripts/concorde/concorde.py',
    '../Legacy/regression/scripts/ducted_fan/ducted_fan_network.py',
    '../Legacy/regression/scripts/ducted_fan/battery_ducted_fan_network.py',
    '../Legacy/regression/scripts/ducted_fan/serial_hybrid_ducted_fan_network.py',
    '../Legacy/regression/scripts/dynamic_stability/dynamicstability.py',
    '../Legacy/regression/scripts/electric_performance/propeller_single_point.py',
    '../Legacy/regression/scripts/electric_performance/electric_V_h_diagram.py',
    '../Legacy/regression/scripts/electric_performance/electric_payload_range.py',
    '../Legacy/regression/scripts/Embraer_E190_constThr/mission_Embraer_E190_constThr.py',
    '../Legacy/regression/scripts/fuel_cell/fuel_cell.py',
    '../Legacy/regression/scripts/gasturbine_network/gasturbine_network.py',
    '../Legacy/regression/scripts/geometry/NACA_airfoil_compute.py',
    '../Legacy/regression/scripts/geometry/NACA_volume_compute.py',
    '../Legacy/regression/scripts/geometry/wing_fuel_volume_compute.py',
    '../Legacy/regression/scripts/geometry/fuselage_planform_compute.py',
    '../Legacy/regression/scripts/industrial_costs/industrial_costs.py',
    '../Legacy/regression/scripts/internal_combustion_propeller/ICE_Test.py',
    '../Legacy/regression/scripts/internal_combustion_propeller/ICE_CS_Test.py',
    '../Legacy/regression/scripts/lifting_line/lifting_line.py',
    '../Legacy/regression/scripts/mission_range_and_weight_sizing/landing_field_length.py',
    '../Legacy/regression/scripts/mission_range_and_weight_sizing/take_off_field_length.py',
    '../Legacy/regression/scripts/mission_range_and_weight_sizing/take_off_weight_from_tofl.py',
    '../Legacy/regression/scripts/motor/motor_test.py',
    '../Legacy/regression/scripts/multifidelity/optimize_mf.py',
    '../Legacy/regression/scripts/noise_optimization/Noise_Test.py',
    '../Legacy/regression/scripts/noise_fidelity_zero/DC_10_noise.py', 
    '../Legacy/regression/scripts/noise_fidelity_one/propeller_noise.py',
    '../Legacy/regression/scripts/noise_fidelity_one/aircraft_noise.py',
    '../Legacy/regression/scripts/nonuniform_propeller_inflow/nonuniform_propeller_inflow.py',
    '../Legacy/regression/scripts/optimization_packages/optimization_packages.py',
    '../Legacy/regression/scripts/payload_range/payload_range.py',
    '../Legacy/regression/scripts/plots/plot_test.py',
    '../Legacy/regression/scripts/propeller/propeller_test.py',
    '../Legacy/regression/scripts/propeller_speeds/range_endurance_speeds.py',
    '../Legacy/regression/scripts/propulsion_surrogate/propulsion_surrogate.py',
    '../Legacy/regression/scripts/ramjet_network/ramjet_network.py',
    '../Legacy/regression/scripts/Regional_Jet_Optimization/Optimize2.py',
    '../Legacy/regression/scripts/scramjet_network/scramjet_network.py',
    '../Legacy/regression/scripts/rocket_network/Rocketdyne_F1.py',
    '../Legacy/regression/scripts/rocket_network/Rocketdyne_J2.py',
    '../Legacy/regression/scripts/segments/segment_test.py',
    '../Legacy/regression/scripts/segments/transition_segment_test.py',
    '../Legacy/regression/scripts/slipstream/slipstream_test.py',
    '../Legacy/regression/scripts/slipstream/propeller_interactions.py',
    '../Legacy/regression/scripts/solar_network/solar_network.py',
    '../Legacy/regression/scripts/solar_network/solar_low_fidelity_network.py',
    '../Legacy/regression/scripts/solar_radiation/solar_radiation.py',
    '../Legacy/regression/scripts/SU2_surrogate/BWB-450.py',
    '../Legacy/regression/scripts/sweeps/test_sweeps.py',
    '../Legacy/regression/scripts/test_input_output/test_xml_read_write.py',
    '../Legacy/regression/scripts/test_input_output/test_freemind_write.py',
    '../Legacy/regression/scripts/turboelectric_HTS_ducted_fan_network/turboelectric_HTS_ducted_fan_network.py',
    '../Legacy/regression/scripts/turboelectric_HTS_dynamo_ducted_fan_network/turboelectric_HTS_dynamo_ducted_fan_network.py',
    '../Legacy/regression/scripts/variable_cruise_distance/variable_cruise_distance.py',
    '../Legacy/regression/scripts/V_n_diagram/V_n_diagram_regression.py',
    '../Legacy/regression/scripts/VTOL/test_Multicopter.py',
    '../Legacy/regression/scripts/VTOL/test_Tiltwing.py',
    '../Legacy/regression/scripts/VTOL/test_Stopped_Rotor.py',
    '../Legacy/regression/scripts/weights/weights.py'
    
]

# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main():

    # preallocate test results
    results = DataOrdered()
    for module in modules:
        results[module] = 'Untested'

    sys.stdout.write('# --------------------------------------------------------------------- \n')
    sys.stdout.write('#   SUAVE Automatic Regression \n')
    sys.stdout.write('#   %s \n' % time.strftime("%B %d, %Y - %H:%M:%S", time.gmtime()) )
    sys.stdout.write('# --------------------------------------------------------------------- \n')
    sys.stdout.write(' \n')

    # run tests
    all_pass = True
    for module in modules:
        passed = test_module(module)
        if passed:
            results[module] = '  Passed'
        else:
            results[module] = '* FAILED'
            all_pass = False

    # final report
    sys.stdout.write('# --------------------------------------------------------------------- \n')
    sys.stdout.write('Final Results \n')
    for module,result in list(results.items()):
        sys.stdout.write('%s - %s\n' % (result,module))

    if all_pass:
        sys.exit(0)
    else:
        sys.exit(1)


# ----------------------------------------------------------------------
#   Module Tester
# ----------------------------------------------------------------------

def test_module(module_path):

    home_dir = os.getcwd()
    test_dir, module_name = os.path.split( os.path.abspath(module_path) )

    sys.stdout.write('# --------------------------------------------------------------------- \n')
    sys.stdout.write('# Start Test: %s \n' % module_path)
    sys.stdout.flush()

    tic = time.time()

    # try the test
    try:

        # see if file exists
        os.chdir(test_dir)
        if not os.path.exists(module_name) and not os.path.isfile(module_name):
            raise ImportError('file %s does not exist' % module_name)

        # add module directory
        sys.path.append(test_dir)

        # do the import
        name = os.path.splitext(module_name)[0]
        module = __import__(name)

        # run main function
        module.main()

        passed = True

    # catch an error
    except Exception as exc:

        # print traceback
        sys.stderr.write( 'Test Failed: \n' )
        sys.stderr.write( traceback.format_exc() )
        sys.stderr.write( '\n' )
        sys.stderr.flush()

        passed = False

    # final result
    if passed:
        sys.stdout.write('# Passed: %s \n' % module_name)
    else:
        sys.stdout.write('# FAILED: %s \n' % module_name)
    sys.stdout.write('# Test Duration: %.4f min \n' % ((time.time()-tic)/60) )
    sys.stdout.write('\n')

    # cleanup
    plt.close('all')
    os.chdir(home_dir)

    # make sure to write to stdout
    sys.stdout.flush()
    sys.stderr.flush()

    return passed

# ----------------------------------------------------------------------
#   Call Main
# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
