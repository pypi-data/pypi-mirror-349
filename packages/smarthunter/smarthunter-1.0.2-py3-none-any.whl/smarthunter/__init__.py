"""SmartHunter - A tool to find encoded strings in binary files."""

__version__ = "1.0.2"

from .main import scan_file

__all__ = ["scan_file"] 