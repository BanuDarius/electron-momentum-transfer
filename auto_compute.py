import os
import scripts.create_video as video
import scripts.plotting_scripts as plots
import scripts.programs as programs

all_states = False
final_states = True
wavelength = 2 * 3.141592 * 137.036 / 0.057
substeps_electromag = 8
substeps_pond = 2
framerate = 3

num_full = 16000
num_phase = 512
sweep_steps = 512
wave_count = 1
steps_electromag = 8192
steps_pond = 128
tauf = 8000.0
xif = 0.0 * 3.141592
sigma = 16.0 * 3.141592

steps_electromag_final = int(steps_electromag / substeps_electromag)
steps_pond_final = int(steps_pond / substeps_pond)

if __name__ == "__main__":
    programs.clean_output_folder()
    for i in range(0, sweep_steps):
        a0 = 0.005 + i / 1024
        
        #programs.run_simulation("electromagnetic", final_states, a0, xif, tauf, wave_count, num_full, steps_electromag)
        
        #plots.plot_2d_colormap("electromagnetic", a0, wave_count, i)
        
        programs.run_simulation("electromagnetic", all_states, a0, xif, tauf, sigma, wave_count, num_phase, steps_electromag, substeps_electromag)
        
        programs.find_final_py("electromagnetic", num_phase, steps_electromag_final)
        
        programs.find_max_py("electromagnetic", a0, num_phase, steps_electromag_final)
        
        #programs.find_enter_exit_time("electromagnetic", num_phase, steps_electromag_final)
        
        plots.plot_enter_exit_time("electromagnetic", a0, num_phase, steps_electromag_final, i)
        
        #plots.plot_phases("electromagnetic", a0, wave_count, num_phase, steps_electromag_final, i)
        
        # ----------------------------------- #
        
        programs.run_simulation("ponderomotive", all_states, a0, xif, tauf, sigma, wave_count, num_phase, steps_pond, substeps_pond)
        
        programs.find_final_py("ponderomotive", num_phase, steps_pond_final)
        
        #programs.find_enter_exit_time("ponderomotive", num_phase, steps_pond_final)
        
        #plots.plot_enter_exit_time("ponderomotive", a0, num_phase, steps_pond_final, i)
        
        #plots.plot_phases("ponderomotive", a0, wave_count, num_phase, steps_pond_final, i)
        
        # ---------------------------------- #
        programs.calculate_errors(a0, num_phase)
        
        plots.plot_errors(a0, num_phase, i)
        
        print(f"Ended parameter sweep step: {i}/{sweep_steps}.")
        
        #plotting.plot_phases_oscillator(a0, i, num_phase, wavelength, wave_count)
        
    plots.plot_max_py("electromagnetic", a0, i)
    
    plots.plot_average_errors(a0, i)
    
    plots.plot_all_errors(sweep_steps, num_phase, wave_count)
    
    plots.plot_2d_heatmap_all("electromagnetic", sweep_steps, num_phase, wave_count)
    
    #plots.plot_2d_heatmap_all("ponderomotive", sweep_steps, num_phase, wave_count)

    '''video.create_2d_colormap_video("electromagnetic", framerate)
    video.create_2d_colormap_video("ponderomotive", framerate)
    video.create_enter_exit_video("electromagnetic", framerate)
    video.create_phase_video("electromagnetic", framerate)
    video.create_phase_video("ponderomotive", framerate)
    video.create_error_video(framerate)'''
    
    #programs.clean_image_folder()

    print(f"Program executed successfully. \a")