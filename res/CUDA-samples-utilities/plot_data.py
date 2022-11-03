"""
Plot the roofline ridges (peak throughput, and peak L1/L2/HBM BW).

TODO: better organization of the plots
"""

import numpy as np

import matplotlib.pyplot as plt
plt.style.use('ggplot')

T4_MEM_ROOFS = {'HBM': 245.2, 'L2': 12866.6, 'L1': 4051.9}  # measured memory BW in GB/s
T4_CMP_ROOFS = {'FP32': 8100}  # measured F32 performance in GFLOP/s

RTX_MEM_ROOFS = {'HBM': 558.7, 'L2': 22774.0, 'L1': 8124.2}  # measured memory BW in GB/s
RTX_CMP_ROOFS = {'FP32': 16200}  # measured F32 performance in GFLOP/s

A100_MEM_ROOFS = {'HBM': 1607.3, 'L2': 14970.5, 'L1': 18843.7}  # measured memory BW in GB/s
A100_CMP_ROOFS = {'FP32': 19370}  # measured F32 performance in GFLOP/s

NX = 200
X_MIN = -0.8
X_MAX = 2.2
Y_MIN = 10
Y_MAX = 100000


def plot_ridge_data(ax, flag, col_str):
    if flag == "T4":
        perf, l1, l2, hbm = T4_CMP_ROOFS['FP32'], T4_MEM_ROOFS['L1'], T4_MEM_ROOFS['L2'], T4_MEM_ROOFS['HBM']
    elif flag == "A100":
        perf, l1, l2, hbm = A100_CMP_ROOFS['FP32'], A100_MEM_ROOFS['L1'], A100_MEM_ROOFS['L2'], A100_MEM_ROOFS['HBM']
    elif flag == "TitanRTX":
        perf, l1, l2, hbm = RTX_CMP_ROOFS['FP32'], RTX_MEM_ROOFS['L1'], RTX_MEM_ROOFS['L2'], RTX_MEM_ROOFS['HBM']
    else:
        print("Wrong input!")
        return

    y_L1, y_L2, y_HBM = [], [], []
    x = np.logspace(X_MIN, X_MAX, NX)

    def helper(target, val_cap, val_bw, val_x):
        target.append(val_cap) if val_x * val_bw >= val_cap else target.append(val_x * val_bw)

    for i in range(NX):
        helper(y_L1, perf, l1, x[i])
        helper(y_L2, perf, l2, x[i])
        helper(y_HBM, perf, hbm, x[i])

    ax.plot(x, y_L1, c=col_str, ls='-.', label=flag + ': L1 limit')
    ax.plot(x, y_L2, c=col_str, ls=':', label=flag + ': L2 limit')
    ax.plot(x, y_HBM, c=col_str, ls='-', label=flag + ': HBM limit')


def plot_roofline_ridge():

    fig = plt.figure(1)
    plt.clf()
    ax = fig.gca()
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Arithmetic Intensity [FLOPs/Byte]')
    ax.set_ylabel('Performance [GFLOPs/sec]')

    ax.set_xlim(10 ** X_MIN, 10 ** X_MAX)
    ax.set_ylim(Y_MIN, Y_MAX)

    # plot the ridges
    plot_ridge_data(ax, "T4", 'g')
    plot_ridge_data(ax, "TitanRTX", 'b')
    plot_ridge_data(ax, "A100", 'r')
    plt.legend()

    plt.title('Hierarchical roofline plots of the ifarm GPUs')
    plt.savefig('./docs/roofline.png')


plot_roofline_ridge()
