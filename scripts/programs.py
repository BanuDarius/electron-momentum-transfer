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

def run_simulation(method, sim_parameters, lasers):
    if method == "electromagnetic":
        mode = 0
    elif method == "ponderomotive":
        mode = 1
    elif method == "electromagnetic-rk4":
        mode = 2

    sim_parameters.mode = mode    
    program_path = f"{BIN_DIR}/laser_electron"
    filename_out = sim_parameters.filename_out
    
    common.output_all_parameters(sim_parameters, lasers)
    
    arguments = [program_path, sim_parameters.filename_parameters, sim_parameters.filename_lasers, filename_out]
    
    try:
        res = subprocess.run(arguments, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        sys.exit(1)

# ----------------------------------------------------------------------- #

def check_convergence(method, sim_parameters, lasers, axis_pos, axis_p, multiplier):
    if(method == "electromagnetic"):
        mode = "electromag"
    else:
        mode = "pond"
    axis_text_p = common.get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    num = sim_parameters.num
    
    filename_final_1 = f"{OUTPUT_DIR}/out-final-p{lowercase_text_p}-{mode}.bin"
    filename_final_2 = f"{OUTPUT_DIR}/out-final-p{lowercase_text_p}-{mode}-conv.bin"
    filename_out_conv = f"{OUTPUT_DIR}/out-data-conv-{mode}-{lowercase_text_p}.bin"
    filename_conv_average = f"{OUTPUT_DIR}/average-conv-{mode}-{lowercase_text_p}.bin"
    filename_conv_all = f"{OUTPUT_DIR}/average-conv-all-{mode}-{lowercase_text_p}.bin"
    
    filename_conv = f"{OUTPUT_DIR}/conv.bin"
    program_conv = f"{BIN_DIR}/error_calc"
    
    sim_parameters.steps = sim_parameters.steps * multiplier
    sim_parameters.filename_out = filename_out_conv
    sim_parameters.check_convergence = True
    
    run_simulation(method, sim_parameters, lasers)
    find_final_p(method, sim_parameters, axis_pos, axis_p)
    find_max_p(method, sim_parameters, axis_p)
    
    arguments = [program_conv, num, filename_final_1, filename_final_2, filename_conv, filename_conv_average, filename_conv_all]
    arguments = [str(x) for x in arguments]
    
    try:
        res = subprocess.run(arguments, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        sys.exit(1)
        
# ----------------------------------------------------------------------- #

def find_enter_exit_time(method, sim_parameters, axis_pos, axis_p):
    if(method == "electromagnetic"):
        mode = "electromag"
    else:
        mode = "pond"
    axis_text_pos = common.get_axis_text(axis_pos)
    lowercase_text_pos = axis_text_pos.lower()
    
    axis_text_p = common.get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    filename_out = f"{OUTPUT_DIR}/out-enter-exit-time-{mode}-{lowercase_text_pos}{lowercase_text_p}.bin"
    
    program_enter_exit = f"{BIN_DIR}/find_enter_exit_time"
    filename = sim_parameters.filename_out
    
    num = sim_parameters.num
    steps_final = sim_parameters.steps // sim_parameters.substeps
    
    arguments = [program_enter_exit, filename, num, steps_final, axis_pos, axis_p, filename_out]
    arguments = [str(x) for x in arguments]
    
    try:
        res = subprocess.run(arguments, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        sys.exit(1)
        
# ----------------------------------------------------------------------- #

def find_max_p(method, sim_parameters, axis):
    if(method == "electromagnetic"):
        mode = "electromag"
    else:
        mode = "pond"
    
    if(sim_parameters.check_convergence):
        mode = mode + "-conv"
        
    axis_text = common.get_axis_text(axis)
    lowercase_text = axis_text.lower()
    
    filename_in = f"{OUTPUT_DIR}/out-final-p{lowercase_text}-{mode}.bin"
    filename_out = f"{OUTPUT_DIR}/out-max-p{lowercase_text}-{mode}.bin"
    
    program_path = f"{BIN_DIR}/find_max_p"
    
    index = sim_parameters.i
    num = sim_parameters.num
    steps_final = sim_parameters.steps // sim_parameters.substeps
    
    arguments = [program_path, filename_in, num, steps_final, filename_out]
    arguments = [str(x) for x in arguments]
    
    try:
        res = subprocess.run(arguments, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        sys.exit(1)
    
# ----------------------------------------------------------------------- #

def find_final_p(method, sim_parameters, axis_pos, axis_p):
    read_num = 8
    filename = sim_parameters.filename_out
    
    if(method == "electromagnetic"):
        mode = "electromag"
    elif(method == "ponderomotive"):
        mode = "pond"
    else:
        mode = "analytic"
        filename = f"{OUTPUT_DIR}/out-data-analytic.bin"
        read_num = 4
    
    if(sim_parameters.check_convergence):
        mode = mode + "-conv"
    
    if(axis_p < 0):
        axis_text_p = common.get_axis_text(axis_p + 4)
    else:
        axis_text_p = common.get_axis_text(axis_p)
    
    lowercase_text_p = axis_text_p.lower()
    filename_out = f"{OUTPUT_DIR}/out-final-p{lowercase_text_p}-{mode}.bin"
    filename_out_all = f"{OUTPUT_DIR}/out-final-p{lowercase_text_p}-all-{mode}.bin"
    
    program_path = f"{BIN_DIR}/find_final_p"
    
    num = sim_parameters.num
    steps_final = sim_parameters.steps // sim_parameters.substeps
    
    arguments = [program_path, filename, num, steps_final, axis_pos, axis_p, read_num, filename_out, filename_out_all]
    arguments = [str(x) for x in arguments]
    
    try:
        res = subprocess.run(arguments, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        sys.exit(1)

# ----------------------------------------------------------------------- #

def calculate_errors(sim_parameters, a0_array, axis):
    axis_text = common.get_axis_text(axis)
    lowercase_text = axis_text.lower()
    
    filename = sim_parameters.filename_out
    program_path = f"{BIN_DIR}/error_calc"
    filename_in_a = f"{OUTPUT_DIR}/out-final-p{lowercase_text}-electromag.bin"
    filename_in_b = f"{OUTPUT_DIR}/out-final-p{lowercase_text}-pond.bin"
    filename_out = f"{OUTPUT_DIR}/out-error-{lowercase_text}.bin"
    filename_out_average_error = f"{OUTPUT_DIR}/out-average-error-{lowercase_text}.bin"
    filename_out_error_all = f"{OUTPUT_DIR}/out-error-all-{lowercase_text}.bin"
    
    num = sim_parameters.num
    
    arguments = [program_path, num, filename_in_a, filename_in_b, filename_out, filename_out_average_error, filename_out_error_all]
    arguments = [str(x) for x in arguments]
    
    try:
        res = subprocess.run(arguments, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        sys.exit(1)

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
    filename_out_displacement = f"{OUTPUT_DIR}/out-displacement.bin"
    
    common.output_all_parameters(sim_parameters, lasers)
    
    arguments = [program_path, sim_parameters.filename_parameters, sim_parameters.filename_lasers, filename_out, filename_out_displacement]
    
    try:
        res = subprocess.run(arguments, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        sys.exit(1)
    
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
    filename_final_pos_numeric_x = f"{OUTPUT_DIR}/out-final-px-electromag.bin"
    filename_final_pos_numeric_y = f"{OUTPUT_DIR}/out-final-py-electromag.bin"
    filename_final_pos_numeric_z = f"{OUTPUT_DIR}/out-final-pz-electromag.bin"
    
    data_analytic = np.fromfile(filename_displacement_analytic, dtype=np.float64).reshape(-1, 1)
    data_x = np.fromfile(filename_final_pos_numeric_x, dtype=np.float64).reshape(1, 2)
    data_y = np.fromfile(filename_final_pos_numeric_y, dtype=np.float64).reshape(1, 2)
    data_z = np.fromfile(filename_final_pos_numeric_z, dtype=np.float64).reshape(1, 2)
    
    x = data_x[0, 1]
    y = data_y[0, 1]
    z = data_z[0, 1]
    pos_f_numeric = np.array([x, y, z])
    
    displacement = data_analytic[i, 0]
    pos_f_analytic = pos_i + spherical_coordinates(displacement, phi, theta)
    
    analytic_error = np.linalg.norm(pos_f_analytic - pos_f_numeric) / np.linalg.norm(pos_f_analytic) * 100.0
    
    filename_error = f"{OUTPUT_DIR}/analytic_error.bin"
    with open(filename_error, "ab") as file:
        analytic_error.tofile(file)

# ----------------------------------------------------------------------- #

def check_passed_comparison_test(sim_parameters):
    i = sim_parameters.i
    
    filename = f"{OUTPUT_DIR}/analytic_error.bin"
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
    sys.exit(0)

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