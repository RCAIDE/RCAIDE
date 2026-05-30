# import_rcaide_data.py
#
# Created:  May 2026, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import json
import importlib
import numpy as np
import RCAIDE
from RCAIDE.Framework.Core import Data, DataOrdered

# Keys skipped during reconstruction (internal metadata / bookkeeping)
_SKIP_KEYS = frozenset({'__type__'})

# Vehicle-level component containers that must go through append_component()
_VEHICLE_COMPONENT_CONTAINERS = frozenset({
    'fuselages', 'wings', 'booms', 'landing_gears', 'cargo_bays', 'nacelles'
})


# ----------------------------------------------------------------------------------------------------------------------
#  import_rcaide_data
# ----------------------------------------------------------------------------------------------------------------------
def import_rcaide_data(filename):
    """
    Reads a JSON file produced by export_rcaide_data and reconstructs RCAIDE
    native data structures corresponding to what was exported.

    The JSON must contain __type__ metadata fields (written by export_rcaide_data)
    that identify the fully-qualified Python class for each data object.  Those
    class paths are used to instantiate the correct RCAIDE types, including nested
    sub-components such as:

        RCAIDE.Framework.Networks.Fuel
        RCAIDE.Library.Components.Powertrain.Distributors.Fuel_Line
        RCAIDE.Library.Components.Powertrain.Propulsors.Turbofan
        RCAIDE.Library.Components.Powertrain.Converters.Fan
        RCAIDE.Library.Components.Powertrain.Converters.Combustor
        ... and all other RCAIDE component classes.

    Vehicle-level components are registered via vehicle.append_component() so
    that the internal _component_root_map is kept consistent.  Energy networks
    are registered via vehicle.append_energy_network().

    Parameters
    ----------
    filename : str
        Path to the JSON file produced by export_rcaide_data.  The .json
        extension is added automatically if omitted.

    Returns
    -------
    result : RCAIDE.Framework.Core.Data
        A Data container with the following attributes mirroring the export:

        result.vehicle         — RCAIDE.Vehicle with all sub-components typed
        result.propulsor_names — list of propulsor-tag groups (list of lists)
                                 used to populate GUI mission checkboxes
        result.configurations  — reconstructed from 'rcaide_configurations' key, or None
        result.analyses        — reconstructed from 'rcaide_analyses' key, or None
        result.missions        — reconstructed from 'rcaide_missions' key, or None

    See Also
    --------
    RCAIDE.export_rcaide_data
        Complementary export function that writes the JSON consumed here.
    """
    if not filename.endswith('.json'):
        filename += '.json'

    with open(filename, 'r') as f:
        file_data = json.load(f)

    result                  = Data()
    result.vehicle          = _reconstruct_vehicle(file_data.get('rcaide_vehicle', {}))
    result.propulsor_names  = file_data.get('propulsor_names', [[]])
    result.configurations   = _reconstruct_obj(file_data['rcaide_configurations']) if isinstance(file_data.get('rcaide_configurations'), dict) else None
    result.analyses         = _reconstruct_obj(file_data['rcaide_analyses'])       if isinstance(file_data.get('rcaide_analyses'),       dict) else None
    result.missions         = _reconstruct_obj(file_data['rcaide_missions'])       if isinstance(file_data.get('rcaide_missions'),       dict) else None
    return result


# ----------------------------------------------------------------------------------------------------------------------
#  Internal helpers
# ----------------------------------------------------------------------------------------------------------------------

def _class_for_type_string(type_str):
    """
    Return the Python class identified by a dotted type string.

    Handles nested classes (e.g. 'RCAIDE.Library.Components.Wings.Wing.Segments.Container')
    by trying progressively shorter module paths until the import succeeds and
    the remaining parts resolve as class attributes.
    """
    if not type_str or not isinstance(type_str, str):
        return None
    parts = type_str.split('.')
    # Try longest module prefix first (most specific), working backwards
    for i in range(len(parts) - 1, 0, -1):
        module_path = '.'.join(parts[:i])
        attr_chain  = parts[i:]
        try:
            mod = importlib.import_module(module_path)
            obj = mod
            for attr in attr_chain:
                obj = getattr(obj, attr)
            if isinstance(obj, type):
                return obj
        except Exception:
            continue
    return None


def _is_unit_pair(v):
    """Return True if *v* is a GUI [value, unit_index] export pair."""
    return isinstance(v, list) and len(v) == 2 and isinstance(v[1], int)


def _list_to_array(lst):
    """Convert a list to a numpy array when all elements are numeric."""
    if not lst:
        return lst
    try:
        arr = np.array(lst)
        if arr.dtype.kind in ('f', 'i', 'u'):
            return arr
    except Exception:
        pass
    return lst


def _convert_value(v):
    """
    Convert a single JSON value to its Python/numpy equivalent.

    Rules
    -----
    - dict                    → reconstruct as typed RCAIDE object
    - [value, int] unit pair  → unwrap; convert numeric lists to numpy arrays
    - anything else           → return as-is (plain string, int, float, None …)
    """
    if isinstance(v, dict):
        return _reconstruct_obj(v)

    if _is_unit_pair(v):
        inner = v[0]
        if isinstance(inner, list):
            return _list_to_array(inner)
        return inner  # scalar: float, int, bool, or None

    return v  # plain string or primitive scalar


# ----------------------------------------------------------------------------------------------------------------------
#  Generic object reconstruction
# ----------------------------------------------------------------------------------------------------------------------

