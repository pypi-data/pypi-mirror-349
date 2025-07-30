"""
JavaScript snippets package for Hermes Inspector.

This package contains JavaScript code generation classes used by the Hermes Inspector
to interact with React Native applications via the Hermes debugger.
"""

# Import classes for convenient access
from .ui import UI
from .interaction import Interaction

__all__ = ["UI", "Interaction"] 