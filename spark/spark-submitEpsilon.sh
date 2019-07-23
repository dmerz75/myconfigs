#!/usr/bin/env bash

# Run on a Kubernetes cluster in cluster deploy mode
#  --conf spark.yarn.max.executor.failures 4 \
#         spark.yarn.am.memoryOverhead
#  --conf spark.yarn.executor.memoryOverhead=800 \
#  --conf spark.io.compression.codec=org.apache.spark.io.LZ4CompressionCodec \
#  --conf spark.task.maxFailures 8 \
#  --conf spark.yarn.maxAppAttempts 5 \
spark2-submit \
  --conf spark.lineage.enabled=false \
  --conf spark.dynamicAllocation.enabled=false \
  --conf spark.eventLog.compress=true \
  --master yarn \
  --deploy-mode cluster \
  --class com.pg.bigdata.template.actions.Epsilon \
  --num-executors 30 \
  --executor-cores 7 \
  --executor-memory 45G \
  --principal merz.d@NA.PG.COM \
  --keytab ~/.ssh/merz.d.keytab \
  --files configBU.properties \
  $1 configBU.properties

