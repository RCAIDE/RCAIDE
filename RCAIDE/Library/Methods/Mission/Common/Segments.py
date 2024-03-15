## @ingroup Library-Methods-Mission-Common  
# RCAIDE/Library/Methods/Missions/Common/helper_functions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports 
import RCAIDE 
from RCAIDE.Framework.Core  import Data

def pre_process(mission): 
    for tag,segment in mission.segments.items():     
        segment.pre_process()

def sequential_segments(mission):  
    
    last_tag = None
    for tag,segment in mission.segments.items(): 
        if last_tag:
            segment.state.initials = mission.segments[last_tag].state
        last_tag = tag        
        
        segment.process.initialize.expand_state(segment) 
        segment.process.initialize.expand_state = RCAIDE.Library.Methods.skip        
        segment.evaluate()
        
def update_segments(mission):   
    for tag,segment in mission.segments.items():
        segment.post_process() 
        
def merge_segment_states(mission): 
    mission.state.update(mission.merged())
    
def unpack_segments(mission): 
    # Build a dict with the sections, sections start at 0
    counter = Data()
    
    for key in mission.state.unknowns.keys():
        counter[key] = 0

    for i, segment in enumerate(mission.segments):
        for key in segment.state.unknowns.keys():
            if key=='tag':
                continue
            points = segment.state.unknowns[key].size
            segment.state.unknowns[key] = mission.state.unknowns[key][counter[key]:counter[key]+points]
            counter[key] = counter[key]+points
            
    return
            
            


def _pre_process(State, Settings, System):
	'''
	Framework version of pre_process.
	Wraps pre_process with State, Settings, System pack/unpack.
	Please see pre_process documentation for more details.
	'''

	#TODO: mission = [Replace With State, Settings, or System Attribute]

	results = pre_process('mission',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


def _sequential_segments(State, Settings, System):
	'''
	Framework version of sequential_segments.
	Wraps sequential_segments with State, Settings, System pack/unpack.
	Please see sequential_segments documentation for more details.
	'''

	#TODO: mission = [Replace With State, Settings, or System Attribute]

	results = sequential_segments('mission',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


def _update_segments(State, Settings, System):
	'''
	Framework version of update_segments.
	Wraps update_segments with State, Settings, System pack/unpack.
	Please see update_segments documentation for more details.
	'''

	#TODO: mission = [Replace With State, Settings, or System Attribute]

	results = update_segments('mission',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


def _merge_segment_states(State, Settings, System):
	'''
	Framework version of merge_segment_states.
	Wraps merge_segment_states with State, Settings, System pack/unpack.
	Please see merge_segment_states documentation for more details.
	'''

	#TODO: mission = [Replace With State, Settings, or System Attribute]

	results = merge_segment_states('mission',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


def _unpack_segments(State, Settings, System):
	'''
	Framework version of unpack_segments.
	Wraps unpack_segments with State, Settings, System pack/unpack.
	Please see unpack_segments documentation for more details.
	'''

	#TODO: mission = [Replace With State, Settings, or System Attribute]

	results = unpack_segments('mission',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System