__all__ = [
    'Format',
    'Type',
    'Migrator'
]

import logging
from enum import Enum, auto

logging.getLogger(__name__).addHandler(logging.NullHandler())


class Format(Enum):
    UNSUPPORTED = auto()
    CSV = auto()
    PARQUET = auto()
    JSON = auto()
    # XML = auto()
    # IMAGE = auto()
    # VIDEO = auto()
    # AUDIO = auto()
    # TABLE = auto()


class Type(Enum):
    UNSUPPORTED = auto()
    # DATABASE = auto()
    FILE_SYSTEM = auto()
    # BUCKET = auto()
    # STREAM = auto()
    # FTP = auto()