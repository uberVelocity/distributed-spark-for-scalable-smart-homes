from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import functions as F
from pyspark.sql.functions import col

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

    # Filter out all values in column higher than -1
    df = df.select(col("t"), col(column)).where(column + " > -1")
    n = df.select("t").count()

    # Compute required statistics
    df_stats = df.select(
        F.mean(col(column)).alias('mean_' + column),
        F.mean(col("t")).alias('mean_t'),
        F.max(col(column)).alias('max_' + column),
        F.min(col(column)).alias('min_' + column),
        F.sum(col(column) * col("t")).alias("sum(" + column + "*t)"),
        F.sum(col("t") * col("t")).alias("sum(t^2)")
    ).collect()[0]

    # Regression
    mean_t = df_stats['mean_t']
    mean_var = df_stats['mean_' + column]

    SS_tvar = df_stats["sum(" + column + "*t)"] - n*mean_var*mean_t
    SS_tt = df_stats["sum(t^2)"] - n*mean_t*mean_t

    a = SS_tvar / SS_tt
    b = mean_var - a * mean_t

    # print()
    # print("Summary of " + str(column))
    # print((a, b, df_stats['min_' + column], df_stats['max_' + column]))
    # print(flush=True)

    return df_stats['min_' + column], df_stats['min_' + column], a, b


def get_coefficients_for(df):
    """
    Gets the a, b and limit coefficients per parameter column for use in prediction.
    :param df: DataFrame containing the training data.
    :return: List containing tuples (a, b, max, min) with linear regression coefficients and limits.
    """

    results = []
    for column in df.schema.names[4:]:
        results.append((column, compute_coefficients(df, column)))

    return results


if __name__ == '__main__':

    models = ['heaters']

    spark_config = SparkConf()
    spark_config.set('spark.cassandra.connection.host', 'cassandra-cluster')

    spark_context = SparkContext(master='spark://spark-master:7077', appName='regression', conf=spark_config)
    sql_context = SQLContext(spark_context)  # needed to be able to query data.

    for model in models:
        df = load_and_get_table_df('household', model)
        coefficients = get_coefficients_for(df)

    # Finish
    spark_context.stop()

