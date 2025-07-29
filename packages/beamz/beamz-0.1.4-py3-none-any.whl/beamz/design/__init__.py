"""
Design module for BEAMZ - Contains components for designing photonic structures.
"""

from beamz.design.materials import Material, VarMaterial
from beamz.design.structures import (
    Design, Rectangle, Circle, Ring,
    CircularBend, Polygon, Taper
)
from beamz.design.sources import ModeSource, GaussianSource
from beamz.design.monitors import Monitor
from beamz.design.signals import ramped_cosine, plot_signal
from beamz.design.mode import solve_modes, slab_mode_source

__all__ = [
    'Material', 'VarMaterial',
    'Design', 'Rectangle', 'Circle', 'Ring',
    'CircularBend', 'Polygon', 'Taper',
    'ModeSource', 'GaussianSource',
    'Monitor',
    'ramped_cosine', 'plot_signal',
    'solve_modes', 'slab_mode_source'
]
