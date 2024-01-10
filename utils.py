import streamlit as st
import json
import os
from datetime import datetime
import uuid
from qdrant_client import QdrantClient, models 
import openai
from pathlib import Path



client = QdrantClient(https://1be15a39-6a90-4270-b4fe-09cdf7a01d22.us-east4-0.gcp.cloud.qdrant.io,
                      prefer_grpc=True,
                      api_key=api_key,
                      )


now_utc = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")



def read_markdown_file(markdown_file):
   return Path(markdown_file).read_text()


openai.api_key = st.secrets["OPENAI_API_KEY"]


def query(question, response_file):
    with open(response_file) as f:
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
