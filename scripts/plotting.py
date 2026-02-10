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

# ----------------------------------------------------------------------- #

def plot_2d_colormap(method, sim_parameters, a0_array):
    i = sim_parameters.i
    a0 = a0_array[i]
    r = sim_parameters.r
    wave_count = sim_parameters.wave_count
    square_size = sim_parameters.square_size
    
    if(method == "electromagnetic"):
        filename_out = f"{OUTPUT_IMAGE_DIR}/out-colormap-electromag-{i}.png"
    else:
        filename_out = f"{OUTPUT_IMAGE_DIR}/out-colormap-pond-{i}.png"
    filename = f"{OUTPUT_DIR}/out-data.bin"
    
    data = np.fromfile(filename, dtype=np.float64).reshape(-1, 16)
    
    x = data[:, 2] / r
    y = data[:, 3] / r
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

def plot_phases(method, sim_parameters, a0_array):
    i = sim_parameters.i
    a0 = a0_array[i]
    r = sim_parameters.r
    num = sim_parameters.num
    wave_count = sim_parameters.wave_count
    steps = sim_parameters.steps // sim_parameters.substeps
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
        
        x = traj[:, 2] / r
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
    r = sim_parameters.r
    num = sim_parameters.num
    steps = sim_parameters.steps // sim_parameters.substeps
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
    r = sim_parameters.r
    num = sim_parameters.num
    sweep_steps = sim_parameters.sweep_steps
    wave_count = sim_parameters.wave_count
    
    if(method == "electromagnetic"):
        filename_in = f"{OUTPUT_DIR}/out-final-py-all-electromag.bin"
        filename_out = f"{OUTPUT_IMAGE_DIR}/_out-2d-heatmap-electromag.png"
    else:
        filename_in = f"{OUTPUT_DIR}/out-final-py-all-pond.bin"
        filename_out = f"{OUTPUT_IMAGE_DIR}/_out-2d-heatmap-pond.png"
    
    data = np.fromfile(filename_in, dtype=np.float64).reshape(sweep_steps, num, 2)
    
    x = data[:, :, 0] / r
    y = np.repeat(a0_array[:, np.newaxis], num, axis=1)
    z = data[:, :, 1]
    fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
    
    pcm = ax.pcolormesh(x, y, z, cmap='RdBu_r', shading='auto', rasterized=True)
    
    cbar = plt.colorbar(pcm, ax=ax, label=r"$p_y$")
    cbar.set_label("Final momentum [a.u.]")
    
    plt.xlim(-wave_count, wave_count)
    plt.ylim(min(a0_array), max(a0_array))
    plt.xlabel(r"Y [$\lambda$]")
    plt.ylabel(r"$a_0$")
    plt.title(f"Full parameter sweep heatmap ({method})")
    
    plt.savefig(filename_out, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Created 2D heatmap of full {method} parameter sweep.")

# ----------------------------------------------------------------------- #

def plot_2d_errors_heatmap(sim_parameters, a0_array):
    r = sim_parameters.r
    num = sim_parameters.num
    wave_count = sim_parameters.wave_count
    sweep_steps = sim_parameters.sweep_steps
    
    filename_out = f"{OUTPUT_IMAGE_DIR}/_out-2d-heatmap-errors.png"
    filename_in = f"{OUTPUT_DIR}/out-error-all.bin"
    filename_in_max_py = f"{OUTPUT_DIR}/out-max-py-electromag.bin"
    
    data = np.fromfile(filename_in, dtype=np.float64).reshape(sweep_steps, num, 2)
    data_max_py = np.fromfile(filename_in_max_py, dtype=np.float64).reshape(sweep_steps, 2)
    
    error = data[:, :, 1]
    x = data[:, :, 0] / r
    y = np.repeat(a0_array[:, np.newaxis], num, axis=1)
    norm = data_max_py[:, 1][:, np.newaxis]
    z = error / norm
    
    fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
    pcm = ax.pcolormesh(x, y, z, cmap='inferno', shading='auto', rasterized=True)
    
    cbar = plt.colorbar(pcm, ax=ax)
    cbar.set_label("Relative error [%]")
    
    plt.xlim(-wave_count, wave_count)
    plt.ylim(min(a0_array), max(a0_array))
    plt.xlabel(r"Y [$\lambda$]")
    plt.ylabel(r"$a_0$")
    plt.title(f"Full error heatmap")
    
    plt.savefig(filename_out, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Created 2D error heatmap.")

# ----------------------------------------------------------------------- #

def plot_enter_exit_time(method, sim_parameters, a0_array):
    r = sim_parameters.r
    num = sim_parameters.num
    i = sim_parameters.i
    a0 = a0_array[i]
    steps = sim_parameters.steps // sim_parameters.substeps
    
    if method == "electromagnetic":
        mode = 0
        filename_enter_exit_time = f"{OUTPUT_DIR}/out-enter-exit-time-electromag.bin"
    else:
        mode = 1
        filename_enter_exit_time = f"{OUTPUT_DIR}/out-enter-exit-time-pond.bin"
        
    data = np.fromfile(filename_enter_exit_time, dtype=np.float64).reshape(-1, 4)
    
    x = data[:, 0] / r
    y1 = data[:, 1] / 137.036
    y2 = data[:, 2] / 137.036
    
    mask = (y1 != 0.0) & (y2 != 0.0)
    
    x = x[mask]
    y1 = y1[mask]
    y2 = y2[mask]
    
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
    r = sim_parameters.r
    a0 = sim_parameters.a0
    num = sim_parameters.num
    
    filename = f"{OUTPUT_DIR}/out-error.bin"
    filename_max_py = f"{OUTPUT_DIR}/out-max-py-electromag.bin"

    data = np.fromfile(filename, dtype=np.float64).reshape(-1, 2)
    data2 = np.fromfile(filename_max_py, dtype=np.float64).reshape(-1, 2)
    
    x = data[:, 0] / r
    y = data[:, 1]
    
    y_max = data2[i, 1]
    print(f"For a0 = {a0:0.3f}, max(py) = {y_max:0.3f}")
    
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