from typing import Any
from .exceptions import ValidationError

def validate_parameters(optimizer: Any) -> None:
    """Validate all optimizer parameters.
    
    Args:
        optimizer: GSO instance to validate
        
    Raises:
        ValidationError: If any parameter is invalid
    """
    # Required parameters
    if not isinstance(optimizer.pop_size, int) or optimizer.pop_size <= 0:
        raise ValidationError(f"Population size must be positive integer. Given: {optimizer.pop_size}")
        
    if not isinstance(optimizer.max_iter, int) or optimizer.max_iter <= 0:
        raise ValidationError(f"Maximum iterations must be positive integer. Given: {optimizer.max_iter}")
        
    if optimizer.obj_type not in ['min', 'max']:
        raise ValidationError(f"Optimization type must be 'min' or 'max'. Given: {optimizer.obj_type}")
        
    if not isinstance(optimizer.neighbour_count, int) or optimizer.neighbour_count < 1:
        raise ValidationError(f"Neighbor count must be positive integer. Given: {optimizer.neighbour_count}")
        
    if optimizer.neighbour_count >= optimizer.pop_size:
        raise ValidationError(f"Neighbor count must be less than population size")
        
    # Optional parameters
    if not (0 <= optimizer.gradient_strength <= 1):
        raise ValidationError(f"Gradient strength must be between 0 and 1. Given: {optimizer.gradient_strength}")
        
    if not (0 <= optimizer.base_learning_rate <= 1):
        raise ValidationError(f"Base learning rate must be between 0 and 1. Given: {optimizer.base_learning_rate}")
        
    # Function validations
    if not callable(optimizer.obj_func):
        raise ValidationError("Objective function must be callable")
        
    # Known optimum and tolerance
    if optimizer.known_optimum is not None and optimizer.tolerance is None:
        raise ValidationError("Tolerance must be specified when known optimum is provided")
        
    if optimizer.tolerance is not None and optimizer.tolerance <= 0:
        raise ValidationError(f"Tolerance must be positive. Given: {optimizer.tolerance}")
        
    # Timeout
    if optimizer.timeout is not None and optimizer.timeout <= 0:
        raise ValidationError(f"Timeout must be positive. Given: {optimizer.timeout}")