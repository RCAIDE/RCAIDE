# export_rcaide_data.py
#
# Created:  Mar 2026, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import numpy as np
import types
import json
import re
import pickle
import os
import shutil
from collections import OrderedDict

GUI_DEFAULT_UNIT_INDEX = 0

# ----------------------------------------------------------------------------------------------------------------------
#  export_rcaide_data
# ----------------------------------------------------------------------------------------------------------------------
def export_rcaide_data(vehicle=None, configurations=None,  analyses=None, missions=None,
                       filename='RCAIDE_data', pickle_format=False):
    """
    Converts a RCAIDE data structure to a JSON file readable by the RCAIDE GUI
    and by import_rcaide_data.

    The output JSON format matches the structure expected by the RCAIDE GUI's
    values.py read_from_json function. Every RCAIDE Data container in the output
    carries a '__type__' field that records its fully-qualified Python class path,
    e.g.::

        "fan": {
            "__type__": "RCAIDE.Library.Components.Powertrain.Converters.Fan.Fan",
            ...
        }
        "networks": {
            "fuel_network": {
                "__type__": "RCAIDE.Framework.Networks.Fuel.Fuel",
                "fuel_lines": {
                    "fuel_line_1": {
                        "__type__": "RCAIDE.Library.Components.Powertrain.Distributors.Fuel_Line.Fuel_Line",
                        ...
                    }
                }
            }
        }

    This metadata allows import_rcaide_data (and the GUI's read_from_json) to
    reconstruct exact RCAIDE classes—including nested sub-components such as
    Fan, Compressor, Turbine, Combustor, Fuel_Line, etc.—rather than falling
    back to generic DataOrdered containers.

    Scalar and array leaf values are stored as [value, unit_index] pairs where
    unit_index 0 means SI units.  Strings are stored plain.

    Airfoil coordinate files referenced by coordinate_file fields are copied
    into the same directory as the JSON so the GUI can locate them on any machine.

    Parameters
    ----------
    vehicle : RCAIDE.Vehicle, optional
        Vehicle object to export.
    configurations : optional
        Vehicle configurations (stored as empty list; GUI manages configs separately).
    missions : optional
        Mission objects (stored as empty list; GUI manages missions separately).
    analyses : optional
        Analysis objects (stored as empty list; GUI manages analyses separately).
    filename : str
        Output file path without extension.
    pickle_format : bool, optional
        If True, saves as a pickle file instead of JSON. Default is False.

    Returns
    -------
    None

    See Also
    --------
    RCAIDE.import_rcaide_data
        Complementary function that reads the JSON and reconstructs the vehicle.
    """

    # STEP 1: Check Input
    if vehicle is None and configurations is None and missions is None and analyses is None:
        raise AssertionError('No data to be saved!')

    # STEP 2: Save data
    if pickle_format:
        RCAIDE_DATA = {}
        if vehicle       is not None: RCAIDE_DATA['rcaide_vehicle']        = vehicle
        if configurations is not None: RCAIDE_DATA['rcaide_configurations'] = configurations
        if analyses      is not None: RCAIDE_DATA['rcaide_analyses']       = analyses
        if missions      is not None: RCAIDE_DATA['rcaide_missions']       = missions
        with open(filename + '.pkl', 'wb') as file:
            pickle.dump(RCAIDE_DATA, file)
        return

    # STEP 3: Build GUI-compatible JSON
    output_path = os.path.abspath(filename + '.json')
    output_dir  = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    # Serialise vehicle using the GUI [value, unit_index] format
    if vehicle is not None:
        vehicle_dict = build_dict_base(vehicle)
        # Copy any referenced airfoil coordinate files into the output directory
        # and replace paths with just the basename so the GUI can find them.
        _relocate_coordinate_files(vehicle_dict, output_dir)
    else:
        vehicle_dict = {}

    # Generate minimal config_data entries (name only) so the GUI Aircraft Configs
    # tab shows the configuration list on load. CS deflections and propulsor
    # settings default to empty and can be filled in the GUI.
    if configurations is not None:
        gui_config_data = [
            {"config name": name, "cs deflections": {}, "propulsors": {}, "gear down": False}
            for name in configurations
        ]
    else:
        gui_config_data = []

    # Build the top-level structure that read_from_json expects.
    # RCAIDE-native objects are stored under their own keys for import_rcaide_data.
    rcaide_data = {
        "rcaide_vehicle":        vehicle_dict,
        "config_data":           gui_config_data,
        "analysis_data":         [],
        "mission_data":          [],
        "propulsor_names":       _extract_propulsor_names(vehicle),
        "rcaide_configurations": build_dict_r(configurations) if configurations is not None else None,
        "rcaide_analyses":       build_dict_r(analyses)       if analyses       is not None else None,
        "rcaide_missions":       build_dict_r(missions)        if missions       is not None else None,
    }

    with open(output_path, 'w') as f:
        f.write(_dumps_compact(rcaide_data))


