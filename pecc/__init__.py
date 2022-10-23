import importlib.metadata

__version__: str = importlib.metadata.version("pecc")

from . import epitope_comparison
