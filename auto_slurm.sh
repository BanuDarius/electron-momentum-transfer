#!/bin/bash
#SBATCH --job-name=auto_compute
#SBATCH --output=compute_%j.log
#SBATCH --error=compute_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=256
#SBATCH --mem=2G
#SBATCH --time=2:00:00

source $HOME/python3-env/bin/activate

srun python3 auto_compute.py

deactivate