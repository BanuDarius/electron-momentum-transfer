import os
import scripts.programs as programs
import scripts.create_video as video
import scripts.plotting as plots

pi = 3.14159265359
wavelength = 2.0 * pi * 137.036 / 0.057
first_quarter = 4
first_eighth = 8
all_states = False
final_states = True
full_trajectory = True
trajectory_until_exit = False
substeps_electromag = 8
substeps_pond = 1
square_size = 1
framerate = 3
core_num = 4

# ----------------------------------- #

wave_count = 1.0
num_full = 16000
num_phase = 512
sweep_steps = 512
steps_pond = 256
steps_electromag = 4096
tauf = 10000.0
xif = 4.0 * pi
sigma = 4.0 * pi

# ----------------------------------- #

steps_electromag_final = int(steps_electromag / substeps_electromag)
steps_pond_final = int(steps_pond / substeps_pond)

if __name__ == "__main__":
    programs.clean_output_folder()
    for i in range(0, sweep_steps):
        a0 = 0.03 + i / 500
        
        #programs.run_simulation("electromagnetic", final_states, a0, xif, tauf, sigma, wave_count, num_full, steps_electromag, substeps_electromag, core_num)
        
        #plots.plot_2d_colormap("electromagnetic", a0, wave_count, i)
        
        # ----------------------------------- #
        
        programs.run_simulation("electromagnetic", all_states, a0, xif, tauf, sigma, wave_count, num_phase, steps_electromag, substeps_electromag, core_num)
        
        programs.find_final_py("electromagnetic", num_phase, steps_electromag_final)
        
        programs.find_max_py("electromagnetic", a0, num_phase, steps_electromag_final)
        
        programs.find_enter_exit_time("electromagnetic", num_phase, steps_electromag_final)
        
        #plots.plot_time_momentum("electromagnetic", full_trajectory, a0, num_phase, steps_electromag_final, i, first_eighth)
        
        #plots.plot_enter_exit_time("electromagnetic", a0, num_phase, steps_electromag_final, i)
        
        #plots.plot_phases("electromagnetic", full_trajectory, a0, wave_count, num_phase, steps_electromag_final, i)
        
        # ----------------------------------- #
        
        programs.run_simulation("ponderomotive", all_states, a0, xif, tauf, sigma, wave_count, num_phase, steps_pond, substeps_pond, core_num)
        
        programs.find_final_py("ponderomotive", num_phase, steps_pond_final)
        
        programs.find_max_py("ponderomotive", a0, num_phase, steps_electromag_final)
        
        programs.find_enter_exit_time("ponderomotive", num_phase, steps_pond_final)
        
        #plots.plot_time_momentum("ponderomotive", full_trajectory, a0, num_phase, steps_pond_final, i, first_eighth)
        
        #plots.plot_enter_exit_time("ponderomotive", a0, num_phase, steps_pond_final, i)
        
        #plots.plot_phases("ponderomotive", a0, wave_count, num_phase, steps_pond_final, i)
        
        # ---------------------------------- #
        programs.calculate_errors(a0, num_phase)
        
        print(f"Ended parameter sweep step: {i+1}/{sweep_steps}.")
        
        #plots.plot_errors(a0, num_phase, i)
        
        #plotting.plot_phases_oscillator(a0, i, num_phase, wavelength, wave_count)
        
    plots.plot_max_py("electromagnetic", a0, i)
    
    plots.plot_average_errors(a0, i)
    
    plots.plot_all_errors(sweep_steps, num_phase, wave_count)
    
    plots.plot_2d_heatmap_all("electromagnetic", sweep_steps, num_phase, wave_count, square_size)
    
    plots.plot_2d_heatmap_all("ponderomotive", sweep_steps, num_phase, wave_count, square_size)

    '''video.create_2d_colormap_video("electromagnetic", framerate)
    video.create_2d_colormap_video("ponderomotive", framerate)
    video.create_enter_exit_video("electromagnetic", framerate)
    video.create_phase_video("electromagnetic", framerate)
    video.create_phase_video("ponderomotive", framerate)
    video.create_error_video(framerate)'''
    
    #programs.clean_image_folder()

    print(f"Program executed successfully. \a")