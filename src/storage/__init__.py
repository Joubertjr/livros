"""Módulo de persistência de resumos."""
from .summary_storage import (
    SummaryStorageManager,
    get_storage_manager
)

__all__ = [
    "SummaryStorageManager",
    "get_storage_manager"
]
