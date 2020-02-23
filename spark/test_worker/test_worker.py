"""
Spark packages need to be called at job commission, which are then available in the script by some package name, through
the usual import statements
"""
import pyspark_cassandra

if __name__ == '__main__':
    conf = SparkConf() \
        .setAppName("PySpark Cassandra Test") \
        .setMaster("spark://spark-master:7077") \
        .set("spark.cassandra.connection.host", "cas-1")

    sc = CassandraSparkContext(conf=conf)

    sc \
        .cassandraTable("keyspace", "table") \
        .select("col-a", "col-b") \
        .where("key=?", "x") \
        .filter(lambda r: r["col-b"].contains("foo")) \
        .map(lambda r: (r["col-a"], 1)
             .reduceByKey(lambda a, b: a + b)
             .collect()

    pass
