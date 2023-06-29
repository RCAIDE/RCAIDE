# Regressions/automatic_regression.py
# (c) Copyright The Board of Trustees of RCAIDE

""" RCAIDE Regressions
"""
# Created:  Jun M. Clarke
# Modified: 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import sys, os, traceback, time

from Legacy.regression.automatic_regression import main as legacy_regressions

def regressions():
    
    pass_fail = legacy_regressions()
    
    return pass_fail

# ----------------------------------------------------------------------
#   Call Main
# ----------------------------------------------------------------------

if __name__ == '__main__':
    regressions()