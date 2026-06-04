"""
Units.py

A pure-float SI unit conversion module. 
Usage: 
    Multiply by a unit to convert FROM that unit to base SI.
    Divide by a unit to convert TO that unit from base SI.
    
    Example: 
    span_meters = 50 * ft
    span_feet = span_meters / ft
"""
import math

# ==============================================================================
# BASE SI UNITS (The Single Source of Truth)
# ==============================================================================
m   = 1.0  # Length: meter
kg  = 1.0  # Mass: kilogram
s   = 1.0  # Time: second
K   = 1.0  # Temperature: Kelvin
A   = 1.0  # Current: Ampere
rad = 1.0  # Angle: radian

# ==============================================================================
# DERIVED SI UNITS
# ==============================================================================
N  = kg * m / s**2     # Force: Newton
Pa = N / m**2          # Pressure: Pascal
J  = N * m             # Energy: Joule
W  = J / s             # Power: Watt
Hz = 1.0 / s           # Frequency: Hertz
C  = A * s             # Charge: Coulomb
V  = W / A             # Voltage: Volt

# Constants
g0 = 9.80665 * m / s**2  # Standard gravity

# ==============================================================================
# LENGTH
# ==============================================================================
km  = 1000.0 * m
cm  = 0.01 * m
mm  = 0.001 * m
um  = 1e-6 * m
nm  = 1e-9 * m

# Imperial / Aviation Lengths
inch = 0.0254 * m
ft   = 12.0 * inch
yd   = 3.0 * ft
mi   = 5280.0 * ft
nmi  = 1852.0 * m      # Nautical mile

# ==============================================================================
# MASS
# ==============================================================================
gram = 0.001 * kg
mg   = 1e-6 * kg
tonne = 1000.0 * kg

# Imperial Masses (The headache zone)
lbm  = 0.45359237 * kg           # Pound-mass
slug = lbm * g0 / (ft / s**2)    # Slug (14.5939 kg)
oz   = lbm / 16.0                # Ounce

# ==============================================================================
# FORCE & PRESSURE
# ==============================================================================
# The classic lbm vs lbf distinction:
lbf = lbm * g0                   # Pound-force (~4.448 N)

# Imperial Pressures
psi = lbf / inch**2              # Pounds per square inch
psf = lbf / ft**2                # Pounds per square foot
atm = 101325.0 * Pa              # Standard atmosphere
bar = 100000.0 * Pa              # Bar

# ==============================================================================
# VELOCITY & AREA/VOLUME
# ==============================================================================
knots = nmi / (3600.0 * s)
mph   = mi / (3600.0 * s)
kph   = km / (3600.0 * s)

liter = 0.001 * m**3
gal   = 3.78541 * liter          # US Gallon

# ==============================================================================
# ANGLES
# ==============================================================================
deg = math.pi / 180.0 * rad
rev = 2.0 * math.pi * rad

# ==============================================================================
# TEMPERATURE (ABSOLUTE)
# ==============================================================================
# Note: These are for absolute temperature multiplication only
# DO NOT use these to convert offset temperatures (like 70°F to °C).
R = 5.0 / 9.0 * K                # Rankine


# ==============================================================================
# THE MAGIC STRING PARSER
# ==============================================================================
def parse(unit_string: str) -> float:
    """
    Evaluates a string of units and returns the float multiplier.
    
    Example:
        Units.parse("kg * m**2 / s**3")
        Units.parse("lbf / inch**2")
    """
    # Grab the dictionary of everything defined in this module
    module_dict = globals()
    
    # Evaluate the string securely, using only this module's variables.
    # We disable Python's built-ins (like __import__) for security.
    try:
        return eval(unit_string, {"__builtins__": None}, module_dict)
    except Exception as e:
        raise ValueError(f"Failed to parse unit string '{unit_string}'. Error: {e}")