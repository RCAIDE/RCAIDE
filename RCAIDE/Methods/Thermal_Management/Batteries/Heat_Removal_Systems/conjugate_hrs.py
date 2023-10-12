
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports   

# python packaged 
import numpy as np
from scipy.optimize import minimize

def design_conjugate_cooling_heat_removal_system(hrs,battery,inlet_coolant_temperature = 278 ,T_bat = 315, Q_gen = 50000):
    
    # solve for mass flow rate in the channel    
    opt_params = size_conjugate_cooling(hrs,battery,inlet_coolant_temperature,T_bat,Q_gen)
        
    m_coolant =  opt_params[0]
    Q_convec  = 0 # add correct variable 
    return 


def size_conjugate_cooling(hrs,battery,inlet_coolant_temperature,T_bat, Q_gen, m_coolant_lower_bound=0.01, m_coolant_upper_bound=10.0 ): 

    arguments = (hrs,battery,inlet_coolant_temperature,T_bat, Q_gen)
    
    cons = [{'type':'eq', 'fun': constraint_1,'args': arguments}] 
    initials = [0.1]
    bnds = [(m_coolant_lower_bound, m_coolant_upper_bound)]

    sol = minimize(objective,initials , args=arguments , method='SLSQP', bounds=bnds, tol=1e-6) 
    
    if sol.success == False:
        print('Sizing Failed ')
    return sol.x   


# objective function
def objective(x,hrs,battery,inlet_coolant_temperature,T_bat,Q_gen) : 
    m_coolant = x[0] 
    
    # Battery 
    d_cell    = battery.cell.diameter                    
    h_cell    = battery.cell.height                      
    A_cell    = np.pi*d_cell*h_cell                      
    N_battery = battery.pack.electrical_configuration.total
     
    # Inital Channel Geometric Properties    
    b        = hrs.channel_thickness                    
    d        = hrs.channel_width                        
    c        = hrs.channel_height                       
    theta    = hrs.channel_contact_angle     
    k_chan   = hrs.channel_thermal_conductivity                   # Conductivity of the Channel (Replace with function)    
    coolant  = hrs.coolant
    AR       = d/c    
    T_i      = inlet_coolant_temperature 
    
    # Surface area of the channel 
    A_chan = N_battery*theta*A_cell/360

    # Hydraullic diameter    
    dh = (4*c*d)/(2*(c+d))   
 
    # Thermophysical Properties of Coolant  
    rho  = coolant.density
    mu   = coolant.compute_absolute_viscosity(T_i)  
    cp   = coolant.compute_cp(T_i)
    Pr   = coolant.compute_prandtl_number(T_i) 
    k    = coolant.compute_thermal_conductivity(T_i) 
 
    # COMPUTE POWER  Q_convec  
    
    #calculate the velocity of the fluid in the channel 
    v=rho*c*d*m_coolant
    
    # calculate the Reynolds Number 
    Re=(rho*dh*v)/mu
    
    # fanning friction factor (eq 32)
    if Re< 2300:
        f= 24*(1-(1.3553*AR)+(1.9467*AR**2)-(1.7012*AR**3)+(0.9564*AR**4)-(0.2537*AR**5))
    elif Re>=2300:
        f= (0.0791*(Re**(-0.25)))*(1.8075-0.1125*AR)
        
    # Nusselt Number (eq 12)   
    if Re< 2300:
        Nu= 8.235*(1-(2.0421*AR)+(3.0853*AR**2)-(2.4765*AR**3)+(1.0578*AR**4)-(0.1861*AR**5))    
    elif Re >= 2300:
        Nu = ((f/2)*(Re-1000)*Pr)/(1+(12.7*(f**0.5)*(Pr**(2/3)-1)))   
    
    # heat transfer coefficient of the channeled coolant (eq 11)
    h = k*Nu/dh
    
    # Overall Heat Transfer Coefficient from battery surface to the coolant fluid (eq 10)
    U_total = 1/((1/h)+(b/k_chan))
    
    # Calculate NTU
    NTU = U_total*A_chan/(m_coolant*cp)
    
    # Calculate Outlet Temparture To ( eq 8)
    T_o = ((T_bat-T_i)*(1-np.exp(-NTU)))+T_i
    
    # Calculate the Log mean temperature 
    T_lm = ((T_bat-T_i)-(T_bat-T_o))/(np.log((T_bat-T_i)/(T_bat-T_o)))
    
    # Calculated Heat Convected 
    Q_conv = U_total*A_chan*T_lm
    
    
    # COMPUTE POWER 
    
    
    # COMPUTE WEIGHT 
    
    
    
    # Residuals
    Heat_Residual = Q_gen-Q_conv
    
    return  Heat_Residual


# hard efficiency constraint
def constraint_1( x,hrs,battery,inlet_coolant_temperature,T_bat,Q_gen): 
    
    
    return 0

 