import importlib.metadata

__version__: str = importlib.metadata.version("pelc")

from . import eplet_comparison, eplet_comparison_aux, output_type
