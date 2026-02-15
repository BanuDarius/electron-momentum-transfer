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

def run_simulation(method, sim_parameters, lasers):
    if method == "electromagnetic":
        mode = 0
    elif method == "ponderomotive":
        mode = 1
    elif method == "electromagnetic-rk4":
        mode = 2
    
    program_path = f"{BIN_DIR}/laser_electron"
    filename_out = sim_parameters.filename_out
    filename_input = f"{INPUT_DIR}/input.txt"
    filename_lasers = f"{INPUT_DIR}/lasers.txt"
    
    output_mode = int(sim_parameters.output_mode == True)
    
    with open(filename_input, "w") as file:
        file.write(f"r_min {sim_parameters.r_min}\n")
        file.write(f"r_max {sim_parameters.r_max}\n")
        file.write(f"num {sim_parameters.num}\n")
        file.write(f"tf {sim_parameters.tf}\n")
        file.write(f"steps {sim_parameters.steps}\n")
        file.write(f"substeps {sim_parameters.substeps}\n")
        file.write(f"core_num {sim_parameters.core_num}\n")
        file.write(f"output_mode {output_mode}\n")
        file.write(f"mode {mode}\n")
        file.write(f"rotate_angle {sim_parameters.rotate_angle}\n")
        file.write(f"num_lasers {len(lasers)}\n")
   
    with open(filename_lasers, "w") as file:
        for i in range(len(lasers)):
            file.write(f"a0 {lasers[i].a0}\n")
            file.write(f"sigma {lasers[i].sigma}\n")
            file.write(f"omega {lasers[i].omega}\n")
            file.write(f"xif {lasers[i].xif}\n")
            file.write(f"zetax {lasers[i].zetax}\n")
            file.write(f"zetay {lasers[i].zetay}\n")
            file.write(f"phi {lasers[i].phi}\n")
            file.write(f"theta {lasers[i].theta}\n")
            file.write(f"psi {lasers[i].psi}\n")
            file.write(f"pond_integrate_steps {lasers[i].pond_integrate_steps}\n")
    
    arguments = [program_path, filename_input, filename_lasers, filename_out]
    
    try:
        res = subprocess.run(arguments, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        sys.exit(1)

# ----------------------------------------------------------------------- #

def check_convergence(method, sim_parameters, lasers, axis_pos, axis_p, steps_1, steps_2):
    axis_text_p = common.get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    if(method == "electromagnetic"):
        filename_final = f"{OUTPUT_DIR}/out-final-p{lowercase_text_p}-electromag.bin"
        filename_max = f"{OUTPUT_DIR}/out-max-p{lowercase_text_p}-electromag.bin"
    else:
        filename_final = f"{OUTPUT_DIR}/out-final-p{lowercase_text_p}-pond.bin"
        filename_max = f"{OUTPUT_DIR}/out-max-p{lowercase_text_p}-pond.bin"
    
    filename_final_1 = f"{OUTPUT_DIR}/out-final-1.bin"
    filename_final_2 = f"{OUTPUT_DIR}/out-final-2.bin"
        
    i = sim_parameters.i
    num = sim_parameters.num
    filename_data_1 = f"{OUTPUT_DIR}/out-data-1.bin"
    filename_data_2 = f"{OUTPUT_DIR}/out-data-2.bin"
    filename_conv = f"{OUTPUT_DIR}/difference.bin"
    filename_conv_average = f"{OUTPUT_DIR}/average-difference.bin"
    program_conv = f"{BIN_DIR}/conv_calc"
    
    sim_parameters.steps = steps_1
    sim_parameters.filename_out = filename_data_1
    run_simulation(method, sim_parameters, lasers)
    find_final_p(method, sim_parameters, axis_pos, axis_p)
    find_max_p(method, sim_parameters, axis_p)
    os.rename(filename_final, filename_final_1)
    
    sim_parameters.steps = steps_2
    sim_parameters.filename_out = filename_data_2
    run_simulation(method, sim_parameters, lasers)
    find_final_p(method, sim_parameters, axis_pos, axis_p)
    os.rename(filename_final, filename_final_2)
    find_max_p(method, sim_parameters, axis_p)
    
    arguments = [program_conv, num, i, filename_final_1, filename_final_2, filename_conv, filename_conv_average]
    arguments = [str(x) for x in arguments]
    
    try:
        res = subprocess.run(arguments, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        sys.exit(1)
    
    data_conv = np.fromfile(filename_conv_average, dtype=np.float64).reshape(1, 1)
    data_max = np.fromfile(filename_max, dtype=np.float64).reshape(1, 2)
    
    result = (data_conv[0] / data_max[0, 0] * 100)[0]
    print(f"The average error is: {result:0.3f}%.")
    
    sys.exit(0)
    
# ----------------------------------------------------------------------- #

def find_enter_exit_time(method, sim_parameters, axis_pos, axis_p):
    axis_text_pos = common.get_axis_text(axis_pos)
    lowercase_text_pos = axis_text_pos.lower()
    
    axis_text_p = common.get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    if(method == "electromagnetic"):
        filename_out = f"{OUTPUT_DIR}/out-enter-exit-time-electromag-{lowercase_text_pos}{lowercase_text_p}.bin"
    else:
        filename_out = f"{OUTPUT_DIR}/out-enter-exit-time-pond-{lowercase_text_pos}{lowercase_text_p}.bin"
    program_enter_exit = f"{BIN_DIR}/find_enter_exit_time"
    filename = sim_parameters.filename_out
    
    num = sim_parameters.num
    steps_final = sim_parameters.steps // sim_parameters.substeps

    #os.system(f"{program_enter_exit} {filename} {num} {steps_final} {axis_pos} {axis_p} {filename_out}")
    arguments = [program_enter_exit, filename, num, steps_final, axis_pos, axis_p, filename_out]
    arguments = [str(x) for x in arguments]
    
    try:
        res = subprocess.run(arguments, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        sys.exit(1)
        
# ----------------------------------------------------------------------- #

def find_max_p(method, sim_parameters, axis):
    axis_text = common.get_axis_text(axis)
    lowercase_text = axis_text.lower()
    if(method == "electromagnetic"):
        filename_out = f"{OUTPUT_DIR}/out-max-p{lowercase_text}-electromag.bin"
        filename_in = f"{OUTPUT_DIR}/out-final-p{lowercase_text}-electromag.bin"
    else:
        filename_out = f"{OUTPUT_DIR}/out-max-p{lowercase_text}-pond.bin"
        filename_in = f"{OUTPUT_DIR}/out-final-p{lowercase_text}-pond.bin"
    
    program_path = f"{BIN_DIR}/find_max_p"
    
    index = sim_parameters.i
    num = sim_parameters.num
    steps_final = sim_parameters.steps // sim_parameters.substeps
    
    #os.system(f"{program_path} {filename_in} {num} {steps_final} {index} {filename_out}")
    arguments = [program_path, filename_in, num, steps_final, filename_out]
    arguments = [str(x) for x in arguments]
    
    try:
        res = subprocess.run(arguments, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        sys.exit(1)
    
# ----------------------------------------------------------------------- #

def find_final_p(method, sim_parameters, axis_pos, axis_p):
    axis_text_p = common.get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    if(method == "electromagnetic"):
        filename_out = f"{OUTPUT_DIR}/out-final-p{lowercase_text_p}-electromag.bin"
        filename_out_all = f"{OUTPUT_DIR}/out-final-p{lowercase_text_p}-all-electromag.bin"
    else:
        filename_out = f"{OUTPUT_DIR}/out-final-p{lowercase_text_p}-pond.bin"
        filename_out_all = f"{OUTPUT_DIR}/out-final-p{lowercase_text_p}-all-pond.bin"
    filename = sim_parameters.filename_out
    program_path = f"{BIN_DIR}/find_final_p"
    
    num = sim_parameters.num
    steps_final = sim_parameters.steps // sim_parameters.substeps
    
    #os.system(f"{program_path} {filename} {num} {steps_final} {axis_pos} {axis_p} {filename_out} {filename_out_all}")
    arguments = [program_path, filename, num, steps_final, axis_pos, axis_p, filename_out, filename_out_all]
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
    
    i = sim_parameters.i
    num = sim_parameters.num
    
    #os.system(f"{program_path} {num} {i} {filename_in_a} {filename_in_b} {filename_out} {filename_out_average_error} {filename_out_error_all}")
    arguments = [program_path, num, i, filename_in_a, filename_in_b, filename_out, filename_out_average_error, filename_out_error_all]
    arguments = [str(x) for x in arguments]
    
    try:
        res = subprocess.run(arguments, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Critical error: {e.returncode}")
        sys.exit(1)

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