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
        StructField("timestamp", TimestampType(), False),
        StructField("sensors", StructType([
            StructField("wattage", DoubleType(), False)
        ]), False)
    ])
    def parse_data_from_kafka_message(stringDF, schema):
        from pyspark.sql.functions import split
        assert stringDF.isStreaming == True, "DataFrame doesn't receive streaming data"
        col = split(stringDF['value'], ',')
        for index, field in enumerate(schema):
            stringDF = stringDF.withColumn(field.name, col.getItem(index).cast(field.dataType))
        return stringDF.select([field.name for field in schema])
    
    #df = parse_data_from_kafka_message(stringDF, schema)
    df = stringDF.select(from_json("value", schema))
    manipulatedDF = df
    stringDF.printSchema()
    # Print the stream for 10 seconds
    query = stringDF.writeStream.outputMode("append").format("console").option("truncate", False).start().awaitTermination()
    # time.sleep()
    # query.stop()