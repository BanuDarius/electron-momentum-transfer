#!/bin/bash
#SBATCH --job-name=electron-momentum-transfer
#SBATCH --output=log-%j.txt
#SBATCH --error=errors-%j.txt
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=128
#SBATCH --mem=16G
#SBATCH --hint=nomultithread
#SBATCH --time=2:00:00

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_PLACES=cores
export OMP_PROC_BIND=true

source $HOME/python-env/bin/activate

srun python3 auto_compute.py

deactivate

#An example SLURM script for running the program on a single compute cluster node