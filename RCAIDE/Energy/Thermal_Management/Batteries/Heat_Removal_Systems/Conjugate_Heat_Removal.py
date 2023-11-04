# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Core import Data , Units
from RCAIDE.Attributes.Coolants.Glycol_Water import Glycol_Water
from RCAIDE.Energy.Energy_Component            import Energy_Component  
from RCAIDE.Attributes.Solids.Aluminum       import Aluminum  
     
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
# Conjugate_Heat_Removal_System  
# ----------------------------------------------------------------------------------------------------------------------
class Conjugate_Heat_Removal(Energy_Component):
    
    def __defaults__(self):  
        self.tag                          = 'Conjugate_Heat_Removal_System' 
        self.heat_transfer_efficiency     = 1.0
        
        self.coolant                      = Glycol_Water()
        self.coolant_Reynolds_number       = 1.
        self.coolant_velocity              = 1.
        self.coolant_flow_rate_per_module  = 1.
        self.coolant_flow_rate             = 0.1
        self.coolant_hydraulic_diameter    = 1.
        self.channel_side_thickness        = 0.002                  # Thickness of the Chanel through which condcution occurs 
        self.channel_top_thickness         = 0.002                  # Thickness of Channel on the top where no conduction occurs
        self.channel_width                 = 0.01                   # width of the channel 
        self.channel_height                = 0.03                   # height of the channel 
        self.channel_contact_angle         = 47.5 * Units.degrees   # Contact Arc angle in degrees    
        self.channel_thermal_conductivity  = 237                    # Conductivity of the Channel
        self.channel_density               = 2710                   # Denisty of the Channel
        self.channel_aspect_ratio          = 1. 
        self.channels_per_module           = 1
        self.battery_contact_area          = 1.
        self.contact_area_per_module       = 1.  
        self.power_draw                    = 1.    
        self.coolant_inlet_temperature     = None
        self.design_battery_temperature    = None
        self.design_heat_generated         = None    
    
    def compute_heat_removed(self,battery, Q_heat_gen,numerics, freestream):
        """Computes the net heat generated in a battery module during cycling.
        Assumptions:
        1) Battery pack cell heat transfer can be modelled as a cooling columns in a cross-flow
        2) Isothermal battery cell - the temperature at the center of the cell is the same at
        the surface of the cell
    
        Inputs:
            battery.
                  h                         (heat transfer coefficient)  [W/(m^2*K)]
                  As_cell                   (battery cell surface area)  [meters^2]
                  H_cell                    (battery cell height)        [meters]
                  T_ambient                 (ambient temperature)        [Kelvin]
                  T_current                 (pack temperature)           [Kelvin]
                  T_cell                    (battery cell temperature)   [Kelvin]
                  heat_transfer_efficiency                               [unitless]
    
          Outputs:
            battery.
                 net_power                                               [Watts]
        """
        # ---------------------------------------------------------------------
        #   Default code from the air cooling
        # --------------------------------------------------------------------- 
        T_ambient                = freestream.temperature  
        T_current                = battery.pack.temperature      
        cell_mass                = battery.cell.mass
        Cp                       = battery.cell.specific_heat_capacity
        I                        = numerics.time.integrate
        heat_transfer_efficiency = self.heat_transfer_efficiency  
    
        Nn                = battery.module.geometrtic_configuration.normal_count            
        Np                = battery.module.geometrtic_configuration.parallel_count   
        n_total_module    = Nn*Np   
    
        # ---------------------------------------------------------------------
        #   Input Thermophysical Properties
        # --------------------------------------------------------------------- 
        # coolant liquid
        Coolant      = Glycol_Water() 
        k_coolant    = Coolant.thermal_conductivity
        cp_coolant   = Coolant.specific_heat_capacity 
        Pr_coolant   = Coolant.Prandtl_number
        
        # wavy channel material
        Channel   = Aluminum() 
        k_chan    = Channel.thermal_conductivity 
    
        # ---------------------------------------------------------------------
        #   Calculate the Output Temperature
        # ---------------------------------------------------------------------
        # heat transfer coefficient & heat transfer area
        m_dot_h_module              = self.coolant_flow_rate_per_module
        A_chan_module               = self.contact_area_per_module
        Re_coolant                  = self.coolant_Reynolds_number
        gamma_chan                  = self.aspect_ratio_of_chan
        d_H                         = self.coolant_hydraulic_diameter
        b                           = self.cross_section.b
        
        if Re_coolant <= 2300:
            # Nusselt number
            Nu = 8.235 * (1 - 2.0421 * gamma_chan + 3.0853 * np.power(gamma_chan, 2) - 2.4765 * np.power(gamma_chan, 3)
                          + 1.0578 * np.power(gamma_chan, 4) - 0.1861 * np.power(gamma_chan, 5))
            # Colburn factor
            j_coolant = Nu / Re_coolant * np.power(Pr_coolant, -1 / 3)
        else:
            # Colburn factor
            f_coolant = 1 / (4 * (1.8 * np.log10(Re_coolant / 7.7)) ** 2)
            # use Gnielinski equation to calculate Nu for 0.5 < Pr < 2000, 3000 < Re < 5e6
            Nu = (f_coolant / 2) * (Re_coolant - 1000) * Pr_coolant / (
                    1 + 12.7 * np.power((f_coolant / 2), 0.5) * (np.power(Pr_coolant, 2 / 3) - 1))
            # Colburn factor
            j_coolant = Nu / Re_coolant * np.power(Pr_coolant, -1 / 3)
    
        # heat transfer coefficient of channeled coolant fluid
        h_coolant = k_coolant * Nu / d_H
        # total heat transfer coefficient
        h_tot = 1 / (1 / h_coolant + b / k_chan)
    
        # number of transfer units and effectiveness
        NTU                     = h_tot * A_chan_module / (m_dot_h_module * cp_coolant)
        eff_WavyChan            = 1 - np.exp(-NTU)
    
        # log mean temperature
        T_i                     = self.operating_conditions.wavy_channel_inlet_temperature
        Tw_Ti                   = T_current - T_i
        Tw_To                   = Tw_Ti * np.exp(-NTU)
        dT_lm                   = (Tw_Ti - Tw_To) / np.log(Tw_Ti / Tw_To)
    
        # convective heat from the battery
        Q_convec                = heat_transfer_efficiency * h_tot * A_chan_module * dT_lm
        Q_convec[Tw_Ti == 0.]   = 0.
    
        # check the heat generated
        T_o                     = T_current - Tw_To
        Q_conv_check            = m_dot_h_module * cp_coolant * (T_o - T_i)
        delta_Q_conv = np.abs(Q_convec - Q_conv_check) 
    
        # check the wavy channel effectiveness
        eff_WavyChan_check      = (T_o - T_i) / (T_current - T_i)
        delta_eff_WavyChan      = np.abs(eff_WavyChan - eff_WavyChan_check)
    
        # net heat stored in the battery
        P_net                   = Q_heat_gen*n_total_module - Q_convec
    
        # temperature rise [update cell temperature]
        #print( P_net )
        dT_dt                   = P_net/(cell_mass*n_total_module*Cp)
        T_current               = T_current[0] + np.dot(I,dT_dt)
        T_current[T_ambient>T_current] = T_ambient[T_ambient>T_current]
    
        return T_current, Q_convec, T_o, eff_WavyChan    
 