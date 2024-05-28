import os
import yaml
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from datetime import datetime
import pyspark_spy

from Kafka import KafkaEventProducer, SparkKafkaEventsListener
import argparse

class datasourcefactory:
    @staticmethod
    def read_data_source(spark, source_details, job_config):
        source_type = source_details['source_type']

        if source_type == 'database':
            return DatabaseDataSource(spark, source_details, job_config)
        elif source_type == 'FILE_SYSTEM':
            return FileSystemDataSource(spark, source_details, job_config)
        elif source_type in ['image', 'video']:
            return ImageOrVideoDataSource(spark, source_details, job_config)
        else:
            raise ValueError(f"Unsupported file type: {source_type}")

class DataSource:
    def __init__(self, spark, source_details):
        self.spark = spark
        self.source_details = source_details

    def read_data(self):
        raise NotImplementedError("Subclasses must implement read_data method")

class DatabaseDataSource(DataSource):
    def __init__(self, spark, source_details, job_config):
        super().__init__(spark, source_details)
        self.job_config = job_config

    def read_data(self, secrets):
        jdbc_url = self.source_details['url']
        table_name = self.job_config['name']
        schema = self.job_config.get('schema', 'public')
        predicates = self.job_config.get('predicates', [])
        username = secrets.get('username', '')
        password = secrets.get('password', '')

        df = self.spark.read.format('jdbc') \
            .option("url", jdbc_url) \
            .option("dbtable", f"{schema}.{table_name}") \
            .option("user", username) \
            .option("password", password) \
            .load()

        return df

class FileSystemDataSource(DataSource):
    def __init__(self, spark, source_details, job_config):
        super().__init__(spark, source_details)
        self.job_config = job_config

    def read_data(self):
        file_path = self.source_details['path']
        file_type = self.source_details['file_Type']

        if file_type == 'csv':
            return self.spark.read.csv(file_path, header=True, inferSchema=True)
        elif file_type == 'json':
            return self.spark.read.json(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

class DataMigrator:
    def __init__(self, spark):
        self.spark = spark

    def read_config_file(self, *file_paths):
        combined_config = {}

        for file_path in file_paths:
            try:
                with open(file_path, "r") as file:
                    config = yaml.safe_load(file)
                    combined_config.update(config)
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except yaml.YAMLError as exc:
                print(f"Error parsing YAML file: {file_path}\n{exc}")

        return combined_config

    def read_data_source(self, source_details, job_config):
        data_source = datasourcefactory.read_data_source(self.spark, source_details, job_config)
        return data_source.read_data()

    def df_transformation(self, df, source_details):
        # Placeholder for any transformations
        return df

    def write_to_destination(self, df, destination_details):
        file_format = destination_details.get('format', 'csv')
        path = destination_details.get('path', '')
        name = destination_details.get('name', 'output_file')

        if not path:
            raise ValueError("Destination path is required in the configuration.")

        # Get today's date and format it
        today = datetime.today().strftime('%d-%m-%Y')

        # Construct the output file name
        output_file_name = f"{name}_{today}"

        # Determine the full output path
        output_path = os.path.join(path, output_file_name)

        # Write the DataFrame to the destination path with overwrite mode
        if file_format == 'parquet':
            df.write.mode('overwrite').parquet(output_path)
        elif file_format == 'csv':
            # df.write.mode('overwrite').csv(output_path)
            df.write.mode('overwrite').option("header", "true").csv(output_path)
        elif file_format == 'json':
            df.write.mode('overwrite').json(output_path)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")

    def migrate_data(self, source_details, job_config, destination_details):
        df = self.read_data_source(source_details, job_config)
        df.show(5)
        df = self.df_transformation(df, source_details)
        self.write_to_destination(df, destination_details)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--job", type=str , help = "Provide the Job name that needs to be run")
    args = parser.parse_args()
    
    job_name = args.job
    src_dir="../../Processing_Folder/Job_dump"
    config_file = f"{src_dir}/{job_name}_job_configurations.yaml"
    config_file_des = f"{src_dir}/{job_name}_destination_details.yaml"
    config_file_access = f"{src_dir}/{job_name}_access_data.yaml"

    spark = SparkSession.builder \
        .appName(job_name) \
        .getOrCreate()

    kafka_config = {'bootstrap.servers': 'localhost:9092'}

    topic = 'processing_progress_events_topic'

    kafka_producer = KafkaEventProducer(kafka_config, topic)
    listener = SparkKafkaEventsListener(kafka_producer)
    pyspark_spy.register_listener(spark.sparkContext, listener)



    #  All spark processing should come below this line
    
    migrator = DataMigrator(spark)
    combined_config = migrator.read_config_file(config_file, config_file_des, config_file_access)
    source_details = combined_config.get('source', {})
    job_config = combined_config.get('job', {})
    destination_details = combined_config.get('destination', {})
    migrator.migrate_data(source_details, job_config, destination_details)
    
    #  All spark processing should come above this line

    try:
        spark.sparkContext._gateway.shutdown_callback_server()
    except Exception as e:
        pass

    spark.stop()