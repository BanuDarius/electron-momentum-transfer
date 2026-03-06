#!/bin/bash
#SBATCH --job-name=electron-momentum-transfer
#SBATCH --output=output-%j.txt
#SBATCH --error=errors-%j.txt
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=256
#SBATCH --mem=4G
#SBATCH --time=2:00:00

source $HOME/python-env/bin/activate

srun python3 auto_compute.py

deactivate

#An example SLURM script for running the program on a single compute cluster node