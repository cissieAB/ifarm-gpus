#!/bin/bash

#SBATCH --gres gpu:T4:1   # update GPU name when needed
#SBATCH -N 1  # number of nodes
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=4000  # MB
#SBATCH --partition=gpu
#SBATCH --mail-type=END,FAIL
#SBATCH --output=paradnn_%j-%N.out
#SBATCH --job-name=fc-gpu
#SBATCH -t 24:00:00   # extend wall time

set -euxo pipefail

source /etc/profile.d/modules.sh
module use /apps/modulefiles
module load python3

pip3 install pandas numpy sklearn torch matplotlib

hostname_str=`hostname -s`
platform=${hostname_str}-gpu

data_type='f32'
outpath=./output/fc_${SLURM_JOBID}
mkdir -p $outpath

use_gpu=1

# todo: develop features on AMP
# bash iteration on: use_gpu, input_type, layers, nodes, use_amp
srun python3 fc.py --use_gpu=${use_gpu} --input_type=${data_type}

# for layers in 4 8 16 32 64 128
for layers in 4
do
for nodes in 32 64 128 256  512 1024 2048 4096 8192
  do
    name=benchmark_l_${layers}_n_${nodes}_${data_type}_${platform}
    srun python3 fc.py -b --layers=${layers} --nodes=${nodes} --use_gpu=${use_gpu} --input_type=${data_type}\
    >> ${outpath}/${name}.csv
  done
done
