# Regressions/automatic_regression.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Regressions
"""
# Created:  Jun 2023, M. Clarke
# Modified: Oct 2023, Racheal M. Erhard

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.regression.automatic_regression import main as regressions




# ----------------------------------------------------------------------
#   RCAIDE Modules to Test
# ----------------------------------------------------------------------
RCAIDE_modules = [

    # ----------------------- Regression List --------------------------
    '../regression/scripts/propeller/propeller_test.py',
    
]

# ----------------------------------------------------------------------
#   Call Main
# ----------------------------------------------------------------------

if __name__ == '__main__':
    regressions(RCAIDE_modules)