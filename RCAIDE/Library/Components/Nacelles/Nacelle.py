# RCAIDE/Compoments/Nacelles/Nacelle.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from RCAIDE.Framework.Core              import Data 
from RCAIDE.Library.Components          import Component   
import scipy as sp
import numpy as np
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Nacalle
# ----------------------------------------------------------------------------------------------------------------------  
class Nacelle(Component):
    """ Default nacelle compoment class.
    """
    
    def __defaults__(self):
        """ This sets the default values for the component to function.
        
        Assumptions:
            None
    
        Source:
            None 
        """      
        
        self.tag                       = 'nacelle'
        self.origin                    = [[0.0,0.0,0.0]]
        self.aerodynamic_center        = [0.0,0.0,0.0]  
        self.areas                     = Data()
        self.areas.front_projected     = 0.0
        self.areas.side_projected      = 0.0
        self.areas.wetted              = 0.0 
        self.diameter                  = 0.0 
        self.inlet_diameter            = 0.0
        self.has_pylon                 = True 
        self.fuselage_integrated       = False 
        self.length                    = 0.0   
        self.orientation_euler_angles  = [0.,0.,0.]    
        self.flow_through              = True 
        self.cowling_airfoil_angle     = 0.0
        
    def append_operating_conditions(self,segment,fuel_line,propulsor):  
        return

    def nac_vel_to_body(self):
        """This rotates from the systems body frame to the nacelles velocity frame

        Assumptions:
            There are two nacelle frames, the vehicle frame describing the location and the nacelle velocity frame
            velocity frame is X out the nose, Z towards the ground, and Y out the right wing
            vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
            None

        Args:
            self  (dict): nacelle data object 

        Returns:
            rot_mat (numpy.ndarray) : rotated matrix array 
        """
        
        body2nacvel = self.body_to_nac_vel()
        
        r = sp.spatial.transform.Rotation.from_matrix(body2nacvel)
        r = r.inv()
        rot_mat = r.as_matrix()

        return rot_mat
    
    def body_to_nac_vel(self):
        """This rotates from the systems body frame to the nacelles velocity frame

        Assumptions:
            There are two nacelle frames, the vehicle frame describing the location and the nacelle velocity frame
            velocity frame is X out the nose, Z towards the ground, and Y out the right wing
            vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing Y out the right wing

        Source:
            None

        Args:
            self  (dict): nacelle data object 

        Returns:
            rot_mat (numpy.ndarray) : rotated matrix array 
        """
        
        # Go from body to vehicle frame
        body_2_vehicle = sp.spatial.transform.Rotation.from_rotvec([0,np.pi,0]).as_matrix()
        
        # Go from vehicle frame to nacelle vehicle frame: rot 1 including the extra body rotation
        rots    = np.array(self.orientation_euler_angles) * 1. 
        vehicle_2_nac_vec = sp.spatial.transform.Rotation.from_rotvec(rots).as_matrix()        
        
        # GO from the nacelle vehicle frame to the nacelle velocity frame: rot 2
        nac_vec_2_nac_vel = self.rotor_to_velocity_frame_rotation()
        
        # Do all the matrix multiplies
        rot1    = np.matmul(body_2_vehicle,vehicle_2_nac_vec)
        rot_mat = np.matmul(rot1,nac_vec_2_nac_vel) 
        return rot_mat    
    

    def rotor_to_velocity_frame_rotation(self):
        """This rotates from the nacelles vehicle frame to the nacelles velocity frame

        Assumptions:
            There are two nacelle frames, the vehicle frame describing the location and the nacelle velocity frame
            velocity frame is X out the nose, Z towards the ground, and Y out the right wing
            vehicle frame is X towards the tail, Z towards the ceiling, and Y out the right wing

        Source:
            None

        Args:
            self  (dict): nacelle data object 

        Returns:
            rot_mat (numpy.ndarray) : rotated matrix array 
        """
        
        rot_mat = sp.spatial.transform.Rotation.from_rotvec([0,np.pi,0]).as_matrix()
        
        return rot_mat
    
    
        