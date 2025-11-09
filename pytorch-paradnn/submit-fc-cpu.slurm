#!/bin/bash

#SBATCH -N 1  # number of nodes
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=4000  # MB
#SBATCH --partition=gpu
#SBATCH --mail-type=END,FAIL
#SBATCH --output=paradnn_%j_%N.out
#SBATCH --job-name=fc-cpu
#SBATCH -t 24:00:00   # extend wall time

## usage: sbatch -w ${nodename} submit-fc-xxx.slurm

set -euxo pipefail

source /etc/profile.d/modules.sh
module use /apps/modulefiles
module load python3

pip3 install pandas numpy sklearn torch matplotlib

platform_long=`lscpu | grep "Model name"`

hostname_str=`hostname -s`
platform=${hostname_str}-cpu

# a test
srun python3 fc.py

data_type='f32'  # options: 'f32', 'f64', 'f16', 'bf16'
outpath=./output/fc_${platform}_${SLURM_JOBID}
mkdir -p $outpath

# bash iteration on: use_gpu, input_type, layers, nodes
#for layers in 4 8 16 32 64 128
for layers in 4
do
#  for nodes in 32 64 128 256 512 1024 2048 4096 8192
  for nodes in 1024
  do
    name=benchmark_l_${layers}_n_${nodes}_${data_type}
    srun python3 fc.py -b --layers=${layers} --nodes=${nodes} --input_type=${data_type} >> ${outpath}/${name}.csv
  done
done
