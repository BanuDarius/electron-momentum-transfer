import os
import sys
import numpy as np
import matplotlib.pyplot as plt

i = 1
for a0 in np.arange(0.50, 0.51, 0.05):
    os.system(f"LaserElectron.exe {a0:0.3f}")
    '''data = None
    data = np.loadtxt(f"out-{a0:0.3f}.txt", usecols=(2, 3, 13))
    x, y, color = data[:, 0], data[:, 1], data[:, 2]
    cMin = np.min(color)
    cMax = np.max(color)
    if cMax > abs(cMin):
        cMax = -cMin
    else:
        cMin = -cMax
    normColor = np.clip(color, cMin, cMax)
    plt.figure(figsize=(10, 10))
    plt.scatter(x, y, s = 2, c = color, cmap="gray", alpha=0.7)
    plt.xlim(-20000, 20000)
    plt.ylim(-20000, 20000)
    plt.title(f"Exact method - px - a0 = {a0:0.3f}")
    plt.xlabel("Y")
    plt.ylabel("Z")
    plt.axis('equal')
    plt.colorbar()
    plt.savefig(f"out-px-{i}.png", dpi=100)
    print(f"Image saved: out-px-{i}.png")
    plt.close()'''
    
    data = np.loadtxt(f"out-{a0:0.3f}.txt", usecols=(2, 3, 14))
    x, y, color = data[:, 0], data[:, 1], data[:, 2]
    cMin = np.min(color)
    cMax = np.max(color)
    if cMax > abs(cMin):
        cMax = -cMin
    else:
        cMin = -cMax
    normColor = np.clip(color, cMin, cMax)
    plt.figure(figsize=(10, 10))
    plt.scatter(x, y, s = 2, c = normColor, cmap="bwr", alpha=0.7)
    plt.xlim(-20000, 20000)
    plt.ylim(-20000, 20000)
    plt.title(f"Ponderomotive a0 = {a0:0.3f} max(p) = {np.max(color):0.3f}")
    plt.xlabel("Y")
    plt.ylabel("Z")
    plt.axis('equal')
    plt.colorbar()
    plt.savefig(f"out-py-ponderomotive-{i}.png", dpi=100)
    print(f"Image saved: out-py-{i}.png")
    plt.close()
    
    '''data = np.loadtxt(f"out-{a0:0.3f}.txt", usecols=(2, 3, 15))
    x, y, color = data[:, 0], data[:, 1], data[:, 2]
    cMin = np.min(color)
    cMax = np.max(color)
    if cMax > abs(cMin):
        cMax = -cMin
    else:
        cMin = -cMax
    normColor = np.clip(color, cMin, cMax)
    plt.figure(figsize=(10, 10))
    plt.scatter(x, y, s = 2, c = color, cmap="bwr", alpha=0.7)
    plt.xlim(-20000, 20000)
    plt.ylim(-20000, 20000)
    plt.title(f"Exact method - pz - a0 = {a0:0.3f}")
    plt.xlabel("Y")
    plt.ylabel("Z")
    plt.axis('equal')
    plt.colorbar()
    plt.savefig(f"out-pz-{i}.png", dpi=100)
    print(f"Image saved: out-pz-{i}.png")
    plt.close()'''
    os.remove(f"out-{a0:0.3f}.txt")
    i+=1