# Databricks notebook source
from pyspark.sql import functions as F

# Leitura dos dados Parquet raw
df_raw = spark.read.table("brewery_adf_v2.bronze.raw_data")

# Transformações:
# remoção de registros com dados nulos nas colunas chaves para o projeto (como nome, cidade, estado)
df_cleaned = df_raw.dropna(subset=["name", "city", "state"])

# criação de uma coluna de localização concatenando a cidade e o estado
df_transformed = df_cleaned.withColumn("location", F.concat_ws(", ", F.col("city"), F.col("state")))

# transfomrnado latitude e longitude em floats
df_transformed = df_transformed.withColumn("latitude", F.col("latitude").cast("float")) \
                               .withColumn("longitude", F.col("longitude").cast("float"))
                               
# Armazenamento em Delta particionado por cidade e estado
df_transformed.write \
    .partitionBy("city", "state") \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("brewery_adf_v2.silver.silver_data")