import numpy as np
from scipy.optimize import root

# Sizing Problem for a Heat Exchanger

# Given values in the problem 
# Overall HEX properties
eff_hex     = 0.8381
delta_p_h   = 9.05 #KPa
delta_p_c   = 8.79 #KPa

# Inlet Temperatures 
T_i_h   = 900 #deg C
T_i_c   = 100 #deg C

# Inlet Pressures
P_i_h   = 160 #KPa
P_i_c   = 200 #KPa

# Hydraulic Diameters
d_h_c   = 0.00154 #m 
d_h_h   = 0.00154 #m

# Fin Height/Spaceing 
b_c     = 2.49 #mm
b_h     = 2.49 #mm 

# Fin thickness
delta_h = 0.102 #mm
delta_c = 0.102 #mm

#Fin and wall Conductivity 
k_f     = 18 #W/mK
k_w     = 18 #W/mK

# Ratio of finned area to total area 
Af_A_h  = 0.785  
Af_A_c  = 0.785

#Finned area density 
beta_h  = 2254 #m^2/m^3
beta_h  = 2254 #m^2/m^3

#mass flow rates of the fluids
m_dot_h = 1.66 #kg/s
m_dot_c = 2.00 #kg/s 

# The length, width, & height of this heat exchanger needs to be determined.

# Calculate the Outlet Temperatures 

T_o_h   = T_i_h-eff_hex*(T_i_h-T_i_c)
T_o_c   = T_i_c+(eff_hex*m_dot_h/m_dot_c)*(T_i_h-T_i_c)

# Evaluate the fluid properties at mean temperature 

T_m_h   =(T_o_h+T_i_h)/2
T_m_c   =(T_o_c+T_i_c)/2

# Evaluate the bulk Cp values 
c_p_h   = 1.117 #J/kg-K
c_p_c   = 1.079 #J/kg-K

# Update Outlet Air temperature 
T_o_c   = T_i_c+(eff_hex*m_dot_h/(m_dot_c*c_p_c))*(T_i_h-T_i_c)
T_m_c   =(T_o_c+T_i_c)/2

#The new value of c_p_c is very close to the old one so no further iterations are required. 

# Heat Capacity 
C_h     = m_dot_h*c_p_h
C_c     = m_dot_c*c_p_c

C_min, C_max = min(C_h, C_c), max(C_h, C_c)
C_r = C_min / C_max

# Solve for NTU 
def equation(NTU):
    return 1 - (1 - np.exp(((NTU[0]**0.22)/C_r)*(np.exp(-C_r*(NTU[0]**0.78))))) - eff_hex


# Initial guess for NTU
initial_guess = 2.0

# Solve for NTU using fsolve
#NTU_solution = fsolve(equation, initial_guess,xtol=1e-6)
#NTU= NTU_solution[0] 

# Solve for NTU using root 
result = root(equation, initial_guess)
NTU_solution = result.x
print(NTU_solution)