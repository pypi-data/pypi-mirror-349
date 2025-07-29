from .base import Storage
from .json_file_storage import JsonFileStorage
# Import your concrete backends here if you like:
# from .postgres_storage import PostgresStorage
# from .json_file_storage import JsonFileStorage

__all__ = ["Storage", "JsonFileStorage"]