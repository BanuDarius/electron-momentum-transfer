import scripts.programs as programs
import scripts.create_video as video
import scripts.plotting as plots

pi = 3.14159265359
wavelength = 2.0 * pi * 137.036 / 0.057

core_num = 4
framerate = 3
square_size = 2
first_eighth = 8
first_quarter = 4
all_states = False
final_states = True
full_trajectory = True
trajectory_until_exit = False
substeps_electromag = 8
substeps_pond = 1

# ----------------------------------- #

wave_count = 1.0
num_full = 16000
num_phase = 256
sweep_steps = 256
steps_electromag = 4096
steps_pond = 256
tauf = 10000.0
xif = 4.0 * pi
sigma = 16.0 * pi

# ----------------------------------- #

class SimParameters:
    def __init__(self, a0, num, xif, tauf, sigma, steps, substeps, core_num, wave_count, output_mode):
        self.a0 = a0
        self.num = num
        self.xif = xif
        self.tauf = tauf
        self.sigma = sigma
        self.steps = steps
        self.substeps = substeps
        self.core_num = core_num
        self.wave_count = wave_count
        self.output_mode = output_mode

# ----------------------------------- #

if __name__ == "__main__":
    programs.clean_output_folder()
    for i in range(0, sweep_steps):
        
        a0 = 0.03 + i / 200
        
        sim_parameters = SimParameters(a0, num_full, xif, tauf, sigma, steps_electromag, substeps_electromag, core_num, wave_count, final_states)
        
        programs.run_simulation("electromagnetic", sim_parameters)
        
        plots.plot_2d_colormap("electromagnetic", a0, wave_count, i)
        
        # ----------------------------------- #
        
        sim_parameters = SimParameters(a0, num_phase, xif, tauf, sigma, steps_electromag, substeps_electromag, core_num, wave_count, all_states)
        
        programs.run_simulation("electromagnetic", sim_parameters)
        
        programs.find_final_py("electromagnetic", sim_parameters)
        
        programs.find_max_py("electromagnetic", sim_parameters)
        
        programs.find_enter_exit_time("electromagnetic", sim_parameters)
        
        #plots.plot_time_momentum("electromagnetic", full_trajectory, a0, num_phase, steps_electromag_final, i, first_eighth)
        
        #plots.plot_enter_exit_time("electromagnetic", a0, num_phase, steps_electromag_final, i)
        
        #plots.plot_phases("electromagnetic", full_trajectory, a0, wave_count, num_phase, steps_electromag_final, i)
        
        # ----------------------------------- #
        
        sim_parameters = SimParameters(a0, num_phase, xif, tauf, sigma, steps_pond, substeps_pond, core_num, wave_count, all_states)
        
        programs.run_simulation("ponderomotive", sim_parameters)
        
        programs.find_final_py("ponderomotive", sim_parameters)
        
        programs.find_max_py("ponderomotive", sim_parameters)
        
        programs.find_enter_exit_time("ponderomotive", sim_parameters)
        
        #plots.plot_time_momentum("ponderomotive", full_trajectory, a0, num_phase, steps_pond_final, i, first_eighth)
        
        #plots.plot_enter_exit_time("ponderomotive", a0, num_phase, steps_pond_final, i)
        
        #plots.plot_phases("ponderomotive", a0, wave_count, num_phase, steps_pond_final, i)
        
        # ---------------------------------- #
        programs.calculate_errors(sim_parameters)
        
        print(f"Ended parameter sweep step: {i+1}/{sweep_steps}.")
        
        #plots.plot_errors(a0, num_phase, i)
        
        #plotting.plot_phases_oscillator(a0, i, num_phase, wavelength, wave_count)
        
    plots.plot_max_py("electromagnetic")
    
    plots.plot_max_py("ponderomotive")
    
    plots.plot_average_errors()
    
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