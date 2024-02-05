import streamlit as st
import json
import io
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
import uuid
from uuid import UUID
from qdrant_client import QdrantClient, models 
import openai
from pathlib import Path
import pandas as pd
from st_files_connection import FilesConnection
import logging
from google.cloud import storage


api_key = st.secrets["QDRANT_API_KEY_2"]
openai.api_key = st.secrets["OPENAI_API_KEY"]

client = QdrantClient("https://1be15a39-6a90-4270-b4fe-09cdf7a01d22.us-east4-0.gcp.cloud.qdrant.io",
                    prefer_grpc=True,
                    api_key=api_key,
                    )


now_utc = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")



def read_markdown_file(markdown_file):
    """read in a markdown file for display in streamlit"""
    return Path(markdown_file).read_text()



# Custom JSON encoder that converts UUIDs to strings
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)



def append_to_gcs_file(data_object, gcs_file_name):
    '''Example usage
    append_to_gcs_file(session, 'sessions.csv')
    '''
    data_object_dict = data_object.dict(by_alias=True)
    df = pd.json_normalize(data_object_dict, sep='_')
    storage_client = storage.Client.from_service_account_info(st.secrets["gcs_connections"])
    bucket = storage_client.get_bucket('streamlit-data-bucket')
    blob = bucket.blob('intent/' + gcs_file_name)
    blob_data = blob.download_as_text()
    existing_df = pd.read_csv(io.StringIO(blob_data))
    updated_df = pd.concat([existing_df, df], ignore_index=True)
    updated_csv = updated_df.to_csv(index=False)
    blob.upload_from_string(updated_csv, content_type='text/csv')





def query(question, response_file):
    """read in the json file as source data for the QA (this is temporary as we're building)"""
    with open(response_file, encoding='utf-8') as f:
        data = json.load(f)
        messages =  [  
            {'role':'system', 
            'content': "You are a helpful assistant. Try to answer the users question based on the info in the INTENTs provided. You can supplement your response with your own information, but if you do please let user know what information you added. If you don't know the answer to something, just say I don't know."},    
            {'role':'user', 
            'content': f"""{question}```{data}```"""}  
        ] 
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",  #gpt-4
            messages=messages,
            temperature=0.8, # 0-2. Controls response randomness vs determinism. Higher is more random 
            max_tokens=8000,
        )
        return response.choices[0].message["content"]
