#!/bin/bash -l
# ===========================================
# Slurm Header
# ===========================================
# SBATCH -J relax
#SBATCH --partition=CLUSTER
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.error
# SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --get-user-env
#SBATCH --time=999:00:00
#SBATCH --exclude=compute-0-[8,9,10]
# SBATCH --nodelist=compute-0-7
# SBATCH --mem-per-cpu=150
#SBATCH --mem=6G
# ===========================================
. startjob      # Do not remove this line!
# ===========================================
# Your Commands Go Here 
# ===========================================


module load ips/2019

rm -f CHARGES
/home/jorge/Fireball/progs_charges/progs/fireball.x > salida.out


# ===========================================
# End Commands
# ===========================================
. endjob        # Do not remove this line!
#--------------------------------------------
