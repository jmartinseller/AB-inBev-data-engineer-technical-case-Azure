# Databricks notebook source
import requests
from datetime import datetime
from pyspark.sql import SparkSession
import json

# Define o caminho de destino
storage_path = "abfss://<seu-container>@<sua-conta>.dfs.core.windows.net/bronze/"

# Requisição à API
url = "https://api.openbrewerydb.org/breweries"
response = requests.get(url)
data = response.json()

# Salva o JSON como um arquivo temporário
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"brewery_raw_{now}.json"
json_path = f"/tmp/{file_name}"

with open(json_path, 'w') as f:
    json.dump(data, f)

# Lê no Spark e escreve no Data Lake
spark = SparkSession.builder.getOrCreate()
df = spark.read.option("multiline", "true").json(json_path)
df.write.mode("overwrite").json(f"{storage_path}{file_name}")
