# Approx
## About
This project deals with approximations of arithmetic circuits using Cartesian Genetic Programming. We aim to reduce the complexity of a circuit while preserving certain allowed error rates. For circuit simulation we use the [ArithsGen](https://github.com/ehw-fit/ariths-gen) package. Optimizer accept specifically 8-bit multipliers.

## Setup
Pull ArithsGen
```
git submodule init
git submodule update
```

Launch solver for `mul8.cgp` output with max allowed error `2%`.
```
python3 main.py mul8.cgp --error 2
```
