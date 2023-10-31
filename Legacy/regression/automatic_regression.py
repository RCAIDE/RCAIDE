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
    '../regression/scripts/aerodynamics/aerodynamics.py',
    '../regression/scripts/aerodynamics/all_moving_surfaces_vlm.py',
    '../regression/scripts/aerodynamics/control_surfaces_vlm.py',
    '../regression/scripts/aerodynamics/sears_haack.py',
    '../regression/scripts/aerodynamics/sideslip_and_rotation_vlm.py',
    '../regression/scripts/airfoil_import/airfoil_import_test.py',
    '../regression/scripts/airfoil_import/airfoil_interpolation_test.py',
    '../regression/scripts/airfoil_analysis/airfoil_panel_method_test.py', 
    '../regression/scripts/atmosphere/atmosphere.py',
    '../regression/scripts/atmosphere/constant_temperature.py',
    '../regression/scripts/AVL/test_AVL.py',
    '../regression/scripts/B737/mission_B737.py',
    '../regression/scripts/battery/aircraft_discharge_comparisons.py',
    '../regression/scripts/battery/battery_cell_discharge_tests.py',
    '../regression/scripts/cmalpha/cmalpha.py',
    '../regression/scripts/cnbeta/cnbeta.py',
    '../regression/scripts/concorde/concorde.py',
    '../regression/scripts/ducted_fan/ducted_fan_network.py',
    '../regression/scripts/ducted_fan/battery_ducted_fan_network.py',
    '../regression/scripts/ducted_fan/serial_hybrid_ducted_fan_network.py',
    '../regression/scripts/dynamic_stability/dynamicstability.py',
    '../regression/scripts/electric_performance/propeller_single_point.py',
    '../regression/scripts/electric_performance/electric_V_h_diagram.py',
    '../regression/scripts/electric_performance/electric_payload_range.py',
    '../regression/scripts/Embraer_E190_constThr/mission_Embraer_E190_constThr.py',
    '../regression/scripts/fuel_cell/fuel_cell.py',
    '../regression/scripts/gasturbine_network/gasturbine_network.py',
    '../regression/scripts/geometry/NACA_airfoil_compute.py',
    '../regression/scripts/geometry/NACA_volume_compute.py',
    '../regression/scripts/geometry/wing_fuel_volume_compute.py',
    '../regression/scripts/geometry/fuselage_planform_compute.py',
    '../regression/scripts/industrial_costs/industrial_costs.py',
    '../regression/scripts/internal_combustion_propeller/ICE_Test.py',
    '../regression/scripts/internal_combustion_propeller/ICE_CS_Test.py',
    '../regression/scripts/lifting_line/lifting_line.py',
    '../regression/scripts/mission_range_and_weight_sizing/landing_field_length.py',
    '../regression/scripts/mission_range_and_weight_sizing/take_off_field_length.py',
    '../regression/scripts/mission_range_and_weight_sizing/take_off_weight_from_tofl.py',
    '../regression/scripts/motor/motor_test.py',
    '../regression/scripts/multifidelity/optimize_mf.py',
    '../regression/scripts/noise_optimization/Noise_Test.py',
    '../regression/scripts/noise_fidelity_zero/DC_10_noise.py', 
    '../regression/scripts/noise_fidelity_one/propeller_noise.py',
    '../regression/scripts/noise_fidelity_one/aircraft_noise.py',
    '../regression/scripts/nonuniform_propeller_inflow/nonuniform_propeller_inflow.py',
    '../regression/scripts/optimization_packages/optimization_packages.py',
    '../regression/scripts/payload_range/payload_range.py',
    '../regression/scripts/plots/plot_test.py',
    '../regression/scripts/propeller/propeller_test.py',
    '../regression/scripts/propeller_speeds/range_endurance_speeds.py',
    '../regression/scripts/propulsion_surrogate/propulsion_surrogate.py',
    '../regression/scripts/ramjet_network/ramjet_network.py',
    '../regression/scripts/Regional_Jet_Optimization/Optimize2.py',
    '../regression/scripts/scramjet_network/scramjet_network.py',
    '../regression/scripts/rocket_network/Rocketdyne_F1.py',
    '../regression/scripts/rocket_network/Rocketdyne_J2.py',
    '../regression/scripts/segments/segment_test.py',
    '../regression/scripts/segments/transition_segment_test.py',
    '../regression/scripts/slipstream/slipstream_test.py',
    '../regression/scripts/slipstream/propeller_interactions.py',
    '../regression/scripts/solar_network/solar_network.py',
    '../regression/scripts/solar_network/solar_low_fidelity_network.py',
    '../regression/scripts/solar_radiation/solar_radiation.py',
    '../regression/scripts/SU2_surrogate/BWB-450.py',
    '../regression/scripts/sweeps/test_sweeps.py',
    '../regression/scripts/test_input_output/test_xml_read_write.py',
    '../regression/scripts/test_input_output/test_freemind_write.py',
    '../regression/scripts/turboelectric_HTS_ducted_fan_network/turboelectric_HTS_ducted_fan_network.py',
    '../regression/scripts/turboelectric_HTS_dynamo_ducted_fan_network/turboelectric_HTS_dynamo_ducted_fan_network.py',
    '../regression/scripts/variable_cruise_distance/variable_cruise_distance.py',
    '../regression/scripts/V_n_diagram/V_n_diagram_regression.py',
    '../regression/scripts/VTOL/test_Multicopter.py',
    '../regression/scripts/VTOL/test_Tiltwing.py',
    '../regression/scripts/VTOL/test_Stopped_Rotor.py',
    '../regression/scripts/weights/weights.py'
    
]

# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main(modules_to_test):

    # preallocate test results
    results = DataOrdered()
    for module in modules_to_test:
        results[module] = 'Untested'

    sys.stdout.write('# --------------------------------------------------------------------- \n')
    sys.stdout.write('#   SUAVE Automatic Regression \n')
    sys.stdout.write('#   %s \n' % time.strftime("%B %d, %Y - %H:%M:%S", time.gmtime()) )
    sys.stdout.write('# --------------------------------------------------------------------- \n')
    sys.stdout.write(' \n')

    # run tests
    all_pass = True
    for module in modules_to_test:
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
    main(modules)
