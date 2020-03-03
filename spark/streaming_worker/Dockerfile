FROM bitnami/spark:2.4.5

COPY streaming_worker.py /opt/bitnami/spark

USER root
RUN mkdir .ivy2
RUN chown 1001:1001 .ivy2
USER 1001

#RUN pip install --no-cache-dir -r requirements.txt
# spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-streaming-kafka-0-8_2.12:2.4.5 --py-files streaming_worker.py streaming_worker.py