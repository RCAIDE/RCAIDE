## @ingroup Energy-Propulsion-Converters
# RCAIDE/Library/Compoments/Energy/Propulsion/Converters/Rotor.py
# 
# 
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports 
from RCAIDE.Framework.Core                              import Data , Units, Container
from RCAIDE.Library.Components                          import Component 
from RCAIDE.Framework.Analyses.Propulsion               import Rotor_Wake_Fidelity_Zero 
from RCAIDE.Library.Methods.Propulsors.Converters.Rotor.append_rotor_conditions import  append_rotor_conditions

# package imports
import numpy as np
import scipy as sp

# ---------------------------------------------------------------------------------------------------------------------- 
#  Generalized Rotor Class
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Propulsion-Converters
class Rotor(Component):
    """This is a general rotor component.

    Assumptions:
    None

    Source:
    None
    """
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """

        self.tag                               = 'rotor' 
        
        # geometry properties 
        self.number_of_blades                  = 0.0
        self.tip_radius                        = 0.0
        self.hub_radius                        = 0.0
        self.twist_distribution                = 0.0
        self.sweep_distribution                = 0.0         # quarter chord offset from quarter chord of root airfoil
        self.chord_distribution                = 0.0
        self.thickness_to_chord                = 0.0
        self.radius_distribution               = None
        self.mid_chord_alignment               = 0.0
        self.blade_solidity                    = 0.0 
        self.flap_angle                        = 0.0
        self.number_azimuthal_stations         = 24  
        self.vtk_airfoil_points                = 40        
        self.Airfoils                          = Airfoil_Container()
        self.airfoil_polar_stations            = None 
        
        # design flight conditions 
        self.cruise                            = Data() 
        self.cruise.design_power               = None
        self.cruise.design_thrust              = None
        self.cruise.design_power_coefficient   = 0.01 

        # operating conditions 
        self.induced_power_factor              = 1.48        # accounts for interference effects
        self.profile_drag_coefficient          = .03
        self.clockwise_rotation                = True
        self.phase_offset_angle                = 0.0
        self.orientation_euler_angles          = [0.,0.,0.]  # vector of angles defining default orientation of rotor
        self.pitch_command                     = 0.0
        self.ducted                            = False
        self.sol_tolerance                     = 1e-8 
        self.use_2d_analysis                   = False       # True if rotor is at an angle relative to freestream or nonuniform freestream
        self.nonuniform_freestream             = False   
        self.axial_velocities_2d               = None        # user input for additional velocity influences at the rotor
        self.tangential_velocities_2d          = None        # user input for additional velocity influences at the rotor
        self.radial_velocities_2d              = None        # user input for additional velocity influences at the rotor 
        self.start_angle                       = 0.0         # angle of first blade from vertical
        self.start_angle_idx                   = 0           # azimuthal index at which the blade is started 
        self.variable_pitch                    = False
        self.electric_propulsion_fraction      = 1.0

        # Initialize the default wake set to Fidelity Zero 
        self.Wake                      = Rotor_Wake_Fidelity_Zero() 
        
        # blade optimization parameters     
        self.optimization_parameters                                    = Data() 
        self.optimization_parameters.tip_mach_range                     = [0.3,0.7] 
        self.optimization_parameters.multiobjective_aeroacoustic_weight = 1.0
        self.optimization_parameters.multiobjective_performance_weight  = 1.0
        self.optimization_parameters.multiobjective_acoustic_weight     = 1.0
        self.optimization_parameters.noise_evaluation_angle             = 135 * Units.degrees 
        self.optimization_parameters.tolerance                          = 1E-4
        self.optimization_parameters.ideal_SPL_dBA                      = 30
        self.optimization_parameters.ideal_efficiency                   = 1.0     
        self.optimization_parameters.ideal_figure_of_merit              = 1.0

    def append_operating_conditions(rotor,segment,distribution_line,propulsor): 
        energy_conditions       = segment.state.conditions.energy[distribution_line.tag][propulsor.tag]
        noise_conditions        = segment.state.conditions.noise[distribution_line.tag][propulsor.tag]
        append_rotor_conditions(rotor,segment,energy_conditions,noise_conditions)
        return        
         
    def append_airfoil(self,airfoil):
        """ Adds an airfoil to the segment

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """  
        # assert database type
        if not isinstance(airfoil,Data):
            raise Exception('input component must be of type Data()')


        # See if the component exists, if it does modify the name
        keys = self.keys()
        if airfoil.tag in keys:
            string_of_keys = "".join(self.keys())
            n_comps = string_of_keys.count(airfoil.tag)
            airfoil.tag = airfoil.tag + str(n_comps+1)    
            
        # store data
        self.Airfoils.append(airfoil)
    
    def vec_to_vel(self):
        """This rotates from the propeller's vehicle frame to the propeller's velocity frame

        Assumptions:
        There are two propeller frames, the propeller vehicle frame and the propeller velocity frame. When propeller
        is axially aligned with the vehicle body:
           - The velocity frame is X out the nose, Z towards the ground, and Y out the right wing
           - The vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """

        rot_mat = sp.spatial.transform.Rotation.from_rotvec([0,np.pi,0]).as_matrix()

        return rot_mat
    

    def body_to_prop_vel(self,rotor_conditions):
        """This rotates from the system's body frame to the propeller's velocity frame

        Assumptions:
        There are two propeller frames, the vehicle frame describing the location and the propeller velocity frame.
        Velocity frame is X out the nose, Z towards the ground, and Y out the right wing
        Vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """

        # Go from velocity to vehicle frame
        body_2_vehicle = sp.spatial.transform.Rotation.from_rotvec([0,np.pi,0]).as_matrix()

        # Go from vehicle frame to propeller vehicle frame: rot 1 including the extra body rotation
        cpts       = len(np.atleast_1d(rotor_conditions.orientation))
        rots       = np.array(self.orientation_euler_angles) * 1.
        rots       = np.repeat(rots[None,:], cpts, axis=0)
        rots[:,0] += rotor_conditions.orientation[:,0]
        rots[:,1] += rotor_conditions.orientation[:,1]
        rots[:,2] += rotor_conditions.orientation[:,2]
        
        vehicle_2_prop_vec = sp.spatial.transform.Rotation.from_rotvec(rots).as_matrix()

        # GO from the propeller vehicle frame to the propeller velocity frame: rot 2
        prop_vec_2_prop_vel = self.vec_to_vel()

        # Do all the matrix multiplies
        rot1    = np.matmul(body_2_vehicle,vehicle_2_prop_vec)
        rot_mat = np.matmul(rot1,prop_vec_2_prop_vel)
 
        return rot_mat , rots


    def prop_vel_to_body(self,rotor_conditions):
        """This rotates from the propeller's velocity frame to the system's body frame

        Assumptions:
        There are two propeller frames, the vehicle frame describing the location and the propeller velocity frame
        velocity frame is X out the nose, Z towards the ground, and Y out the right wing
        vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """

        body2propvel,rots = self.body_to_prop_vel(rotor_conditions)

        r = sp.spatial.transform.Rotation.from_matrix(body2propvel)
        r = r.inv()
        rot_mat = r.as_matrix()

        return rot_mat, rots
    
    def vec_to_prop_body(self,rotor_conditions):
        rot_mat, rots =  self.prop_vel_to_body(rotor_conditions) 
        return rot_mat, rots

 
## @ingroup Library-Components-Wings
class Airfoil_Container(Container):
    """ Container for rotor airfoil  
    
    Assumptions:
    None

    Source:
    N/A

    Inputs:
    None

    Outputs:
    None

    Properties Used:
    N/A
    """     

    def get_children(self):
        """ Returns the components that can go inside
        
        Assumptions:
        None
    
        Source:
        N/A
    
        Inputs:
        None
    
        Outputs:
        None
    
        Properties Used:
        N/A
        """       
        
        return []
