import importlib.metadata

__version__: str = importlib.metadata.version("pecc")

from . import epitope_comparison, epitope_comparison_aux, output_type
