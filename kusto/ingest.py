import os
import io
from azure.kusto.data import KustoConnectionStringBuilder
from azure.kusto.data.data_format import DataFormat
from azure.kusto.ingest import IngestionProperties, KustoStreamingIngestClient
from azure.identity import DefaultAzureCredential


clusterPath = os.getenv("CLUSTER_PATH")
dbName = os.getenv("DB_NAME")

credential = DefaultAzureCredential()
csb = KustoConnectionStringBuilder.with_azure_token_credential(clusterPath, credential)
client = KustoStreamingIngestClient(csb)

ingestionProperties = IngestionProperties(
    database=dbName,
    table="",
    data_format=DataFormat.CSV
    #,flush_immediately=True
)

ingest_total=0

def ingest_kusto(t_name, data):
    global ingest_total
    ingestionProperties.table=t_name
    str_stream = io.StringIO(data)
    try:
        res = client.ingest_from_stream(str_stream, ingestion_properties=ingestionProperties)
        ingest_total += 1
        print(ingest_total)
    except Exception as e:
        print(e)
        pass
