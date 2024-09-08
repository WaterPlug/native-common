# Native common stuff

#### Prerequisites

* Conan C++ package manager 2.7.0 or higher
* CMake 3.28 or higher
* GCC 13 or higher / Clang 15 or higher

## Build

### Linux

```shell
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -GNinja \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_CXX_FLAGS="-stdlib=libc++"  \
    ..
```

### Windows

```shell
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo ^
    -DCMAKE_C_FLAGS_DEBUG=/MT ^
    -DCMAKE_CXX_FLAGS_DEBUG=/MT ^
    -G Ninja ^
    ..
```

### macOS

```shell
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -GNinja \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_CXX_FLAGS="-stdlib=libc++" \
    ..
```
