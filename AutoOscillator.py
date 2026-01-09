import os
import sys
import numpy as np
import matplotlib.pyplot as plt

filename = "out.bin"
wavelength = 2 * 3.141592 * 137.036 / 0.057
num = 1024

def exp_graph_fused_py(filename, a0, i):
    raw_data = np.fromfile(filename, dtype=np.float64)
    data = raw_data.reshape(-1, 3)

    subset_num = int(num / 8)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10), dpi=150)
    
    steps = 4096
    t_data_raw = data[:, 0]
    y_data_raw = data[:, 1] / wavelength
    py_data_raw = data[:, 2]
    
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

    ax1.set_title(f"(Potential) a0 = {a0:0.3f} - N = {subset_num}")
    ax1.set_xlabel('ct')
    ax1.set_ylabel(r"$p_y$")

    ax2.set_title(f"(Potential) a0 = {a0:0.3f} - N = {subset_num}")
    ax2.set_xlim(-1.1, 1.1)
    ax2.set_xlabel(r"y [λ]")
    ax2.set_ylabel(r"$p_y$")

    filename_out = f"graph-combined-potential-{i:03d}.png"
    plt.savefig(filename_out, bbox_inches='tight')
    plt.close()
    
    print(f"Saved plot: {filename_out}")
    
if __name__ == '__main__':
    for i in range(0, 100):
        a0 = 0.001 + i / 500.0
        os.system(f"./Oscillator {a0:0.3f} {num}")
        exp_graph_fused_py(filename, a0, i)
    print(f"Program executed successfully. \a")
    os.remove(filename)