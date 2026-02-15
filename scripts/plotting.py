import os
import sys
import warnings
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import scripts.common as common

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BIN_DIR = PROJECT_ROOT / "bin"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_IMAGE_DIR = PROJECT_ROOT / "output-image"

plt.rcParams.update({'font.size': 12})

def plot_2d_colormap(method, sim_parameters, a0_array, axis_horiz, axis_vert, axis_p):
    axis_text_horiz = common.get_axis_text(axis_horiz)
    lowercase_text_horiz = axis_text_horiz.lower()
    
    axis_text_vert = common.get_axis_text(axis_vert)
    lowercase_text_vert = axis_text_vert.lower()
    
    axis_text_p = common.get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    i = sim_parameters.i
    a0 = a0_array[i]
    num = sim_parameters.num
    r_min = sim_parameters.r_min
    r_max = sim_parameters.r_min
    wavelength = sim_parameters.wavelength
    square_size = sim_parameters.square_size
    
    if(method == "electromagnetic"):
        filename_out = f"{OUTPUT_IMAGE_DIR}/out-colormap-electromag-{lowercase_text_horiz}{lowercase_text_vert}{lowercase_text_p}-{i}.png"
    else:
        filename_out = f"{OUTPUT_IMAGE_DIR}/out-colormap-pond-{lowercase_text_horiz}{lowercase_text_vert}{lowercase_text_p}-{i}.png"
    
    filename = sim_parameters.filename_out
    
    data = np.fromfile(filename, dtype=np.float64).reshape(-1, 16)
    
    x = data[:, axis_horiz + 1] / r
    y = data[:, axis_vert + 1] / r
    c = data[:, axis_p + 13]
    
    plt.figure(figsize=(10,10))
    plt.scatter(x, y, c=c, marker='s', s=square_size, cmap='RdBu_r')
    plt.xlim(r_min / wavelength, r_max / wavelength)
    plt.ylim(r_min / wavelength, r_max / wavelength)
    plt.xlabel(rf"{axis_text_horiz} [$\lambda$]")
    plt.ylabel(rf"{axis_text_vert} [$\lambda$]")
    plt.title(rf"Final $p_{lowercase_text_p}$ for ({method}) mode")
    cbar = plt.colorbar()
    cbar.set_label(rf"Final $p_{lowercase_text_p}$ [a.u.]")
    plt.savefig(filename_out, dpi=250, bbox_inches='tight')
    plt.close()
        
    print(f"Created colormap.")

# ----------------------------------------------------------------------- #

def plot_phases(method, sim_parameters, a0_array, axis_pos, axis_p):
    axis_text_pos = common.get_axis_text(axis_pos)
    lowercase_text_pos = axis_text_pos.lower()
    
    axis_text_p = common.get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    i = sim_parameters.i
    a0 = a0_array[i]
    num = sim_parameters.num
    r_min = sim_parameters.r_min
    r_max = sim_parameters.r_min
    wavelength = sim_parameters.wavelength
    steps = sim_parameters.steps // sim_parameters.substeps
    full_trajectory = sim_parameters.full_trajectory
    divider = sim_parameters.divider
    subsection = num // divider
    
    if(method == "electromagnetic"):
        filename_out = f"{OUTPUT_IMAGE_DIR}/out-phase-space-electromag-{lowercase_text_pos}{lowercase_text_p}-{i}.png"
        filename_exit = f"{OUTPUT_DIR}/out-enter-exit-time-electromag-{lowercase_text_pos}{lowercase_text_p}.bin"
    else:
        filename_out = f"{OUTPUT_IMAGE_DIR}/out-phase-space-pond-{lowercase_text_pos}{lowercase_text_p}-{i}.png"
        filename_exit = f"{OUTPUT_DIR}/out-enter-exit-time-pond-{lowercase_text_pos}{lowercase_text_p}.bin"
    filename = sim_parameters.filename_out
    
    data = np.fromfile(filename, dtype=np.float64).reshape(num, steps, 8)
    if(not full_trajectory):
        data_exit = np.fromfile(filename_exit, dtype=np.float64).reshape(num, 4)
        data_exit = data_exit[:subsection]
    
    fig, ax = plt.subplots(figsize=(10, 10), dpi=250)
    colmap = plt.get_cmap('Spectral')
    
    data = data[:subsection]
    
    for idx in range(subsection):
        if(full_trajectory):
            last_step = steps
        else:
            last_step = int(data_exit[idx, 3])
        traj = data[idx]
        traj = traj[:last_step]
        color = idx / subsection
        color_cmap = colmap(color)
        
        x = traj[:, axis_pos + 1] / wavelength
        y = traj[:, axis_p + 5]
        
        sc = ax.plot(x, y, c=color_cmap, linewidth=0.5)
        
    ax.set_title(f"Phase space: $a_0 = {a0:0.3f}$ - $N = {subsection}$")
    ax.set_xlabel(rf"${axis_text_pos}$ [$\lambda$]")
    ax.set_ylabel(rf"$p_{axis_text_p}$ [a.u.]")
    
    plt.xlim(r_min / wavelength - 2.0 * r_min / wavelength, r_max / wavelength + 2.0 * r_max / wavelength)
    
    plt.savefig(filename_out, bbox_inches='tight')
    plt.close()
    
    print(f"Created phase plot.")
    
