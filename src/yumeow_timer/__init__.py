"""
yumeow-timer: Lightweight timing utilities for optional performance diagnostics.

Provides Timer, NamedTimer, and ParallelTimer classes for tracking
execution time and iteration counts with human-readable output.
"""

from .timing import Timer, NamedTimer, ParallelTimer

__version__ = "0.1.0"
__all__ = ["Timer", "NamedTimer", "ParallelTimer", "__version__"]
