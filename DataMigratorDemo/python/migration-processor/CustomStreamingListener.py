import json
import time
import logging
from kafka import KafkaProducer
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.listener import StreamingListener
from pyspark.sql import SparkSession, Row

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomStreamingListener(StreamingListener):
    def __init__(self, kafka_producer):
        self.kafka_producer = kafka_producer
        logger.info("CustomStreamingListener initialized.")

    def onBatchCompleted(self, batchCompleted):
        try:
            batch_info = batchCompleted.batchInfo()
            event_data = {
                "batchTime": batch_info.batchTime().toString(),
                "totalDelay": batch_info.totalDelay().get(),
                "numRecords": batch_info.numRecords(),
                "processingDelay": batch_info.processingDelay().get(),
                "schedulingDelay": batch_info.schedulingDelay().get()
            }
            event = {
                "event_type": "batch_completed",
                "event_timestamp": int(time.time() * 1000),
                "metadata": {
                    "source": "SparkStreamingJob",
                    "job_id": "Job123"  # Customize this as needed
                },
                "event_data": event_data
            }
            self.kafka_producer.send('spark-events', json.dumps(event).encode('utf-8'))
            logger.info(f"Sent event 'batch_completed' to Kafka: {event_data}")
        except Exception as e:
            logger.error(f"Failed to process 'batch_completed' event: {e}")

class CustomSparkListener(SparkListener):
    def __init__(self, kafka_producer):
        self.kafka_producer = kafka_producer
        logger.info("CustomSparkListener initialized.")

    def onJobEnd(self, jobEnd):
        try:
            event = {
                "event_type": "job_end",
                "event_timestamp": int(time.time() * 1000),
                "metadata": {
                    "source": "SparkJob",
                    "job_id": jobEnd.jobId()
                },
                "event_data": {
                    "job_result": str(jobEnd.jobResult())
                }
            }
            self.kafka_producer.send('spark-events', json.dumps(event).encode('utf-8'))
            logger.info(f"Sent event 'job_end' to Kafka: {event['event_data']}")
        except Exception as e:
            logger.error(f"Failed to process 'job_end' event: {e}")

    def onStageCompleted(self, stageCompleted):
        try:
            stage_info = stageCompleted.stageInfo()
            event_data = {
                "stage_id": stage_info.stageId(),
                "stage_name": stage_info.name(),
                "num_tasks": stage_info.numTasks(),
                "completion_time": stage_info.completionTime(),
                "failure_reason": stage_info.failureReason()
            }
            event = {
                "event_type": "stage_completed",
                "event_timestamp": int(time.time() * 1000),
                "metadata": {
                    "source": "SparkStage",
                    "stage_id": stage_info.stageId()
                },
                "event_data": event_data
            }
            self.kafka_producer.send('spark-events', json.dumps(event).encode('utf-8'))
            logger.info(f"Sent event 'stage_completed' to Kafka: {event_data}")
        except Exception as e:
            logger.error(f"Failed to process 'stage_completed' event: {e}")

    def onExecutorMetricsUpdate(self, executorMetricsUpdate):
        try:
            for executor_id, executor_metrics in executorMetricsUpdate.executorUpdates().items():
                event_data = {
                    "executor_id": executor_id,
                    "metrics": executor_metrics
                }
                event = {
                    "event_type": "executor_metrics_update",
                    "event_timestamp": int(time.time() * 1000),
                    "metadata": {
                        "source": "SparkExecutor",
                        "executor_id": executor_id
                    },
                    "event_data": event_data
                }
                self.kafka_producer.send('spark-events', json.dumps(event).encode('utf-8'))
                logger.info(f"Sent event 'executor_metrics_update' to Kafka: {event_data}")
        except Exception as e:
            logger.error(f"Failed to process 'executor_metrics_update' event: {e}")

def main():
    conf = SparkConf().setAppName("StreamingMetricsApp")
    sc = SparkContext(conf=conf)
    
    # Initialize Kafka producer
    kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')
    
    # Register Custom Listeners
    sc._jsc.sc().addSparkListener(CustomSparkListener(kafka_producer))
    
    ssc = StreamingContext(sc, 5)
    ssc.addStreamingListener(CustomStreamingListener(kafka_producer))

    # Example DStream processing
    lines = ssc.socketTextStream("localhost", 9999)
    words = lines.flatMap(lambda line: line.split(" "))
    word_counts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

    def save_to_db(rdd):
        if not rdd.isEmpty():
            spark = SparkSession.builder.config(conf=rdd.context.getConf()).getOrCreate()
            df = rdd.map(lambda x: Row(word=x[0], count=x[1])).toDF()
            df.write.format("jdbc").options(
                url="jdbc:mysql://localhost:3306/streaming",
                driver="com.mysql.cj.jdbc.Driver",
                dbtable="word_counts",
                user="root",
                password="password"
            ).mode("append").save()
            logger.info(f"Saved {df.count()} records to MySQL")

    word_counts.foreachRDD(save_to_db)

    ssc.start()
    ssc.awaitTermination()

if __name__ == "__main__":
    main()
