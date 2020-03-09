FROM bitnami/spark:latest

COPY regression.py /opt/bitnami/spark

USER root
RUN mkdir .ivy2
RUN chown 1001:1001 .ivy2
USER 1001

# spark-submit --master spark://spark-master:7077 --packages com.datastax.spark:spark-cassandra-connector_2.11:2.4.2 --conf spark.cassandra.connection.host=cassandra-cluster:9042 --py-files regression.py regression.py
