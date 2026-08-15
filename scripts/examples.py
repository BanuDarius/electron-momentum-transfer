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

import sys
import time
import numpy as np
from pathlib import Path
import scripts.common as common
import scripts.sim_init as sim_init
import scripts.programs as programs
import scripts.plotting as plotting
import scripts.create_video as create_video

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
filename_out = f"{OUTPUT_DIR}/out-data.bin"

c = 137.036

x_axis = 0
y_axis = 1
z_axis = 2

framerate = 3
first_eighth = 8
first_quarter = 4
all_particles = 1

all_states = False
final_states = True
full_trajectory = True
trajectory_until_exit = False

def run_example(example_num, thread_num):
    if(example_num == 1):
        min_a0 = 0.02
        max_a0 = 1.00
        zetax = 0.0
        zetay = 1.0
        min_tf = 10000.0
        max_tf = 16000.0
        tauf = 7000.0
        num_part = 1024
        sweep_steps = 1024
        omega = 0.057
        etaf = 0.0 * np.pi
        sigma = 19.0 * np.pi
        psi = -4.0 * sigma
        wavelength = 2.0 * np.pi * c / omega
        r_min = -1.00 * wavelength
        r_max = +1.00 * wavelength
        phi = np.radians(90.0)
        rotate_angle = np.radians(90.0)
        alpha = np.radians(0.0)
        min_steps_pond = 128
        max_steps_pond = 512
        min_steps_electromag = 4000
        max_steps_electromag = 16000
        substeps_pond = 1
        substeps_electromag = 16
        pond_integrate_steps = 4
        v0_mag = 0.0 * c
        phi_v0 = np.radians(0.0)
        theta_v0 = np.radians(0.0)
        
        use_gaussian = False
        w0 = 5.0
        zeta_x_gauss = [ 1.0, 0.0 ]
        zeta_y_gauss = [ 0.0, 0.0 ]
        axis_i = y_axis
    elif(example_num == 2):
        min_a0 = 0.02
        max_a0 = 0.50
        zetax = 0.0
        zetay = 1.0
        min_tf = 10000.0
        max_tf = 16000.0
        tauf = 7000.0
        num_part = 1024
        sweep_steps = 1024
        omega = 0.057
        etaf = 0.0 * np.pi
        sigma = 19.0 * np.pi
        psi = -4.0 * sigma
        wavelength = 2.0 * np.pi * c / omega
        r_min = -1.00 * wavelength
        r_max = +1.00 * wavelength
        phi = np.radians(90.0)
        rotate_angle = np.radians(90.0)
        alpha = np.radians(0.0)
        min_steps_pond = 128
        max_steps_pond = 512
        min_steps_electromag = 4000
        max_steps_electromag = 16000
        substeps_pond = 1
        substeps_electromag = 16
        pond_integrate_steps = 4
        v0_mag = 0.0 * c
        phi_v0 = np.radians(0.0)
        theta_v0 = np.radians(0.0)
        
        use_gaussian = False
        w0 = 5.0
        zeta_x_gauss = [ 1.0, 0.0 ]
        zeta_y_gauss = [ 0.0, 0.0 ]
        axis_i = y_axis
    elif(example_num == 3):
        min_a0 = 0.05
        max_a0 = 0.50
        zetax = 1.0 / np.sqrt(2)
        zetay = 1.0 / np.sqrt(2)
        min_tf = 10000.0
        max_tf = 16000.0
        tauf = 7000.0
        num_part = 1024
        sweep_steps = 1024
        omega = 0.057
        etaf = 0.0 * np.pi
        sigma = 19.0 * np.pi
        psi = -4.0 * sigma
        wavelength = 2.0 * np.pi * c / omega
        r_min = 0.00 * wavelength
        r_max = 1.00 * wavelength
        phi = np.radians(90.0)
        rotate_angle = np.radians(90.0)
        alpha = np.radians(0.0)
        min_steps_pond = 128
        max_steps_pond = 512
        min_steps_electromag = 4000
        max_steps_electromag = 16000
        substeps_pond = 1
        substeps_electromag = 16
        pond_integrate_steps = 4
        v0_mag = 0.0 * c
        phi_v0 = np.radians(0.0)
        theta_v0 = np.radians(0.0)
        
        use_gaussian = False
        w0 = 5.0
        zeta_x_gauss = [ 1.0, 0.0 ]
        zeta_y_gauss = [ 0.0, 0.0 ]
        axis_i = y_axis
    elif(example_num == 4):
        min_a0 = 0.02
        max_a0 = 0.50
        zetax = 0.0
        zetay = 1.0
        min_tf = 8000.0
        max_tf = 14000.0
        tauf = 7000.0
        num_part = 1024
        sweep_steps = 1024
        omega = 0.057
        etaf = 0.0 * np.pi
        sigma = 19.0 * np.pi
        psi = -4.0 * sigma
        wavelength = 2.0 * np.pi * c / omega
        r_min = -1.00 * wavelength
        r_max = +1.00 * wavelength
        phi = np.radians(90.0)
        theta = np.radians(90.0)
        alpha = np.radians(0.0)
        rotate_angle = np.radians(0.0)
        min_steps_pond = 128
        max_steps_pond = 512
        min_steps_electromag = 4000
        max_steps_electromag = 16000
        substeps_pond = 1
        substeps_electromag = 16
        pond_integrate_steps = 4
        v0_mag = 0.0 * c
        phi_v0 = np.radians(0.0)
        theta_v0 = np.radians(0.0)
        
        use_gaussian = False
        w0 = 5.0
        zeta_x_gauss = [ 1.0, 0.0 ]
        zeta_y_gauss = [ 0.0, 0.0 ]
        axis_i = x_axis
    else:
        print("Error: Example number not found.")
        exit()
        
    start_time = time.time()
    a0_array = np.array([])
    programs.clean_output_folder()
    
    for i in range(0, sweep_steps):
        tf = common.interpolate(min_tf, max_tf, i, sweep_steps)
        a0 = common.interpolate(min_a0, max_a0, i, sweep_steps)
        steps_electromag = int(common.interpolate(min_steps_electromag, max_steps_electromag, i, sweep_steps))
        steps_electromag = common.modulo_steps(steps_electromag, substeps_electromag)
        steps_pond = int(common.interpolate(min_steps_pond, max_steps_pond, i, sweep_steps))
        steps_pond = common.modulo_steps(steps_pond, substeps_pond)
        a0_array = np.append(a0_array, a0)
        
        lasers = []
        if(example_num == 1):
            lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(90.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
            lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(270.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
        elif(example_num == 2 or example_num == 3):
            lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(90.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
            lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(135.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
            lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(225.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
            lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(270.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
        else:
            lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(0.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
            lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(60.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
            lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(120.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
        
        # ------------------------------------------------------- #
        
        sim_parameters = sim_init.SimParameters(i, r_min, r_max, num_part, tf, steps_electromag, all_particles,
            substeps_electromag, v0_mag, phi_v0, theta_v0, thread_num, all_states, rotate_angle, sweep_steps, full_trajectory, wavelength, c)
        
        programs.run_simulation("electromagnetic", sim_parameters, lasers)
        
        # ------------------------------------------------------- 
        
        sim_parameters = sim_init.SimParameters(i, r_min, r_max, num_part, tauf, steps_pond, first_eighth,
            substeps_pond, v0_mag, phi_v0, theta_v0, thread_num, all_states, rotate_angle, sweep_steps, full_trajectory, wavelength, c)
        
        programs.run_simulation("ponderomotive", sim_parameters, lasers)
        
        # ------------------------------------------------------- 
        
        print(f"Ended parameter sweep step: {i+1}/{sweep_steps}.")
        
        # ------------------------------------------------------- #
    
    programs.calculate_errors(sim_parameters)
    
    plotting.plot_average_errors_all(a0_array)
    plotting.plot_max_p_all("electromagnetic", a0_array)
    plotting.plot_max_p_all("ponderomotive", a0_array)
    
    plotting.plot_2d_errors_heatmap_all(sim_parameters, a0_array, axis_i)
    plotting.plot_2d_heatmap_all("electromagnetic", sim_parameters, a0_array, axis_i)
    plotting.plot_2d_heatmap_all("ponderomotive", sim_parameters, a0_array, axis_i)
            
    total_time = time.time() - start_time
    print(f"Program executed successfully.")
    print(f"Total time taken: {total_time:0.3f}s.\a")
    print(f"Ended reproducing example {example_num}.")
    exit(0)

def replicate_prl_results(thread_num):
    min_a0 = 0.02
    max_a0 = 1.00
    zetax = 1.0
    zetay = 0.0
    min_tf = 1500.0
    max_tf = 1500.0
    tauf = 1500.0
    num_part = 1024
    sweep_steps = 1024
    omega = 0.057
    etaf = 50000.0 * np.pi
    sigma = 0.1 * np.pi
    psi = 0.0 * sigma
    wavelength = 2.0 * np.pi * c / omega
    r_min = -0.50 * wavelength
    r_max = +0.50 * wavelength
    phi = np.radians(90.0)
    rotate_angle = np.radians(0.0)
    alpha = np.radians(0.0)
    min_steps_pond = 128
    max_steps_pond = 256
    min_steps_electromag = 4000
    max_steps_electromag = 16000
    substeps_pond = 1
    substeps_electromag = 16
    pond_integrate_steps = 4
    v0_mag = 0.0 * c
    phi_v0 = np.radians(0.0)
    theta_v0 = np.radians(0.0)
    
    use_gaussian = False
    w0 = 5.0
    zeta_x_gauss = [ 1.0, 0.0 ]
    zeta_y_gauss = [ 0.0, 0.0 ]
    
    start_time = time.time()
    a0_array = np.array([])
    programs.clean_output_folder()
    
    for i in range(0, sweep_steps):
        tf = common.interpolate(min_tf, max_tf, i, sweep_steps)
        a0 = common.interpolate(min_a0, max_a0, i, sweep_steps)
        steps_electromag = int(common.interpolate(min_steps_electromag, max_steps_electromag, i, sweep_steps))
        steps_electromag = common.modulo_steps(steps_electromag, substeps_electromag)
        steps_pond = int(common.interpolate(min_steps_pond, max_steps_pond, i, sweep_steps))
        steps_pond = common.modulo_steps(steps_pond, substeps_pond)
        a0_array = np.append(a0_array, a0)
        
        lasers = []
        lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(0.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
        lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, np.radians(180.0), phi, np.radians(180.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
        
        # ------------------------------------------------------- #
        
        sim_parameters = sim_init.SimParameters(i, r_min, r_max, num_part, tf, steps_electromag, all_particles,
            substeps_electromag, v0_mag, phi_v0, theta_v0, thread_num, all_states, rotate_angle, sweep_steps, full_trajectory, wavelength, c)
        
        programs.run_simulation("electromagnetic", sim_parameters, lasers)
        
        #programs.check_laser_polarization("electromagnetic", sim_parameters, lasers)
        
        programs.check_convergence("electromagnetic", sim_parameters, lasers, 2)
        
        # ------------------------------------------------------- #
        
        sim_parameters = sim_init.SimParameters(i, r_min, r_max, num_part, tauf, steps_pond, first_eighth,
            substeps_pond, v0_mag, phi_v0, theta_v0, thread_num, all_states, rotate_angle, sweep_steps, full_trajectory, wavelength, c)
        
        programs.run_simulation("ponderomotive", sim_parameters, lasers)
        
        # ------------------------------------------------------- #
        
        print(f"Ended parameter sweep step: {i+1}/{sweep_steps}.")
        
        # ------------------------------------------------------- #
        
    programs.calculate_errors(sim_parameters)
    programs.calculate_convergence_errors("electromagnetic", sim_parameters)
    
    plotting.plot_average_errors_all(a0_array)
    plotting.plot_max_p_all("electromagnetic", a0_array)
    plotting.plot_max_p_all("ponderomotive", a0_array)
    
    plotting.plot_convergence("electromagnetic", a0_array, x_axis)
    plotting.plot_2d_convergence_heatmap("electromagnetic", sim_parameters, a0_array, x_axis, x_axis)
    
    plotting.plot_2d_errors_heatmap_all(sim_parameters, a0_array, x_axis)
    plotting.plot_2d_heatmap_all("electromagnetic", sim_parameters, a0_array, x_axis)
    plotting.plot_2d_heatmap_all("ponderomotive", sim_parameters, a0_array, x_axis)
            
    total_time = time.time() - start_time
    print(f"Program executed successfully.")
    print(f"Total time taken: {total_time:0.3f}s.\a")
    print("Ended reproducing PRL paper results.")
    exit(0)