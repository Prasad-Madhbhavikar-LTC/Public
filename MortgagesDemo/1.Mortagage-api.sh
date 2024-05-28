echo "Starting the Backend API server"
cd Mortgage-api
gradle clean build
cd build/libs
java -jar MortgageManagementSystem-0.0.1-SNAPSHOT.jar