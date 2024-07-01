## @ingroup Energy-Propulsion-Converters
# RCAIDE/Library/Compoments/Energy/Propulsion/Converters/Rotor.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports 
from RCAIDE.Framework.Core                              import Data , Units, Container 
from RCAIDE.Library.Components                          import Component 
from RCAIDE.Framework.Analyses.Propulsion               import Rotor_Wake_Fidelity_Zero  

# package imports
import numpy as np
import scipy as sp

# ---------------------------------------------------------------------------------------------------------------------- 
#  Generalized Rotor Class
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Propulsion-Converters
class Rotor(Component):
    """This is a general rotor component. 
    """
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
            Default model is the Blade Element Momentum Theory Model

        Source:
            None 
        """

        self.tag                               = 'rotor' 
        
        # geometric properties 
        self.number_of_blades                  = 0.0
        self.tip_radius                        = 0.0
        self.hub_radius                        = 0.0
        self.twist_distribution                = None
        self.sweep_distribution                = None          
        self.chord_distribution                = None
        self.thickness_to_chord                = None
        self.radius_distribution               = None
        self.mid_chord_alignment               = None 
        self.blade_solidity                    = 0.0 
        self.flap_angle                        = 0.0
        self.number_azimuthal_stations         = 24  
        self.vtk_airfoil_points                = 40        
        self.Airfoils                          = Airfoil_Container()
        self.airfoil_polar_stations            = None 
        
        # design point flight conditions 
        self.cruise                            = Data() 
        self.cruise.design_thrust              = None
        self.cruise.design_power               = None
        self.cruise.design_power_coefficient   = 0.01

        # Initialize the default wake set to Fidelity Zero 
        self.Wake                              = Rotor_Wake_Fidelity_Zero()         

        # operating conditions 
        self.induced_power_factor              = 1.48        # accounts for interference effects
        self.profile_drag_coefficient          = .03
        self.clockwise_rotation                = True
        self.phase_offset_angle                = 0.0
        self.orientation_euler_angles          = [0.,0.,0.]  # vector of angles defining default orientation of rotor 
        self.ducted                            = False
        self.sol_tolerance                     = 1e-8 
        self.use_2d_analysis                   = False       # True if rotor is at an angle relative to freestream or nonuniform freestream
        self.nonuniform_freestream             = False   
        self.axial_velocities_2d               = None        # user input for additional velocity influences at the rotor
        self.tangential_velocities_2d          = None        # user input for additional velocity influences at the rotor
        self.radial_velocities_2d              = None        # user input for additional velocity influences at the rotor 
        self.start_angle                       = 0.0         # angle of first blade from vertical
        self.start_angle_idx                   = 0           # azimuthal index at which the blade is started
        self.inputs.y_axis_rotation            = 0.          # vector of angles updated by the network during a mission
        self.inputs.pitch_command              = 0.          
        self.variable_pitch                    = False
        self.electric_propulsion_fraction      = 1.0 
        
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
         
    def append_airfoil(self,airfoil):
        """ Adds an airfoil to the segment

        Assumptions:
            None

        Source:
             None

        Args:
            None

        Returns:
            None

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
    
    def rotor_to_velocity_frame_rotation(self):
        """This rotates from the rotor's vehicle frame to the rotor's velocity frame

        Assumptions:
            There are two rotor frames, the rotor vehicle frame and the rotor velocity frame. When rotor
            is axially aligned with the vehicle body:
               - The velocity frame is X out the nose, Z towards the ground, and Y out the right wing
               - The vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
            None

        Args:
            None

        Returns:
            None 

        """

        rot_mat = sp.spatial.transform.Rotation.from_rotvec([0,np.pi,0]).as_matrix()

        return rot_mat
    

    def vehicle_to_velocity_frame_rotation(self):
        """This rotates from the system's body frame to the rotor's velocity frame

        Assumptions:
            There are two rotor frames, the vehicle frame describing the location and the rotor velocity frame.
            Velocity frame is X out the nose, Z towards the ground, and Y out the right wing
            Vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
            None

        Args:
            None

        Returns:
            None 

        """

        # Go from velocity to vehicle frame
        body_2_vehicle = sp.spatial.transform.Rotation.from_rotvec([0,np.pi,0]).as_matrix()

        # Go from vehicle frame to rotor vehicle frame: rot 1 including the extra body rotation
        cpts       = len(np.atleast_1d(self.inputs.y_axis_rotation))
        rots       = np.array(self.orientation_euler_angles) * 1.
        rots       = np.repeat(rots[None,:], cpts, axis=0)
        rots[:,1] += np.atleast_2d(self.inputs.y_axis_rotation)[:,0]
        
        vehicle_2_prop_vec = sp.spatial.transform.Rotation.from_rotvec(rots).as_matrix()

        # GO from the rotor vehicle frame to the rotor velocity frame: rot 2
        prop_vec_2_prop_vel = self.rotor_to_velocity_frame_rotation()

        # Do all the matrix multiplies
        rot1    = np.matmul(body_2_vehicle,vehicle_2_prop_vec)
        rot_mat = np.matmul(rot1,prop_vec_2_prop_vel)


        return rot_mat 

    def velocity_to_vehicle_frame_rotation(self):
        """This rotates from the rotor's velocity frame to the system's body frame

        Assumptions:
            There are two rotor frames, the vehicle frame describing the location and the rotor velocity frame
            velocity frame is X out the nose, Z towards the ground, and Y out the right wing
            vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
           None

        Args:
            None

        Returns:
            None 
        """

        body2propvel = self.vehicle_to_velocity_frame_rotation()

        r = sp.spatial.transform.Rotation.from_matrix(body2propvel)
        r = r.inv()
        rot_mat = r.as_matrix()

        return rot_mat 
 
## @ingroup Library-Components-Wings
class Airfoil_Container(Container):
    """ Container for rotor airfoil   
    """     

    def get_children(self):
        """ Returns the components that can go inside
        
        Assumptions:
            None
    
        Source:
           None
    
        Args:
            None
    
        Returns:
            None
        """       
        
        return []
