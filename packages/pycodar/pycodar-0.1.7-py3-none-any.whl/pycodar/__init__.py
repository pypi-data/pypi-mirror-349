"""
Codar - A Radar for Your Code
A simple tool for auditing and understanding your codebase.
"""

__version__ = "0.1.6"

from .cli import main
from .analyze import analyze_directory

__all__ = ['main', 'analyze_directory'] 