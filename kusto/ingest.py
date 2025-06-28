import os
import io
from azure.kusto.data import KustoConnectionStringBuilder
from azure.kusto.data.data_format import DataFormat
from azure.kusto.ingest import (
    IngestionProperties,
    KustoStreamingIngestClient,
    ManagedStreamingIngestClient,
    IngestionStatus,
    QueuedIngestClient
)

from dotenv import load_dotenv

load_dotenv()
# get ADX Azure AD app credentials from env file
clusterPath = os.getenv("CLUSTER_PATH")
appId = os.getenv("APP_ID")
appKey = os.getenv("APP_KEY")
appTenant = os.getenv("APP_TENANT")
dbName = os.getenv("DB_NAME")


ingest_total=0

csb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
    clusterPath,
    appId,
    appKey,
    appTenant
)

client = KustoStreamingIngestClient (csb)#KustoStreamingIngestClient (csb) # ManagedStreamingIngestClient.from_engine_kcsb(csb) #QueuedIngestClient(dmb)

ingestionProperties = IngestionProperties(
    database=dbName,
    table="",
    data_format=DataFormat.CSV
    #,flush_immediately=True
)

def ingest_kusto(t_name, data):
    global ingest_total
    ingestionProperties.table=t_name
    str_stream = io.StringIO(data)
    try:
        res = client.ingest_from_stream(str_stream, ingestion_properties=ingestionProperties)
        ingest_total += 1
        print(ingest_total)
        #print(res.status)
    except Exception as e:
        print(e)
        pass
