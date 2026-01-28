# UK NSS DOLFINx Benchmark

The DOLFINx Benchmark is a performance benchmark for testing
matrix-free operator evaluation on unstructured hexahedral grids. It
is available at [https://github.com/ukri-bench/benchmark-dolfinx] with
an MIT license.

## Status

Stable

## Maintainers

- Chris Richardson
- Garth Wells

## Overview

### Software

[https://github.com/ukri-bench/benchmark-dolfinx](https://github.com/ukri-bench/benchmark-dolfinx)

### Architectures

- CPU: x86, Arm
- GPU: NVIDIA, AMD

### Languages and programming models

- Programming languages: C++
- Parallel models: MPI
- Accelerator offload models: CUDA, HIP

## Building the benchmark

### Permitted modifications

- `benchmark-dolfinx` has been written with standard C++20 and tested with ROCm 6.3.4 and CUDA
12.9. Modifications for later versions of ROCm and CUDA are permitted,
if required to resolve unavoidable compilation or runtime errors.

### Requirements

- The host-code compiler must support C++20 including
`std::format`. This limits the choice of host-code compilers to
reasonably recent versions (gcc-13 or later).
- For NVIDIA GPUs, CUDA version 12.x is recommended.
- For AMD GPUs, ROCm version 6.x is recommended.

### Manual build

Detailed build instructions can be found in the (benchmark source
code)[https://github.com/ukri-bench/benchmark-dolfinx].

## Running the benchmark

The benchmark is designed to run on GPU, but does not do automatic
allocation of devices. For example, if there are multiple GPUs on the
same host, they must be presented individually with a "gpu_select"
script, when running in parallel with MPI. For example:
```
#!/bin/bash
export CUDA_VISIBLE_DEVICES=$OMPI_COMM_WORLD_LOCAL_RANK
exec $*
```
and then `mpirun -n 64 ./gpu_select bench_dolfinx ...`

### Command-line arguments

Command line arguments can be shown with the `-h` option.
For benchmarking purposes, use the following options:

- Correctness comparison with matrix result: `bench_dolfinx
  --ndofs=10000 --mat_comp --ndofs_global=100000 --degree=3 --json
  mat_comp.json`
- Throughput at Q3, 10M degrees-of-freedom: `bench_dolfinx --degree=3
  --ndofs=10000000 --json Q3-10M.json`
- Throughput at Q6, 10M degrees-of-freedom: `bench_dolfinx --degree=6
  --ndofs=10000000 --json Q6-10M.json`
- Throughput at Q3, 60M degrees-of-freedom: `bench_dolfinx --degree=3
  --ndofs=60000000 --json Q3-60M.json`
- Throughput at Q6, 60M degrees-of-freedom: `bench_dolfinx --degree=6
  --ndofs=60000000 --json Q6-60M.json`

The matrix comparison should be run on 1 GPU and 4 GPUs with the same
output (within numerical roundoff precision). *PASS/FAIL*
The throughput tests can in principle be run on any number of GPU/GCD
devices. The *Figure of Merit* is the data throughput measured in
GDoFs/s, which is reported at the end of each run, and also saved to
the JSON files.
Some baseline data is shown below.

* LUMI-G (MI-250X)

### Throughput in GDoFs/s

|Operation|1|2|4|8|16|
|mat comp|5.7797|8.10161|12.5999|19.2768|29.68|
|Q3 1M|17.328|33.2159|58.6681|114.966|225.56|
|Q6 1M|21.1168|38.4989|51.486|73.6816|195.58|
|Q3 10M|18.9448|36.0356|67.4767|137.571|262.282|
|Q6 10M|26.5277|50.4899|94.0343|142.381|371.053|
|Q3 60M|19.6491|38.9419|73.6595|147.589|299.465|
|Q6 60M|28.0689|55.0029|103.26|197.221|415.822|
