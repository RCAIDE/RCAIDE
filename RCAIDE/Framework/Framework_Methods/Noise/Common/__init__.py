## @defgroup Framework-Methods-Noise " + f"Common
# RCAIDE/Library/Methods/Noise/Common/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Noise

from .atmospheric_attenuation import _atmospheric_attenuation as atmospheric_attenuation
from .background_noise import _background_noise as background_noise
from .noise_tone_correction import _noise_tone_correction as noise_tone_correction
from .decibel_arithmetic import _pressure_ratio_to_SPL_arithmetic as pressure_ratio_to_SPL_arithmetic
from .decibel_arithmetic import _SPL_arithmetic as SPL_arithmetic
from .convert_to_third_octave_band import _convert_to_third_octave_band as convert_to_third_octave_band
from .compute_noise_source_coordinates import _compute_rotor_point_source_coordinates as compute_rotor_point_source_coordinates
from .generate_microphone_locations import _generate_zero_elevation_microphone_locations as generate_zero_elevation_microphone_locations
from .generate_microphone_locations import _generate_terrain_elevated_microphone_locations as generate_terrain_elevated_microphone_locations
from .generate_microphone_locations import _generate_noise_hemisphere_microphone_locations as generate_noise_hemisphere_microphone_locations
from .compute_relative_noise_evaluation_locations import _compute_relative_noise_evaluation_locations as compute_relative_noise_evaluation_locations
