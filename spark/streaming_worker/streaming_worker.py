from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
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
    stringDF = df.selectExpr("CAST(value AS STRING)")

    schema = StructType([
        StructField("id", DoubleType(), False),
        StructField("t", DoubleType(), False)
    ])

    df = stringDF.select(from_json("value", schema).alias("value")).select("value.*")#.selectExpr("CAST(id AS DOUBLE", "CAST(t AS DOUBLE)")
    manipulatedDF = df
    print("########################")
    stringDF.printSchema()
    print("########################")
    df.printSchema()
    print("########################")
    # Print the stream for 10 seconds
    query = df.writeStream.outputMode("append").format("console").option("truncate", False).start()#.awaitTermination()
    time.sleep(5)
    query.stop()