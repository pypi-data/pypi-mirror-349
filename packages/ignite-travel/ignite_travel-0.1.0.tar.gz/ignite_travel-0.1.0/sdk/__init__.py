# Setup the SDK as a package
from dotenv import load_dotenv
from pathlib import Path
import os
from .client import DimsInventoryClient


# Load the environment variables
load_dotenv(
  Path(__file__).parent.parent / ".env"
)

__all__ = ["DimsInventoryClient"]
