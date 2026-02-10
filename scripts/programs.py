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
        file.write(f"num {sim_parameters.num}\n")
        file.write(f"tauf {sim_parameters.tauf}\n")
        file.write(f"steps {sim_parameters.steps}\n")
        file.write(f"substeps {sim_parameters.substeps}\n")
        file.write(f"core_num {sim_parameters.core_num}\n")
        file.write(f"wave_count {sim_parameters.wave_count}\n")
        file.write(f"output_mode {output_mode}\n")
        file.write(f"mode {mode}\n")
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
    
    os.system(f"{program_path} {filename_input} {filename_lasers} {filename_out}")

# ----------------------------------------------------------------------- #

def find_enter_exit_time(method, sim_parameters):
    if(method == "electromagnetic"):
        filename_out = f"{OUTPUT_DIR}/out-enter-exit-time-electromag.bin"
    else:
        filename_out = f"{OUTPUT_DIR}/out-enter-exit-time-pond.bin"
    program_enter_exit = BIN_DIR/"find_enter_exit_time"
    filename = f"{OUTPUT_DIR}/out-data.bin"
    
    num = sim_parameters.num
    steps_final = sim_parameters.steps // sim_parameters.substeps

    os.system(f"{program_enter_exit} {filename} {num} {steps_final} {filename_out}")

# ----------------------------------------------------------------------- #

def find_max_py(method, sim_parameters):
    if(method == "electromagnetic"):
        filename_out = f"{OUTPUT_DIR}/out-max-py-electromag.bin"
        filename_in = f"{OUTPUT_DIR}/out-final-py-electromag.bin"
    else:
        filename_out = f"{OUTPUT_DIR}/out-max-py-pond.bin"
        filename_in = f"{OUTPUT_DIR}/out-final-py-pond.bin"
    
    program_path = f"{BIN_DIR}/find_max_py"
    
    index = sim_parameters.i
    num = sim_parameters.num
    steps_final = sim_parameters.steps // sim_parameters.substeps
    
    os.system(f"{program_path} {filename_in} {num} {steps_final} {index} {filename_out}")

# ----------------------------------------------------------------------- #

def find_final_py(method, sim_parameters):
    if(method == "electromagnetic"):
        filename_out = f"{OUTPUT_DIR}/out-final-py-electromag.bin"
        filename_out_all = f"{OUTPUT_DIR}/out-final-py-all-electromag.bin"
    else:
        filename_out = f"{OUTPUT_DIR}/out-final-py-pond.bin"
        filename_out_all = f"{OUTPUT_DIR}/out-final-py-all-pond.bin"
    filename = f"{OUTPUT_DIR}/out-data.bin"
    program_path = f"{BIN_DIR}/find_final_py"
    
    num = sim_parameters.num
    steps_final = sim_parameters.steps // sim_parameters.substeps
    
    os.system(f"{program_path} {filename} {num} {steps_final} {filename_out} {filename_out_all}")

# ----------------------------------------------------------------------- #

def calculate_errors(sim_parameters, a0_array):
    filename = f"{OUTPUT_DIR}/out-data.bin"
    program_path = f"{BIN_DIR}/error_calculator"
    filename_in_a = f"{OUTPUT_DIR}/out-final-py-electromag.bin"
    filename_in_b = f"{OUTPUT_DIR}/out-final-py-pond.bin"
    filename_out = f"{OUTPUT_DIR}/out-error.bin"
    filename_out_average_error = f"{OUTPUT_DIR}/out-average-error.bin"
    filename_out_error_all = f"{OUTPUT_DIR}/out-error-all.bin"
    
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