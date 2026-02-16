import sys
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
filename_out = f"{OUTPUT_DIR}/out-data.bin"

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

def run_quick_example(core_num):
    min_a0 = 0.02
    max_a0 = 1.00
    zetax = 0.0
    zetay = 1.0
    min_tf = 10000.0
    max_tf = 16000.0
    tauf = 7000.0
    num_part = 128
    sweep_steps = 128
    omega = 0.057
    xif = 0.0 * np.pi
    sigma = 19.0 * np.pi
    psi = -3.0 * sigma
    wavelength = 2.0 * np.pi * c / omega
    r_min = -1.00 * wavelength
    r_max = +1.00 * wavelength
    phi = np.radians(90.0)
    rotate_angle = np.radians(90.0)
    min_steps_pond = 128
    max_steps_pond = 512
    min_steps_electromag = 4000
    max_steps_electromag = 16000
    substeps_pond = 1
    substeps_electromag = 16
    pond_integrate_steps = 4
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
        lasers.append(sim_init.LaserParameters(a0, sigma, omega, xif, zetax, zetay, phi, np.radians(90.0), psi, pond_integrate_steps))
        lasers.append(sim_init.LaserParameters(a0, sigma, omega, xif, zetax, zetay, phi, np.radians(270.0), psi, pond_integrate_steps))
        
        # ------------------------------------------------------- #
        
        sim_parameters = sim_init.SimParameters(i, r_min, r_max, num_part, tf, steps_electromag, first_eighth,
            substeps_electromag, core_num, all_states, rotate_angle, sweep_steps, full_trajectory, wavelength, c)
        
        programs.run_simulation("electromagnetic", sim_parameters, lasers)
        
        programs.find_final_p("electromagnetic", sim_parameters, y_axis, x_axis)
        programs.find_max_p("electromagnetic", sim_parameters, x_axis)
        
        programs.find_final_p("electromagnetic", sim_parameters, y_axis, y_axis)
        programs.find_max_p("electromagnetic", sim_parameters, y_axis)
        
        programs.find_final_p("electromagnetic", sim_parameters, y_axis, z_axis)
        programs.find_max_p("electromagnetic", sim_parameters, z_axis)
        
        # ------------------------------------------------------- #
        
        sim_parameters = sim_init.SimParameters(i, r_min, r_max, num_part, tauf, steps_pond, first_eighth,
            substeps_pond, core_num, all_states, rotate_angle, sweep_steps, full_trajectory, wavelength, c)
        
        programs.run_simulation("ponderomotive", sim_parameters, lasers)
        
        programs.find_final_p("ponderomotive", sim_parameters, y_axis, x_axis)
        programs.find_max_p("ponderomotive", sim_parameters, x_axis)
        
        programs.find_final_p("ponderomotive", sim_parameters, y_axis, y_axis)
        programs.find_max_p("ponderomotive", sim_parameters, y_axis)
        
        programs.find_final_p("ponderomotive", sim_parameters, y_axis, z_axis)
        programs.find_max_p("ponderomotive", sim_parameters, z_axis)
        
        # ------------------------------------------------------- #
        
        programs.calculate_errors(sim_parameters, a0_array, x_axis)
        programs.calculate_errors(sim_parameters, a0_array, y_axis)
        programs.calculate_errors(sim_parameters, a0_array, z_axis)
        
        print(f"Ended parameter sweep step: {i+1}/{sweep_steps}.")
        
        # ------------------------------------------------------- #
        
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
    print(f"Ended quick example parameter sweep.")
    sys.exit(0)