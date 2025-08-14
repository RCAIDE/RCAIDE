
from re import I
import numpy as np
from scipy.optimize import minimize

from RCAIDE.Framework.Core import Units
import RCAIDE


def thermal_solver_basic(fuel_tank):#mat_prop,H2_prop,atmos_prop,mt,mi,li,ri,ro,Ti,Ta,Qo,multipliers):

    #Reads properties, tank material (mt), insulation material (mi), tank geometry - 
    #inner length (li), inner radius (ri), outer radius (ro), H2 temperature (Ti), 
    #ambient temperature (Ta), allowable heat flux (Qo), and multipliers

    #Returns insulation thickness (t_ins) and insulation mass (mass_ins)
    PI_Q = 1.5 #heat flow multiplier for thermal sizing
    PI_M = 1.25 #total mass multiplier

    
    atmosphere = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmo_data  = atmosphere.compute_values(fuel_tank.design_altitude,fuel_tank.design_isa_deviation)
  
    
    p   = atmo_data.pressure          
    rho_air = atmo_data.density             
    mu_air  = atmo_data.dynamic_viscosity
    k_air = atmo_data.thermal_conductivity   
    Ta = atmo_data.temperature
    Cp_air = atmosphere.fluid_properties.compute_cp(Ta) 
    g = 9.81  

    ro = fuel_tank.outer_diameter/2
    ri = fuel_tank.inner_diameter/2
    li = fuel_tank.inner_length 


   

    t_ins = minimize(insulation_width,0.01,bounds=[(1e-8,1e8)],method='L-BFGS-B',tol=1e-10,args=(Ta,PI_Q,fuel_tank,atmo_data)).x

    a_ins = 2*np.pi*ro*(li-2*ri) + 4*np.pi*ro**2
    v_ins = (np.pi*(ro+t_ins)**2*(li-2*ri) + (4/3)*np.pi*(ro+t_ins)**3) - (np.pi*ro**2*(li-2*ri) + (4/3)*np.pi*ro**3)

    mass_ins = v_ins*fuel_tank.insulation_material.density + a_ins*fuel_tank.insulation_material.specific_density
    
    t_ins = t_ins[0]
    mass_ins = mass_ins[0]
    print("Insulation thickness (in)=",t_ins/Units.inches)
    print("Insulation mass (lbs)=",mass_ins/Units.lbs)
    
    return t_ins, mass_ins


def insulation_width(t_ins,Ta,PI_Q,fuel_tank,atmo_data):   
    ri = fuel_tank.inner_diameter/2
    li = fuel_tank.inner_length 
    Ti = fuel_tank.design_inlet_temperature
    Qo = fuel_tank.acceptable_heat_leak

    Te = minimize(heat_transfer_wrap,(Ta[0]+Ti)/2,method='L-BFGS-B',bounds=[(Ti,Ta)],tol=1e-10,args=(t_ins,fuel_tank,atmo_data)).x

    #Qv_amb, Qr_amb, Qc_mat = heat_transfer(Te) 
    Qc_mat = fuel_tank.insulation_wall_conductive_heat_transfer
    t_ins = np.abs(PI_Q*Qc_mat/(2*np.pi*ri*(li-2*ri) + 4*np.pi*ri**2) - Qo)
    return t_ins



def heat_transfer_wrap(Te,t_ins,fuel_tank,atmo_data):
    ro = fuel_tank.outer_diameter/2
    ri = fuel_tank.inner_diameter/2
    li = fuel_tank.inner_length 
    p   = atmo_data.pressure          
    rho_air = atmo_data.density             
    mu_air  = atmo_data.dynamic_viscosity
    k_air = atmo_data.thermal_conductivity   
    Ta = atmo_data.temperature
    atmosphere = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    Cp_air = atmosphere.fluid_properties.compute_cp(Ta) 
    g = 9.81
    Ti = fuel_tank.design_inlet_temperature

    nu = mu_air/rho_air #kinematic viscosity
    alpha = k_air/(rho_air*Cp_air) #thermal diffusivity
    Pr = nu/alpha #Prandtl number
    Ra = (g/Ta)*(Ta - Te)*(2*ro+2*t_ins)**3/(alpha*nu) #Rayleigh number
    
    #Heat transfer through cylindrical tank side
    Nu_cyl = ( 0.60 + 0.387*Ra**(1/6)/(1 + (0.559/Pr)**(9/16))**(8/27) )**2 #Nusselt number for cylinder
    h_cyl = Nu_cyl*k_air/(2*ro + 2*t_ins) #heat transfer coefficient for cylinder
    
    Qv_amb_cyl = h_cyl*(np.pi*(2*ro+2*t_ins)*(li-2*ri))*(Ta-Te) #ambient to insulation convective heat transfer
    Qr_amb_cyl = (5.67*10**-8)*0.03*(np.pi*(2*ro+2*t_ins)*(li-2*ri))*(Ta**4 - Te**4) #ambient to insulation radiative heat transfer
    Qc_mat_cyl = (Te-Ti)/(np.log(ro/ri)/(2*np.pi*(li-2*ri)*fuel_tank.material.thermal_conductivity) + np.log((ro+t_ins)/ro)/(2*np.pi*(li-2*ri)*fuel_tank.insulation_material.thermal_conductivity)) #insulation and wall conductive heat transfer 
    
    # #Heat transfer through spherical tank endcaps
    Nu_sph = 2 + 0.589*Ra**(1/4)/(1 + (0.469/Pr)**(9/16))**(4/9) #Nusselt number for sphere
    h_sph = Nu_sph*k_air/(2*ro + 2*t_ins) #heat transfer coefficient for sphere
    
    Qv_amb_sph = h_sph*(np.pi*(2*ro+2*t_ins)**2)*(Ta-Te) #ambient to insulation convective heat transfer
    Qr_amb_sph = (5.67*10**-8)*0.03*(np.pi*(2*ro+2*t_ins)**2)*(Ta**4 - Te**4) #ambient to insulation radiative heat transfer
    Qc_mat_sph = (Te-Ti)/( (ro-ri)/(4*np.pi*fuel_tank.material.thermal_conductivity*ri*ro) + t_ins/(4*np.pi*fuel_tank.insulation_material.thermal_conductivity*ro*(ro+t_ins)) ) #insulation and wall conductive heat transfer
    
    Qv_amb = Qv_amb_cyl + Qv_amb_sph #total ambient to insulation convective heat transfer
    Qr_amb = Qr_amb_cyl + Qr_amb_sph #total ambient to insulation radiative heat transfer
    Qc_mat = Qc_mat_cyl + Qc_mat_sph #total insulation and wall conductive heat transfer
    fuel_tank.insulation_wall_conductive_heat_transfer = Qc_mat
    return np.abs(Qv_amb + Qr_amb - Qc_mat)