import os
import plotting_scripts as psc

wavelength = 2 * 3.141592 * 137.036 / 0.057

num = 32000
stepsElectromagnetic = 4096
stepsPonderomotive = 1024
waveCount = 1
xif = 32.0 * 3.141592
tauf = 8300

if __name__ == "__main__":
    try:
        os.remove("out-deriv.txt")
        os.remove("out-max-py.txt")
        os.remove("out-average-error.bin")
    except OSError:
        pass
    for i in range(0, 100):
        a0 = 0.010 + i / 500.0
        
        psc.plot_2d_colormap("electromagnetic", a0, xif, tauf, i, wavelength, waveCount, num, stepsElectromagnetic)
        
        psc.analyze_data("electromagnetic", True, a0, waveCount, num)
        
        psc.plot_2d_colormap("ponderomotive", a0, xif, tauf, i, wavelength, waveCount, num, stepsPonderomotive)
        
        psc.analyze_data("ponderomotive", False, a0, waveCount, num)

        psc.plot_errors(a0, i, wavelength, num)

        psc.plot_phases("electromagnetic", a0, xif, tauf, i, wavelength, waveCount, 1024, stepsElectromagnetic)
    
    psc.plot_max_py(a0, i)
    psc.plot_average_errors(a0, i)
    print(f"Program executed successfully. \a")