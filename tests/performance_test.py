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
first_eighth = 8
first_quarter = 4
all_states = False
final_states = True
full_trajectory = True
trajectory_until_exit = False

def run_performance_test(method, sim_parameters, lasers, thread_num_final):
    a0_array = np.array([])
    programs.clean_output_folder()
    sim_parameters.thread_num = 1
    i = 1
    
    while(sim_parameters.thread_num <= thread_num_final):
        start_time = time.time()
        programs.run_simulation(method, sim_parameters, lasers)
        
        total_time = time.time() - start_time
        print(f"Time taken with {sim_parameters.thread_num} threads: {total_time:0.3f}s.")
        
        with open(f"{OUTPUT_DIR}/performance.bin", "ab") as file:
            file.write(np.double(sim_parameters.thread_num))
            file.write(np.double(total_time))
        
        sim_parameters.thread_num = 2 * i
        i += 1
        
        # ------------------------------------------------------- #
    
    plotting.plot_performance()
    
    print(f"Performance test executed successfully.\a")
    exit()

def run_example_performance_test(thread_num_final):
    i = 1
    a0 = 0.50
    zetax = 0.0
    zetay = 1.0
    tf = 10000.0
    num_part = 32000
    omega = 0.057
    xif = 0.0 * np.pi
    sigma = 19.0 * np.pi
    psi = -4.0 * sigma
    wavelength = 2.0 * np.pi * c / omega
    r_min = -1.00 * wavelength
    r_max = +1.00 * wavelength
    phi = np.radians(90.0)
    theta = np.radians(0.0)
    alpha = np.radians(0.0)
    rotate_angle = np.radians(0.0)
    steps_electromag = 16000
    substeps_electromag = 320
    pond_integrate_steps = 4
    v0_mag = 0.0 * c
    phi_v0 = np.radians(0.0)
    theta_v0 = np.radians(0.0)
    square_size = 1.0
    steps_electromag = common.modulo_steps(steps_electromag, substeps_electromag)

    programs.clean_output_folder()
    
    lasers = []
    lasers.append(sim_init.LaserParameters(a0, sigma, omega, xif, zetax, zetay, alpha, phi, np.radians(0.0), psi, pond_integrate_steps))
    lasers.append(sim_init.LaserParameters(a0, sigma, omega, xif, zetax, zetay, alpha, phi, np.radians(180.0), psi, pond_integrate_steps))

    sim_parameters = sim_init.SimParameters(i, r_min, r_max, num_part, tf, steps_electromag, first_eighth,
        substeps_electromag, v0_mag, phi_v0, theta_v0, i, all_states, rotate_angle, i, full_trajectory, wavelength, c)
    
    while(sim_parameters.thread_num <= thread_num_final):
        start_time = time.time()
        programs.run_simulation("electromagnetic", sim_parameters, lasers)
        
        total_time = time.time() - start_time
        print(f"Time taken with {sim_parameters.thread_num} threads: {total_time:0.3f}s.")
        
        with open(f"{OUTPUT_DIR}/performance.bin", "ab") as file:
            file.write(np.double(sim_parameters.thread_num))
            file.write(np.double(total_time))
        
        sim_parameters.thread_num = 2 * i
        i += 1
        
        # ------------------------------------------------------- #
    
    plotting.plot_performance()
    
    print(f"Performance test executed successfully.\a")
    exit()