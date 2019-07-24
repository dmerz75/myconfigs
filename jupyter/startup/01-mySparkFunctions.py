import os
from pyspark.sql import SparkSession
from IPython.display import display, HTML

print("Loading My Spark Functions.")
# print(dir(spark))

def read_df(spark, path):
    lst = [os.path.splitext(x)[1] for x in os.listdir(path)]
    # print(lst)

    if ".csv" in lst:
        format_in = "csv"
    else:
        format_in = "parquet"
    # return
    if format_in == "parquet":
        print("df = spark.read.parquet(path)")
        df = spark.read.parquet(path)
    else:
        csv_code = """df = spark.read.format("csv") \
    .option("header", True) \
    .option("inferSchema", True) \
    .load(path)"""
        print(csv_code)

        df = spark.read.format("csv") \
            .option("header", True) \
            .option("inferSchema", True) \
            .load(path)
    df.printSchema()
    print(df.count())
    return df


readDF = read_df
readdf = read_df
ReadDF = read_df

def column_comparison(df1,df2):
    '''
    Get the column names present in both dataframes.
    :param df1: first dataframe
    :param df2: second dataframe
    '''
    df1_cols = df1.columns
    df2_cols = df2.columns
    only1_cols = set(df1_cols) - set(df2_cols)
    only2_cols = set(df2_cols) - set(df1_cols)
    common = list(set(df1_cols).intersection(set(df2_cols)))
    print("Unique to df1:\n\t",only1_cols)
    print("Unique to df2:\n\t",only2_cols)
    print("Members in both:\n\t",common)
    return common


def view(df, x=4):
    print("df.limit(4).toPandas()")
    df1 = df.limit(x)
    HTML(df1.toPandas().to_html())
    # print(HTML(df1.toPandas().to_html()))
    display(HTML(df1.toPandas().to_html()))
