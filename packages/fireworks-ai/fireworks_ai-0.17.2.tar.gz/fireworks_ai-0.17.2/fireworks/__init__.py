from .llm import LLM
from .dataset import Dataset
import importlib.metadata

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"  # Fallback for development mode

__all__ = ["LLM", "Dataset", "__version__"]
