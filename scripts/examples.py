import sys
import time
import numpy as np
import scripts.sim_init as sim_init
import scripts.programs as programs
import scripts.plotting as plotting

c = 137.036
pi = 3.14159265359
deg_to_rad = pi / 180.0

x_axis = 0
y_axis = 1
z_axis = 2

framerate = 3
first_eighth = 8
first_quarter = 4

all_states = False
final_states = True
full_trajectory = True
trajectory_until_exit = False

def run_example(example_num, core_num):
    if(example_num == 1):
        min_a0 = 0.02
        max_a0 = 1.00

        zetax = 1.0
        zetay = 0.0
        tf = 12000.0
        tauf = 10000.0

        num_part = 1024
        sweep_steps = 1024
        num_full = 16000

        omega = 0.057
        xif = 0.0 * pi
        sigma = 19.0 * pi
        psi = -3.0 * sigma

        wavelength = 2.0 * pi * c / omega
        r_min = -1.00 * wavelength
        r_max = +1.00 * wavelength

        phi = 90.0 * deg_to_rad
        rotate_angle = 90.0 * deg_to_rad

        steps_pond = 512
        steps_electromag = 8192
        substeps_pond = 1
        substeps_electromag = 16
        pond_integrate_steps = 8
        
    a0_array = np.array([])
    programs.clean_output_folder()
    
    start_time = time.time()
    
    for i in range(0, sweep_steps):
        a0 = min_a0 + (max_a0 - min_a0) * i / sweep_steps
        a0_array = np.append(a0_array, a0)
        
        lasers = []
        lasers.append(sim_init.LaserParameters(a0, sigma, omega, xif, zetax, zetay, phi, 90.0 * deg_to_rad, psi, pond_integrate_steps))
        lasers.append(sim_init.LaserParameters(a0, sigma, omega, xif, zetax, zetay, phi, 270.0 * deg_to_rad, psi, pond_integrate_steps))
        
        # ------------------------------------------------------- #
        
        sim_parameters = sim_init.SimParameters(i, r_min, r_max, num_part, tf, steps_electromag, first_eighth,
            substeps_electromag, core_num, all_states, rotate_angle, sweep_steps, full_trajectory, wavelength, c) 
        
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
        
        # ------------------------------------------------------- #
        
        sim_parameters = sim_init.SimParameters(i, r_min, r_max, num_part, tauf, steps_pond, first_eighth,
            substeps_pond, core_num, all_states, rotate_angle, sweep_steps, full_trajectory, wavelength, c)
        
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
        
        # ------------------------------------------------------- #
        
        programs.calculate_errors(sim_parameters, a0_array, x_axis)
        programs.calculate_errors(sim_parameters, a0_array, y_axis)
        programs.calculate_errors(sim_parameters, a0_array, z_axis)
        
        print(f"Ended parameter sweep step: {i+1}/{sweep_steps}.")
        
    plotting.plot_max_p("electromagnetic", a0_array, x_axis)
    plotting.plot_max_p("electromagnetic", a0_array, y_axis)
    plotting.plot_max_p("electromagnetic", a0_array, z_axis)
    plotting.plot_max_p("ponderomotive", a0_array, x_axis)
    plotting.plot_max_p("ponderomotive", a0_array, y_axis)
    plotting.plot_max_p("ponderomotive", a0_array, z_axis)
    plotting.plot_average_errors(a0_array, x_axis)
    plotting.plot_average_errors(a0_array, y_axis)
    plotting.plot_average_errors(a0_array, z_axis)
    
    plotting.plot_2d_heatmap_all("electromagnetic", sim_parameters, a0_array, y_axis, x_axis)
    plotting.plot_2d_heatmap_all("electromagnetic", sim_parameters, a0_array, y_axis, y_axis)
    plotting.plot_2d_heatmap_all("electromagnetic", sim_parameters, a0_array, y_axis, z_axis)
    plotting.plot_2d_heatmap_all("ponderomotive", sim_parameters, a0_array, y_axis, x_axis)
    plotting.plot_2d_heatmap_all("ponderomotive", sim_parameters, a0_array, y_axis, y_axis)
    plotting.plot_2d_heatmap_all("ponderomotive", sim_parameters, a0_array, y_axis, z_axis)
    plotting.plot_2d_errors_heatmap(sim_parameters, a0_array, y_axis, x_axis)
    plotting.plot_2d_errors_heatmap(sim_parameters, a0_array, y_axis, y_axis)
    plotting.plot_2d_errors_heatmap(sim_parameters, a0_array, y_axis, z_axis)
            
    total_time = time.time() - start_time
    print(f"Program executed successfully.")
    print(f"Total time taken: {total_time:0.3f}s.\a")
    print(f"Ended reproducing example {example_num}.")
    sys.exit(1)