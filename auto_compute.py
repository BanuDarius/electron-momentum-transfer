import time
import numpy as np
from pathlib import Path
import scripts.common as common
import scripts.sim_init as sim_init
import scripts.programs as programs
import scripts.plotting as plotting
import scripts.examples as examples
import scripts.create_video as create_video
import tests.quick_example as quick_example
    
c = 137.036

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

# ------------------------------------------------------- #

thread_num = 8 #Number of threads

min_a0 = 0.02
max_a0 = 1.00 #Minimum and maximum of a0 for lasers

zetax = 0.0
zetay = 1.0 #Polarization parameters
min_tf = 10000.0
max_tf = 16000.0 #Final time for electromagnetic mode 
tauf = 7000.0 #Final proper time for ponderomotive mode

num_part = 256 #Number of particles
sweep_steps = 256 #Number of parameter sweeps
num_full = 16000 #Number of particles for 2D colormaps

omega = 0.057
xif = 0.0 * np.pi
sigma = 19.0 * np.pi
psi = -3.0 * sigma #Laser parameters

wavelength = 2.0 * np.pi * c / omega
r_min = -1.00 * wavelength
r_max = 1.00 * wavelength #Minimum and maximum radius for particle positions

phi = np.radians(90.0)
theta = np.radians(90.0) #Angles for the lasers
rotate_angle = np.radians(0.0) #Angles for rotating the initial particles
alpha = np.radians(0.0) #Angle for rotating the laser polarization vectors

min_steps_pond = 128
max_steps_pond = 512
min_steps_electromag = 4000
max_steps_electromag = 16000 #Minimum and maximum simulation steps
substeps_pond = 1
substeps_electromag = 16 #Substeps for data output
pond_integrate_steps = 4 #Steps used for the integrals in ponderomotive mode

square_size = 1.0 #Size of squares in 2D colormaps

# ------------------------------------------------------- #

