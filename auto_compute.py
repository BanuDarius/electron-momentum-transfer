'''MIT License

Copyright (c) 2026 Banu Darius-Matei

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

import time
import numpy as np
import scripts.common as common
import scripts.sim_init as sim_init
import scripts.programs as programs
import scripts.plotting as plotting
import scripts.examples as examples
import scripts.create_video as create_video
import tests.quick_example as quick_example
import tests.analytic_test as analytic_test
import tests.performance_test as performance_test

c = 137.036 #Speed of light in atomic units

x_axis = 0
y_axis = 1
z_axis = 2 #Definitions for the x, y, z axis

framerate = 3 #Video output framerate
first_eighth = 8 #First eight takes the first 1/8 of the simulation domain
first_quarter = 4 #First quarter takes 1/4 of the simulation domain

all_states = False
final_states = True
full_trajectory = True
trajectory_until_exit = False #Definitions for simulation parameters

# ------------------------------------------------------- #

thread_num = 8 #Number of threads

min_a0 = 0.02
max_a0 = 0.50 #Minimum and maximum of a0 for lasers

zetax = 0.0
zetay = 1.0 #Polarization parameters
min_tf = 8000.0
max_tf = 14000.0 #Final time for electromagnetic mode
tauf = 7000.0 #Final proper time for ponderomotive mode

num_part = 256 #Number of particles
sweep_steps = 256 #Number of parameter sweeps
num_full = 128000 #Number of particles for 2D colormaps

omega = 0.057
etaf = 0.0 * np.pi
sigma = 19.0 * np.pi
psi = -4.0 * sigma #Laser parameters

wavelength = 2.0 * np.pi * c / omega
r_min = -1.00 * wavelength
r_max = +1.00 * wavelength #Minimum and maximum radius for particle positions

phi = np.radians(90.0)
theta = np.radians(0.0) #Angles for the lasers
alpha = np.radians(0.0) #Angle for rotating the laser polarization vectors
rotate_angle = np.radians(0.0) #Angle for rotating the initial particles

min_steps_pond = 128
max_steps_pond = 128
min_steps_electromag = 4000
max_steps_electromag = 16000 #Minimum and maximum simulation steps
substeps_pond = 1
substeps_electromag = 16 #Substeps for data output
pond_integrate_steps = 4 #Steps used for the integrals in ponderomotive mode

v0_mag = 0.00 * c #Magnitude of initial velocity vector
phi_v0 = np.radians(0.0)
theta_v0 = np.radians(0.0) #Angles for the initial velocity vector

square_size = 1.0 #Size of squares in 2D colormaps

# ------------------------------------------------------- #

if __name__ == "__main__":
    start_time = time.time()
    a0_array = np.array([]) #This array will be passed to plotting functions
    programs.clean_output_folder() #Remove output data from previous run
    
    #Uncomment to run a quick test to showcase the program's capabilities
    #This will run a low resolution (256x256) parameter sweep
    #Will complete in ~1 minute on average consumer hardware
    #quick_example.run_quick_example(thread_num)
    
    #In the examples/ directory there are several examples whose filenames start with 1, 2, 3, and 4
    #Uncomment this line to reproduce any of them
    #examples.run_example(1, thread_num)
    
    #Uncomment to replicate the results obtained in the Physical Review Letters paper
    #"Relativistic Ponderomotive Force, Uphill Acceleration, and Transition to Chaos", D. Bauer et al. (1995)
    #examples.replicate_prl_results(thread_num)
    
    #Uncomment this line to run a quick parameter sweep test for a0 = 0.02 to 10.00,
    #Comparing the Higuera-Cary integrator with an analytical solution for one laser
    #analytic_test.run_complete_test(v0_mag)
    
    #Uncomment to create a relative performance speedrup analysis for a pre-defined scenario
    #performance_test.run_example_performance_test(thread_num)
    
    for i in range(0, sweep_steps):
        tf = common.interpolate(min_tf, max_tf, i, sweep_steps)
        a0 = common.interpolate(min_a0, max_a0, i, sweep_steps)
        steps_electromag = int(common.interpolate(min_steps_electromag, max_steps_electromag, i, sweep_steps))
        steps_electromag = common.modulo_steps(steps_electromag, substeps_electromag)
        steps_pond = int(common.interpolate(min_steps_pond, max_steps_pond, i, sweep_steps))
        steps_pond = common.modulo_steps(steps_pond, substeps_pond)
        a0_array = np.append(a0_array, a0)
        
        lasers = [] #Array for all the lasers
        lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(0.0), psi, pond_integrate_steps))
        lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(60.0), psi, pond_integrate_steps))
        lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(120.0), psi, pond_integrate_steps))
        
        # ------------------------------------------------------- #
        
        '''sim_parameters = sim_init.SimParameters(i, r_min, r_max, num_full, tf, steps_electromag, first_eighth,
            substeps_electromag, v0_mag, phi_v0, theta_v0, thread_num, final_states, rotate_angle, sweep_steps, full_trajectory, wavelength, c)
        
        programs.run_simulation("electromagnetic", sim_parameters, lasers)
        
        sim_parameters.square_size = square_size
        plotting.plot_2d_colormap("electromagnetic", sim_parameters, a0_array, x_axis, z_axis, x_axis)'''
        
        # ------------------------------------------------------- #
        
        #Properties for the electromagneteic mode
        sim_parameters = sim_init.SimParameters(i, r_min, r_max, num_part, tf, steps_electromag, first_eighth,
            substeps_electromag, v0_mag, phi_v0, theta_v0, thread_num, all_states, rotate_angle, sweep_steps, full_trajectory, wavelength, c)
        
        #Uncomment to calculate the trajectory using an analytic solution
        #It will only use the first laser from the lasers array
        #programs.check_analytic_solution("electromagnetic", sim_parameters, lasers)
        #plotting.plot_trajectory_comparison(sim_parameters, lasers, x_axis)
        
        #Uncomment to run a performance test on this scenario
        #performance_test.run_performance_test("electromagnetic", sim_parameters, lasers, thread_num)
        
        #Uncomment to check the propagation vector, epsilon1, and epsilon2 for all lasers
        #programs.check_laser_polarization("electromagnetic", sim_parameters, lasers)
        
        programs.run_simulation("electromagnetic", sim_parameters, lasers)
        
        programs.find_final_p("electromagnetic", sim_parameters, x_axis, x_axis)
        programs.find_max_p("electromagnetic", sim_parameters, x_axis)
        #programs.find_enter_exit_time("electromagnetic", sim_parameters, x_axis, x_axis)
        
        programs.find_final_p("electromagnetic", sim_parameters, x_axis, y_axis)
        programs.find_max_p("electromagnetic", sim_parameters, y_axis)
        
        programs.find_final_p("electromagnetic", sim_parameters, x_axis, z_axis)
        programs.find_max_p("electromagnetic", sim_parameters, z_axis)
        
        #Uncomment to check the convergence of the momentum transfer by running another simulation with double the number of steps
        #programs.check_convergence("electromagnetic", sim_parameters, lasers, x_axis, x_axis, 2)
        
        #plotting.plot_time_momentum("electromagnetic", sim_parameters, a0_array, x_axis, y_axis)
        #plotting.plot_phases("electromagnetic", sim_parameters, a0_array, x_axis, y_axis)
        
        # ------------------------------------------------------- #
        
        #Properties for the ponderomotive mode
        sim_parameters = sim_init.SimParameters(i, r_min, r_max, num_part, tauf, steps_pond, first_eighth,
            substeps_pond, v0_mag, phi_v0, theta_v0, thread_num, all_states, rotate_angle, sweep_steps, full_trajectory, wavelength, c)
        
        programs.run_simulation("ponderomotive", sim_parameters, lasers)
        
        programs.find_final_p("ponderomotive", sim_parameters, x_axis, x_axis)
        programs.find_max_p("ponderomotive", sim_parameters, x_axis)
        
        programs.find_final_p("ponderomotive", sim_parameters, x_axis, y_axis)
        programs.find_max_p("ponderomotive", sim_parameters, y_axis)
        #programs.find_enter_exit_time("ponderomotive", sim_parameters, y_axis, y_axis)
        
        programs.find_final_p("ponderomotive", sim_parameters, x_axis, z_axis)
        programs.find_max_p("ponderomotive", sim_parameters, z_axis)
        
        #programs.check_convergence("ponderomotive", sim_parameters, lasers, x_axis, y_axis, 2)
        
        #plotting.plot_time_momentum("ponderomotive", sim_parameters, a0_array, x_axis, x_axis)
        #plotting.plot_phases("ponderomotive", sim_parameters, a0_array, y_axis, y_axis)
        
        # ------------------------------------------------------- #
        
        programs.calculate_errors(sim_parameters, x_axis)
        programs.calculate_errors(sim_parameters, y_axis)
        programs.calculate_errors(sim_parameters, z_axis)
        
        print(f"Ended parameter sweep step: {i+1}/{sweep_steps}.")
        
        # ------------------------------------------------------- #
        
    #Plots for data analysis
    plotting.plot_average_errors(a0_array, x_axis)
    plotting.plot_average_errors(a0_array, y_axis)
    plotting.plot_average_errors(a0_array, z_axis)
    plotting.plot_max_p("electromagnetic", a0_array, x_axis)
    plotting.plot_max_p("electromagnetic", a0_array, y_axis)
    plotting.plot_max_p("electromagnetic", a0_array, z_axis)
    plotting.plot_max_p("ponderomotive", a0_array, x_axis)
    plotting.plot_max_p("ponderomotive", a0_array, y_axis)
    plotting.plot_max_p("ponderomotive", a0_array, z_axis)
    
    #plotting.plot_convergence("electromagnetic", a0_array, x_axis)
    #plotting.plot_2d_convergence_heatmap("electromagnetic", sim_parameters, a0_array, x_axis, x_axis)
    
    plotting.plot_2d_heatmap_all("electromagnetic", sim_parameters, a0_array, x_axis, x_axis)
    plotting.plot_2d_heatmap_all("electromagnetic", sim_parameters, a0_array, x_axis, y_axis)
    plotting.plot_2d_heatmap_all("electromagnetic", sim_parameters, a0_array, x_axis, z_axis)
    plotting.plot_2d_heatmap_all("ponderomotive", sim_parameters, a0_array, x_axis, x_axis)
    plotting.plot_2d_heatmap_all("ponderomotive", sim_parameters, a0_array, x_axis, y_axis)
    plotting.plot_2d_heatmap_all("ponderomotive", sim_parameters, a0_array, x_axis, z_axis)
    plotting.plot_2d_errors_heatmap(sim_parameters, a0_array, x_axis, x_axis)
    plotting.plot_2d_errors_heatmap(sim_parameters, a0_array, x_axis, y_axis)
    plotting.plot_2d_errors_heatmap(sim_parameters, a0_array, x_axis, z_axis)
    
    #Uncomment to render videos using ffmpeg
    #create_video.create_2d_colormap_video("electromagnetic", framerate, x_axis, z_axis, x_axis)
    #create_video.create_phase_video("electromagnetic", framerate, x_axis, y_axis)
    #create_video.create_time_momentum_video("electromagnetic", framerate, x_axis, y_axis)
    
    #Uncomment to remove images if you created a video
    #programs.clean_image_folder()
    
    total_time = time.time() - start_time
    print(f"Program executed successfully.")
    print(f"Total time taken: {total_time:0.3f}s.\a")