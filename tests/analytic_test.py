import time
import numpy as np
from pathlib import Path
import scripts.common as common
import scripts.sim_init as sim_init
import scripts.programs as programs
import scripts.plotting as plotting
    
c = 137.036

x_pos_axis = -4
y_pos_axis = -3
z_pos_axis = -2

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

thread_num = 1
min_a0 = 0.02
max_a0 = 5.00
zetax = 0.0
zetay = 1.0
tf = 20000.0
num_part = 1
sweep_steps = 128
omega = 0.057
xif = 8.0 * np.pi
sigma = 19.0 * np.pi
psi = -4.0 * sigma
wavelength = 2.0 * np.pi * c / omega
r = 1.00 * wavelength
phi = np.radians(60.0)
theta = np.radians(0.0)
alpha = np.radians(0.0)
rotate_angle = np.radians(0.0)
steps_electromag = 16000
substeps_electromag = 1
pond_integrate_steps = 4

# ------------------------------------------------------- #

def run_complete_test():
    a0_array = np.array([])
    
    for i in range(0, sweep_steps):
        a0 = common.interpolate(min_a0, max_a0, i, sweep_steps)
        a0_array = np.append(a0_array, a0)
        
        lasers = []
        lasers.append(sim_init.LaserParameters(a0, sigma, omega, xif, zetax, zetay, alpha, phi, theta, psi, pond_integrate_steps))
        
        sim_parameters = sim_init.SimParameters(i, r, r, num_part, tf, steps_electromag, first_eighth,
            substeps_electromag, thread_num, all_states, rotate_angle, sweep_steps, full_trajectory, wavelength, c) 
            
        programs.check_analytic_solution("electromagnetic", sim_parameters, lasers)
        
        programs.find_final_p("electromagnetic", sim_parameters, x_axis, x_pos_axis)
        programs.find_final_p("electromagnetic", sim_parameters, x_axis, y_pos_axis)
        programs.find_final_p("electromagnetic", sim_parameters, x_axis, z_pos_axis)
        
        programs.find_final_p("analytic", sim_parameters, x_axis, x_pos_axis)
        programs.find_final_p("analytic", sim_parameters, x_axis, y_pos_axis)
        programs.find_final_p("analytic", sim_parameters, x_axis, z_pos_axis)
        
        #pos_i = programs.spherical_coordinates(r, np.radians(90.0), rotate_angle)
        #programs.calculate_displacement_error(sim_parameters, pos_i, phi, theta)
        
        if(i % 8 == 0):
            plotting.plot_trajectory_comparison(sim_parameters, lasers, x_axis)
            plotting.plot_trajectory_comparison(sim_parameters, lasers, y_axis)
            plotting.plot_trajectory_comparison(sim_parameters, lasers, z_axis)
        
        #programs.calculate_errors_analytic("electromagnetic", sim_parameters, x_axis)
        #programs.calculate_errors_analytic("electromagnetic", sim_parameters, y_axis)
        #programs.calculate_errors_analytic("electromagnetic", sim_parameters, z_axis)
        
        print(f"Ended parameter sweep step: {i+1}/{sweep_steps}.")
        
        # ------------------------------------------------------- #
    
    plotting.plot_final_position_comparison(a0_array, sim_parameters, x_axis)
    plotting.plot_final_position_comparison(a0_array, sim_parameters, y_axis)
    plotting.plot_final_position_comparison(a0_array, sim_parameters, z_axis)
    
    print(f"Completed analytical comparison test.")
    exit()