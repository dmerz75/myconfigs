#include <stdio.h>

// http://www.geforce.com/hardware/notebook-gpus/geforce-gtx-870m/specifications
// GPU Engine Specs:
// CUDA Cores                      1344
// Graphics Clock (MHz)            941 + Boost
// Memory Specs:
// Memory Clock (MHZ)              Up to 2500 MHz
// Standard Memory Configuration   GDDR5
// Memory Interface Width          192-bit
// Memory Bandwidth (GB/sec)       120.0

int main() {

    // Number of CUDA devices
    int nDevices;

    cudaGetDeviceCount(&nDevices);

    printf("CUDA Device Query...\n");
    printf("There are %d CUDA devices.\n", nDevices);


    for (int i = 0; i < nDevices; i++) {
        cudaDeviceProp prop;
        cudaGetDeviceProperties(&prop, i);
        printf("\n\n");
        printf("Device Number: %d\n", i);
        printf("  Device name: %s\n", prop.name);
        printf("  Memory Clock Rate (KHz): %d\n", prop.memoryClockRate);
        printf("  Memory Clock Rate (MHz): %d\n", prop.memoryClockRate / 1000);
        printf("  Memory Bus Width (bits): %d\n", prop.memoryBusWidth);
        printf("  Peak Memory Bandwidth (GB/s): %f", 2.0*prop.memoryClockRate*(prop.memoryBusWidth/8)/1.0e6);
        printf("\n\n");


        // CUDA Device Query
        /* From Nitin Gupta */
        /* http://cuda-programming.blogspot.com/2013/01/how-to-query-to-devices-in-cuda-cc.html */
        // modified
        printf("Major revision number:         %d\n",  prop.major);
        printf("Minor revision number:         %d\n",  prop.minor);
        printf("Name:                          %s\n",  prop.name);
        printf("Total global memory:           %u\n",  prop.totalGlobalMem);

        printf("Total global memory (GB):      %u\n",  prop.totalGlobalMem / 1024 / 1024);

        printf("Total shared memory per block: %u\n",  prop.sharedMemPerBlock);
        printf("Total registers per block:     %d\n",  prop.regsPerBlock);
        printf("Warp size:                     %d\n",  prop.warpSize);
        printf("Maximum memory pitch:          %u\n",  prop.memPitch);
        printf("Maximum threads per block:     %d\n",  prop.maxThreadsPerBlock);
        // for (int i = 0; i < 3; ++i)
        //     printf("Maximum dimension %d of block:  %d\n", i, prop.maxThreadsDim[i]);
        // for (int i = 0; i < 3; ++i)
        //     printf("Maximum dimension %d of grid:   %d\n", i, prop.maxGridSize[i]);
        printf("Clock rate:                    %d\n",  prop.clockRate);
        printf("Total constant memory:         %u\n",  prop.totalConstMem);
        printf("Texture alignment:             %u\n",  prop.textureAlignment);
        printf("Concurrent copy and execution: %s\n",  (prop.deviceOverlap ? "Yes" : "No"));
        printf("Number of multiprocessors:     %d\n",  prop.multiProcessorCount);
        printf("Kernel execution timeout:      %s\n",  (prop.kernelExecTimeoutEnabled ? "Yes" : "No"));

    }
}