def _reconstruct_obj(d):
    """
    Reconstruct a RCAIDE Data object from a serialised dict.

    If *d* contains a '__type__' field the corresponding class is instantiated;
    otherwise a DataOrdered is used as a fallback.  All sub-keys are converted
    recursively via _convert_value so that nested components, scalars, and
    numpy arrays are handled automatically.
    """
    if not isinstance(d, dict):
        return d

    type_str = d.get('__type__')
    # Unwrap [value, unit_index] if __type__ was stored in GUI [str, 0] format
    if _is_unit_pair(type_str):
        type_str = type_str[0]
    cls = _class_for_type_string(type_str) if isinstance(type_str, str) and type_str else None

    try:
        obj = cls() if cls is not None else DataOrdered()
    except Exception:
        obj = DataOrdered()

    for k, v in d.items():
        if k in _SKIP_KEYS:
            continue
        obj[k] = _convert_value(v)

    return obj


# ----------------------------------------------------------------------------------------------------------------------
#  Specialised sub-structure reconstruction
# ----------------------------------------------------------------------------------------------------------------------

def _reconstruct_fuel_line(fldata):
    """
    Reconstruct a Fuel_Line together with its nested fuel_tanks container.

    fuel_tanks items are appended via fuel_line.fuel_tanks.append() so that
    the container is populated without replacing the default Container instance.
    """
    if not isinstance(fldata, dict):
        return _reconstruct_obj(fldata)

    type_str = fldata.get('__type__')
    if _is_unit_pair(type_str):
        type_str = type_str[0]
    cls = _class_for_type_string(type_str) if isinstance(type_str, str) and type_str else None
    try:
        fuel_line = cls() if cls is not None else \
            RCAIDE.Library.Components.Powertrain.Distributors.Fuel_Line()
    except Exception:
        fuel_line = DataOrdered()

    for k, v in fldata.items():
        if k in _SKIP_KEYS:
            continue
        if k == 'fuel_tanks' and isinstance(v, dict):
            for tk, tv in v.items():
                if tk in _SKIP_KEYS or not isinstance(tv, dict):
                    continue
                tank = _reconstruct_obj(tv)
                try:
                    fuel_line.fuel_tanks.append(tank)
                except Exception:
                    fuel_line.fuel_tanks[tk] = tank
        else:
            fuel_line[k] = _convert_value(v)

    return fuel_line


def _reconstruct_network(ndata):
    """
    Reconstruct an energy network (Fuel, Electric, Hybrid, etc.) with all
    of its sub-containers properly populated.

    Sub-containers handled explicitly
    ----------------------------------
    propulsors    → net.propulsors.append()   (generic _reconstruct_obj)
    fuel_lines    → net.fuel_lines.append()   (_reconstruct_fuel_line)
    busses        → net.busses.append()       (generic _reconstruct_obj)
    coolant_lines → net.coolant_lines.append()
    converters    → net.converters.append()

    All other keys are set directly on the network instance.
    """
    if not isinstance(ndata, dict):
        return _reconstruct_obj(ndata)

    type_str = ndata.get('__type__')
    if _is_unit_pair(type_str):
        type_str = type_str[0]
    cls = _class_for_type_string(type_str) if isinstance(type_str, str) and type_str else None
    try:
        net = cls() if cls is not None else RCAIDE.Framework.Networks.Fuel()
    except Exception:
        net = RCAIDE.Framework.Networks.Fuel()

    _NETWORK_CONTAINERS = {
        'propulsors':    (net.propulsors,    _reconstruct_obj),
        'busses':        (net.busses,        _reconstruct_obj),
        'coolant_lines': (net.coolant_lines, _reconstruct_obj),
        'converters':    (net.converters,    _reconstruct_obj),
        'fuel_lines':    (net.fuel_lines,    _reconstruct_fuel_line),
    }

    for k, v in ndata.items():
        if k in _SKIP_KEYS:
            continue
        if k in _NETWORK_CONTAINERS and isinstance(v, dict):
            container, builder = _NETWORK_CONTAINERS[k]
            for ck, cv in v.items():
                if ck in _SKIP_KEYS or not isinstance(cv, dict):
                    continue
                item = builder(cv)
                try:
                    container.append(item)
                except Exception:
                    container[ck] = item
        else:
            net[k] = _convert_value(v)

    return net


# ----------------------------------------------------------------------------------------------------------------------
#  Vehicle reconstruction (top-level entry point)
# ----------------------------------------------------------------------------------------------------------------------

def _reconstruct_vehicle(vdata):
    """
    Reconstruct a RCAIDE.Vehicle from the top-level serialised dict.

    Component containers (fuselages, wings, booms, landing_gears, cargo_bays,
    nacelles) are populated via vehicle.append_component() so that the internal
    _component_root_map remains consistent.  Energy networks are added via
    vehicle.append_energy_network().  All other scalar / Data attributes are
    set directly on the vehicle.
    """
    if not isinstance(vdata, dict):
        raise ValueError('Vehicle data must be a dict.')

    vehicle = RCAIDE.Vehicle()

    for k, v in vdata.items():
        if k in _SKIP_KEYS:
            continue

        if k in _VEHICLE_COMPONENT_CONTAINERS and isinstance(v, dict):
            for ck, cv in v.items():
                if ck in _SKIP_KEYS or not isinstance(cv, dict):
                    continue
                component = _reconstruct_obj(cv)
                try:
                    vehicle.append_component(component)
                except Exception:
                    # Fallback: set directly if append fails (e.g. unknown type)
                    vehicle[k][ck] = component

        elif k == 'networks' and isinstance(v, dict):
            for nk, nv in v.items():
                if nk in _SKIP_KEYS or not isinstance(nv, dict):
                    continue
                network = _reconstruct_network(nv)
                try:
                    vehicle.append_energy_network(network)
                except Exception:
                    vehicle.networks[nk] = network

        else:
            vehicle[k] = _convert_value(v)

    return vehicle
