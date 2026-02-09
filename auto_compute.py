import scripts.programs as programs
import scripts.create_video as video
import scripts.plotting as plots

pi = 3.14159265359
wavelength = 2.0 * pi * 137.036 / 0.057

framerate = 3
first_eighth = 8
first_quarter = 4
all_states = False
final_states = True
full_trajectory = True
trajectory_until_exit = False
substeps_electromag = 8
substeps_pond = 1

# ------------------------------------------------------- #

core_num = 8
square_size = 2
sweep_steps = 256
wave_count = 1.0
num_full = 64000
num_phase = 256
steps_electromag = 4096
steps_pond = 256
tauf = 10000.0
xif = 0.0 * pi
sigma = 16.0 * pi

# ------------------------------------------------------- #

class SimParameters:
    def __init__(self, i, a0, num, xif, tauf, sigma, steps, divider,substeps, core_num, wave_count, output_mode, square_size, sweep_steps, full_trajectory):
        self.i = i
        self.a0 = a0
        self.num = num
        self.xif = xif
        self.tauf = tauf
        self.sigma = sigma
        self.steps = steps
        self.divider = divider
        self.substeps = substeps
        self.core_num = core_num
        self.wave_count = wave_count
        self.output_mode = output_mode
        self.square_size = square_size
        self.sweep_steps = sweep_steps
        self.full_trajectory = full_trajectory

# ------------------------------------------------------- #

if __name__ == "__main__":
    programs.clean_output_folder()
    for i in range(0, sweep_steps):
        
        a0 = 0.02 + i / 400.0
        
        '''sim_parameters = SimParameters(i, a0, num_full, xif, tauf, sigma, steps_electromag, first_eighth,
            substeps_electromag, core_num, wave_count, final_states, square_size, sweep_steps, full_trajectory)
        
        programs.run_simulation("electromagnetic", sim_parameters)
        
        plots.plot_2d_colormap("electromagnetic", sim_parameters)'''
        
        # ------------------------------------------------------- #
        
        sim_parameters = SimParameters(i, a0, num_phase, xif, tauf, sigma, steps_electromag, first_eighth,
            substeps_electromag, core_num, wave_count, all_states, square_size, sweep_steps, full_trajectory)
        
        programs.run_simulation("electromagnetic", sim_parameters)
        
        programs.find_final_py("electromagnetic", sim_parameters)
        
        programs.find_max_py("electromagnetic", sim_parameters)
        
        programs.find_enter_exit_time("electromagnetic", sim_parameters)
        
        #plots.plot_time_momentum("electromagnetic", sim_parameters)
        
        #plots.plot_enter_exit_time("electromagnetic", sim_parameters)
        
        #plots.plot_phases("electromagnetic", sim_parameters)
        
        # ------------------------------------------------------- #
        
        sim_parameters = SimParameters(i, a0, num_phase, xif, tauf, sigma, steps_pond, first_eighth,
            substeps_pond, core_num, wave_count, all_states, square_size, sweep_steps, trajectory_until_exit)
        
        programs.run_simulation("ponderomotive", sim_parameters)
        
        programs.find_final_py("ponderomotive", sim_parameters)
        
        programs.find_max_py("ponderomotive", sim_parameters)
        
        programs.find_enter_exit_time("ponderomotive", sim_parameters)
        
        #plots.plot_time_momentum("ponderomotive", sim_parameters)
        
        #plots.plot_enter_exit_time("ponderomotive", sim_parameters)
        
        #plots.plot_phases("ponderomotive", sim_parameters)
        
        # ------------------------------------------------------- #
        programs.calculate_errors(sim_parameters)
        
        print(f"Ended parameter sweep step: {i+1}/{sweep_steps}.")
        
        #plots.plot_errors(a0, num_phase, i)
        
        #plotting.plot_phases_oscillator(a0, i, num_phase, wavelength, wave_count)
        
    plots.plot_max_py("electromagnetic")
    
    plots.plot_max_py("ponderomotive")
    
    plots.plot_average_errors()
    
    plots.plot_all_errors(sim_parameters)
    
    plots.plot_2d_heatmap_all("electromagnetic", sim_parameters)
    
    plots.plot_2d_heatmap_all("ponderomotive", sim_parameters)

    '''video.create_2d_colormap_video("electromagnetic", framerate)
    video.create_2d_colormap_video("ponderomotive", framerate)
    video.create_enter_exit_video("electromagnetic", framerate)
    video.create_phase_video("electromagnetic", framerate)
    video.create_phase_video("ponderomotive", framerate)
    video.create_error_video(framerate)'''
    
    #programs.clean_image_folder()

    print(f"Program executed successfully. \a")