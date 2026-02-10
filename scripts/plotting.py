import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BIN_DIR = PROJECT_ROOT / "bin"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_IMAGE_DIR = PROJECT_ROOT / "output-image"

wavelength = 2 * 3.141592 * 137.036 / 0.057

# ----------------------------------------------------------------------- #

def plot_2d_colormap(method, sim_parameters, a0_array):
    i = sim_parameters.i
    a0 = a0_array[i]
    wave_count = sim_parameters.wave_count
    square_size = sim_parameters.square_size
    
    if(method == "electromagnetic"):
        filename_out = f"{OUTPUT_IMAGE_DIR}/out-colormap-electromag-{i}.png"
    else:
        filename_out = f"{OUTPUT_IMAGE_DIR}/out-colormap-pond-{i}.png"
    filename = f"{OUTPUT_DIR}/out-data.bin"
    
    
    data = np.fromfile(filename, dtype=np.float64).reshape(-1, 16)
    
    x = data[:, 2] / wavelength
    y = data[:, 3] / wavelength
    c = data[:, 14]
    
    plt.figure(figsize=(10,10))
    plt.scatter(x, y, c=c, marker='s', s=square_size, cmap='RdBu_r')
    plt.xlim(-wave_count, wave_count)
    plt.ylim(-wave_count, wave_count)
    plt.xlabel(r"Y [$\lambda$]")
    plt.ylabel(r"Z [$\lambda$]")
    plt.title(f"a0 = {a0:0.3f}")
    plt.colorbar()
    plt.savefig(filename_out, dpi=150, bbox_inches='tight')
    plt.close()
        
    print(f"Created colormap.")

# ----------------------------------------------------------------------- #

def plot_phases(method, sim_parameters):
    i = sim_parameters.i
    a0 = sim_parameters.a0
    num = sim_parameters.num
    steps = sim_parameters.steps // sim_parameters.substeps
    wave_count = sim_parameters.wave_count
    full_trajectory = sim_parameters.full_trajectory
    divider = sim_parameters.divider
    
    if(method == "electromagnetic"):
        filename_out = f"{OUTPUT_IMAGE_DIR}/out-phase-space-electromag-{i}.png"
        filename_exit = f"{OUTPUT_DIR}/out-enter-exit-time-electromag.bin"
    else:
        filename_out = f"{OUTPUT_IMAGE_DIR}/out-phase-space-pond-{i}.png"
        filename_exit = f"{OUTPUT_DIR}/out-enter-exit-time-pond.bin"
    filename = f"{OUTPUT_DIR}/out-data.bin"
    
    
    data = np.fromfile(filename, dtype=np.float64).reshape(num, steps, 8)
    data_exit = np.fromfile(filename_exit, dtype=np.float64).reshape(num, 4)
    fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
    
    colmap = plt.get_cmap('Spectral')
    
    subsection = num // divider
    
    data = data[:subsection]
    data_exit = data_exit[:subsection]
    
    for idx in range(subsection):
        if(full_trajectory):
            last_step = steps
        else:
            last_step = int(data_exit[idx, 3])
        traj = data[idx]
        traj = traj[:last_step]
        color = idx / subsection
        color_cmap = colmap(color)
        
        x = traj[:, 2] / wavelength
        y = traj[:, 6]
        
        sc = ax.plot(x, y, c=color_cmap, linewidth=0.5)
        
    ax.set_title(f"Phase space: $a_0 = {a0:0.3f}$ - $N = {subsection}$")
    ax.set_xlabel(r"$y$ [$\lambda$]")
    ax.set_ylabel(r"$p_y$")
    
    ax.set_xlim(-1.1 * wave_count, 1.1 * wave_count)
    
    plt.savefig(filename_out, bbox_inches='tight')
    plt.close()
    
    print(f"Created phase plot.")
    
# ----------------------------------------------------------------------- #

