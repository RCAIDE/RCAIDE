## @ingroup Methods-Aerodynamics-AVL-Data
# Aircraft.py
# 
# Created:  Oct 2014, T. Momose
# Modified: Jan 2016, E. Botero
#           Jul 2017, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from Legacy.trunk.S.Core import Data

from .Wing import Wing
from .Body import Body

# ------------------------------------------------------------
#   Aircraft
# ------------------------------------------------------------

## @ingroup Methods-Aerodynamics-AVL-Data
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
	
	def func___defaults__(self):
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
	
	def func_append_wing(self,wing):
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


	def func_append_body(self,body):
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




__defaults__(State, Settings, System):
	#TODO: self = [Replace With State, Settings, or System Attribute]

	results = func___defaults__('self',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


append_wing(State, Settings, System):
	#TODO: self = [Replace With State, Settings, or System Attribute]
	#TODO: wing = [Replace With State, Settings, or System Attribute]

	results = func_append_wing('self', 'wing')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


append_body(State, Settings, System):
	#TODO: self = [Replace With State, Settings, or System Attribute]
	#TODO: body = [Replace With State, Settings, or System Attribute]

	results = func_append_body('self', 'body')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System