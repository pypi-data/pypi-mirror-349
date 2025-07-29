# Import constants from the const module
from beamz.const import (
    LIGHT_SPEED, VAC_PERMITTIVITY, VAC_PERMEABILITY, 
    EPS_0, MU_0, um, nm
)

# Define micro-meter constants directly for multiple Unicode variants
globals()['µm'] = 1e-6  # variant 1
globals()['μm'] = 1e-6  # variant 2 (different unicode)

# Import design-related classes and functions
from beamz.design.materials import Material, VarMaterial
from beamz.design.structures import (
    Design, Rectangle, Circle, Ring, 
    CircularBend, Polygon, Taper
)
from beamz.design.sources import ModeSource, GaussianSource
from beamz.design.monitors import Monitor
from beamz.design.signals import ramped_cosine, plot_signal
from beamz.design.mode import solve_modes, slab_mode_source

# Import simulation-related classes and functions
from beamz.simulation.meshing import RegularGrid
from beamz.simulation.fdtd import FDTD
from beamz.simulation.backends import get_backend

# Import optimization-related classes
# (Currently empty, to be filled as the module grows)

# Import UI helpers
from beamz.helpers import (
    display_header, display_status, create_rich_progress,
    display_parameters, display_results,
    display_simulation_status, display_optimization_progress,
    display_time_elapsed, tree_view, code_preview, get_si_scale_and_label, calc_optimal_fdtd_params
)

# Prepare a dictionary of all our exports
_exports = {
    # Constants
    'LIGHT_SPEED': LIGHT_SPEED,
    'VAC_PERMITTIVITY': VAC_PERMITTIVITY,
    'VAC_PERMEABILITY': VAC_PERMEABILITY,
    'EPS_0': EPS_0,
    'MU_0': MU_0,
    'um': um,
    'nm': nm,
    'µm': globals()['µm'],
    'μm': globals()['μm'],
    
    # Materials
    'Material': Material,
    'VarMaterial': VarMaterial,
    
    # Structures
    'Design': Design,
    'Rectangle': Rectangle,
    'Circle': Circle,
    'Ring': Ring,
    'CircularBend': CircularBend, 
    'Polygon': Polygon,
    'Taper': Taper,
    
    # Sources
    'ModeSource': ModeSource,
    'GaussianSource': GaussianSource,
    
    # Monitors
    'Monitor': Monitor,
    
    # Signals
    'ramped_cosine': ramped_cosine,
    'plot_signal': plot_signal,
    
    # Mode calculations
    'solve_modes': solve_modes,
    'slab_mode_source': slab_mode_source,
    
    # Simulation
    'RegularGrid': RegularGrid,
    'FDTD': FDTD,
    'get_backend': get_backend,
    
    # UI helpers
    'display_header': display_header,
    'display_status': display_status,
    'create_rich_progress': create_rich_progress,
    'display_parameters': display_parameters,
    'display_results': display_results,
    'display_simulation_status': display_simulation_status,
    'display_optimization_progress': display_optimization_progress,
    'display_time_elapsed': display_time_elapsed,
    'tree_view': tree_view,
    'code_preview': code_preview,
    'get_si_scale_and_label': get_si_scale_and_label,
    'calc_optimal_fdtd_params': calc_optimal_fdtd_params,
}

# Update module's dictionary with our exports
globals().update(_exports)

# Define what should be available with "from beamz import *"
__all__ = list(_exports.keys())

# Version information
__version__ = "0.1.4"