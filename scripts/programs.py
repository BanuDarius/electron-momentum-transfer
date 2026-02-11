import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BIN_DIR = PROJECT_ROOT / "bin"
INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_IMAGE_DIR = PROJECT_ROOT / "output-image"

# ----------------------------------------------------------------------- #

def get_axis_text(axis):
    if(axis == 0):
        axis_text = "X"
    elif(axis == 1):
        axis_text = "Y"
    else:
        axis_text = "Z"
    return axis_text
    
def get_lowercase_text(axis):
    text = get_axis_text(axis).lower()
    return text

# ----------------------------------------------------------------------- #

def run_simulation(method, sim_parameters, lasers):
    if method == "electromagnetic":
        mode = 0
    else:
        mode = 1
    
    program_path = f"{BIN_DIR}/laser_electron"
    filename_out = f"{OUTPUT_DIR}/out-data.bin"
    filename_input = f"{INPUT_DIR}/input.txt"
    filename_lasers = f"{INPUT_DIR}/lasers.txt"
    
    output_mode = int(sim_parameters.output_mode == True)
    
    with open(filename_input, "w") as file:
        file.write(f"r {sim_parameters.r}\n")
        file.write(f"num {sim_parameters.num}\n")
        file.write(f"tauf {sim_parameters.tauf}\n")
        file.write(f"steps {sim_parameters.steps}\n")
        file.write(f"substeps {sim_parameters.substeps}\n")
        file.write(f"core_num {sim_parameters.core_num}\n")
        file.write(f"output_mode {output_mode}\n")
        file.write(f"mode {mode}\n")
        file.write(f"line_angle {sim_parameters.line_angle}\n")
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
    
    os.system(f"{program_path} {filename_input} {filename_lasers} {filename_out}")

# ----------------------------------------------------------------------- #

def find_enter_exit_time(method, sim_parameters, axis_pos, axis_p):
    axis_text_pos = get_axis_text(axis_pos)
    lowercase_text_pos = axis_text_pos.lower()
    
    axis_text_p = get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    if(method == "electromagnetic"):
        filename_out = f"{OUTPUT_DIR}/out-enter-exit-time-electromag-{lowercase_text_pos}{lowercase_text_p}.bin"
    else:
        filename_out = f"{OUTPUT_DIR}/out-enter-exit-time-pond-{lowercase_text_pos}{lowercase_text_p}.bin"
    program_enter_exit = BIN_DIR/"find_enter_exit_time"
    filename = f"{OUTPUT_DIR}/out-data.bin"
    
    num = sim_parameters.num
    steps_final = sim_parameters.steps // sim_parameters.substeps

    os.system(f"{program_enter_exit} {filename} {num} {steps_final} {axis_pos} {axis_p} {filename_out}")

# ----------------------------------------------------------------------- #

def find_max_p(method, sim_parameters, axis):
    axis_text = get_axis_text(axis)
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
    
    os.system(f"{program_path} {filename_in} {num} {steps_final} {index} {filename_out}")

# ----------------------------------------------------------------------- #

def find_final_p(method, sim_parameters, axis_pos, axis_p):
    axis_text_p = get_axis_text(axis_p)
    lowercase_text_p = axis_text_p.lower()
    
    if(method == "electromagnetic"):
        filename_out = f"{OUTPUT_DIR}/out-final-p{lowercase_text_p}-electromag.bin"
        filename_out_all = f"{OUTPUT_DIR}/out-final-p{lowercase_text_p}-all-electromag.bin"
    else:
        filename_out = f"{OUTPUT_DIR}/out-final-p{lowercase_text_p}-pond.bin"
        filename_out_all = f"{OUTPUT_DIR}/out-final-p{lowercase_text_p}-all-pond.bin"
    filename = f"{OUTPUT_DIR}/out-data.bin"
    program_path = f"{BIN_DIR}/find_final_p"
    
    num = sim_parameters.num
    steps_final = sim_parameters.steps // sim_parameters.substeps
    
    os.system(f"{program_path} {filename} {num} {steps_final} {axis_pos} {axis_p} {filename_out} {filename_out_all}")

# ----------------------------------------------------------------------- #

def calculate_errors(sim_parameters, a0_array, axis):
    axis_text = get_axis_text(axis)
    lowercase_text = axis_text.lower()
    
    filename = f"{OUTPUT_DIR}/out-data.bin"
    program_path = f"{BIN_DIR}/error_calculator"
    filename_in_a = f"{OUTPUT_DIR}/out-final-p{lowercase_text}-electromag.bin"
    filename_in_b = f"{OUTPUT_DIR}/out-final-p{lowercase_text}-pond.bin"
    filename_out = f"{OUTPUT_DIR}/out-error-{lowercase_text}.bin"
    filename_out_average_error = f"{OUTPUT_DIR}/out-average-error-{lowercase_text}.bin"
    filename_out_error_all = f"{OUTPUT_DIR}/out-error-all-{lowercase_text}.bin"
    
    i = sim_parameters.i
    num = sim_parameters.num
    
    os.system(f"{program_path} {num} {i} {filename_in_a} {filename_in_b} {filename_out} {filename_out_average_error} {filename_out_error_all}")

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