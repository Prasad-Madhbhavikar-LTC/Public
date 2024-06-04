from Source import Type
from Source.Unsupported import NOP


class SourceFactory:
    def __init__(self) -> None:
        pass

    @staticmethod
    def create(spark_context, source_config):
        source = None
        source_type = source_config['type']
        match source_type:
            case Type.DATABASE:
                source = DataBase(spark_context, source_type)
            case Type.FILE_SYSTEM:
                source = FileSystem(spark_context, source_type)
            case Type.BUCKET:
                source = Bucket(spark_context, source_type)
            case Type.FTP:
                source = FTP(spark_context, source_type)
            case Type.STREAM:
                source = Stream(spark_context, source_type)
            case _:
                source = NOP(spark_context, source_type)

        return source
