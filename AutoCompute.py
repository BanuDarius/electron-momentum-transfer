import os
import sys
import PlottingScripts as psc

wavelength = 2 * 3.141592 * 137.036 / 0.057

mode = 1
outputMode = 1
num = 8000
stepsElectromagnetic = 8192
stepsPonderomotive = 512
waveCount = 1

if __name__ == "__main__":
    try:
        os.remove("out-deriv.txt")
    except OSError:
        pass

    for i in range(3, 4):
        a0 = 0.010 + i / 500.0
        scale = waveCount * wavelength
        filename = "out-data.bin"
        os.system(f"./LaserElectron 0 1 {a0:0.3f} {num} {stepsElectromagnetic} {waveCount}")
        psc.plot_2d_colormap(filename, a0, i, wavelength, waveCount)
        os.system(f"./DataAnalyst {filename} {num} {waveCount} {a0:0.3f}")
        os.rename("out-stats.bin", "out-stats-1.bin")

        #os.system(f"./LaserElectron 1 1 {a0:0.3f} {num} {stepsPonderomotive} {waveCount}")
        #psc.plot_2d_colormap(filename, a0, i, wavelength, waveCount)
        #os.system(f"./DataAnalyst {filename} {num} {waveCount} {a0:0.3f}")
        #os.rename("out-stats.bin", "out-stats-2.bin")

        os.system(f"./ErrorCalculator {num}")
        psc.plot_errors("out-error.bin", a0, i, wavelength)
    
    print(f"Program executed successfully. \a")