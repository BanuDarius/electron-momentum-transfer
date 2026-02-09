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

def run_simulation(method, sim_parameters):
    if method == "electromagnetic":
        mode = 0
    else:
        mode = 1
    
    program_path = f"{BIN_DIR}/laser_electron"
    filename_out = f"{OUTPUT_DIR}/out-data.bin"
    filename_input = f"{INPUT_DIR}/input.txt"
    
    a0 = sim_parameters.a0
    num = sim_parameters.num
    xif = sim_parameters.xif
    tauf = sim_parameters.tauf
    steps = sim_parameters.steps
    sigma = sim_parameters.sigma
    substeps = sim_parameters.substeps
    core_num = sim_parameters.core_num
    wave_count = sim_parameters.wave_count
    output_mode = int(sim_parameters.output_mode == True)
    
    with open(filename_input, "w") as file:
        file.write(f"a0 {a0}\n")
        file.write(f"num {num}\n")
        file.write(f"xif {xif}\n")
        file.write(f"tauf {tauf}\n")
        file.write(f"steps {steps}\n")
        file.write(f"sigma {sigma}\n")
        file.write(f"substeps {substeps}\n")
        file.write(f"core_num {core_num}\n")
        file.write(f"wave_count {wave_count}\n")
        file.write(f"output_mode {output_mode}\n")
        file.write(f"mode {mode}\n")
    
    os.system(f"{program_path} {filename_input} {filename_out}")

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
    
    a0 = sim_parameters.a0
    num = sim_parameters.num
    steps_final = sim_parameters.steps // sim_parameters.substeps
    
    os.system(f"{program_path} {filename_in} {num} {steps_final} {a0:0.3f} {filename_out}")

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

def calculate_errors(sim_parameters):
    filename = f"{OUTPUT_DIR}/out-data.bin"
    program_path = f"{BIN_DIR}/error_calculator"
    
    a0 = sim_parameters.a0
    num = sim_parameters.num
    
    os.system(f"{program_path} {num} {a0:0.3f}")

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