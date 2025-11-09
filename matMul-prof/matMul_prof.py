import torch
from torch.profiler import profile, record_function, ProfilerActivity

# Set the target device and matrix size
device = "cuda"
SIZE = 16384

print("GPU:", torch.cuda.get_device_name(0))
# Get CUDA Compute Capability (CC)
print(f"Compute Capability: \
      {torch.cuda.get_device_properties(0).major}.{torch.cuda.get_device_properties(0).minor}")

# TF32 is supported by CC 8.0 and above
has_tf32 = torch.cuda.get_device_capability(0)[0] >= 8
print("Supports TF32:", has_tf32)  # Ampere or newer
print()

torch.backends.cudnn.benchmark = True   
torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction = True
if has_tf32:
    print("Running with TF32 enabled:")
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

dtypes = [torch.float32, torch.float16, torch.bfloat16]

for dtype in dtypes:
    print(f"\n\n=== Testing dtype: {dtype} ===")

    # Create random matrices
    with torch.cuda.device(device):
        a = torch.randn((SIZE, SIZE), device=device, dtype=dtype)
        b = torch.randn((SIZE, SIZE), device=device, dtype=dtype)

    # Cold matrix multiplication to warm up
    with torch.no_grad():
        for _ in range(20):
            _ = torch.matmul(a, b)
        torch.cuda.synchronize()

    # Profiling round
    with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], 
                 record_shapes=True, 
                 with_stack=True) as prof:
        with record_function(f"matrix_multiplication_{dtype}"):
            _ = torch.matmul(a, b)
        torch.cuda.synchronize()

    # Print profiling results
    print(prof.key_averages().table(sort_by="cuda_time_total"))
    
    print("\n")