if __name__ == "__main__":
    #Uncomment to run a quick test to showcase the program's capabilities
    #This will run a low resolution (128x128) parameter sweep
    #Will complete in ~1 minute on consumer hardware
    #quick_example.run_quick_example(thread_num)
    
    #In the examples/ directory there are several examples
    #Uncomment this line to reproduce any of them
    #examples.run_example(1, thread_num)
    
    start_time = time.time()
    a0_array = np.array([]) #This array will be passed to plotting functions
    programs.clean_output_folder() #Remove output data from previous run
    
    for i in range(0, sweep_steps):
        tf = common.interpolate(min_tf, max_tf, i, sweep_steps)
        a0 = common.interpolate(min_a0, max_a0, i, sweep_steps)
        steps_electromag = int(common.interpolate(min_steps_electromag, max_steps_electromag, i, sweep_steps))
        steps_electromag = common.modulo_steps(steps_electromag, substeps_electromag)
        steps_pond = int(common.interpolate(min_steps_pond, max_steps_pond, i, sweep_steps))
        steps_pond = common.modulo_steps(steps_pond, substeps_pond)
        a0_array = np.append(a0_array, a0)
        
        lasers = [] #Defines all lasers
        lasers.append(sim_init.LaserParameters(a0, sigma, omega, xif, zetax, zetay, np.radians(0.0), phi, np.radians(0.0), psi, pond_integrate_steps))
        #lasers.append(sim_init.LaserParameters(a0, sigma, omega, xif, zetax, zetay, np.radians(180.0), phi, np.radians(45.0), psi, pond_integrate_steps))
        #lasers.append(sim_init.LaserParameters(a0, sigma, omega, xif, zetax, zetay, np.radians(180.0), phi, np.radians(135.0), psi, pond_integrate_steps))
        lasers.append(sim_init.LaserParameters(a0, sigma, omega, xif, zetax, zetay, np.radians(0.0), phi, np.radians(180.0), psi, pond_integrate_steps))
        
        # ------------------------------------------------------- #
        
        '''sim_parameters = sim_init.SimParameters(i, r, num_full, tf,  steps_electromag, first_eighth,
            substeps_electromag, thread_num, final_states, rotate_angle, sweep_steps, full_trajectory, c)
        
        programs.run_simulation("electromagnetic", sim_parameters, lasers)
        
        plotting.plot_2d_colormap("electromagnetic", sim_parameters, a0_array, y_axis, z_axis, x_axis)
        plotting.plot_2d_colormap("electromagnetic", sim_parameters, a0_array, y_axis, z_axis, y_axis)
        plotting.plot_2d_colormap("electromagnetic", sim_parameters, a0_array, y_axis, z_axis, z_axis)'''
        
        # ------------------------------------------------------- #
        
        #Properties for the electromagneteic mode
        sim_parameters = sim_init.SimParameters(i, r_min, r_max, num_part, tf, steps_electromag, first_eighth,
            substeps_electromag, thread_num, all_states, rotate_angle, sweep_steps, trajectory_until_exit, wavelength, c) 
        
        #Uncomment to check the propagation vector, epsilon1, and epsilon2 for all lasers
        #programs.check_laser_polarization("electromagnetic", sim_parameters, lasers)
        
        programs.run_simulation("electromagnetic", sim_parameters, lasers)
        
        programs.find_final_p("electromagnetic", sim_parameters, x_axis, x_axis)
        programs.find_max_p("electromagnetic", sim_parameters, x_axis)
        
        programs.find_final_p("electromagnetic", sim_parameters, x_axis, y_axis)
        programs.find_max_p("electromagnetic", sim_parameters, y_axis)
        #programs.find_enter_exit_time("electromagnetic", sim_parameters, x_axis, y_axis)
        
        programs.find_final_p("electromagnetic", sim_parameters, x_axis, z_axis)
        programs.find_max_p("electromagnetic", sim_parameters, z_axis)
        
        programs.check_convergence("electromagnetic", sim_parameters, lasers, x_axis, x_axis, 2)
        
        #plotting.plot_time_momentum("electromagnetic", sim_parameters, a0_array, x_axis, y_axis)
        #plotting.plot_enter_exit_time("electromagnetic", sim_parameters, a0_array, y_axis, y_axis)
        #plotting.plot_phases("electromagnetic", sim_parameters, a0_array, x_axis, y_axis)
        
        # ------------------------------------------------------- #
        
        #Properties for the ponderomotive mode
        sim_parameters = sim_init.SimParameters(i, r_min, r_max, num_part, tauf, steps_pond, first_eighth,
            substeps_pond, thread_num, all_states, rotate_angle, sweep_steps, full_trajectory, wavelength, c)
        
        programs.run_simulation("ponderomotive", sim_parameters, lasers)
        
        programs.find_final_p("ponderomotive", sim_parameters, x_axis, x_axis)
        programs.find_max_p("ponderomotive", sim_parameters, x_axis)
        
        programs.find_final_p("ponderomotive", sim_parameters, x_axis, y_axis)
        programs.find_max_p("ponderomotive", sim_parameters, y_axis)
        #programs.find_enter_exit_time("ponderomotive", sim_parameters, y_axis, y_axis)
        
        programs.find_final_p("ponderomotive", sim_parameters, x_axis, z_axis)
        programs.find_max_p("ponderomotive", sim_parameters, z_axis)
        
        #programs.check_convergence("ponderomotive", sim_parameters, lasers, x_axis, y_axis, 2)
        
        #plotting.plot_time_momentum("ponderomotive", sim_parameters, a0_array, y_axis, y_axis)
        #plotting.plot_enter_exit_time("ponderomotive", sim_parameters, a0_array, y_axis, y_axis)
        #plotting.plot_phases("ponderomotive", sim_parameters, a0_array, y_axis, y_axis)'
        
        # ------------------------------------------------------- #
        
        programs.calculate_errors(sim_parameters, a0_array, x_axis)
        programs.calculate_errors(sim_parameters, a0_array, y_axis)
        programs.calculate_errors(sim_parameters, a0_array, z_axis)
        
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
    
    plotting.plot_convergence("electromagnetic", a0_array, x_axis)
    plotting.plot_2d_convergence_heatmap("electromagnetic", sim_parameters, a0_array, x_axis, x_axis)
    
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
    #create_video.create_2d_colormap_video("electromagnetic", framerate, y_axis, z_axis, y_axis)
    #create_video.create_phase_video("electromagnetic", framerate, x_axis, y_axis)
    #create_video.create_time_momentum_video("electromagnetic", framerate, x_axis, y_axis)
    
    #Uncomment to remove images if you created a video
    #programs.clean_image_folder()
    
    total_time = time.time() - start_time
    print(f"Program executed successfully.")
    print(f"Total time taken: {total_time:0.3f}s.\a")