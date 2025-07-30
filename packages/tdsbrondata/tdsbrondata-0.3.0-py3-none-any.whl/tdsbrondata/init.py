import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tdsbrondata

def modules(notebookutils, spark):
    tdsbrondata._notebookutils = notebookutils
    tdsbrondata._spark = spark
    tdsbrondata._spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "false")
    tdsbrondata._spark.conf.set("spark.sql.parquet.vorder.enabled", "true")
    tdsbrondata._spark.conf.set("spark.microsoft.delta.optimizeWrite.enabled", "true")
    tdsbrondata._spark.conf.set("spark.microsoft.delta.optimizeWrite.binSize", "134217728")
    tdsbrondata._spark.conf.set("spark.databricks.delta.retentionDurationCheck.enabled", "false")

def lakehouse(schemaName, sourceDataMode, sourceDataPeriod):
    tdsbrondata.schemaName = schemaName
    tdsbrondata.schemaNameBronze = schemaName.replace('S', 'B')
    tdsbrondata.schemaNameSilver = schemaName.replace('B', 'S')
    tdsbrondata.sourceDataMode = sourceDataMode
    tdsbrondata.sourceDataPeriod = sourceDataPeriod
    tdsbrondata.workspaceName = workspaceName = tdsbrondata._spark.conf.get("trident.workspace.name", "")
    tdsbrondata.lakehouseName = lakehouseName = tdsbrondata._spark.conf.get("trident.lakehouse.name", "")
    tdsbrondata._spark.sql(f"USE database {lakehouseName}.{schemaName}")
    tdsbrondata.automaticDataPath = f"abfss://{workspaceName}@onelake.dfs.fabric.microsoft.com/{lakehouseName}.Lakehouse/Files/AutomaticData/{schemaName}/{sourceDataPeriod}"
    tdsbrondata.manualDataPath = f"abfss://{workspaceName}@onelake.dfs.fabric.microsoft.com/{lakehouseName}.Lakehouse/Files/ManualData/{schemaName}"
    tdsbrondata.tablesRootPath = f"abfss://{workspaceName}@onelake.dfs.fabric.microsoft.com/{lakehouseName}.Lakehouse/Tables/{schemaName}"

def keyvault(keyvaultName):
    tdsbrondata.keyvaultName = keyvaultName
    tdsbrondata.keyvaultUrl = f"https://{keyvaultName}.vault.azure.net/"