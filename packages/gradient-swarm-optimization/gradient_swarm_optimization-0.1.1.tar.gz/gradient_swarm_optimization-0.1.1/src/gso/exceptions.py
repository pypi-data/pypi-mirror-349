class OptimizationError(Exception):
    """Base exception class for optimization errors."""
    pass

class ConvergenceError(OptimizationError):
    """Raised when the algorithm fails to converge."""
    pass

class TimeoutError(OptimizationError):
    """Raised when optimization exceeds the specified timeout."""
    pass

class ValidationError(OptimizationError):
    """Raised when input parameters fail validation."""
    pass