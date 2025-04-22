# Technical Case: Breweries Case – Using Databricks and Azure Data Factory for API Data

## Project Overview
This project implements a data pipeline to consume brewery information from the Open Brewery DB API, process it, and store it in a data lake using the medallion architecture (Bronze, Silver, and Gold layers). The solution uses Azure Databricks for processing with PySpark and Azure Data Factory for data pipeline orchestration.

## Architecture
![alt text](Images/arquitetura_ab_inbev.png)

The solution’s architecture follows the Medallion Architecture model, consisting of three main layers: Bronze, Silver, and Gold. Azure Databricks was chosen as the processing platform, while Azure Data Factory (ADF) handles orchestration. Data is stored in the Databricks File System (DBFS).

## Bronze Layer — Raw Data
Goal: Store raw data retrieved from the API without any transformation, preserving the original format for future analysis.
-	Format: Delta table.
-	Detalhes:
    -	Data extracted from the public Open Brewery DB API with automated pagination.
    -	No transformations are applied at this layer.
    -	Files are stored in DBFS in the Bronze layer.

## Silver Layer — Processed Data
Goal: Clean, normalize, and partition the data to ensure consistency and quality for analysis.
-	Format: Delta table.
-	Transformations Applied:
    -	Removal of irrelevant null fields.
    -	Conversion of data types to a standard format.
    -	Partitioning of data by state and city to facilitate processing and analysis.

## Gold Layer — Aggregated Data
Goal: Generate an analytical layer with aggregated data to provide business insights.
-	Format: Delta table and view.
-	Transformations Applied:
    -	Count of breweries by brewery_type and location (by state and city).


## Orchestration with Azure Data Factory
The pipeline orchestration is handled through Azure Data Factory (ADF), using a pipeline with the following main activities:
ADF Pipeline
The pipeline contains three main activities:
1.	Bronze Layer Ingestion:
-	Executes the bronze_extraction.py notebook, which consumes data from the Open Brewery DB API and stores the raw data in the Bronze layer.
  
2.	Transformation from Bronze to Silver:
-	Executes the silver_transformation.py notebook, which performs data cleaning and normalization, and partitions it by state and city.
  
3.	Aggregation from Silver to Gold:
-	Executes the gold_aggregation.py notebook, which generates aggregations by brewery_type, state, and city, and stores the result in the Gold layer as both a Delta table and a view.

## Flow Control and Error Handling
-	Flow control: The pipeline is configured to ensure that activities run in the correct order.
-	Automatic retries: Activities have automatic retry settings in case of failure, ensuring the robustness of the process.
-	Alerts: In case of failure, email alerts are sent via Azure Monitor integration, ensuring visibility of issues.
## Execution Trigger
-	The pipeline is scheduled to run daily at 08:00 AM (or on-demand as needed).

![alt text](Images/agendamento_adf.png)

## Databricks Notebooks
bronze_extraction.py
-	Goal: Consume data from the Open Brewery DB public API and store it in the Bronze layer.
-   Features:
    -	Handles automatic pagination to ensure all records are retrieved.
    -	Stores raw data in Delta table format in the Bronze layer path of Unity Catalog.
![alt text](Images/qtd_registros_api.png)

silver_transformation.py
-	Goal: Transform data from the Bronze to the Silver layer, cleaning and normalizing it.
-	Features:
    -	Reads data from the Bronze layer stored in Delta table format.
    -	Applies cleaning (removal of irrelevant null values), normalization (standardization of data types), and partitioning (by state and city).
    -	he data is then written back into a partitioned Delta table.
![alt text](Images/particionamento_silver.png)

![alt text](Images/particionamento_silver2.png)

gold_aggregation.py
-	Goal: Aggregate data from the Silver layer to provide analytical insights in the Gold layer.
-	Features:
    -	Reads data from the Silver layer.
    -	Applies aggregations such as count of breweries by type (brewery_type) and location (state and city).
    -	Stores results in the Gold layer as a Delta table and a view, making it easier for stakeholders to query.
![alt text](Images/view_gold.png)

After executing the notebooks, we will have a Databricks Data Catalog similar to the image below:
![alt text](Images/catalago.png)

## Monitoring and Alerts
To ensure data integrity and proper pipeline execution, monitoring and alerting processes were implemented
Monitoring via Azure Data Factory (ADF)
-	Automatic retries: In case of activity failures, ADF is configured to retry automatically, minimizing interruptions.
-	Failure alerts: Through Azure Monitor integration, alerts are sent to a configured email group whenever a pipeline failure occurs.
Data Validations
-	Minimum record count check per layer: Each pipeline layer (Bronze, Silver, and Gold) includes a validation to ensure processed data is not empty or below expected thresholds.
-	Expected schema check: Before moving to the next layers, a validation process ensures that data is in the correct format and schema.
-	Data consistency: Consistency checks are performed to ensure that data has not been corrupted during ingestion or transformations.

## Final Considerations
This data pipeline was designed to be scalable and resilient, applying best practices in data engineering on the Azure platform. It can be easily extended to include new data sources or additional transformations as needed. The use of Azure Databricks and Azure Data Factory ensures not only performance and flexibility, but also effective control and monitoring of each step of the process.

Some steps in this process could not be implemented due to restrictions in the available development account. However, parallel mechanisms were developed to enable testing and validation of the data extraction, processing, and storage procedures.

