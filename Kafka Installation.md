# Kafka Installation

## Prerequisites

This document assumes that the below prerequisites have been already satisfied.  

1. You have [WSL enabled](./pyDeeQu%20Installation.md#enable-and-install-wsl)  
2. You have successfully installed Scala (Provided you are using scala!)

## Installation

1. Going forward make sure you are in the correct environment, if now run the command below every time you open a new ubuntu terminal.
    ```
    conda activate spark
    ```

2. In this terminal run the following commands  
    ```
    mkdir -p ~/nonSDKManSDK
    cd ~/nonSDKManSDK
    wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz
    tar -zxvf kafka_2.13-3.7.0.tgz
    rm kafka_2.13-3.7.0.tgz
    ```
3. Set the environment variables in the `~/.bashrc` file, at the end

    ```
    nano ~/.bashrc
    ```

    Append the following lines  

    ```
    export KAFKA_HOME=~/nonSDKManSDK/kafka_2.13-3.7.0
    export PATH=${PATH}:~/nonSDKManSDK/kafka_2.13-3.7.0/bin
    ```

4. Run Kafka with default configurations  
    1. Open a new terminal and set the correct environment by following the step 1
        Start the Zookeeper server  
        ```
        cd ${KAFKA_HOME}/bin
        ./zookeeper-server-start.sh ../config/zookeeper.properties
        ```  
    2. I another terminal window set the correct environment by following step 1  
        Start the Kafka Broker service  
        ```
        cd ${KAFKA_HOME}/bin
        ./kafka-server-start.sh ../config/server.properties
        ```  

    You can also use the below aliases in the `~/.bashrc` file to save some keystrokes.

    ```  
    alias skafka='kafka-server-start.sh ${KAFKA_HOME}/config/server.properties'
    alias szoo='zookeeper-server-start.sh ${KAFKA_HOME}/config/zookeeper.properties'
    ```
5. You have successfully installed basic kafka. [Refer](https://kafka.apache.org/36/documentation.html#quickstart) the official doc for further configurations  