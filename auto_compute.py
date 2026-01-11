import os
import sys
import plotting_scripts as psc

wavelength = 2 * 3.141592 * 137.036 / 0.057

num = 8000
stepsElectromagnetic = 4096
stepsPonderomotive = 512
waveCount = 1

if __name__ == "__main__":
    try:
        os.remove("out-deriv.txt")
        os.remove("out-max-py.txt")
    except OSError:
        pass
    for i in range(0, 20):
        a0 = 0.010 + i / 100.0
        filename = "out-data.bin"
        os.system(f"./laser_electron 0 1 {a0:0.3f} {num} {stepsElectromagnetic} {waveCount}")
        psc.plot_2d_colormap(filename, a0, i, wavelength, waveCount)
        os.rename(f"out-colormap-{i}.png", f"out-colormap-electromag-{i}.png")
        
        os.system(f"./data_analyst {filename} {num} {waveCount} {a0:0.3f} 0")
        os.rename("out-stats.bin", "out-stats-1.bin")

        os.system(f"./laser_electron 1 1 {a0:0.3f} {num} {stepsPonderomotive} {waveCount}")
        psc.plot_2d_colormap(filename, a0, i, wavelength, waveCount)
        os.rename(f"out-colormap-{i}.png", f"out-colormap-pond-{i}.png")
        
        os.system(f"./data_analyst {filename} {num} {waveCount} {a0:0.3f} 1")
        os.rename("out-stats.bin", "out-stats-2.bin")

        os.system(f"./error_calculator {num}")
        psc.plot_errors("out-error.bin", a0, i, wavelength)
    
    psc.plot_max_py("out-max-py.txt", a0, i)
    print(f"Program executed successfully. \a")