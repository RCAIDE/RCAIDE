## @ingroup Methods
def func_skip(*args,**kwarg):
    """This method can be used to replace default functions when
    no action is desired instead.

    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    None

    Outputs:
    None

    Properties Used:
    N/A
    """          
    pass



def skip(State, Settings, System):

	results = func_skip()
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System