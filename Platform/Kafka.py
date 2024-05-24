import json
import time    
from Events import EventProducer
from confluent_kafka import Producer

from pyspark_spy.interface import SparkListener

class KafkaEventProducer(EventProducer):
    def __init__(self, kafka_config, topic_name):
        super().__init__("Kafka")
        self.__kafka_producer = Producer(kafka_config)
        self.__topic_name = topic_name
    
    def send_event(self, event_name, event_data, event_creation_time : int):
        message= {
            "meta" : {
                "source" : self._producer_name,
                "creation_time" : event_creation_time,
                "received_time" : int(time.time())
            },
            "data" :{
            "event_name" : event_name,
            "event_data" : self.__convert_java_object(event_data)
            }
        }
        
        self.__kafka_producer.produce(self.__topic_name, key=event_name, value=json.dumps(message))
        self.__kafka_producer.flush()

    def __convert_java_object(self, obj):
        if self.__is_java_object(obj):
            python_dict = {}
            for field in obj.getClass().getDeclaredFields():
                field.setAccessible(True)
                name = field.getName()
                value = field.get(obj)
                if isinstance(value, (str, int, float)):
                    python_dict[name] = self.__convert_java_object(value)
            return python_dict
        elif isinstance(obj, dict):
            new_dict = {}
            for key, value in obj.items():
                if isinstance(value, (str, int, float)):
                    new_dict[key] = self.__convert_java_object(value)
            return new_dict
        else:
            return obj


    
    def __is_java_object(self, obj):
        return 'JavaObject' in str(type(obj))

    
    def __is_java_object(self, obj):
        return 'JavaObject' in str(type(obj))
            

class SparkKafkaEventsListener(SparkListener):
    def __init__(self, producer:EventProducer):
        self.__producer = producer

    def on_spark_event(self, event_name, java_event):
        self.__producer.send_event(event_name, java_event, int(time.time()))

    def onApplicationEnd(self, application_end):
        self.__producer.send_event('applicationEnd', application_end, int(time.time()))

    def onApplicationStart(self, application_start):
        self.__producer.send_event('applicationStart', application_start, int(time.time()))

    def onBlockManagerRemoved(self, block_manager_removed):
        self.__producer.send_event('blockManagerRemoved', block_manager_removed, int(time.time()))

    def onBlockUpdated(self, block_updated):
        self.__producer.send_event('blockUpdated', block_updated, int(time.time()))
        
    def onEnvironmentUpdate(self, environment_update):
        self.__producer.send_event('environmentUpdate', environment_update, int(time.time()))

    def onExecutorAdded(self, executor_added):
        self.__producer.send_event('executorAdded', executor_added, int(time.time()))

    def onExecutorMetricsUpdate(self, executor_metrics_update):
        self.__producer.send_event('executorMetricsUpdate', executor_metrics_update, int(time.time()))

    def onExecutorRemoved(self, executor_removed):
        self.__producer.send_event('executorRemoved', executor_removed, int(time.time()))

    def onJobEnd(self, job_end):
        self.__producer.send_event('jobEnd', job_end, int(time.time()))

    def onJobStart(self, job_start):
        self.__producer.send_event('jobStart', job_start, int(time.time()))

    def onOtherEvent(self, other_event):
        self.__producer.send_event('otherEvent', other_event, int(time.time()))

    def onStageCompleted(self, stage_completed):
        self.__producer.send_event('stageCompleted', stage_completed, int(time.time()))

    def onStageSubmitted(self, stage_submitted):
        self.__producer.send_event('stageSubmitted', stage_submitted, int(time.time()))

    def onTaskEnd(self, task_end):
        self.__producer.send_event('taskEnd', task_end, int(time.time()))

    def onTaskGettingResult(self, task_getting_result):
        self.__producer.send_event('taskGettingResult', task_getting_result, int(time.time()))

    def onTaskStart(self, task_start):
        self.__producer.send_event('taskStart', task_start, int(time.time()))

    def onUnpersistRDD(self, unpersist_rdd):
        self.__producer.send_event('unpersistRDD', unpersist_rdd, int(time.time()))
