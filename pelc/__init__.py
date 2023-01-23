import importlib.metadata

__version__: str = importlib.metadata.version("pelc")

from . import batch_eplet_comp, batch_eplet_comp_aux, output_type
