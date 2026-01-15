import os
import scripts.create_video as video
import scripts.plotting_scripts as plotting

wavelength = 2 * 3.141592 * 137.036 / 0.057
framerate = 3

num = 4000
numPhase = 128
waveCount = 2
stepsElectromagnetic = 4096
stepsPonderomotive = 32
xif = 8.0 * 3.141592
tauf = 4300

if __name__ == "__main__":
    try:
        os.remove("./output/out-deriv.bin")
        os.remove("./output/out-max-py.bin")
        os.remove("./output/out-average-error.bin")
    except OSError:
        pass
    for i in range(0, 10):
        a0 = 0.010 + i / 100.0
        
        plotting.plot_2d_colormap("electromagnetic", a0, xif, tauf, i, wavelength, waveCount, num, stepsElectromagnetic)

        plotting.analyze_data("electromagnetic", True, True, a0, waveCount, num)
       
        #plotting.plot_phases("electromagnetic", a0, xif, tauf, i, wavelength, waveCount, numPhase, stepsElectromagnetic)

        #plotting.plot_enter_exit_time("electromagnetic", a0, i, wavelength, numPhase, stepsElectromagnetic)
        
        plotting.plot_2d_colormap("ponderomotive", a0, xif, tauf, i, wavelength, waveCount, num, stepsPonderomotive)
        
        plotting.analyze_data("ponderomotive", False, True, a0, waveCount, num)

        plotting.plot_errors(a0, i, wavelength, num)

        #plotting.plot_phases_oscillator(a0, i, numPhase, wavelength, waveCount)
    
    plotting.plot_max_py(a0, i)
    plotting.plot_average_errors(a0, i)
    video.create_2d_colormap_video("electromagnetic", framerate)
    video.create_2d_colormap_video("ponderomotive", framerate)
    video.create_error_video(framerate)
    print(f"Program executed successfully. \a")