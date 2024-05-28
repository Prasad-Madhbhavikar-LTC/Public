echo "Starting the Backend API server"
cd java/config-api
gradle clean build
cd build/libs
java -jar DataJobConfigProvider-0.0.1-SNAPSHOT.jar