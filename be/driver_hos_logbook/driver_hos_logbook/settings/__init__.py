from pathlib import Path
from .settings import Dev, Prod

# Load .env file
BASE_DIR = Path(__file__).resolve().parent.parent.parent

__all__ = [
    'Dev',
    'Prod'
]