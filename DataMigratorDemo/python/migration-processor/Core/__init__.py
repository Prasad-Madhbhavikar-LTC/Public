__all__ = [
    'Format',
    'Type'
]

import logging
from enum import Enum

logging.getLogger(__name__).addHandler(logging.NullHandler())


class Format(Enum):
    UNSUPPORTED = 0
    CSV = 1
    PARQUET = 2
    JSON = 3
    XML = 4
    IMAGE = 10


    VIDEO = 11
    AUDIO = 12
    TABLE = 20


class Type(Enum):
    UNSUPPORTED = 0
    DATABASE = 1
    FILE_SYSTEM = 2
    BUCKET = 10
    STREAM = 11
    FTP = 12
