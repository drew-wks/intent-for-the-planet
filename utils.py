import streamlit as st
import json
import os
from datetime import datetime
import uuid
from uuid import UUID
from qdrant_client import QdrantClient, models 
import openai
from pathlib import Path
import pandas as pd
from st_files_connection import FilesConnection


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




import pandas as pd
from google.cloud import storage
from pydantic import BaseModel
import uuid
from typing import List


# Custom JSON encoder that converts UUIDs to strings
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
    

def session_to_csv(file_name: str):
    session = st.session_state['session']
    # Convert the session object to a dictionary and then to JSON
    session_dict = session.dict()
    session_json = json.dumps(session_dict, cls=JSONEncoder)
    
    # Normalize JSON data into a DataFrame
    df = pd.json_normalize(json.loads(session_json), sep='_')

    # Read existing CSV file from Google Cloud Storage
    conn = st.connection('gcs', type=FilesConnection)
    sessions_df = conn.read("streamlit-data-bucket/intent/" + file_name, input_format="csv", ttl=600)

    # Append new data to the DataFrame
    updated_sessions_df = sessions_df.append(df, ignore_index=True)

    # Convert updated DataFrame to CSV format
    updated_sessions_csv = updated_sessions_df.to_csv(index=False)

    # Write the CSV data back to Google Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('streamlit-data-bucket')
    blob = bucket.blob('intent/' + file_name)
    blob.upload_from_string(updated_sessions_csv, content_type='text/csv')



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
