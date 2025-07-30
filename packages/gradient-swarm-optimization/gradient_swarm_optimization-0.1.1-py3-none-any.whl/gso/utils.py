"""Utility functions for GSO algorithm."""

import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Union, Optional, Callable

def get_cli_args() -> argparse.Namespace:
    """Get command line arguments for GSO."""
    parser = argparse.ArgumentParser(description='Gradient-guided Swarm Optimization')
    parser.add_argument('--save-results', choices=['yes', 'no'], default='no',
                      help='Whether to save optimization results')
    parser.add_argument('--results-dir', type=str, default='results',
                      help='Directory to save results')
    parser.add_argument('--seed', type=int, default=None,
                      help='Random seed for reproducibility')
    return parser.parse_args()

def default_callback(iteration: int, best_fitness: float, best_solution: Any) -> None:
    """Default callback function for optimization progress."""
    if iteration % 10 == 0:  # Print every 10 iterations
        print(f"Iteration {iteration}: Best Fitness = {best_fitness}")

def print_results(best_solution: Any, best_fitness: float) -> None:
    """Print optimization results."""
    print("\nOptimization completed!")
    print(f"Best solution: {best_solution}")
    print(f"Best fitness: {best_fitness}")

def save_results(
    results: Dict[str, Any],
    output_dir: Union[str, Path],
    prefix: str = "",
    include_fitness: bool = True,
    include_timestamp: bool = True
) -> Path:
    """Save optimization results to a JSON file.
    
    Args:
        results: Dictionary containing optimization results
        output_dir: Directory to save the results
        prefix: Optional prefix for the filename
        include_fitness: Whether to include fitness in filename
        include_timestamp: Whether to include timestamp in filename
        
    Returns:
        Path object of the saved file
    """
    # Convert to Path object
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build filename
    filename_parts = []
    if prefix:
        filename_parts.append(prefix)
    if include_fitness and 'best_fitness' in results:
        filename_parts.append(f"f{results['best_fitness']:.6f}")
    if include_timestamp:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename_parts.append(timestamp)
    
    filename = '_'.join(filename_parts) + '.json'
    output_file = output_dir / filename
    
    # Add metadata
    results_to_save = results.copy()
    results_to_save['timestamp'] = datetime.now().isoformat()
    
    # Save to file
    with open(output_file, 'w') as f:
        json.dump(results_to_save, f, indent=2)
        
    return output_file

def load_results(filepath: Union[str, Path]) -> Dict[str, Any]:
    """Load optimization results from a JSON file.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Dictionary containing the loaded results
    """
    with open(filepath, 'r') as f:
        return json.load(f)

def format_time(seconds: float) -> str:
    """Format time duration in a human-readable format.
    
    Args:
        seconds: Time duration in seconds
        
    Returns:
        Formatted time string
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{int(minutes)}m {int(remaining_seconds)}s"
    else:
        hours = seconds // 3600
        remaining = seconds % 3600
        minutes = remaining // 60
        seconds = remaining % 60
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"