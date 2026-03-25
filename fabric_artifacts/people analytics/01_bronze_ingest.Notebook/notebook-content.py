# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "b94d792f-0f2a-42b5-81e8-b4582c606795",
# META       "default_lakehouse_name": "people_analytics_lakehouse",
# META       "default_lakehouse_workspace_id": "aca4b91c-3a43-4f0a-b169-85f40788c6e7",
# META       "known_lakehouses": [
# META         {
# META           "id": "b94d792f-0f2a-42b5-81e8-b4582c606795"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# ### Read the CSV from Lakehouse Files

# CELL ********************

# Read raw CSV from Lakehouse Files into a Spark DataFrame

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

# Define file path
CSV_PATH = 'Files/raw_uploads/WA_Fn-UseC_-HR-Employee-Attrition.csv'

# Read CSV with head and infer schema
df_raw = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(CSV_PATH)

print(f"Rows loaded: {df_raw.count()}")
print(f"Columns: {len(df_raw.columns)}")
df_raw.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Normalize Column Names

# CELL ********************

# Normalize column names to lowercase snake_case
# This prevents downstream SQL issues with mixed-case column names

import re

def normalize_col_name(col: str) -> str:
    # lowercase, replace spaces and special characters with underscore
    col = col.strip().lower()
    col = re.sub(r'[^a-z0-9]+', '_', col)
    col = col.strip('_')
    return col 

# Rename all columns
renamed_cols = [normalize_col_name(c) for c in df_raw.columns]
df_normalized = df_raw.toDF(*renamed_cols)

# Add a metadata column - ingested timestamp
df_bronze = df_normalized.withColumn("_ingested_at", current_timestamp())

print("Normalized column names:")
print(df_bronze.columns)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Write to Bronze Delta Table

# CELL ********************

# Write the DataFrame to Bronze Delta Table
# Using overwrite mode so this is idempotent 

TABLE_NAME = "bronze_hr_attrition"

df_bronze.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(TABLE_NAME)

print(f"Written to delta table: {TABLE_NAME}")
print(f"Row count: {spark.table(TABLE_NAME).count()}")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Data quality validation

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
