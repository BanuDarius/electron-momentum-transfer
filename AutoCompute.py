import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def create_plot(filename, a0, i):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
    data_column = np.loadtxt(filename, usecols=(14))
    
    axes[0].hist(data_column, bins=150, edgecolor='black')
    axes[0].set_title(f'a0 = {a0:0.3f}')
    axes[0].set_xlim(-30, 30)
    axes[0].set_ylim(0, 1100)
    axes[0].set_xlabel('p_y')
    axes[0].set_ylabel('N')

    data = np.loadtxt(filename, usecols=(2, 3, 14))
    wavelength = 2 * 3.141592 * 137.036 / 0.057
    x = data[:, 0] / wavelength
    y = data[:, 1] / wavelength
    c = data[:, 2]  # This is p_y (column 14)
    sc = axes[1].scatter(x, y, c=c, cmap='bwr', s=5)
    
    #fig.colorbar(sc, ax=axes[1], label='p_y')
    
    axes[1].set_title(f'a0 = {a0:0.3f}')
    axes[1].set_xlim(-2, 2)
    axes[1].set_ylim(-2, 2)
    axes[1].set_xlabel('Y [λ]')
    axes[1].set_ylabel('Z [λ]')
    axes[1].set_aspect('equal', adjustable='box')

    imageFilename = f"out-{i}.png"
    plt.savefig(imageFilename, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Output image {imageFilename}")

for i in range(0, 50):
    a0 = 0.01 + i / 250
    filename = f"out-{a0:0.3f}.txt"
    os.system(f"LaserElectron {a0:0.3f}")
    create_plot(filename, a0, i)
    os.remove(filename)