# ----------------------------------------------------------------------------------------------------------------------
#  _dumps_compact
# ----------------------------------------------------------------------------------------------------------------------
def _dumps_compact(data, indent=4):
    """
    Like json.dumps(indent=indent) but collapses [scalar, unit_index] pairs onto
    a single line so the file remains human-navigable in editors that support
    JSON folding.  Multi-element arrays (e.g. numpy arrays stored as lists) are
    left in their expanded form.
    """
    raw = json.dumps(data, indent=indent)
    # Match arrays whose only content is a single scalar (number, bool, null)
    # followed by a single non-negative integer — i.e. [value, 0] unit pairs.
    raw = re.sub(
        r'\[\s*\n\s*([^\[\]\{\}\n]+?),\s*\n\s*(\d+)\s*\n\s*\]',
        lambda m: f'[{m.group(1).strip()}, {m.group(2)}]',
        raw,
    )
    return raw


# ----------------------------------------------------------------------------------------------------------------------
#  _extract_propulsor_names
# ----------------------------------------------------------------------------------------------------------------------
def _extract_propulsor_names(vehicle):
    """
    Build the propulsor_names list expected by the GUI from the vehicle's networks.

    Each fuel line and electrical bus stores an assigned_propulsors list whose
    entries are propulsor-tag groups (lists of strings).  This function collects
    all unique groups across every network so the GUI can populate propulsor
    checkboxes in the Mission tab without additional user input.

    Returns
    -------
    list of list of str
        e.g. [['starboard_propulsor', 'port_propulsor']] for a symmetric twin-
        engine aircraft.  Returns [[]] when no assignments are found.
    """
    if vehicle is None:
        return [[]]

    groups = []
    try:
        for network in vehicle.networks:
            for distributor in list(network.fuel_lines) + list(network.busses):
                for group in getattr(distributor, 'assigned_propulsors', []):
                    if isinstance(group, list) and group and group not in groups:
                        groups.append(group)
    except Exception:
        pass

    return groups if groups else [[]]


# ----------------------------------------------------------------------------------------------------------------------
#  _relocate_coordinate_files
# ----------------------------------------------------------------------------------------------------------------------
def _relocate_coordinate_files(obj, output_dir):
    """
    Walk the serialised dict, copy any existing coordinate files into
    output_dir, and replace the stored path with just the basename.
    If the file cannot be found the field is left unchanged so the
    GUI's own repair_airfoil_path logic can attempt a fallback lookup.
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'coordinate_file':
                obj[key] = _copy_airfoil_file(value, output_dir)
            else:
                _relocate_coordinate_files(value, output_dir)
    elif isinstance(obj, list):
        for item in obj:
            _relocate_coordinate_files(item, output_dir)


def _copy_airfoil_file(value, output_dir):
    """
    Given a raw or [path, 0]-wrapped coordinate_file value, copy the
    referenced file to output_dir and return just the basename as a
    plain string (or the original value if the file cannot be found).
    """
    # Unwrap [path, unit_index] if needed
    if isinstance(value, list) and len(value) == 2 and isinstance(value[1], int):
        path = value[0]
        wrapped = True
    else:
        path = value
        wrapped = False

    if not path or not isinstance(path, str):
        return value  # nothing to do (None or non-string)

    basename = os.path.basename(path)

    if os.path.isfile(path):
        dest = os.path.join(output_dir, basename)
        if os.path.abspath(path) != os.path.abspath(dest):
            shutil.copy2(path, dest)
        result = basename
    else:
        # File not found — keep basename only so the GUI can try to resolve it
        result = basename if basename else path

    return [result, GUI_DEFAULT_UNIT_INDEX] if wrapped else result


# ----------------------------------------------------------------------------------------------------------------------
#  build_dict_base / build_dict_r   (GUI [value, unit_index] serialisation)
# ----------------------------------------------------------------------------------------------------------------------
def build_dict_base(base):
    """Serialise a RCAIDE Data object to a plain dict using GUI [value, unit_index] format."""
    keys = base.keys()
    base_dict = {}
    for k in keys:
        if k in ('_component_root_map', '_energy_network_root_map'):
            continue
        base_dict[k] = build_dict_r(base[k])
    return base_dict


def build_dict_r(v):
    """Recursive serialisation step.  Leaf values become [value, 0] pairs."""
    tv = type(v)

    if tv is type:
        return None

    if tv is str:
        # Store tag/label strings as plain strings — the GUI reads them either way.
        return v

    if tv in (np.ndarray, np.float64):
        return [v.tolist(), GUI_DEFAULT_UNIT_INDEX]

    if tv is bool:
        return [v, GUI_DEFAULT_UNIT_INDEX]

    if tv in (float, int):
        return [v, GUI_DEFAULT_UNIT_INDEX]

    if tv is type(None):
        return [None, GUI_DEFAULT_UNIT_INDEX]

    if tv is types.FunctionType:
        return None

    if tv is list:
        return [v, GUI_DEFAULT_UNIT_INDEX]

    # Assume RCAIDE Data container — recurse
    try:
        keys = v.keys()
    except AttributeError:
        if callable(tv):
            return None
        raise TypeError(f'Unexpected type in RCAIDE data structure: {tv}')

    ret = {}
    # Record the fully-qualified class name so the GUI can reconstruct the right type.
    module   = getattr(tv, '__module__', '') or ''
    qualname = getattr(tv, '__qualname__', '') or ''
    if module and qualname and not qualname.startswith('<'):
        ret['__type__'] = f"{module}.{qualname}"

    for k in keys:
        if isinstance(k, type) or k in ('_component_root_map', '_energy_network_root_map'):
            continue
        ret[k] = build_dict_r(v[k])
    return ret
