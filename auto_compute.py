import numpy as np
import scripts.programs as programs
import scripts.create_video as video
import scripts.plotting as plots

pi = 3.14159265359
deg_to_rad = pi / 180.0

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

tauf = 1e4
core_num = 8
omega = 0.057
xif = 0.0 * pi
num_phase = 512
psi = -60.0 * pi
steps_pond = 256
num_full = 16000
wave_count = 1.0
sigma = 16.0 * pi
square_size = 3.0
sweep_steps = 256
steps_electromag = 4096
phi = 90.0 * deg_to_rad
theta = 90.0 * deg_to_rad

# ------------------------------------------------------- #

class SimParameters:
    def __init__(self, i, num, tauf, steps, divider, substeps, core_num, wave_count, output_mode, square_size, sweep_steps, full_trajectory):
        self.i = i
        self.num = num
        self.tauf = tauf
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

class LaserParameters:
    def __init__(self, a0, sigma, omega, xif, zetax, zetay, phi, theta, psi):
        self.a0 = a0
        self.xif = xif
        self.phi = phi
        self.psi = psi
        self.sigma = sigma
        self.zetax = zetax
        self.zetay = zetay
        self.omega = omega
        self.theta = theta

# ------------------------------------------------------- #

if __name__ == "__main__":
    a0_array = np.array([])
    programs.clean_output_folder()
    
    for i in range(0, sweep_steps):
        a0 = 0.02 + i / 500
        a0_array = np.append(a0_array, a0)
        
        laser_1 = LaserParameters(a0, sigma, omega, xif, 0.0, 1.0, phi, theta, psi)
        laser_2 = LaserParameters(a0, sigma, omega, xif, 0.0, 1.0, phi, -theta, psi)
        
        lasers = (laser_1, laser_2)
        
        '''sim_parameters = SimParameters(i, num_full, tauf,  steps_electromag, first_eighth,
            substeps_electromag, core_num, wave_count, final_states, square_size, sweep_steps, full_trajectory)
        
        programs.run_simulation("electromagnetic", sim_parameters, lasers)
        
        plots.plot_2d_colormap("electromagnetic", sim_parameters, a0_array)'''
        
        # ------------------------------------------------------- #
        
        sim_parameters = SimParameters(i, num_phase, tauf,  steps_electromag, first_eighth,
            substeps_electromag, core_num, wave_count, all_states, square_size, sweep_steps, full_trajectory)
        
        programs.run_simulation("electromagnetic", sim_parameters, lasers)
        
        programs.find_final_py("electromagnetic", sim_parameters)
        
        programs.find_max_py("electromagnetic", sim_parameters)
        
        programs.find_enter_exit_time("electromagnetic", sim_parameters)
        
        #plots.plot_time_momentum("electromagnetic", sim_parameters)
        
        #plots.plot_enter_exit_time("electromagnetic", sim_parameters)
        
        #plots.plot_phases("electromagnetic", sim_parameters)
        
        # ------------------------------------------------------- #
        
        sim_parameters = SimParameters(i, num_phase, tauf, steps_pond, first_eighth,
            substeps_pond, core_num, wave_count, all_states, square_size, sweep_steps, trajectory_until_exit)
        
        programs.run_simulation("ponderomotive", sim_parameters, lasers)
        
        programs.find_final_py("ponderomotive", sim_parameters)
        
        programs.find_max_py("ponderomotive", sim_parameters)
        
        programs.find_enter_exit_time("ponderomotive", sim_parameters)
        
        #plots.plot_time_momentum("ponderomotive", sim_parameters)
        
        #plots.plot_enter_exit_time("ponderomotive", sim_parameters)
        
        #plots.plot_phases("ponderomotive", sim_parameters)
        
        # ------------------------------------------------------- #
        programs.calculate_errors(sim_parameters, a0_array)
        
        print(f"Ended parameter sweep step: {i+1}/{sweep_steps}.")
        
        #plots.plot_errors(a0, num_phase, i)
        
        #plotting.plot_phases_oscillator(a0, i, num_phase, wavelength, wave_count)
        
    plots.plot_max_py("electromagnetic", a0_array)
    
    plots.plot_max_py("ponderomotive", a0_array)
    
    plots.plot_average_errors(a0_array)
    
    plots.plot_all_errors(sim_parameters, a0_array)
    
    plots.plot_2d_heatmap_all("electromagnetic", sim_parameters, a0_array)
    
    plots.plot_2d_heatmap_all("ponderomotive", sim_parameters, a0_array)
    
    '''video.create_2d_colormap_video("electromagnetic", framerate)
    video.create_2d_colormap_video("ponderomotive", framerate)
    video.create_enter_exit_video("electromagnetic", framerate)
    video.create_phase_video("electromagnetic", framerate)
    video.create_phase_video("ponderomotive", framerate)
    video.create_error_video(framerate)'''
    
    #programs.clean_image_folder()
    
    print(f"Program executed successfully. \a")