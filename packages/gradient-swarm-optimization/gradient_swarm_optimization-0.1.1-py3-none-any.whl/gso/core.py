import numpy as np
import time
from typing import Callable, Optional, Tuple, Dict, Any, Union
from pathlib import Path
from .exceptions import OptimizationError, ConvergenceError, TimeoutError
from .validators import validate_parameters

class GSO:
    """Gradient-guided Swarm Optimization algorithm implementation."""
    
    def __init__(
        self,
        pop_size: int,
        max_iter: int,
        obj_type: str,
        neighbour_count: int,
        obj_func: Callable[[np.ndarray], float],
        dim: Optional[int] = None,
        load_problem_file: Optional[Callable] = None,
        gradient_strength: float = 0.8,
        base_learning_rate: float = 0.1,
        known_optimum: Optional[float] = None,
        tolerance: Optional[float] = None,
        timeout: Optional[int] = None,
        seed: Optional[int] = None,
        save_results: bool = False,
        results_dir: Union[str, Path] = "results"
    ):
        """Initialize the GSO optimizer.
        
        Args:
            pop_size: Population size
            max_iter: Maximum number of iterations
            obj_type: Optimization type ('min' or 'max')
            neighbour_count: Number of neighbors to consider
            obj_func: Objective function to optimize
            dim: Problem dimension
            load_problem_file: Function to load problem data
            gradient_strength: Gradient field effect strength
            base_learning_rate: Base learning rate for neighbor influence
            known_optimum: Known optimal solution value
            tolerance: Convergence tolerance
            timeout: Maximum runtime in seconds
            seed: Random seed for reproducibility
        """
        # Store parameters
        self.pop_size = pop_size
        self.max_iter = max_iter
        self.obj_type = obj_type.lower()
        self.neighbour_count = neighbour_count
        self.obj_func = obj_func
        self.gradient_strength = gradient_strength
        self.base_learning_rate = base_learning_rate
        self.known_optimum = known_optimum
        self.tolerance = tolerance
        self.timeout = timeout
        self.save_results = save_results
        self.results_dir = Path(results_dir)
        if self.save_results:
            self.results_dir.mkdir(parents=True, exist_ok=True)
        # Validate parameters
        validate_parameters(self)
        
        # Set random seed
        if seed is not None:
            np.random.seed(seed)
            
        # Load problem if file loader provided
        self.problem_data = None
        if load_problem_file:
            result = load_problem_file()
            if isinstance(result, tuple):
                self.problem_data, file_optimum = result
                if self.known_optimum is None:
                    self.known_optimum = file_optimum
            else:
                self.problem_data = result
                
        # Set dimension from problem data or parameter
        if dim is None:
            if self.problem_data is not None and hasattr(self.problem_data, 'dim'):
                self.dim = self.problem_data.dim
            else:
                raise ValueError("Problem dimension must be provided when no problem file is loaded")
        else:
            self.dim = dim
            
        # Initialize population and tracking variables
        self.population = self._initialize_population()
        self.fitness_values = np.zeros(pop_size)
        self.best_solution = None
        self.best_fitness = float('inf')
        self.gradient_vector = np.zeros(dim)
        self.history = []
        
    @classmethod
    def run(cls, obj_func: Callable, dim: int, **kwargs):
        """Run optimization with CLI arguments.
        
        Args:
            obj_func: Objective function to optimize
            dim: Problem dimension
            **kwargs: Additional arguments to pass to GSO constructor
        """
        optimizer = cls(
            obj_func=obj_func,
            dim=dim,
            **kwargs
        )
        
        # Run optimization
        return optimizer.optimize()
        
    def _initialize_population(self) -> np.ndarray:
        """Initialize binary population with smart initialization strategy."""
        population = np.zeros((self.pop_size, self.dim), dtype=int)
        
        # Random initialization
        num_random = self.pop_size // 3
        population[:num_random] = np.random.randint(2, size=(num_random, self.dim))
        
        # Half-filled solutions
        num_half = self.pop_size // 3
        half_filled = np.zeros((num_half, self.dim), dtype=int)
        for i in range(num_half):
            positions = np.random.choice(self.dim, size=self.dim//2, replace=False)
            half_filled[i, positions] = 1
        population[num_random:num_random+num_half] = half_filled
        
        # Dense solutions
        remaining = self.pop_size - (num_random + num_half)
        dense_filled = np.ones((remaining, self.dim), dtype=int)
        for i in range(remaining):
            positions = np.random.choice(self.dim, size=self.dim//4, replace=False)
            dense_filled[i, positions] = 0
        population[num_random+num_half:] = dense_filled
        
        return population
        
    def _is_better(self, fitness1: float, fitness2: float) -> bool:
        """Compare two fitness values based on optimization type."""
        if self.obj_type == 'min':
            return fitness1 < fitness2
        return fitness1 > fitness2
        
    def _calculate_fitness(self, solution: np.ndarray) -> float:
        """Calculate fitness using user-provided function."""
        if self.problem_data is not None:
            return self.obj_func(solution, self.problem_data)
        return self.obj_func(solution)
        
    def _update_gradient_vector(self):
        """Update gradient field based on best solution."""
        if self.best_solution is not None:
            self.gradient_vector = (self.best_solution - np.mean(self.population, axis=0))
            norm = np.linalg.norm(self.gradient_vector)
            if norm > 0:
                self.gradient_vector = self.gradient_vector / norm
                
    def _update_position(self, current_pos: np.ndarray, gradient_influence: np.ndarray,
                        iteration: int, solution_idx: int) -> np.ndarray:
        """Update position of a solution."""
        new_pos = current_pos.copy()
        
        # Global best influence
        if self.best_solution is not None:
            gradient_diff = gradient_influence * (self.best_solution - current_pos)
            gradient_change_prob = np.abs(gradient_diff)
            gradient_mask = np.random.random(self.dim) < gradient_change_prob
            new_pos[gradient_mask] = self.best_solution[gradient_mask]
        
        # Neighbor influence
        k = min(self.neighbour_count, self.pop_size-1)
        distances = []
        
        for i in range(self.pop_size):
            if i != solution_idx:
                dist = np.sum(np.abs(current_pos - self.population[i]))
                distances.append((dist, i, self.fitness_values[i]))
        
        distances.sort()
        for _, neighbor_idx, neighbor_fitness in distances[:k]:
            if self._is_better(neighbor_fitness, self.fitness_values[solution_idx]):
                neighbor = self.population[neighbor_idx]
                learn_mask = np.random.random(self.dim) < self.base_learning_rate
                new_pos[learn_mask] = neighbor[learn_mask]
        
        return new_pos
        
    def _update_solution(self, solution_idx: int, iteration: int):
        """Update a single solution in the population."""
        solution = self.population[solution_idx].copy()
        gradient_influence = self.gradient_strength * self.gradient_vector
        
        new_position = self._update_position(
            solution,
            gradient_influence,
            iteration,
            solution_idx
        )
        
        # Calculate fitness        
        new_fitness = self._calculate_fitness(new_position)
        
        # Update if better
        if self._is_better(new_fitness, self.fitness_values[solution_idx]):
            self.population[solution_idx] = new_position
            self.fitness_values[solution_idx] = new_fitness
            
            if self._is_better(new_fitness, self.best_fitness):
                self.best_fitness = new_fitness
                self.best_solution = new_position.copy()
                
    def optimize(self, callback: Optional[Callable] = None) -> Tuple[np.ndarray, float]:
        """Run the optimization process.
        
        Args:
            callback: Optional callback function called after each iteration
            
        Returns:
            Tuple of (best_solution, best_fitness)
        """
        from .utils import default_callback, print_results
        
        start_time = time.time()
        
        # Use default callback if none provided
        if callback is None:
            callback = default_callback
        
        # Calculate initial fitness values
        for i in range(self.pop_size):
            self.fitness_values[i] = self._calculate_fitness(self.population[i])
            
        # Initialize best solution
        best_idx = np.argmin(self.fitness_values) if self.obj_type == 'min' else np.argmax(self.fitness_values)
        self.best_solution = self.population[best_idx].copy()
        self.best_fitness = self.fitness_values[best_idx]
        
        # Main optimization loop
        try:
            for iteration in range(self.max_iter):
                # Check timeout
                if self.timeout and time.time() - start_time > self.timeout:
                    raise TimeoutError(f"Optimization exceeded timeout of {self.timeout} seconds")
                    
                # Update gradient field and solutions
                self._update_gradient_vector()
                for solution_idx in range(self.pop_size):
                    self._update_solution(solution_idx, iteration)
                    
                # Record history
                current_time = time.time() - start_time
                self.history.append({
                    'iteration': iteration,
                    'best_fitness': float(self.best_fitness),
                    'best_solution': self.best_solution.tolist(),
                    'time': current_time
                })
                
                # Check for convergence
                if self.known_optimum is not None and self.tolerance is not None:
                    if abs(self.best_fitness - self.known_optimum) <= self.tolerance:
                        print(f"\nConverged to known optimum within tolerance at iteration {iteration}")
                        break
                        
                # Call callback
                callback(iteration, self.best_fitness, self.best_solution)
                    
        except Exception as e:
            raise OptimizationError(f"Optimization failed: {str(e)}")
            
        # Print final results
        print_results(self.best_solution, self.best_fitness)
        
        # Save results if requested
        if self.save_results:
            from .utils import save_results
            results = {
                'best_fitness': float(self.best_fitness),
                'best_solution': self.best_solution.tolist(),
                'parameters': {
                    'pop_size': self.pop_size,
                    'max_iter': self.max_iter,
                    'obj_type': self.obj_type,
                    'neighbour_count': self.neighbour_count,
                    'gradient_strength': self.gradient_strength,
                    'base_learning_rate': self.base_learning_rate,
                    'known_optimum': self.known_optimum,
                    'timeout': self.timeout
                },
                'history': self.history
            }
            saved_file = save_results(results, self.results_dir)
            print(f"\nResults saved to: {saved_file}")
            
        return self.best_solution, self.best_fitness