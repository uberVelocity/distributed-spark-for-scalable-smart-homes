import os

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.functions import mean as _mean, stddev as _stddev, col

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

    # Store the average of the "temperature" column
    df_stats = heaters.select(
    _mean(col('temp')).alias('mean'),
    _stddev(col('temp')).alias('std')
    ).collect()

    # Compute mean and std
    mean = df_stats[0]['mean']
    std = df_stats[0]['std']

    # Collect all Rows of 'temp' column
    rows = heaters.select('temp').collect()
    vals = []
    for item in rows:
        vals.append(item[0])

    z_scores = heaters.select('temp').rdd.map(lambda x:((x[0] - mean) / std, 1)).toDF()
    print('z_scores df: ', z_scores.show())
    
    # troublesome = filter(lambda x: x > 0.01, z_scores)
    # print('FILTER: ', list(troublesome))

    heaters.show()
    spark_context.stop()

