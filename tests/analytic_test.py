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

import os
import time
import numpy as np
from pathlib import Path
import scripts.common as common
import scripts.sim_init as sim_init
import scripts.programs as programs
import scripts.plotting as plotting

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "output"

c = 137.036

x_axis = 0
y_axis = 1
z_axis = 2

all_states = False
final_states = True
full_trajectory = True
trajectory_until_exit = False

# ------------------------------------------------------- #

thread_num = 1
max_tf = 100000.0
min_a0 = 0.02
max_a0 = 10.00
a0_dt = 2.0
zetax = 1.0
zetay = 0.0
num_part = 1
sweep_steps = 128
omega = 0.057
etaf = 8.0 * np.pi
sigma = 19.0 * np.pi
psi = -6.0 * sigma
wavelength = 2.0 * np.pi * c / omega
r = 1.00 * wavelength
phi = np.radians(60.0)
theta = np.radians(0.0)
alpha = np.radians(0.0)
rotate_angle = np.radians(0.0)
steps_electromag = 100000
min_steps_dt = 8000
max_steps_dt = 100000
substeps_electromag = 1
pond_integrate_steps = 4
phi_v0 = np.radians(90.0)
theta_v0 = np.radians(0.0)

use_gaussian = False
w0 = 5.0
zeta_x_gauss = [ 1.0, 0.0 ]
zeta_y_gauss = [ 0.0, 0.0 ]

# ------------------------------------------------------- #

def run_complete_test(v0_mag):
    programs.clean_output_folder()
    a0_array = np.array([])
    dt_array = np.array([])
    
    for i in range(0, sweep_steps):
        a0 = common.interpolate(min_a0, max_a0, i, sweep_steps)
        a0_array = np.append(a0_array, a0)
        
        lasers = []
        lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, theta, psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
        
        sim_parameters = sim_init.SimParameters(i, r, r, num_part, max_tf, steps_electromag, substeps_electromag, v0_mag, phi_v0, theta_v0, thread_num, all_states, rotate_angle, sweep_steps, wavelength, c)
        
        sim_parameters.output_final_pos = True
        
        programs.check_analytic_solution("electromagnetic", sim_parameters, lasers)
        
        if(v0_mag < 1e-3):
            pos_i = programs.spherical_coordinates(r, np.radians(90.0), rotate_angle)
            programs.calculate_displacement_error(sim_parameters, pos_i, phi, theta)
        
        if(i % 8 == 0):
            plotting.plot_trajectory_comparison(sim_parameters, lasers, x_axis)
            plotting.plot_trajectory_comparison(sim_parameters, lasers, y_axis)
            plotting.plot_trajectory_comparison(sim_parameters, lasers, z_axis)
        
        print(f"Ended a0 sweep step: {i+1}/{sweep_steps}.")
        
        # ------------------------------------------------------- #
        
    plotting.plot_final_position_comparison(a0_array, sim_parameters, x_axis)
    plotting.plot_final_position_comparison(a0_array, sim_parameters, y_axis)
    plotting.plot_final_position_comparison(a0_array, sim_parameters, z_axis)
    
    if(v0_mag < 1e-3):
        plotting.plot_analytic_errors(a0_array, sim_parameters)
        programs.check_passed_comparison_test(sim_parameters)
        
    programs.clean_output_folder()
    
    for i in range(0, sweep_steps):
        current_steps = int(common.interpolate(min_steps_dt, max_steps_dt, i, sweep_steps))
        current_steps = common.modulo_steps(current_steps, substeps_electromag)
        
        lasers = []
        lasers.append(sim_init.LaserParameters(a0_dt, sigma, omega, etaf, zetax, zetay, alpha, phi, theta, psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
        
        current_dt = max_tf / current_steps
        dt_array = np.append(dt_array, current_dt)
        
        sim_parameters = sim_init.SimParameters(i, r, r, num_part, max_tf, current_steps, substeps_electromag, v0_mag, phi_v0, theta_v0, thread_num, all_states, rotate_angle, sweep_steps, wavelength, c)
        
        sim_parameters.output_final_pos = True
        
        programs.check_analytic_solution("electromagnetic", sim_parameters, lasers)
        
        if v0_mag < 1e-3:
            pos_i = programs.spherical_coordinates(r, np.radians(90.0), rotate_angle)
            programs.calculate_displacement_error(sim_parameters, pos_i, phi, theta)
        
        print(f"Ended dt sweep step: {i+1}/{sweep_steps}")
        
        # ------------------------------------------------------- #
        
    if v0_mag < 1e-3:
        plotting.plot_analytic_errors_dt(dt_array, sim_parameters)
        programs.check_passed_comparison_test(sim_parameters)
        
    print(f"Completed analytical comparison test.")
    exit(0)