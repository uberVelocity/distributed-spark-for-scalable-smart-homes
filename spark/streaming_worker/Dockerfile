FROM bitnami/spark:2

WORKDIR /usr/src/app

COPY . .

#RUN pip install --no-cache-dir -r requirements.txt
spark-submit --master spark://spark_master:8080 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:2.4.5 --py-files streaming_worker.py
     