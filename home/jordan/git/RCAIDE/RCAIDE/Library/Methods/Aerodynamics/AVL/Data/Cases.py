## @ingroup Methods-Aerodynamics-AVL-Data
# Cases.py
# 
# Created:  Oct 2014, T. Momose
# Modified: Jan 2016, E. Botero
#           Jun 2017, M. Clarke
#           Aug 2019, M. Clarke
#           Dec 2021, M. Clarke
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from Legacy.trunk.S.Core import Data
from Legacy.trunk.S.Core import DataOrdered 

# ------------------------------------------------------------
#  AVL Case
# ------------------------------------------------------------

## @ingroup Methods-Aerodynamics-AVL-Data
class Run_Case(Data):
    """ This data class defines the parameters for the analysis cases 
    including angle of attack and mach number 

    Assumptions:
        None
        
    Source:
        None

    Inputs:
        None

    Outputs:
        None

    Properties Used:
        N/A
    """    
    
    def func___defaults__(self):
        """Defines the data structure and defaults of aerodynamics coefficients, 
        body axis derivatives and stability axis derivatives   

        Assumptions:
            None
    
        Source:
            None
    
        Inputs:
            None
    
        Outputs:
            None
    
        Properties Used:
            N/A
        """ 

        self.index                      = 0		 
        self.tag                        = 'case'
        self.mass                       = 0.0

        self.conditions                 = Data()
        self.stability_and_control      = Data()
        free                            = Data()
        aero                            = Data()

        free.mach                       = 0.0
        free.velocity                   = 0.0
        free.density                    = 1.225
        free.gravitational_acceleration = 9.81

        aero.parasite_drag              = 0.0
        aero.angle_of_attack            = None
        aero.lift_coefficient           = None
        aero.side_slip_angle            = 0.0

        self.stability_and_control.control_surface_names     = None
        self.stability_and_control.control_surface_functions = None
        self.stability_and_control.number_control_surfaces   = 0
        self.conditions.freestream      = free
        self.conditions.aerodynamics    = aero

        self.aero_result_filename_1     = None
        self.aero_result_filename_2     = None
        self.aero_result_filename_3     = None 
        self.aero_result_filename_4     = None
        self.eigen_result_filename_1    = None 
        self.eigen_result_filename_2    = None 
        return
 
class Container(DataOrdered):
    """ This is a data class for the addition of a cases to the set of run cases

    Assumptions:
        None
        
    Source:
        None

    Inputs:
        None

    Outputs:
        None

    Properties Used:
        N/A
    """    
    def func_append_case(self,case):
        """ Adds a case to the set of run cases "
        
	Assumptions:
	    None
    
	Source:
	    None
    
	Inputs:
	    None
    
	Outputs:
	    None
    
	Properties Used:
	    N/A
	"""         
        case.index = len(self)+1
        self.append(case)

        return
    
    
# ------------------------------------------------------------
#  Handle Linking
# ------------------------------------------------------------
Run_Case.Container = Container



def __defaults__(State, Settings, System):
	#TODO: self = [Replace With State, Settings, or System Attribute]

	results = func___defaults__('self',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


def append_case(State, Settings, System):
	#TODO: self = [Replace With State, Settings, or System Attribute]
	#TODO: case = [Replace With State, Settings, or System Attribute]

	results = func_append_case('self', 'case')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System