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
    
    print(f"Performance test executed successfully.")
    exit()