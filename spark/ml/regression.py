import os

from pyspark import SparkContext
from pyspark.sql import SQLContext


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


if __name__ == '__main__':
    os.environ['PYSPARK_SUBMIT_ARGS'] = '--master spark://spark-master:7077 ' \
                                        '--packages com.datastax.spark:spark-cassandra-connector_2.11:2.4.2 ' \
                                        '--conf spark.cassandra.connection.host=cassandra-cluster:9042'

    spark_context = SparkContext(appName='regression')  # spark-master, appName
    sql_context = SQLContext(spark_context)  # needed to be able to query data.

    heaters = load_and_get_table_df('household', 'heatersensor')

    heaters.show()
    spark_context.stop()