# ----------------------------------------------------------------------- #

def plot_time_momentum(method, sim_parameters, a0_array, axis_pos, axis_p):
    axis_text_pos = common.get_axis_text(axis_pos)
    lowercase_text_pos = axis_text_pos.lower()
    
    axis_text_p = common.get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    i = sim_parameters.i
    a0 = a0_array[i]
    num = sim_parameters.num
    r_min = sim_parameters.r_min
    r_max = sim_parameters.r_min
    divider = sim_parameters.divider
    c_value = sim_parameters.c_value
    wavelength = sim_parameters.wavelength
    full_trajectory = sim_parameters.full_trajectory
    steps = sim_parameters.steps // sim_parameters.substeps
    
    if(method == "electromagnetic"):
        filename_out = f"{OUTPUT_IMAGE_DIR}/out-time-momentum-electromag-{lowercase_text_pos}{lowercase_text_p}-{i}.png"
        filename_exit = f"{OUTPUT_DIR}/out-enter-exit-time-electromag-{lowercase_text_pos}{lowercase_text_p}.bin"
    else:
        filename_out = f"{OUTPUT_IMAGE_DIR}/out-time-momentum-pond-{lowercase_text_pos}{lowercase_text_p}-{i}.png"
        filename_exit = f"{OUTPUT_DIR}/out-enter-exit-time-pond-{lowercase_text_pos}{lowercase_text_p}.bin"
    filename = sim_parameters.filename_out
    
    data = np.fromfile(filename, dtype=np.float64).reshape(num, steps, 8)
    data_exit = np.fromfile(filename_exit, dtype=np.float64).reshape(num, 4)
    fig, ax = plt.subplots(figsize=(10, 10), dpi=250)
    
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
        
        x = traj[:, 0] / c_value
        y = traj[:, axis_p + 5]
        
        sc = ax.plot(x, y, c=color_cmap, linewidth=0.5)
        
    ax.set_title(f"Time - momentum plot for: $a_0 = {a0:0.3f}$ - $N = {subsection}$")
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(rf"$p_{lowercase_text_p}$ [a.u.]")
    
    plt.savefig(filename_out, bbox_inches='tight')
    plt.close()
    
    print(f"Created time-momentum plot.")
    
# ----------------------------------------------------------------------- #

