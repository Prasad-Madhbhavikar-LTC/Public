 sdk use java 11.0.23-ms
 sdk use scala 2.12.19
 sdk use spark 3.1.2
 sdk use hadoop 3.1.4


export SPARK_VERSION='3.1'


java -version
scala -version
spark-submit --version
python3 -V
pip3 -V
pyspark --version


 pip install pyspark==3.1.2 pydeequ==1.0.1



kafka-topics.sh --create --topic processing_progress_events_topic --bootstrap-server localhost:9092
kafka-topics.sh --describe --topic processing_progress_events_topic --bootstrap-server localhost:9092
kafka-console-consumer.sh --topic processing_progress_events_topic --from-beginning --bootstrap-server localhost:9092