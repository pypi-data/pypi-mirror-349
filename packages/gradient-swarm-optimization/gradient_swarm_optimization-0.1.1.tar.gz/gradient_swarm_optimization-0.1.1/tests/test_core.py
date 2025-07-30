"""Unit tests for GSO core functionality."""

import unittest
import numpy as np
from gso import GSO
from gso.exceptions import ValidationError, OptimizationError, TimeoutError

class TestGSO(unittest.TestCase):
    """Test cases for GSO algorithm."""
    
    def setUp(self):
        """Set up test cases."""
        self.dim = 10
        self.pop_size = 20
        
        # Simple fitness function for testing
        def simple_fitness(solution):
            return np.sum(solution)
            
        self.fitness_func = simple_fitness
        
    def test_initialization(self):
        """Test optimizer initialization."""
        optimizer = GSO(
            pop_size=self.pop_size,
            max_iter=100,
            obj_type='max',
            neighbour_count=3,
            obj_func=self.fitness_func,
            dim=self.dim
        )
        
        self.assertEqual(optimizer.pop_size, self.pop_size)
        self.assertEqual(optimizer.dim, self.dim)
        self.assertEqual(optimizer.population.shape, (self.pop_size, self.dim))
        
    def test_invalid_parameters(self):
        """Test parameter validation."""
        # Test invalid population size
        with self.assertRaises(ValidationError):
            GSO(pop_size=-1, max_iter=100, obj_type='max',
                neighbour_count=3, obj_func=self.fitness_func, dim=self.dim)
                
        # Test invalid objective type
        with self.assertRaises(ValidationError):
            GSO(pop_size=20, max_iter=100, obj_type='invalid',
                neighbour_count=3, obj_func=self.fitness_func, dim=self.dim)
                
        # Test invalid neighbor count
        with self.assertRaises(ValidationError):
            GSO(pop_size=20, max_iter=100, obj_type='max',
                neighbour_count=0, obj_func=self.fitness_func, dim=self.dim)
                
    def test_optimization(self):
        """Test basic optimization run."""
        optimizer = GSO(
            pop_size=self.pop_size,
            max_iter=50,
            obj_type='max',
            neighbour_count=3,
            obj_func=self.fitness_func,
            dim=self.dim,
            seed=42
        )
        
        best_solution, best_fitness = optimizer.optimize()
        
        self.assertEqual(len(best_solution), self.dim)
        self.assertGreaterEqual(best_fitness, 0)
        
    def test_convergence(self):
        """Test convergence to known optimum."""
        # Simple problem where optimum is known
        def test_fitness(solution):
            return np.sum(solution)
            
        optimizer = GSO(
            pop_size=20,
            max_iter=100,
            obj_type='max',
            neighbour_count=3,
            obj_func=test_fitness,
            dim=5,
            known_optimum=5.0,
            tolerance=1e-6,
            seed=42
        )
        
        best_solution, best_fitness = optimizer.optimize()
        self.assertAlmostEqual(best_fitness, 5.0, places=6)

    def test_timeout(self):
        """Test timeout functionality."""
        def slow_fitness(solution):
            import time
            time.sleep(0.01)  # Reduced sleep time
            return np.sum(solution)
            
        # Test that optimization completes with adequate timeout
        optimizer = GSO(
            pop_size=10,  # Reduced population size
            max_iter=20,  # Reduced iterations
            obj_type='max',
            neighbour_count=3,
            obj_func=slow_fitness,
            dim=5,
            timeout=5  # Increased timeout
        )
        
        # This should complete successfully
        best_solution, best_fitness = optimizer.optimize()
        
        # Now test timeout error
        optimizer = GSO(
            pop_size=20,
            max_iter=1000,
            obj_type='max',
            neighbour_count=3,
            obj_func=slow_fitness,
            dim=5,
            timeout=0.1  # Very short timeout
        )
        
        with self.assertRaises(OptimizationError) as context:
            optimizer.optimize()
        self.assertIn("timeout", str(context.exception).lower())
            
    def test_history_tracking(self):
        """Test optimization history tracking."""
        optimizer = GSO(
            pop_size=20,
            max_iter=50,
            obj_type='max',
            neighbour_count=3,
            obj_func=self.fitness_func,
            dim=5
        )
        
        optimizer.optimize()
        
        self.assertGreater(len(optimizer.history), 0)
        for entry in optimizer.history:
            self.assertIn('iteration', entry)
            self.assertIn('best_fitness', entry)
            self.assertIn('best_solution', entry)
            self.assertIn('time', entry)

if __name__ == '__main__':
    unittest.main()