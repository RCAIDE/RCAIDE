## @ingroup Library-Methods-Aerdoynamics-AVL-Data
# RCAIDE/Library/Methods/Aerdoynamics/AVL/Data/Aircraft.py
# 
# 
# Created:  Jul 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    

from RCAIDE.Framework.Core import Data

from .Wing import Wing
from .Body import Body

# ----------------------------------------------------------------------------------------------------------------------
#  Aircraft
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Library-Methods-Aerodynamics-AVL-Data
class Aircraft(Data):
	"""A data class defining the entire AVL aircraft geometry

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
	
	def __defaults__(self):
		""" Defines the data structure and defaults of aircraft classes

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
		self.tag    = 'aircraft'
		self.wings  = Data()
		self.bodies = Data()
	
	def append_wing(self,wing):
		""" Appends wing geometry onto aircraft class

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
		# assert database type
		if not isinstance(wing,Wing):
			raise Exception('input component must be of type AVL.Data.Wing()')

		# store data
		self.wings.append(wing)
		return


	def append_body(self,body):
		""" Appends body geometry onto aircraft class

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
		# assert database type
		if not isinstance(body,Body):
			raise Exception('input component must be of type AVL.Data.Body()')

		# store data
		self.bodies.append(body)
		return

