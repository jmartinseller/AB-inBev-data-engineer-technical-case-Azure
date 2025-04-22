# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql.functions import count, col

spark = SparkSession.builder \
    .appName("AgregacaoCervejarias") \
    .getOrCreate()
    
    
# Ler os dados da tabela Delta silve
df_cervejarias = spark.read.table("brewery_adf_v2.silver.silver_data")

# criar a agregações
df_agregado = df_cervejarias.groupBy("brewery_type", "state", "city") \
    .agg(count("*").alias("quantidade_cervejarias")) \
    .orderBy(col("quantidade_cervejarias").desc(), "state", "city")
    
# salvando tabela Delta gold
df_agregado.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("brewery_adf_v2.gold.gold_data")
    
#Criar uma view SQL para tabela gold
spark.sql('''
CREATE OR REPLACE VIEW brewery_adf_v2.gold.vw_cervejarias AS
SELECT 
    brewery_type as tipo_cervejaria,
    state as estado,
    city as cidade,
    quantidade_cervejarias
FROM brewery_adf_v2.gold.gold_data
''')