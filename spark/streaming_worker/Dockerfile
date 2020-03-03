FROM bitnami/spark:2

WORKDIR /usr/src/app

COPY . .

#RUN pip install --no-cache-dir -r requirements.txt
spark-submit --master spark://spark-master:7077 --py-files streaming_worker.py streaming_worker.py