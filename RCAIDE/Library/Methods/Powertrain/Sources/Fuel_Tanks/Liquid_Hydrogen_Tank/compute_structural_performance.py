



from copy import deepcopy
from RCAIDE.Framework.Core import Units
import numpy as np
from scipy.optimize import minimize

def structural_solver(fuel_tank):#(mat_prop,H2_prop,mt,Vl,ul,AR,Ti,multipliers):

    #Reads properties, tank material (mt), LH2 volume (Vl), ullage volume fraction (ul),
    #tank aspect ratio (AR), H2 avg. temp (Ti), and relevant multipliers
    
    #Returns tank mass (mass) and tank geometry - inner length (li), inner radius (ri),
    #and outer radius (ro)

    
    n = 1.6 #structural factor of safety
    PI_P = 5 #internal pressure multiplier for structural sizing
    Ti =  fuel_tank.design_inlet_temperature

    P_sat   = fuel_tank.fuel.liquid_hydrogen_properties(Ti, "Pressure (MPa)")*Units.MPa #H2 saturation pressure
    Pi = PI_P*P_sat #design internal pressure
    Po = 0 #design external pressure
    tol = 1e-5

    if fuel_tank.symmetric:
        V_guess  = deepcopy(fuel_tank.external_volume*0.45) # Inital Estimate of the volume of liquid hydrogen in the tank
    else:
        V_guess = deepcopy(fuel_tank.external_volume*0.75) # Inital Estimate of the volume of liquid hydrogen in the tank)
    error = 100
    alpha = 0.5
    iteration = 0
    while abs(error)>tol and iteration <1000:
        
        V = V_guess/(1-fuel_tank.ullage_volume_fraction) #tank volume (including ullage)

        ri = ( V/(np.pi*(2*fuel_tank.aspect_ratio-2/3)) )**(1/3) #inner radius in m 
        li = 2*ri*fuel_tank.aspect_ratio #inner length in m
        
        ro_ri = minimize(tank_width,(1+1e-3),method='L-BFGS-B',tol=1e-5,args=(Pi,Po,fuel_tank)).x
        ro = ro_ri[0]*ri #outer radius in m
        fuel_tank.mass = (np.pi*(ro_ri*ri)**2*( (4/3)*(ro_ri*ri)+li-2*ri ) - V)*fuel_tank.material.density #tank mass in kg

        error = fuel_tank.outer_diameter/2 - ro
        rel_error = error / (fuel_tank.outer_diameter / 2)
        V_guess += alpha * rel_error 
        iteration +=1
        
    fuel_tank.inner_diameter = ri*2
    fuel_tank.inner_length  = li
    print(V/Units.gallons)
    
    return 


def tank_width(ro_ri,Pi,Po,fuel_tank):
        A = (Pi - Po*ro_ri**2)/(ro_ri**2 - 1) #Lame's constant 1
        B = (Pi - Po)*ro_ri**2/(ro_ri**2 - 1) #Lame's constant 2
        s1 = A + B #hoop stress
        s2 = A - B #radial stress
        s3 = A #axial stress
        sv = (np.sqrt( ( (s1-s2)**2 + (s2-s3)**2 + (s3-s1)**2 )/2 )) #von Mises stress
        return np.abs(sv - fuel_tank.material.yield_tensile_strength) #von Mises criteria
