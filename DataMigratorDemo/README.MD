/home/prasad/Development/DataMigratorDemo/Processing_Folder/Source/fake_customer_data.csv
/home/prasad/Development/DataMigratorDemo/Processing_Folder/Sink
/home/prasad/Development/DataMigratorDemo/Processing_Folder/Job_dump




cd ~/Development/DataMigratorDemo/node/datajob-config-provider && ng serve


cd ~/Development/DataMigratorDemo/java/DataJobConfigProvider && gradle build && cp build/libs/DataJobConfigProvider-0.0.1-SNAPSHOT.jar .

cd ~/Development/DataMigratorDemo/java/DataJobConfigProvider &&  java -jar DataJobConfigProvider-0.0.1-SNAPSHOT.jar



conda deactivate && conda activate sparkd && sdk use java  11.0.23-ms && cd ~/Development/DataMigratorDemo/java/JobWatcher &&  java JobWatcher /home/prasad/Development/DataMigratorDemo/Processing_Folder/Job_dump python3  /home/prasad/Development/DataMigratorDemo/vpython/DataMigratorProcessor/try.py test



kafka-console-consumer.sh --topic processing_progress_events_topic --from-beginning --bootstrap-server localhost:9092