def plot_time_momentum(method, sim_parameters, a0_array):
    i = sim_parameters.i
    a0 = a0_array[i]
    num = sim_parameters.num
    steps = sim_parameters.steps // sim_parameters.substeps
    wave_count = sim_parameters.wave_count
    divider = sim_parameters.divider
    full_trajectory = sim_parameters.full_trajectory
    
    if(method == "electromagnetic"):
        filename_out = f"{OUTPUT_IMAGE_DIR}/out-time-momentum-electromag-{i}.png"
        filename_exit = f"{OUTPUT_DIR}/out-enter-exit-time-electromag.bin"
    else:
        filename_out = f"{OUTPUT_IMAGE_DIR}/out-time-momentum-pond-{i}.png"
        filename_exit = f"{OUTPUT_DIR}/out-enter-exit-time-pond.bin"
    filename = f"{OUTPUT_DIR}/out-data.bin"
    
    
    data = np.fromfile(filename, dtype=np.float64).reshape(num, steps, 8)
    data_exit = np.fromfile(filename_exit, dtype=np.float64).reshape(num, 4)
    fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
    
    colmap = plt.get_cmap('Spectral')
    
    subsection = num // divider
    
    data = data[:subsection]
    data_exit = data_exit[:subsection]
    
    for idx in range(subsection):
        if(full_trajectory):
            last_step = steps
        else:
            last_step = int(data_exit[idx, 3])
        traj = data[idx]
        traj = traj[:last_step]
        color = idx / subsection
        color_cmap = colmap(color)
        
        x = traj[:, 0] / 137.036
        y = traj[:, 6]
        
        sc = ax.plot(x, y, c=color_cmap, linewidth=0.5)
        
    ax.set_title(f"Time - momentum plot for: $a_0 = {a0:0.3f}$ - $N = {subsection}$")
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$p_y$")
    
    
    plt.savefig(filename_out, bbox_inches='tight')
    plt.close()
    
    
    print(f"Created time-momentum plot.")
    
# ----------------------------------------------------------------------- #

def plot_2d_heatmap_all(method, sim_parameters, a0_array):
    num = sim_parameters.num
    wave_count = sim_parameters.wave_count
    sweep_steps = sim_parameters.sweep_steps
    square_size = sim_parameters.square_size
    
    if(method == "electromagnetic"):
        filename_in = f"{OUTPUT_DIR}/out-final-py-all-electromag.bin"
        filename_out = f"{OUTPUT_IMAGE_DIR}/_out-2d-heatmap-electromag.png"
        filename_in_max_py = f"{OUTPUT_DIR}/out-max-py-electromag.bin"
    else:
        filename_in = f"{OUTPUT_DIR}/out-final-py-all-pond.bin"
        filename_out = f"{OUTPUT_IMAGE_DIR}/_out-2d-heatmap-pond.png"
        filename_in_max_py = f"{OUTPUT_DIR}/out-max-py-pond.bin"
        
    data = np.fromfile(filename_in, dtype=np.float64).reshape(sweep_steps, num, 2)
    data_max_py = np.fromfile(filename_in_max_py, dtype=np.float64).reshape(sweep_steps, 2)
    fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
    
    for idx in range(sweep_steps):
        a0_current = a0_array[idx]
        
        pos = data[idx, :, 0] / wavelength
        py = data[idx, :, 1]
        a0_now = np.full(num, a0_current, dtype=np.float64)
        
        sc = ax.scatter(pos, a0_now, c=py, cmap='RdBu_r', s=square_size, marker='s')
        
    plt.xlim(-wave_count, wave_count)
    plt.ylim(min(a0_array), max(a0_array))
    plt.xlabel(r"Y [$\lambda$]")
    plt.ylabel(r"$a_0$")
    plt.title(f"Full parameter sweep heatmap")
    plt.savefig(filename_out, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"Created 2D heatmap of full {method} parameter sweep.")

# ----------------------------------------------------------------------- #

