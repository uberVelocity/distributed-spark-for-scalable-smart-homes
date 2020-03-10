from pyspark.sql import SparkSession
import time
if __name__ == '__main__':
    print('Started script')
    spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29091,kafka2:29092") \
        .option("startingOffsets", "earliest") \
        .option("subscribe", "sensor_data") \
        .load()
    dataframe = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
    
    # Print the stream for 10 seconds
    query = df.writeStream.format("console").start() 
    time.sleep(10)
    query.stop()