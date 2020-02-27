from pyspark.sql import SparkSession

if __name__ == '__main__':
    print('Started script')
    spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29091,kafka2:29092") \
        .option("subscribe", "historical") \
        .load()
    df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    print('showing df')
    df.show(n=2)
    spark.stop()
