# RCAIDE/Library/Components/Powertrain/Energy/Sources/Fuel_Tanks/Non_Integral_Tank.py
# 
# 
# Created:  Aug 2025, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Framework.Core import Units

# Python Imports
from copy import deepcopy
import numpy as np
from scipy.optimize import minimize

# ----------------------------------------------------------------------------------------------------------------------
#  Structural Solver
# ---------------------------------------------------------------------------------------------------------------------    
def structural_solver(fuel_tank):
    
    n = 1.6 #structural factor of safety
    PI_P = 5 #internal pressure multiplier for structural sizing
    Ti =  fuel_tank.design_inlet_temperature

    P_sat   = fuel_tank.fuel.liquid_hydrogen_properties(Ti, "Pressure (MPa)")*Units.MPa #H2 saturation pressure
    Pi = PI_P*P_sat #design internal pressure
    Po = fuel_tank.design_external_pressure
  
    if fuel_tank.symmetric:
        V_guess  = deepcopy(fuel_tank.outer_volume*0.45) # Inital Estimate of the volume of liquid hydrogen in the tank
    else:
        V_guess = deepcopy(fuel_tank.outer_volume*0.75) # Inital Estimate of the volume of liquid hydrogen in the tank)
    
    tol = 1e-5
    error = 100
    alpha = 0.5
    iteration = 0
    while abs(error)>tol and iteration <1000:
        
        V = V_guess/(1-fuel_tank.ullage_volume_fraction) #tank volume (including ullage)

        ri = ( V/(np.pi*(2*fuel_tank.aspect_ratio-2/3)) )**(1/3) #inner radius in m 
        li = 2*ri*fuel_tank.aspect_ratio #inner length in m
        
        ro_ri = minimize(tank_width,(1+1e-3),method='L-BFGS-B',tol=1e-5,args=(Pi,Po,n,fuel_tank)).x
        ro = ro_ri[0]*ri #outer radius in m
        fuel_tank.mass = (np.pi*(ro_ri*ri)**2*( (4/3)*(ro_ri*ri)+li-2*ri) - V)*fuel_tank.material.density #tank mass in kg

        error = fuel_tank.outer_diameter/2 - ro
        rel_error = error / (fuel_tank.outer_diameter / 2)
        fuel_tank.fuel_volume = V_guess
        V_guess += alpha * rel_error 
        iteration +=1
        
    fuel_tank.inner_diameter = ri*2
    fuel_tank.internal_volume = V
    fuel_tank.inner_length  = li

    if fuel_tank.symmetric:
        fuel_tank.fuel_volume *= 2 
        fuel_tank.internal_volume = V*2
    
    return 


def tank_width(ro_ri,Pi,Po,n,fuel_tank):
        A = (Pi - Po*ro_ri**2)/(ro_ri**2 - 1) #Lame's constant 1
        B = (Pi - Po)*ro_ri**2/(ro_ri**2 - 1) #Lame's constant 2
        s1 = A + B #hoop stress
        s2 = A - B #radial stress
        s3 = A #axial stress
        sv = (np.sqrt( ( (s1-s2)**2 + (s2-s3)**2 + (s3-s1)**2 )/2 )) #von Mises stress
        return np.abs(sv - fuel_tank.material.yield_tensile_strength/n) #von Mises criteria
