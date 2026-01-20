import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BIN_DIR = PROJECT_ROOT / "bins"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_IMAGE_DIR = PROJECT_ROOT / "output-image"

# ----------------------------------------------------------------------- #

def run_simulation(method, output_mode, a0, xif, tauf, wave_count, num, steps, substeps):
    programPath = BIN_DIR/"laser_electron"
    if method == "electromagnetic":
        mode = 0
    else:
        mode = 1
    output_mode = int(output_mode == True)
    os.system(f"{programPath} {mode} {output_mode} {a0:0.3f} {num} {steps} {wave_count} {xif:0.3f} {tauf:0.3f} {substeps}")

# ----------------------------------------------------------------------- #

def find_enter_exit_time(num, steps):
    programEnterExit = BIN_DIR/"find_enter_exit_time"
    filename = f"{OUTPUT_DIR}/out-data.bin"

    os.system(f"{programEnterExit} {filename} {num} {steps}")

# ----------------------------------------------------------------------- #

def find_max_py(method, a0, num, steps):
    if(method == "electromagnetic"):
        filenameOut = f"{OUTPUT_DIR}/out-max-py-electromag.bin"
        filenameIn = f"{OUTPUT_DIR}/out-final-py-electromag.bin"
    else:
        filenameOut = f"{OUTPUT_DIR}/out-max-py-pond.bin"
        filenameIn = f"{OUTPUT_DIR}/out-final-py-pond.bin"
    
    programPath = f"{BIN_DIR}/find_max_py"
    
    os.system(f"{programPath} {filenameIn} {num} {steps} {a0:0.3f} {filenameOut}")

# ----------------------------------------------------------------------- #

def find_final_py(method, num, steps):
    if(method == "electromagnetic"):
        filenameOut = f"{OUTPUT_DIR}/out-final-py-electromag.bin"
        filenameOutAll = f"{OUTPUT_DIR}/out-final-py-all-electromag.bin"
    else:
        filenameOut = f"{OUTPUT_DIR}/out-final-py-pond.bin"
        filenameOutAll = f"{OUTPUT_DIR}/out-final-py-all-pond.bin"
    filename = f"{OUTPUT_DIR}/out-data.bin"
    programPath = f"{BIN_DIR}/find_final_py"
    
    os.system(f"{programPath} {filename} {num} {steps} {filenameOut} {filenameOutAll}")

# ----------------------------------------------------------------------- #

def calculate_errors(a0, num):
    filename = f"{OUTPUT_DIR}/out-data.bin"
    programPath = f"{BIN_DIR}/error_calculator"
    
    os.system(f"{programPath} {num} {a0:0.3f}")

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