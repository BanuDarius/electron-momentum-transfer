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
from pathlib import Path
import scripts.common as common
import scripts.sim_init as sim_init
import scripts.programs as programs
import scripts.plotting as plotting

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "output"

c = 137.036

all_states = False
final_states = True

def run_performance_test(method, sim_parameters, lasers, thread_num_final):
    a0_array = np.array([])
    programs.clean_output_folder()
    sim_parameters.thread_num = 1
    i = 1
    
    while(i <= thread_num_final):
        start_time = time.time()
        programs.run_simulation(method, sim_parameters, lasers)
        
        total_time = time.time() - start_time
        print(f"Time taken with {sim_parameters.thread_num} threads: {total_time:0.3f}s.")
        
        with open(f"{OUTPUT_DIR}/performance.bin", "ab") as file:
            file.write(np.double(sim_parameters.thread_num))
            file.write(np.double(total_time))
        
        i *= 2
        sim_parameters.thread_num = i
    
    plotting.plot_performance()
    
    print(f"Performance test executed successfully.\a")
    exit(0)

def run_example_performance_test(thread_num_final):
    i = 1
    a0 = 0.50
    zetax = 0.0
    zetay = 1.0
    tf = 10000.0
    num_part = 8000
    omega = 0.057
    etaf = 0.0 * np.pi
    sigma = 19.0 * np.pi
    psi = -4.0 * sigma
    wavelength = 2.0 * np.pi * c / omega
    r_min = -1.00 * wavelength
    r_max = +1.00 * wavelength
    phi = np.radians(90.0)
    theta = np.radians(0.0)
    alpha = np.radians(0.0)
    rotate_angle = np.radians(0.0)
    steps_electromag = 64000
    substeps_electromag = 640
    pond_integrate_steps = 4
    v0_mag = 0.0 * c
    phi_v0 = np.radians(0.0)
    theta_v0 = np.radians(0.0)
    steps_electromag = common.modulo_steps(steps_electromag, substeps_electromag)
    
    use_gaussian = False
    w0 = 5.0
    zeta_x_gauss = [ 1.0, 0.0 ]
    zeta_y_gauss = [ 0.0, 0.0 ]

    programs.clean_output_folder()
    
    lasers = []
    lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(0.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
    lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(180.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
    lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(60.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
    lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(300.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
    lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(45.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))
    lasers.append(sim_init.LaserParameters(a0, sigma, omega, etaf, zetax, zetay, alpha, phi, np.radians(90.0), psi, pond_integrate_steps, use_gaussian, w0, zeta_x_gauss, zeta_y_gauss))

    sim_parameters = sim_init.SimParameters(i, r_min, r_max, num_part, tf, steps_electromag, substeps_electromag, v0_mag, phi_v0, theta_v0, 1, all_states, rotate_angle, 1, wavelength, c)
    
    while(i <= thread_num_final):
        start_time = time.time()
        programs.run_simulation("electromagnetic", sim_parameters, lasers)
        total_time = time.time() - start_time
        
        print(f"Time taken with {sim_parameters.thread_num} threads: {total_time:0.3f}s.")
        
        with open(f"{OUTPUT_DIR}/performance.bin", "ab") as file:
            file.write(np.double(sim_parameters.thread_num))
            file.write(np.double(total_time))
        
        i *= 2
        sim_parameters.thread_num = i
        
    plotting.plot_performance()
    
    print(f"Example performance test executed successfully.\a")
    exit(0)