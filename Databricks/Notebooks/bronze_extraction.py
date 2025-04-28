# Databricks notebook source
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from datetime import datetime

# Inicializa sessão Spark
spark = SparkSession.builder.appName("case_API").getOrCreate()

#URL Base e limites
base_url = "https://api.openbrewerydb.org/v1/breweries"
per_page = 200
page = 1
all_data = []

# Loop de coleta paginada
while True:
    print(f"Buscando página {page}...")
    response = requests.get(f"{base_url}?page={page}&per_page={per_page}")
    
    if response.status_code != 200:
        print(f"Erro na requisição: {response.status_code}")
        break

    data = response.json()
    
    if not data:
        print("Fim da coleta.")
        break

    all_data.extend(data)
    page += 1


# Criação do DataFrame e salvamento
if all_data:
    # Cria DataFrame diretamente da lista de dicionários
    df = spark.createDataFrame(all_data)

    # Adiciona coluna com data de extração
    df = df.withColumn("extraction_date", lit(datetime.today().strftime('%Y-%m-%d')))

    # Caminho do Azure Data Lake ou Blob Storage
    #output_path = "abfss://brewery-data@brewerydatalakes.dfs.core.windows.net/bronze/"

    # Escreve no Data Lake em formato JSON
    #df.write.mode("overwrite").json(output_path) brewery_adf_v2.default
    # Write transformed data back to a different table
    df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("brewery_adf_v2.bronze.raw_data")

    print(f"Dados salvos com sucesso")
else:
    print("Nenhum dado coletado.")
