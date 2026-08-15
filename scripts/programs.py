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
import sys
import subprocess
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import scripts.common as common

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BIN_DIR = PROJECT_ROOT / "bin"
INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_IMAGE_DIR = PROJECT_ROOT / "output-image"

# ----------------------------------------------------------------------- #

def run_simulation(method, sim_parameters, lasers, filename_final_p_custom=None, filename_max_p_custom=None):
    if method == "electromagnetic":
        mode = 0
        mode_text = "electromag"
    elif method == "ponderomotive":
        mode = 1
        mode_text = "pond"
    elif method == "electromagnetic-rk4":
        mode = 2
        mode_text = "electromag"
    else:
        print("Invalid simulation mode.")
        exit(1)
    sim_parameters.mode = mode
    
    program_path = f"{BIN_DIR}/laser_electron"
    
    filename_max_p = filename_max_p_custom if filename_max_p_custom else (OUTPUT_DIR / f"out-max-p-{mode_text}.bin")
    filename_final_p = filename_final_p_custom if filename_final_p_custom else (OUTPUT_DIR / f"out-final-p-{mode_text}.bin")
    filename_final_pos = OUTPUT_DIR / f"out-final-pos-{mode_text}.bin"
    filename_initial_pos = OUTPUT_DIR / f"out-initial-pos-{mode_text}.bin"
    
    common.output_all_parameters(sim_parameters, lasers)
    
    arguments = [program_path,sim_parameters.filename_parameters,sim_parameters.filename_lasers,sim_parameters.filename_out,filename_max_p,filename_final_p,filename_initial_pos,filename_final_pos]
    
    try:
        subprocess.run(arguments, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        exit(1)

# ----------------------------------------------------------------------- #

def check_convergence(method, sim_parameters, lasers, multiplier=2):
    if method == "electromagnetic":
        mode = "electromag"
    else:
        mode = "pond"
        
    filename_final_conv = OUTPUT_DIR / f"out-final-p-{mode}-conv.bin"
    filename_max_p_conv = OUTPUT_DIR / f"out-max-p-{mode}-conv.bin"
    
    sim_parameters.steps *= multiplier
    run_simulation(method, sim_parameters, lasers, filename_final_p_custom=filename_final_conv, filename_max_p_custom=filename_max_p_conv)
    sim_parameters.steps //= multiplier
        
# ----------------------------------------------------------------------- #

def calculate_errors(sim_parameters):
    num = sim_parameters.num
    sweep_steps = sim_parameters.sweep_steps
    
    program_path = f"{BIN_DIR}/error_calc"
    filename_in_b = f"{OUTPUT_DIR}/out-final-p-pond.bin"
    filename_in_a = f"{OUTPUT_DIR}/out-final-p-electromag.bin"
    filename_out_error_all = f"{OUTPUT_DIR}/out-error-all.bin"
    filename_out_average_error = f"{OUTPUT_DIR}/out-average-error.bin"
    
    arguments = [program_path, num, sweep_steps, filename_in_a, filename_in_b, filename_out_error_all, filename_out_average_error]
    arguments = [str(x) for x in arguments]
    
    try:
        res = subprocess.run(arguments, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        exit(1)

# ----------------------------------------------------------------------- #


def calculate_convergence_errors(method, sim_parameters):
    if method == "electromagnetic":
        mode = "electromag"
    else:
        mode = "pond"
        
    num = sim_parameters.num
    sweep_steps = sim_parameters.sweep_steps
    
    filename_final_1 = OUTPUT_DIR / f"out-final-p-{mode}.bin"
    filename_final_2 = OUTPUT_DIR / f"out-final-p-{mode}-conv.bin"
    filename_conv_all = OUTPUT_DIR / f"conv-all-{mode}.bin"
    filename_conv_avg = OUTPUT_DIR / f"average-conv-{mode}.bin"
    
    program_conv = f"{BIN_DIR}/error_calc"
    
    arguments = [program_conv, num, sweep_steps, filename_final_1, filename_final_2, filename_conv_all, filename_conv_avg]
    arguments = [str(x) for x in arguments]
    
    try:
        subprocess.run(arguments, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        exit(1)

# ----------------------------------------------------------------------- #

def check_analytic_solution(method, sim_parameters, lasers):
    if method == "electromagnetic":
        mode = 0
    elif method == "ponderomotive":
        mode = 1
    elif method == "electromagnetic-rk4":
        mode = 2
    
    sim_parameters.num = 1
    sim_parameters.substeps = 1
    sim_parameters.thread_num = 1
    sim_parameters.mode = mode
    lasers = [lasers[0]]
    
    run_simulation(method, sim_parameters, lasers)
    
    program_path = f"{BIN_DIR}/analytic_solution"
    filename_out = f"{OUTPUT_DIR}/out-data-analytic.bin"
    filename_out_final_pos = f"{OUTPUT_DIR}/out-final-pos-analytic.bin"
    filename_out_displacement = f"{OUTPUT_DIR}/out-displacement.bin"
    
    common.output_all_parameters(sim_parameters, lasers)
    
    arguments = [program_path, sim_parameters.filename_parameters, sim_parameters.filename_lasers, filename_out, filename_out_final_pos, filename_out_displacement]
    
    try:
        res = subprocess.run(arguments, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        exit(1)
    
# ----------------------------------------------------------------------- #

def spherical_coordinates(r, phi, theta):
    x = r * np.cos(theta) * np.sin(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(phi)
    pos = np.array([x, y, z])
    return pos

# ----------------------------------------------------------------------- #

def calculate_displacement_error(sim_parameters, pos_i, phi, theta):
    i = sim_parameters.i
    
    filename_displacement_analytic = f"{OUTPUT_DIR}/out-displacement.bin"
    filename_final_pos_numeric = f"{OUTPUT_DIR}/out-final-pos-electromag.bin"
    
    data_analytic = np.fromfile(filename_displacement_analytic, dtype=np.float64).reshape(-1, 1)
    data = np.fromfile(filename_final_pos_numeric, dtype=np.float64).reshape(-1, 3)
    
    x = data[i, 0]
    y = data[i, 1]
    z = data[i, 2]
    pos_f_numeric = np.array([x, y, z])
    
    displacement = data_analytic[i, 0]
    pos_f_analytic = pos_i + spherical_coordinates(displacement, phi, theta)
    
    analytic_error = np.linalg.norm(pos_f_analytic - pos_f_numeric) / np.linalg.norm(pos_f_analytic) * 100.0
    
    filename_error = f"{OUTPUT_DIR}/analytic-error.bin"
    with open(filename_error, "ab") as file:
        analytic_error.tofile(file)

# ----------------------------------------------------------------------- #

def check_passed_comparison_test(sim_parameters):
    i = sim_parameters.i
    
    filename = f"{OUTPUT_DIR}/analytic-error.bin"
    data = np.fromfile(filename, dtype=np.float64).reshape(-1, 1)
    final_error = data[i, 0]
    
    if(final_error < 1.0):
        print(f"PASSED!")
    else:
        print(f"FAILED!")
    
    print(f"Last relative error between analytic and numeric methods: {final_error:0.3f}%.")

# ----------------------------------------------------------------------- #

def check_laser_polarization(method, sim_parameters, lasers):
    sim_parameters.check_polarization = True
    run_simulation(method, sim_parameters, lasers)
    exit(1)

# ----------------------------------------------------------------------- #

def clean_output_folder():
    filenames = [f for f in os.listdir(OUTPUT_DIR)]
    for i in range(len(filenames)):
        os.remove(f"{OUTPUT_DIR}/{filenames[i]}")

# ----------------------------------------------------------------------- #

def clean_image_folder():
    filenames = [f for f in os.listdir(OUTPUT_IMAGE_DIR) if not f.startswith('_')]
    for i in range(len(filenames)):
        os.remove(f"{OUTPUT_IMAGE_DIR}/{filenames[i]}")

# ----------------------------------------------------------------------- #