def plot_enter_exit_time(method, sim_parameters, a0_array):
    i = sim_parameters.i
    a0 = a0_array[i]
    num = sim_parameters.num
    steps = sim_parameters.steps//sim_parameters.substeps
    
    if method == "electromagnetic":
        mode = 0
        filename_enter_exit_time = f"{OUTPUT_DIR}/out-enter-exit-time-electromag.bin"
    else:
        mode = 1
        filename_enter_exit_time = f"{OUTPUT_DIR}/out-enter-exit-time-pond.bin"

    data = np.fromfile(filename_enter_exit_time, dtype=np.float64).reshape(-1, 4)
    
    
    x = data[:, 0] / wavelength
    y1 = data[:, 1] / 137.036
    y2 = data[:, 2] / 137.036
    
    plt.figure(figsize=(10,10))
    plt.plot(x, y1, linestyle='-', c='blue', linewidth=1)
    plt.plot(x, y2, linestyle='-', c='red', linewidth=1)
    plt.title(f"Enter and exit time for $a_0$ = {a0:0.3f}")
    plt.xlabel(r"$y$ [$\lambda$]")
    plt.ylabel(f"t")
    
    plt.axhline(0, color='black', linestyle='--')
    
    filename_out = f"{OUTPUT_IMAGE_DIR}/out-enter-exit-time-{i}.png"
    plt.savefig(filename_out, dpi=150, bbox_inches='tight')
    plt.close()
    
    if(mode == 0):
        os.rename(filename_out, f"{OUTPUT_IMAGE_DIR}/out-enter-exit-time-electromag-{i}.png")
    else:
        os.rename(filename_out, f"{OUTPUT_IMAGE_DIR}/out-enter-exit-time-pond-{i}.png")

    print(f"Created enter exit time plot.")

# ----------------------------------------------------------------------- #

