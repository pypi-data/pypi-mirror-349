from datetime import datetime
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.functions import col, lit, sha2, concat_ws
from pyspark.sql.types import StructType, ArrayType

def Stage(spark: SparkSession, input_path: str, output_path: str, metadata: dict) -> None:
    """
    Чтение parquet с S3, преобразование сложных типов, обогащение метаданными, запись обратно.
    """
    df = spark.read.parquet(input_path)

    def convert_to_string(column_name, column_type):
        if isinstance(column_type, StructType):
            return F.concat_ws(",", *[F.col(f"{column_name}.{field.name}") for field in column_type])
        elif isinstance(column_type, ArrayType):
            return F.concat_ws(",", F.col(column_name))
        else:
            return F.col(column_name)

    for column in df.columns:
        column_type = df.schema[column].dataType
        df = df.withColumn(column, convert_to_string(column, column_type))

    enriched_df = df
    
    if 'derived_columns' in metadata:
        for column_name, column_value in metadata['derived_columns'].items():
            if isinstance(column_value, str) and column_value.startswith("!"):
                enriched_df = enriched_df.withColumn(column_name, F.lit(column_value[1:]))
            else:
                enriched_df = enriched_df.withColumn(column_name, F.expr(column_value))
    if 'hashed_columns' in metadata:
        for column_name, columns in metadata['hashed_columns'].items():
            enriched_df = enriched_df.withColumn(column_name, F.hash(*columns))
    if 'hashdiff_columns' in metadata:
        for column_name, columns in metadata['hashdiff_columns'].items():
            enriched_df = enriched_df.withColumn(column_name, F.sha2(F.concat_ws("", *columns), 256)) 
    if 'date_columns' in metadata:
        for column_name, column_value in metadata['date_columns'].items():
            enriched_df = enriched_df.withColumn(column_name, F.expr(column_value))

    enriched_df.write.mode("overwrite").parquet(output_path)


def Hub(spark: SparkSession, input_path: str, output_path: str, metadata: dict) -> None:
    """
    Создание Hub таблицы в Data Vault.
    """
    df = spark.read.parquet(input_path)
    
    df = df.withColumn(metadata['src_ldts'], F.current_timestamp())
    df = df.withColumn(metadata['src_source'], F.lit(metadata['src_source_value']))

    hub_columns = [metadata['src_pk']] + metadata['src_nk'] + [metadata['src_ldts'], metadata['src_source']]
    hub_df = df.select(hub_columns)
    
    hub_df.write.mode("overwrite").parquet(output_path)


def Satellite(spark: SparkSession, input_path: str, output_path: str, metadata: dict) -> None:
    """
    Создание Satellite таблицы в Data Vault.
    """
    df = spark.read.parquet(input_path)

    df = df.withColumn(metadata['src_ldts'], F.current_timestamp())
    df = df.withColumn(metadata['src_source'], F.lit(metadata['src_source_value']))
    df = df.withColumn("HASHDIFF", sha2(concat_ws("||", *metadata['src_hashdiff']), 256))

    satellite_columns = [
        metadata['src_pk'],
        "HASHDIFF"
    ] + metadata['src_payload'] + [
        metadata['src_eff'],
        metadata['src_ldts'],
        metadata['src_source']
    ]

    satellite_df = df.select(satellite_columns)

    satellite_df.write.mode("overwrite").parquet(output_path)


def Link(
    spark: SparkSession,
    table_path_1: str,
    table_path_2: str,
    join_key: str,
    columns: dict,
    business_keys_1: list,
    business_keys_2: list,
    save_path: str,
    incremental_key: str = None,
):
    """
    Создание Link таблицы в Data Vault с join по техническому ключу и хэшем бизнес-ключей.
    """
    df1 = spark.read.parquet(table_path_1).alias("df1")
    df2 = spark.read.parquet(table_path_2).alias("df2")

    if incremental_key:
        max_ldts_1 = df1.agg({incremental_key: "max"}).collect()[0][0]
        max_ldts_2 = df2.agg({incremental_key: "max"}).collect()[0][0]
        df1 = df1.filter(col(incremental_key) > lit(max_ldts_1))
        df2 = df2.filter(col(incremental_key) > lit(max_ldts_2))

    df_joined = df1.join(df2, df1[join_key] == df2[join_key], "inner")

    full_bk_expr = [col(f"df1.{k}") for k in business_keys_1] + [col(f"df2.{k}") for k in business_keys_2]
    df_link = df_joined.withColumn(
        columns["src_pk"],
        sha2(concat_ws("||", *full_bk_expr), 256)
    ).select(
        columns["src_pk"],
        *[col(f"df1.{k}").alias(k) for k in business_keys_1],
        *[col(f"df2.{k}").alias(k) for k in business_keys_2],
        col(f"df1.{columns['src_ldts']}").alias("LOAD_DATETIME"),
        col(f"df1.{columns['src_source']}").alias("SOURCE"),
        lit(datetime.now().date()).alias("LOAD_DATE")
    ).dropDuplicates()

    df_link.write.mode("overwrite").parquet(save_path)

    return df_link
