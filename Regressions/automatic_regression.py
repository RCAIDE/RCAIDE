# Regressions/automatic_regression.py
# (c) Copyright The Board of Trustees of RCAIDE

""" RCAIDE Regressions
"""
# Created:  Jun M. Clarke
# Modified: 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import matplotlib
import sys, os, traceback, time 
from Legacy.regression.automatic_regression import main as legacy_regressions
from Legacy.trunk.S.Core.DataOrdered import DataOrdered

matplotlib.use('Agg')  
 
# ----------------------------------------------------------------------------------------------------------------------
#  LIST OF MODULES
# ----------------------------------------------------------------------------------------------------------------------
'''  The "modules" list contains the name of the file you would like to run. Each test script must include a main 
     function, this will be called by this automatic regression script.
  '''
modules = [

    # ----------------------- Regression List -------------------------- 
    'Regression/Tests/mission_segments/segment_test.py', 
    
]

# ----------------------------------------------------------------------------------------------------------------------
#  RUN REGRESSIONS
# ----------------------------------------------------------------------------------------------------------------------

def regressions():
    
    legacy_pass_fail = legacy_regressions()

    # preallocate test results
    results = DataOrdered()
    for module in modules:
        results[module] = 'Untested'

    sys.stdout.write('# --------------------------------------------------------------------- \n')
    sys.stdout.write('#   RCAIDE Automatic Regression \n')
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

    if all_pass and legacy_pass_fail:
        sys.exit(0)
    else:
        sys.exit(1)

        
# ----------------------------------------------------------------------------------------------------------------------
# MPDULE TESTER 
# ----------------------------------------------------------------------------------------------------------------------

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
    regressions()
    
    
    