def plot_errors(sim_parameters):
    i = sim_parameters.i
    a0 = sim_parameters.a0
    num = sim_parameters.num
    
    filename = f"{OUTPUT_DIR}/out-error.bin"
    filename_max_py = f"{OUTPUT_DIR}/out-max-py-electromag.bin"

    data = np.fromfile(filename, dtype=np.float64).reshape(-1, 2)
    data2 = np.fromfile(filename_max_py, dtype=np.float64).reshape(-1, 2)
    
    x = data[:, 0] / wavelength
    y = data[:, 1]
    
    y_max = data2[i, 1]
    print(f"For a0 = {a0:0.3f}, max(py) = {yMax:0.3f}")
    
    y_final = y / y_max * 100.0
    
    plt.figure(figsize=(10,10))
    plt.plot(x, y_final, c='black',linestyle='-', linewidth=1)
    plt.title(f"Errors for a0 = {a0:0.3f}")
    plt.xlabel(r"Y [$\lambda$]")
    plt.ylabel(f"Error (%)")
    
    plt.axhline(0, color='black', linestyle='--')
    
    filename_out = f"{OUTPUT_IMAGE_DIR}/out-errors-{i}.png"
    plt.savefig(filename_out, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Created error scatter plot.")

# ----------------------------------------------------------------------- #

def plot_all_errors(sim_parameters, a0_array):
    num = sim_parameters.num
    wave_count = sim_parameters.wave_count
    square_size = sim_parameters.square_size
    sweep_steps = sim_parameters.sweep_steps
    
    filename_out = f"{OUTPUT_IMAGE_DIR}/_out-2d-heatmap-errors.png"
    filename_in = f"{OUTPUT_DIR}/out-error-all.bin"
    filename_in_max_py = f"{OUTPUT_DIR}/out-max-py-electromag.bin"
    
    data = np.fromfile(filename_in, dtype=np.float64).reshape(sweep_steps, num, 2)
    data_max_py = np.fromfile(filename_in_max_py, dtype=np.float64).reshape(sweep_steps, 2)
    fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
    
    for idx in range(sweep_steps):
        a0_current = a0_array[idx]
        
        pos = data[idx, :, 0] / wavelength
        error = data[idx, :, 1] / data_max_py[idx, 1]
        a0_now = np.full(num, a0_current, dtype=np.float64)
        
        sc = ax.scatter(pos, a0_now, c=error, cmap='inferno', s=square_size, marker='s')
        
    plt.xlim(-wave_count, wave_count)
    plt.ylim(min(a0_array), max(a0_array))
    plt.xlabel(r"Y [$\lambda$]")
    plt.ylabel(r"$a_0$")
    plt.title(f"Full error heatmap")
    plt.savefig(filename_out, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"Created 2D heatmap of errors.")

# ----------------------------------------------------------------------- #

def plot_max_py(method, a0_array):
    if(method == "electromagnetic"):
        filename = f"{OUTPUT_DIR}/out-max-py-electromag.bin"
        filename_out = f"{OUTPUT_IMAGE_DIR}/_out-max-py-electromag.png"
    else:
        filename = f"{OUTPUT_DIR}/out-max-py-pond.bin"
        filename_out = f"{OUTPUT_IMAGE_DIR}/_out-max-py-pond.png"
    
    data = np.fromfile(filename, dtype=np.float64).reshape(-1, 2)
    
    x = a0_array
    y = data[:, 1]
    
    plt.figure(figsize=(10,10))
    plt.plot(x, y, c='black', linestyle='-', linewidth=1)
    plt.title(r"max($p_y$)")
    plt.xlabel(r"$a_0$")
    plt.ylabel(r"max($p_y$)")
    
    plt.axhline(0, color='black', linestyle='--')
    
    plt.savefig(filename_out, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Created max(py) scatter plot for {method} mode.")
    
# ----------------------------------------------------------------------- #    

def plot_average_errors(a0_array):
    filename = f"{OUTPUT_DIR}/out-average-error.bin"
    data = np.fromfile(filename, dtype=np.float64).reshape(-1, 2)
    
    x = np.array(a0_array)
    y = data[:, 1]
    
    plt.figure(figsize=(10,10))
    plt.plot(x, y, c='black', linestyle='-', linewidth=1)
    plt.title(r"Average errors")
    plt.xlabel(r"$a_0$")
    plt.ylabel(r"<$\epsilon$> (%)")
    
    plt.axhline(0, color='black', linestyle='--')
    
    filename_out = f"{OUTPUT_IMAGE_DIR}/_out-average-errors.png"
    plt.savefig(filename_out, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Created average error scatter plot.")

# ----------------------------------------------------------------------- #

def plot_phases_oscillator(a0, i, num, wavelength, wave_count):
    programPath = f"{BIN_DIR}/oscillator"
    os.system(f"{programPath} {a0:0.3f} {num}")

    filename = f"{OUTPUT_DIR}/out-oscillator.bin"
    data = np.fromfile(filename, dtype=np.float64).reshape(num, 4096, 3)
    fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
    time_indices = np.arange(4096)
    
    for idx in range(num):
        traj = data[idx]
        
        x = traj[:, 1] / wavelength
        y = traj[:, 2]
        
        sc = ax.scatter(x, y, c=time_indices, cmap='viridis', s=0.5)

    ax.set_title(f"Phase space (potential): $a_0 = {a0:0.3f}$ - $N = {num}$")
    ax.set_xlabel(r"$y$ [$\lambda$]")
    ax.set_ylabel(r"$p_y$")
    
    ax.set_xlim(-1.1 * wave_count, 1.1 * wave_count)
    
    filename_out = f"{OUTPUT_IMAGE_DIR}/out-phase-space-potential-{i}.png"
    
    plt.savefig(filename_out, bbox_inches='tight')
    plt.close()
    
    print(f"Created potential phase plot.")

# ----------------------------------------------------------------------- #