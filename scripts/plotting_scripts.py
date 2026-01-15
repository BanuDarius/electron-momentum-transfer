import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BIN_DIR = PROJECT_ROOT / "bins"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_IMAGE_DIR = PROJECT_ROOT / "output-image"

def plot_2d_colormap(method, a0, xif, tauf, i, wavelength, waveCount, num, steps):
    if(method == "electromagnetic"):
        mode = 0
    else:
        mode = 1
    outputMode = 1 #Always output the final state
    programPath = BIN_DIR/"laser_electron"
    os.system(f"{programPath} {mode} {outputMode} {a0:0.3f} {num} {steps} {waveCount} {xif:0.3f} {tauf:0.3f}")

    filename = f"{OUTPUT_DIR}/out-data.bin"
    data = np.fromfile(filename, dtype=np.float64).reshape(-1, 16)
    
    x = data[:, 2] / wavelength
    y = data[:, 3] / wavelength
    c = data[:, 14]

    plt.figure(figsize=(10,10))
    plt.scatter(x, y, c=c, s=3, cmap='RdBu_r')
    plt.xlim(-waveCount, waveCount)
    plt.ylim(-waveCount, waveCount)
    plt.xlabel(r"Y [$\lambda$]")
    plt.ylabel(r"Z [$\lambda$]")
    plt.title(f"a0 = {a0:0.3f}")
    filenameOut = f"{OUTPUT_IMAGE_DIR}/out-colormap-{i}.png"
    plt.savefig(filenameOut, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Created colormap for a0 = {a0:0.3f}.")
    if(mode == 0):
        os.rename(filenameOut, f"{OUTPUT_IMAGE_DIR}/out-colormap-electromag-{i}.png")
    else:
        os.rename(filenameOut, f"{OUTPUT_IMAGE_DIR}/out-colormap-pond-{i}.png")


def plot_phases(method, a0, xif, tauf, i, wavelength, waveCount, num, steps):
    if method == "electromagnetic":
        mode = 0
    else:
        mode = 1
    outputMode = 0 #Always output the full state
    programPath = BIN_DIR/"laser_electron"
    os.system(f"{programPath} {mode} {outputMode} {a0:0.3f} {num} {steps} {waveCount} {xif:0.3f} {tauf:0.3f}")

    filename = f"{OUTPUT_DIR}/out-data.bin"
    data = np.fromfile(filename, dtype=np.float64).reshape(num, steps, 8)
    fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
    time_indices = np.arange(steps)
    
    for idx in range(num):
        traj = data[idx]
        
        x = traj[:, 2] / wavelength
        y = traj[:, 6]
        
        sc = ax.scatter(x, y, c=time_indices, cmap='viridis', s=0.5)

    ax.set_title(f"Phase space: $a_0 = {a0:0.3f}$ - $N = {num}$")
    ax.set_xlabel(r"$y$ [$\lambda$]")
    ax.set_ylabel(r"$p_y$")
    
    ax.set_xlim(-1.1 * waveCount, 1.1 * waveCount)
    
    filenameOut = f"{OUTPUT_IMAGE_DIR}/out-phase-space-{i}.png"
    plt.savefig(filenameOut, bbox_inches='tight')
    plt.close()
    if(mode == 0):
        os.rename(filenameOut, f"{OUTPUT_IMAGE_DIR}/out-phase-space-electromag-{i}.png")
    else:
        os.rename(filenameOut, f"{OUTPUT_IMAGE_DIR}/out-phase-space-pond-{i}.png")
    
    print(f"Created phase plot for a0 = {a0:0.3f}.")
    
def plot_phases_oscillator(a0, i, num, wavelength, waveCount):
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
    
    ax.set_xlim(-1.1 * waveCount, 1.1 * waveCount)

    filenameOut = f"{OUTPUT_IMAGE_DIR}/out-phase-space-potential-{i}.png"
    
    plt.savefig(filenameOut, bbox_inches='tight')
    plt.close()
    
    print(f"Created potential phase plot for a0 = {a0:0.3f}.")


def plot_enter_exit_time(method, a0, i, wavelength, num, steps):
    if method == "electromagnetic":
        mode = 0
    else:
        mode = 1
    filename = f"{OUTPUT_DIR}/out-data.bin"
    programPath = f"{BIN_DIR}/find_enter_exit_time"
    enterExitTimePath = f"{OUTPUT_DIR}/out-enter-exit-time.bin"
    os.system(f"{programPath} {filename} {num} {steps}")
    data = np.fromfile(enterExitTimePath, dtype=np.float64).reshape(-1, 3)
    
    x = data[:, 0] / wavelength
    y1 = data[:, 1] / 137.036
    y2 = data[:, 2] / 137.036
    
    plt.figure(figsize=(10,10))
    plt.plot(x, y1, linestyle='-', linewidth=1)
    plt.plot(x, y2, linestyle='-', linewidth=1)
    plt.title(f"Exit time for $a_0$ = {a0:0.3f}")
    plt.xlabel(r"$y$ [$\lambda$]")
    plt.ylabel(f"t")
    
    plt.axhline(0, color='black', linestyle='--')
    
    filenameOut = f"{OUTPUT_IMAGE_DIR}/out-enter-exit-time-{i}.png"
    plt.savefig(filenameOut, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Created enter and exit time scatter plot for a0 = {a0:0.3f}.")
    if(mode == 0):
        os.rename(filenameOut, f"{OUTPUT_IMAGE_DIR}/out-enter-exit-time-electromag-{i}.png")
    else:
        os.rename(filenameOut, f"{OUTPUT_IMAGE_DIR}/out-enter-exit-time-pond-{i}.png")

def analyze_data(method, outputMaxP, outputExitTime, a0, waveCount, num):
    filename= f"{OUTPUT_DIR}/out-data.bin"
    filenameOut = f"{OUTPUT_DIR}/out-stats.bin"
    outputMaxP = int(outputMaxP == True)
    outputExitTime = int(outputExitTime == True)
    programPath = f"{BIN_DIR}/data_analyst"
    os.system(f"{programPath} {filename} {num} {waveCount} {a0:0.3f} {outputMaxP} {outputExitTime}")
    if(method == "electromagnetic"):
        os.rename(filenameOut, f"{OUTPUT_DIR}/out-stats-1.bin")
    else:
        os.rename(filenameOut, f"{OUTPUT_DIR}/out-stats-2.bin")

def plot_errors(a0, i, wavelength, num):
    filename = f"{OUTPUT_DIR}/out-error.bin"
    filenameMaxPy = f"{OUTPUT_DIR}/out-max-py.bin"
    programPath = f"{BIN_DIR}/error_calculator"
    os.system(f"{programPath} {a0:0.3f}")
    data = np.fromfile(filename, dtype=np.float64).reshape(-1, 2)
    data2 = np.fromfile(filenameMaxPy, dtype=np.float64).reshape(-1, 2)
    
    x = data[:, 0] / wavelength
    y = data[:, 1]
    
    yMax = data2[i, 1]
    print(f"For a0 = {a0:0.3f}, yMax = {yMax:0.3f}")
    
    yFinal = y / yMax * 100
    
    plt.figure(figsize=(10,10))
    plt.plot(x, yFinal, linestyle='-', linewidth=1)
    plt.title(f"Errors for a0 = {a0:0.3f}")
    plt.xlabel(r"Y [$\lambda$]")
    plt.ylabel(f"Error (%)")
    
    plt.axhline(0, color='black', linestyle='--')
    
    filenameOut = f"{OUTPUT_IMAGE_DIR}/out-errors-{i}.png"
    plt.savefig(filenameOut, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Created error scatter plot for a0 = {a0:0.3f}.")

def plot_max_py(a0, i):
    filename = f"{OUTPUT_DIR}/out-max-py.bin"
    data = np.fromfile(filename, dtype=np.float64).reshape(-1, 2)
    
    x = data[:, 0]
    y = data[:, 1]
    
    plt.figure(figsize=(10,10))
    plt.plot(x, y, linestyle='-', linewidth=1)
    plt.title(r"max($p_y$)")
    plt.xlabel(r"$a_0$")
    plt.ylabel(r"max($p_y$)")
    
    plt.axhline(0, color='black', linestyle='--')
    
    filenameOut = f"{OUTPUT_IMAGE_DIR}/out-max-py.png"
    plt.savefig(filenameOut, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Created max(py) scatter plot for a0 = {a0:0.3f}.")
    
def plot_average_errors(a0, i):
    filename = f"{OUTPUT_DIR}/out-average-error.bin"
    data = np.fromfile(filename, dtype=np.float64).reshape(-1, 2)
    
    x = data[:, 0]
    y = data[:, 1]
    
    plt.figure(figsize=(10,10))
    plt.plot(x, y, linestyle='-', linewidth=1)
    plt.title(r"Average errors")
    plt.xlabel(r"$a_0$")
    plt.ylabel(r"<$\epsilon$> (%)")
    
    plt.axhline(0, color='black', linestyle='--')
    
    filenameOut = f"{OUTPUT_IMAGE_DIR}/out-average-errors.png"
    plt.savefig(filenameOut, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Created average error scatter plot.")
    

'''def plot_slope(filename):
    n = 2 * waveCount
    data = np.loadtxt(filename)
    
    x = data[:, 0]
    
    plt.figure(figsize=(10, 10))
    
    for i in range(1, n + 1):
        y = data[:, i]
        plt.plot(x, y, '-', linewidth=1, label=f'Node {i}')
        
    plt.title(f'Slope of dpy/dy in node points')
    plt.xlabel('a0')
    plt.ylabel('dpy/dy')
    
    plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
    
    plt.legend()
    
    plt.savefig("slope.png", dpi=150, bbox_inches='tight')
    print("Slope plot completed")
    os.remove("out-deriv.txt")
    
def exp_graph_fused_py(filename, a0, i, num, wavelength, steps):
    steps = int(steps)
    raw_data = np.fromfile(filename, dtype=np.float64)
    data = raw_data.reshape(-1, 8)

    subset_num = int(num / 8)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10), dpi=150)
    t_data_raw = data[:, 0] / 137.036
    y_data_raw = data[:, 2] / wavelength
    py_data_raw = data[:, 6]
    
    t = t_data_raw.reshape(-1, steps)
    py = py_data_raw.reshape(-1, steps)
    y = y_data_raw.reshape(-1, steps)

    ax1.axhline(y=0, color='black', linestyle='--', linewidth=0.5)

    limit = min(t.shape[0], subset_num)
    
    cmap = plt.get_cmap('coolwarm') 

    for p in range(limit):
        fraction = p / max(limit - 1, 1)
        line_color = cmap(fraction)

        ax1.plot(t[p], py[p], linestyle='-', linewidth=0.5, color=line_color)
        current_y = y[p]
        current_py = py[p]

        mask = (abs(current_y) > 0.01) | (abs(current_py) > 0.01)

        ax2.plot(current_y[mask], current_py[mask], linestyle='-', linewidth=0.5, color=line_color)

    ax1.set_title(f"a0 = {a0:0.3f} - N = {subset_num}")
    ax1.set_xlabel('ct')
    ax1.set_ylabel(r"$p_y$")

    ax2.set_title(f"a0 = {a0:0.3f} - N = {subset_num}")
    ax2.set_xlim(-1.1, 1.1)
    ax2.set_xlabel(r"y [λ]")
    ax2.set_ylabel(r"$p_y$")

    filename_out = f"graph-combined-{i:03d}.png"
    plt.savefig(filename_out, bbox_inches='tight')
    plt.close()
    
    print(f"Saved plot: {filename_out}")
    
def exp_graph_scatter(filename, a0, i):
    raw_data = np.fromfile(filename, dtype=np.float64)
    data = raw_data.reshape(-1, 8)
    plt.figure(figsize=(10, 5), dpi=200)

    t_data = data[:, 0]
    y_data = data[:, 6]

    steps = 4096
    t = t_data.reshape(-1, steps)
    Y = y_data.reshape(-1, steps)
    

    plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
    for p in range(t.shape[0]):
        plt.plot(t[p], Y[p], linestyle='-', linewidth=1)
    plt.title(f"a0 = {a0:0.3f} - N = {num}")
    plt.xlabel('ct')
    plt.ylabel('py')
    
    plt.savefig(f"graph-scatter-{i:03d}.png", bbox_inches='tight')
    plt.close()
    
def exp_graph_2d(filename, a0, i):
    raw_data = np.fromfile(filename, dtype=np.float64)
    data = raw_data.reshape(-1, 8)

    t_data = data[:, 0] / 137.036
    x_data = data[:, 2] / wavelength
    y_data = data[:, 6]
    final_index = int(num * 4096)
    x_data = x_data[0 : final_index]
    y_data = y_data[0 : final_index]
    t_data = t_data[0 : final_index]

    plt.figure(figsize=(10, 10), dpi=150)
    current_indices = np.arange(len(x_data))
    
    plt.scatter(x_data, y_data, c=t_data, cmap='coolwarm', s=1, alpha=1)
    plt.title(f"a0 = {a0:0.3f} - N = {num}")
    plt.xlim(-1.1, 1.1)
    plt.xlabel(r"y [λ]")
    plt.ylabel(r"$p_y$")
    filename_out = f"graph-phase-{i:03d}.png"
    plt.savefig(filename_out, bbox_inches='tight')
    plt.close()
    
    print(f"Successfully saved plot")

def exp_graph_2d_all(filename, a0, i):
    raw_data = np.fromfile(filename, dtype=np.float64)
    data = raw_data.reshape(-1, 8)
    
    for i in range(0, num):
        chunk_size = 4096
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size
        batch = data[start_idx : end_idx]

        x_data = batch[:, 2] / wavelength
        y_data = batch[:, 6]
        t = batch[:, 0] / 137.036

        plt.figure(figsize=(10, 10), dpi=150)
        
        plt.scatter(x_data, y_data, c=t, cmap='coolwarm', s=1, alpha=1)
        
        y0 = x_data[0]
        plt.title(f"y0 = {y0:0.3f} [λ]")
        max_py = max(y_data) * 1.1
        plt.ylim(-max_py, max_py)
        plt.xlabel(r"y [λ]")
        plt.ylabel(r"$p_y$")

        filename_out = f"frame-{i:03d}.png"
        plt.savefig(filename_out, bbox_inches='tight')
        plt.close()
        
        print(f"Saved {filename_out}")


def exp_graph_3d(filename, a0, i):
    raw_data = np.fromfile(filename, dtype=np.float64)
    data = raw_data.reshape(-1, 8)

    x = data[:, 1]
    y = data[:, 2]
    z = data[:, 3]
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(x, y, z, c=z, cmap='viridis', s=1)
    
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_zlabel('$z$')
    ax.set_title(f'N = {num}, a0 = {a0:0.3f}')

    num_frames = 1
    #for i in range(num_frames):
        #angle = (360 / num_frames) * i
        
    ax.view_init(elev=30, azim=0)
    plt.savefig(f"frame-{i:03d}.png", dpi=150, bbox_inches='tight')
    print(f"Saved image: {i}")

    plt.close(fig)

def create_plot(filename, a0, i):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
    
    raw_data = np.fromfile(filename, dtype=np.float64)
    line_data = raw_data.reshape(-1, 8)
    wavelength = 2 * 3.141592 * 137.036 / 0.057
    x = line_data[:, 0] / wavelength
    y = line_data[:, 1]
    
    axes[0].plot(x, y, '-', linewidth=1, markersize=3)
    axes[0].set_title(f'a0 = {a0:0.3f}')
    axes[0].set_xlim(-waveCount, waveCount)
    axes[0].set_xlabel('Y [λ]')
    axes[0].set_ylabel('p_y')
    axes[0].axhline(y=0, color='black', linestyle='--', linewidth=0.5)
    
    raw_data = np.fromfile(filename, dtype=np.float64)
    data_matrix = raw_data.reshape(-1, 16)
    data = data_matrix[:, [2, 3, 14]]

    x = data[:, 0] / wavelength
    y = data[:, 1] / wavelength
    c = data[:, 2]  # p_y (column 14)
    
    sc = axes[1].scatter(x, y, c=c, cmap='RdBu_r', s=6)
    
    # fig.colorbar(sc, ax=axes[1], label='p_y')
    
    axes[1].set_title(f'a0 = {a0:0.3f}')
    axes[1].set_xlim(-waveCount, waveCount)
    axes[1].set_ylim(-waveCount, waveCount)
    axes[1].set_xlabel('Y [λ]')
    axes[1].set_ylabel('Z [λ]')
    axes[1].set_aspect('equal', adjustable='box')

    imageFilename = f"out-{i}.png"
    plt.savefig(imageFilename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Output image {imageFilename}")'''