def plot_2d_heatmap_all(method, sim_parameters, a0_array, axis_pos, axis_p):
    axis_text_pos = common.get_axis_text(axis_pos)
    lowercase_text_pos = axis_text_pos.lower()
    
    axis_text_p = common.get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    num = sim_parameters.num
    r_min = sim_parameters.r_min
    r_max = sim_parameters.r_max
    wavelength = sim_parameters.wavelength
    sweep_steps = sim_parameters.sweep_steps
    
    if(method == "electromagnetic"):
        filename_in = f"{OUTPUT_DIR}/out-final-p{lowercase_text_p}-all-electromag.bin"
        filename_in_max_p = f"{OUTPUT_DIR}/out-max-p{lowercase_text_p}-electromag.bin"
        filename_out = f"{OUTPUT_IMAGE_DIR}/_out-2d-heatmap-electromag-{lowercase_text_pos}{lowercase_text_p}.png"
    else:
        filename_in = f"{OUTPUT_DIR}/out-final-p{lowercase_text_p}-all-pond.bin"
        filename_in_max_p = f"{OUTPUT_DIR}/out-max-p{lowercase_text_p}-pond.bin"
        filename_out = f"{OUTPUT_IMAGE_DIR}/_out-2d-heatmap-pond-{lowercase_text_pos}{lowercase_text_p}.png"
    
    data = np.fromfile(filename_in, dtype=np.float64).reshape(sweep_steps, num, 2)
    data_max_p = np.fromfile(filename_in_max_p, dtype=np.float64).reshape(sweep_steps, 1)
    
    x = data[:, :, 0] / wavelength
    y = np.repeat(a0_array[:, np.newaxis], num, axis=1)
    max_py = data_max_p[:, 0][:, np.newaxis]
    z = data[:, :, 1] / max_py
    fig, ax = plt.subplots(figsize=(10, 10), dpi=250)
    
    with warnings.catch_warnings(record=True) as warn:
        warnings.simplefilter("always")
        pcm = ax.pcolormesh(x, y, z, cmap='RdBu_r', shading='auto', rasterized=True)
    
    cbar = plt.colorbar(pcm, ax=ax)
    cbar.set_label(f"Normalized final momentum [a.u.]")
    
    plt.xlim(r_min / wavelength, r_max / wavelength)
    plt.ylim(min(a0_array), max(a0_array))
    plt.xlabel(rf"{axis_text_pos} [$\lambda$]")
    plt.ylabel(r"$a_0$")
    plt.title(f"Final $p_{lowercase_text_p}$ heatmap for ({method})")
    
    plt.savefig(filename_out, dpi=250, bbox_inches='tight')
    plt.close()
    
    print(f"Created 2D heatmap of full {method} parameter sweep.")

# ----------------------------------------------------------------------- #

def plot_2d_errors_heatmap(sim_parameters, a0_array, axis_pos, axis_p):
    axis_text_pos = common.get_axis_text(axis_pos)
    lowercase_text_pos = axis_text_pos.lower()
    
    axis_text_p = common.get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    num = sim_parameters.num
    r_min = sim_parameters.r_min
    r_max = sim_parameters.r_max
    wavelength = sim_parameters.wavelength
    sweep_steps = sim_parameters.sweep_steps
    
    filename_in = f"{OUTPUT_DIR}/out-error-all-{lowercase_text_p}.bin"
    filename_in_max_p = f"{OUTPUT_DIR}/out-max-p{lowercase_text_p}-electromag.bin"
    filename_out = f"{OUTPUT_IMAGE_DIR}/_out-2d-heatmap-errors-{lowercase_text_pos}{lowercase_text_p}.png"
    
    data = np.fromfile(filename_in, dtype=np.float64).reshape(sweep_steps, num, 2)
    data_max_p = np.fromfile(filename_in_max_p, dtype=np.float64).reshape(sweep_steps, 1)
    
    difference = data[:, :, 1]
    x = data[:, :, 0] / wavelength
    y = np.repeat(a0_array[:, np.newaxis], num, axis=1)
    max_p = data_max_p[:, 0][:, np.newaxis]
    z = difference / max_p * 100.0
    
    row_max = np.max(z, axis=1)[:, np.newaxis]
    z_final = z / row_max * 100.0
    
    fig, ax = plt.subplots(figsize=(10, 10), dpi=250)
    with warnings.catch_warnings(record=True) as warn:
        warnings.simplefilter("always")
        pcm = ax.pcolormesh(x, y, z_final, cmap='inferno', shading='auto', rasterized=True)
    
    cbar = plt.colorbar(pcm, ax=ax)
    cbar.set_label("Normalized error [%]")
    
    plt.xlim(r_min / wavelength, r_max / wavelength)
    plt.ylim(min(a0_array), max(a0_array))
    plt.xlabel(rf"{axis_text_pos} [$\lambda$]")
    plt.ylabel(r"$a_0$")
    plt.title(rf"Full error heatmap for $p_{lowercase_text_p}$")
    
    plt.savefig(filename_out, dpi=250, bbox_inches='tight')
    plt.close()
    
    print(f"Created 2D error heatmap.")

# ----------------------------------------------------------------------- #

