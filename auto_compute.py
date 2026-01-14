import os
import plotting_scripts as psc

wavelength = 2 * 3.141592 * 137.036 / 0.057

num = 4000
numPhase = 128
stepsElectromagnetic = 4096
stepsPonderomotive = 128
waveCount = 1
xif = 2.0 * 3.141592
tauf = 7000

if __name__ == "__main__":
    try:
        os.remove("./output/out-deriv.txt")
        os.remove("./output/out-max-py.txt")
        os.remove("./output/out-average-error.bin")
    except OSError:
        pass
    for i in range(0, 20):
        a0 = 0.010 + i / 100.0
        
        psc.plot_2d_colormap("electromagnetic", a0, xif, tauf, i, wavelength, waveCount, num, stepsElectromagnetic)

        psc.analyze_data("electromagnetic", True, True, a0, waveCount, num)
       
        psc.plot_phases("electromagnetic", a0, xif, tauf, i, wavelength, waveCount, numPhase, stepsElectromagnetic)

        psc.plot_exit_time("electromagnetic", a0, i, wavelength, numPhase, stepsElectromagnetic)
        
        psc.plot_2d_colormap("ponderomotive", a0, xif, tauf, i, wavelength, waveCount, num, stepsPonderomotive)
        
        psc.analyze_data("ponderomotive", False, True, a0, waveCount, num)

        psc.plot_errors(a0, i, wavelength, num)
    
    psc.plot_max_py(a0, i)
    psc.plot_average_errors(a0, i)
    print(f"Program executed successfully. \a")