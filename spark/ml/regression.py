from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.functions import mean as _mean, stddev as _stddev, col

import pyspark


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


# def z_score(x, mean, std):
#     return (x - mean) / std
#
#
# def convert_to_zscore(df):
#     """
#     Converts a DataFrame to z score values.
#     :param df: DataFrame to be converted
#     :return: A DataFrame containing the transformed table.
#     """
#
#     means = {}
#     stds = {}
#
#     for column in df.schema.names[2:]:  # leave out the first two columns
#         df_stats = df.select(
#             _mean(col(column)).alias('mean'),  # Compute mean for column
#             _stddev(col(column)).alias('std')  # Compute std for column
#         ).collect()
#
#         means[column] = df_stats[0]['mean']
#         stds[column] = df_stats[0]['std']
#
#     cols = df.schema.names[2:]  # Needs to be specified here, otherwise references to names not available.
#
#     # RDD used to distribute task
#     transformed = df.rdd.map(lambda x: (x[0],
#                                         x[1],
#                                         z_score(x[2], means[cols[0]], stds[cols[0]]),
#                                         z_score(x[3], means[cols[1]], stds[cols[1]])
#                                         )
#                              ).toDF(df.schema.names)
#
#     return transformed


def compute_coefficients(df, column):
    """
    Computes min and max values for the given DataFrame column
    :param df: DataFrame to be used.
    :param column: String of the column name.
    :return: (min value, max value)
    """
    n = df.select("id").count()

    # Select desired column and filter out all values higher than -1
    df = df.select(col(column)).filter(column + " > -1")

    # -1 values are excluded as these are used as sensor malfunction labeling.
    max_val = df.max(column)
    min_val = df.min(column)

    # Regression
    mean_t = df.mean("t")
    mean_var = df.mean(column)

    SS_tvar = df.withColumn(column + "*t", col(column) * col("t")).sum() - n*mean_var*mean_t
    SS_tt = df.select("t2").sum() - n*mean_t*mean_t

    a = SS_tvar / SS_tt
    b = mean_var - a * mean_t

    print()
    print(column)
    print((a, b, min_val, max_val))
    print()

    return a, b, min_val, max_val


def get_coefficients_for(df):
    """
    Gets the a, b and limit coefficients per parameter column for use in prediction.
    :param df: DataFrame containing the training data.
    :return: List containing tuples (a, b, max, min) with linear regression coefficients and limits.
    """

    n = df.withColumn("t2", col("t")*col("t")).count()

    results = spark_context.parallelize(range(4, len(df.schema.names)))
    results = results.map(
        lambda x: (
            df.schema.names[x],
            compute_coefficients(df, df.schema.names[x])
        )
    )

    return results


if __name__ == '__main__':

    spark_config = SparkConf()
    spark_config.set('spark.cassandra.connection.host', 'cassandra-cluster')

    spark_context = SparkContext(master='spark://spark-master:7077', appName='regression', conf=spark_config)
    sql_context = SQLContext(spark_context)  # needed to be able to query data.

    heaters = load_and_get_table_df('household', 'heaters')
    heaters.show()

    parameters = get_coefficients_for(heaters)

    print()
    print(parameters)
    print()

    # Finish
    spark_context.stop()

