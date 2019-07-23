#!/usr/bin/env bash

## Run application locally on 8 cores
#./bin/spark-submit \
#  --class org.apache.spark.examples.SparkPi \
#  --master local[8] \
#  /path/to/examples.jar \
#  100
#
## Run on a Spark standalone cluster in client deploy mode
#./bin/spark-submit \
#  --class org.apache.spark.examples.SparkPi \
#  --master spark://207.184.161.138:7077 \
#  --executor-memory 20G \
#  --total-executor-cores 100 \
#  /path/to/examples.jar \
#  1000
#
## Run on a Spark standalone cluster in cluster deploy mode with supervise
#./bin/spark-submit \
#  --class org.apache.spark.examples.SparkPi \
#  --master spark://207.184.161.138:7077 \
#  --deploy-mode cluster \
#  --supervise \
#  --executor-memory 20G \
#  --total-executor-cores 100 \
#  /path/to/examples.jar \
#  1000
#
## Run on a YARN cluster
#export HADOOP_CONF_DIR=XXX
#./bin/spark-submit \
#  --class org.apache.spark.examples.SparkPi \
#  --master yarn \
#  --deploy-mode cluster \  # can be client for client mode
#  --executor-memory 20G \
#  --num-executors 50 \
#  /path/to/examples.jar \
#  1000



# Run on a Kubernetes cluster in cluster deploy mode
#  --master k8s://137.185.232.81:443 \
#  $1 = Epsilon_v1.0-scala_2.11.12-spark_2.3.0-jar-with-dependencies.jar \
#  --master yarn \
#  --master yarn-client \
#  --files  \
#  --master yarn \
#  --conf spark.lineage.enabled=false \
#  --conf spark.dynamicAllocation.enabled=false \
#  --conf spark.eventLog.compress=true \
#  --conf spark.io.compression.codec=org.apache.spark.io.LZ4CompressionCodec \
spark2-submit \
  --class com.pg.bigdata.template.actions.Epsilon \
  --master yarn \
  --deploy-mode cluster \
  --num-executors 12 \
  --executor-cores 4 \
  --executor-memory 16G \
  --principal merz.d@NA.PG.COM \
  --keytab ~/.ssh/merz.d.keytab \
  --files config.properties \
  $1 config.properties

#  --py-files hdfs://hanameservice/user/pyrett.j/programmatic/test_framework2.zip,hdfs://hanameservice/application/prod/datapipe_status/python/dq_framework/settings.py,hdfs://hanameservice/user/pyrett.j/programmatic/debug_spark_executor.py \
# hdfs://hanameservice/user/pyrett.j/programmatic/debug_spark_executor.py \
# -p programmatic