# Compiler
CC = nvcc

# Compiler: lib
NVCC65 = /opt/cuda-6.5/bin/nvcc
OPTCUDA = /opt/cuda/bin/nvcc

# Compiler for library cluster.
# CC = /usr/local/cuda-5.0/bin/nvcc
# export LD_LIBRARY_PATH=/usr/local/cuda-5.0/lib64:$LD_LIBRARY_PATH    # MUST USE!

# .cu files
CFILES = cuda_device_query.cu

query:
	$(CC) $(CFILES) -o devicequery.exe

65:
	$(NVCC65) $(CFILES) -o devicequery.exe

optcuda:
	$(OPTCUDA) $(CFILES) -o devicequery-optcuda2.exe
