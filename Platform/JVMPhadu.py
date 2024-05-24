from pyspark.sql import SparkSession, Row
from Kafka import KafkaEventProducer, SparkKafkaEventsListener
import pyspark_spy



spark = (SparkSession
    .builder
    .getOrCreate()
    )

kafka_config = {'bootstrap.servers': 'localhost:9092'}

topic = 'processing_progress_events_topic'

kafka_producer = KafkaEventProducer(kafka_config, topic)
listener = SparkKafkaEventsListener(kafka_producer)
pyspark_spy.register_listener(spark.sparkContext, listener)
#  All spark processing should come after this line

df=spark.read.csv('merged_customer_data.csv', header=True,inferSchema=True)
df_cartesian = df.crossJoin(df)
all_data = df_cartesian.collect()
print(all_data)

#  All spark processing should come above this line

try:
    spark.sparkContext._gateway.shutdown_callback_server()
except Exception as e:
    pass
spark.stop()