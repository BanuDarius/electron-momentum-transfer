import os
import sys
import numpy as np
import matplotlib.pyplot as plt

wavelength = 2 * 3.141592 * 137.036 / 0.057
waveCount = 2
num = 50

def plot_slope(filename):
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
    
def exp_graph(filename):
    data = np.loadtxt(filename)

    x = data[:, 1]
    y = data[:, 2]
    z = data[:, 3]
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(x, y, z, c=z, cmap='viridis', s=1, alpha=0.7)
    
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_zlabel('$z$')
    ax.set_title(f'N = {num}')

    num_frames = 60
    for i in range(num_frames):
        angle = (360 / num_frames) * i
        
        ax.view_init(elev=30, azim=angle)
        plt.savefig(f"frame-{i:02d}.png", dpi=150, bbox_inches='tight')
        print(f"Saved image: {i}")

    plt.close(fig)

def create_plot(filename, a0, i):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
    
    line_data = np.loadtxt("out-file.txt")
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
    
    axes[1].set_title(f'(Ponderomotive) a0 = {a0:0.3f}')
    axes[1].set_xlim(-waveCount, waveCount)
    axes[1].set_ylim(-waveCount, waveCount)
    axes[1].set_xlabel('Y [λ]')
    axes[1].set_ylabel('Z [λ]')
    axes[1].set_aspect('equal', adjustable='box')

    imageFilename = f"out-{i}.png"
    plt.savefig(imageFilename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Output image {imageFilename}")
    os.remove(filename)

if __name__ == "__main__":
    try:
        os.remove("out-deriv.txt")
    except OSError:
        pass

    for i in range(0, 1):
        a0 = 0.010 + i / 250.0
        scale = waveCount * wavelength
        filename = f"out-{a0:0.3f}.bin"
        os.system(f"./LaserElectron {a0:0.3f} {num} {waveCount}")
        os.system(f"./DataAnalyst {filename} {num} {waveCount} {a0:0.3f}")
        #create_plot(filename, a0, i)
        exp_graph(filename)
    #plot_slope("out-deriv.txt")
    #os.remove("out-file.txt")
    
    print(f"Program executed successfully. \a")