# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Caminhos
bronze_path = "abfss://<seu-container>@<sua-conta>.dfs.core.windows.net/bronze/"
silver_path = "abfss://<seu-container>@<sua-conta>.dfs.core.windows.net/silver/"

spark = SparkSession.builder.getOrCreate()
df_raw = spark.read.json(bronze_path)

# Limpeza e normalização
df_clean = df_raw.select(
    "id", "name", "brewery_type", "city", "state", "country", "website_url"
).dropna(subset=["id", "name", "state"])

# Particiona por estado
df_clean.write.mode("overwrite").partitionBy("state").parquet(silver_path)
