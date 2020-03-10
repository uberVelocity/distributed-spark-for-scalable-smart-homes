import os

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.functions import mean as _mean, stddev as _stddev, col
import pyspark.sql.functions as f

def load_and_get_table_df(keys_space_name, table_name):
    """
    Reads a table from a Cassandra keyspace as a PySpark DataFrame.
    :param keys_space_name: Cassandra keyspace as string.
    :param table_name: Table in keyspace as string.
    :return: PySpark DataFrame containing table data.
    """
    table_df = sql_context.read\
        .format("org.apache.spark.sql.cassandra")\
        .options(table=table_name, keyspace=keys_space_name)\
        .load()
    return table_df

def z_scores(x, mean, std):
    print(x[0])
    return (x - mean) / std


if __name__ == '__main__':

    spark_config = SparkConf()
    spark_config.set('spark.cassandra.connection.host', 'cassandra-cluster')

    spark_context = SparkContext(master='spark://spark-master:7077', appName='regression', conf=spark_config)
    sql_context = SQLContext(spark_context)  # needed to be able to query data.

    heaters = load_and_get_table_df('household', 'heatersensor')
    heaters.show()

    # Compute the mean and std of the 'temp' column
    df_stats = heaters.select(
    _mean(col('temp')).alias('mean'),
    _stddev(col('temp')).alias('std')
    ).collect()

    # Store mean and std
    mean = df_stats[0]['mean']
    std = df_stats[0]['std']

    # Set z-score threshold
    threshold = 0.4

    # Compute z-scores of 'temp' column
    z_scores = heaters.select('temp').rdd.map(lambda x:((x[0] - mean) / std, 1)).toDF()
    print('z_scores df: ', z_scores.show())

    # Filter z-scores values above threshold
    filtered = z_scores.filter(f.col('_1') > threshold)
    print('FILTER: ', filtered.show())

    # Reduce (count how many)
    reduced = filtered.rdd.reduce(lambda a, b: ('sum', a[1] + b[1]))[1]
    print('REDUCED: ', reduced)
    
    # Finish
    spark_context.stop()

