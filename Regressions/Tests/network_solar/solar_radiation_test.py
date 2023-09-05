# Regression/scripts/Tests/network_solar/solar_radiation_test.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE
from RCAIDE.Core import Units, Data, Container 

# python imports 
import numpy as np
import copy, time 

# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------
def main():
    
    # Setup and pack inputs, test several cases
    
    conditions                                     = Data()
    conditions.frames                              = Data()
    conditions.frames.body                         = Data()    
    conditions.frames.planet                       = Data()
    conditions.frames.inertial                     = Data()
    conditions.freestream                          = Data()
    conditions.frames.body.inertial_rotations      = np.zeros((4,3))
    conditions.frames.planet.start_time            = time.strptime("Thu, Mar 20 12:00:00  2014", "%a, %b %d %H:%M:%S %Y",)
    conditions.frames.planet.latitude              = np.array([[0.0],[35],[70],[0.0]])
    conditions.frames.planet.longitude             = np.array([[0.0],[0.0],[0.0],[0.0]])
    conditions.frames.body.inertial_rotations[:,0] = np.array([0.0,np.pi/10,np.pi/5,0.0]) # Phi
    conditions.frames.body.inertial_rotations[:,1] = np.array([0.0,np.pi/10,np.pi/5,0.0]) # Theta
    conditions.frames.body.inertial_rotations[:,2] = np.array([0.0,np.pi/2,np.pi,0.0])    # Psi
    conditions.freestream.altitude                 = np.array([[600000.0],[0.0],[60000],[1000]])
    conditions.frames.inertial.time                = np.array([[0.0],[0.0],[0.0],[43200]])
    
    # Call solar radiation
    rad    = RCAIDE.Energy.Processes.Solar_Radiation()
    fluxes = rad.solar_radiation(conditions)
    
    print('Solar Fluxes')
    print(fluxes)
    truth_fluxes = [[ 1365.96369614],[  853.74651524],[  820.78323974],[    0.        ]]

    
    max_error =  np.max(np.abs(fluxes-truth_fluxes))
    
    assert( max_error < 1e-5 )
    
    return

# ----------------------------------------------------------------------------------------------------------------------
#   Call Main
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
    