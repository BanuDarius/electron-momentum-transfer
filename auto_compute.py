import time
import numpy as np
import scripts.sim_init as sim_init
import scripts.programs as programs
import scripts.create_video as video
import scripts.plotting as plots

pi = 3.14159265359
c = 137.036
deg_to_rad = pi / 180.0

x_axis = 0
y_axis = 1
z_axis = 2

framerate = 3
first_eighth = 8
first_quarter = 4
substeps_pond = 1
all_states = False
final_states = True
full_trajectory = True
substeps_electromag = 8
trajectory_until_exit = False

# ------------------------------------------------------- #

min_a0 = 0.02
max_a0 = 0.60

tf = 1e4
zetax = 1.0
zetay = 0.0
core_num = 4
omega = 0.057
xif = 0.0 * pi
num_phase = 512
psi = -80.0 * pi
steps_pond = 256
num_full = 16000
wave_count = 1.0
sigma = 4.0 * pi
square_size = 1.0
sweep_steps = 128
steps_electromag = 4096
phi = 90.0 * deg_to_rad
theta = 90.0 * deg_to_rad
r = wave_count * 2.0 * pi * c / omega
rotate_angle = 90.0 * deg_to_rad
pond_integrate_steps = 4

# ------------------------------------------------------- #

if __name__ == "__main__":
    a0_array = np.array([])
    programs.clean_output_folder()
    start_time = time.time()
    for i in range(0, sweep_steps):
        a0 = min_a0 + (max_a0 - min_a0) * i / sweep_steps
        a0_array = np.append(a0_array, a0)
        
        laser_1 = sim_init.LaserParameters(a0, sigma, omega, xif, zetax, zetay, phi, theta, psi, pond_integrate_steps)
        laser_2 = sim_init.LaserParameters(a0, sigma, omega, xif, zetax, zetay, phi, -theta, psi, pond_integrate_steps)
        laser_3 = sim_init.LaserParameters(a0, sigma, omega, xif, zetax, zetay, phi, -135.0 * deg_to_rad, psi, pond_integrate_steps)
        laser_4 = sim_init.LaserParameters(a0, sigma, omega, xif, zetax, zetay, phi, 135.0 * deg_to_rad, psi, pond_integrate_steps)
        
        lasers = (laser_1, laser_2, laser_3, laser_4)
        
        # ------------------------------------------------------- #
        
        '''sim_parameters = sim_init.SimParameters(i, r, num_full, tf,  steps_electromag, first_eighth,
            substeps_electromag, core_num, final_states, wave_count, rotate_angle, sweep_steps, full_trajectory)
        
        programs.run_simulation("electromagnetic", sim_parameters, lasers)
        
        plots.plot_2d_colormap("electromagnetic", sim_parameters, a0_array, y_axis, z_axis, x_axis)
        plots.plot_2d_colormap("electromagnetic", sim_parameters, a0_array, y_axis, z_axis, y_axis)
        plots.plot_2d_colormap("electromagnetic", sim_parameters, a0_array, y_axis, z_axis, z_axis)'''
        
        # ------------------------------------------------------- #
        
        sim_parameters = sim_init.SimParameters(i, r, num_phase, tf,  steps_electromag, first_eighth,
            substeps_electromag, core_num, all_states, wave_count, rotate_angle, sweep_steps, full_trajectory)
        
        programs.run_simulation("electromagnetic", sim_parameters, lasers)
        
        programs.find_final_p("electromagnetic", sim_parameters, y_axis, x_axis)
        programs.find_max_p("electromagnetic", sim_parameters, x_axis)
        programs.find_enter_exit_time("electromagnetic", sim_parameters, y_axis, x_axis)
        
        programs.find_final_p("electromagnetic", sim_parameters, y_axis, y_axis)
        programs.find_max_p("electromagnetic", sim_parameters, y_axis)
        programs.find_enter_exit_time("electromagnetic", sim_parameters, y_axis, y_axis)
        
        programs.find_final_p("electromagnetic", sim_parameters, y_axis, z_axis)
        programs.find_max_p("electromagnetic", sim_parameters, z_axis)
        programs.find_enter_exit_time("electromagnetic", sim_parameters, y_axis, z_axis)
        
        #plots.plot_time_momentum("electromagnetic", sim_parameters, a0_array, y_axis, y_axis)
        #plots.plot_enter_exit_time("electromagnetic", sim_parameters, a0_array, y_axis, y_axis)
        #plots.plot_phases("electromagnetic", sim_parameters, a0_array, y_axis, y_axis)
        
        # ------------------------------------------------------- #
        
        sim_parameters = sim_init.SimParameters(i, r, num_phase, tf, steps_pond, first_eighth,
            substeps_pond, core_num, all_states, wave_count, rotate_angle, sweep_steps, full_trajectory)
        
        programs.run_simulation("ponderomotive", sim_parameters, lasers)
        
        programs.find_final_p("ponderomotive", sim_parameters, y_axis, x_axis)
        programs.find_max_p("ponderomotive", sim_parameters, x_axis)
        programs.find_enter_exit_time("ponderomotive", sim_parameters, y_axis, x_axis)
        
        programs.find_final_p("ponderomotive", sim_parameters, y_axis, y_axis)
        programs.find_max_p("ponderomotive", sim_parameters, y_axis)
        programs.find_enter_exit_time("ponderomotive", sim_parameters, y_axis, y_axis)
        
        programs.find_final_p("ponderomotive", sim_parameters, y_axis, z_axis)
        programs.find_max_p("ponderomotive", sim_parameters, z_axis)
        programs.find_enter_exit_time("ponderomotive", sim_parameters, y_axis, z_axis)
        
        #plots.plot_time_momentum("ponderomotive", sim_parameters, a0_array, y_axis, y_axis)
        #plots.plot_enter_exit_time("ponderomotive", sim_parameters, a0_array, y_axis, y_axis)
        #plots.plot_phases("ponderomotive", sim_parameters, a0_array, y_axis, y_axis)
        
        # ------------------------------------------------------- #
        programs.calculate_errors(sim_parameters, a0_array, x_axis)
        programs.calculate_errors(sim_parameters, a0_array, y_axis)
        programs.calculate_errors(sim_parameters, a0_array, z_axis)
        
        print(f"Ended parameter sweep step: {i+1}/{sweep_steps}.")
        
    plots.plot_max_p("electromagnetic", a0_array, x_axis)
    plots.plot_max_p("electromagnetic", a0_array, y_axis)
    plots.plot_max_p("electromagnetic", a0_array, z_axis)
    plots.plot_max_p("ponderomotive", a0_array, x_axis)
    plots.plot_max_p("ponderomotive", a0_array, y_axis)
    plots.plot_max_p("ponderomotive", a0_array, z_axis)
    plots.plot_average_errors(a0_array, x_axis)
    plots.plot_average_errors(a0_array, y_axis)
    plots.plot_average_errors(a0_array, z_axis)
    
    plots.plot_2d_errors_heatmap(sim_parameters, a0_array, y_axis, x_axis)
    plots.plot_2d_errors_heatmap(sim_parameters, a0_array, y_axis, y_axis)
    plots.plot_2d_errors_heatmap(sim_parameters, a0_array, y_axis, z_axis)
    plots.plot_2d_heatmap_all("electromagnetic", sim_parameters, a0_array, y_axis, x_axis)
    plots.plot_2d_heatmap_all("electromagnetic", sim_parameters, a0_array, y_axis, y_axis)
    plots.plot_2d_heatmap_all("electromagnetic", sim_parameters, a0_array, y_axis, z_axis)
    plots.plot_2d_heatmap_all("ponderomotive", sim_parameters, a0_array, y_axis, x_axis)
    plots.plot_2d_heatmap_all("ponderomotive", sim_parameters, a0_array, y_axis, y_axis)
    plots.plot_2d_heatmap_all("ponderomotive", sim_parameters, a0_array, y_axis, z_axis)
    
    '''video.create_2d_colormap_video("electromagnetic", framerate, y_axis, z_axis, y_axis)
    video.create_phase_video("electromagnetic", framerate, y_axis, y_axis)
    video.create_time_momentum_video("electromagnetic", framerate, y_axis, x_axis)
    video.create_time_momentum_video("electromagnetic", framerate, y_axis, y_axis)
    video.create_time_momentum_video("electromagnetic", framerate, y_axis, z_axis)'''
    
    #programs.clean_image_folder()
    
    total_time = time.time() - start_time
    print(f"Program executed successfully.")
    print(f"Total time taken: {total_time:0.3f}s.\a")