from typing import Dict, Optional
import numpy as np
from beamz.const import *
from beamz.simulation.meshing import RegularGrid
from beamz.design.sources import ModeSource, GaussianSource
from beamz.design.structures import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as MatplotlibRectangle, Circle as MatplotlibCircle, PathPatch
from matplotlib.path import Path
from matplotlib.animation import FuncAnimation
from beamz.simulation.backends import get_backend
from beamz.helpers import (
    display_header, display_status, create_rich_progress, 
    display_parameters, display_results, display_simulation_status, 
    display_time_elapsed
)
import datetime
from beamz.helpers import get_si_scale_and_label

class FDTD:
    """FDTD simulation class."""
    def __init__(self, design, time, mesh: str = "regular", resolution: float = 0.02*µm, backend="numpy", backend_options=None):
        # Initialize the design and mesh
        self.design = design
        self.resolution = resolution
        self.mesh = RegularGrid(design=self.design, resolution=self.resolution) if mesh == "regular" else None
        self.dx = self.mesh.dx
        self.dy = self.mesh.dy
        self.epsilon_r = self.mesh.permittivity
        self.mu_r = self.mesh.permeability
        self.sigma = self.mesh.conductivity
        # Initialize the backend
        backend_options = backend_options or {}
        self.backend = get_backend(name=backend, **backend_options)
        # Initialize the fields with the backend
        self.nx, self.ny = self.mesh.shape
        
        # Create complex fields in a backend-compatible way
        try:
            # Try with dtype parameter if supported
            self.Ez = self.backend.zeros((self.nx, self.ny), dtype=np.complex128)
        except TypeError:
            # Fallback if dtype not supported - create real array and handle complex values in code
            self.Ez = self.backend.zeros((self.nx, self.ny))
            self.is_complex_backend = False
        else:
            self.is_complex_backend = True
            
        self.Hx = self.backend.zeros((self.nx, self.ny-1))
        self.Hy = self.backend.zeros((self.nx-1, self.ny))
        
        # Convert material properties to backend arrays
        self.epsilon_r = self.backend.from_numpy(self.epsilon_r)
        self.mu_r = self.backend.from_numpy(self.mu_r)
        self.sigma = self.backend.from_numpy(self.sigma)
        # Initialize the time
        self.time = time
        self.dt = self.time[1] - self.time[0]
        self.num_steps = len(self.time)
        # Initialize the sources
        self.sources = self.design.sources
        # Initialize the results
        self.results = {"Ez": [], "Hx": [], "Hy": [], "t": []}
        # Initialize animation attributes
        self.fig = None
        self.ax = None
        self.anim = None
        self.im = None
        # Initialize monitor data storage
        self.monitor_data = {}
        # Initialize power accumulation
        self.power_accumulated = None
        self.power_accumulation_count = 0
        # Initialize simulation start time
        self.start_time = None

    def simulate_step(self):
        """Perform one FDTD step with stability checks."""
        self.Hx, self.Hy = self.backend.update_h_fields(
            self.Hx, self.Hy, self.Ez, self.sigma, 
            self.dx, self.dy, self.dt, MU_0, EPS_0)
        self.Ez = self.backend.update_e_field(
            self.Ez, self.Hx, self.Hy, self.sigma, self.epsilon_r,
            self.dx, self.dy, self.dt, EPS_0)

    def plot_field(self, field: str = "Ez", t: float = None) -> None:
        """Plot a field at a given time with proper scaling and units."""
        if len(self.results['t']) == 0:
            current_field = getattr(self, field)
            current_t = self.t
        else:
            t_idx = np.argmin(np.abs(np.array(self.results['t']) - t))
            current_field = self.results[field][t_idx]
            current_t = self.results['t'][t_idx]
            
        # Convert to NumPy array if it's a backend array
        if hasattr(current_field, 'device'):
            current_field = self.backend.to_numpy(current_field)
            
        # Handle complex data - we'll display the real part for visualization
        if np.iscomplexobj(current_field):
            current_field = np.real(current_field)
            field_label = f'Re({field})'
        else:
            field_label = field
            
        # Determine appropriate SI unit and scale for spatial dimensions
        scale, unit = get_si_scale_and_label(max(self.design.width, self.design.height))
        # Calculate figure size based on grid dimensions
        grid_height, grid_width = current_field.shape
        aspect_ratio = grid_width / grid_height
        base_size = 6  # Base size for the smaller dimension
        if aspect_ratio > 1: figsize = (base_size * aspect_ratio, base_size)
        else: figsize = (base_size, base_size / aspect_ratio)
        # Create the figure with the added structure outlines
        plt.figure(figsize=figsize)
        plt.imshow(current_field, origin='lower', 
                  extent=(0, self.design.width, 0, self.design.height),
                  cmap='RdBu', aspect='equal', interpolation='bicubic')
        plt.colorbar(label=f'{field_label} Field Amplitude')
        plt.title(f'{field_label} Field at t = {current_t:.2e} s')
        plt.xlabel(f'X ({unit})'); plt.ylabel(f'Y ({unit})')
        plt.gca().xaxis.set_major_formatter(lambda x, pos: f'{x*scale:.1f}')
        plt.gca().yaxis.set_major_formatter(lambda x, pos: f'{x*scale:.1f}')
        for structure in self.design.structures:
            # Use dashed lines for PML regions
            if hasattr(structure, 'is_pml') and structure.is_pml:
                structure.add_to_plot(plt.gca(), edgecolor="black", linestyle='--', facecolor='none', alpha=0.5)
            else:
                structure.add_to_plot(plt.gca(), facecolor="none", edgecolor="black", linestyle="-")
        plt.tight_layout()
        plt.show()

    def animate_live(self, field_data=None, field="Ez", axis_scale=[-1,1]):
        """Animate the field in real time using matplotlib animation."""
        if field_data is None: field_data = self.backend.to_numpy(getattr(self, field))
        
        # Handle complex data - we'll display the real part for visualization
        if np.iscomplexobj(field_data):
            field_data = np.real(field_data)
            
        # If animation already exists, just update the data
        if self.fig is not None and plt.fignum_exists(self.fig.number):
            current_field = field_data
            self.im.set_array(current_field)
            self.ax.set_title(f't = {self.t:.2e} s')
            self.fig.canvas.draw_idle()
            self.fig.canvas.flush_events()
            return

        # Get current field data
        current_field = field_data
        # Calculate figure size based on grid dimensions
        grid_height, grid_width = current_field.shape
        aspect_ratio = grid_width / grid_height
        base_size = 5  # Base size for the smaller dimension
        if aspect_ratio > 1: figsize = (base_size * aspect_ratio * 1.2, base_size)
        else: figsize = (base_size * 1.2, base_size / aspect_ratio)
        # Create the figure and axis
        self.fig, self.ax = plt.subplots(figsize=figsize)
        # Create initial plot with proper scaling
        self.im = self.ax.imshow(current_field, origin='lower',
                                extent=(0, self.design.width, 0, self.design.height),
                                cmap='RdBu', aspect='equal', interpolation='bicubic', vmin=axis_scale[0], vmax=axis_scale[1])
        # Add colorbar
        colorbar = plt.colorbar(self.im, orientation='vertical', aspect=30, extend='both')
        colorbar.set_label(f'{field} Field Amplitude')
        # Add design structure outlines
        for structure in self.design.structures:
            # Use dashed lines for PML regions
            if hasattr(structure, 'is_pml') and structure.is_pml:
                structure.add_to_plot(self.ax, edgecolor="black", linestyle='--', facecolor='none', alpha=0.5)
            else:
                structure.add_to_plot(self.ax, facecolor="none")
        # Set axis labels with proper scaling
        max_dim = max(self.design.width, self.design.height)
        if max_dim >= 1e-3: scale, unit = 1e3, 'mm'
        elif max_dim >= 1e-6: scale, unit = 1e6, 'µm'
        elif max_dim >= 1e-9: scale, unit = 1e9, 'nm'
        else: scale, unit = 1e12, 'pm'
        # Add axis labels with proper scaling
        plt.xlabel(f'X ({unit})')
        plt.ylabel(f'Y ({unit})')
        self.ax.xaxis.set_major_formatter(lambda x, pos: f'{x*scale:.1f}')
        self.ax.yaxis.set_major_formatter(lambda x, pos: f'{x*scale:.1f}')
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(0.001)  # Small pause to ensure window is shown

    def run(self, steps: Optional[int] = None, save=True, live=True, axis_scale=[-1,1], save_animation=False, 
            animation_filename='fdtd_animation.mp4', clean_visualization=True, 
            save_fields=['Ez', 'Hx', 'Hy'], decimate_save=1, accumulate_power=False,
            save_memory_mode=False) -> Dict:
        """Run the simulation.
        
        Args:
            steps: Number of steps to run. If None, run until the end of the time array.
            save: Whether to save field data at each step.
            live: Whether to show live animation of the simulation.
            axis_scale: Color scale limits for the field visualization.
            save_animation: Whether to save an animation of the simulation as an mp4 file.
            animation_filename: Filename for the saved animation (must end in .mp4).
            save_fields: List of fields to save (['Ez'], ['Ez', 'Hx', 'Hy'], etc.)
            decimate_save: Save only every nth time step (1 = save all, 10 = save every 10th step)
            accumulate_power: Instead of saving all fields, accumulate power and save that
            save_memory_mode: If True, avoid storing all field data and only keep monitors/power
        
        Returns:
            Dictionary containing the simulation results.
        """
        # Record start time
        self.start_time = datetime.datetime.now()
        # Initialize simulation state
        self.t = 0
        self._total_steps = self.num_steps
        self._save_results = save
        # Save mode flags as class attributes for monitor access
        self.save_memory_mode = save_memory_mode
        self.accumulate_power = accumulate_power
        
        # Display simulation header and parameters
        sim_params = {
            "Domain size": f"{self.design.width:.2e} x {self.design.height:.2e} m",
            "Resolution": f"{self.resolution:.2e} m",
            "Time steps": self.num_steps,
            "Time delta": f"{self.dt:.2e} s",
            "Total time": f"{self.time[-1]:.2e} s",
            "Backend": self.backend.__class__.__name__,
            "Save fields": ", ".join(save_fields),
            "Memory-saving mode": "Enabled" if save_memory_mode else "Disabled",
            "Accumulate power": "Enabled" if accumulate_power else "Disabled",
            "Live animation": "Enabled" if live else "Disabled",
            "Save animation": "Enabled" if save_animation else "Disabled"
        }
        display_parameters(sim_params, "Simulation Parameters")
        
        # Check stability using the helper function
        from beamz.helpers import check_fdtd_stability
        n_max = np.sqrt(np.max(self.epsilon_r))
        is_stable, courant, safe_limit = check_fdtd_stability(dt=self.dt, dx=self.dx, dy=self.dy, n_max=n_max)
        if not is_stable:
            display_status(f"Simulation may be unstable! Courant number = {courant:.3f} > {safe_limit:.3f}", "warning")
            display_status("Consider reducing dt or increasing dx/dy", "warning")
        else: display_status(f"Stability check passed (Courant number = {courant:.3f} / {safe_limit:.3f})", "success")
        
        # Set up power accumulation if requested
        if accumulate_power:
            self.power_accumulated = np.zeros((self.nx, self.ny))
            self.power_accumulation_count = 0
            
        # Determine optimal save frequency based on backend type
        is_gpu_backend = hasattr(self.backend, 'device') and self.backend.device.type in ['cuda', 'mps']
        # For GPU backends, avoid excessive CPU-GPU transfers by batching the result saves
        if is_gpu_backend and save:
            save_freq = max(10, self.num_steps // 100)  # Save approximately every 1% of steps or min of 10 steps
            display_status(f"GPU backend detected: Optimizing result storage (saving every {save_freq} steps)", "info")
        else: save_freq = 1  # Save every step for CPU backends
            
        # Apply additional decimation based on user setting
        effective_save_freq = save_freq * decimate_save
        
        # If in save_memory_mode, clear any existing results to start fresh
        if save_memory_mode: 
            for field in self.results: 
                if field != 't': self.results[field] = []
            display_status("Memory-saving mode active: Only storing monitor data and/or power accumulation", "info")
        
        # Use a single progress bar for the entire simulation
        with create_rich_progress() as progress:
            # Create a task that will be updated throughout the simulation
            task = progress.add_task("Running simulation...", total=self.num_steps)            
            for step in range(self.num_steps):
                # Update fields
                self.simulate_step()
                # Apply sources
                for source in self.sources:
                    if isinstance(source, ModeSource):
                        # Get the mode profile for the first mode
                        mode_profile = source.mode_profiles[0]
                        # Get the time modulation for this step
                        modulation = source.signal[step]
                        # Apply the mode profile to all points
                        for point in mode_profile:
                            amplitude, x_raw, y_raw = point
                            # Convert the position to the nearest grid point using correct resolutions
                            x = int(round(x_raw / self.dx))
                            y = int(round(y_raw / self.dy))
                            # Skip points outside the grid
                            if x < 0 or x >= self.nx or y < 0 or y >= self.ny: continue
                            
                            # Add the source contribution to the field (handling complex values)
                            # This handles both complex-enabled and real-only backends
                            if hasattr(self, 'is_complex_backend') and not self.is_complex_backend:
                                # For backends that don't support complex numbers, we need to extract real part
                                if isinstance(amplitude * modulation, complex):
                                    # Only use real part for backends that don't support complex
                                    self.Ez[y, x] += np.real(amplitude * modulation)
                                else:
                                    self.Ez[y, x] += amplitude * modulation
                            else:
                                # Backend supports complex values or we're using default handling
                                self.Ez[y, x] += amplitude * modulation
                                
                            # Apply direction to the source
                            if source.direction == "+x": self.Ez[y, x-1] = 0
                            elif source.direction == "-x": self.Ez[y, x+1] = 0
                            elif source.direction == "+y": self.Ez[y-1, x] = 0
                            elif source.direction == "-y": self.Ez[y+1, x] = 0
                    elif isinstance(source, GaussianSource):
                        modulation = source.signal[step]
                        center_x_phys, center_y_phys = source.position
                        width_phys = source.width  # Assuming width is standard deviation (sigma)
                        # Convert physical units to grid coordinates
                        center_x_grid = center_x_phys / self.dx
                        center_y_grid = center_y_phys / self.dy
                        # sigma in grid units
                        width_x_grid = width_phys / self.dx 
                        width_y_grid = width_phys / self.dy 
                        # Define the grid range to apply the source (e.g., +/- 3 sigma)
                        # Use max(1, ...) to ensure at least one grid cell width if sigma_grid is very small
                        wx_grid_cells = max(1, int(round(3 * width_x_grid)))
                        wy_grid_cells = max(1, int(round(3 * width_y_grid)))
                        # Calculate bounding box indices, clamped to grid boundaries
                        x_center_idx = int(round(center_x_grid))
                        y_center_idx = int(round(center_y_grid))
                        x_start = max(0, x_center_idx - wx_grid_cells)
                        x_end = min(self.nx, x_center_idx + wx_grid_cells + 1)
                        y_start = max(0, y_center_idx - wy_grid_cells)
                        y_end = min(self.ny, y_center_idx + wy_grid_cells + 1)
                        # Create meshgrid for the affected area
                        y_indices = np.arange(y_start, y_end)
                        x_indices = np.arange(x_start, x_end)
                        y_grid, x_grid = np.meshgrid(y_indices, x_indices, indexing='ij')
                        # Calculate squared distances from the center in grid units
                        dist_x_sq = (x_grid - center_x_grid)**2
                        dist_y_sq = (y_grid - center_y_grid)**2
                        # Calculate Gaussian amplitude (handle zero width appropriately)
                        # Use small epsilon to avoid division by zero if width_grid is exactly 0
                        epsilon = 1e-9
                        sigma_x_sq = width_x_grid**2 + epsilon
                        sigma_y_sq = width_y_grid**2 + epsilon
                        exponent = -(dist_x_sq / (2 * sigma_x_sq) + dist_y_sq / (2 * sigma_y_sq))
                        gaussian_amp = np.exp(exponent) / 4 # TODO: This is normalized to 2D. In 3D, it should be / 8!!! (Right?)
                        
                        gaussian_amp = self.backend.from_numpy(gaussian_amp)
                        # Add the source contribution to the Ez field slice
                        self.Ez[y_start:y_end, x_start:x_end] += gaussian_amp * modulation
                
                # Record monitor data
                self._record_monitor_data(step)
                
                # Accumulate power if requested
                if accumulate_power:
                    # Calculate instantaneous power
                    Ez_np = self.backend.to_numpy(self.Ez)
                    Hx_np = self.backend.to_numpy(self.Hx)
                    Hy_np = self.backend.to_numpy(self.Hy)
                    
                    # Check if any field is complex
                    is_complex = np.iscomplexobj(Ez_np) or np.iscomplexobj(Hx_np) or np.iscomplexobj(Hy_np)
                    
                    # Handle complex Ez data
                    if np.iscomplexobj(Ez_np):
                        Ez_real = np.real(Ez_np)
                        Ez_imag = np.imag(Ez_np)
                    else:
                        Ez_real = Ez_np
                        Ez_imag = np.zeros_like(Ez_np)
                    
                    # Extend magnetic fields to match Ez dimensions
                    # Create arrays with matching dtype to avoid warnings
                    if is_complex:
                        Hx_full = np.zeros_like(Ez_np, dtype=np.complex128)
                        Hy_full = np.zeros_like(Ez_np, dtype=np.complex128)
                    else:
                        Hx_full = np.zeros_like(Ez_real)
                        Hy_full = np.zeros_like(Ez_real)
                        
                    # Properly handle filling the arrays
                    if np.iscomplexobj(Hx_np):
                        Hx_full[:, :-1] = Hx_np
                    else:
                        Hx_full[:, :-1] = Hx_np
                        
                    if np.iscomplexobj(Hy_np):
                        Hy_full[:-1, :] = Hy_np
                    else:
                        Hy_full[:-1, :] = Hy_np
                    
                    # For complex fields, extract real/imag parts for power calculation
                    if is_complex:
                        Hx_real = np.real(Hx_full)
                        Hx_imag = np.imag(Hx_full)
                        Hy_real = np.real(Hy_full)
                        Hy_imag = np.imag(Hy_full)
                        
                        # Calculate Poynting vector components for real and imaginary parts
                        # Using complete formula for complex Poynting vector:
                        # S = (1/2) Re[E × H*] where H* is complex conjugate of H
                        Sx = -Ez_real * Hy_real - Ez_imag * Hy_imag
                        Sy = Ez_real * Hx_real + Ez_imag * Hx_imag
                    else:
                        # Real-only fields, simple calculation
                        Sx = -Ez_real * Hy_full
                        Sy = Ez_real * Hx_full
                    
                    # Calculate power magnitude (|S|²)
                    power_mag = Sx**2 + Sy**2
                    
                    # Accumulate power
                    self.power_accumulated += power_mag
                    self.power_accumulation_count += 1
                
                # Save results if requested and at the right frequency
                if save and not save_memory_mode and (step % effective_save_freq == 0 or step == self.num_steps - 1):
                    # Convert arrays to numpy for saving
                    self.results['t'].append(self.t)
                    # Save only the requested fields
                    if 'Ez' in save_fields: self.results['Ez'].append(self.backend.to_numpy(self.backend.copy(self.Ez)))
                    if 'Hx' in save_fields: self.results['Hx'].append(self.backend.to_numpy(self.backend.copy(self.Hx)))
                    if 'Hy' in save_fields: self.results['Hy'].append(self.backend.to_numpy(self.backend.copy(self.Hy)))
                
                # Show live animation if requested and at the right frequency
                if live and (step % 1 == 0 or step == self.num_steps - 1):
                    Ez_np = self.backend.to_numpy(self.Ez)
                    self.animate_live(field_data=Ez_np, field="Ez", axis_scale=axis_scale)

                # Update time & progress
                self.t += self.dt
                progress.update(task, advance=1)
                
        # Clean up animation
        if live and self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
            self.im = None
                
        # Display completion information
        display_status("Simulation complete!", "success")
        display_time_elapsed(self.start_time)
        
        # Save animation if requested
        if save_animation and (save or accumulate_power):
            display_status(f"Saving animation to {animation_filename}...", "info")
            if not save_memory_mode and 'Ez' in save_fields and len(self.results['Ez']) > 0:
                self.save_animation(field="Ez", axis_scale=axis_scale, filename=animation_filename, clean_visualization=clean_visualization)
            elif accumulate_power: 
                display_status("Cannot create animation in memory-saving mode without field data.", "warning")
        
        # Calculate final power average if accumulating
        if accumulate_power and self.power_accumulation_count > 0:
            self.power_accumulated /= self.power_accumulation_count
            
        # Display memory usage estimate
        memory_usage = self.estimate_memory_usage(time_steps=self.num_steps, save_fields=save_fields)
        display_status(f"Estimated memory usage: {memory_usage['Full simulation']['Total memory (MB)']:.2f} MB", "info")
        
        return self.results
        
    def _record_monitor_data(self, step):
        """Record field data at monitor locations"""
        # Convert field data to numpy for monitors
        Ez_np = self.backend.to_numpy(self.Ez)
        Hx_np = self.backend.to_numpy(self.Hx)
        Hy_np = self.backend.to_numpy(self.Hy)
        
        # Record data for each monitor
        for monitor in self.design.monitors:
            # Use the monitor's record_fields method
            monitor.record_fields(
                Ez=Ez_np,  # Ez is already complex if needed
                Hx=Hx_np, 
                Hy=Hy_np,
                t=self.t,
                dx=self.dx,
                dy=self.dy,
                save_memory=self.save_memory_mode,
                accumulate_power=self.accumulate_power)

    def save_animation(self, field: str = "Ez", axis_scale=[-1, 1], filename='fdtd_animation.mp4', fps=60, frame_skip=4, clean_visualization=False):
        """Save an animation of the simulation results as an mp4 file."""
        if len(self.results[field]) == 0:
            print("No field data to animate. Make sure to run the simulation with save=True.")
            return
        # Create list of frame indices to use (applying frame_skip)
        total_frames = len(self.results[field])
        frame_indices = range(0, total_frames, frame_skip)
        # Calculate figure size based on grid dimensions
        grid_height, grid_width = self.results[field][0].shape
        aspect_ratio = grid_width / grid_height
        base_size = 5  # Base size for the smaller dimension
        if aspect_ratio > 1: figsize = (base_size * aspect_ratio * 1.2, base_size)
        else: figsize = (base_size * 1.2, base_size / aspect_ratio)
        # Set up figure and axes based on visualization style
        if clean_visualization:
            # Create figure with absolutely no padding or borders
            # Use tight_layout and adjust figure parameters to eliminate all whitespace
            if aspect_ratio > 1: figsize = (base_size * aspect_ratio, base_size)
            else: figsize = (base_size, base_size / aspect_ratio)
            fig = plt.figure(figsize=figsize, frameon=False)
            # Use the entire figure space with no margins
            ax = fig.add_axes([0, 0, 1, 1])
            ax.set_axis_off()
            # Ensure no padding or margins
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
            # Explicitly turn off all spines, ticks, and labels
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
        else:
            # Create standard figure with normal padding
            fig, ax = plt.subplots(figsize=figsize)
            # Get units for axis labels
            max_dim = max(self.design.width, self.design.height)
            if max_dim >= 1e-3: scale, unit = 1e3, 'mm'
            elif max_dim >= 1e-6: scale, unit = 1e6, 'µm'
            elif max_dim >= 1e-9: scale, unit = 1e9, 'nm'
            else: scale, unit = 1e12, 'pm'
        # Create initial plot
        im = ax.imshow(self.results[field][0], origin='lower',
                      extent=(0, self.design.width, 0, self.design.height),
                      cmap='RdBu', aspect='equal', interpolation='bicubic', 
                      vmin=axis_scale[0], vmax=axis_scale[1])
        # Add colorbar if not using clean visualization
        if not clean_visualization:
            colorbar = plt.colorbar(im, orientation='vertical', aspect=30, extend='both')
            colorbar.set_label(f'{field} Field Amplitude')
        # Add design structure outlines
        for structure in self.design.structures:
            # Use dashed lines for PML regions
            if hasattr(structure, 'is_pml') and structure.is_pml:
                structure.add_to_plot(ax, edgecolor="black", linestyle='--', facecolor='none', alpha=0.5)
            else:
                structure.add_to_plot(ax, facecolor="none", edgecolor="black")
        # Configure standard plot elements if not using clean visualization
        if not clean_visualization:
            # Add axis labels with proper scaling
            plt.xlabel(f'X ({unit})')
            plt.ylabel(f'Y ({unit})')
            ax.xaxis.set_major_formatter(lambda x, pos: f'{x*scale:.1f}')
            ax.yaxis.set_major_formatter(lambda x, pos: f'{x*scale:.1f}')
            # Title with time information
            title = ax.set_title(f't = {self.results["t"][0]:.2e} s')
        else: title = None
        # Animation update function
        def update(frame_idx):
            frame = frame_indices[frame_idx]
            im.set_array(self.results[field][frame])
            if not clean_visualization:
                title.set_text(f't = {self.results["t"][frame]:.2e} s')
                return [im, title]
            return [im]
        # Create animation with only the selected frames
        frames = len(frame_indices)
        ani = FuncAnimation(fig, update, frames=frames, blit=True)
        # Save animation
        try:
            from matplotlib.animation import FFMpegWriter
            writer = FFMpegWriter(fps=fps)
            if clean_visualization: ani.save(filename, writer=writer, dpi=300)
            else: ani.save(filename, writer=writer, dpi=100)
            print(f"Animation saved to {filename} (using {frames} of {total_frames} frames)")
        except Exception as e:
            print(f"Error saving animation: {e}")
            print("Make sure FFmpeg is installed on your system.")
        # Close the figure
        plt.close(fig)
        
    def plot_power(self, cmap: str = "hot", vmin: float = None, vmax: float = None, db_colorbar: bool = False):
        """Plot the time-integrated power distribution from the E and H fields.
        
        Args:
            cmap: Colormap to use for the plot (default: 'hot')
            log_scale: Whether to plot power in logarithmic scale (dB) (default: False)
            vmin: Minimum value for colorbar scaling (optional)
            vmax: Maximum value for colorbar scaling (optional)
            db_colorbar: Whether to display colorbar in dB scale even with linear data (default: False)
            
        Returns:
            None
        """
        # Check if we have accumulated power
        if self.power_accumulated is not None:
            # Use pre-accumulated power
            power = self.power_accumulated
            print("Using accumulated power data")
        elif len(self.results['Ez']) > 0 and len(self.results['Hx']) > 0 and len(self.results['Hy']) > 0:
            # Calculate power from saved field data
            print("Calculating power from saved field data")
            # Initialize power array
            power = np.zeros((self.nx, self.ny))
            # Calculate average power over all time steps
            for t_idx in range(len(self.results['t'])):
                Ez = self.results['Ez'][t_idx]
                Hx_raw = self.results['Hx'][t_idx]
                Hy_raw = self.results['Hy'][t_idx]
                
                # Check if any field is complex
                is_complex = np.iscomplexobj(Ez) or np.iscomplexobj(Hx_raw) or np.iscomplexobj(Hy_raw)
                
                # Handle complex Ez data
                if np.iscomplexobj(Ez):
                    Ez_real = np.real(Ez)
                    Ez_imag = np.imag(Ez)
                else:
                    Ez_real = Ez
                    Ez_imag = np.zeros_like(Ez)
                
                # Extend magnetic fields to match Ez dimensions
                if is_complex:
                    Hx = np.zeros_like(Ez, dtype=np.complex128)
                    Hy = np.zeros_like(Ez, dtype=np.complex128)
                else:
                    Hx = np.zeros_like(Ez_real)
                    Hy = np.zeros_like(Ez_real)
                    
                # Properly handle filling the arrays
                if np.iscomplexobj(Hx_raw):
                    Hx[:, :-1] = Hx_raw
                else:
                    Hx[:, :-1] = Hx_raw
                    
                if np.iscomplexobj(Hy_raw):
                    Hy[:-1, :] = Hy_raw
                else:
                    Hy[:-1, :] = Hy_raw
                
                # For complex fields, use proper calculation
                if is_complex:
                    Hx_real = np.real(Hx)
                    Hx_imag = np.imag(Hx)
                    Hy_real = np.real(Hy)
                    Hy_imag = np.imag(Hy)
                    
                    # Calculate Poynting vector components for real and imaginary parts
                    # Using formula for complex Poynting vector: S = (1/2) Re[E × H*]
                    Sx = -Ez_real * Hy_real - Ez_imag * Hy_imag
                    Sy = Ez_real * Hx_real + Ez_imag * Hx_imag
                else:
                    # Real-only fields
                    Sx = -Ez_real * Hy
                    Sy = Ez_real * Hx
                
                # Calculate power magnitude (|S|²)
                power_mag = Sx**2 + Sy**2
                
                # Accumulate power
                power += power_mag
            # Average power over time steps
            power /= len(self.results['t'])
        else:
            print("No field data to calculate power. Make sure to run the simulation with save=True or accumulate_power=True.")
            return
        # Determine appropriate SI unit and scale for spatial dimensions
        max_dim = max(self.design.width, self.design.height)
        if max_dim >= 1e-3: scale, unit = 1e3, 'mm'
        elif max_dim >= 1e-6: scale, unit = 1e6, 'µm'
        elif max_dim >= 1e-9: scale, unit = 1e9, 'nm'
        else: scale, unit = 1e12, 'pm'
        # Configure plot size
        aspect_ratio = power.shape[1] / power.shape[0]
        base_size = 8  # Base size for the smaller dimension
        if aspect_ratio > 1: figsize = (base_size * aspect_ratio, base_size)
        else: figsize = (base_size, base_size / aspect_ratio)
        # Apply logarithmic scaling if requested
        max_power = np.max(power)
        if max_power <= 0:
            print("Warning: Maximum power is zero or negative. Cannot plot logarithmic scale.")
            log_scale = False

        # Create the figure and axis
        self.fig, self.ax = plt.subplots(figsize=figsize)
        # Create initial plot with proper scaling
        self.im = self.ax.imshow(power, origin='lower',
                                extent=(0, self.design.width, 0, self.design.height),
                                cmap=cmap, aspect='equal', interpolation='bicubic', vmin=vmin, vmax=vmax)
        # Add colorbar
        colorbar = plt.colorbar(self.im, orientation='vertical', aspect=30, extend='both')
        # Convert to dB scale for colorbar if requested
        if db_colorbar:
            # Define a formatter function to convert linear values to dB
            def db_formatter(x, pos):
                if x <= 0: return "-∞ dB"  # Return negative infinity for zero/negative values
                ratio = max(x / max_power, 1e-10)  # Ensure minimum value is 1e-10 (-100 dB)
                db_val = 10 * np.log10(ratio)
                return f"{db_val:.1f} dB"
            colorbar.formatter = plt.FuncFormatter(db_formatter)
            # Set specific dB ticks
            colorbar.update_ticks() 
            colorbar.set_label('Relative Power (dB)')
        else: colorbar.set_label('Power (a.u.)')
        # Add design structure outlines
        for structure in self.design.structures:
            # Use dashed lines for PML regions
            if hasattr(structure, 'is_pml') and structure.is_pml:
                structure.add_to_plot(self.ax, edgecolor="white", linestyle='--', facecolor='none', alpha=0.5)
            else:
                structure.add_to_plot(self.ax, facecolor="none", edgecolor="white")
        # Add axis labels with proper scaling
        plt.xlabel(f'X ({unit})')
        plt.ylabel(f'Y ({unit})')
        self.ax.xaxis.set_major_formatter(lambda x, pos: f'{x*scale:.1f}')
        self.ax.yaxis.set_major_formatter(lambda x, pos: f'{x*scale:.1f}')
        # Add plot elements
        plt.title('Time-Averaged Power Distribution')
        plt.tight_layout()
        plt.show()

    def estimate_memory_usage(self, time_steps=None, save_fields=None):
        """Estimate memory usage of the simulation with current settings.
        
        Args:
            time_steps: Number of time steps to estimate for (defaults to self.num_steps)
            save_fields: List of fields to save (defaults to ['Ez', 'Hx', 'Hy'])
            
        Returns:
            Dictionary with memory usage estimates in MB
        """
        if time_steps is None: time_steps = self.num_steps
        if save_fields is None: save_fields = ['Ez', 'Hx', 'Hy']
        # Calculate size of a single array
        bytes_per_value = np.float64(0).nbytes  # Usually 8 bytes for float64
        # Sizes of the arrays
        ez_size = self.nx * self.ny * bytes_per_value
        hx_size = self.nx * (self.ny-1) * bytes_per_value
        hy_size = (self.nx-1) * self.ny * bytes_per_value
        t_size = time_steps * bytes_per_value
        # Calculate total memory for all time steps
        total_size = t_size
        if 'Ez' in save_fields: total_size += ez_size * time_steps
        if 'Hx' in save_fields: total_size += hx_size * time_steps
        if 'Hy' in save_fields: total_size += hy_size * time_steps
        # Convert to more readable units
        kb = 1024
        mb = kb * 1024
        gb = mb * 1024
        result = {
            'Single timestep': {
                'Ez': ez_size / mb,
                'Hx': hx_size / mb,
                'Hy': hy_size / mb,
                'Total': (ez_size + hx_size + hy_size) / mb
            },
            'Full simulation': {
                'Total memory (MB)': total_size / mb,
                'Total memory (GB)': total_size / gb,
                'Time steps': time_steps,
                'Grid size': f"{self.nx} x {self.ny}",
                'Fields saved': ', '.join(save_fields)
            }
        }
        # After calculation, display results with new helpers
        display_status(f"Estimated memory usage: {total_size / mb:.2f} MB", "info")
        return result

    def plot_monitors(self, field='Ez', figsize=(10, 6), power=False, log_scale=False, db_scale=False):
        """Plot the data from all monitors.
        
        Args:
            field: Field to plot ('Ez', 'Hx', or 'Hy')
            figsize: Figure size tuple
            power: If True, plot power instead of field
            log_scale: If True, use logarithmic scale for power plots
            db_scale: If True, use dB scale for power plots
            
        Returns:
            List of (monitor, fig, ax) tuples
        """
        import matplotlib.pyplot as plt
        # Check if we have monitors
        if not self.design.monitors:
            print("No monitors in the design.")
            return []
        # Create plots for each monitor
        results = []
        for monitor in self.design.monitors:
            if power: fig, ax = monitor.plot_power(figsize=figsize, log_scale=log_scale, db_scale=db_scale)
            else: fig, ax = monitor.plot_fields(field=field, figsize=figsize)
            if fig is not None: results.append((monitor, fig, ax))
        return results