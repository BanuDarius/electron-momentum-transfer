import os
import sys
import numpy as np
import matplotlib.pyplot as plt

wavelength = 2 * 3.141592 * 137.036 / 0.057
scaleFactor = 3
num = 32000

'''def create_plot(filename, a0, i):
    fig, ax = plt.subplots(figsize=(10, 10))
    
    data = np.loadtxt(filename)
    normalizeY = np.abs(np.min(data[:, 1]))
    x = data[:, 0]
    y = data[:, 1]
    
    ax.scatter(x, y, s=0.2)
    y0 = (2.0 * i * wavelength / 200 - wavelength) / wavelength 
    ax.set_title(f'a0 = {a0:0.3f}, y0 = {y0:0.3f} [λ]')
    ax.set_xlabel('t')
    ax.set_ylabel('A^2')
    ax.set_xlim(0, 10000)
    ax.set_ylim(-1000, 0.1)
    ax.set_box_aspect(1)
    ax.set_aspect('auto')

    imageFilename = f"out-{i}.png"
    plt.savefig(imageFilename, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Output image {imageFilename}")'''


def create_plot(filename, a0, i):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
    
    line_data = np.loadtxt("out-file.txt")
    wavelength = 2 * 3.141592 * 137.036 / 0.057
    x = line_data[:, 0] / wavelength
    y = line_data[:, 1]
    
    axes[0].plot(x, y, '-', linewidth=1, markersize=4)
    axes[0].set_title(f'Ponderomotive - a0 = {a0:0.3f}')
    axes[0].set_xlim(-scaleFactor, scaleFactor)
    axes[0].set_xlabel('Y [λ]')
    axes[0].set_ylabel('p_y')
    axes[0].axhline(y=0, color='black', linestyle='--', linewidth=1)

    data = np.loadtxt(filename, usecols=(2, 3, 14))

    x = data[:, 0] / wavelength
    y = data[:, 1] / wavelength
    c = data[:, 2]  # p_y (column 14)
    
    sc = axes[1].scatter(x, y, c=c, cmap='bwr', s=5)
    
    # fig.colorbar(sc, ax=axes[1], label='p_y')
    
    axes[1].set_title(f'Ponderomotive - a0 = {a0:0.3f}')
    axes[1].set_xlim(-scaleFactor, scaleFactor)
    axes[1].set_ylim(-scaleFactor, scaleFactor)
    axes[1].set_xlabel('Y [λ]')
    axes[1].set_ylabel('Z [λ]')
    axes[1].set_aspect('equal', adjustable='box')

    imageFilename = f"out-{i}.png"
    plt.savefig(imageFilename, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Output image {imageFilename}")

for i in range(0, 200):
    a0 = 0.010 + i / 1000
    scale = scaleFactor * wavelength
    filename = f"out-{a0:0.3f}.txt"
    os.system(f"./LaserElectron {a0:0.3f} {i}")
    os.system(f"./OutputFormatter {filename} {num} {scale:0.3f}")
    create_plot(filename, a0, i)
    os.remove(filename)