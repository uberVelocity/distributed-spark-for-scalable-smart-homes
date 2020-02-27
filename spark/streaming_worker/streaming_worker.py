import spark
from time import sleep

if __name__ == '__main__':
    sleep(30)

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29091,kafka2:29092") \
        .option("subscribe", "historical") \
        .load()
    df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    df.show(n=2)
