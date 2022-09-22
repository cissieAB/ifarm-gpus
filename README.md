# The Performance of the JLab ifarm GPUs

A quick view of the ifarm GPUs.


|  | Tesla T4	| Titan RTX	|A100_PCIe |
| -- | ----------- | ----------- |-----|
| Compute capacity | 7.5 | 7.5 | 8.0|
| Boost GPU core clock (MHz)	| 1590	| 1770	| 1410 |
|# SM	| 40	| 72	| 108 |
| Theoretical F32 fma performance (TFlops)	| 8.14| 16.31	| 19.49 |
| Memory size (MB)	| 15110	| 24220 |	81251 |
| Memory clock (MHz)	| 5001	| 7001| 1512 |
| Memory bus width (bits) | 256	| 384	| 5120 |
|Theoretical peak memory BW (GB/s)	|320.06	|672.10|1935.36|
|Measured peak memory BW (GB/s)	|241.6	|558.7|	1607.3 |	
|L2 cache size (Mebibyte)	|4	|6	|40|
|Measured L2 bandwidth (GB/s)	|5760.9	|5857.2	|14659.7|		
| L1 cache size (Kilibyte) per SM	|64	|64	|164|
| Measured L1 bandwidth (GB/s)	| 4051.9	|8124.2 |	18799.4 |


## Other docs
* Benchmarking esults from the CUDA samples: https://github.com/cissieAB/ifarm-gpus/tree/master/res


- [ ] Guide to get the harware limit of the GPUs
- [ ] Roofline plot of the ifarm GPUs
