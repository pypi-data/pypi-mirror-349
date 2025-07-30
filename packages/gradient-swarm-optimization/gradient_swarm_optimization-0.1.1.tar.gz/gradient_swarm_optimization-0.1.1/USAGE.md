# GSO Usage Guide

## Basic Usage

The simplest way to use GSO is with a basic fitness function:

```python
from gso import GSO
import numpy as np

def fitness(solution):
    return np.sum(solution)

GSO.run(
    obj_func=fitness,
    dim=20,
    pop_size=50,
    max_iter=100,
    obj_type='max'
)
```

## Solving DUF Benchmark Functions

DUF (Decomposable Unitation-based Functions) are standard benchmark functions for binary optimization. The package includes a standalone script for solving these problems.

```bash
# Available DUF functions: duf1, duf2, duf3, duf4
# Basic usage
python solve_dufs.py duf1

# Custom parameters
python solve_dufs.py duf2 --dim 200 --pop-size 2000
python solve_dufs.py duf3 --seed 42 --max-iter 1000
python solve_dufs.py duf4 --neighbour-count 5 --gradient-strength 0.7
```

Available parameters for DUF problems:
- `--dim`: Problem dimension (default: 100)
- `--pop-size`: Population size (default: 1000)
- `--max-iter`: Maximum iterations (default: 800)
- `--neighbour-count`: Number of neighbors (default: 3)
- `--gradient-strength`: Gradient field strength (default: 0.8)
- `--learning-rate`: Learning rate (default: 0.1)
- `--seed`: Random seed
- `--save-results`: Save results to file (yes/no, default: yes)

## Solving UFLP Problems

The package includes a standalone script for solving Uncapacitated Facility Location Problems (UFLP).

```bash
# Basic usage
python solve_uflp.py cap71.txt

# Custom parameters
python solve_uflp.py cap71.txt --pop-size 2000 --max-iter 1000
python solve_uflp.py cap72.txt --seed 42 --gradient-strength 0.7
python solve_uflp.py cap73.txt --neighbour-count 5 --learning-rate 0.2
```

Available parameters for UFLP:
- `--pop-size`: Population size (default: 1000)
- `--max-iter`: Maximum iterations (default: 800)
- `--neighbour-count`: Number of neighbors (default: 3)
- `--gradient-strength`: Gradient field strength (default: 0.8)
- `--learning-rate`: Learning rate (default: 0.1)
- `--tolerance`: Convergence tolerance (default: 1e-6)
- `--seed`: Random seed
- `--save-results`: Save results to file (yes/no, default: yes)

## Command Line Arguments

All GSO scripts support common command line arguments:

```bash
# Save results
python your_script.py --save-results yes

# Set random seed
python your_script.py --seed 42
```

## Results

When saving is enabled (default), results are stored in JSON format in the `results/` directory:

- DUF results: `results/dufX_dY/`
- UFLP results: `results/uflp/instance_name/`

Each result file contains:
- Best solution found
- Best fitness value
- Full optimization history
- All parameters used
- Execution time
- Progress tracking