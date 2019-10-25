import tensorflow as tf
from google.cloud import bigquery, bigquery_storage_v1beta1
from google import auth
import os
import json 


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'bigquery.json'
bqstorageclient = bigquery_storage_v1beta1.BigQueryStorageClient()

client = bigquery.Client()
string = """
    Select  * from dota.dota_mini
"""


query_job = client.query(string)


results = query_job.result().to_dataframe()
print(results)