def plot_enter_exit_time(method, sim_parameters, a0_array, axis_pos, axis_p):
    axis_text_pos = common.get_axis_text(axis_pos)
    lowercase_text_pos = axis_text_pos.lower()
    
    axis_text_p = common.get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    r = sim_parameters.r
    num = sim_parameters.num
    i = sim_parameters.i
    a0 = a0_array[i]
    steps = sim_parameters.steps // sim_parameters.substeps
    
    if method == "electromagnetic":
        mode = 0
        filename_enter_exit_time = f"{OUTPUT_DIR}/out-enter-exit-time-electromag-{lowercase_text_pos}{lowercase_text_p}.bin"
        filename_out = f"{OUTPUT_IMAGE_DIR}/out-enter-exit-time-electromag-{lowercase_text_pos}{lowercase_text_p}-{i}.png"
    else:
        mode = 1
        filename_enter_exit_time = f"{OUTPUT_DIR}/out-enter-exit-time-electromag-{lowercase_text_pos}{lowercase_text_p}.bin"
        filename_out = f"{OUTPUT_IMAGE_DIR}/out-enter-exit-time-pond-{lowercase_text_pos}{lowercase_text_p}-{i}.png"
    
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
    plt.xlabel(rf"{axis_text} [$\lambda$]")
    plt.ylabel(f"t")
    
    plt.axhline(0, color='black', linestyle='--')

    plt.savefig(filename_out, dpi=250, bbox_inches='tight')
    plt.close()

    print(f"Created enter exit time plot.")

# ----------------------------------------------------------------------- #

def plot_max_p(method, a0_array, axis):
    axis_text = common.get_axis_text(axis)
    lowercase_text = axis_text.lower()
    
    if(method == "electromagnetic"):
        filename = f"{OUTPUT_DIR}/out-max-p{lowercase_text}-electromag.bin"
        filename_out = f"{OUTPUT_IMAGE_DIR}/_out-max-p{lowercase_text}-electromag.png"
    else:
        filename = f"{OUTPUT_DIR}/out-max-p{lowercase_text}-pond.bin"
        filename_out = f"{OUTPUT_IMAGE_DIR}/_out-max-p{lowercase_text}-pond.png"
    
    data = np.fromfile(filename, dtype=np.float64).reshape(-1, 1)
    
    x = a0_array
    y = data[:, 0]
    
    plt.figure(figsize=(10,10))
    plt.plot(x, y, c='black', linestyle='-', linewidth=1)
    plt.title(rf"max($p_{lowercase_text}$) ({method})")
    plt.xlabel(r"$a_0$")
    plt.ylabel(rf"max($p_{lowercase_text}$)")
    
    plt.axhline(0, color='black', linestyle='--')
    
    plt.savefig(filename_out, dpi=250, bbox_inches='tight')
    plt.close()
    
    print(f"Created max(p) scatter plot for {method} mode.")
    
# ----------------------------------------------------------------------- #    

def plot_average_errors(a0_array, axis):
    axis_text = common.get_axis_text(axis)
    lowercase_text = axis_text.lower()
    
    filename = f"{OUTPUT_DIR}/out-average-error-{lowercase_text}.bin"
    filename_max_p = f"{OUTPUT_DIR}/out-max-p{lowercase_text}-electromag.bin"
    
    data = np.fromfile(filename, dtype=np.float64).reshape(-1, 2)
    data2 = np.fromfile(filename_max_p, dtype=np.float64).reshape(-1, 1)
    
    x = np.array(a0_array)
    y = data[:, 1]
    y_max = data2[:, 0]
    
    y_final = y / y_max * 100
    
    plt.figure(figsize=(10,10))
    plt.plot(x, y_final, c='black', linestyle='-', linewidth=1)
    plt.title(f"Average errors on {axis_text} axis")
    plt.xlabel(r"$a_0$")
    plt.ylabel(r"<$\epsilon$> (%)")
    
    plt.axhline(0, color='black', linestyle='--')
    
    filename_out = f"{OUTPUT_IMAGE_DIR}/_out-average-errors-{lowercase_text}.png"
    plt.savefig(filename_out, dpi=250, bbox_inches='tight')
    plt.close()
    
    print(f"Created average error scatter plot.")

# ----------------------------------------------------------------------- #