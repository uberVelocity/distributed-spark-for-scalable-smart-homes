from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import time

def read_from_kafka_topic(topic_name, broker_ports_string):
    spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", broker_ports_string) \
        .option("startingOffsets", "earliest") \
        .option("subscribe", topic_name) \
        .load()
    return df

def parse_kafka_json_into_df(kafka_json, schema):
    return stringDF.select(from_json("value", schema).alias("value"))

def push_json_to_kafka_topic(json_df, topic_name, broker_ports_string):
    return json_df
    .writeStream
    .outputMode("append")
    .format("kafka")
    .option("checkpointLocation", "/tmp/checkpoint")
    .option("kafka.bootstrap.servers", broker_ports_string)
    .option("topic", topic_name)
    .option("truncate", False)
    .start()

if __name__ == '__main__':
    print('Started script')
    originalDF = read_from_kafka_topic("sensor_data", "kafka:29091,kafka2:29092")
    stringDF = originalDF.selectExpr("CAST(value AS STRING)")

    schema = StructType([
        StructField("id", DoubleType(), False),
        StructField("t", DoubleType(), False)
    ])
    df = parse_kafka_json_into_df(stringDF, schema)

    manipulatedDF = df.select("value.*").select(to_json(struct("id", "t")).alias("value"))

    query = push_json_to_kafka_topic(manipulatedDF, "predictions", "sensor_data", "kafka:29091,kafka2:29092")
    time.sleep(30)
    query.stop()