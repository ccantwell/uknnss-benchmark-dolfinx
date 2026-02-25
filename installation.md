## Complete manual installation instructions

The `benchmark-dolfinx` code depends on `dolfinx`, `basix` and `ffcx` which are part of the FEniCS software suite.

### Installing `ffcx` and `basix`

`basix` is a C++/Python package, and can be installed using `pip`, e.g. `pip install git+https://git@github.com/FEniCS/basix@v0.10.0`

`ffcx` is a Python package, and can be installed using `pip`, e.g. `pip install git+https://git@github.com/FEniCS/ffcx@v0.10.0`

### Installing `dolfinx`

`dolfinx` is a C++ package with a number of dependencies. The following are needed for `benchmark-dolfinx`:

- boost
- spdlog
- pkgconfig
- pugixml
- BLAS
- HDF5 (including parallel MPI support)
- MPI
- ParMETIS or PT-SCOTCH

PETSc is not required for the benchmark. A modern compiler, capabale
of C++20 features (including `std::format`) is required. **The minimum
gcc version supported is gcc-13**.

In the source code, create a build directory, e.g.

```
git clone https://git@github.com/FEniCS/dolfinx
cd dolfinx
git checkout v0.10.0.post4
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=install_dir ../cpp
make -j 4
make install
```

### Building the benchmark

The benchmark is built on top of `dolfinx`, e.g.

```
cd
git clone https://git@github.com/ukri-bench/benchmark-dolfinx
cd benchmark-dolfinx
mkdir build && cd build
cmake -DCUDA_ARCH=89 ../src
make -j 4
```

## Example installation on Ubuntu 24.04

The following set of commands has been tested on a clean Ubuntu 24.04
container. This will build a CPU version of the benchmark. In order to
build the required GPU version, *appropriate CUDA or ROCm packages must
be installed becore building* `benchmark-dolfinx` with `CUDA_ARCH` or
`HIP_ARCH` flags - see [main instructions](https://github.com/ukri-bench/benchmark-dolfinx/blob/main/README.md).

```
# Install required Ubuntu packages
apt-get update
apt-get install -y git cmake g++ libopenmpi-dev libpugixml-dev \
libspdlog-dev libboost-dev libboost-program-options-dev libboost-json-dev \
libhdf5-mpi-dev python3-pip libopenblas-dev pkg-config libparmetis-dev

# Install (system-wide) FEniCS Python components
pip install --break-system-packages git+https://git@github.com/fenics/basix@v0.10.0
pip install --break-system-packages git+https://git@github.com/fenics/ffcx@v0.10.0

# Checkout dolfinx and build
git clone https://git@github.com/FEniCS/dolfinx
cd dolfinx
git checkout v0.10.0.post4
mkdir build && cd build
cmake ../cpp
make -j 4 && make install

# Checkout benchmark and build
cd
export Basix_DIR=/usr/local/lib/python3.12/dist-packages/basix
git clone https://git@github.com/ukri-bench/benchmark-dolfinx
cd benchmark-dolfinx
mkdir build && cd build
cmake ../src
make -j 4

```

### Potential issues and workarounds

- The dependency `basix` requires BLAS libraries. On Cray systems using `cray-libsci` these need to be specified to `cmake`.
This is encoded in the spack recipe at [https://github.com/FEniCS/spack-fenics/blob/e8b5e9fdd299889b4cb6209559de04b9289c20ab/spack_repo/fenics/packages/fenics_basix/package.py].

- The version of `mdspan.hpp` distributed in `basix` v0.10.0 is not compatible with CUDA 13. A patch is available at [https://github.com/FEniCS/spack-fenics/blob/07b9fd0dfd3d878c383ed8cba9e2a10fa52b478a/spack_repo/fenics/packages/fenics_basix/mdspan.patch], which should be applied if using CUDA 13.0 or higher.

- A C++20 compiler capable of handling `std::format` is required. On some systems, it is necessary to explicitly pass this to `nvcc` or `hipcc` through a command line argument, e.g. `--gcc-toolchain=/opt/rh/gcc-toolset-13/root/usr`.
