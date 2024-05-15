# PyDeeQu Installation  

## Enable and install WSL

Open a Power shell window and run the following commands

1. Enable WSL

    ```
    wsl --install --no-distribution
    ```

    It may ask you to reboot, do it now

2. Install Ubuntu, and do the pre configuration as below  

    ```
    wsl --set-default-version 2
    wsl --install --distribution Ubuntu
    ```

    This command will lead you to a ubuntu terminal.  
  
    ```
    sudo su -
    ```

    Run the below command  

    ```
    cat <<EOF> /etc/wsl.conf
    [boot]
    systemd=true
    
    [network]
    generateResolvConf = false
    EOF
    ```  

    Now run the below command

    ```
    cat <<EOF> /etc/resolv.conf
    nameserver 8.8.8.8
    nameserver 4.4.4.4
    nameserver 1.1.1.1
    EOF
    ```

    Logout the root user

    ```
    exit
    ```

3. Update the distro and install the prerequisites

    ```
    sudo apt update 
    sudo apt upgrade
    sudo apt install zip unzip git python3-pip
    ```

4. We will install the required softwares now.
    + Java 11
    + Scala 2.13
    + Spark 2.13
    + Hadoop 3.3
    + Gradle and Maven (Optional)

    You have 2 options  
    1. Install every software manually and the set the corresponding software home and path in the `~/.bashrc` file.

        You would need to set the following environment variables
        + JAVA_HOME
        + SCALA_HOME
        + SPARK_HOME
        + HADOOP_HOME
        + GRADLE_HOME
        + M2_HOME and MAVEN_HOME

    2. Use a automated process using **SDK Manager** which would allow you to use multiple versions simulataniously.
        In the Ubuntu terminal which is already open run the below commands  

        ```
        curl -s "https://get.sdkman.io" | bash
        ```

        Close the terminal and reopen a new Ubuntu terminal

        ```
        sdk install java 11.0.23-ms
        sdk install scala 2.13.14
        sdk install spark 3.5.0
        sdk install hadoop 3.3.5

        # optionally for graddle and maven
        sdk install mvnd
        sdk install gradle
        ```

5. Optionally you can install Ananconda, to have better control over the environment

    ```
    wget https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh 
    bash Anaconda3-2024.02-1-Linux-x86_64.sh
    rm Anaconda3-2024.02-1-Linux-x86_64.sh
    exit
    ```

    Close the Terminal and open a new Ubuntu terminal to run the below commands

    ```
    conda create --name spark
    ```

    Going forward make sure you are in the correct environment, if now run the command below every time you open a new ubuntu terminal.

    ```
    conda activate spark
    ```

6. Download the DeeQu dependancy

    ```
    wget https://repo1.maven.org/maven2/com/amazon/deequ/deequ/2.0.7-spark-3.5/deequ-2.0.7-spark-3.5.jar -O ${SPARK_HOME}/jars/deequ-2.0.7-spark-3.5.jar
    ```

7. Assuming you are using conda as described in the step 5, make sure you are in the correct environment `(spark)` if not, run the `conda activate spark`

    Run this command to install python dependancies

    ```
    pip3 install pyspark==3.5.1 pydeequ==1.3.0
    ```

8. Set the environment variables in the `~/.bashrc` file, at the end

    ```
    nano ~/.bashrc
    ```

    Append the following lines  

    ```
    export SPARK_VERSION='3.3'
    export PATH="${PATH}:/home/prasad/.local/bin"
    ```

    You can also use the below aliases.

    ```  
    alias py=python3
    alias python=python3
    alias pip=pip3

    alias cas="conda activate spark"
    alias cab="conda activate base"
    alias cde="conda deactivate"
    ```  

9. Check if every thing is correctly installed  

    ```
    java -version
    scala -version
    spark-submit --version
    python3 -V
    pip3 -V
    pyspark --version
    ```

10. Run a sample code to test pydeequ is working correctly  

    ```
    from pyspark.sql import SparkSession, Row
    import pydeequ

    spark = (SparkSession
        .builder
        .config("spark.jars.packages", pydeequ.deequ_maven_coord)
        .config("spark.jars.excludes", pydeequ.f2j_maven_coord)
        .getOrCreate())

    df = spark.sparkContext.parallelize([
        Row(a="foo", b=1, c=5),
        Row(a="bar", b=2, c=6),
        Row(a="baz", b=3, c=None)]).toDF()

    from pydeequ.analyzers import *

    analysisResult = AnalysisRunner(spark) \
        .onData(df) \
        .addAnalyzer(Size()) \
        .addAnalyzer(Completeness("b")) \
        .run()

    analysisResult_df = AnalyzerContext.successMetricsAsDataFrame(spark, analysisResult)
    analysisResult_df.show()

    from pydeequ.profiles import *

    result = ColumnProfilerRunner(spark) \
        .onData(df) \
        .run()

    for col, profile in result.profiles.items():
        print(profile)
    ```

11. Open a Power shell window and run the below command

    ```
    wsl --set-default Ubuntu
    ```
