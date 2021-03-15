#!/bin/bash
 
#SBATCH -N 1  # number of nodes
#SBATCH --exclusive  # number of "tasks" (cores)
#SBATCH --mem=0        # GigaBytes of memory required (per node) Setting to 0 requests all memory on node.
#SBATCH -t 0-04:00:00   # time in d-hh:mm:ss
#SBATCH -p htc1       # partition 
#SBATCH -q normal       # QOS
#SBATCH -o slurm.%j.out # file to save job's STDOUT (%j = JobId)
#SBATCH -e slurm.%j.err # file to save job's STDERR (%j = JobId)
#SBATCH --mail-type=ALL # Send an e-mail when a job starts, stops, or fails
#SBATCH --mail-user=rmanzorr@asu.edu # Mail-to address

# Always purge modules to ensure consistent environments
module purge    

# Load required modules for job's environment
module load anaconda/py3 drprobe/1.0

# Peform Multi-slice calculations
parallel -kj $SLURM_CPUS_ON_NODE python /home/rmanzorr/MSpar_Sim/code/MS_Sims_single_1024x1024.py ::: /home/rmanzorr/MSpar_Sim/input/models/3nm/04x/Pt*.cel