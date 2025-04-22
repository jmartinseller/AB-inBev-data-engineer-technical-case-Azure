# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql.functions import count

# Caminhos
silver_path = "abfss://<seu-container>@<sua-conta>.dfs.core.windows.net/silver/"
gold_path = "abfss://<seu-container>@<sua-conta>.dfs.core.windows.net/gold/"

spark = SparkSession.builder.getOrCreate()
df_silver = spark.read.parquet(silver_path)

# Agregação: contagem por tipo e estado
df_agg = df_silver.groupBy("brewery_type", "state").agg(count("*").alias("brewery_count"))
df_agg.write.mode("overwrite").parquet(gold_path)
